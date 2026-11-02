![image](uploads/121315/4037b224-c518-43e3-83a3-c5d39f4b5559/image.png)

# 概述

## 适用范围

适用于Postgresql V12.x及以上版本。

## 角色和职责

数据库设计人员：负责按照规范进行数据库对象设计

# 数据库设计规范

## 命名规范

【**${\color{red}强制}$**】字段名、表名限制命名长度，建议表名、字段名长度控制在30字符以内，索引长度控制在64字符以内。（人工检查）

【**${\color{red} 强制}$**】对象名（表名、列名、函数名、视图名、序列名等对象名称）应该使用有意义的英文单词或缩写，务必只使用小写字母，下划线，数字，非必要情况下不要使用拼音以及中文。（人工检查）

【**${\color{red} 强制}$**】命名统一采用snake_case格式，不要以pg开头，不要以数字开头，不要使用保留字。（人工检查）

保留字参考：https://www.postgresql.org/docs/12/sql-keywords-appendix.html

## 表设计规范

### 格式

【**${\color{green}建议}$**】表名格式建议为模块名+正常表名+后缀或者项目缩写+表名+后缀，多个模块公共表，可不设置模块前缀。

【**${\color{green}建议}$**】表名不使用复数名词。

### 约束

【**${\color{red} 强制}$**】多表中的相同列，必须保证列名一致，数据类型一致。（人工检查）

【**${\color{red} 强制}$**】每个表都必须有主键，主键初始化之后不允许修改，可以是多列组合。主键约束命名格式为：**`pk_表名_字段`**、唯一约束命名格式为：**`un_表名_字段`**（人工检查）

【**${\color{green}建议}$**】可以考虑使用uuid作为主键值，但是uuid主键并非适用于所有场景。

【**${\color{red} 强制}$**】实例表禁止使用外键，配置表上可以根据场景建立外键。外键约束会降低插入和更新性能，使用外键时，引用必须设置相应的动作并创建索引：`set null, set default, cascade`，外键推荐的命名格式为：**`fk_childtable（源表名称）_parenttable（目标表名称）_column（字段名称）`**。

### 容量

【**${\color{green}建议}$**】尽量慎用宽表，字段数目超过15个的表视作宽表，宽表应当考虑进行纵向拆分，通过相同的主键与主表相互引用；因为MVCC机制，宽表的写放大现象比较明显，尽量减少对宽表的频繁更新。

【**${\color{green}建议}$**】单表数据容量最大不超过20G，建议超过2千万条数据则进行分区。

【**${\color{green}建议}$**】对于频繁更新的表，建议建表时指定表的fillfactor=85，每页预留15%的空间给HOT更新使用。

```sql
postgres=# create table test123(id int, info text) with(fillfactor=85);  
create table
```

### 分区

**范围分区**：根据某个列的范围将数据分布到不同的分区中。适用于按照时间、数字范围等进行分区的场景；

```sql
create table measurement (
    city_id int not null,
    logdate date not null,
    peaktemp int,
    unitsales int
) partition by range (logdate);
 
create table measurement_y2006m02 partition of measurement
    for values from ('2006-02-01') to ('2006-03-01');
 
create table measurement_y2007m02 partition of measurement
    for values from ('2007-02-01') to ('2007-03-01');
```

**列表分区**：根据某个列的值将数据分布到不同的分区中。适用于按照离散值进行分区的场景。例如，按照地理位置、产品类别等进行分区的表；

```sql
create table employees (
    department_id int not null,
    employee_id int not null,
    name text,
    salary int
) partition by list (department_id);
 
create table employees_sales partition of employees
    for values in (1, 2, 3);
 
create table employees_engineering partition of employees
    for values in (4, 5, 6);
```

**哈希分区**：根据哈希算法将数据均匀地分布到不同的分区中。适用于需要均匀地将数据分布到多个分区中的场景。例如，将数据分布到多个物理机器上，以提高查询性能和可伸缩性；

