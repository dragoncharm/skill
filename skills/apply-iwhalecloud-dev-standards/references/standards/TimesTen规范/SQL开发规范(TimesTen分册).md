![image](uploads/4067/0a92a1da-9df9-4696-a012-4c6dd13e9179/PG_dev_TT.png)

# 概述

## 编写目的

- 统一SQL语句编写格式。
- 让SQL语句更美观，更易阅读。
- 增强SQL可维护性。
- 提醒关注TimesTen中易发的一些性能问题。

## 适用范围

开发人员在使用TimesTen 6.X及其后版本时，需参考和遵循此规范。

## 角色和职责

开发：负责按照SQL规范进行SQL编码；

# SQL开发规范

## SQL书写规范

对于Java Source、C/C++程序中编写的SQL语句，建议在最大程度上遵循此规范。无法适用此规范的场景可以自行考虑格式，但必须遵循“格式整齐、美观大方”的总体原则。

具体的书写格式与布局请参考《SQL开发规范\_-\_Oracle分册》，TimesTen的SQL相对更简单，不赘述。

## 性能优化

### 【推荐】尽量减少SELECT要返回的数据列和数据集

**说明：**

尽量只返回有必要的返回的列，多余的列不要出现在SELECT子句当中。

对于数据集，也尽量只返回必要的数据。

**<font color=red>反例</font>**

```sql
SELECT * FROM T1 WHERE COL2=?
```

**正例**

例1：

```sql
SELECT COL1 FROM T1 WHERE COL2=?
```

例2：

```sql
SELECT FIRST {N} COL1 FROM T1 WHERE COL2=?
```

*Note：在只返回前N条记录时候请使用 FIRST 关键字*

**检查方式**：人工检查

### 【推荐】尽量避免使用ORDER BY

**说明：**

尽可能不要在SQL中使用ORDER BY子句，特别是在高并发的业务场景下，这会消耗TimesTen性能，在负载比较重的机器上，会较大程度影响系统的整体性能。排序操作放到Java/C++等业务代码中实现。

*Note：不是绝对禁止使用，如果是在业务低峰期，而且ORDER BY能够带来很大的便利性的情况下，是可以使用的。*

**检查方式**：人工检查

### 【强制】禁止多表关联操作

**说明：**

每个SQL尽量只对单表进行CRUD（增加(Create)、检索(Retrieve)、更新(Update)和删除(Delete)）操作，不用对多表进行关联操作，可以在业务代码中实现相关功能。

**<font color=red>反例</font>**

```sql
SELECT A.GROSS_BAL
  FROM BAL A
 INNER JOIN BAL B
    ON A.BAL_ID = B.BAL_ID
 WHERE A.BAL_ID = ?
```

**检查方式**：人工检查

### 【推荐】尽量少使用函数

**说明：**

过多的使用函数会消耗TimesTen性能，相关的功能尽可能在业务代码中实现。

**<font color=red>反例</font>**

```sql
UPDATE BAL T
   SET T.GROSS_BAL   = T.GROSS_BAL + -1000,
       T.UPDATE_DATE = DECODE(to_date('2015-05-01 22:57:36',
                                      'yyyy-mm-dd hh24:mi:ss'),
                              NULL,
                              SYSDATE,
                              to_date('2015-05-01 22:57:36',
                                      'yyyy-mm-dd hh24:mi:ss')),
       T.INIT_BAL    = -1000,
       T.EXP_DATE = CASE
                      WHEN T.EXP_DATE IS NULL THEN
                       DECODE(to_date('2015-07-02 00:00:00',
                                      'yyyy-mm-dd hh24:mi:ss'),
                              NULL,
                              T.EXP_DATE,
                              to_date('2015-07-02 00:00:00',
                                      'yyyy-mm-dd hh24:mi:ss'))
                      ELSE
                       T.EXP_DATE + NUMTODSINTERVAL(5356800, 'SECOND')
                    END
 WHERE T.BAL_ID = 150036472
```

**检查方式**：人工检查

### 【强制】使用预编译SQL

**说明：**

为实现最佳性能，应预先准备好那些执行不止一次的SQL 语句。

这一准则适用于所有关系数据库；但是对于TimesTen 及其极高的事务处理速度来说，编译一条语句所耗费的时间实际上要比执行该语句所花的时间多好几倍；因此，未预先准备好语句的应用程序将使TimesTen 的性能大打折扣。

除了要预先准备好语句，那些语句的输入参数和输出列也应预先绑定。

- ODBC用户使用SQLPrepare 函数预先准备语句。

- TTClasses用户使用TTCmd::Prepare()方法预先准备语句。

- JDBC用户使用PreparedStatement 类预先准备语句。

**检查方式**：人工检查

### 【强制】使用预编译，在业务结束时必须进行提交或者回滚事务

**说明**：

Timesten的预编译会生成一个事务，如果有预编译，则不论是否是只进行查询，都要**在业务成功或者失败时候进行提交或者回滚**，否则将会导致事务变得非常大，耗尽日志空间、造成大量的锁

