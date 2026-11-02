<blockquote class="read-author-info">
<p>文档路径：epg/岗位能力认证/浩鲸在线规范库/Oracle规范/SQL开发规范(Oracle分册)<svg class="copy-doc-path" style="cursor: pointer; margin-left: 8px; vertical-align: middle;" title="复制文档路径" data-doc-path="epg/岗位能力认证/浩鲸在线规范库/Oracle规范/SQL开发规范(Oracle分册)" width="14" height="14" viewBox="0 0 1024 1024" xmlns="http://www.w3.org/2000/svg"><path fill="currentColor" d="M768 832a128 128 0 0 1-128 128H192A128 128 0 0 1 64 832V384a128 128 0 0 1 128-128v64a64 64 0 0 0-64 64v448a64 64 0 0 0 64 64h448a64 64 0 0 0 64-64h64z"/><path fill="currentColor" d="M384 128a64 64 0 0 0-64 64v448a64 64 0 0 0 64 64h448a64 64 0 0 0 64-64V192a64 64 0 0 0-64-64H384zm0-64h448a128 128 0 0 1 128 128v448a128 128 0 0 1-128 128H384a128 128 0 0 1-128-128V192A128 128 0 0 1 384 64z"/></svg></p>
</blockquote>

![image](uploads/4061/2a99b098-0e70-4750-bf21-7a135a42abc3/PG_dev_Oracle.png)

# 概述

## 编写目的

- 统一SQL语句编写格式。
- 让SQL语句更美观，更易阅读。
- 增强SQL可维护性。
- 避免低效SQL导致的性能问题。

## 适用范围

在使用Oracle 9i及其后版本中创建和维护存储过程、Function、视图、Trigger等数据库对象时，需遵循此规范。在C/C++、Java等各种编程语言中编写SQL语句时，需要遵循此规范。

## 角色和职责

开发：负责按照SQL规范进行SQL编码

运维人员：负责根据SQL规范编写运维需要的SQL脚本

# 命名规则

本章主要约定在数据库编程中为数据库对象、变量命名的规则。如给一个存储过程、视图、Package等对象命名，或者给存储过程中的出入参、内部变量命名。

**数据库对象的命名格式：*ObjectTypeAb\[\_ProjectName\]\[\_SubSystemNameAb\]\_ObjectNameAb*，各部分直接使用下划线隔开。**

| **数据库对象**    | **说明**                                             |
|-------------------|------------------------------------------------------|
| *ObjectTypeAb*    | 数据库对象类型的缩写。                               |
| *ProjectName*     | 项目名称，表示此数据库对象为哪个项目所专用，可选项。 |
| *SubSystemNameAb* | 数据库对象所属子系统(功能域)名的缩写，可选项。       |
| *ObjectNameAb*    | 数据库对象有意义的名子的缩写。                       |

*Note：ObjectTypeAb*的缩写规则参看《数据模型设计规范\_Oracle分册.docx》中对象命名规范。

## 数据库对象命名

本节规范了数据库对象命名的总体原则。

### 【强制】数据库命名对象遵循大写方式

**说明**：

在编写SQL脚本时，数据库命名对象应统一保持大写风格。

**<font color=red>反例</font>**

```sql
CREATE OR REPLACE PROCEDURE p_init_sp
```

**正例**

```sql
CREATE OR REPLACE PROCEDURE P_INIT_SP
```

**检查方式**：工具检查（暂未支持）

### 【参考】名字要清晰并且容易理解

**<font color=red>反例</font>**

```sql
CREATE OR REPLACE PROCEDURE TMP1
```

*[说明] 存储过程命名含义不明确，无法被理解。*

**正例**

```sql
CREATE OR REPLACE PROCEDURE P_INIT_SP
```

*[说明] 一目了然知道这个存储过程是用来初始化SP的。*

**检查方式**：人工检查

### 【参考】名字要使用同一种语法，一律使用英语

**说明：**

政企项目例外，允许使用汉语拼音。

**检查方式**：人工检查

## 变量命名

### 输入/输出参数

**输入/输出标记：**

&ensp;​&ensp; I表示输入参数

&ensp;​&ensp; O表示输出参数

**数据类型标记：**

&ensp;​&ensp; N表示NUMBER/LONG/INTEGER型

​&ensp;​&ensp; V表示VARCHAR2型

​&ensp;​&ensp; D表示DATE型

&ensp;​&ensp; C表示CHAR型

&ensp;​&ensp; B表示LOB型（BLOB/CLOB）

#### 【强制】存储过程、Function等对象的参数要明确写出输入输出类型(IN/OUT/IN\_OUT)

**检查方式**：工具检查（暂未支持）

#### 【强制】以“输入/输出标记”+“数据类型标记”作为前缀

**检查方式**：工具检查（暂未支持）

#### 【强制】输入/输出参数全部大写

**检查方式**：工具检查（暂未支持）

#### 【推荐】输入/输出参数单词之间使用下划线“\_”分隔

**正例**

```sql
IN_EVENT_ID，表示一个NUMBER类型的输入参数
```

**检查方式**：人工检查

### 变量

#### 【推荐】以数据类型标记作为前缀，为小写字符

**检查方式**：人工检查

#### 【参考】尽量使用能够表达用意的英文单词，不使用汉语拼音

**说明**：

政企项目例外，允许使用汉语拼音。

**检查方式**：人工检查

#### 【强制】单词之间不使用任何分隔符

**检查方式**：人工检查

#### 【推荐】前缀之后的所有单词第一个字母大写，其他字母小写（即Pascal格式）

**检查方式**：人工检查

#### 【参考】尽量引用数据库实体类型，如：表名.字段%TYPE，避免由于数据库结构变更引起变量声明的变更

**<font color=red>反例</font>**

```sql
（1）nFlag NUMBER
```

*[说明]含义不明，不易理解*

**正例**

```sql
（1）nSubsId NUMBER  -- id of subscriber
（2）vProdState VARCHAR2(2)  -- state of product
（3）nEventId SUBS_EVENT.EVENT_ID%type
```

**检查方式**：人工检查

### 常量

#### 【强制】常量名全部大写

**检查方式**：人工检查

#### 【参考】常量名能够直观的表达其用意

**检查方式**：人工检查

#### 【推荐】常量名单词之间使用下划线“\_”分隔

**检查方式**：人工检查

# PL/SQL书写与布局

本章约定了数据库对象中的SQL语句的书写格式与布局。

对于Java Source、C/C++程序中编写的SQL语句，建议在最大程度上遵循此规范。无法适用此规范的场景可以自行考虑格式，但必须遵循“格式整齐、美观大方”的总体原则。

## 书写

### 【强制】SQL语句的所有表名、字段名全部大写，系统保留字、内置函数名、SQL保留字也大写

**<font color=red>反例</font>**

```sql
SELECT
	subs_id,
	prefix,
	acc_nbr
 FROM
	Subs
WHERE
	Subs_Id = 10001
```

**正例**

```sql
SELECT
	SUBS_ID,
	PREFIX,
	ACC_NBR
 FROM
	SUBS
WHERE
	SUBS_ID = 10001
```

**检查方式**：工具检查

### 【强制】使用INSERT时，必须指定插入的字段名，严禁不指定字段名直接插入VALUES

**<font color=red>反例</font>**

```sql
INSERT INTO SUBS 
VALUES (nSubsId, vPrefix, vAccNbr, ......)
```

**正例**

```sql
INSERT INTO SUBS (SUBS_ID,PREFIX,ACC_NBR, .....) 
VALUES (nSubsId, vPrefix, vAccNbr, ......)
```

**检查方式**：工具检查

## 空格

### 【强制】＝、<=、>=、<\>等符号前后加上一个空格

**检查方式**：工具检查（暂未支持）

### 【强制】逗号之后必须接一个空格或换行

**检查方式**：工具检查

### 【强制】关键字、保留字和左括号之间必须有一个空格或换行

**正例**

```sql
SELECT
	A.SUBS_ID,
	A.PREFIX,
	A.ACC_NBR,
	B.PROD_STATE,
	C.SERV_TYPE
 FROM
	SUBS A,
	PROD B,
	INDEP_PROD_SPEC C
WHERE
      A.SUBS_ID = B.PROD_ID
  AND B.PROD_SPEC_ID = C.INDEP_PROD_SPEC_ID
  AND B.PROD_STATE NOT IN ('B', 'F')
  AND B.CREATED_DATE >= : CREATE_DATE
```

**检查方式**：工具检查

## 缩进

### 【强制】最外层的CREATE、BEGIN、END等关键字要顶格书写

**检查方式**：工具检查（暂未支持）

### 【强制】对于存储过程、Function、视图等数据库对象，缩进为4个空格，禁止使用TAB符号

**检查方式**：工具检查（暂未支持）

## 换行

### SQL语句的向右缩进风格

#### 【推荐】 一行有多列，超过120个字符时，基于列对齐原则，采用下行向右缩进；也可以一列一行。

**正例**

```sql
SELECT B.ACC_NBR, B.PREFIX, B.PRICE_PLAN_ID,
       A.COMPLETED_DATE
  FROM PROD A,
       SUBS B
 WHERE A.PROD_ID = B.SUBS_ID
   AND A.PROD_STATE = 'A'
   AND B.PRICE_PLAN_ID = 101
```

**检查方式**：工具检查（暂未支持）

#### 【强制】WHERE子句书写时，每个条件占一行，语句另起一行时，以保留字开始，保留字右对齐, 对于连接符＝、<=、\>=之类的不换行

**正例**

```sql
SELECT B.ACC_NBR, B.PREFIX, B.PRICE_PLAN_ID,
       A.COMPLETED_DATE
  FROM PROD A,
       SUBS B
 WHERE A.PROD_ID = B.SUBS_ID
   AND A.PROD_STATE = 'A'
   AND B.PRICE_PLAN_ID = 101
```

**检查方式**：工具检查（暂未支持）

#### 【强制】同一语句中的SELECT、UPDATE、SET、INSERT、DELETE、FROM、WHERE、ORDER BY、GROUP BY、HAVING等第一个关键字换行后右对齐；如果有关键字长度大于SELECT/DELETE/UPDATE，则采用左对齐

**正例**

```sql
SELECT A.BOX_ID,
       ...,
       B.ORG_NAME
  FROM GM_BOX A, BFM_ORG B
 WHERE 1 = 1
   AND A.ORG_ID = B.ORG_ID(+)
CONNECT BY PRIOR PARENT_BOX_ID = BOX_ID
 START WITH BOX_ID IN (...)
```

**检查方式**：工具检查（暂未支持）

#### 【强制】IF THEN ELSE、FOR LOOP、WHILE、UNTIL等嵌套语句的子句部分增加一个向右缩进

**正例**

```sql
FOR benefitItem ...... LOOP
    -- insert ACM_BENEFIT
    INSERT INTO ACM_BENEFIT(ACM_THRESHOLD_ID,
    SELECT nNewThresholdId,nNewSubBalTypeId,A
      FROM ACM_BENEFIT A
     WHERE A.SUB_BAL_TYPE_ID = benefitItem.su
    ......)
END LOOP;
```

**检查方式**：工具检查（暂未支持）

### 【强制】多表连接时，使用表的别名来引用列，一个表及其别名一行，折行后表名与上一行表名对齐

**正例**

```sql
SELECT B.ACC_NBR, B.PREFIX, B.PRICE_PLAN_ID,
       A.COMPLETED_DATE
  FROM PROD A,
       SUBS B
 WHERE A.PROD_ID = B.SUBS_ID
   AND A.PROD_STATE = 'A'
   AND B.PRICE_PLAN_ID = 101
```

**检查方式**：工具检查（暂未支持）

## 别名

### 【强制】多表关联操作的SQL，必须使用表的别名

**正例**

```sql
SELECT
       A.SUBS_ID
  FROM
       SUBS A,
       PROD B
 WHERE
       A.SUBS_ID = B.PROD_ID
   AND B.PROD_STATE NOT IN ('B', 'F')
```

**检查方式**： 工具检查

## 注释

### 【推荐】对较为复杂的SQL语句加上注释，说明算法、功能

**说明**：

