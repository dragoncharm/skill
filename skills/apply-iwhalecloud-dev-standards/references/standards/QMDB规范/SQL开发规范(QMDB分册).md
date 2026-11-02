![image](uploads/4070/fa9185c0-1c05-4221-aeac-9ec84598eb0f/PG_dev_QMDB.png)

# 概述

## 编写目的

- 避免低效SQL导致的性能问题。

- 避免执行SQL和获取结果时产生不必要的异常。

## 适用范围

- 在C/C++、Java等各种编程语言中编写SQL语句 访问QMDB V1.2，需要遵循此规范。

- 对于访问QMDB V9的应用需要额外遵守第 5 章。

- 所有的规则条款都采用人工检查方式。

## 角色和职责

- 开发：负责按照SQL规范进行SQL编码

# SQL要求

## 【强制】SQL长度不可超过 8192 字节。

**说明：**

QMDB V1.2支持的SQL最大长度为 65535 字节，QMDB V9中支持的SQL最大长度为 8192 字节。

QMDB V1.2和QMDB V9版本的SQL长度限制不同，为了保证应用程序从QMDBV1.2平滑迁移到QMDB V9，应用程序中的SQL长度最好不要超过 8192 字节。

**检查方式**：人工检查

## 【强制】UPDATE不可更新主键。

**说明：**

当对主键字段进行更新时，接口会报错。

尤其需要注意，对于多个字段复合主键的情况，更新其中任意字段都会报错。

**检查方式**：人工检查

## 【强制】QMDB SQL语法支持与限制如下, 不要使用别的语法

**说明：**

不支持：多表关联以及嵌套查询

支持：INSERT, DELETE, UPDATE, SELECT

支持：ORDER BY, GROUP BY, HAVING, ASC, DESC

支持的函数/关键字包括：IN, COUNT, SYSDATE, MAX, MIN, TO_DATE, TO_CHAR, SUM, NVL, BLOBTOCHAR, ADD_SECONDS, NEXTVAL, CURRVAL, MOD

虽然支持ORDER BY、GROUP BY操作，但是在QMDB V1.2中尽量避免使用，在QMDB V9中禁止使用(参看章节5.14)。

**检查方式**：人工检查

## 【强制】禁止远程执行慢SQL

**说明：**

远程执行包含Java访问、 C++ CS模式访问。慢SQL是指没有走索引的SQL。

**检查方式**：人工检查

## 【强制】不需要的链接，不要去连QMDB

**说明：**

无效链接会导致QMDB的资源浪费，在满足业务需求的情况下，尽量少的连接。

**检查方式**：人工检查

## 【强制】远程访问中，同一个链接的同一个SQL，禁止多次setSQL。

**说明：**

复用相同SQL的句柄。如果多次重复创建Query句柄，会导致句柄数不断增加，内存占用也会越来越高，最终导致系统奔溃。

**检查方式**：人工检查

## 【强制】INSERT、DELETE、UPDATE执行后，要尽快COMMIT或者ROLLBACK，禁止一直都不进行提交、回滚操作。SELECT不需要执行COMMIT、ROLLBACK。

**说明：**

在开启表的回滚的模式下，一直不提交会导致回滚段写爆，从而无法执行新的操作。

无论是否开启了回滚，开发都要养成及时提交的好习惯。

**检查方式**：人工检查

#  性能优化

## 【强制】程序中尽量使用带绑定变量的SQL

**说明：**

SQL尽量采用绑定变量的方式，否则会导致频繁的解析SQL，影响数据库的性能。

**检查方式**：人工检查

## 【强制】在程序代码内部禁止使用“SELECT *”这样的语句

**说明：**

当需要查询表中的所有列时，也需列出所有的字段名。非程序代码访问不受此限制约束。

**检查方式**：人工检查

## 【推荐】尽量减少使用ORDER BY 和GROUP BY排序操作

**说明：**