```sql
create table orders (
    order_id int not null,
    cust_id int not null,
    amount decimal,
    order_date date
) partition by hash (cust_id);
 
create table orders_p0 partition of orders
    for values with (modulus 4, remainder 0);
 
create table orders_p1 partition of orders
    for values with (modulus 4, remainder 1);
```

【**${\color{green}建议}$**】分区表命名格式为**`父表名_分区条件`**

【**${\color{green}建议}$**】有定期历史数据删除需求的业务，表按时间分区，删除时不要使用delete操作，而是drop或者truncate对应的表。

【**${\color{red} 强制}$**】分区表的分区键数据类型应避免使用非整型类型（字符串、浮点数），非整型分区键可能导致数据倾斜或查询时需扫描更多分区。（人工检查）

【**${\color{red} 强制}$**】分区表查询必须带上分区键作为查询条件。（人工检查）

### 序列

【**${\color{red} 强制}$**】pg数据库序列推荐命名格式为：**`table（表名）_column（字段名）_seq`**、**`seq_table（表名）_column（字段名）`**。

【**${\color{green}建议}$**】序列创建方式如下：

```sql
-- 首选推荐通过sequence对象进行创建

CREATE SEQUENCE user_id_seq START 1000 INCREMENT 1 CACHE 20 NO CYCLE;

-- START为起始值设置，默认从 1 开始
-- INCREMENT为步长设置，默认为1
-- CACHE 20为一次预取20个值，可以减少序列争用，提升高并发插入性能，但是缓存值丢失可能导致序列间隙（崩溃/重启时）。对连续性要求极高的系统可设 CACHE 1。
-- NO CYCLE为禁用重置计数，主键列必须要进行设置，防止出现重复数据

CREATE TABLE user (
    id INTEGER DEFAULT nextval('user_id_seq') NOT NULL,
    ...
);

-- 可以在创建表时同时通过IDENTITY设置进行创建
CREATE TABLE user (
    id INT GENERATED ALWAYS AS IDENTITY (START WITH 1000) PRIMARY KEY, -- 自动创建序列 `users_id_seq`
    name TEXT
);

-- 允许使用SERIAL伪类型设置字段序列（不推荐），SERIAL并非真正数据类型，是自动创建序列 + 绑定默认值融合的语法糖
CREATE TABLE user (
    id SERIAL PRIMARY KEY,  -- 自动创建序列 `users_id_seq`
    name TEXT
);

```

【**${\color{green}建议}$**】多个表可以共享一个序列，但是不推荐，因为这样会使表之间的主键产生关联，并且可能难以维护，每个表应该有自己的序列。

【**${\color{green}建议}$**】序列操作在事务之外。即使事务回滚，序列递增的值也不会回滚。这意味着序列保证全局唯一但不保证连续。

### 继承（不推荐使用）

【**${\color{green}建议}$**】PostgreSQL的表继承是一种将多个表组织成层次结构的功能，允许父表定义共享列和约束，子表继承这些定义并可添加额外字段：

```sql
-- 父表定义
create table employee

(   id                    int  not null,
    employee_name         varchar(64),
    salary                int check(salary>0),
    primary key(id)
);

CREATE INDEX idx_employee_01 ON employee(employee_name);

-- 子表定义方式1，继承父表字段，不继承主键、索引
create table employee_info
(   depart_id   int,
    job_title   varchar(64)
)inherits(employee);

-- 子表定义方式2，继承父表字段、主键、索引
create table employee_info
(   like employee including all，
 		depart_id   int,
    job_title   varchar(64)
) inherits (employee);

-- 继承只是继承表结构，数据不会继承，也就是说，父表插入的数据，子表是不存在的
-- 查询父表数据的时候，对应的继承表数据也被查询出来，如果只需要父表数据，需要带上关键字only
```

【**${\color{green}建议}$**】可以考虑通过继承实现逻辑分区，但对于大规模数据和高性能查询，还是建议使用partition物理分区的策略。

## 字段设计规范

### 格式