| **编号** | **说明信息**                                                              |
|----------|---------------------------------------------------------------------------|
| a        | 应对不易理解的分支条件表达式加注释；                                      |
| b        | 对重要的计算应说明其功能；                                                |
| c        | 过长的函数实现，应将其语句按实现的功能分段加以概括性说明；                |
| d        | 每条SQL语句应尽可能有注释说明（表名、字段名）；                           |
| e        | 常量及变量注释时，必须说明被保存值的含义，最好也说明合法取值的范围；      |
| f        | 可采用单行/多行注释（-- 或 /\*\* \*/ 方式）；                             |
| g        | SQL注释中不允许使用中文，一律使用英文（国外现场机器未必安装中文语言包）； |

*Note：样例参看6.1命名与注释章节。*

**检查方式**：工具检查（暂未支持）

### PL/SQL注释主要分成两部分：程序说明区注释和主体区注释

#### 【推荐】程序说明区注释

**说明**：

程序说明区注释是对程序开发情况的说明，包括以下内容：

​&ensp;​&ensp; -- Description: \*\*\* //功能描述

&ensp;​&ensp; -- Author: your name //作者

​&ensp;​&ensp; -- Date: YYYY/MM/DD //创建日期

&ensp;​&ensp; -- Param: description //输入输出参数说明

**正例**

```sql
CREATE OR REPLACE PROCEDURE P_QUERY_USER_STATE
(
    IV_PREFIX IN VARCHAR2,
    IV_ACC_NBR IN VARCHAR2,
    OV_STATE OUT VARCHAR2
)
/** 
  * Description: query the subscriber's state
  * Author: Zhang.San
  * Date: 2012-04-23
  * Param: IV_PREFIX prefix of number
  * Param: IV_ACC_NBR telephone number
  * Param: OV_STATE state of the subscriber
  */
IS

```

**检查方式**：工具检查（暂未支持）

#### 【推荐】程序主体区注释

**说明**：

主体区注释是对程序中某些语句的详细说明，用以加强程序的可读性。

**正例**

```sql
-- enable parallel DML
EXECUTE IMMEDIATE 'ALTER SESSION ENABLE PARALLEL DML';

/**
  * only process the subscribers whose state is in ('A', 'D', 'E')
  * insert the subscribers to a temporary table
  */
FOR ... LOOP
    nSubsId := subsInfoCurItem.SUBS_ID;
    ......
END LOOP
```

**检查方式**：工具检查（暂未支持）

# 性能优化

## 【推荐】尽量减少数据库负担

**说明**：

当执行每条SQL语句时, ORACLE在内部执行了许多工作：解析SQL语句、估算索引的利用率、绑定变量、读数据块等。减少访问数据库的次数，就能实际上减少ORACLE的工作量。

**检查方式**：人工检查

## 【推荐】避免大表关联，大表关联可能存在性能问题

**检查方式**：工具方式（暂未支持）

## 【强制】程序代码中禁止SQL语句直接拼接参数，而不使用绑定变量

**说明**：

在OLTP系统中，SQL尽量采用绑定变量的方式。否则会导致频繁的硬解析，进而严重影响数据库的性能。使用拼接参数还会存在SQL注入的安全隐患。

*Note：SQL中IN子句也需要用绑定变量方式处理。*

**<font color=red>反例</font>**

```sql
SELECT
       DEPOSIT_TYPE_ID,
       NAME,
       COMMENTS,
       CHARGE,
       SP_ID,
       DEPOSIT_TYPE_CODE,
       REFUNDABLE,
       TRANS_CREDIT
 FROM
       DEPOSIT_TYPE
WHERE
       DEPOSIT_TYPE_ID IN (&depositTypeIdStr&)
```

*Note：其中&depositTypeIdStr&为业务代码中的拼接参数*

**正例**

举例1：

```sql
SELECT  A.SUBS_UPP_INST_ID,
        A.SUBS_ID,
        A.PRICE_PLAN_ID,
        A.CREATED_DATE,
        A.EFF_DATE,
        A.EXP_DATE,
        A.UPDATE_DATE,
        A.STATE,
        A.STATE_DATE,
        A.SP_ID,
        A.OFFER_ID
  FROM SUBS_UPP_INST A
 WHERE A.STATE = 'A'
   AND A.SUBS_ID = :SUBS_ID
   AND A.PRICE_PLAN_ID = :PRICE_PLAN_ID
```

举例2：

```sql
SELECT
       DEPOSIT_TYPE_ID,
       NAME,
       COMMENTS,
       CHARGE,
       SP_ID,
       DEPOSIT_TYPE_CODE,
       REFUNDABLE,
       TRANS_CREDIT
 FROM
       DEPOSIT_TYPE
WHERE
       DEPOSIT_TYPE_ID IN (V_DEPOSIT_TYPE_ID)
```

*Note: V_DEPOSIT_TYPE_ID是业务代码中的变量*

**检查方式**：工具检查（暂未支持）

**故障单参考**：2389407

## 【强制】禁止使用“SELECT \*”这样的语句，特别是在程序代码内部

**说明**：

当需要查询表中的所有列时，也需列出所有的字段名。

Note：如果有子查询，而且子查询有列名的，可以使用 "select *" ，样例可参看4.19查询分页场景的举例。

**<font color=red>反例</font>**

```sql
SELECT *
  FROM CUST 
 WHERE CUST_ID = 1
```

**正例**

```sql
SELECT
       CUST_ID,
       CUST_CODE,
       CUST_NAME,
       CUST_TYPE,
       CERT_ID,
       PARENT_ID,
       DELIVER_METHOD,
       ZIPCODE
 FROM
       CUST
WHERE
       CUST_ID = 1
```

**检查方式**：工具检查

## 【推荐】尽量避免多表的关联操作

**说明**：

关联表越多，需要Oracle调度的资源就越多。SQL应尽量简化，查询类语句只查询业务所需的数据，不查询无关数据表。 特别需要关注数据量巨大的表关联操作，使用不当会引发系统故障。

**检查方式**：工具检查

## 【推荐】尽量使用UNION ALL 代替 UNION

**说明：**

UNION在进行表链接后会筛选掉重复的记录，所以在表链接后会对所产生的结果集进行排序运算，删除重复的记录再返回结果，如果表数据量大的话可能会导致用磁盘进行排序。 UNION ALL操作只是简单的将两个结果合并后就返回，所以可能存在重复记录。 需要结合业务需求分析使用UNION ALL的可行性。

**检查方式**：工具检查（暂未支持）

## 【强制】禁止SQL内层使用ORDER BY 和 GROUP BY 排序操作

**说明：**

*Note：查询分页场景下例外。*

**检查方式**：工具检查（暂未支持）

## 【推荐】尽量减少外层使用ORDER BY 和GROUP BY 排序操作

**说明**：

大量的排序操作影响系统性能，如必须使用排序操作，尽量建立在有索引的列上。

**<font color=red>反例</font>**

```sql
SELECT A.SUBS_ID,
       A.PREFIX,
       A.ACC_NBR,
       A.ACCT_ID,
       A.CUST_ID,
       B.PROD_STATE,
       B.COMPLETED_DATE,
       B.OFFER_ID,
       B.SUBS_PLAN_ID
  FROM (SELECT SUBS_ID, PREFIX, ACC_NBR, ACCT_ID, CUST_ID
          FROM SUBS
         ORDER BY SUBS_ID) A,
       PROD B
 WHERE A.SUBS_ID = B.PROD_ID
   AND B.PROD_STATE = 'A'
 ORDER BY PROD_ID
```

**正例**

```sql
SELECT A.SUBS_ID,
       A.PREFIX,
       A.ACC_NBR,
       A.ACCT_ID,
       A.CUST_ID,
       B.PROD_STATE,
       B.COMPLETED_DATE,
       B.OFFER_ID,
       B.SUBS_PLAN_ID,
       B.INDEP_PROD_ID
  FROM (SELECT SUBS_ID, PREFIX, ACC_NBR, ACCT_ID, CUST_ID FROM SUBS) A,
        PROD B
 WHERE A.SUBS_ID = B.PROD_ID
   AND B.PROD_STATE = 'A'
 ORDER BY PROD_ID
```

**检查方式**：工具检查

## 索引的使用

### 【强制】不允许对索引列进行计算

**<font color=red>反例</font>**

```sql
SELECT ...... 
  FROM EMP
 WHERE HIRE_DATE + 100 =TO_DATE('20080411', 'YYYYMMDD')
```

**正例**

```sql
SELECT ...... 
  FROM EMP
 WHERE HIRE_DATE = TO_DATE('20080411','YYYYMMDD') - 100
```

**检查方式**：工具检查（暂未支持）

### 【强制】注意比较值与索引列数据类型的一致性，避免使用数据库的类型自动转换功能

**说明**：

比较值与索引列数据类型不一致，则可能会不走索引，导致全表扫描，故需要避免使用数据库类型自动转换功能（隐式转换）。

**<font color=red>反例1</font>**

```sql
vSubsId VARCHAR(20);
vSubsId := ‘10001’;
SELECT PREFIX, ACC_NBR
  FROM SUBS
 WHERE SUBS_ID = :vSubsId
```

*Note：vSubsID为字符串型变量，表字段SUBS_ID为NUMBER类型；*

**<font color=red>反例2</font>**

```sql
SELECT ACC_NBR_TYPE
  FROM TEST_ACC_NBR
 WHERE ACC_NBR = 10;
```

![image](uploads/4061/ec09b01d-ca75-46af-a32c-1f7bdd2e1761/4.9.2-example-nok.png)

*Note：ACC_NBR为VARCHAR2类型，且ACC_NBR上有索引，执行计划显示为全表扫描。*

**正例1**

```sql
nSubsId NUMBER;
nSubsId := 10001;
SELECT PREFIX, ACC_NBR
  FROM SUBS
 WHERE SUBS_ID = :nSubsId
```

*Note：nSubsId为数值型变量，表字段SUBS_ID为NUMBER类型；*
*另，定义变量建议尽量引用数据库实体类型，参考2.2.2.5章节描述。*

**正例2**

```sql
SELECT ACC_NBR_TYPE
  FROM TEST_ACC_NBR
 WHERE ACC_NBR = '10';
```

![image](uploads/4061/40e5fb84-fd8f-49c9-abe5-e25d0517e144/4.9.2-example-ok.png)

*Note：ACC_NBR为VARCHAR2类型，且ACC_NBR上有索引，执行计划显示有走索引。*

**检查方式**：工具检查（暂未支持）

### 【推荐】对于复合索引，SQL语句的WHERE查询条件尽量使用到索引的第一列，否则可能用不上该复合索引。

**说明**：

如果索引是建立在多个列上, 只有在它的第一个列(leading column)被where子句引用时,优化器才会选择使用该索引。

**<font color=red>反例</font>**

```sql
SELECT PROD_ID, ATTR_ID, VALUE, EFF_DATE, EXP_DATE
  FROM PROD_ATTR_VALUE
 WHERE ATTR_ID = :ATTR_ID
```

*【说明】：PROD_ATTR_VALUE表有复合索引PK_PROD_ATTR_VALUE(PROD_ID,ATTR_ID)*

**正例**

```sql
SELECT PROD_ID, ATTR_ID, VALUE, EFF_DATE, EXP_DATE
  FROM PROD_ATTR_VALUE
 WHERE PROD_ID = :PROD_ID
   AND ATTR_ID = :ATTR_ID
```

*【说明】：PROD_ATTR_VALUE表有复合索引PK_PROD_ATTR_VALUE(PROD_ID,ATTR_ID)*

**检查方式**：工具检查（暂未支持）

### 【推荐】使用Oracle的函数索引解决空字段导致索引失效的问题

**说明**：

如果索引字段有空值，而且空值所占数据量较小，使用IS NULL判断查询，会导致索引失效，此场景建议建索引时使用 表名(列名,0) 的方法，可以走索引提高效率。

**<font color=red>反例</font>**

```sql
SELECT SUBS_ID, CUST_ID, ACCT_ID, PREFIX, ACC_NBR
  FROM SUBS
 WHERE PPS_PWD IS NULL
```

*Note：索引IDX_PPS_PWD ON SUBS(PPS_PWD)，索引失效，全表扫描*

**正例**

```sql
SELECT SUBS_ID, CUST_ID, ACCT_ID, PREFIX, ACC_NBR
  FROM SUBS
 WHERE PPS_PWD IS NULL
```

*Note：索引IDX_PPS_PWD ON SUBS(PPS_PWD,0)，走索引*

**检查方式**：工具检查（暂未支持）

### 【推荐】对于索引的比较，尽量避免使用不等于（!=）

**<font color=red>反例</font>**