QMDB支持分组和排序功能，但是大数据量的分组排序操作影响系统性能，尤其是在远程访问的时候，可能会阻塞别的SQL。

**检查方式**：人工检查

## 【推荐】程序内部尽量不要执行返回大量结果集的SQL

**说明：**

程序访问内存库的SQL应当能够通过索引精准定位到少量结果集，否则将违背内存库高效的本意。

**检查方式**：人工检查

##  索引的使用

### 【推荐】对于需要做范围查找的字段，不推荐创建索引，因为QMDB只支持HASH索引，只能做等值匹配。如果仅仅想要做范围查找，建索引无法起到作用，反而会浪费内存空间和性能。

**说明：**

HASH索引只能够做等值匹配，可以适配 = 和 IN 函数 ， 无法适配大于号小于号。

**检查方式**：人工检查

###  【推荐】关注索引匹配的优先级

**说明：**

与Oracle的索引机制不同，对于一个WHERE条件有多个字段的，会匹配列完全一致的索引。 如果没有相应的完全匹配复合索引，则匹配‘列数匹配最多’的索引。

**检查方式**：人工检查

**正例1**

```sql
表TEST有 A B C 3个字段。
分别建有 IDX_ABC(A、B、C的复合索引)，IDX_AB（A、B的复合索引），IDX_A(A
的单列索引)

select ID,NAME from TEST where A=1 and B=1 and C=1 
会使用 IDX_ABC 作为索引。
但是如果把IDX_ABC 索引删掉，则该SQL会使用IDX_AB 作为索引。
```

**正例2**

```sql
表TEST有 A B C 3个字段。
分别建有 IDX_A (A字段上的索引)，IDX_B（B字段的索引），IDX_C(C字段的索引)。
并且配置文件中索引的顺序就是IDX_A、IDX_B、IDX_C

select ID,NAME from TEST where C=1 and A=1 and B=1
QMDB V1.2：只会使用 IDX_A 作为索引，按照配置文件的顺序。
QMDB V9：会使用IDX_C作为索引，会按照WHERE条件的顺序。
```

## 【推荐】尽量减少跨主机访问的次数

**说明：**

远程访问的性能比本机访问的性能差很多，主要是指QMDB V1.2。因为QMDB V9 主要是远程访问。

**检查方式**：人工检查

## 【建议】尽量不要在QMDB执行批量操作

**说明：**

如果在主机资源压力大的时段，对内存库进行全表扫描操作，可能导致内存库性能下降。可以考虑将数据导出到Oracle中，在Oracle中做大批量数据的处理工作。

**检查方式**：人工检查

> **规范来源**：严重生产故障3782625（本单为TimesTen故障，但QMDB库也需要关注和规避）

#  C++接口使用规范

## 【强制】禁止多线程并发使用同一个TMdbClientDatabase 或者 TMdbDatabase链接。

**说明：**

TMdbClientDatabase类和TMdbDatabase类 自身不是线程安全的，并发使用会产生不确定现象。多线程环境下每个线程需要有独立的连接对象，不可多线程共用连接。

如果出现跨线程的这种用法，会在$QuickMDB_HOME/log/<业务进程名>.log下打出告警信息：
current thread not connect,qmdb not support concurrency on one link

**检查方式**：人工检查

##  【强制】使用GetValue接口时，传入的缓存区大小不得小于QMDB中字段列长。

**说明：**

GetValue接口会把共享内存的数据，按照GetValue传入的列偏移量，拷贝到用户进程的空间，如果空间不够，会产生内存覆盖。

GetValue接口提供长度校验：
(1) 对于字符串（含blob）Struct中给定的长度不能小于qmdb的xml中配置的长度
(2) 对于数值型，长度要为sizeof(long long)
(3) 对于时间类型：
&ensp;​&ensp; 1) 压缩时间（Y）：长度为sizeof(int)
&ensp;​&ensp; 2) 长压缩时间（L）：长度为sizeof(long long)
&ensp;​&ensp; 3) 非压缩（N）：长度不能小于 15