**检查方式**：人工检查

### 【推荐】尽量避免使用子查询

**说明：**

TimesTen可以在 SELECT, CREATE VIEW, DELETE 或者 UPDATE 语句的SET或者 WHERE子句中使用子查询，如以下格式：

```sql
[NOT] EXISTS | [NOT] IN (Subquery) 

Expression {= | <> | > | >= | < | <= } [ANY | ALL] (Subquery) 

Expression [NOT] IN (ValueList | Subquery) 
```

但是子查询一般不是性能最佳的SQL写法，尽量避免子查询的写法。

**检查方式**：人工检查

### 【强制】取序列时需要及时提交，否则会导致长事务问题

**说明：**

TimesTen中取序列时，需要及时commit提交，否则会有长事务，导致问题。

**检查方式**：人工检查

**参考故障单号**：ZMP\931679

## 最佳实践

### 【推荐】选择合适的索引类型

**说明：**

TimesTen的索引有T-TREE INDEX，HASH INDEX和B-TREE INDEX。

- T-TREE INDEX可以用在等值查询、范围查询、ORDER BY、DISTINCT等场合。

- HASH INDEX只能用于精确查询，不能用于范围、分类查询。但是哈希索引要比T-TREE INDEX快，所以尽量能使用HASH INDEX。当 T-TREE INDEX、HASH INDEX都同时可用时候，TimesTen会优先选择使用 T-TREE INDEX。

- B-TREE INDEX可以用于任何场景（TimesTen 11.2.2.5版本开始引入）。

*Note：*
*TimesTen 18版本前，建立主键时候缺省建立的是HASH INDEX。*
*从TimesTen 11.2.2.5版本开始引入B-TREE-INDEX，Oracle建议所有场景都用B-TREE-INDEX，默认索引还是HASH INDEX。*
*从TimesTen 18版本开始，默认索引都是B-TREE INDEX。*
*建议TimesTen 18版本开始，推荐业务上使用的索引都是B-TREE INDEX。*

**检查方式**：人工检查

### 【强制】一个N列的组合T-TREE INDEX或者B-TREE INDEX，需要使用此索引必须在WHERE条件中包含此索引前导列。

**<font color=red>反例</font>**

```sql
SELECT COL1，COL2
  FROM A
 WHERE COL1 = ?
   AND COL2 = ?
```

*Note：表A上的T树索引：(COL3, COL2, COL1)，该语句将无法使用T树索引。*

**正例**

```sql
SELECT COL1，COL2
  FROM A
 WHERE COL3 = ?
   AND COL2 = ?
```

*Note：表A上的T树索引：(COL3, COL2, COL1)，该语句可使用T树索引。*

**检查方式**：人工检查

**参考故障单**：ZMP2686429

### 如何才能使用上HASH INDEX

**说明：**

一个哈希N列索引只能被用于N列全部精确匹配的查询。

**<font color=red>反例</font>**

```sql
SELECT COL1, COL2
  FROM A
 WHERE COL1 = ?
   AND COL2 = ?
```

*Note：表A上的哈希索引：(COL1, COL2, COL3)，该语句将无法使用哈希索引*

**正例**

```sql
SELECT COL1, COL2
  FROM A
 WHERE COL1 = ?
   AND COL2 = ?
   AND COL3 = ?
```

*Note：表A上的哈希索引：(COL1, COL2, COL3)，语句可使用哈希索引。*

**检查方式**：人工检查

### 【推荐】使用索引时候应注意避免在索引字段上使用表达式

**<font color=red>反例</font>**

```sql
WHERE c1+10 = c2+20
```

*Note：c1列上有索引，该语句无法索引。*

**正例**

```sql
WHERE c1 = c2+10
```

*Note：c1列上有索引，该语句可使用索引。*

**检查方式**：人工检查

### 如何查看执行计划

**说明：**

在TimesTen中，可以查询一个某SQL的执行计划，以便确认是否使用了索引、是否是最优的执行路径。

查询执行计划，需要在执行SQL之前执行以下两个SQL：

```sql
Command>autocommit 0; 

Command>showplan 1;
```

**正例**

```sql
Command> autocommit 0;
Command> showplan 1;
Command> select * from bal;
Query Optimizer Plan:
  STEP:        1
  LEVEL:       1
  OPERATION:   RowLkSerialScan     注：全表扫描
  TBLNAME:     BAL
  IXNAME:      <NULL>
  PRED:        <NULL>
  OTHERPRED:   <NULL>
0 rows found.

Command> select * from bal where bal_id=222;
Query Optimizer Plan:
  STEP:        1
  LEVEL:       1
  OPERATION:   RowLkHashScan     注：使用了HASH 索引
  TBLNAME:     BAL
  IXNAME:      BAL
  PRED:        BAL.BAL_ID = 222
  OTHERPRED:   <NULL>
0 rows found.

Command>
```

**检查方式**：人工检查

### 【推荐】建议不要使用过多的连接

**说明：**