```sql
SELECT ACCOUNT_NAME 
  FROM TEST 
 WHERE AMOUNT != 0
```

**正例**

```sql
SELECT ACCOUNT_NAME 
  FROM TEST 
 WHERE AMOUNT > 0
```

**检查方式**：工具检查（暂未支持）

### 【推荐】当SQL的WHERE条件涉及多个可用索引时，必须在研发阶段评估执行计划跳变风险，并采取规避措施。

**说明**：

如果一条SQL的WHERE条件涉及多个列，且这些列各自存在独立的索引（单列索引或联合索引），Oracle优化器在执行时可能因统计信息变化、绑定变量窥探（bind peeking）、数据分布倾斜等因素，在不同的执行计划之间跳变，选择非最优的索引访问路径，导致SQL性能从毫秒级恶化到秒级甚至分钟级，在核心业务场景下可能引发系统故障。

常见风险场景包括：
多索引竞争（WHERE条件涉及的多个列分别有可用索引，优化器需要从中选择）、内外层嵌套查询有不同索引、游标分页查询的排序与过滤分别使用不同索引、绑定变量窥探导致执行计划对后续不同参数值不友好等。

研发人员在编写此类SQL时，必须在研发阶段评估执行计划跳变风险并采取规避措施，包括但不限于：
1）提请SA重新设计索引（如将多个单列索引合并为覆盖查询条件的复合索引，从根源上消除索引选择歧义）；
2）通过SQL改写（如UNION ALL替代OR、拆分子查询、调整条件顺序等）减少优化器选错的可能；
3）在项目现场建立执行计划监控，及时发现并告警执行计划跳变（运维人员关注）；

**<font color=red>反例1</font>**

```sql
-- PROD表上PROD_ID和ACTIVE_DATE分别建有单列索引
-- 内层查询用ACTIVE_DATE条件，外层查询用SUBS_ID(=PROD_ID)条件
-- 统计信息过期时，优化器可能选择ACTIVE_DATE索引而非PROD_ID索引
-- 执行计划跳变导致扫描大量数据块，性能恶化
SELECT 1 FROM (
  SELECT A.PROD_ID SUBS_ID 
    FROM PROD A 
   WHERE A.INDEP_PROD_ID IS NULL 
     AND A.ACTIVE_DATE > SYSDATE - 1
) WHERE ROWNUM = 1 AND SUBS_ID = :1;
```

*Note：PROD表两个单列索引导致跳变，对应案例1故障*

**<font color=red>反例2</font>**

```sql
-- ACCT_BOOK表上ACCT_ID和CREATED_DATE分别建有单列索引，优化器需从这两个单列索引中选择
-- 若选CREATED_DATE索引，需扫描1天全部数据再回表过滤ACCT_ID，性能恶化
-- 若选ACCT_ID索引，精确定位少量数据行，性能正常
-- 统计信息变化时执行计划跳变，不可预期
SELECT ACCT_BOOK_ID, ACCT_ID, AMT, CREATED_DATE
  FROM ACCT_BOOK
 WHERE ACCT_ID = 1143002
   AND CREATED_DATE >= TO_DATE('2026/5/26', 'YYYY/MM/DD')
   AND CREATED_DATE < TO_DATE('2026/5/27', 'YYYY/MM/DD')
   AND PART_ID = 1
 ORDER BY CREATED_DATE;
```

*Note：ACCT_BOOK表两个单列索引导致跳变，对应案例2故障*

**正例1**

```sql
-- PROD表建有复合索引 IDX_PROD_PRODID_ACTIVEDATE(prod_id, active_date)
-- 复合索引覆盖内外层查询条件，优化器无二选一的歧义，执行计划稳定
SELECT 1 
  FROM PROD A 
 WHERE A.PROD_ID = :1
   AND A.INDEP_PROD_ID IS NULL 
   AND A.ACTIVE_DATE > SYSDATE - 1
   AND ROWNUM = 1;
```

*Note：复合索引从根源消除歧义*

**正例2**

```sql
-- ACCT_BOOK表建有复合索引 IDX_ACCT_BOOK_ACCT_CRTDATE(acct_id, created_date)
-- ORDER BY 增加 acct_id，与复合索引列顺序对齐，消除排序步骤(SORT ORDER BY)
-- 优化器在任何统计信息下均使用该复合索引，执行计划稳定
SELECT ACCT_BOOK_ID, ACCT_ID, AMT, CREATED_DATE
  FROM ACCT_BOOK
 WHERE ACCT_ID = 1143002
   AND CREATED_DATE >= TO_DATE('2026/5/26', 'YYYY/MM/DD')
   AND CREATED_DATE < TO_DATE('2026/5/27', 'YYYY/MM/DD')
   AND PART_ID = 1
 ORDER BY ACCT_ID, CREATED_DATE;
```

*Note：复合索引 + ORDER BY 与索引对齐*

**检查方式**：【工具检查】(待开发)

**案例说明**：
**案例1** - 故障单3796253 
**故障描述**：
某项目核心业务SQL涉及大容量实例表的多条件查询，数据库统计信息过期后，Oracle优化器执行计划发生跳变，选择了非最优索引，导致SQL执行性能急剧下降，占用大量数据库资源，影响前台业务正常操作。 
**原因分析**：
该SQL使用了SUBS_ID和ACTIVE_DATE分别做外层和内层查询条件，表上在SUBS_ID和ACTIVE_DATE列分别建有单列索引。当数据库统计信息过期时，优化器没有选择最优的SUBS_ID索引，而是选择了ACTIVE_DATE索引，导致扫描大量无效数据块，SQL执行时间从毫秒级恶化到秒级，严重拖累系统性能（参看反例1）。 
**解决方案**：
根据业务查询特点，将多个单列索引合并为覆盖查询条件的复合索引，从根源上消除优化器索引选择的歧义。

**案例2** - 故障单981078，1110043
**故障描述**：
ACCT_BOOK表中ACCT_ID和CREATED_DATE分别建有两个单列索引，在多个项目现场发生过因执行计划跳变导致的严重故障，影响计费核心业务流程。 
**原因分析**：
该SQL涉及查询条件：ACCT_ID（等值条件）、CREATE_DATE（范围条件 + 排序字段），表上在ACCT_ID和CREATE_DATE分别建有单列索引，优化器需要从中选择一个。若选ACCT_ID索引，精确定位少量数据行后再回表过滤，扫描量小且可利用索引有序性消除排序；若选CREATE_DATE索引，需扫描范围内所有数据行（1天的数据量可能很大），再回表过滤ACCT_ID条件，扫描大量无效数据块。当统计信息变化时优化器跳变选择CREATED_DATE索引，SQL执行时间从毫秒级恶化到秒级，严重拖累系统性能（参看反例2）。 
**解决方案**：
将两个单列索引改为(ACCT_ID, CREATED_DATE)的复合索引后，优化器在任何统计信息下都使用该复合索引：ACCT_ID等值条件在前精确定位+CREATED_DATE在后范围扫描+索引天然支持排序，可以彻底消除索引选择歧义。

## 【推荐】在IF/ELSE类型的查询中，可使用DECODE替代

**说明**：

使用DECODE函数可以避免重复扫描相同记录或重复连接相同的表。

**<font color=red>反例</font>**

```sql
SELECT COUNT(1), SUM(SAL)
  FROM EMP
 WHERE DEPT_NO = '0020'
　 AND ENAME LIKE 'SMITH%';
　　
SELECT COUNT(1), SUM(SAL)
　FROM EMP
 WHERE DEPT_NO = '0030'
   AND ENAME LIKE 'SMITH%';
```

**正例**

```sql
SELECT COUNT(DECODE(DEPT_NO, '0020', 'X', NULL)) D0020_COUNT,
       COUNT(DECODE(DEPT_NO, '0030', 'X', NULL)) D0030_COUNT,
       SUM(DECODE(DEPT_NO, '0020', SAL, NULL)) D0020_SAL,
       SUM(DECODE(DEPT_NO, '0030', SAL, NULL)) D0030_SAL
  FROM EMP
 WHERE ENAME LIKE 'SMITH%';
```

**检查方式**：工具检查（暂未支持）

## 【推荐】用CASE … WHEN … THEN … ELSE … END格式减少表的扫描次数

**说明**：

在我们的开发维护工作中常常必须基于多组数据表计算不同的聚集，需要多次扫描业务数据表，而CASE语句就可以把多次扫描合并成一次来完成。

**<font color=red>反例</font>**

```sql
SELECT
       COUNT(0)
 FROM
       BLACKLIST_SUBS
WHERE
       BLACKLIST_TYPE = 'A'
  AND  SUBS_ID = 24147;

SELECT
        COUNT(0)
  FROM
        BLACKLIST_SUBS
 WHERE
        BLACKLIST_TYPE = 'B'
   AND  SUBS_ID = 24147;

SELECT
        COUNT(0)
  FROM
        BLACKLIST_SUBS
 WHERE
        BLACKLIST_TYPE = 'C'
   AND  SUBS_ID = 24147;
```

**正例**

```sql
SELECT COUNT(CASE BLACKLIST_TYPE WHEN 'A' THEN 1 ELSE NULL END) A,
       COUNT(CASE BLACKLIST_TYPE WHEN 'B' THEN 1 ELSE NULL END) B,
       COUNT(CASE BLACKLIST_TYPE WHEN 'C' THEN 1 ELSE NULL END) C
  FROM BLACKLIST_SUBS
 WHERE SUBS_ID = 24147;
```

**检查方式**：人工检查

## 【推荐】用WHERE子句替换HAVING子句

**说明**：

避免使用HAVING子句，HAVING只会在检索出所有记录之后才对结果集进行过滤，这个处理需要排序、统计等操作。如果能通过WHERE子句限制记录的数目，那就能减少这方面的开销。

**<font color=red>反例</font>**

```sql
SELECT REGION, AVG(LOG_SIZE)
  FROM LOCATION
 GROUP BY REGION
HAVING REGION != 'SYDNEY'
   AND REGION != 'PERTH'
```

**正例**

```sql
SELECT REGION, AVG(LOG_SIZE)
  FROM LOCATION
 WHERE REGION != 'SYDNEY'
   AND REGION != 'PERTH'
 GROUP BY REGION
```

**检查方式**：工具检查

## 【推荐】LIKE子句尽量前端匹配

**说明**：

LIKE 参数使用得非常频繁，因此如果能够对于LIKE 子句使用索引（B树索引），将很好地提高查询的效率。

**<font color=red>反例</font>**

```sql
SELECT CUST_ID, CUST_NAME 
  FROM CUST 
 WHERE CUST_NAME LIKE '%Tom%'
```

**正例**

```sql
SELECT CUST_ID, CUST_NAME 
  FROM CUST 
 WHERE CUST_NAME LIKE 'Tom%'
```

**检查方式**：工具检查（暂未支持）

## 【强制】程序代码中禁止使用Database Link进行任何跨库访问

**说明**：

ORACLE的Database Link功能已知缺陷较多，程序代码中使用Database Link对程序的性能和稳定性都有影响。比如，在某些场景下，使用Database Link进行跨数据库访问可能导致分布式锁问题、事务不一致性以及网络带来的潜在延迟，这些都可能引发异常或性能瓶颈。故程序代码中严禁使用Database Link进行任何跨库访问。

Note：程序代码包含源代码、配置文件等。

**检查方式**：工具检查（暂未支持）

**案例说明**：
**案例1** - 故障单3659330
**故障描述**：
某项目 多个SHARD库之间使用DBLINK连接（shard1连shard2/shard3（@LINK_VPN2、@LINK_VPN3））。过户场景涉及多个SHARD库之间的业务数据迁移，每天都会有一两笔业务数据迁移失败。
**原因分析**：
DBLINK不稳定，数据库日志中有ORA-03150: end-of-file on communication channel for database link报错。
**解决方案**：
业务侧自行优化，通过多次重试的方式解决问题。

**案例2** - 故障单2662934，2629701
**故障描述**：
某项目 PredictRate 处理租费生成短信插入ADVICE表失败导致进程挂起；dboperator写表失败导致信控、通知短信无法下发。
**原因分析**：
分析发现相关业务SQL插入语句中 表和序列 都使用了DBLINK，而使用DBLINK的SEQUENCE执行结果为空，导致核心业务服务结果错误。
此场景可能触发了ORACLE的bug，但ORACLE未提供根本原因。
**解决方案**：
最终业务侧调整解决方案，改用UIP方式写ADVICE表，弃用DBLINK方式。