若校验失败，会在$QuickMDB_HOME/log/<业务进程名>.log下打出告警信息：
*RowDataStruct Column[date_1] ColumnLen=[8] but OutLen=[4].* 这种告警信息
**但是最后一个字段的长度空间 GetValue接口无法校验，需要人工去检查**。

对于最后一个字段长度空间无法校验的解释：
void GetValue(void *pStruct,int* Column)，第一个参数待拷贝的目的内存块，第二个参数表示每个列的偏移。因为QMDB内部是根据第 2 个参数传入的列偏移来校验长度空间是否足够。

```cpp
struct my_table_value
{
  Long long A;
  Char B[17];//最后末尾要有个’\ 0 ’
  char C[15];//假设is-zip-time = N
};
my_table_value stValue;
Int arrColumn[3] = {0};
//设定各列的偏移,这边不建议手动设定，考虑字节对齐
arrColumn[0] = 0;
arrColumn[1] = stValue.B- (char *)&(stValue);
arrColumn[2] = stValue.C- (char *)&(stValue);//......
GetValue(&stValue,arrColumn);//调用GetValue接口
```

**检查方式**：人工检查

# V9要求

对于访问QMDB V9 版本的应用，除了要遵守其他章节的要求外，还要遵守本章的要求。

应用访问V9主要是远程访问，QMDB1.2主要是本地直连访问。V9的SQL访问不能直接拷贝QMDB1.2的SQL语句，主要是因为QMDB1.2没有分片字段，用1.2的SQL访问V9可能会导致性能问题，也可能因为表结构的（QMDB1.2对应的V8业务，QMDBV9对应的V9业务，业务表结构也不一样）而发生报错。

##  【强制】禁止使用高冲突索引来查询记录

**说明：**

高冲突索引的索引区分度很低，很多记录的这个字段值（索引所在字段）都一样。

通过这种索引来查询记录，耗时较长，严重情况下可能导致业务中断。如果目前有这种访问方式，需要考虑更改设计方案。

**检查方式**：人工检查

## 【强制】应用每次操作的字节总数不超过64K

**说明：**

QMDB内部的缓冲区大小为 64 K，如果当前发送的字节总数超过 64 K，会报错。如果有报错，可以尝试降低当前一个批量内的操作个数。

**检查方式**：人工检查

## 【强制】SQL、NOSQL操作不允许同时存在于同一个链接上

**说明：**

SQL、NOSQL访问属于完全不同的两种访问方式，不能混合使用。

**检查方式**：人工检查

## 【强制】禁止执行不带where条件的全表更新、删除操作。

**说明：**

执行全表的更新删除操作，属于很危险的操作，会占用大量CPU、内存资源，可能会导致业务中断。

**检查方式**：人工检查

## 【强制】合理控制链接上的Query个数，不要超过 100 。

**说明：**

应用通过具体的Query来执行具体的SQL操作，太多的Query会占用额外的内存资源，可能会导致QMDB 本身内存不足，导致系统异常。如果一个链接上的Query个数超过 100 个，就需要分析是否需要这么多。

**检查方式**：人工检查

## 【强制】访问序列需要使用步长属性，不能频繁获取序列，步长至少是 100 。

**说明：**

应用需要缓存序列的步长，每次都从QMDB来获取序列会严重影响业务性能，序列的步长设置至少是 100 。

**检查方式**：人工检查

## 【推荐】V9的SQL、NOSQL操作条件需要指定分片字段。

**说明：**

V9支持多分组部署，如果没有指定分片字段，就会遍历所有分组。

**检查方式**：人工检查

## 【推荐】查询字段时，只查询需要的字段。

**说明：**

禁止简单的拷贝所有字段，这样会占用额外的CPU、内存资源，也会导致访问性能下降。

**检查方式**：人工检查