【**${\color{red} 强制}$**】避免使用保留字作为列名。（人工检查）

【**${\color{green}建议}$**】字段推荐格式如下：BODY(主体名)_SUFFIX（后缀名）

例如: 客户编码 cust_nbr

其中，

- BODY为主体名，应该能够清楚地说明对象的含义,采用英文缩写；
- SUFFIX是后缀名，提供特殊的含义；
- 字段名称不能出现数据库中的关键字。

【**${\color{green}建议}$**】布尔类型字段推荐使用 **`is_BODY(主体名)/has_BODY(主体名)`**的格式

【**${\color{green}建议}$**】表常备三字段：xxx_id,  created_date, update_date表示主键、创建时间和更新时间。时间类型均为 timestamp类型

### 约束

【**${\color{red} 强制}$**】有默认值的字段必须添加default子句指定默认值。（人工检查）

【**${\color{red} 强制}$**】字段语义上没有零值与空值区分的，不允许空值存在，必须为字段配置not null约束。（人工检查）

【**${\color{red} 强制}$**】唯一约束必须由数据库保证，任何唯一列须有唯一约束。（人工检查）

【**${\color{green}建议}$**】如果需要限制列值范围，可以通过设置check约束（建议在应用程序进行范围限制），命名格式为：**`chk_column（字段名称）_条件`**：

```sql
CREATE TABLE employee (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    age INT,
    CONSTRAINT chk_age_18_65 CHECK (age >= 18 AND age <= 65) -- 限制年龄在18到65之间
);
```

### 字段类型

【**${\color{green}建议}$**】主键推荐使用bigint类型，允许使用不超过64字节的字符串，允许使用Serial自动生成，建议使用default next_id()发号器函数。

【**${\color{green}建议}$**】存储布尔类型的字段推荐使用BOOLEAN类型，而不是CHAR(1)。

【**${\color{green}建议}$**】大文本字段应与主表分开存储以提高查询性能。

【**${\color{green}建议}$**】较稳定的，取值空间较小（十几个内）的字段应当使用枚举类型，不要使用整型与字符串表示，使用枚举类型有性能、存储、可维护性上的优势，但是枚举类型不利于后期修改。

【**${\color{green}建议}$**】文本类型字段通常建议使用varchar或text（可变长字符串优先选择varchar，超长文本如文章内容应使用text），带有(n)修饰符的类型会检查字符串长度，会导致微小的额外开销，对字符串长度有限制时应当使用varchar(n)，避免插入过长的脏数据。

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

【**${\color{green}建议}$**】避免使用char(n)作为文本字段类型，为了与SQL标准兼容，该类型存在空格补齐、截断等行为。

【**${\color{green}建议}$**】存储时间字段可以考虑实际业务场景，合理选择timestamp、date、time、interval类型存储不同格式。

【**${\color{green}建议}$**】存储IP地址推荐使用INET字段类型，PostgreSQL的INET类型专为IP地址设计。

【**${\color{green}建议}$**】bytea类型可以存储二进制字符串，是Postgresql数据库中保存字节流的类型，对于一些涉及到需要加密的字段，推荐使用BYTEA类型存储加密后的值。

【**${\color{green}建议}$**】图片存储建议放在文件系统中，数据库存储对应路径，不建议使用bytea或者text类型字段存储图片的二进制值。

【**${\color{green}建议}$**】在PostgreSQL中，数组类型字段允许你在单个列中存储固定数量的元素序列，这对于存储一系列关联数据非常有用，数据类型字段同样支持通过`GIN`索引进行查询加速，例如：一组产品分类的tag标签、一组日期时间、一组枚举数字等等。数组类型虽然强大，但会增加查询复杂度，使用方式如下：