**案例3** - 故障单1664054
**故障描述**：
某项目 已注册用户激活延迟，历史上已出现过多次类似问题。
**原因分析**：
AWR报告中显示故障期间插入SHINT_ASA_IF_Q表的SQL耗时很长，该表为三方系统数据库的表，我方系统中通过DBLINK创建同义词方式访问。
**解决方案**：
按照ORACLE建议增加启动参数，同时业务完善了日志能力，进行后续观察。

**案例4** - 故障单1561994
**故障描述**：
某OCS项目 自上线以来，每次号码回收时都会出现IL8将DBLINK断链的情况，同时IL8侧会将提供给OCS的用户锁定10分钟，10分钟后自动将锁释放，导致号码回收不完全，且在号码回收期间，其他的开通事务也受到影响会失败，甚至影响号码激活和VAS订购。
**原因分析**：
经IL8侧反馈，是OCS侧有INSERT语句未提交导致对端锁表，并将OCS的用户锁住10分钟。
经排查发现由于OCS与IL8之间使用DBLINK进行连接，事务在提交时只能保证程序与ORACLE的连接释放，不能确保DBLINK的释放。且性能测试发现最终DBLINK的连接未释放，导致连接池满。
**解决方案**：
在无法主动调整与IL8的DBLINK连接方式的情况下，业务侧将当前的100条一次的批量处理，改为单条插数据的方式。

**案例5** - 故障单541889
**故障描述**：
某项目 WEBSERVICE接口机TOMCAT挂死，重启后恢复正常，可能与局方开始测试AddVPNCluster和AddVPNMember两个接口有关。这两个接口在后付费环境上，用于更新预付费环境上的8个DBLINK的配置项。
**原因分析**：
测试发现通过DBLINK 插入数据到预付费同一套系统，SQL执行时间不稳定，有时快有时很慢5s左右；这两个接口耗时很长，主要慢在DBLINK上。
**解决方案**：
最终业务侧改造了这两个接口的实现逻辑，弃用DBLINK。

## 【推荐】Database Link仅在访问频率较低的非程序调用场景下使用，如跨库的数据割接、数据同步、数据迁移、报表生成等

**说明**：

Database Link应谨慎使用，仅适合在访问频率较低的 **非程序调用** 场景下使用，如跨库的数据割接、数据同步、数据迁移、报告生成等，以避免性能问题和安全隐患。

**正例**

```sql
INSERT INTO LOCAL_TABLE  
  (ID, NAME, VALUE)  
  SELECT ID, NAME, VALUE FROM REMOTE_TABLE@REMOTE_DBLINK WHERE ID > 1000;
```

*Note: 割接场景使用Database Link从远程数据库同步数据到本地表。*

**检查方式**：人工检查

## 【强制】避免超长SQL，SQL长度不可超过4000长度。

**说明**：

超长SQL往往导致难以理解，并可能伴随性能隐患。同时，应尽量减少SQL语句复杂度，用简单的SQL完成任务，复杂的业务逻辑尽量由业务代码来实现。

**检查方式**：工具检查（暂未支持）

## 【推荐】SQL子查询嵌套不宜超过3层

**说明**：

禁止使用多层的SQL嵌套，除了分页查询，一般SQL语句建议不超过3层嵌套，过于复杂的SQL可根据业务逻辑拆分为多条SQL来实现。

**检查方式**：工具检查（暂未支持）

## 【推荐】避免不必要的排序

**说明**：

避免不必要的排序，对查询结果进行排序会大大降低系统性能。应将大多数的排序工作交给应用层去完成。

**检查方式**：人工检查

## 【推荐】WEB页面分页查询使用多层SQL方式，建议如下分页格式，先查询过滤出一部分数据，再做下一层过滤查询

**说明**：
对于WEB页面分页查询场景推荐多层SQL方式，适用于高并发，响应要求高的场景，SQL语句简单明了，也易于开发和后期维护。
对于后台JOB批处理查询推荐使用游标方式，参看规范4.26。

ORACLE中推荐通过逐层嵌套子查询的方式来过滤并提取一定范围内的行数据。首先内层子查询对数据进行ORDER BY排序操作，确保提取记录的顺序；外层的查询通过ROWNUM限制返回的结果集，减少需要处理的数据量，避免不必要的全表扫描，提高分页查询性能；最外层再次对ROWNUM进行筛选，可以灵活指定不同页码和页大小。利用ROWNUM这一轻量级机制避免全表扫描，在大数据集环境下，能有效降低开销和提高查询性能。适用于希望对大结果集进行高效分页访问的场景，特别是在版本较低的Oracle数据库系统中，这种方法仍然是实现分页的常用选择。

请注意，分页查询的内层子查询中必须使用ORDER BY对数据进行排序，参看规范4.25。

**<font color=red>反例</font>**

```sql
SELECT *
  FROM (SELECT A.*, ROWNUM RN
          FROM (SELECT OWNER, CREATED, OBJECT_ID, OBJECT_TYPE
                  FROM T1
                 WHERE OWNER = 'SYS'
                 ORDER BY OBJECT_ID DESC) A)
 WHERE RN > 10
   AND RN <= 20
```

**正例**

```sql
SELECT *
  FROM (SELECT A.*, ROWNUM RN
          FROM (SELECT OWNER, CREATED, OBJECT_ID, OBJECT_TYPE
                  FROM T1
                 WHERE OWNER = 'SYS'
                 ORDER BY OBJECT_ID DESC) A
         WHERE ROWNUM <= 20)
 WHERE RN > 10
```

**检查方式**：人工检查

## 【参考】尽量避免HINT在代码中出现

**说明**：

通过hint的影响，使执行计划固化下来，有时会导致错误的结果，一般不建议使用，特别应用场景情况下除外。

**检查方式**：工具检查（暂未支持）

## 【参考】并行度使用需谨慎

**说明**：

并行技术的使用需要考虑CPU核数，系统负载等情况，并行执行的SQL会对其它语句的性能产生影响，一般常用在报表分析任务和OLAP系统中。

在使用PRARLLEL时，不要直接使用/\*+ PRARLLEL \*/，因为有可能数据库会使用较多的CPU资源，引起性能问题。而需要指明具体的并行度值/\*+ PRARLLEL(4) \*/，一般并行度取值不能太高，理论上并行度最大取值为物理CPU总数减1。

**<font color=red>反例</font>**

```sql
SELECT /*+PRARLLEL*/SUBS_ID,CUST_ID,
	   ACCT_ID,PREFIX,ACC_NBR
  FROM SUBS
 WHERE ACC_NBR LIKE '87%'
```

**正例**

```sql
SELECT /*+PRARLLEL(4)*/ SUBS_ID, CUST_ID, 
       ACCT_ID, PREFIX, ACC_NBR
  FROM SUBS
 WHERE ACC_NBR LIKE '87%'
```

**检查方式**：工具检查（暂未支持）

## 【推荐】SQL里面避免使用标量子查询，标量子查询全部使用外连接实现

**说明：**

举例中标量子查询将A表里把每条ID传到B表里执行，也就是说A表有多少条数据，B表就要执行多少次。当A表数据量很大时，就会存在问题。

建议修改成外连接方式，这样可以走HASH JOIN，避免FILTER，提升性能。

标量子查询用在如下情况较合适：

​        1.A表的count(distinct id)比较小

​        2.B表的连接键，这里就是ID上有比较高效的选择性的索引

**<font color=red>反例</font>**

```sql
SELECT A.OBJECT_ID,
       (SELECT B.USERNAME 
          FROM T1 B 
         WHERE A.OWNER = B.USERNAME)
  FROM T2 A;
```

**正例**

```sql
SELECT A.OBJECT_ID, B.USERNAME
  FROM T2 A,
       T1 B
 WHERE T2.USERNAME = T1.OWNER(+);
```

**检查方式**：人工检查

## 【推荐】在SQL有绑定变量时，尽量少使用 非等式谓词（>，<， >=， <=， <\> ，LIKE），可能会引起性能问题

**说明：**

如 >，<，>=， <=， LIKE，<\>都属于不安全的谓词条件，因为这样有可能引发**高版本问题**（High Version Count），从而可能导致数据库SGA内存争用，继而引发性能问题。

Note： **高版本问题**（High Version Count）是指：当SQL 语句第一次执行时，会创建parent cursor 和child cursor。 这两个是必须的。这两个过程是比较费资源的。也就是硬解析。 当再次执行这个SQL时，Oracle 会先对SQL 语句进行hash 运算，产生一个hash 值，然后用这个HASH 值到buckets里去查找，hash value 存放在parent cursor里。 如果找到了，就去检查child cursor。 如果可以重用这个child cursor，那么就直接调用cursor里的执行计划。 如果不可重用，就会创建一个新的child cursor。 这个child cursor 的个数，就是version count。 不同parent cursor 对应的child cursor 越多，version count 就越高。

**故障单参考：**

ZMP\2377779

## 【禁止】在OLTP系统中，禁止出现结果集连接（JOIN）但无关联条件的情况

**说明：**

如果联接查询中的两个表没有联接条件，那么Oracle返回其笛卡尔积，这种情况很可能是逻辑错误，数据量大时很可能引发性能故障。

可通过执行计划查看：执行计划中如果出现**MERGE JOIN CARTESIAN**那么代表该SQL代码可能存在缺少关联条件或关联字段缺少索引导致。

![image](uploads/4061/3501c2f5-010a-40c6-ae7f-b38279f8f11c/image.png)

**<font color=red>反例1</font>**

```sql
SELECT
       T1.ID,
       T1. NAME,
       T2. NAME
  FROM
       TABLE1 T1
 CROSS JOIN TABLE2 T2;
```

**<font color=red>反例2</font>**

```sql
SELECT
       T1.ID,
       T1. NAME,
       T2. NAME
  FROM
       TABLE1 T1,
       TABLE2 T2;
```

**正例**

```sql
SELECT
       T1.ID,
       T1. NAME,
       T2. NAME
  FROM
       TABLE1 T1,
       TABLE2 T2
 WHERE
       T1.ID = T2.ID
```

**检查方式**：工具检查

## 【强制】分页查询的内层子查询中必须使用ORDER BY对数据进行排序，且建立在有索引的列上，确保分页查询时获取数据的一致性和正确性

**说明**：
WEB页面分页查询使用多层SQL方式（规范4.19），在分页查询的内层子查询中必须使用 ORDER BY，并且基于有索引的列进行排序，主要是为了保证每次分页查询时数据的顺序一致，防止因数据无序或排序字段非唯一导致结果重复或遗漏，确保分页结果的正确性和一致性。同时，基于有索引的列排序能够提升查询性能，避免全表扫描，提高系统的响应速度和稳定性。

另外，在Oracle数据库中，针对分页查询的优化，索引设计至关重要。如何通过索引优化分页查询性能？参看附录7.2。

**<font color=red>反例</font>**

```sql
SELECT *
  FROM (SELECT A.*, ROWNUM RN
          FROM (SELECT OWNER, CREATED, OBJECT_ID, OBJECT_TYPE
                  FROM T1
                 WHERE OWNER = 'SYS') A
         WHERE ROWNUM <= 20)
 WHERE RN > 10
```

**正例**

```sql
SELECT *
  FROM (SELECT A.*, ROWNUM RN
          FROM (SELECT OWNER, CREATED, OBJECT_ID, OBJECT_TYPE
                  FROM T1
                 WHERE OWNER = 'SYS'
                 ORDER BY OBJECT_ID DESC) A
         WHERE ROWNUM <= 20)
 WHERE RN > 10
```

*Note：OBJECT_ID字段有索引*

**检查方式**：人工检查

**案例说明**：
**案例1** - 故障单3234455
**故障描述**：
某项目升级后，各Channel无法订购U25&U35。
**原因分析**：
分页查询功能实现时存在问题，出现重复数据，导致计费入库时主键冲突；同时同步给计费缓存的部分属性丢失，导致offer无法订购。
**解决方案**：
排查整改分页查询语句，查询必须加上唯一性的排序标识。例如，有些业务查询要求根据时间进行排序，时间排序后的结果仍然不具有非唯一性，在主要的业务排序后加上必要的主键排序。

**案例2** - 故障单3319188
**故障描述**：
某项目，38万订户没有收到租费赠送。
**原因分析**：
分页查询全量数据时没有做排序，后续全量同步给计费缓存时，因为存在重复数据，导致OFFER_ATTR数据同步不完整。
**解决方案**：
分页查询时增加字段OFFER_ID和ATTR_ID作为排序字段。