成倍的提供到TimesTen 的连接并不一定能成倍地提供性能，过多的连接反而会造成过多的lock 或者 latch level 而损害性能。所以**连接池大小一般只能是 N × 逻辑CPU个数，N值不超过2**，应用程序要尽可能地复用这个有限的连接池。

查看连接个数的命令：

```
cmd> ttXactAdmin -connections <DSN> 

5 532548 0x0000000110038c90 Ztesoft.CSIP ttcserver Run 5.723821 OCS
```

**检查方式**：人工检查

### 【推荐】及时关闭游标

**说明：**

下面是关闭SQL 游标的方法：

```java
[ODBC] SQLFreeStmt(SQL_CLOSE) 

[TTClasses] TTCmd::Close() 

[JDBC] PreparedStatement.close() 
```

*Note： ZSmart V6\\V7\\V8系列Java技术框架会自动进行关闭，一般无需业务代码显式关闭*

**检查方式**：人工检查

### 【建议】大量数据操作时建议使用分批操作

**说明：**

同 Oracle 类似，如果一次性插入、更新、删除大量数据时候，要使用分批操作，避免大量数据最后提交，容易造成lock和挤占回滚段。

比如在JDBC中，批量操作是 PrepareStatement 的 addBatch , executeBatch 接口。

**检查方式**：人工检查

### 【建议】在TimesTen内存数据中尽量避免执行大规模批量操作和全表扫描

**说明：**

TimesTen是一款基于内存的高性能数据库，主要适用于低延迟、高并发的小型交易操作（如读取、插入、少量更新）。全表扫描或大规模批量操作（如大批量插入或更新）涉及大范围的内存数据遍历和主机资源消耗，会显著增加CPU、内存和I/O负载，最终可能影响数据库的正常事务性能及其实时性优势。

对于批量或复杂的处理任务，可以考虑将数据导出到Oracle中，Oracle等磁盘数据库更擅长此类长耗时的计算任务，并且能更好利用资源完成批量操作。

**检查方式**：人工检查

> **规范来源**：严重生产故障3782625

# 附录

## 参考文档

1. ZSmart国际业务运营中心BSS产品线 - SQL编程规范 - TimesTen分册.doc

# 本文件评审、修正记录

| 文件名称 | SQL开发规范 – MySQL分册                                      |                 |               |        |
| -------- | ------------------------------------------------------------ | --------------- | ------------- | ------ |
| 序号     | 流程                                                         | 拟制人/审核人   | 拟制/审核时间 | 版本号 |
| 1        | 拟制                                                         | 张金华          | 2015/05/04    | V0.1   |
| 2        | 定稿                                                         | SQL编程规范小组 | 2015/05/06    | V0.2   |
| 3        | 基于张金华的版本，按现有模板要求做了调整                     | 崔丽莉          | 2020/12/07    | V0.3   |
| 4        | 基于数据库核心组评审意见修改                                 | 崔丽莉          | 2020/12/11    | V0.4   |
| 5        | 基于数据库核心组评审意见修改                                 | 崔丽莉          | 2020/12/14    | V0.5   |
| 6        | 基于数据库规范组评审意见修改                                 | 崔丽莉          | 2020/12/18    | V0.6   |
| 7        | 章节2.8增加参考的故障单号                                    | 崔丽莉          | 2021/01/11    | V0.7   |
| 8        | 章节3.2.1增加说明信息                                        | 崔丽莉          | 2021/02/1     | V0.8   |
| 9        | 根据核心组审核意见补充和修改部分条目                         | 崔丽莉          | 2021/02/27    | V0.9   |
| 10       | 标准化                                                       | 数据库规范组    | 2021/04/20    | V1.0   |
| 11       | 修正2.2.1章节正例例2中的错误                                 | 崔丽莉          | 2021/05/28    | V1.0.1 |
| 12       | 发布                                                         | 数据库规范组    | 2021/05/30    | V1.1   |
| 13       | 1. 章节1.3角色和职责，去掉运维人员适用的内容；<br/>2.章节2.3.2由推荐修改为强制，并修改规范定义，即[强制] 一个N列的组合T-TREE INDEX或者B-TREE INDEX，需要使用此索引必须在WHERE条件中包含此索引前导列；增加故障参考单信息； | 崔丽莉          | 2021/12/27    | V1.1.1 |
| 14       | 发布                                                         | 数据库规范组    | 2021/12/30    | V1.2   |
| 15       | 增加2.3.9章节 【建议】在TimesTen内存数据中尽量避免执行大规模批量操作和全表扫描   | 崔丽莉    | 2025/01/02    | V1.2.1   |
| 16       | 发布                                                         | 数据库规范组    | 2025/01/20    | V1.3   |
| 17       | 1. 各规范条款增加检查方式。 <br/>2. 章节2.3.9增加规范来源信息（规范来源：严重生产故障3782625）  | 崔丽莉    | 2025/03/01    | V1.3.1   |
| 18       | 发布                                                         | 数据库规范组    | 2025/03/24    | V1.4   |