## 【推荐】单条记录的大小不要超过20K，否则访问性能可能会下降。

**说明：**

V9主要是远程访问，如果单条记录长度太大，一次需要访问多条记录时，需要经过多次网络交互才能访问完毕，这样会导致性能下降。

建议控制单个表中大varchar字段（长度超过 1000 ）的个数，较多的大varchar字段，不但增加了单条记录的长度，也会带来处理varchar的性能损耗，以及网络访问性能的下降。

**检查方式**：人工检查

## 【强制】SQL长度不可超过 8192 字节。

**说明：**

如果应用设置的SQL长度超过 8192 ，访问会报错。

**检查方式**：人工检查

## 【推荐】关注集群部署与非集群部署的区别。

**说明：**

常用的部署方式是集群部署，应用只能通过远程访问来操作数据。正常情况下，商用环境一般至少有两个管理节点和两个数据节点。但是，一些测试环境，可能只部署了一个管理节点和一个数据节点。

还有一种不常用的部署模式，非集群部署。只部署单机QMDB，没有管理节点。这种模式支持远程访问+本地问。

推荐使用集群方式部署。

**检查方式**：人工检查

## 【强制】IN()参数个数限制为50个

**说明：**

过多的参数会导致性能下降。

**检查方式**：QMDB自检，使用不符合规范的直接报错(QMDB自检功能开发中)

> **规范来源**：严重生产故障3793387

## 【强制】只能使用一个IN条件

**说明：**

过多的IN条件会导致性能下降。

**检查方式**：QMDB自检，使用不符合规范的直接报错(QMDB自检功能开发中)

> **规范来源**：严重生产故障3793387

## 【强制】禁止使用ORDER BY、GROUP BY

**检查方式**：QMDB自检，使用不符合规范的直接报错(QMDB自检功能开发中)

# 附录：C++二次开发指南

## 文件引用

1. 对qmdb进行二次开发只需要包含头文件 #include "Interface/mdbQuery.h"

2. 对qmdb进行二次开发需要链接四个库，分别是mdbHelper mdbInterface mdbControl mdbCommon

##  数据库链接

QuickMDB 的数据库类也分为直链模式和 CS 模式两种。

### 直连模式是指直接以嵌入的方式访问共享内存数据

直链模式的数据库链接方式如下：

```cpp
TMdbDatabase mdb;
mdb.SetLogin("user", "password", "dsn");
if(mdb.Connect() == false)
{
  printf("Can't connect to QuickMDB.");
  return 0;
}

首先要创建一个直链数据库的对象：TMdbDatabase mdb;

然后设置访问数据库的用户名密码以及对应的实例名称：
mdb.SetLogin("user", "password", "dsn");

最后链接数据库，如果成功返回 true，失败返回 false：mdb.Connect()。
```

### 远程模式是指以远程网络的方式访问数据库

CS 模式的数据库链接方式如下：

```cpp
TMdbClientDatabase *pDataBase = new TMdbClientDatabase();
pDataBase->SetServer("127.0.0.1",8902);
pDataBase->SetLogin("user","pasword","dsn");
bool bIsConnect = pDataBase->Connect();
{
  printf("Can't connect to QuickMDB.");
  return 0;
}

首先要创建一个直链数据库的对象：
TMdbClientDatabase *pDataBase = new TMdbClientDatabase();

然后设置服务器的 IP 和端口：
pDataBase->SetServer("127.0.0.1", 8902);

然后设置访问数据库的用户名密码以及对应的实例名称：
pDataBase->SetLogin("user","pasword","dsn");

最后链接数据库，如果成功返回 true，失败返回 false：pDataBase->Connect()。
无论是直链模式，还是 CS 模式，提交的接口都是 Commit()，回滚的接口都是 Rollback()。
```

##  SQL执行

SQL执行有两种模式，静态SQL模式和动态SQL模式。 静态SQL没有绑定变量，动态SQL有绑定变量。