## 【推荐】后台JOB批处理查询使用游标方式处理

**说明**：
后台JOB批处理查询推荐使用游标方式处理。后台JOB通常需要处理大量数据，游标可以分批次、顺序的处理数据，避免一次性加载全部数据导致内存溢出。也可以保证处理过程中数据的一致性，适合长事务或需要持续处理的批量操作。游标可以灵活控制数据的提取、处理和提交，便于实现复杂的业务逻辑。

Note:
1）使用游标时，可能导致数据库连接释放变慢，会出现连接泄漏的告警。这类泄漏告警，通常情况下属于误报，可以暂时忽略。
2）国际侧业务产品可以使用框架提供的API：RowSetWrapper rsw = JdbcTemplate.query(JdbcUtil4BL.getDbBackService(), sql, pm, null); 进行处理，最后记得在finally代码块关闭游标。

**<font color=red>反例</font>**

```java
ParamMap pm = new ParamMap();  
String sql = "SELECT XX FROM YY WHERE ...";  
DbIdentifier dbId = JdbcUtil4BL.getDbBackService();  
RowSetWrapper rsw = JdbcTemplate.query(dbId, sql, pm, null);  
while (rsw.next()) {  
  // 根据字段名称获取字段值  
  String strValue = rsw.getString("XXX");  
  Long longValue = rsw.getLong("YYY");  
  // 处理字段值....  
}
```

*Note: 未关闭游标*

**正例**

```java
ParamMap pm = new ParamMap();  
String sql = "SELECT XX FROM YY WHERE ...";  
DbIdentifier dbId = JdbcUtil4BL.getDbBackService();  
RowSetWrapper rsw = JdbcTemplate.query(dbId, sql, pm, null);  
try {  
  while (rsw.next()) {  
  // 根据字段名称获取字段值  
  String strValue = rsw.getString("XXX");  
  Long longValue = rsw.getLong("YYY");  
  // 处理字段值....  
  }  
}
finally {  
  // 关闭游标  
  rsw.closeRowSet();  
}
```

**检查方式**：人工检查

# 最佳实践

## 【推荐】不要将空的变量值直接 用 比较运算符 来比较

**说明**：

如果变量可能为空，应该使用IS NULL或IS NOT NULL或NVL函数来进行比较。

**<font color=red>反例</font>**

```sql
IF vUserName == NULL THEN
   vUserName = ‘UNKOWN’;
END IF;
```

**正例**

```sql
IF vUserName IS NULL THEN
   vUserName = ‘UNKOWN’;
END IF;
```

**检查方式**：工具检查（暂未支持）

## 【强制】多表关联和复杂的SQL，需要进行执行计划分析

**说明**：

在OLTP系统中，SQL语句的执行效率对于系统非常重要，一个效率很低的SQL会降低系统吞吐量，严重时可导致系统宕机。所以，对于SQL语句的执行计划分析显得相当重要，下图是使用PL/SQL Developer分析SQL执行计划的示例。这里仅给出示例，不给出具体如何分析的方法，相关技能请自学或参加培训。
![image](uploads/4061/b9a5ee62-b624-4b60-81f0-08d0bec789af/image.png)

【注】一旦发现对大数据量表的全表扫描SQL，务必与相关同事进行讨论和分析。

*Note：
对于有关联实例表的查询，原则上都需要进行执行计划分析。同时需要结合业务场景分析，比如某些job是需要处理所有记录的，需要全表扫描，这种情况除外。*

**检查方式**：工具检查（暂未支持）

## 【参考】选择合适的多表关联方式

**说明**：

常见的表的关联方式有三种。

- **HASH JOIN**

  当需要进行多表关联操作时，选择使用全表扫描的方式在其中一个表的关联字段上创建HASH表（该表一般选择较小的表，以便可以存于SGA内存中，并达到提高探测的速度的目的），然后对另一表上进行全表扫描且以同样的算法构建HASH表，同时探测基于第一个表中上HASH表，查找匹配的键值。

  使用场景：大数据量等值关联查询，如关联查询大量用户资料及其清单数据。

  等值联接。
  ![image](uploads/4061/9c1682b8-58de-418e-9896-e7736e0c4114/image.png)

- **NESTED LOOP JOIN**

  优化器选择一个驱动表A作为循环扫描的外部表。

  另外一个相关联的表B作为内部表。

  每扫描驱动表A中一条记录，ORACLE扫描B表中所有满足关联条件的记录。

  正例

  ```sql
  SELECT A.CUST_NAME, B.STATE
    FROM CUST A, 
          PROD B
   WHERE A.ID = B.ID 
     AND A.ID = :ID
  ```

![image](uploads/4061/f77c1f25-dc1e-4bd4-a25e-476bce0dd87e/image.png)

- **SORT MERGE JOIN**

  当需要进行多表关联操作时，对相关联的表按关联字段进行排序，然后从各已排序好的结果中取得关联结果。

  适用于非等值关联、数据量比较大的场合。

  在对大数据量的关联查询，且条件为非等值条件，此时性能要好于nested loop join。

  在大多数情况下，HASH JOIN方式比该种关联方式高效。
  ![image](uploads/4061/9476fe99-dbf6-48ec-9c37-e01b8abb6ce8/image.png)

**检查方式**：人工检查

## 【参考】高效删除重复记录的方法

**说明**：

下面是最高效的删除重复记录方法示例( 因为使用了ROWID) 。

**正例**

```sql
DELETE FROM EMP E 
 WHERE E.ROWID > (SELECT MIN(X.ROWID) 
                    FROM EMP X 
                   WHERE X.EMP_NO = E.EMP_NO
                 )
```

**检查方式**：人工检查

## 【参考】关于SELECT COUNT(1) 与SELECT COUNT(\*)

**说明**：

有人总是说“SELECT COUNT(1)”的效率比“SELECT COUNT(\*)”的执行效率要高，而且长久以来我们也一直这么认为。其实，在Oracle高版本中两者的效率基本一致，没有本质差别。

这里还是推荐前一种写法，统一风格。

**检查方式**：人工检查

## 【推荐】清空表记录用TRUNCATE替代DELETE

**说明**：

当删除表中的记录时，在通常情况下，回滚段(rollback segments ) 用来存放可以被恢复的信息。如果你没有COMMIT事务，ORACLE会将数据恢复到删除之前的状态(准确地说是恢复到执行删除命令之前的状况) 。而当运用TRUNCATE时，回滚段不再存放任何可被恢复的信息。当命令运行后，数据不能被恢复，因此很少的资源被调用,执行时间也会很短。

TRUNCATE只在删除全表或者一个分区时适用，TRUNCATE是DDL不是DML。

**检查方式**：人工检查

## 【推荐】用EXISTS替换DISTINCT

**说明**：

当提交一个包含一对多表信息(比如部门表和雇员表)的查询时，避免在SELECT子句中使用DISTINCT。一般可以考虑用EXISTS替换，EXISTS 使查询更为迅速，因为RDBMS核心模块将在子查询的条件一旦满足后，立刻返回结果。

**<font color=red>反例</font>**

```sql
SELECT DISTINCT DEPT_NO,DEPT_NAME 
  FROM DEPT D, 
        EMP E 
 WHERE D.DEPT_NO = E.DEPT_NO
```

**正例**

```sql
SELECT DEPT_NO,DEPT_NAME 
  FROM DEPT D 
 WHERE EXISTS (
               SELECT ‘X' 
                 FROM EMP E 
                WHERE E.DEPT_NO = D.DEPT_NO
              )
```

**检查方式**：人工检查

## 【强制】用UNION ALL替换OR(适用于索引列)

**说明**：

通常情况下，用UNION ALL和LNNVL()函数替换WHERE子句中的OR将会起到较好的效果。对索引列使用OR将造成全表扫描。**注意，以上规则只针对多个索引列有效。**如果有column没有被索引，查询效率可能会因为你没有选择OR而降低。

在下面的例子中，LOC\_ID和P\_ID上都建有索引。

Note：

1. 不能用UNION替换OR，某些场景下UNION 替换后结果与OR操作结果不等；

2. 非索引列的不强制，需要结合具体业务场景分析处理。

**<font color=red>反例</font>**

```sql
SELECT A.LOC_ID, A.P_ID, A.LOC_DESC, A.REGION
  FROM LOCATION A
 WHERE A.LOC_ID = 5
    OR A.P_ID = 6; 
```

**正例**

```sql
SELECT A.LOC_ID, A.P_ID, A.LOC_DESC, A.REGION
  FROM LOCATION A
 WHERE A.LOC_ID = 5
 UNION ALL
SELECT A.LOC_ID, A.P_ID, A.LOC_DESC, A.REGION
  FROM LOCATION A
 WHERE A.P_ID = 6
   AND LNNVL(A.LOC_ID = 5); 
```

**检查方式**：工具检查（暂未支持）

## 【参考】关于索引效率

**说明**：

如果检索数据量超过30%的表中记录数，使用索引将没有显著的效率提高。在特定情况下，使用索引也许会比全表扫描慢，但这是同一个数量级上的区别，即这个情况下使用索引的效率并不比全表扫描的效率差太多。而通常情况下，使用索引比全表扫描要块几倍乃至几千倍。

**检查方式**：人工检查

## 【参考】尽量减少SQL复杂度

**说明**：

尽量减少SQL复杂度，用简单SQL完成任务，复杂的逻辑在代码中实现。对一个大结果集做排序，或者求唯一值，都是比较昂贵的计算，会占用大量数据库系统资源，如果在业务上确实有这方面的需求，尽量放在业务代码中实现。

**检查方式**：人工检查

## 【强制】Oracle中IN()参数的个数限制为50个

**说明：**

IN()参数的个数不能超过50个，参数过多会影响性能。

另外，Oracle本身对于IN()参数的个数也有限制，Oracle 9i超过256个会报错；Oracle 10g及以上版本超过1000个会报错，报错信息为：ORA-01795: maximum number of expressions in a list is 1000。

**<font color=red>反例1</font>**

```sql
SELECT TNAME, TYPE
  FROM T
 WHERE ID IN (1, 2, 3, 4, 5, 6, .. ., 50)
    OR ID IN (51, 52, .. ., 100)
```

**<font color=red>反例2</font>**

```sql
SELECT A.SUBS_UPP_ORDER_ID,
       A.SUBS_ORDER_ID,
       A.PRICE_PLAN_ID,
       A.ABS_EFF_DATE,
       A.ABS_EXP_DATE,
       A.REL_EFF_OFFSET,
       A.REL_EFF_UNIT,
       A.REL_EXP_OFFSET,
       A.REL_EXP_UNIT,
       A.OPERATION_TYPE,
       A.AGM_EXP_DATE,
       A.SP_ID,
       A.OFFER_ID,
       A.SUBS_UPP_INST_ID,
       B.PRICE_PLAN_CODE,
       B.PRICE_PLAN_NAME,
       CO.CREATED_DATE
  FROM SUBS_UPP_ORDER  A,
       PRICE_PLAN      B,
       SUBS_PRICE_PLAN C,
       SUBS_ORDER      S,
       CUST_ORDER      CO
 WHERE A.PRICE_PLAN_ID = B.PRICE_PLAN_ID
   AND B.PRICE_PLAN_ID = C.PRICE_PLAN_ID
   AND C.PRICE_PLAN_TYPE IN ('3', '5')
   AND S.SUBS_ORDER_ID = A.SUBS_ORDER_ID
   AND CO.CUST_ORDER_ID = S.CUST_ORDER_ID
   AND S.SUBS_ID = :1
   AND A.OPERATION_TYPE IN ('A', 'R')
   AND A.PRICE_PLAN_ID IN
       (845108, 845109, .. ., 864036, 864038) --超过50个参数
   AND CO.CREATED_DATE >= :2
   AND CO.CREATED_DATE <= :3
   AND CO.PART_ID IN (7, 8, 9)
 ORDER BY CO.CREATED_DATE DESC;
```

*Note: IN()参数个数超过50个。*

**正例1**

```sql
SELECT T.ID, T.NAME 
  FROM USER T
 WHERE EXISTS (SELECT U.ID
          FROM USER U
         WHERE U.NAME LIKE 'J%'
           AND U.ID = T.ID)
```

*Note: 当IN()参数个数过多时，可考虑修改为EXISTS子查询处理。*

