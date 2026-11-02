# 编写目的

<font style="color:rgb(52, 73, 94);">本文用于描述浩鲸科技软件产品中数据库模型的设计规范（Clickhouse部分）。</font>

# 适用范围

<font style="color:rgb(52, 73, 94);">适用于业务相关的数据模型设计，涉及数据库的种类包含Clickhouse。</font>

<font style="color:rgb(52, 73, 94);">本文所指数据库模型仅包含表（表中主键、字段、索引），以及一些特定表（定义见4.2.1节）的配置规范。</font>

<font style="color:rgb(52, 73, 94);">本文所指脚本范围不包含客服人员以维护系统或者割接为目的而使用的脚本，不包含数据库用户、权限、数据库实例等的建立和维护，此部分由相关集成部门提供，但建议各建库、运维等脚本也参考本标准规范。</font>

# 角色和职责

1. <font style="color:rgb(52, 73, 94);">SA：负责业务的概要设计和相关数据模型设计，并进行验证。</font>
2. <font style="color:rgb(52, 73, 94);">测试：负责对数据库脚本进行第二次检查。</font>
3. <font style="color:rgb(52, 73, 94);">CMO：负责导出指定事务单中的相关数据库脚本，用于发布。</font>
4. <font style="color:rgb(52, 73, 94);">DBA：数据库系统管理员</font>

# Clickhouse数据库模型设计规范

## 基本设计规范

### 构成规范

<font style="color:rgb(52, 73, 94);">【强制】数据库中各种名称必须以字母开头，严禁使用 </font>**<font style="color:rgb(52, 73, 94);">system、sys</font>**<font style="color:rgb(52, 73, 94);"> 等 ClickHouse 内部保留关键字作为库名、表名或字段名前缀。</font>