下面举一个采用静态 SQL 的例子：

```cpp
首先创建一个新的访问句柄：

TMdbClientQuery *m_pQuery = new TMdbClientQuery（pDataBase）;
这里创建句柄，还可以采用如下方式：
TMdbClientQuery *m_pQuery = pDataBase->CreateDBQuery();

然后进行清理，初始化：m_pQuery->CloseSQL();

接下来设置需要访问的 SQL：
m_pQuery->SetSQL("select count(*) from Kernel_T");

对于查询语句，需要通过 Open 函数打开游标，取出数据：m_pQuery->Open();

最后把数据遍历读取出来，供字段访问使用：
while(m_pQuery->Next())
{
   iRecCounts = m_pQuery->Field("count(*)").AsInteger();
}
```

下面举一个采用动态 SQL 的例子：

```cpp
TMdbClientQuery *m_pQuery = new TMdbClientQuery（pDataBase）;
if(m_pQuery == NULL)
{
  printf("Can't CreateDBQuery.");
}

m_pQuery->CloseSQL();
m_pQuery->SetSQL("select value from Kernel_T where id=:id");
这个 SQL 中带有动态参数:id，每一个动态参数都以冒号作为标识。

for(int i=0; i<1000; ++i)
{
  设置好动态参数的值：
  m_pQuery->SetParameter(“id”, i);
  m_pQuery->Open();
  int iRecCounts = 0;
  while(m_pQuery->Next())
  {
    获取字段的值
    iRecCounts = m_pQuery->Field("value").AsInteger();
  }
}
```

## 字段访问

### Field 接口

```cpp
m_pQuery->Field("value").AsInteger();
```

Field 函数得到的就是一个字段的值，可以通过 AsInteger()得到对应的整数， 通过 AsString() 得到对应的字符串。

对于日起类型，通过 AsString()得到 YYYYMMDDHHMMSS 格式的字符串，也可以通过AsDateTime()获取各个部件的值。

对于 BLOB 类型，则通过 AsBlobBuffer()获取对应的数据。

### GetValue接口

为了提高查询性能，提供GetValue获取整条记录的值，直接将QMDB的内存值拷贝出来，省去SQL计算的耗时。对此接口的使用有以下注意事项：

（ 1 ）无论SELECT 中的列段如何写，GetValue都会获取该表的所有列的值，并按QMDB中的列定义顺序拷贝出来。

比如有表my_table，有列A,B,C。那么对于SQL:select A from my_table; GetValue出来的是A,B,C值。

（ 2 ）GetValue(void *pStruct,int* Column)，第一个参数待拷贝的目的内存块，第二个参数表示每个列的偏移。
比如表my_table定义如下

| 列名 | 参数类型  | 字段大小（单位：字节）                                       |
| ---- | --------- | ------------------------------------------------------------ |
| A    | number    | 8                                                            |
| B    | char(16)  | 16                                                           |
| C    | datestamp | 参考表结构属性[is-zip-time]配置<br/>若为Y：则size=4(时间戳，int存储)<br/>若为L：则size=8（时间戳，long long存储）<br/>若为N：则size=14（时间字符串，比如” 20140122110100 ”） |

*注：对于QMDB保存字符串类型，会对数据存放的长度会自动+1，所以在xml中配置的字符串的len长度为实际数据长度，无需考虑结尾符的长度。*

```cpp
Struct my_table_value
{
  Long long A;
  Char B[17];//最后末尾要有个’\ 0 ’
  char C[15];//假设is-zip-time = N
};

my_table_value stValue;
Int arrColumn[3] = {0};
//设定各列的偏移,这边不建议手动设定，考虑字节对齐
arrColumn[0] = 0;
arrColumn[1] = stValue.B- (char *)&(stValue);
arrColumn[2] = stValue.C- (char *)&(stValue);//......

while(m_pQuery->Next())
{
  m_pQuery->GetValue(&stValue,arrColumn);//调用GetValue接口
}
```