**正例2**

```sql
--新建表
CREATE TABLE INLIST_T (PRICE_PLAN_ID NUMBER(12));

--将值预置到新建表
INSERT INTO INLIST_T VALUES (845108);
...
INSERT INTO INLIST_T VALUES (864038);
COMMIT;

--改写成关联查询
SELECT A.SUBS_UPP_ORDER_ID,
       --省略
  FROM SUBS_UPP_ORDER  A,
       PRICE_PLAN      B,
       SUBS_PRICE_PLAN C,
       SUBS_ORDER      S,
       CUST_ORDER      CO,
       INLIST_T        INT
 WHERE A.PRICE_PLAN_ID = B.PRICE_PLAN_ID
   AND B.PRICE_PLAN_ID = C.PRICE_PLAN_ID
   AND C.PRICE_PLAN_TYPE IN ('3', '5')
   AND S.SUBS_ORDER_ID = A.SUBS_ORDER_ID
   AND CO.CUST_ORDER_ID = S.CUST_ORDER_ID
   AND S.SUBS_ID = :1
   AND A.OPERATION_TYPE IN ('A', 'R')
   AND A.PRICE_PLAN_ID = INT.PRICE_PLAN_ID
   AND INT.PRICE_PLAN_ID IS NOT NULL
   AND CO.CREATED_DATE >= :2
   AND CO.CREATED_DATE <= :3
   AND CO.PART_ID IN (7, 8, 9)
 ORDER BY CO.CREATED_DATE DESC;
```

*Note: IN列表元素过多，且值可枚举，比如可通过配置项方式设置。可参照本例方式，新增表存放值列表，改成表关联查询。反例2可参考上述方法调整。*

**正例3** - SQL

```sql
VAR b1 VARCHAR2(2000);
EXEC :b1:='100,101,102,103,104,105,201,202,205,206,300,301,305,308,310,311,312';
WITH STR_LIST AS
(SELECT CAST(REGEXP_SUBSTR( :b1,'[^,]+', 1, LEVEL) AS NUMBER) AS VALUE
FROM DUAL
CONNECT BY LEVEL <= REGEXP_COUNT(:b1, '[^,]+')
)
SELECT OBJECT_NAME FROM T1
 WHERE T1.OBJECT_ID IN (SELECT VALUE FROM STR_LIST);
```

**正例3** - Java代码实现

```java
public List<DynamicDict> selectPurchaseSubsUppOrder(DynamicDict dict) throws BaseAppException {  
  
    String sqlStr = "WITH STR_LIST AS\n" +  
        " (SELECT TO_NUMBER(REGEXP_SUBSTR(:PRICE_PLAN_ID, '[^,]+', 1, LEVEL)) AS VALUE\n" +  
        " FROM DUAL\n" +  
        " CONNECT BY LEVEL <= REGEXP_COUNT(:PRICE_PLAN_ID, '[^,]+'))\n" +  
        " SELECT * FROM " +  
        "(SELECT A.SUBS_UPP_ORDER_ID,\n" +  
        " A.SUBS_ORDER_ID,\n" +  
        " A.PRICE_PLAN_ID,\n" +  
        " A.ABS_EFF_DATE,\n" +  
        " A.ABS_EXP_DATE,\n" +  
        " A.REL_EFF_OFFSET,\n" +  
        " A.REL_EFF_UNIT,\n" +  
        " A.REL_EXP_OFFSET,\n" +  
        " A.REL_EXP_UNIT,\n" +  
        " A.OPERATION_TYPE,\n" +  
        " A.AGM_EXP_DATE,\n" +  
        " A.SP_ID,\n" +  
        " A.OFFER_ID,\n" +  
        " A.SUBS_UPP_INST_ID,\n" +  
        " B.PRICE_PLAN_CODE,\n" +  
        " B.PRICE_PLAN_NAME,\n" +  
        " CO.CREATED_DATE\n" +  
        " FROM SUBS_UPP_ORDER A ,PRICE_PLAN B, SUBS_PRICE_PLAN C, SUBS_ORDER S, CUST_ORDER CO\n" +  
        " WHERE A.PRICE_PLAN_ID = B.PRICE_PLAN_ID\n" +  
        " AND B.PRICE_PLAN_ID = C.PRICE_PLAN_ID\n" +  
        " AND C.PRICE_PLAN_TYPE IN ('3', '5')\n" +  
        " AND S.SUBS_ORDER_ID = A.SUBS_ORDER_ID\n" +  
        " AND CO.CUST_ORDER_ID = S.CUST_ORDER_ID\n" +  
        " AND S.SUBS_ID = :SUBS_ID\n" +  
        " [AND A.OPERATION_TYPE= :OPT]\n" +  
        " [AND A.OPERATION_TYPE IN (&OPERATION_TYPES&)]\n" +  
        " [AND CO.CREATED_DATE >= :START_DATE ]\n" +  
        " [AND CO.CREATED_DATE <= :END_DATE ]\n" +  
        " [AND CO.PART_ID IN (&PART_IDS&) ] ) T\n" +  
        "WHERE T.PRICE_PLAN_ID IN (SELECT VALUE FROM STR_LIST) ";  
    ParamMap pm = new ParamMap();  
    if (dict.getLong("SUBS_ID") != null) {  
      pm.set("SUBS_ID", dict.getLong("SUBS_ID"));  
    }  
    if (StringUtil.isNotEmpty(dict.getString("OPERATION_TYPES"))) {  
      pm.set("OPERATION_TYPES", dict.getString("OPERATION_TYPES"));  
    }  
    if (dict.getDate("START_DATE") != null) {  
      pm.set("START_DATE", dict.getDate("START_DATE"));  
    }  
    if (dict.getDate("END_DATE") != null) {  
      pm.set("END_DATE", dict.getDate("END_DATE"));  
    }  
    if (StringUtil.isNotEmpty(dict.getString("PART_IDS"))) {  
      pm.set("PART_IDS", dict.getString("PART_IDS"));  
    }  
    if (StringUtil.isNotEmpty(dict.getString("PRICE_PLAN_ID"))) {  
      pm.set("PRICE_PLAN_ID", dict.getString("PRICE_PLAN_ID"));  
    }  
    return (List<DynamicDict>) query(sqlStr, pm, null, null, BOMapper.getInstance());  
}
```

*Note: 
1）IN列表元素过多, 个数不固定，比如从表中关联查询的值。当个数过多的时候会导致不走索引而走全表扫描。反例2可参考上述方法调整。
2）Oracle数据中，REGEXP_SUBSTR函数支持最大长度4000。如果使用此方法，需要考虑参数长度，当参数过长时需要适当分段处理。*

**正例3** - 临时表处理方式

```sql
SELECT NVL(A.BAL_ID1,-1)            BAL_ID1, 
       NVL(A.BAL_ID2,-1)            BAL_ID2, 
       NVL(A.BAL_ID3,-1)            BAL_ID3, 
       NVL(A.BAL_ID4,-1)            BAL_ID4, 
       NVL(A.BAL_ID5,-1)            BAL_ID5, 
       NVL(A.BAL_ID6,-1)            BAL_ID6, 
       NVL(A.BAL_ID7,-1)            BAL_ID7, 
       NVL(A.BAL_ID8,-1)            BAL_ID8, 
       NVL(A.BAL_ID9,-1)            BAL_ID9, 
       NVL(A.DEFAULT_BAL_ID1,-1)            DEFAULT_BAL_ID1, 
       NVL(A.DEFAULT_BAL_ID2,-1)            DEFAULT_BAL_ID2, 
       NVL(A.DEFAULT_BAL_ID3,-1)            DEFAULT_BAL_ID3, 
       NVL(A.DEFAULT_BAL_ID4,-1)            DEFAULT_BAL_ID4, 
       NVL(A.DEFAULT_BAL_ID5,-1)            DEFAULT_BAL_ID5, 
       NVL(A.DEFAULT_BAL_ID6,-1)            DEFAULT_BAL_ID6, 
       NVL(A.DEFAULT_BAL_ID7,-1)            DEFAULT_BAL_ID7, 
       NVL(A.DEFAULT_BAL_ID8,-1)            DEFAULT_BAL_ID8, 
       NVL(A.DEFAULT_BAL_ID9,-1)            DEFAULT_BAL_ID9, 
       A.SUBS_ID                    SUBS_ID, 
       NVL(A.ACCT_ID1,-1)           ACCT_ID1, 
       NVL(A.ACCT_ID2,-1)           ACCT_ID2, 
       NVL(A.ACCT_ID3,-1)           ACCT_ID3, 
       NVL(A.ACCT_ID4,-1)           ACCT_ID4, 
       NVL(A.ACCT_ID5,-1)           ACCT_ID5, 
       NVL(A.ACCT_ID6,-1)           ACCT_ID6, 
       NVL(A.ACCT_ID7,-1)           ACCT_ID7, 
       NVL(A.ACCT_ID8,-1)           ACCT_ID8, 
       NVL(A.ACCT_ID9,-1)           ACCT_ID9, 
       NVL(A.ACCT_ITEM_TYPE_ID1,-1) ACCT_ITEM_TYPE_ID1, 
       NVL(A.ACCT_ITEM_TYPE_ID2,-1) ACCT_ITEM_TYPE_ID2, 
       NVL(A.ACCT_ITEM_TYPE_ID3,-1) ACCT_ITEM_TYPE_ID3, 
       NVL(A.ACCT_ITEM_TYPE_ID4,-1) ACCT_ITEM_TYPE_ID4, 
       NVL(A.ACCT_ITEM_TYPE_ID5,-1) ACCT_ITEM_TYPE_ID5, 
       NVL(A.ACCT_ITEM_TYPE_ID6,-1) ACCT_ITEM_TYPE_ID6, 
       NVL(A.ACCT_ITEM_TYPE_ID7,-1) ACCT_ITEM_TYPE_ID7, 
       NVL(A.ACCT_ITEM_TYPE_ID8,-1) ACCT_ITEM_TYPE_ID8, 
       NVL(A.ACCT_ITEM_TYPE_ID9,-1) ACCT_ITEM_TYPE_ID9, 
       NVL(A.SP_ID,0)      SP_ID, 
       A.BILLING_CYCLE_ID           BILLING_CYCLE_ID, 
       A.BYTE_UP+A.BYTE_DOWN USE_FLUX, A.DURATION USE_DURATION,  
       A.CHARGE1                    CHARGES1, 
       A.CHARGE2                    CHARGES2, 
       A.CHARGE3                    CHARGES3, 
       A.CHARGE4                    CHARGES4, 
       A.CHARGE5                    CHARGES5, 
       A.CHARGE6                    CHARGES6, 
       A.CHARGE7                    CHARGES7, 
       A.CHARGE8                    CHARGES8, 
       A.CHARGE9                    CHARGES9, 
       A.RATE_USAGE1             RATE_USAGE1, 
       A.RATE_USAGE2             RATE_USAGE2, 
       A.RATE_USAGE3             RATE_USAGE3, 
       A.RATE_USAGE4             RATE_USAGE4, 
       A.RATE_USAGE5             RATE_USAGE5, 
       A.RATE_USAGE6             RATE_USAGE6, 
       A.RATE_USAGE7             RATE_USAGE7, 
       A.RATE_USAGE8             RATE_USAGE8, 
       A.RATE_USAGE9             RATE_USAGE9, 
       A.DISCT_PERCENT1             DISCT_PERCENT1, 
       A.DISCT_PERCENT2             DISCT_PERCENT2, 
       A.DISCT_PERCENT3             DISCT_PERCENT3, 
       A.DISCT_PERCENT4             DISCT_PERCENT4, 
       A.DISCT_PERCENT5             DISCT_PERCENT5, 
       A.DISCT_PERCENT6             DISCT_PERCENT6, 
       A.DISCT_PERCENT7             DISCT_PERCENT7, 
       A.DISCT_PERCENT8             DISCT_PERCENT8, 
       A.DISCT_PERCENT9             DISCT_PERCENT9, 
       A.USAGE1                     USAGE1, 
       A.USAGE2                     USAGE2, 
       A.USAGE3                     USAGE3, 
       A.USAGE4                     USAGE4, 
       A.USAGE5                     USAGE5, 
       A.USAGE6                     USAGE6, 
       A.USAGE7                     USAGE7, 
       A.USAGE8                     USAGE8, 
       A.USAGE9                     USAGE9, 
       NVL(A.BASIC_ACCT_ITEM_TYPE_ID,-1)  BASIC_ACCT_ITEM_TYPE_ID, 
       NVL(A.BASIC_CHARGE,0)  BASIC_CHARGE, 
       A.START_TIME           EVENT_BEGIN_TIME, 
       A.PAID_ACCT_ID           PAID_ACCT_ID, 
       NVL(A.RESERVE_ATTR14,0)   RESERVE_ATTR14, 
       A.RE_ID                RE_ID ,
       A.STATE_DATE STATE_DATE 
FROM EVENT_USAGE_1058 A  
WHERE (A.PAID_ACCT_ID > 0 OR A.SRC_EVENT_INST_ID <= 0) 
      AND A.BILLING_CYCLE_ID = 1058  
      AND A.SUBS_ID IN(SELECT SUBS_ID FROM TEMP_SUBS_ACCT_20200001) 
      AND A.STATE = 'A';
```