```sql
-- 创建产品表，其中包含一个名为tags的列，可以存储一个文本数组
CREATE TABLE product (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    tags TEXT[]
);

-- 插入数据
INSERT INTO product (name, tags) VALUES ('Product A', '{"red", "large", "electronics"}');

-- 查询数组字段，使用unnest函数，将数组展开为多行
SELECT unnest(tags) FROM product WHERE id = 1;

-- 检查一个值是否在数组中
SELECT * FROM product WHERE 'red' = ANY(tags);

-- 检查一个数组是否是另一个数组的子集
SELECT * FROM product WHERE tags @> '{"red"}';  -- 检查tags是否包含"red"

-- 检查一个数组是否是另一个数组的超集
SELECT * FROM product WHERE tags <@ '{"red", "large"}';  -- 检查tags是否完全包含"red"和"large"

-- 添加元素到数组末尾
UPDATE product SET tags = tags || '{"new_tag"}' WHERE id = 1;

-- 删除特定元素（如果存在）
UPDATE products SET tags = array_remove(tags, 'old_tag') WHERE id = 1;
```

【**${\color{green}建议}$**】数值类型字段建议：

- 常规数值字段使用integer。主键、容量拿不准的数值列使用bigint；
- 无特殊理由不要用smallint，性能与存储提升很小，会有很多额外的问题；
- REAL表示4字节浮点数，float表示8字节浮点数；
- 浮点数仅可用于末尾精度无所谓的场景，例如地理坐标，不要对浮点数使用等值判断；
- 精确数值类型使用numeric注意精度和小数位数设置；
- 货币数值类型使用money；

## 索引设计规范

### 格式

【**${\color{green}建议}$**】主键索引应以 pk_ 开头， 唯一索引要以 uk_ 开头，普通索引要以 idx_ 打头。

### 通用场景设计规范

【**${\color{red}强制}$**】多表需要 JOIN的字段，数据类型必须一致，且被关联的字段要有索引。（人工检查）

【**${\color{red}强制}$**】btree索引字段大小不能超过2kb，如果有超过2kb的字段需要建索引，建议使用函数索引（例如哈希值索引），或者使用分词索引`gin`。（人工检查）

【**${\color{green}建议}$**】空值排序规则需要明确，例如：

```sql
create index on tbl (id desc nulls last);
-- DESC排序的默认规则是NULLS FIRST，即空值会出现在排序的最前面，通常这不是期望行为
```

【**${\color{green}建议}$**】区分度低、经常更新的列不适合建索引。

【**${\color{green}建议}$**】对where中含多个字段条件的高频查询，结合数据分布情况，创建多个字段的联合索引，联合索引区分度高的列需要放到前面，长字段text不应包含在索引中。

【**${\color{green}建议}$**】建议一张表不要建过多index，特别DML操作较多的表，一般不超过6个，核心表可适当增加index个数。

【**${\color{green}建议}$**】V12版本及以下不要使用hash index，该版本hash index不写REDO LOG，在备库只有结构，没有数据，并且数据库crash后无法恢复。V12版本以上可以使用。

### 范围查询场景设计规范

【**${\color{green}建议}$**】对于值与堆表的存储顺序线性相关的数据，如果通常的查询为范围查询，建议使用BRIN索引。例如流式数据，时间字段或自增字段，可以使用BRIN索引，减少索引的大小，加快数据插入速度：

```sql
create index idx on tbl using brin(id);
```

【**${\color{green}建议}$**】当业务有近邻查询（KNN）的需求时，推荐对字段建立GIST或SP-GIST索引，加速近邻查询的需求。

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

**GiST（Generalized Search Tree通用搜索树）**索引是PostgreSQL数据库系统中用于复杂数据类型的高效索引机制，它不是单独一种索引类型，而更像是一种架构。在这个架构上可以扩展出其他的索引，例如 **SP-Gist**（空间分区的通用搜索树），支持进行分区搜索，便于开发各种不同的基于磁盘的非平衡数据结构，例如 **四叉树**、**k-d 树和基数树（tries）**，GIS（地理空间）、多媒体、网络路由、IP路由等存储、查询场景非常适合使用。

【**${\color{green}建议}$**】对于固定条件的查询，可以使用部分索引，减少索引的大小，同时提升查询效率，例如：