**GetValue提供类型长度校验:**
(1) 对于字符串（含blob）Struct中给定的长度不能小于qmdb的xml中配置的长度
(2) 对于数值型，长度要为sizeof(long long)
(3) 对于时间类型：
&ensp;​&ensp; 1) 压缩时间（Y）：长度为sizeof(int)
&ensp;​&ensp; 2) 长压缩时间（L）：长度为sizeof(long long)
&ensp;​&ensp; 3) 非压缩（N）：长度不能小于 15

**不得出现校验失败的情况**
若校验失败，会在$QuickMDB_HOME/log/<业务进程名>.log下打出告警信息：
*RowDataStruct Column[date_1] ColumnLen=[8] but OutLen=[4].*这种告警信息

# 本文件评审、修正记录

| 文件名称 | SQL开发规范 – QMDB分册                                       |               |               |        |
| -------- | ------------------------------------------------------------ | ------------- | ------------- | ------ |
| 序号     | 流程                                                         | 拟制人/审核人 | 拟制/审核时间 | 版本号 |
| 1        | 编写                                                         | 俞连祥/李书刚 | 2020/01/16    | V0.1   |
| 2        | 添加第5章节QMDB V9的要求                                     | 王列豹        | 2021/08/27    | V0.2   |
| 3        | 1. 更新2.1章节SQL长度天正为8192；<br/>2. 更新2.3章节，调整为支持的函数/关键字；<br/>3. 新增5.10章节 明确QMDB V9中SQL长度要求； | 王列豹        | 2021/10/15    | V0.3   |
| 4        | 增加5.11<br/>V9关注集群部署与非集群部署的区别。              | 王列豹        | 2021/11/8     | V0.4   |
| 5        | 5 V9要求中，增加了对V9的SQL访问不能直接拷贝QMDB1.2的SQL语句的说明。 | 王列豹        | 2021/11/19    | V0.5   |
| 6        | 修改1.3角色和职责，只适用开发人员；修改4.2文字描述，使用GetValue接口时，传入的缓存区大小不得小于QMDB中字段列长；修改附录6.4 \0改为结尾符 | 王列豹        | 2021/11/22    | V0.6   |
| 7        | 首次发布 | 数据库规范组        | 2022/10/28    | V1.0   |
| 8        | 新增3.7章节 【建议】尽量不要在QMDB执行批量操作（规范来源：严重生产故障3782625） | 崔丽莉        | 2024/12/03    | V1.0.1   |
| 9        | 发布 | 数据库规范组        | 2024/12/17    | V1.1   |
| 10        | 1. 各规范条款中增加检查方式。 <br/>2. 完善3.7章节中规范来源信息（规范来源：严重生产故障3782625（本单为TimesTen故障，但QMDB库也需要关注和规避））| 崔丽莉        | 2025/3/1    | V1.1.1   |
| 11        | 发布 | 数据库规范组        | 2025/3/24    | V1.2   |
| 12        | 修改章节“2.3. 【强制】QMDB SQL语法支持与限制如下, 不要使用别的语法”，对说明信息“虽然支持ORDER BY、GROUP BY操作，但是尽量避免使用”进行补充完善。修改后说明：虽然支持ORDER BY、GROUP BY操作，但是在QMDB V1.2中尽量避免使用，在QMDB V9中禁止使用(参看章节5.14)<br>新增章节“5.12. 【强制】IN()参数个数限制为50个”（规范来源：严重生产故障3793387）<br>新增章节“5.13. 【强制】只能使用一个IN条件”（规范来源：严重生产故障3793387）<br>新增章节“5.14. 【强制】禁止使用ORDER BY、GROUP BY”   | 崔丽莉        | 2026/02/04    | V1.2.1   |
| 13        | 发布 | 数据库规范组        | 2026/3/23    | V1.3   |

