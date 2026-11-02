![image](uploads/121317/28c7c0e8-7bd3-4bd9-be9a-054258e18be7/image.png)

# 概述

## 编写目的

- 编写高效的SQL语句和使用合适的方式创建表和索引，以达到系统在不断更新和升级时仍能保持良好的稳定性。
- 增强SQL可维护性。

## 适用范围

适用于Postgresql V12.x及以上版本。

## 角色和职责

**开发人员**：负责按照规范进行SQL编码

**运维人员**：负责根据规范编写运维需要的SQL

# SQL开发规范

## 索引使用规范

【**${\color{red}强制}$**】SQL语句禁止使用非同类型的列进行等值查询，并且不要做类型转换。（人工检查）

**注：** 字段类型不同会造成隐式转换，导致索引失效。

【**${\color{red}强制}$**】普通索引列作为查询条件时，不允许对索引列进行计算；表达式索引使用时需要与建立索引的表达式保持一致。（人工检查）

【**${\color{red}强制}$**】对于复合索引，SQL语句的where查询条件必须有使用索引的第一列，复合列数量推荐不超过3个。（人工检查）

【**${\color{red}强制}$**】表结构中字段定义的数据类型与应用程序中的定义保持一致，避免报错或无法使用索引的情况发生。（人工检查）

【**${\color{red}强制}$**】创建索引时加concurrently关键字，就可以并行创建（会有额外的资源消耗），不会堵塞DML操作，否则会堵塞DML操作。（人工检查）

例如：

```sql
create index concurrently idx on tbl(id);
```

【**${\color{green}建议}$**】在创建索引时，可以使用TABLESPACE子句指定索引存储在单独的表空间中，这样可以将索引和表数据分开存储，有助于性能优化。

【**${\color{green}建议}$**】创建主键约束会自动创建一个唯一索引，唯一索引可以确保索引列的值唯一，由于在PostgreSQL中，不同的NULL值被视为不相等，因此唯一索引列允许包含多个NULL值（PG支持NULL值索引（`CREATE INDEX ... NULLS NOT DISTINCT`），但需评估必要性。）。

【**${\color{green}建议}$**】对查询进行优化，应尽量避免全表扫描，首先应考虑在 where 及 order by 涉及的列上建立索引。

**注：** 使用explain可以查看执行计划，如果发现执行计划不优，可以通过索引或者调整查询的写法来解决。

```sql
begin;

explain (verbose,costs,timing,buffers,analyze) SQL语句;

rollback;
```

【**${\color{green}建议}$**】对where中含多个字段条件的高频查询，结合数据分布情况，创建多个字段的联合索引，联合索引区分度高的列需要放到前面。

【**${\color{green}建议}$**】创建索引时使用INCLUDE子句允许在索引中包含非键列，这些列不会作为索引键，但可以用于索引扫描，在索引扫描时可以直接从索引中获取这些列的值，避免回表。

【**${\color{green}建议}$**】对于值与堆表的存储顺序线性相关的数据，如果通常的查询为范围查询，建议使用BRIN（Block Range Index）索引。例如流式数据，时间字段或自增字段，可以使用BRIN索引，减少索引的大小，加快数据插入速度：

```sql
create index idx on tbl using brin(id);
```

BRIN（Block Range Index）索引存储连续数据块的范围摘要，适合非常大的表，且数据按时间顺序插入的情况。它占用空间小，但不适合频繁更新或无序的数据。

【**${\color{green}建议}$**】当业务有近邻查询的需求时，推荐对字段建立GIST或SP-GIST索引，加速近邻查询的需求。

例如：

```sql
create index idx on tbl using gist(col);  
select * from tbl order by col <-> '(0,100)';  

-- 使用范围类型存储IP地址段，使用包含的GIST索引检索，性能比两个字段的between and提升20多倍：
create table ip_address_pool_3 (  
  id serial8 primary key ,  
  start_ip inet not null ,  
  end_ip inet not null ,  
  province varchar(128) not null ,  
  city varchar(128) not null ,  
  region_name varchar(128) not null ,  
  company_name varchar(128) not null ,  
  ip_decimal_segment int8range  
) ;  
  
create index ip_address_pool_3_range on ip_address_pool_3 using gist (ip_decimal_segment);  
  
select province,ip_decimal_segment  from ip_address_pool_3 where ip_decimal_segment @> :ip::int8;
```

【**${\color{green}建议}$**】对于固定条件的查询，可以使用部分索引，减少索引的大小，同时提升查询效率，例如：

```sql
select * from tbl where id=1 and col=?; -- 其中id=1为固定的条件  
create index idx on tbl (col) where id=1;
```

【**${\color{green}建议}$**】对于经常使用表达式作为查询条件的语句，可以使用表达式或函数索引加速查询，例如：

```sql
select * from tbl where exp(xxx);  
create index idx on tbl ( exp );
```

【**${\color{green}建议}$**】当用户有prefix或者 suffix的模糊查询需求时，可以使用索引，或反转索引达到提速的需求，例如：

```sql
select * from tbl where col ~ '^abc';  -- 前缀查询
create index idx on tbl(reverse(col)) -- 创建反转函数索引
select * from tbl where reverse(col) ~ '^def';  -- 后缀查询使用反转函数索引
```

【**${\color{green}建议}$**】当用户有规则表达式查询，或者文本近似度查询的需求时，建议对字段使用trgm的gin索引，提升近似度匹配或规则表达式匹配的查询效率，同时覆盖了前后模糊的查询需求。如果没有创建trgm gin索引，则不推荐使用前后模糊查询例如like %xxxx%。

```sql
create index idx_tab_colname on 表名 using gin(colname gin_trgm_ops);
```

【**${\color{green}建议}$**】对于全文搜索场景，推荐通过对字段建立GIN索引或者GIST索引进行优化，对于中文模糊查询场景，推荐安装zhparser中文分词插件进行优化：
1、下载zhparser源码并进行编译；

2、登陆pg控制台使用 `CREATE EXTENSION zhparser`启用插件；

3、添加分词配置：

```sql
create text search configuration parser_name (parser = zhparser); // 添加配置
alter text search configuration parser_name add mapping for n,v,a,i,e,l,j with simple; // 设置分词规则 （n 名词 v 动词等）
```

4、给某一列的分词结果添加 gin 索引 `create index idx_name on table using gin(to_tsvector('parser_name', field));`

5、根据实际情况在 `postgresql.conf`添加配置：

```markdown
zhparser.multi_short = true #短词复合: 1
zhparser.multi_duality = true  #散字二元复合: 2
zhparser.multi_zmain = true  #重要单字复合: 4
zhparser.multi_zall = false  #全部单字复合: 8
```