```sql
select * from tbl where id=1 and col=?; -- 其中id=1为固定的条件  
create index idx on tbl (col) where id=1;
```

【**${\color{green}建议}$**】对于经常使用表达式作为查询条件的语句，可以使用表达式或函数索引加速查询，减少索引的大小，例如：

```sql
select * from tbl where exp(xxx);  
create index idx on tbl ( exp );
```

### 模糊查询场景设计规范

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

【**${\color{green}建议}$**】对于中文模糊查询、全文搜索场景，推荐对字段建立GIN索引，并安装zhparser中文分词插件。

1、下载zhparser源码并进行编译；

2、登陆pg控制台使用

`CREATE EXTENSION zhparser`启用插件；

3、添加分词配置：

```sql
create text search configuration parser_name (parser = zhparser); // 添加配置
alter text search configuration parser_name add mapping for n,v,a,i,e,l,j with simple; // 设置分词规则 （n 名词 v 动词等）
```

4、给某一列的分词结果添加 gin 索引

`create index idx_name on table using gin(to_tsvector('parser_name', field));`

5、根据实际情况在

`postgresql.conf`添加配置：

```xml
zhparser.multi_short = true #短词复合: 1
zhparser.multi_duality = true  #散字二元复合: 2
zhparser.multi_zmain = true  #重要单字复合: 4
zhparser.multi_zall = false  #全部单字复合: 8
```

参考链接：https://developer.aliyun.com/article/7730

6、查询样例：

```sql
select * from table where to_tsvector('parser_name', field) @@ 'word';// 查询 field 字段分词中带有 word 一词的数据
```

## 其他对象设计规范

### 通用设计规范

【**${\color{red} 强制}$**】数据库字符编码必须为UTF8。（人工检查）

【**${\color{red} 强制}$**】使用utc时区设置，使用ISO-8601格式输入输出时间类型：2006-01-02 15:04:05。（人工检查）

【**${\color{green}建议}$**】尽量避免使用数据库触发器，这会使得数据处理逻辑复杂，不便于调试，触发器推荐命名格式为`tr_表名_操作_目的`。

【**${\color{red} 强制}$**】禁止使用存储过程，业务逻辑由应用程序实现。

【**${\color{green}建议}$**】pg中的表空间实际上就是文件系统中的一个目录, 是pg中数据库对象（包括表、索引等）的容器，使用操作系统的文件系统进行对象存储，每个数据库对象都有自己的数据文件，如果对象很大，它将会被分为多个文件，单个文件大小的上限是1GB。表空间就是包含这些数据文件的目录。当存储分区没有空间时，可以使用表空间把数据存到其他分区。利用表空间对数据库进行性能优化。如频繁使用的数据表或索引放在高性能的硬盘上，而较少使用的放在普通硬盘上。（注意，这时候需要调整表空间参数：`seq_page_cost`和`random_page_cost`）。

### 库、模式命名规范

【**${\color{green}建议}$**】库名最好与应用名称一致，或便于辨识。

【**${\color{green}建议}$**】不使用public schema存放对象（不同业务共享的对象可以使用public schema），应该为每个应用分配对应的schema，schema_name最好与user name一致。

【**${\color{green}建议}$**】多个部分使用 _ 连接。例如：`_chat_shard`，`_payment`等，总共不超过三段

### 关系命名规范

【**${\color{green}建议}$**】临时表以 tmp_ 开头，子表以规则结尾，例如按年分区的主表如果为tbl, 则子表为tbl_2016，tbl_2017，。。。

【**${\color{green}建议}$**】视图以v_ 作为命名前缀，物化视图使用mv_ 作为命名前缀（物化视图不会自动更新，需要手动或者定时更新）。

### 函数命名规范

【**${\color{green}建议}$**】以`select`，`insert`，`delete`，`update`等动词打头，表示动作类型。

【**${\color{green}建议}$**】重要参数可以通过`_by_ids`，`_by_user_ids`的后缀在函数名中体现。