*Note:
1) TEMP_SUBS_ACCT_20200001是临时表。
2) IN列表元素过多且个数不固定（例如从表中关联查询获取的值），推荐通过临时表方式处理，但需注意临时表必须有相应的清理机制。

**检查方式**：工具检查

**案例说明**：
**案例1** - 故障单1810213
**故障描述**：
某项目发现CCDB存在大量的硬解析，影响所有前台业务。
**原因分析**：
检查发现业务SQL中IN操作符使用时未绑定变量导致。
**解决方案**：
业务侧改造硬解析的SQL，使用绑定变量方式。

**案例2** - 故障单3760790
**故障描述**：
某项目Shard2数据库连接超时，影响前台充值，订购，激活等KPI大概15分钟(切双机影响)。
**原因分析**：
分析发现CPU增长到70%是SQL导致的，后续又增长到100%。
ORACLE 的分析结论：SQL 语句的写法不理想，导致 Hard Parse 时间长，高并发的情况下引发 Mutex 等待。
有问题的业务SQL语句使用IN操作符，且非参数化方式，从配置文件中获取pricePlanId列表作为参数值，该列表数量大约500个，超过了50个。因为IN参数过多，导致硬解析等性能问题。
**解决方案**：
业务侧参照oracle建议，将配置文件中的pricePlanId列表存放到表中，优化SQL语句通过表关联方式进行相关查询。
同时排查其他使用IN操作符的业务SQL，对于存在隐患的SQL进行整改，使用绑定变量方式指定IN操作符中参数，且限制IN中参数个数不多于50个，分多批次执行。

**案例3** - 故障单3796439
**故障描述**：
某产品中有一个超长SQL，通过把多个包含IN子句的查询用UNION拼接成一个超长的SQL，该SQL产生超过400个子执行计划(version count)，大量消耗Shared Pool资源，导致Shared Pool接近耗尽，进而触发了Oracle的"Shared Pool Flush"内部事件把Shared Pool几乎清空，引发缓存失效，最终导致另一个高频SQL的执行计划因缓存被清空而发生跳变，造成严重性能隐患。
**原因分析**：
Oracle SQL开发规范中设有IN子句参数不得超过50个的限制条款，开发人员为避免违规该规范，采用了将多个包含IN子句的查询通过UNION拼接成单个超长SQL的方式进行处理，但此举反而引发了更严重的性能问题。
**解决方案**：
根据实际使用场景，参照本规范中提供的正例2(IN列表元素可枚举)或者正例3(IN列表元素个数不固定)进行修改。
**Note**：
历史代码中此类隐患可能大量存在，此前开发人员为了避免SQL违规，针对该条款缺乏合规的实现指引，于是采用了循环拼接SQL的次优方式。当前历史代码中可能仍遗留此类问题，需要各业务单位关注并及时排查整改。

## 【推荐】 SQL的条件子句中如果同时有and和or子句时，条件之间必须加括号以清晰表示多个条件之间的组合关系

**正例**

```sql
SELECT A.CUST_ID, A.NET_TYPE
  FROM CUST A
 WHERE (A.NET_TYPE = 'X' OR A.NET_TYPE = 'A' OR A.NET_TYPE = 'P')
   AND A.CUST_TYPE='C'
```

**检查方式**：工具检查（有or没有括号的需要告警）

## 【推荐】插入和更新操作时，把数据库中字段类型为LONG，LOB的字段放置在最后设置

**说明**：

插入和更新操作时，如果将LONG和LOB类型的字段放到其他字段前，就可能会导致ora-01461（can bind a LONG value only for insert into a LONG column）错误。

**<font color=red>反例</font>**

```xml
<insert id="insertByteArray" parameterType="org.activiti.engine.impl.persistence.entity.ByteArrayEntity">
   insert into ${prefix}ACT_GE_BYTEARRAY(ID_, REV_, NAME_, BYTES_, DEPLOYMENT_ID_)
   values (
     #{id, jdbcType=VARCHAR},
     1, 
     #{name, jdbcType=VARCHAR},
     #{bytes, jdbcType=BLOB},
     #{deploymentId, jdbcType=VARCHAR}
   )  
 </insert>
```

*Note: bytes参数为BLOB类型，未作为最后一个参数，当bytes存放字段值超过4000时，会引发long转换，导致问题。*

**正例**

```xml
<insert id="insertByteArray" parameterType="org.activiti.engine.impl.persistence.entity.ByteArrayEntity">
   insert into ${prefix}ACT_GE_BYTEARRAY(ID_, REV_, NAME_, DEPLOYMENT_ID_, BYTES_)
   values (
     #{id, jdbcType=VARCHAR},
     1, 
     #{name, jdbcType=VARCHAR},
     #{deploymentId, jdbcType=VARCHAR},
     #{bytes, jdbcType=BLOB}
   )  
 </insert>
```

*Note: bytes参数为BLOB类型，作为最后一个参数，代码可正常处理*

**检查方式**：人工检查

**故障单参考**：ZMP2421246

# 模板与举例

## 命名与注释

### 例一

**正例**

```sql
CREATE OR REPLACE PROCEDURE P_SYS_SAVEMANAGERLOG
(
    IC_SUB_SYS_CODE    IN CHAR,
    IN_OPER_STAFF_ID   IN NUMBER,
    IV_START_VALUE_1   IN VARCHAR2,
    IV_END_VALUE_1     IN VARCHAR2,
    IV_START_VALUE_2   IN VARCHAR2,
    IV_END_VALUE_2     IN VARCHAR2,
    ON_RETURN_CODE     OUT VARCHAR2
)
----------------------------------------------------------------------- 
-- Description: save management log
-- Author:  yourname 
-- Date:  2012/04/23 
----------------------------------------------------------------------- 
-- Param: IV_SUB_SYS_CODE: ******
-- Param: IN_OPER_STAFF_ID: ******
-- Param: IV_START_VALUE_1: ******
-- Param: IV_END_VALUE_1: ******
-- Param: IV_START_VALUE_2: ******
-- Param: IV_END_VALUE_2: ******
-- Param: ON_RETURN_CODE: ******
-----------------------------------------------------------------------
IS
   dCurrentDate	DATE; -- current date
BEGIN

END;
```

### 例二

**正例**

```sql
CREATE OR REPLACE FUNCTION F_SYS_GETSEQID
(
    IV_SEQ_NAME IN VARCHAR2
)
RETURN VARCHAR2
----------------------------------------------------------------------- 
-- Description: ******
-- Author: YourName 
-- Date: 2010/10/12 
-- Param: OV_SEQ_NAME ******                                 
-----------------------------------------------------------------------
IS
    vDate   VARCHAR2(8);
    vSeq    VARCHAR2(8);
    vSeqname   VARCHAR2(20);
    vSeqId   VARCHAR2(16);
BEGIN
END;
```

## 控制与DML

### IF语句

**正例**

```sql
BEGIN
    IF vRes = 0 THEN
        NULL;
    ELSE
        NULL;
    END IF;
END;
```

### 循环语句

**正例**

```sql
BEGIN
    LOOP
        EXIT WHEN ....;
    END LOOP;
END;
```

### SELECT语句

**正例**

```sql
BEGIN
    SELECT ... INTO ...
      FROM TABLE
     WHERE condition1
       AND condition2;
EXCEPTION
     WHEN NO_DATA_FOUND THEN
         ......;
     WHEN OTHERS THEN
        vRes := -1;
        vErrInfo := 'error description: '||sqlerrm;
        ......;
END;
```

### INSERT语句

**正例**

例1：

```sql
BEGIN
   INSERT INTO TABLENAME(COLUMN1, COLUMN2)
   VALUES(VALUE1, VALUE2);
EXCEPTION
   WHEN OTHERS THEN
        vRes := -1;
        vErrInfo := 'error description: ' || sqlerrm;
        ......;
END;
```

例2：

```sql
BEGIN
    INSERT INTO TABLENAME
    (
        COLUMN1, COLUMN2, … COLUMNn,
        COLUMNo, COLUMNp
    )
    VALUES
    (
        VALUE1, VALUES2, … , VALUESn,
        VALUEo, VALUEp
    );
EXCEPTION
    WHEN OTHERS THEN
        vRes := -1;
        vErrInfo := 'error description: ' || sqlerrm;
        ......;
END;
```

### UPDATE语句

**正例**

```sql
BEGIN
   UPDATE TABLENAME
      SET A = B, C = D
    WHERE condition1
      AND condition2;
   COMMIT;
EXCEPTION
     WHEN OTHERS THEN
        vRes := -1;
        vErrInfo := 'error description: '||sqlerrm;
        ......;
END;
```

### DELETE语句

**正例**

```sql
BEGIN
    DELETE TABLENAME
     WHERE condition1
       AND condition2;
    COMMIT;
EXCEPTION
     WHEN OTHERS THEN
        vRes := -1;
        vErrInfo := 'error description: '||sqlerrm;
        ......;
END;
```

### 存储过程执行

**正例**

```sql
BEGIN
   P_PROCEDURE_NAME ( vPara1,
                      vPara2,
	                  vPara3,
	                  ……,
	                  vRes,
	                  vErrInfo
	                 );
   IF vRes = -1 THEN
        vErrInfo:='procedure_name:ex_procedure_name return error '||spres;
        ......
   END IF;
END;
```

## 数据库包

### 包声明

**正例**

```sql
CREATE OR REPLACE PACKAGE PACKAGENAME
----------------------------------------------------------------------- 
-- Description: description of this package
-- Author:  yourname 
-- Date:  2012/04/23 
-----------------------------------------------------------------------
IS
    ...

	/**
     * description information
     */
    PROCEDURE PROCEDURENAME1
    (
       ...
    );

	/**
     * description information
     */
    PROCEDURE PROCEDURENAME2
    (
       ...
    );

	/**
     * description information
     */
    FUNCTION FUNCTIONNAME1
    (
       ...
    )
    RETURN ...;

    ...;
END PACKAGENAME;

```

### 包体

**正例**

```sql
CREATE OR REPLACE PACKAGE BODY PACKAGENAME
----------------------------------------------------------------------- 
-- Description: description of this package
-- Author:  yourname 
-- Date:  2012/04/23 
-----------------------------------------------------------------------
IS
    ...

	/**
     * description information
     */
    PROCEDURE PROCEDURENAME1
    (
      ...
    )
    IS
   
    BEGIN
       Some SQL;
       ...;
    END PROCEDURENAME1;
    ------------------------------------------------------------------
    ...
    other package procedure and function definitions
END PACKAGENAME;

```

### 存储过程

**正例**

```sql
CREATE OR REPLACE PROCEDURE PROCEDURENAME1
(
 …
)
IS

BEGIN
  ...;
EXCEPTION
     WHEN NO_DATA_FOUND THEN
        ...;
     WHEN OTHERS THEN
        ...;
END PROCEDURENAME1;

```

### 函数

**正例**

```sql
CREATE OR REPLACE FUNCTION FUNCTIONNAME1
(
)
RETURN INTEGER
/**
  * description information
  */
IS

BEGIN
    ...;
    RETURN ...;
EXCEPTION
     WHEN OTHERS THEN
        ...;
    RETURN …;
END FUNCTIONNAME1;
```

# 附录

## 参考文档

2. ZSmart国际业务运营中心BSS产品线 - SQL编程规范 - Oracle分册.doc

3. ZSmart开发一部 - SQL编程规范.doc

4. ZSmart开发一部 - SQL编程规范检查单.xls

5. ZSmart数据库设计与开发规范v1.0b.doc

## Oracle索引与分页查询优化