<font style="color:rgb(52, 73, 94);">【强制】名称只能含有26个英文字母，0～9这10个自然数和下划线这三类字符。避免出现连续下划线和下划线结尾，$\color{#ff0000}反例$如 user__info_，不利于可读性。</font>

<font style="color:rgb(52, 73, 94);">【强制】命名应能准确反映其含义，采用英文单词或约定缩写，不得中英文混用；缩写需在团队维护的缩写表中统一。</font>

<font style="color:rgb(52, 73, 94);">【强制】命名禁止使用 SQL/ClickHouse 保留字；</font><font style="color:#DF2A3F;">$\color{#ff0000}反例$</font><font style="color:rgb(52, 73, 94);">如 desc、user、key、index、partition、engine等。</font>

> <font style="color:rgb(52, 73, 94);">SQL/ClickHouse 保留字 查看附录</font>

<font style="color:rgb(52, 73, 94);">【推荐】在不同位置出现的、表示相同含义及内容的字段名称命名应该一致。避免同一字段在不同表中使用不同名称表达相同含义（如 user_id、uid、usrid 表示同一内容）。</font>

### 大小写规范

<font style="color:rgb(52, 73, 94);">【推荐】数据库中的数据库名、表名、字段名的所有字符，使用</font>**<font style="color:rgb(52, 73, 94);">小写（Clickhouse数据库库名/表名/字段名大小写敏感）</font>**<font style="color:rgb(52, 73, 94);">。</font>

<font style="color:rgb(52, 73, 94);">【推荐】单词间以下划线分隔，如 user_order_detail_local。</font>

<font style="color:rgb(52, 73, 94);"></font>

### 长度规范

<font style="color:rgb(52, 73, 94);">【强制】所有对象标识符均不能超过50个字符，也即：Clickhouse中的表名、字段名的长度均不能超过50个字符。
</font>

## 表的设计规范

### 表的分类

> <font style="color:rgb(52, 73, 94);">本节对 ClickHouse 表类型进行定义，以便后续章节规范中引用表类型约束。建表语句可参考文档</font>[https://docs.iwhalecloud.com/doi/c7EHkD/sitsbSAs/Clickhouse%E4%B8%AD%E7%9A%84%E8%A1%A8%E5%BC%95%E6%93%8E%E4%BB%A5%E5%8F%8A%E5%A6%82%E4%BD%95%E5%BB%BA%E6%9C%89%E6%95%88%E8%A1%A8.pdf](https://docs.iwhalecloud.com/doi/c7EHkD/sitsbSAs/Clickhouse%E4%B8%AD%E7%9A%84%E8%A1%A8%E5%BC%95%E6%93%8E%E4%BB%A5%E5%8F%8A%E5%A6%82%E4%BD%95%E5%BB%BA%E6%9C%89%E6%95%88%E8%A1%A8.pdf)<font style="color:rgb(52, 73, 94);">《Clickhouse中的表引擎以及如何建有效表》
> </font>**说明**<font style="color:rgb(52, 73, 94);">：本节为概念说明，非具体强制规范。</font>

<font style="color:rgb(52, 73, 94);">【强制】涉及分布式集群的 DDL 建表操作必须加 </font>**<font style="color:rgb(64, 64, 64);">ON CLUSTER </font>**<font style="color:rgb(52, 73, 94);">子句。</font>

#### 本地表

+ **<font style="color:rgb(52, 73, 94);">别名</font>**<font style="color:rgb(52, 73, 94);">：物理表、Local 表</font>
+ **<font style="color:rgb(52, 73, 94);">特性</font>**<font style="color:rgb(52, 73, 94);">：</font>
  - <font style="color:rgb(52, 73, 94);">每个节点独立存储实际数据</font>
  - <font style="color:rgb(52, 73, 94);">如果建表时不使用 </font>**<font style="color:rgb(64, 64, 64);">ON CLUSTER</font>**<font style="color:rgb(52, 73, 94);"> 子句，仅会在当前实例创建</font>
  - <font style="color:rgb(52, 73, 94);">直接承载数据写入和查询负载，是实际数据存储表</font>
+ **<font style="color:rgb(52, 73, 94);">引擎：</font>**
  - <font style="color:rgb(52, 73, 94);">分布式集群环境使用副本表引擎 ReplicatedMergeTree；</font>
  - <font style="color:rgb(52, 73, 94);">经常有数据去重或有update修改数据的场景下，建议使用ReplicatedReplacingMergeTree表引擎；</font>

#### 分布式表

+ **<font style="color:rgb(52, 73, 94);">别名</font>**<font style="color:rgb(52, 73, 94);">：逻辑表、Distributed 表</font>
+ **<font style="color:rgb(52, 73, 94);">特性</font>**<font style="color:rgb(52, 73, 94);">：</font>
  - <font style="color:rgb(52, 73, 94);">不存储实际数据，作为本地表的代理层</font>
  - <font style="color:rgb(52, 73, 94);">通过</font>**<font style="color:rgb(52, 73, 94);"> </font>****<font style="color:rgb(64, 64, 64);">Distributed</font>**<font style="color:rgb(64, 64, 64);"> </font><font style="color:rgb(52, 73, 94);">引擎实现跨节点查询路由</font>
  - <font style="color:rgb(52, 73, 94);">写入时自动分发数据到各分片（需配置</font>**<font style="color:rgb(64, 64, 64);"> sharding_key</font>**<font style="color:rgb(52, 73, 94);">）</font>
  - <font style="color:rgb(52, 73, 94);">查询时并行访问所有分片并聚合结果</font>

#### 视图表

+ **<font style="color:rgb(52, 73, 94);">别名</font>**<font style="color:rgb(52, 73, 94);">：虚拟表、逻辑视图</font>
+ **<font style="color:rgb(52, 73, 94);">特性</font>**<font style="color:rgb(52, 73, 94);">：</font>
  - <font style="color:rgb(52, 73, 94);">不存储数据</font><font style="color:rgb(52, 73, 94);">，仅保存查询逻辑</font>
  - <font style="color:rgb(52, 73, 94);">分为</font><font style="color:rgb(52, 73, 94);"> </font><font style="color:rgb(52, 73, 94);">普通视图</font><font style="color:rgb(52, 73, 94);">（每次查询动态计算）和</font><font style="color:rgb(52, 73, 94);"> </font><font style="color:rgb(52, 73, 94);">物化视图</font><font style="color:rgb(52, 73, 94);">（持久化计算结果）</font>
  - <font style="color:rgb(52, 73, 94);">简化复杂查询，提供数据安全层</font>

### 表名

<font style="color:rgb(52, 73, 94);">【强制】规范发布后的后续版本中，产品版本新增表名为模块名+正常表名。产品模块名参考行销团队发布的产品列表。【例外】多个模块公共表，可不设置模块前缀。</font>

<font style="color:rgb(52, 73, 94);">【推荐】项目版本，项目缩写+表名。如PTO项目的表都pto_为前缀。</font>

<font style="color:rgb(52, 73, 94);">【推荐】对于表名还可以增加相应后缀做标识，即成：[项目编码_模块编码_]主体名_后缀，另外，考虑到跨域实体，为了不影响理解，并保证命名的非二义性，可以在主体名前增加“子域名”作为前缀。</font>
<font style="color:rgb(52, 73, 94);">对于主体名，包含三个及三个以上单词的，建议采取缩写方式。</font>
<font style="color:rgb(52, 73, 94);">例如: 客户表 cust</font>
<font style="color:rgb(52, 73, 94);">客户信用度 cust_credit</font>
<font style="color:rgb(52, 73, 94);">客户附加属性 cust_external_attr</font>

<font style="color:rgb(52, 73, 94);">【推荐】表名不使用复数名词。
</font><font style="color:rgb(52, 73, 94);">说明：表名应该仅仅表示表里面的实体内容，不应该表示实体数量。</font>

#### 后缀名参考

| **<font style="color:rgb(44, 62, 80);">表分类</font>** | **<font style="color:rgb(44, 62, 80);">命名要求</font>** |
| -------------------------------------------------------- | ---------------------------------------------------------- |
| <font style="color:rgb(52, 73, 94);">本地表</font>     | <font style="color:rgb(52, 73, 94);">以_local结尾</font> |
| <font style="color:rgb(52, 73, 94);">分布表</font>     | <font style="color:rgb(52, 73, 94);">以_shard结尾</font> |
| <font style="color:rgb(52, 73, 94);">物化视图表</font> | <font style="color:rgb(52, 73, 94);">以_mv结尾</font>    |
| <font style="color:rgb(52, 73, 94);">日志表</font>     | <font style="color:rgb(52, 73, 94);">以_log结尾</font>   |
| <font style="color:rgb(52, 73, 94);">临时表</font>     | <font style="color:rgb(52, 73, 94);">以_tmp结尾</font>   |
| <font style="color:rgb(52, 73, 94);">测试表</font>     | <font style="color:rgb(52, 73, 94);">以_test结尾</font>  |

<font style="color:rgb(52, 73, 94);">注：以上提供的为使用ClickHouse数据库的业务的表后缀,各业务部门需要根据此定义去创建表。原则上不修改已创建业务表。</font>

#### 前缀名参考

| **<font style="color:rgb(44, 62, 80);">表分类</font>**     | **<font style="color:rgb(44, 62, 80);">命名要求</font>**                 |
| ------------------------------------------------------------ | -------------------------------------------------------------------------- |
| <font style="color:rgb(52, 73, 94);">项目业务独特表</font> | <font style="color:rgb(52, 73, 94);">以项目简称开头，例如pto_开头</font> |

<font style="color:rgb(52, 73, 94);"></font>

### 字段名称

#### 字段命名原则

<font style="color:rgb(52, 73, 94);">【强制】不使用Clickhouse的保留字作为字段名，$\color{#ff0000}反例$如role、select等。</font>

<font style="color:rgb(52, 73, 94);">【推荐】字段命名结构如下：BODY(主体名)_SUFFIX（后缀名）</font>
<font style="color:rgb(52, 73, 94);">例如: 客户编码 cust_nbr</font>
<font style="color:rgb(52, 73, 94);">其中，</font>
+ <font style="color:rgb(52, 73, 94);">BODY为主体名，应该能够清楚地说明对象的含义,采用英文缩写；</font>
+ <font style="color:rgb(52, 73, 94);">SUFFIX是后缀名，提供特殊的含义；</font>
+ <font style="color:rgb(52, 73, 94);">字段名称不能出现数据库中的关键字。</font>
  <font style="color:rgb(52, 73, 94);">以下是一些特别的前后缀，代表了这个字段特殊的含义。在其他的情况，应避免使用以下的前后缀：</font>
  | **<font style="color:rgb(44, 62, 80);">前后缀</font>** | **<font style="color:rgb(44, 62, 80);">定义</font>**                                                                                                                                           |
  | -------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
  | <font style="color:rgb(52, 73, 94);">_desc</font>      | <font style="color:rgb(52, 73, 94);">参数表内的描叙字段 如字段名是offer_desc,表示销售品描述</font>                                                                                             |
  | <font style="color:rgb(52, 73, 94);">_flag</font>      | <font style="color:rgb(52, 73, 94);">布尔型字段</font>                                                                                                                                         |
  | <font style="color:rgb(52, 73, 94);">_nbr/no</font>    | <font style="color:rgb(52, 73, 94);">编号字段</font>                                                                                                                                           |
  | <font style="color:rgb(52, 73, 94);">_num/_nbr</font>  | <font style="color:rgb(52, 73, 94);">号码字段</font>                                                                                                                                           |
  | <font style="color:rgb(52, 73, 94);">_id</font>        | <font style="color:rgb(52, 73, 94);">标识字段</font>                                                                                                                                           |
  | <font style="color:rgb(52, 73, 94);">_type</font>      | <font style="color:rgb(52, 73, 94);">类型字段，用来表示有类型含义的字段 如字段名是offer_type，表示销售品类型</font>                                                                            |
  | <font style="color:rgb(52, 73, 94);">is_</font>        | <font style="color:rgb(52, 73, 94);">描述含有是否含义的字段,主数据值只有0/1或者N/Y两种情况，如is_default，表示是否默认 数据类型是FixedString(1)或者String （N/Y）（1表示是，0表示否）。</font> |

<font style="color:rgb(52, 73, 94);">【推荐】表常备三字段：xxx_id, created_date,update_date表示主键、创建时间和更新时间。时间类型均为 datetime类型。</font>

#### 说明字段

<font style="color:rgb(52, 73, 94);">【推荐】描述、备注、说明用字段，使用comments Nullable(String);</font>

#### 状态及状态变更时间字段

<font style="color:rgb(52, 73, 94);">【推荐】状态字段需标明状态值含义，例如COMMENT 'A:有效 X:删除';</font>

<font style="color:rgb(52, 73, 94);">【推荐】状态变更时间state_date DateTime，记录状态最后一次变更时间，支持历史追踪和审计；</font>

<font style="color:rgb(52, 73, 94);">【推荐】定长状态字段使用state String或者FixedString(X) 字段；</font>

#### 时间字段

<font style="color:rgb(52, 73, 94);">【推荐】生成时间用created_date DateTime；</font>

<font style="color:rgb(52, 73, 94);">【推荐】更新时间用update_date DateTime；</font>

<font style="color:rgb(52, 73, 94);">【推荐】竣工时间用completed_date DateTime；</font>

<font style="color:rgb(52, 73, 94);">【推荐】生效时间eff_date DateTime；</font>

<font style="color:rgb(52, 73, 94);">【推荐】失效时间 exp_date DateTime；</font>

<font style="color:rgb(52, 73, 94);">【推荐】记录创建时间rec_created_date DateTime。</font>

#### 工号字段

<font style="color:rgb(52, 73, 94);">【推荐】</font>

| **<font style="color:rgb(44, 62, 80);">字段中文名</font>** | **<font style="color:rgb(44, 62, 80);">字段名</font>** | **<font style="color:rgb(44, 62, 80);">字段类型</font>**          | **<font style="color:rgb(44, 62, 80);">是否可空</font>** | **<font style="color:rgb(44, 62, 80);">描述</font>**                                                                                       |
| ------------------------------------------------------------ | -------------------------------------------------------- | ------------------------------------------------------------------- | ---------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------- |
| <font style="color:rgb(52, 73, 94);">参与方类型</font>     | <font style="color:rgb(52, 73, 94);">party_type</font> | <font style="color:rgb(52, 73, 94);">FixedString(1)/String</font> | <font style="color:rgb(52, 73, 94);">可空，默认值</font> | <font style="color:rgb(52, 73, 94);">描述参与方的类型。A：员工岗位、B：银行、C：客户、E：外系统、O：组织、F:员工等。</font>                |
| <font style="color:rgb(52, 73, 94);">参与方标识</font>     | <font style="color:rgb(52, 73, 94);">party_code</font> | <font style="color:rgb(52, 73, 94);">Int64</font>                 | <font style="color:rgb(52, 73, 94);">可空，默认值</font> | <font style="color:rgb(52, 73, 94);">描述参与方的标识。根据参与方类型的不同，可以是staff_job_id、bank_id、cust_id、org_id、staff_id</font> |

<font style="color:rgb(52, 73, 94);"></font>

| **<font style="color:rgb(44, 62, 80);">字段中文名</font>** | **<font style="color:rgb(44, 62, 80);">字段名</font>**   | **<font style="color:rgb(44, 62, 80);">字段类型</font>** | **<font style="color:rgb(44, 62, 80);">是否可空</font>** | **<font style="color:rgb(44, 62, 80);">描述</font>**               |
| ------------------------------------------------------------ | ---------------------------------------------------------- | ---------------------------------------------------------- | ---------------------------------------------------------- | -------------------------------------------------------------------- |
| <font style="color:rgb(52, 73, 94);">创建人</font>         | <font style="color:rgb(52, 73, 94);">create_staff</font> | <font style="color:rgb(52, 73, 94);">Int64</font>        | <font style="color:rgb(52, 73, 94);">可空，默认值</font> | <font style="color:rgb(52, 73, 94);">描述创建记录的员工标识</font> |
| <font style="color:rgb(52, 73, 94);">修改人</font>         | <font style="color:rgb(52, 73, 94);">update_staff</font> | <font style="color:rgb(52, 73, 94);">Int64</font>        | <font style="color:rgb(52, 73, 94);">可空，默认值</font> | <font style="color:rgb(52, 73, 94);">描述更新记录的员工标识</font> |

<font style="color:rgb(52, 73, 94);"></font>

<font style="color:rgb(52, 73, 94);">【推荐】注意Nuallable字段会对性能有影响，额外的bitmap	开销/计算逻辑增加，对NULL值额外做处理，谨慎使用。建议正常使用字段类型，默认值为负数，来标识为空字段。约定非法值代表null -> -999。</font>

<font style="color:rgb(52, 73, 94);"></font>

### 字段数据类型

<font style="color:rgb(52, 73, 94);">【强制】布尔值字段：使用Bool 类型字段，需加上DEFAULT 默认值。</font>

<font style="color:rgb(52, 73, 94);">【强制】固定长度字符串：使用FixedString(n),长度根据需要定义。</font>

<font style="color:rgb(52, 73, 94);">【强制】可变字符串字段：使用String/LowCardinality(String)数据类型。</font>

<font style="color:rgb(52, 73, 94);">【强制】日期型字段：统一使用 DateTime相关日期数据类型。</font>

<font style="color:rgb(52, 73, 94);">【推荐】枚举值数量 ≤ 10000 的字符串字段建议使用 LowCardinality(String) 数据类型，并在 COMMENT 中说明枚举值含义。</font>

> <font style="color:rgb(52, 73, 94);">低基数维度：根据官方建议和实践经验，在纬度基数小于1万的时候，对维度字段做LowCardinality编码，导入性能会有略微下降，查询性能提升明显，数据存储空间下降明显。</font>

<font style="color:rgb(52, 73, 94);">【推荐】版本ver类型（ReplicatedReplacingMergeTree表引擎字段，主要用于在分区内去重）时间字段建议使用DateTime64，默认值为 now()。</font>

<font style="color:rgb(52, 73, 94);">【推荐】数值字段：使用Int/decimal/UInt数据类型，无小数，根据所存放的数据大小选择合适的子类型。任何字段如果为非负数，必须是UInt。</font>

<font style="color:rgb(52, 73, 94);">【推荐】合适的字符存储长度，不但节约数据库表空间、节约索引存储，更重要的是提升查询速度。</font>

<font style="color:rgb(52, 73, 94);">【推荐】从性能考虑能用数字表达的不使用字符串。</font>

<font style="color:rgb(52, 73, 94);">【推荐】如果表中不是必须保留全量历史数据，建议指定TTL，可以免去手动过期历史数据的麻烦。</font>

<font style="color:rgb(52, 73, 94);">【推荐】尽量不要使用Nullable类型,该类型对性能有一定影响,且不能包含在索引中。</font>

<font style="color:rgb(52, 73, 94);">【推荐】优先使用数值类型或时间戳（数值化存储）。</font>

<font style="color:rgb(52, 73, 94);">【推荐】所有字段选择按照最小范围原则。根据业务场景所需选择最小满足的类型使用。</font>

| **使用场景**                              | **类型推荐**   |
| ------------------------------------------- | ---------------- |
| 固定长度字段                              | FixedString(N) |
| 日志、文本、备注、URL、JSON字段等变长内容 | String         |

### 字段注释

<font style="color:rgb(52, 73, 94);">【推荐】字段取值如果可以枚举，并且无对应域表时，需要在字段注释中针对每个字段取值进行枚举和含义解释。</font>

<font style="color:rgb(52, 73, 94);">【推荐】要求每个字段有注释，默认中文便于理解，部分项目不能出现中文时用英文注释，或者在生成脚本时，配置管理员选择不生成注释的方式完成。</font>

<font style="color:rgb(52, 73, 94);">【推荐】字段取值非枚举，但一些特殊取值有特定的含义，比如：NULL值用于区分是优惠还是原费用的税记录，需要在字段注释中说明。</font>

<font style="color:rgb(52, 73, 94);">【推荐】字段注释、domain和配置表的区分使用：如果仅仅代码用于判断使用的字段，无需在界面展示，则可用字段注释说明字段取值含义。如prod表state字段，
</font><font style="color:rgb(52, 73, 94);">subs_goods_inst表的state字段,acct表的state等字段。domain表和配置表的使用由设计时具体分析判断。</font>

<font style="color:rgb(52, 73, 94);">【推荐】主键备注写明对应的序列。</font>

<font style="color:rgb(52, 73, 94);">【推荐】如果修改字段含义或对字段表示的状态追加时，需要及时更新字段注释，以及检查该字段是否在同步任务中。

</font>

### 主键-排序键-分区建

#### 主键

<font style="color:rgb(52, 73, 94);">【强制】主键在任何情况下不允许被更新。</font>

<font style="color:rgb(52, 73, 94);">【推荐】主键最好设计成单一主键，但是也可以使用复合主键。</font>

<font style="color:rgb(52, 73, 94);">【推荐】主键优先选择数值类型字段，避免字符串类型，尤其是 UUID、MD5、HASH 等。</font>

+ ⚠️<font style="color:rgb(52, 73, 94);"> 原因：字符串作为主键会增加存储空间和索引计算开销。</font>

#### 排序键

<font style="color:rgb(52, 73, 94);">【推荐】</font>**<font style="color:rgb(64, 64, 64);">ORDER BY</font>**<font style="color:rgb(52, 73, 94);"> 首列必须是高频过滤条件（查询中常用于 WHERE 条件，访问比例 ≥ 30% 的查询）。</font>

<font style="color:rgb(52, 73, 94);">【推荐】排序键字段数量建议控制在 1~3 个之间，字段应为常用于查询筛选或范围过滤的高区分度字段。</font>

<font style="color:rgb(52, 73, 94);">【推荐】避免使用低基数字段（如性别）作为排序键首列，否则范围查询可能会扫描大量数据。</font>

#### 分区键

<font style="color:rgb(52, 73, 94);">【强制】单表导分区数量要合理，分区过多，会因需要打开的文件描述符过多导致查询效率不佳。单表总分区数 ≤ 2000（依据集群节点数和数据量）；</font>

<font style="color:rgb(52, 73, 94);">【强制】ClickHouse的分布式表性能性价比不如物理表高，分区字段过多会导致数据导入过程磁盘可能会被打满。分区字段数量 1~2 个，绝对上限：不超过 3 个字段；</font>

<font style="color:rgb(52, 73, 94);">【强制】不要在唯一列或大基数列上进行分组或去重操作，基数太大（> 10^6）会消耗过多的io和内存。</font>

<font style="color:rgb(52, 73, 94);">【推荐】建议表要指定分区键,尤其是数据量达到亿级别的表，插入/查询/合并都是以分区为单位，合理的分区可以提升整体性能。</font>

<font style="color:rgb(52, 73, 94);">【推荐】合理设置分区，所有本地表使用order by关键字指定分区字段，建议采用日期toYYYYMMDD作为一级分区。</font>

<font style="color:rgb(52, 73, 94);">【推荐】如果保存多年数据，建议考虑使用月做分区，toYYYYMM。</font>

<font style="color:rgb(52, 73, 94);">【推荐】查询时如果可以建议带上分区键查询,可以有效减少数据扫描量,提升查询效率。</font>

### 约束

<font style="color:rgb(52, 73, 94);">【强制】不允许使用update/delete。</font>

<font style="color:rgb(52, 73, 94);">【推荐】尽量保证每个表的约束完整，仅针对有特殊性能或者数据归档需求时不需要约束。</font>

<font style="color:rgb(52, 73, 94);">【推荐】建议规划好业务需要的列，必要时可提前预置一些属性列，避免频繁的增删列。</font>

<font style="color:rgb(52, 73, 94);">【推荐】不适合高并发写入，最好还是从异步化队列写入，batch insert 5w-10w 起步，尽量不要执行单条或插入操作，会产生大量小分区文件，给后台merge任务带来巨大压力。</font>

<font style="color:rgb(52, 73, 94);">【推荐】数据在写入ClickHouse前预先的对数据进行分组，避免一次插入的数据属于多个分区。</font>

<font style="color:rgb(52, 73, 94);"></font>

### 表引擎

<font style="color:rgb(52, 73, 94);">【推荐】建表都需要加上on cluster搭配replicatedMergetree表引擎。</font>

<font style="color:rgb(52, 73, 94);">【推荐】表引擎尽量选择 ReplicatedMergeTree，去重使用ReplicatedReplacingMergeTree。</font>

### 大表的数据保留策略

<font style="color:rgb(52, 73, 94);">【推荐】大表（数据量 ≥ 1 亿行，或表大小 ≥ 500GB）需要有明确的数据保留策略。在设计阶段，需要明确业务字段的生命周期，并与数据生命周期匹配，制定表的数据迁移、归档、保留等策略。</font>

<font style="color:rgb(52, 73, 94);">【推荐】在表的物理设计阶段，建议每个表都添加几个有用的字段：记录创建日期、状态时间等，有助于分析记录中出现null数据或者数据丢失的原因，并辅助执行数据迁移/归档策略。</font>

### 临时表的清理机制

<font style="color:rgb(52, 73, 94);">【强制】临时表需要业务本身考虑清理机制。业务确实需用中间临时表，设计时必须要考虑清理机制。</font>

<font style="color:rgb(52, 73, 94);">【推荐】个人备份或临时表，必须使用维护用户创建，个人表以pers_创建人名字全称_为前缀，以跟业务用的临时表区分开，防止运维事故。</font>

## ClickHouse 索引规范

### 索引命名规范

<font style="color:rgb(52, 73, 94);">【强制】ClickHouse 的索引名称应遵循统一命名规范：跳跃索引（data skipping index）：采用 idx_表名_字段名 格式，例如：idx_order_number。</font>

<font style="color:rgb(52, 73, 94);">【推荐】如索引名超30字符，则缩写表名和字段名：例如 idx_osi_cd（order_subs_info 的 created_date 字段）。
</font>

### 索引使用规范

<font style="color:rgb(52, 73, 94);">【强制】必须为 MergeTree 表设置合适的排序键（ORDER BY），以利用稀疏索引优化查询性能。</font>

<font style="color:rgb(52, 73, 94);">【强制】必须为MergeTree系列表定义排序键，以支持主键索引跳跃。例如：ORDER BY (user_id, event_time)；跳跃索引是 ClickHouse 中的一种辅助索引机制，通过对数据块进行预计算摘要信息，在查询时快速跳过不相关的数据块，从而大幅减少扫描数据量。</font>

<font style="color:rgb(52, 73, 94);">【强制】跳跃索引必须显式声明，不会自动创建，适用于低基数字段或范围查询字段的优化。</font>

<font style="color:rgb(52, 73, 94);">【推荐】对于低基数但查询倾向性强的字段，使用 数据跳跃索引（Data Skipping Index），提高查询效率。
</font><font style="color:rgb(52, 73, 94);">            ALTER TABLE prod ADD INDEX idx_prod_state prod_state TYPE set(0) GRANULARITY 1;</font>

<font style="color:rgb(52, 73, 94);">【推荐】不建议在区分度极低的列上建立跳跃索引（如性别字段）。但若对某个值（如性别=“女”）频繁查询，则仍可考虑加索引。</font>

<font style="color:rgb(52, 73, 94);">【推荐】对于参与关联查询的字段（如user_id、order_id等），应在排序键中体现或使用跳跃索引优化。</font>

<font style="color:rgb(52, 73, 94);">【推荐】ClickHouse 所有基于 MergeTree 的表都会自动维护稀疏索引，该索引由排序键（primary key）字段定义，索引点位于每个数据块（granule）首行，默认每 8192 行记录一个索引点。</font>

<font style="color:rgb(52, 73, 94);">【推荐】避免使用低区分度字段（如性别、是否标记）作为排序键，会导致跳跃索引失效。</font>

<font style="color:rgb(52, 73, 94);">【推荐】稀疏索引无法像传统索引那样逐行索引，但对于范围查询、时间过滤等批量检索性能极高。</font>

<font style="color:rgb(52, 73, 94);">【推荐】排序键定义也影响数据分片后的局部性，排序键字段尽可能与查询条件字段、分片键字段对齐。</font>

### 索引策略说明

<font style="color:rgb(52, 73, 94);">ClickHouse不支持B-Tree索引，传统意义上的“建索引”在ClickHouse中主要体现在：
</font><font style="color:rgb(52, 73, 94);">主键索引（Primary Index） 一级索引设计
</font><font style="color:rgb(52, 73, 94);">数据跳跃索引（Skip Index / Secondary Index）

</font><font style="color:rgb(52, 73, 94);">示例（跳跃索引）：
</font><font style="color:rgb(52, 73, 94);">ALTER TABLE user_log
</font><font style="color:rgb(52, 73, 94);">ADD INDEX idx_user_event_type event_type TYPE set(0) GRANULARITY 1;
</font>

### 索引个数限制规范

<font style="color:rgb(52, 73, 94);">【推荐】每张表跳跃索引（data skipping index）建议不超过5个，避免因索引过多影响写入性能。</font>

<font style="color:rgb(52, 73, 94);">【推荐】排序键字段数量也建议控制在3个以内，排序键越复杂，写入开销越大。</font>

### 其他

<font style="color:rgb(52, 73, 94);">【强制】不在布尔值字段上建立索引。</font>

<font style="color:rgb(52, 73, 94);">【推荐】避免冗余和重复索引。尽量使用复合索引，而不是添加新的索引；</font>

<font style="color:rgb(52, 73, 94);">【推荐】ClickHouse 的数据跳跃索引可以对含有空值（NULL）或默认值的字段建立索引，可考虑在字段非空的场景中再使用索引，或搭配 IS NOT NULL 条件查询提高效果。对于Nullable字段，推荐配合 WHERE column IS NOT NULL AND column = xxx 使用索引。</font>

## Clickhouse分布式数据库补充规范

<font style="color:rgb(52, 73, 94);">这里描述的是在Clickhouse数据库规范基础上，使用分布式集群数据库时补充的一些规范要求。</font>

### 基本规范

<font style="color:rgb(52, 73, 94);">【强制】不同业务需要进行资源隔离。在业务规划时，不同业务归属于不同数据库。</font>

<font style="color:rgb(52, 73, 94);">【强制】不要在system库下创建业务表；</font>

<font style="color:rgb(52, 73, 94);">【强制】同一个分布式集群内，相同表名的表结构必须一致，禁止连接单点数据库修改表结构且不加on cluster。</font>

<font style="color:rgb(52, 73, 94);">【强制】表结构变更（如ALTER）必须在所有副本节点上同步执行，避免副本重连失败。执行DDL语句添加on cluster 可保证一致性；</font>

<font style="color:rgb(52, 73, 94);">【强制】DDL 禁止在高并发 DML 期间执行；</font>

<font style="color:rgb(52, 73, 94);">【推荐】实际业务实践中，DDL与DML需要分离；</font>

<font style="color:rgb(52, 73, 94);">【推荐】尽量不去使用字符串类型,时间类型最终会转换成数值类型进行处理,数值类型在执行效率和存储上远好过字符串。

</font>

### 分片规范

<font style="color:rgb(52, 73, 94);">【强制】分布式表必须明确指定分片键（sharding key），以确保数据尽量均匀分布在各个分片上，避免热点分片导致查询或写入瓶颈。</font>

<font style="color:rgb(52, 73, 94);">【强制】分片键字段必须在分布式表和底层本地表中均存在，否则可能导致分片失败或查询错误。

【推荐】优先选择高基数、均匀分布、业务常用查询维度作为分片键，例如用户ID、订单ID等。

<font style="color:rgb(52, 73, 94);">【推荐】常见分片键选型示例：用户类业务：user_id;设备类业务：device_id;交易类业务：order_id。<font style="color:rgb(52, 73, 94);">

【推荐】避免使用时间字段作为唯一分片键，时间分片容易产生数据倾斜。</font>

<font style="color:rgb(52, 73, 94);">【推荐】shard_weight可用于数据倾斜控制场景，如主机性能不同或地域数据集中特殊分片上。

</font><font style="color:rgb(52, 73, 94);">【推荐】增加分片数据，节点数增长为2的倍数（如2、4、6等），便于扩容和故障切换策略规划。

</font>

### 副本规范

<font style="color:rgb(52, 73, 94);">【强制】所有关键业务表在分布式集群中必须启用副本表引擎机制，确保数据高可用。</font>

<font style="color:rgb(52, 73, 94);">【强制】建表元数据路径中使用的副本名、分片名使用宏变量。示例如下：表名需要按实际情况变更，尤其是路径里的表名 ReplacedMergeTree('/clickhouse/tables/{shard}/{database}/</font><font style="color:rgb(52, 73, 94);background-color:#FBDE28;">order</font><font style="color:rgb(52, 73, 94);">', '{replica}')，除了表名，其他路径不允许变更。</font>

```shell
CREATE TABLE order on cluster ck_cluster(
        id UInt32,
        timestamp DateTime,
        value Float64
    ) ENGINE = ReplacedMergeTree('/clickhouse/tables/{shard}/{database}/order', '{replica}')
    PARTITION BY toYYYYMM(timestamp)
    ORDER BY (id, timestamp);
```

<font style="color:rgb(52, 73, 94);">【强制】副本间表结构必须完全一致，包括列定义、表引擎、排序键、TTL设置等。</font>

<font style="color:rgb(52, 73, 94);">【强制】副本同步使用底层ReplicatedMergeTree引擎,提升副本同步性能以及数据一致性。</font>

<font style="color:rgb(52, 73, 94);">【推荐】使用两副本（共两份数据）（ReplicatedMergeTree）配置及以上。</font>

<font style="color:rgb(52, 73, 94);">【推荐】新增副本节点时，需使用原始备份或通过 clickhouse-backup 工具恢复结构和数据，避免直接 copy 元数据。

</font>

### 逻辑视图设计规范

<font style="color:rgb(52, 73, 94);">【推荐】业务逻辑上有很多比较复杂的SQL运算，可以封装为一个视图，后续查询时只能查询视图，简化业务查询使用。</font>

<font style="color:rgb(52, 73, 94);">【推荐】如果业务间有权限隔离诉求，可将部分数据查询封装到视图中，使用视图方只能看到视图下有限行及列的数据。

</font>

### 数据入库规范

<font style="color:rgb(52, 73, 94);">【推荐】写本地表，查询分布式表，提升写入和查询性能，保证写入和查询的数据一致性。</font>

<font style="color:rgb(52, 73, 94);">【推荐】多副本并行导入。 有大数据的导入场景，建议将数据提前拆分成多份，在一个shard内的多个副本同时导入，以分摊一个节点导入数据的压力，同时能提升数据入库的性能，缩短入库时间。</font>

<font style="color:rgb(52, 73, 94);">【推荐】慎用分布式表批量插入：</font>

> + 数据会分发到集群的所有本地表，每个本地表插入的数据量是总插入量的1/N。
> + 如果batch size较小，可能导致data part过多，merge压力变大，甚至出现异常影响数据插入。
> + 数据的一致性问题：数据先在分布式表写入节点的主机落盘，然后数据被异步地发送到本地表所在主机进行存储，中间没有一致性的校验，如果分布式表写入数据的主机出现宕机，会导致数据丢失风险。
> + 分布式表和数据写入性能也会变慢，单批次分布式表写，写入节点的磁盘和网络IO会成为性能瓶颈点。
> + 分布式表转发给各个shard成功与否，插入数据的客户端无法感知，转发失败的数据会不断重试转发，消耗CPU。

<font style="color:rgb(52, 73, 94);">【推荐】大批量数据导入要分时、分节点、扩容：</font>

> + 如果数据盘为SATA盘，当大批量数据集中插入时候，会抢占磁盘，使得磁盘长时间处于繁忙状态，影响其他alter类操作的效率。
> + 尽量避免批量导数据的SQL并发执行，会给磁盘和ClickHouse并发能力带来冲击。

### 数据查询规范

<font style="color:rgb(52, 73, 94);">【强制】禁止 select * 查询：只查询需要的字段可以减少磁盘 IO 和网络 IO，提升查询性能。</font>

<font style="color:rgb(52, 73, 94);">【强制】关联查询必须大表join小表，即小表在右原则：</font>

> + 对于ClickHouse来说，通常需要将多表JOIN模型提前加工为宽表模型。但在某些情况下，如果维度表变化频繁，则不适合进行宽表加工处理。
> + 如果不得不使用JOIN模型以实时查询到最新数据，建议两表JOIN，并且大表JOIN小表。
> + 小表的数据量控制在百万到千万级别，并且需要在JOIN前尽量把小表数据通过条件进行有效过滤。

<font style="color:rgb(52, 73, 94);">【推荐】使用 uniqCombined 替代 distinct：uniqCombined 对去重逻辑进行了优化，通过近似去重提升十倍查询性能。如果对查询允许有误差，可以使用 uniqCombined 替代 distinct 语法。</font>

<font style="color:rgb(52, 73, 94);">【推荐】建议使用 limit 限制返回数据条数使用limit返回指定的结果集数量，不会进行向下扫描，大大提升了查询效率。</font>

<font style="color:rgb(52, 73, 94);">【推荐】降低对表的修改频次：默认场景下 ClickHouse 执行 alter 语句是异步执行，对同一张表频繁执行 alter 操作可能导致业务失败。</font>

<font style="color:rgb(52, 73, 94);">【推荐】多表复杂 join 拆分为两表 join 或子查询：多表复杂 join 场景，建议拆分为两两表 join，且两表 join 为大小表 join、小大表 join，尽量避免大大表 join。也可以将多表复杂 join 拆分为子查询模式。</font>

<font style="color:rgb(52, 73, 94);">【推荐】多表查询性能较差，多表Join时要满足小表在右的原则，右表关联时被加载到内存中与左表进行比较，ClickHouse中无论是Left Join 、Right Join还是Inner Join永远都是拿着右表中的每一条记录到左表中查找该记录是否存在，所以右表必须是小表。</font>

<font style="color:rgb(52, 73, 94);">【推荐】join/in/not in需要添加Global关键字：在进行JOIN、IN或NOT IN操作时，需要在前面添加Global关键字，避免查询放大问题。</font>

<font style="color:rgb(52, 73, 94);">【推荐】当多表联查时，查询的数据仅从其中一张表出时，可考虑使用IN操作而不是JOIN。</font>

<font style="color:rgb(52, 73, 94);">【推荐】建议查询指定分区：通过指定分区字段会减少底层数据库扫描的文件数量，提升查询性能。</font>

> 实际经验：700个分区的列大表，需要查询一个分区中有7000万数据，其他699个分区中无数据。虽然只有一个分区有数据，其他分区无数据，但是查询指定分区为百毫秒级性能，没有指定分区查询性能为1~2秒左右，性能相差20倍。

<font style="color:rgb(52, 73, 94);">【推荐】慎用final查询：</font>

> 在查询语句的最后跟上final，通常是对ReplacingMergeTree引擎，数据不能完全去重情况下，有些开发人员习惯写final关键字进行实时合并去重操作（merge-on-read），保证查询数据无重复数据。可以通过argMax函数或其他方式规避此问题。

<font style="color:rgb(52, 73, 94);"></font>

### 数据修改规范

<font style="color:rgb(52, 73, 94);">【强制】禁止在业务高峰期修改索引列：修改期间会触发重建索引，期间查询数据不准确。</font>

<font style="color:rgb(52, 73, 94);">【推荐】建议慎用delete、update的mutation操作</font>

> + 标准SQL中的update和delete操作是同步的，客户端会等待服务端返回执行结果。而在ClickHouse中，这些操作是异步执行的。当执行update或delete语句时，服务端会立即返回一个结果，但实际的数据修改可能还没有完成，还在后台排队处理。
> + 这种异步执行可能导致操作被覆盖，并且无法保证操作的原子性。因此，建议谨慎使用这些操作。

<font style="color:rgb(52, 73, 94);">【推荐】对于批量数据清理，建议根据分区来操作。</font>

<font style="color:rgb(52, 73, 94);"></font>

### 数据merge规范

<font style="color:rgb(52, 73, 94);">【推荐】建议谨慎执行 optimize 操作。Optimize 一般会对表做重写操作，建议在业务压力小时进行操作，否则对 IO/MEM/CPU 资源有较大消耗，导致业务查询变慢或不可用。</font>

<font style="color:rgb(52, 73, 94);"></font>

# 附录

## 数值类型范围

|                                                     Type                                                     | Range                                                                                                                                                            |
| :-------------------------------------------------------------------------------------------------------------: | ------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
|  **<font style="color:rgb(0, 0, 0) !important;background-color:rgb(245, 245, 245) !important;">Int8</font>**  | [-128 : 127]                                                                                                                                                     |
| **<font style="color:rgb(0, 0, 0) !important;background-color:rgb(245, 245, 245) !important;">Int16</font>** | [-32768 : 32767]                                                                                                                                                 |
| **<font style="color:rgb(0, 0, 0) !important;background-color:rgb(245, 245, 245) !important;">Int32</font>** | [-2147483648 : 2147483647]                                                                                                                                       |
| **<font style="color:rgb(0, 0, 0) !important;background-color:rgb(245, 245, 245) !important;">Int64</font>** | [-9223372036854775808 : 9223372036854775807]                                                                                                                     |
| **<font style="color:rgb(0, 0, 0) !important;background-color:rgb(245, 245, 245) !important;">Int128</font>** | [-170141183460469231731687303715884105728 : 170141183460469231731687303715884105727]                                                                             |
| **<font style="color:rgb(0, 0, 0) !important;background-color:rgb(245, 245, 245) !important;">Int256</font>** | [-57896044618658097711785492504343953926634992332820282019728792003956564819968 : 57896044618658097711785492504343953926634992332820282019728792003956564819967] |

|                                                      Type                                                      | Range                                                                                |
| :--------------------------------------------------------------------------------------------------------------: | -------------------------------------------------------------------------------------- |
| **<font style="color:rgb(0, 0, 0) !important;background-color:rgb(245, 245, 245) !important;"> UInt8</font>** | [0 : 255]                                                                            |
| **<font style="color:rgb(0, 0, 0) !important;background-color:rgb(245, 245, 245) !important;">UInt16</font>** | [0 : 65535]                                                                          |
| **<font style="color:rgb(0, 0, 0) !important;background-color:rgb(245, 245, 245) !important;">UInt32</font>** | [0 : 4294967295]                                                                     |
| **<font style="color:rgb(0, 0, 0) !important;background-color:rgb(245, 245, 245) !important;">UInt64</font>** | [0 : 18446744073709551615]                                                           |
| **<font style="color:rgb(0, 0, 0) !important;background-color:rgb(245, 245, 245) !important;">UInt128</font>** | [0 : 340282366920938463463374607431768211455]                                        |
| **<font style="color:rgb(0, 0, 0) !important;background-color:rgb(245, 245, 245) !important;">UInt256</font>** | [0 : 115792089237316195423570985008687907853269984665640564039457584007913129639935] |

<font style="color:rgb(52, 73, 94);"></font>

## SQL/ClickHouse 常见保留字清单

### 通用 SQL 保留字（部分）

避免直接使用以下关键字作为库名、表名、字段名。

```sql
select, insert, update, delete, from, where, group, having, order, by,
desc, asc, into, values, create, alter, drop, truncate, table, view,
index, key, primary, foreign, unique, constraint, check, null, not,
and, or, in, like, join, inner, left, right, full, union, distinct,
as, case, when, then, else, end
```

### ClickHouse 特有保留字（部分）

ClickHouse 在语法中有一些额外保留字，尤其是 **表引擎、分区、索引相关**，应避免使用。

```sql
database, system, partition, partitions, sample, settings, format,
engine, codec, ttl, type, merge, replace, dictionary, exists, show,
describe, optimize, sync, detach, attach, flush, kill, mutations,
row, rows, offset, limit
```