### 注释规范

【**${\color{green}建议}$**】尽量为对象提供注释（comment），注释不要使用中文，因为编码可能不一样，如果存进去和读取时的编码不一致，导致可读性不强。 pg_dump时也必须与注释使用的编码一致，否则可能乱码。

# 本文件评审、修正记录

| 文件名称 | 数据库模型设计规范(PostgreSQL分册) |                                                                             |               |        |
| ---------- | ------------------------------------ | ----------------------------------------------------------------------------- | --------------- | -------- |
| 序号     | 流程                               | 拟制人/审核人                                                            | 拟制/审核时间 | 版本号 |
| 1        | 编写                               | 李昱华                                                                  | 2025-3-3      | V0.1   |
| 2        | 评审                               | 李昱华/刘伯英/马列/赵长兴/张南雨/廖保平/刘凯/陶振杰/黄翕子/秦强/曹智/盛建华 | 2025-3-19     | V0.2   |
| 3        | 正式发布                           | 数据库规范组 | 2025-6-30     | V1.0   |
| 4        | 完善章节 “2.1 命名规范”措辞，使其更严谨：<br>【强制】字段名、表名限制命名长度，建议表名、字段名长度控制在30字符以内，索引长度控制在64字符以内。<br>【强制】对象名（表名、列名、函数名、视图名、序列名等对象名称）应该使用有意义的英文单词或缩写，务必只使用小写字母，下划线，数字，非必要情况下不要使用拼音以及中文。<br> | 李昱华 | 2025-10-10     | V1.0.1  |
| 5        | 完善章节 “2.2.2 约束”措辞，使其更严谨：<br>【强制】每个表都必须有主键，主键初始化之后不允许修改，可以是多列组合。主键约束命名格式为：pk_表名_字段、唯一约束命名格式为：un_表名_字段<br>【建议】可以考虑使用uuid作为主键值，但是uuid主键并非适用于所有场景<br>【强制】实例表禁止使用外键，配置表上可以根据场景建立外键。外键约束会降低插入和更新性能，使用外键时，引用必须设置相应的动作并创建索引：set null, set default, cascade，外键推荐的命名格式为：fk_childtable（源表名称）_parenttable（目标表名称）_column（字段名称）<br> | 李昱华 | 2025-10-10     | V1.0.2  |
| 6        | 章节“2.2.4 分区”补充命名要求等内容： <br>【建议】分区表命名格式为父表名_分区条件<br>【强制】分区表的分区键数据类型应避免使用非整型类型（字符串、浮点数），非整型分区键可能导致数据倾斜或查询时需扫描更多分区<br>【强制】分区表查询必须带上分区键作为查询条件<br> | 李昱华 | 2025-10-10     | V1.0.3  |
| 7        | 新增章节2.2.5 序列、2.2.6. 继承| 李昱华 | 2025-10-10     | V1.0.4  |
| 8        | 章节“2.3.1 格式”补充布尔类型字段命名格式等内容：<br>【强制】避免使用保留字作为列名<br>【建议】布尔类型字段推荐使用 is_BODY(主体名)/has_BODY(主体名)的格式<br>| 李昱华 | 2025-10-10     | V1.0.5  |
| 9        | 章节“2.3.2 约束”补充字段check约束相关条目： <br>【建议】如果需要限制列值范围，可以通过设置check约束（建议在应用程序进行范围限制），命名格式为：chk_column（字段名称）_条件<br>| 李昱华 | 2025-10-10     | V1.0.6  |
| 10       | 完善章节 “2.3.3 字段类型”措辞，使其更严谨，并补充json、jsonb字段类型等内容：<br>【建议】存储布尔类型的字段推荐使用BOOLEAN类型，而不是CHAR(1)<br>【建议】大文本字段应与主表分开存储以提高查询性能<br>【建议】较稳定的，取值空间较小（十几个内）的字段应当使用枚举类型，不要使用整型与字符串表示，使用枚举类型有性能、存储、可维护性上的优势，但是枚举类型不利于后期修改<br>【建议】文本类型字段通常建议使用varchar或text（可变长字符串优先选择varchar，超长文本如文章内容应使用text），带有(n)修饰符的类型会检查字符串长度，会导致微小的额外开销，对字符串长度有限制时应当使用varchar(n)，避免插入过长的脏数据<br>【建议】对象文本类型可以考虑用JSONB字段类型进行存储，PostgreSQL 支持 JSON 和 JSONB 两种 JSON 类型：<br>             JSON：存储为 纯文本，查询时需要解析，效率较低。<br>             JSONB：存储为 二进制格式，支持索引，查询性能更好。（推荐）<br>【建议】存储时间字段可以考虑实际业务场景，合理选择timestamp、date、time、interval类型存储不同格式<br>【建议】存储IP地址推荐使用INET字段类型，PostgreSQL的INET类型专为IP地址设计<br>【建议】bytea类型可以存储二进制字符串，是Postgresql数据库中保存字节流的类型，对于一些涉及到需要加密的字段，推荐使用BYTEA类型存储加密后的值<br>【建议】图片存储建议放在文件系统中，数据库存储对应路径，不建议使用bytea或者text类型字段存储图片的二进制值<br>【建议】在PostgreSQL中，数组类型字段允许你在单个列中存储固定数量的元素序列，这对于存储一系列关联数据非常有用，数据类型字段同样支持通过GIN索引进行查询加速，例如：一组产品分类的tag标签、一组日期时间、一组枚举数字等等。数组类型虽然强大，但会增加查询复杂度<br>| 李昱华 | 2025-10-10     | V1.0.7  |
| 11       | 完善章节“2.4.2 通用场景设计规范”措辞，使其更严谨： <br>【建议】空值排序规则需要明确<br>【建议】区分度低、经常更新的列不适合建索引<br>【建议】对where中含多个字段条件的高频查询，结合数据分布情况，创建多个字段的联合索引，联合索引区分度高的列需要放到前面，长字段text不应包含在索引中<br>【建议】V12版本及以下不要使用hash index，该版本hash index不写REDO LOG，在备库只有结构，没有数据，并且数据库crash后无法恢复。V12版本以上可以使用<br>| 李昱华 | 2025-10-10     | V1.0.8  |
| 12       | 章节“2.4.3 范围查询场景设计规范”补充GiST索引介绍<br>| 李昱华 | 2025-10-10     | V1.0.9  |
| 14       | 完善章节“2.5.1 通用设计规范”措辞，使其更严谨，并补充表空间相关内容： <br>【建议】尽量避免使用数据库触发器，这会使得数据处理逻辑复杂，不便于调试，触发器推荐命名格式为tr_表名_操作_目的<br>【强制】禁止使用存储过程，业务逻辑由应用程序实现<br>【建议】pg中的表空间实际上就是文件系统中的一个目录, 是pg中数据库对象（包括表、索引等）的容器，使用操作系统的文件系统进行对象存储，每个数据库对象都有自己的数据文件，如果对象很大，它将会被分为多个文件，单个文件大小的上限是1GB。表空间就是包含这些数据文件的目录。当存储分区没有空间时，可以使用表空间把数据存到其他分区。利用表空间对数据库进行性能优化。如频繁使用的数据表或索引放在高性能的硬盘上，而较少使用的放在普通硬盘上。（注意，这时候需要调整表空间参数：seq_page_cost和random_page_cost）<br>| 李昱华 | 2025-10-10     | V1.0.10  |
| 15       | 完善章节“2.5.3 关系命名规范”措辞，使其更严谨： <br>【建议】视图以v_ 作为命名前缀，物化视图使用mv_ 作为命名前缀（物化视图不会自动更新，需要手动或者定时更新）<br>| 李昱华 | 2025-10-10     | V1.0.11  |
| 16       | 发布 | 数据库规范组 | 2025-10-27     | V1.1  |