分页查询的性能往往是一个系统的痛点，本文主要介绍如何通过索引来优化分页查询语句。

不管是 单表分页查询 还是 多表分页查询，都是要利用索引已 排序的特点，消除执行计划中的排序步骤（消除 SORT ORDER BY STOPKEY , 只有 COUNT STOPKEY）。
![image](uploads/109475/b9158a88-b426-4e7e-8578-4558808ec7b8/image.png)

### 索引与单表分页查询优化

如果分页语句中有排序，要利用索引已经排序的特性，将 ORDER BY 的列包含在索引中。

#### 不带过滤条件的分页查询

![image](uploads/109475/f1c50856-973b-4854-96b1-8576e12e2ffc/image.png)

- 单字段排序
  如果排序列是单列，且所建索引是只含该字段的索引，那么该字段一定不能为可空
  字段非空
  ![image](uploads/109475/9a3a4bb2-baf4-4c43-99f8-0923ff7c6c92/image.png)
  字段可空
  ![image](uploads/109475/0f7b7170-9767-4875-af1c-2bbbbd485195/image.png)

- 多字段排序
  如果排序列有多列，创建索引的时候，我们要将所有的排序列包含在索引中，并且要注意排序列先后顺序（语句中是怎么排序的，创建索引的时候就对应排序）。
  多字段排序，至少一个字段要为非空
  ![image](uploads/109475/3cfa5d86-c4eb-4a4c-b8c2-bc0735121647/image.png)
  Note：单字段排序和多字段排序中的字段都是可空时，可通过给索引中加入一个常量，让排序走索引。

#### 带过滤条件的分页语句

继承（不带过滤条件的分页查询）原则。
![image](uploads/109475/500ead10-a120-415a-999e-fdb5bffde695/image.png)

索引符合 ESR 原则
过滤条件有等值条件，也有非等值条件，要将等值过滤条件优先组合在一起，然后将排序列放在等值 过滤条件后面，最后将非等值过滤列放在序列后面（ESR 原则）。
ESR
E 精确(Equal)匹配的字段放最前面
S 排序(Sort)条件放中间
R 范围(Range)匹配的字段放最后面)
![image](uploads/109475/140a2158-c613-4666-b250-e9e8d77e542d/image.png)
![image](uploads/109475/d35fd1f3-9c04-424b-8a33-2e05dbe9659d/image.png)

Note：如果分页语句中没有等值过滤条件，我们应该先将排序列放在索引前面，将非等值过滤列放在后面。

### 索引与多表关联分页查询优化

多表关联分页语句必须要走 NESTED LOOPS 嵌套循环连接，并且要消除 SORT ORDER BY。为什么多表关联的 分页语句必须走嵌套循环？ 这是因为嵌套循环是驱动表传值给被驱动表，如果驱动表返回的数据有有序的，那么关联之后 的结果集也是有序的，这样就可以消除 SORT ORDER BY。
![image](uploads/109475/9f2bde60-4c2e-4231-b5b1-07c4de1e9ae2/image.png)

- 多表关联分页语句 ORDER BY 排序字段必须来自同一个表（同表不同索引也不行）。
  分页语句排序列来自多个表，这就需要等两个表关联完成之后再进行排序，这样无法消除 SORT ORDER BY，所以 SQL 就无法优化了，如果要想优化这个分页语句，必须与研发沟通，去掉一个表的排序列。
  ![image](uploads/109475/876812ac-228a-420a-9127-64cc857a6a80/image.png)
  ![image](uploads/109475/852a429a-abfd-4505-b518-fc021246302b/image.png)

- 语句中不能有 DISTINCT, GROUP BY, MAX, MIN, AVG, UNION, UNION ALL
  ![image](uploads/109475/a96b1a72-e236-47a6-a902-cd08d8acdcdb/image.png)
  ![image](uploads/109475/f4ea5f29-ec1a-48e4-b5e8-2239db7cc40d/image.png)

- 多表关联如果有外连接，必须选择主表的列作为排序列，且驱动表必须是主表。
  ![image](uploads/109475/6105c9cd-f9a2-41a5-aced-0aa794fea19a/image.png)
  ![image](uploads/109475/dd4bfff2-5dae-4226-9acb-86648b6aae6c/image.png)

### 分页查询中排序的表是分区表

跨分区查询：索引要建成GLOBAL索引
单分区查询：索引要建成LOCAL索引

### 总结

- 使用的索引要把 ORDER BY 字段带上，ORDER BY 字段尽可能少 (不排序就不用)；
- 如果谓词条件有等值条件，可以放到 ORDER BY 字段前面，组成联合索引：WHERE COL1='xxx' AND COL2>'yyyy' ORDER BY COL3 ==>(COL1,COL3,COL2)；
- 如果 ORDER BY 字段都是 ASC 或 DESC，普通联合索引即可，优化器一般可以自动选择 ASC 或 DESC 扫描(也可以使用 HINT 强制 DESC)；
- 如果是 ORDER BY COL1 DESC,COL2 ASC，则需要创建 DESC 索引( COL1 DESC,COL2)；
- LEFT JOIN：主要看主表,ORDER BY 主表的字段；
- 分页前一般会计算满足条件的所有记录数，这一步可能比较耗时; 如果不用显示页数，可以在取当前页时多取一条记录，如果能取到，则显示"下一页"，否则不显示；
- 包含 DISTINCT/UNION 无法消除 SORT ORDER BY；

# 本文件评审、修正记录

| 文件名称 | SQL编程规范 – Oracle分册                                     |               |               |        |
| -------- | ------------------------------------------------------------ | ------------- | ------------- | ------ |
| 序号     | 流程                                                         | 拟制人/审核人 | 拟制/审核时间 | 版本号 |
| 1        | 编写                                                         | 赵灵歌        | 2015/05/04    | V0.1   |
| 2        | 替换文档模板，调整文档格式，加入强制/推荐/参考标识，补充条目，并增加检查方式的说明，按照内部评审意见更新内容。 | 崔丽莉        | 2019/12/23    | V0.2   |
| 3        | 发布                                                         | 数据库规范组  | 2019/12/28    | V1.0   |
| 3        | 结合核心组成员和数据库规范培训群提及的问题进行修订，涉及如下：<br/>1. 格式错误修订<br/>2. 4.3章节 更新条目及描述信息；<br/>3. 4.13章节完善说明信息；<br/>4. 5.8章节条目和内容更新；<br/>5. 新增5.11章节，IN()函数参数个数限制；<br/>6. 章节4.9.2，补充例子中的说明信息 | 崔丽莉        | 2020/06/22    | V1.0.1 |
| 4        | 根据数据库规范核心组评审意见修改                             | 崔丽莉        | 2020/08/31    | V1.0.2 |
| 5        | 根据ZMP\2248780（一级故障改进单）补充5.12章节               | 崔丽莉        | 2020/11/14    | V1.0.3 |
| 6        | 根据ZMP\2387057（一级故障单改进单）补充4.23章节             | 崔丽莉        | 2021/03/19    | V1.0.4 |
| 7        | 更新4.3章节内容，增加IN子查询也需要绑定变量的说明和举例      | 崔丽莉        | 2021/03/29    | V1.0.5 |
| 8        | 1. 修正章节3.2.3举例中的错误；<br/>2. 章节3.4.1.1规范条目变更并调整说明信息；<br/>3. 调整5.8章节规范条目及其说明和举例信息； | 崔丽莉        | 2021/05/28    | V1.0.6 |
| 9        | 发布                                                         | 数据库规范组  | 2021/05/30    | V1.1   |
| 10       | 1. 修改章节5.11规范条目，oracle IN()函数参数个数限制的条款，由原来1000，调整为50，且对应条目由推荐修改为强制，同时更新了说明信息；<br/>2. 章节4.9.2 增加说明信息，使用数据库隐式转换功能，可能会走不上索引，导致全表扫描，并补充了对应的正反例。<br/>3. 新增章节5.13 插入和更新操作时，需要将Long和LOB类型字段放最后设置。<br/>4. 章节4.21 关于并行度使用的条目，补充了说明信息即针对为何不要直接使用/*+ PRARLLEL */，增加了原因说明。 | 崔丽莉        | 2021/6/30     | V1.1.1 |
| 11       | 增加4.24章节 表关联避免出现笛卡尔积的情况 。                 | 崔丽莉        | 2021/7/21     | V1.1.2 |
| 12       | 修改4.24章节，根据规范组建议修改。                           | 崔丽莉        | 2021/7/30     | V1.1.3 |
| 13       | 章节4.14增加说明信息 和 故障单参考信息                       | 崔丽莉        | 2021/12/27    | V1.1.4 |
| 14       | 发布                                                         | 数据库规范组  | 2021/12/30    | V1.2   |
| 15       | 章节4.9.3 完善规范条目描述说明                               | 崔丽莉  | 2022/06/01    | V1.2.1   |
| 16       | 发布                              | 数据库规范组  | 2022/06/14    | V1.3   |
| 17       | 1. 修正4.10章节正例错误； <br/> 2. 修正4.21章节正例反例，将中文引号修改为英文引号；<br/> 3. 修正5.12章节正例，将中文引号修改为英文引号； <br/> 4. 修正5.13章节反例，调整函数参数BYTES_的位置；| 数据库规范组  | 2024/05/20    | V1.3.1   |
| 18       | 发布                              | 数据库规范组  | 2024/05/22    | V1.4   |
| 19       | 修正4.9.2章节 反例1和正例1中 涉及变量引用表达错误的地方 | 崔丽莉  | 2024/09/13    | V1.4.1   |
| 20       | 发布                              | 数据库规范组  | 2024/09/18    | V1.5   |
| 21       | 1. 章节4.14 规范条款更新，修改前：【强制】程序代码中禁止使用DB_LINK，修改后：【强制】程序代码中禁止使用Database Link进行任何跨库访问。同时更新说明信息，去掉故障参考单，补充案例说明。  <br/> 2. 章节4.15 规范条款更新，修改前：【推荐】其他场景下尽量不使用DB_LINK，修改后：【推荐】Database Link仅在访问频率较低的非程序调用场景下使用，如跨库的数据割接、数据同步、数据迁移、报表生成等。同时更新说明信息和举例。<br/> 3. 章节4.19 规范条款更新，修改前【推荐】查询分页场景，建议如下分页格式，先查询过滤出一部分数据，再做下一层过滤查询，修改后【推荐】WEB页面分页查询使用多层SQL方式，建议如下分页格式，先查询过滤出一部分数据，再做下一层过滤查询，并增加了说明信息 和 案例说明。 <br/> 4. 新增4.25规范 【强制】分页查询的内层子查询中必须使用ORDER BY对数据进行排序，且建立在有索引的列上，确保分页查询时获取数据的一致性和正确性。 <br/> 5. 新增4.26规范 【推荐】后台JOB批处理查询使用游标方式处理。 <br/>6. 章节5.11 【强制】Oracle中IN()参数的个数限制为50个，更新正反例 和 案例说明。<br/> 7. 新增7.2章节 Oracle索引与分页查询优化。      | 崔丽莉  | 2025/07/18    | V1.5.1   |
| 22       | 发布                              | 数据库规范组  | 2025/07/25    | V1.6   |
| 23       | 修订章节5.11“【强制】Oracle中IN()参数的个数限制为50个”的举例信息，修正[正例1]中的SQL，调整[正例3]中的缩进格式。| 崔丽莉  | 2025/08/15    | V1.6.1   |
| 24       | 发布                              | 数据库规范组  | 2025/08/22    | V1.7   |
| 25       | 修订章节5.11“【强制】Oracle中IN()参数的个数限制为50个”的正例3，将其中CASE修改为CAST。| 崔丽莉  | 2025/10/18    | V1.7.1   |
| 26       | 发布                              | 数据库规范组  | 2025/10/27    | V1.8   |
| 27       | 1. 新增章节“4.9.6. 【推荐】当SQL的WHERE条件涉及多个可用索引时，必须在研发阶段评估执行计划跳变风险，并采取规避措施”（规范来源：严重生产故障3796253,981078,1110043）<br/> 2.修改章节“5.11. 【强制】Oracle中IN()参数的个数限制为50个”：新增 “案例3 - 故障单3796439”说明 和 “正例3 - 临时表处理方式”  | 崔丽莉  | 2026/06/22    | V1.8.1   |
| 28       | 发布                              | 数据库规范组  | 2026/07/20    | V1.9   |