参考链接：[https://developer.aliyun.com/article/7730](https://developer.aliyun.com/article/7730)

【**${\color{green}建议}$**】当数据被大量更新或删除后，索引可能会产生碎片，导致性能下降，此时应该重建索引（此外，重建索引可以解决索引膨胀问题，可以考虑定期进行重建）。PostgreSQL提供了REINDEX命令来重建索引，不需要停止数据库，但是重建期间会进行锁表，生产环境执行需谨慎。

【**${\color{green}建议}$**】对象文本类型可以考虑用JSONB字段类型进行存储，PostgreSQL 支持 `JSON` 和 `JSONB` 两种 JSON 类型：
- **`JSON`**：存储为 **纯文本**，查询时需要解析，效率较低。
- **`JSONB`**：存储为 **二进制格式**，支持索引，查询性能更好。（推荐）

查询JSON中的某个key值：

```sql
-- -> 返回 JSON 类型
SELECT params->'name' FROM demo_json;

-- ->> 返回 TEXT 类型
SELECT params->>'name' FROM demo_json;

-- 查询 JSON 数组中的元素，返回第一个元素
SELECT params->'skills'->0 FROM demo_json;
```

条件查询：

```sql
-- 查询 JSON 中包含某个值
SELECT * FROM demo_json WHERE params->>'name' = 'Alice';

-- 查询 JSON 数字值
SELECT * FROM demo_json WHERE (params->>'age')::INT > 25;

-- 查询 JSON 布尔值
SELECT * FROM demo_json WHERE (params->>'is_active')::BOOLEAN = true;

-- 查询 JSON 中 null 值
SELECT * FROM demo_json WHERE params->>'salary' IS NULL;
```

`JSON`字段类型本身不支持索引，必须用 **表达式索引** 才能加速查询：

```sql
CREATE INDEX idx_json_name ON demo_json ((params->>'name'));
```

`JSON`独有的高级查询：

```sql
-- 使用 @> 进行 JSONB 包含查询: 查询 params 是否包含 {"age": 25}
SELECT * FROM demo_jsonb WHERE params @> '{"age": 25}';

-- 查询 JSONB 数组是否包含某个值
SELECT * FROM demo_jsonb WHERE params->'skills' ? 'Java';

-- 查询 JSONB 数组是否包含至少值
SELECT * FROM demo_jsonb WHERE params->'skills' ?| array['Java', 'Python'];

-- 查询 JSONB 数组是否包含所有值
SELECT * FROM demo_jsonb WHERE params->'skills' ?& array['Java', 'SQL'];

-- 更新 JSONB 的某个key值
UPDATE demo_jsonb 
SET params = jsonb_set(params, '{age}', '40') 
WHERE params->>'name' = 'Alice';
```

`JSONB`字段类型支持`BTREE`、`GIN`索引进行加速查询：

```sql
CREATE INDEX idx_jsonb_name ON demo_jsonb USING GIN (params);
```

## SQL规约

### 查询限制

【**${\color{red}强制}$**】当只需要查询一行数据时使用LIMIT 1。（人工检查）

【**${\color{red}强制}$**】对数据库的批量增删改操作，应拆分成多个事务进行操作，每次不超过 5000 条记录。（人工检查）

【**${\color{red}强制}$**】10万数据量以上的大表禁止使用没有where条件的查询（报表等低频场景例外）。（人工检查）

【**${\color{red}强制}$**】查询禁止使用“select *”这样的语句，不要返回用不到的任何字段。会影响优化器对执行计划的选择，也会增加宝贵的硬件资源消耗。另外表结构发生变化也容易出现问题。特别是在程序代码内部。即使需要查询表中的所有列时，也需列出所有的字段名。例外场景：对子查询结果集进行的外层嵌套查询可以用select *（人工检查）

【**${\color{red}强制}$**】分区表查询必须带上分区键作为查询条件。（人工检查）

【**${\color{green}建议}$**】在PostgreSQL中对关键字大小写不敏感，需要使用大写的标志符时，必须要加上双引号，否则会被转为小写。为了提高可读性，建议关键字、表名和列名全部使用小写。

【**${\color{green}建议}$**】表名和列名的别名应该使用有意义的英文单词或缩写，不能包含空格，非必要情况下不要使用拼音或者中文。

【**${\color{green}建议}$**】限制单个事务所操作的数据集大小，单个事务查询结果不超过10000条，批量增删改场景下操作对象不超过5000条。

**注：** 大数据量，过滤条件未加索引，且事先知道结果只有一条记录时使用limit 1，可加快执行效率。

【**${\color{green}建议}$**】避免超长SQL，建议长度不超过4000字符。

**注：** 超长SQL往往导致难以理解，并可能伴随性能隐患。同时，应尽量减少SQL语句复杂度，用简单的SQL完成任务，复杂的业务逻		辑尽量由业务代码来实现。

【**${\color{green}建议}$**】SQL子查询嵌套不宜超过3层

**注：** 禁止使用多层的SQL嵌套，除了分页查询，一般SQL语句建议不超过3层嵌套，过于复杂的SQL可根据业务逻辑拆分为多条SQL来实现。

【**${\color{green}建议}$**】在PostgreSQL中，子查询（Subquery）是一种在另一个查询内部嵌套的查询。根据子查询是否依赖于外部查询的某些行，子查询可以分为两大类：相关子查询（Correlated Subquery）和非相关子查询（Non-Correlated Subquery），相关子查询依赖于外部查询的某些行。换句话说，子查询中的某些条件或计算是基于外部查询的当前行的。例如：

```sql
select name, salary
from employees e
where salary > (select avg(salary) from employees where department_id = e.department_id);
```

相关子查询可能会因为需要多次执行而产生性能问题，尤其是当外部表很大时。优化相关子查询的一种方法是使用临时表、CTE（公用表表达式）或者将子查询重写为 JOIN 操作，这通常可以提高性能。例如，上述相关子查询可以使用以下 JOIN 方法重写：

```sql
select e.name, e.salary
from employees e
join (select department_id, avg(salary) as avg_salary from employees group by department_id) as dept_avg
on e.department_id = dept_avg.department_id
where e.salary > dept_avg.avg_salary;
```

【**${\color{green}建议}$**】尽量避免多表的关联操作，对于join 实例表的总数量控制在3个及以内，表设计中需要注意关联表之间的设计关系，关联字段类型的数据类型必须一致，建议字段名也应一致，并建立索引加速查询。

**注：** 关联表越多，要调度的资源就越多。SQL应尽量简化，查询类语句只查询业务所需的数据，不查询无关数据表。特别关注数据量		巨大的表关联操作，使用不当会引发系统故障。实际场景中遇到此类问题，建议在设计层面提前设计好数据库宽表或者将需关联数据		抽取到ES、数仓等其他存储介质中，应用程序直接对宽表进行查询。

【**${\color{green}建议}$**】尽量减少外层使用order by 和group by 排序操作。

**注：** 大量的排序操作影响系统性能，如必须使用排序操作，要尽量建立在有索引的列上。

【**${\color{green}建议}$**】避免不必要的排序。

**注：** 避免不必要的排序，对查询结果进行排序会大大降低系统性能。应将大多数的排序工作交给应用层去完成。

【**${\color{green}建议}$**】尽量避免在 where 子句中使用!=或<>操作符，否则引擎放弃使用索引而进行全表扫描。

【**${\color{green}建议}$**】避免使用大表做join、group by分组、排序。

【**${\color{green}建议}$**】尽量减少SQL复杂度。

**注：** 用简单SQL完成任务，复杂的逻辑在代码中实现。对一个大结果集做排序，或者求唯一值，都是比较昂贵的计算，占用大量数据		库系统资源，如果业务上有这方面需求，尽量放在业务代码中实现。

### 计数场景

【**${\color{red}强制}$**】在函数中，或程序中，不要使用count(*)判断是否有数据，很慢。 建议的方法是limit 1; （人工检查）

例如：

```sql
select 1 from tbl where xxx limit 1;  
if found -- 存在  
else  -- 不存在
```

【**${\color{green}建议}$**】选取合适的计数方式：

- `count(*)`是统计行数的标准语法，空值会纳入统计；
- `count(col)`统计的是col列中的非空记录数。该列中的null值不会被计入；
- `count(distinct col)` 对col列除重计数，同样忽视空值，即只统计非空不同值的个数；
- `count((col1, col2))`对多列计数，即使待计数的列全为空也会被计数，`(null,null)`有效；
- `count(distinct (col1, col2))`对多列除重计数，即使待计数列全为空也会被计数，`(null,null)`有效；

### 空值场景

【**${\color{green}建议}$**】注意以下各种空值的场景处理

- 【**${\color{red}强制}$**】明确区分零值与空值，空值使用is null进行等值判断，零值使用常规的=运算符进行等值判断。（人工检查）

- 注意空值比较逻辑：任何涉及到空值比较运算结果都是unknown，需要注意unknown参与布尔运算的逻辑：

  · and：`true or unknown`会因为逻辑短路返回 `true`。
  · or：`false and unknown`会因为逻辑短路返回 `false`
  其他情况只要运算对象出现 `unknown`，结果都是 `unknown`。

- 空值与任何值的逻辑判断，其结果都为空值，例如 `null=null`返回结果是 `null`而不是 `true/false`。

- 【**${\color{green}建议}$**】涉及空值与非空值的等值比较，请使用 `is distinct from` 进行比较，保证比较结果非空。（人工检查）

- 注意聚合函数的空值问题，除了count之外的所有聚合函数都会忽略空值输入，因此当输入值全部为空时，结果是NULL，如果聚集函数返回空并不是期望的结果，使用coalesce来设置缺省值。

### 判断是否存在场景

【**${\color{green}建议}$**】IN操作能避免则避免，若使用需评估 `in`后边的集合元素数量控制在 50个之内。

**注：** 可以用`exist`代替 `in`，`exist`在某些场景比 `in`效率高。

```sql
select num from a where num in (select num from b);
-- 用下面的语句替换：
select num from a where exists(select 1 from b where num=a.num)
```

【**${\color{green}建议}$**】使用 `=any(array[1,2,3,4])`代替 `in (1,2,3,4)`，效果更佳

【**${\color{green}建议}$**】尽量不使用 `not in`。

【**${\color{green}建议}$**】使用 `select 1 from tbl where xxx limit 1`判断是否存满足条件的列，要比 `count`快。

【**${\color{green}建议}$**】可以使用 `select exists(select * FROM app.sjqq where xxx limit 1)`将存在性结果转换为布尔值。

### 递归场景

【**${\color{green}建议}$**】树形查询应该使用递归查询，尽量减少数据库的交互或join，例如：

```sql
create table tbl_test  
(  
id    numeric,  
name text,  
pid   numeric                                  default 0  
);  
insert into tbl_test(id,name,pid) values('1','10','0');  
insert into tbl_test(id,name,pid) values('2','11','1');  
insert into tbl_test(id,name,pid) values('3','20','0');  
insert into tbl_test(id,name,pid) values('4','12','1');  
insert into tbl_test(id,name,pid) values('5','121','2');  

-- 从Root往树末梢递归
with recursive t_result as (  
  select * from tbl_test where id=1  
    union all  
  select t2.* from t_result t1 join tbl_test t2 on t1.id=t2.pid  
)  
select * from t_result;  
  
 id | name | pid   
----+------+-----  
  1 | 10   |   0  
  2 | 11   |   1  
  4 | 12   |   1  
  5 | 121  |   2  
(4 rows)  

-- 从末梢往树ROOT递归
with recursive t_result as (  
  select * from tbl_test where id=5  
    union all  
  select t2.* from t_result t1 join tbl_test t2 on t1.pid=t2.id  
)  
select * from t_result;  
  
 id | name | pid   
----+------+-----  
  5 | 121  |   2  
  2 | 11   |   1  
  1 | 10   |   0  
(3 rows)
```

递归查询的注意事项 ：

1、一定要能跳出循环，即循环子句查不到结果为止；

2、树形结构如果有多个值，则会出现查到的结果比实际的多的情况，这个业务上是需要保证不出现重复的。

### 其他场景

【**${\color{red}强制}$**】在代码中写分页查询逻辑时，若count为0应直接返回，避免执行后面的分页语句。 （人工检查）

【**${\color{red}强制}$**】分页查询中的子查询必须要进行order by排序。 （人工检查）

【**${\color{green}建议}$**】在PostgreSQL中，`||`操作符是标准的字符串连接操作符，推荐使用。`concat`函数也可以使用，但`||`更简洁。

【**${\color{green}建议}$**】PostgreSQL提供了丰富的日期时间函数，常见场景使用方法推荐：时区转换（例如`AT TIME ZONE`），`current_date`获取当前日期，now()函数获取当前时间戳，以及对日期和时间进行加减计算：

```sql
-- 这条SQL语句首先将时间值转换为UTC时区，然后再转换回美国纽约的时区
SELECT TIMESTAMP '2023-01-01 08:00:00' AT TIME ZONE 'UTC' AT TIME ZONE 'America/New_York';

-- 获取当前日期，返回格式为：YYYY-MM-DD
select current_date;

-- 获取当前时间戳，返回样例为：2025-07-21 16:00:00.168784 +00:00
select now();
```

【**${\color{green}建议}$**】聚合函数（如`SUM`, `AVG`, `COUNT`等）会忽略NULL值，使用时需要注意。例如，`COUNT(column)`只计算非NULL值。

【**${\color{green}建议}$**】合理选择 `union all`与 `union`。

**注：**` union`会对所产生的结果集进行排序运算，删除重复的记录再返回结果，如果表数据量大的话可能会导致用磁盘进行排序。		`union all`操作只是简单的将两个结果合并后就返回，所以可能存在重复记录。

【**${\color{green}建议}$**】利用`row_number`窗口函数优化超多分页场景，窗口函数不会改变结果集的行数，它只是为每一行计算一个值，基于与当前行相关的行集。

**注：** limit N offset M 。PG是取 M+N行，然后放弃前 M行，返回N行，当 M特别大的时候，效率非常低，要么控制返回的总页数，要		么对超过特定阈值的页数进行 SQL改写。

```sql
-- 普通分页查询写法
select *
from your_table
order by some_column
limit m offset (n - 1) * m;

-- 大分页场景可用以下写法优化：
with numbered_rows as (
select *, row_number() over (order by column_name) as row_num
from your_table
)

select *
from numbered_rows
where row_num between (n - 1) * m + 1 and n * m;
```

【**${\color{green}建议}$**】如果用户需要在插入数据，删除数据，或修改数据后马上拿到插入或被删除或修改后的数据，建议使用 `insert into .. returning ..`; `delete .. returning ..`或 `update .. returning ..`; 语法，减少数据库交互次数。

```sql
insert into test (first_name, last_name, age, salary)
values ('Eve', 'Wilson', 45, 90000.00)
returning id, first_name, last_name, age, salary;
```

【**${\color{green}建议}$**】可以使用`insert into ... select`或者`copy`操作（`copy`导出到文件再导入表，性能比`insert`更好）从另一个表快速批量插入数据，注意批量插入数据时，应该使用事务来包裹。

## 应用程序规约

【**${\color{red}强制}$**】两阶段提交的事务，要及时提交或回滚，否则可能导致数据库膨胀。（人工检查）

【**${\color{red}强制}$**】代码中使用 prepared statement 对象，只传参数，比传递 SQL 语句更高效；一次解析，多次使用；降低SQL 注入概率。（人工检查）

【**${\color{red}强制}$**】事务要简单，尽量避免长事务，长事务可能造成垃圾膨胀或锁争用。特殊场景比如：批量增、删、改或者连续修改单行数据场景下可以考虑开启长事务，其他场景建议单条语句执行完之后立即提交事务。（人工检查）

【**${\color{red}强制}$**】对于高并发的应用场景，务必使用程序的连接池，否则性能会很低下。 如果程序没有连接池，建议在应用层和数据库之间架设连接池，例如使用pgbouncer或者pgpool-II作为连接池。（人工检查）
- 连接池应该设置合适的最大连接数，以防止连接过多，避免超过数据库的最大连接数限制；
- 连接池应该设置最大空闲超时时间，防止连接泄漏；
- 连接池应设置最小连接数避免冷启动，并使用 `SET SESSION` 初始化连接参数；
- 自动提交通常开启（显式事务除外）；

【**${\color{red}强制}$**】禁用默认超级用户，业务角色权限分配应遵循最小权限原则，禁用 `PUBLIC` 默认权限：（人工检查）

```sql
ALTER ROLE postgres RENAME TO <unique_superuser_name>;
ALTER ROLE <unique_superuser_name> WITH NOSUPERUSER; -- 按需降权

REVOKE ALL ON DATABASE mydb FROM PUBLIC;
REVOKE ALL ON SCHEMA public FROM PUBLIC;
```

【**${\color{red}强制}$**】在开发使用PostgreSQL的应用程序时，应用程序应该捕获并处理数据库错误，记录数据库错误信息以便排查问题，并且应该根据错误类型进行相应的处理（如重试、回滚等），禁止将详细的数据库错误信息直接展示给用户，因为这可能暴露敏感信息（如数据库结构等）。（人工检查）

【**${\color{red}强制}$**】应用程序应该设置查询超时（例如使用statement_timeout参数或在应用层设置超时），以避免长时间运行的查询占用资源。（人工检查）

【**${\color{red}强制}$**】禁止在事务中混合读写和DDL操作，DDL在事务中可能导致锁冲突或不可回滚（如TRUNCATE）。（人工检查）

【**${\color{green}建议}$**】微服务架构下，推荐schema名称与服务一一对应，应用内不允许有跨schema的sql操作

【**${\color{green}建议}$**】可以通过以下手段防止SQL注入：
- 使用参数化查询；
- 限制数据库用户权限；
- 使用 prepared statement 预编译对象；

【**${\color{green}建议}$**】并行度使用需谨慎。

**注：** 使用并行需要考虑CPU核数，系统负载等情况，并行执行的SQL会对其它语句的性能产生影响。

【**${\color{green}建议}$**】应该尽量在业务层面避免死锁的产生，例如一个用户的数据，尽量在一个线程内处理，而不要跨线程。

【**${\color{green}建议}$**】应用程序配置文件中的pg连接URL中，可以考虑添加应用名称标识参数，例如：

```xml
ftf.datasource.druid.url=jdbc:postgresql://172.16.108.98:5432/rc_meta_dev?currentSchema=rc_meta_dev&ApplicationName=frankstan
```

可于pg活动实例pg_stat_activity表中体现，便于后期数据库问题排查分析

【**${\color{green}建议}$**】可以考虑于应用框架层面对于sql执行语句添加hint标注，并将sql来源设置进来，便于后续的sql日志采集分析：

例如：

```sql
2025-01-14T17:52:11.378293895+08:00 2025/01/14-17:52:11 DEBUG com.iwhalecloud.oss.product.res.biz.core.context.dal.persistent.itsp.dao.SrvExchangeLogDAO.insertEntity- ==>  Preparing: /**RES:jsdx-rom*/ insert into pm_srv_exchange_log ( exchange_id, interface_code, start_time, end_time, item_id, in_message, out_message, state ) values ( ?, ?, ?, ?, ?, ?, ?, ? )
```

【**${\color{green}建议}$**】建议应用框架层面对于select sql语句统一设置limit数量，最好不超过500条，特殊业务场景做例外处理。

【**${\color{green}建议}$**】大结果集处理推荐使用游标`cursor` + `fetch_size` 参数分批次获取。

【**${\color{green}建议}$**】在客户端应用程序中，应当避免在循环中执行SQL语句，应该尽量使用批量操作。

【**${\color{green}建议}$**】避免频繁创建和删除临时表，以减少系统表资源的消耗，因为创建临时表会产生元数据，频繁创建，元数据可能会出现碎片。

# 最佳实践

## PG执行计划解读

在数据库中，分析和优化SQL的执行，最重要就是解读执行计划，在 PostgreSQL 中，执行计划的获取介绍如下。

![image](uploads/118496/5460235a-94bf-43fe-bad4-7d41de1961db/图片.png)

一个顺序磁盘页面操作的cost值由系统参数seq_page_cost (floating point)参数指定的，由于这个参数默认为1.0，所以我们可以认为一次顺序磁盘页面操作的cost值为1。

常见指标如下：

- Cost

  cost是比较重要的指标,比如例子中的cost=0.00..458.00有两个部分。第一个数字0.00表示启动cost，是执行到返回第一行时需要

  的cost值。第二个数字458.00表示执行整个SQL的cost值。

- Rows

  预测的行数。与实际的行数可能有出入，经常vacuum或者analyze的话，这个值和实际值将更加接近。

- Width

  查询结果的所有字段的总宽度。这个参数并不是关键指标。

- 其他

  - loops：循环的次数。如果一个计划节点在运行过程中，相关参数发生变化，需要重新运行该计划节点。
  - Planning time：计划时间。
  - Execution time：执行时间。

查看执行计划，一般关注消耗值cost和扫描的方式，如走索引或全表扫描。当COST值比较大时需要注意是否有优化的可能，并进一步调试。

表顺序扫描由于是立即可以获得第一行，所以启动cost一般都是0，而如果是排序操作，则需要处理完所有行后才能返回第一行，所以排序操作是需要启动cost的，下表列出了有无需要启动cost的操作：

| **执行计划运算类型** | **操作说明**         | **是否有启动cost** |
| ---------------------- | ---------------------- | -------------------- |
| seq scan             | 顺序扫描表               | 无                 |
| index scan           | 索引扫描（需要访问索引与数据）            | 无                 |
| index only scan    | 索引扫描（只需要访问索引，不需要访问数据，效率最高）            | 有                 |
| bitmap index scan    | 索引扫描（通过建立位图的方式将原来的索引扫描中的随机堆表访问转换成顺序堆表访问）             | 有                 |
| bitmap heap scan     | 索引扫描（一次性将满足条件的索引项全部取出，并在内存中进行排序, 然后根据排序后的索引项访问表数据）             | 有                 |
| subquery scan        | 子查询               | 无                 |
| tid scan             | ctid = 条件          | 无                 |
| function scan        | 函数扫描             | 无                 |
| nested loop          | 循环结合             | 无                 |
| merge join           | 合并结合             | 有                 |
| hash join            | 哈希结合             | 有                 |
| sort                 | 排序                 | 有                 |
| hash                 | 哈希运算             | 有                 |
| result               | 函数扫描和具体表无关 | 无                 |
| unique               | distinct，union      | 有                 |
| limit                | limit,offset         | 有                 |
| aggregate            | count,sum,avg,stddev | 有                 |
| group                | group by             | 有                 |
| append               | union                | 无                 |
| materialize          | 子查询               | 有                 |
| setop                | intercept,except     | 有                 |

explain 子句用于展示和分析执行计划。其语法如下：

```sql
explain [ ( option [, ...] ) ] statement
explain [ analyze ] [ verbose ] statement
where option can be one of:
analyze [ boolean ]
verbose [ boolean ]
costs [ boolean ]
buffers [ boolean ]
format { text | xml | json | yaml }
```

选项含义:

- analyze：执行语句并显示真正的运行时间和其它统计信息，会真正执行SQL语句;
- verbose：显示额外的信息,尤其是计划树中每个节点的字段列表,schema识别表和函数名称。总是打印统计数据中显示的每个触发器的名字;
- costs：包括每个计划节点的启动成本预估和总成本的消耗，也包括行数和行宽度的预估;
- buffers：使用信息，特别包括共享块命中、读、脏和写的次数，本地块命中、读、脏和写，临时块读和写的次数;
- timing：在输出中包含实际启动时间和每个节点花费的时间，重复读系统块在某些系统上会显著的减缓查询的速度，只在analyze也启用的时候使用;
- format：声明输出格式，可以为text、xml、json 或 yaml，默认 text;

最常用的选项是 analyze ，通过这个参数会真正执行SQL，务必谨慎，真正执行SQL可以获得真实的执行计划。explain 只进行执行计划解析，并不真实执行SQL。执行计划解读，自底向上，自右向左。

例如：

```sql
explain select error_code,array_to_string(array_agg(db_version),',') from oracode where error_code='ORA-04031' group by error_code;
QUERY PLAN
----------------------------------------------------------------
GroupAggregate (cost=0.00..17.06 rows=3 width=90)
Group Key: error_code
-> Seq Scan on oracode (cost=0.00..17.00 rows=3 width=116)
Filter: ((error_code)::text = 'ORA-04031'::text)
```

在上述执行计划中，涉及4个关键字：Fiter 指应用限定条件进行记录过滤；Seq Scan 指表扫描，也即全表扫描；Group Key 指分组查询的分组键值；GroupAggregate 指分组聚合结果；

另外一个查询，涉及两个表，总成本是 45.80，对两个表进行了 Nested Loop 的嵌套循环处理：

```sql
explain select a.error_code,array_to_string(array_agg(db_version),',') from oracode a,pgcode where a.error_code='ORA-04031' group by a.error_code;
QUERY PLAN
----------------------------------------------------------------
GroupAggregate (cost=0.00..45.80 rows=3 width=90)
Group Key: a.error_code
-> Nested Loop (cost=0.00..41.26 rows=900 width=116)
-> Seq Scan on pgcode (cost=0.00..13.00 rows=300 width=0)
-> Materialize (cost=0.00..17.02 rows=3 width=116)
-> Seq Scan on oracode a (cost=0.00..17.00 rows=3 width=116)
Filter: ((error_code)::text = 'ORA-04031'::text)
```

可以加analyze 让这个语句真实执行，由于这两个表没有关联条件，也没有索引，所以执行计划是对两个表进行全表扫描，然后 NL ，事实上就是笛卡儿积:

```sql
explain analyze select a.error_code,array_to_string(array_agg(db_version),',') from oracode a,pgcode where a.error_code='ORA-04031' group by a.error_code;
 
QUERY PLAN
------------------------------------------------------------------------------
GroupAggregate (cost=0.00..45.80 rows=3 width=90) (actual time=0.324..0.324 rows=1 loops=1)
Group Key: a.error_code
-> Nested Loop (cost=0.00..41.26 rows=900 width=116) (actual time=0.214..0.224 rows=6 loops=1)
-> Seq Scan on pgcode (cost=0.00..13.00 rows=300 width=0) (actual time=0.086..0.088 rows=3 loops=1)
-> Materialize (cost=0.00..17.02 rows=3 width=116) (actual time=0.036..0.038 rows=2 loops=3)
-> Seq Scan on oracode a (cost=0.00..17.00 rows=3 width=116) (actual time=0.047..0.049 rows=2 loops=1)
Filter: ((error_code)::text = 'ORA-04031'::text)
Planning Time: 0.280 ms
Execution Time: 2.387 ms
(9 rows)
```

PostgreSQL支持并行索引扫描，但需要设置max_parallel_workers_per_gather大于0。

## gis拓展

【**${\color{green}建议}$**】pg与geoserver的兼容性很强，需要在pg库中进行gis相关存储、计算，推荐以下插件：

| 插件名称               | 插件用途                  |
| ------------------------ | --------------------------- |
| postgis                | gis计算基础插件，空间计算 |
| postgis_topology       | 基于postgis的拓扑插件     |
| pgrouting              | 路径规划插件              |
| postgis_tiger_geocoder | tiger英文地址编码         |
| address_standardizer   | 地址标准化插件            |
| pg-trajectory          | 时空检索插件              |

【**${\color{red}强制}$**】postgis支持以下数据类型：

| 数据类型      | 用途                                                                                                       |
| --------------- | ------------------------------------------------------------------------------------------------------------ |
| box2d         | 二维边框                                                                                                   |
| box3d         | 三维边框                                                                                                   |
| geometry      | 用于在平面(欧几里得)坐标系中表示要素                                                                       |
| geometry_dump | 复合数据类型包含以下字段：geom -- 表示转储几何体的组件的几何体；path[] -- 定义转储的几何体中指向的geom组件 |
| geography     | 在大地坐标系中表示要素的空间数据类型                                                                       |

【**${\color{red}强制}$**】几何体输入输出格式：**知名文本(WKT)**和**知名二进制(WKB)**，详细资料可参考：https://www.osgeo.cn/postgis-manual/reference.html#idm8230

## pg_vector拓展

`pgvector` 为 PostgreSQL 提供了一个名为 `vector` 的数据类型，用于存储和操作高维向量。它特别适用于需要进行向量相似度计算和向量检索的场景，例如推荐系统、图像检索、自然语言处理等领域。使用时需要确认pgvector的版本与pg数据库版本适配，安装方式可参考官方教程：https://github.com/pgvector/pgvector，pg V13版本以下不支持。使用样例如下：

1、创建向量类型表，并设置特定维度的向量字段：

```sql
create table items (
    id serial primary key,
    embedding vector(300) -- 定义300维向量
);
```

向量存储在 PostgreSQL 中时实质上是定长的浮点数组。

`pgvector` 中的向量数据类型提供了针对这些浮点数组的优化存储和操作。

2、写入向量数据：

```sql
insert into items (embedding) values ('[1.0, 0.0, -1.0, ..., 0.5]');  -- 此处代表300维的向量
```

3、设置向量索引：

**HNSW（Hierarchical Navigable Small World）索引**是一种基于图的索引结构，其主要通过构建多层次的导航图来实现高效的相似性搜索：

```sql
create index on items using hnsw (embedding) with (M = 16, ef_construction = 200);
-- M：每个节点的最大连接数，增加该值能提高检索准确度，但降低插入与耗耗的性能。
-- ef_construction：构建时的邻近搜索数量，增加此值可以提升准确性，但增加内存消耗。
```

**IVFFlat（Inverted File with Flat Quantization）索引**基于聚类的思想，主要通过将数据分为多个簇来实现高效的相似性搜索：

```sql
create index on items using ivfflat (embedding) with (lists = 100);
-- lists：设置总簇数量，通常是数据量的平方根，簇越多，查询精度越高，但查询速度越慢，且会增加索引的创建和维护成本。
```

4、向量检索与相似度计算：

`pgvector` 支持常见的向量相似度计算方法，如欧氏距离计算、余弦相似度计算和内积计算。

**欧氏距离（Euclidean distance）**：衡量两个向量之间的直线距离：

```sql
select id, embedding
from items
order by embedding <-> '[1.0, 0.5, 0.3, ..., 0.2]' -- 指定查询向量
limit 5;
-- 表示计算 embedding 列中向量与指定向量之间的欧氏距离，并按距离排序
```

**余弦相似度（Cosine similarity）**：衡量两个向量的夹角，适合衡量向量方向的相似度:

```sql
select id, embedding
from items
order by embedding <=> '[1.0, 0.5, 0.3, ..., 0.2]' -- 指定查询向量
limit 5;
-- 表示计算 embedding 列中向量与指定向量之间的余弦相似度，并按相似度排序
```

**内积（dot product）**：计算两个向量的点积，适合某些特定的推荐系统:

```sql
select id, embedding
from items
order by embedding <#> '[1.0, 0.5, 0.3, ..., 0.2]' -- 指定查询向量
limit 5;
-- 表示计算 embedding 列中向量与指定向量的内积，并按内积值排序
```

5、优化建议：

- **参数调整：** 对于 HNSW，调整 `M` 和 `ef_construction` 可以有效提高查询精度，适当的内存开销是值得的；对于 IVFFlat，`lists` 的选择直接影响查询速度和精度，需根据数据量和应用场景进行调整。
- **数据预处理**：对数据进行归一化或标准化处理，可以提高模型的效果，特别是在 K-means 聚类阶段时。
- **物化视图**：对于频繁的复杂查询，可预先计算并存储结果，减少实时计算量。
- **负载均衡**：在多用户环境中，考虑负载均衡或者使用分片存储数据，如果向量数据量非常大，可以结合分区表策略，进一步提高查询性能。避免单一索引的性能瓶颈。
- **监控与调试**：使用 PostgreSQL 的性能监控工具，定期检查索引性能，必要时进行重建或再优化。

## PG监控工具pgbadger

### 安装

安装包地址：https://github.com/darold/pgbadger

下载后，放入目标主机：

```XML
unzip pgbadger-master.zip    ---因为我下载的是zip档
cd ./pgbadger-master        ---进入解压缩后的目录
perl Makefile.PL            ---会产生makefile文件
make && make install        ---安装
```

相关参数调整：

```XML
log_checkpoints = on
log_connections = on
log_disconnections = on
log_lock_waits = on
log_temp_files = 0
log_autovacuum_min_duration = 0
log_min_duration_statement = 1000
log_error_verbosity = default
log_statement = none
lc_messages='en_US.UTF-8'
log_line_prefix = '%t [%p]: [%l-1] user=%u,db=%d,app=%a,client=%h'
log_rotation_size = 10240
log_rotation_size = 1440
log_truncate_on_rotation = off
```

重启数据库，配置apache

```XML
apt install apache2*
其他具体细节省略，可以参考apache的配置
sudo mkdir /var/www/html/pgbadger_reports     ---在apache默认的home目录下创建一个folder用于存放pgbadger产生的报告
sudo chown postgres /var/www/html/pgbadger_reports
```

### 报告输出

手动产生报告：

```sql
-- 时间范围取决于rotation参数设定
postgres=# select name,setting,unit from pg_settings where name like '%rotation%';
           name           | setting | unit 
--------------------------+---------+------
 log_rotation_age         | 1440    | min
 log_rotation_size        | 10240   | kB
 log_truncate_on_rotation | off     |    ----log轮转时会保留旧的logfile
```

这个时间范围可以按照需求调整，这儿是分析当天的所有日志(使用了$CURRDATE*):

```sql
export CURRDATE=`date +%Y-%m-%d`
/usr/local/bin/pgbadger -q /data/pg_log/postgresql-$CURRDATE*.csv -o $REPTDIR/reports_$CURRDATE.html -j 8 -f csv --prefix '%t [%p]: [%l-1] user=%u,db=%d,app=%a,client=%h'
---注意：
1.如果logifle格式是csv，指定-f csv,如果是stderr指定-f stderr
2.--prefix，指定与log_line_prefix参数一致
```

自动产生报告：

```shell
#脚本位置及名称：#/backup/script/pg_logrpt.sh,
CURRDATE=`date +%Y-%m-%d`
PGDATA=/data
REPTDIR=/var/www/html/pgbadger_reports
if  [ ! -d $REPTDIR ]; then
    mkdir -p $REPTDIR
fi
/usr/local/bin/pgbadger -q $PGDATA/pg_log/postgresql-$CURRDATE*.csv -o $REPTDIR/reports_$CURRDATE.html -j 8 -f csv --prefix '%t [%p]: [%l-1] user=%u,db=%d,app=%a,client=%h'
echo "$PGDATA/pg_log/postgresql-$CURRDATE"
find $REPTDIR -name reports_*.html -mtime +8 -exec rm -rf {} \;


# 脚本授权
sudo chmod +755 /backup/script/pg_logrpt.sh  
# 设置crontab
00 23 * * * /backup/script/pg_logrpt.sh
```

### 报告样例

整体视图：

![image](uploads/118496/33fd1ac3-4a01-4fb3-b5c1-be79640382ff/图片.png)

常用视图：

- 慢sql统计：

![image](uploads/118496/9212e528-7b7c-43e9-8ec8-4cf87fb64123/图片.png)

- 会话视图统计：

![image](uploads/118496/4aa5c631-1819-4335-ba33-587debad933e/图片.png)

- 数据库连接视图统计：

![image](uploads/118496/f3cf1703-517c-4eed-8323-33273514ce54/图片.png)

## PG版本与JDBC版本对应推荐关系

根据 PostgreSQL JDBC 驱动项目的官方文档，其兼容性策略如下：

| JDBC 驱动版本 | 支持的最小 PostgreSQL 服务器版本 | 支持的最大 PostgreSQL 服务器版本（测试范围） | 支持的 Java 版本 (JDK) |
| :--- | :--- | :--- | :--- |
| **PGJDBC 42.7.x** | PostgreSQL 8.2 | PostgreSQL 16 (全面测试和支持) | **Java 8** 或更高版本 |
| **PGJDBC 42.6.x** | PostgreSQL 8.2 | PostgreSQL 15 | **Java 8** 或更高版本 |
| **PGJDBC 42.5.x** | PostgreSQL 8.2 | PostgreSQL 14 | **Java 8** 或更高版本 |
| **PGJDBC 42.4.x** | PostgreSQL 8.2 | PostgreSQL 13 | **Java 8** 或更高版本 |
| **PGJDBC 42.3.x** | PostgreSQL 8.2 | PostgreSQL 12 | **Java 8** 或更高版本 |
| **PGJDBC 42.2.x** | PostgreSQL 8.2 | PostgreSQL 11 | **Java 7** 或更高版本 (42.2.25 后需 Java 8) |
| ... | ... | ... | ... |

# 本文件评审、修正记录

| 文件名称 | SQL开发规范(PostgreSQL分册) |                                                                             |               |        |
| ---------- | ----------------------------- | ----------------------------------------------------------------------------- | --------------- | -------- |
| 序号     | 流程                        | 拟制人/审核人                                                               | 拟制/审核时间 | 版本号 |
| 1        | 编写                        | 李昱华                                                                      | 2024-3-3      | V0.1   |
| 2        | 评审                        | 李昱华/刘伯英/赵长兴/马列/张南雨/廖保平/刘凯/陶振杰/黄翕子/秦强/曹智/盛建华 | 2024-3-19     | V0.2   |
| 3        | 正式发布                     | 数据库规范组 | 2025-6-30     | V1.0   |
| 4        | 完善章节 “2.1 索引使用规范”措辞，使其更严谨，并补充索引、全文搜索、JSON、JSONB字段类型等内容： <br>【强制】对于复合索引，SQL语句的where查询条件必须有使用索引的第一列，复合列数量推荐不超过3个 <br>【强制】创建索引时加concurrently关键字，就可以并行创建（会有额外的资源消耗），不会堵塞DML操作，否则会堵塞DML操作 <br>【建议】在创建索引时，可以使用TABLESPACE子句指定索引存储在单独的表空间中，这样可以将索引和表数据分开存储，有助于性能优化 <br>【建议】创建主键约束会自动创建一个唯一索引，唯一索引可以确保索引列的值唯一，由于在PostgreSQL中，不同的NULL值被视为不相等，因此唯一索引列允许包含多个NULL值（PG支持NULL值索引（CREATE INDEX ... NULLS NOT DISTINCT），但需评估必要性） <br>【建议】对where中含多个字段条件的高频查询，结合数据分布情况，创建多个字段的联合索引，联合索引区分度高的列需要放到前面 <br>【建议】创建索引时使用INCLUDE子句允许在索引中包含非键列，这些列不会作为索引键，但可以用于索引扫描，在索引扫描时可以直接从索引中获取这些列的值，避免回表 <br>【建议】对于全文搜索场景，推荐通过对字段建立GIN索引或者GIST索引进行优化，对于中文模糊查询场景，推荐安装zhparser中文分词插件进行优化 <br>【建议】当数据被大量更新或删除后，索引可能会产生碎片，导致性能下降，此时应该重建索引（此外，重建索引可以解决索引膨胀问题，可以考虑定期进行重建）。PostgreSQL提供了REINDEX命令来重建索引，不需要停止数据库，但是重建期间会进行锁表，生产环境执行需谨慎 <br>【建议】对象文本类型可以考虑用JSONB字段类型进行存储，PostgreSQL 支持 JSON 和 JSONB 两种 JSON 类型： <br>            JSON：存储为 纯文本，查询时需要解析，效率较低。 <br>            JSONB：存储为 二进制格式，支持索引，查询性能更好。（推荐） <br>                   | 李昱华 | 2025-10-23     | V1.0.1   |
| 5        | 完善章节 “2.2.1. 查询限制”措辞，使其更严谨，并补充分区表查询、JOIN优化建议等内容：<br>【强制】当只需要查询一行数据时使用LIMIT 1<br>【强制】10万数据量以上的大表禁止使用没有where条件的查询（报表等低频场景例外）<br>【强制】分区表查询必须带上分区键作为查询条件<br>【建议】在PostgreSQL中对关键字大小写不敏感，需要使用大写的标志符时，必须要加上双引号，否则会被转为小写。为了提高可读性，建议关键字、表名和列名全部使用小写<br>【建议】表名和列名的别名应该使用有意义的英文单词或缩写，不能包含空格，非必要情况下不要使用拼音或者中文<br>【建议】在PostgreSQL中，子查询（Subquery）是一种在另一个查询内部嵌套的查询。根据子查询是否依赖于外部查询的某些行，子查询可以分为两大类：相关子查询（Correlated Subquery）和非相关子查询（Non-Correlated Subquery），相关子查询依赖于外部查询的某些行。换句话说，子查询中的某些条件或计算是基于外部查询的当前行的<br>【建议】尽量避免多表的关联操作，对于join 的表的数量控制在5个以内，表设计中需要注意关联表之间的设计关系，关联字段类型的数据类型必须一致，建议字段名也应一致，并建立索引加速查询<br><br> 完善章节 “2.2.3 空值场景”措辞，使其更严谨：<br>【建议】涉及空值与非空值的等值比较，请使用 is distinct from 进行比较，保证比较结果非空<br>                 | 李昱华 | 2025-10-23     | V1.0.2   |
| 6        | 完善章节“2.2.6. 其他场景”措辞，使其更严谨，并补充&124;&124;操作符、日期函数、copy复制表操作等内容：<br>【建议】在PostgreSQL中，&124;&124;操作符是标准的字符串连接操作符，推荐使用。concat函数也可以使用，但&124;&124;更简洁<br>【建议】PostgreSQL提供了丰富的日期时间函数，常见场景使用方法推荐：时区转换（例如AT TIME ZONE），current_date获取当前日期，now()函数获取当前时间戳，以及对日期和时间进行加减计算<br>【建议】聚合函数（如SUM, AVG, COUNT等）会忽略NULL值，使用时需要注意。例如，COUNT(column)只计算非NULL值<br>【建议】利用row_number窗口函数优化超多分页场景，窗口函数不会改变结果集的行数，它只是为每一行计算一个值，基于与当前行相关的行集<br>【建议】可以使用insert into ... select或者copy操作（copy导出到文件再导入表，性能比insert更好）从另一个表快速批量插入数据，注意批量插入数据时，应该使用事务来包裹<br>                     | 李昱华 | 2025-10-23     | V1.0.3   |
| 7        | 章节“2.3. 应用程序规约”补充连接池配置等内容：<br>【强制】对于高并发的应用场景，务必使用程序的连接池，否则性能会很低下。 如果程序没有连接池，建议在应用层和数据库之间架设连接池，例如使用pgbouncer或者pgpool-II作为连接池：<br>      连接池应该设置合适的最大连接数，以防止连接过多，避免超过数据库的最大连接数限制；<br>      连接池应该设置最大空闲超时时间，防止连接泄漏；<br>      连接池应设置最小连接数避免冷启动，并使用 SET SESSION 初始化连接参数；<br>      自动提交通常开启（显式事务除外）；<br>【强制】禁用默认超级用户，业务角色权限分配应遵循最小权限原则，禁用 PUBLIC 默认权限<br>【强制】在开发使用PostgreSQL的应用程序时，应用程序应该捕获并处理数据库错误，记录数据库错误信息以便排查问题，并且应该根据错误类型进行相应的处理（如重试、回滚等），禁止将详细的数据库错误信息直接展示给用户，因为这可能暴露敏感信息（如数据库结构等）<br>【强制】应用程序应该设置查询超时（例如使用statement_timeout参数或在应用层设置超时），以避免长时间运行的查询占用资源<br>【强制】禁止在事务中混合读写和DDL操作，DDL在事务中可能导致锁冲突或不可回滚（如TRUNCATE）<br>【建议】可以通过以下手段防止SQL注入：<br>      用参数化查询；<br>      制数据库用户权限；<br>   用 prepared statement 预编译对象；<br>【建议】大结果集处理推荐使用游标cursor + fetch_size 参数分批次获取<br>【建议】在客户端应用程序中，应当避免在循环中执行SQL语句，应该尽量使用批量操作<br>                    | 李昱华 | 2025-10-23     | V1.0.4   |
| 8        | 新增章节3.5 PG版本与JDBC版本对应推荐关系<br>                   | 李昱华 | 2025-10-23     | V1.0.5   |
| 9        | 正式发布                     | 数据库规范组 | 2025-10-27     | V1.1   |
| 10        | 修改章节“2.2.1. 查询限制”中对join表的数量控制，由5个降到3个及以内，和MySQL数据库保持一致，修改后规范：<br>【建议】尽量避免多表的关联操作，对于join 实例表的总数量控制在3个及以内，表设计中需要注意关联表之间的设计关系，关联字段类型的数据类型必须一致，建议字段名也应一致，并建立索引加速查询                     | 李昱华 | 2026-01-23     | V1.1.1   |
| 11        | 正式发布                     | 数据库规范组 | 2026-03-23     | V1.2   |

