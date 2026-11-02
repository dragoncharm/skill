![image](uploads/4068/b34f8787-8345-4be8-82a8-0342a3326e8f/PG_OPE_TT.png)

# 编写目的

本文用于指导浩鲸科技运维人员进行数据库运维工作(TimesTen部分)。

# 适用范围

浩鲸科技所有使用Oracle内存数据库 TimesTen 11.X，18.X 的项目。

# 角色和职责

运维人员：参考文档对项目数据库进行运维；

DBA : 负责运维文档的更新并对运维人员进行技术指导。

# 公司TimesTen相关规范

检查方式： 本章节内容中2.5长事务条款由网管负责监控，告警需干系人员及时处理，其他条款均人工检查。

1、【国际】工程实施行为规范-第六条：【强制】内存数据库（TimesTen，Altibase，QMDB等）操作必须使用公司统一发布的DBTool工具，禁止用命令方式直接操作内存数据库，特殊情况除外。

2、【集成】内存数据库操作规范：

第一条：【强制】一次性大批量删除生产表数据时，生成批量删除文件，文件中的删除脚本以主键字段为删除条件做单条删除。

第二条：【强制】对于TimesTen，/tt/DS目录下所有文件，不允许擅自手动删除和修改。

第三条：【强制】在线重建sequence，要重启相关应用程序。

第四条：【强制】对于TimesTen，不允许使用ttbulkcp在线备份相关表，会导致锁表。

第五条：【推荐】对于TimesTen，要定期检查TT长事务，发现以后要尽快处理。

第六条：【强制】若主机异常断电或异常重启，必须要确保TT复制器正常工作。

第七条：【强制】内存数据库（TimesTen，QMDB，Altibase等）数据的修改等只能在主机上执行。

第八条：【强制】禁止私自修改操作系统内核参数。

3、【国际】十大高压线-第七条：【强制】TT数据是关键，不可直连来操作。

4、【集成】除了以上规范，集成侧新增如下操作规范：

（1）【强制】禁止人为删除TimesTen事务同步日志（DSN.log\*）和checkpoint文件DSN.ds\*。

（2）【强制】禁止私自修改TT配置文件：sys.odbc.ini、sys.ttconnect.ini、ttendaemon.options等。

（3）【强制】业务高峰期禁止批量清理数据，特殊情况除外。

（4）【强制】白天禁止切换TT双机，特殊情况除外。

（5）【强制】禁止在备机或者DR操作数据修改，引发TT双向复制。

（6）【强制】删除数据操作必须在在用节点进行，避免双向复制。

（7）【推荐】在规划表字段类型时，尽量不要使用OUT-OF-LINE字段。

# TimesTen日常维护场景

【说明】相关参考文件，请参考此链接下载。

[数据库运维规范-TimesTen分册参考文献](https://docs.iwhalecloud.com/dmz-proxy/cos/download/406/规范附件/数据库/TimesTen_Operation__Reference.zip)

## 表维护

### 增加新表并添加到复制器中

- **规范：**

【强制】Datastore中增加新表，初始创建时必须为空表，主备机须同时创建该表定义，由于新增的表默认不参加复制，必须修改复制器定义将新增的表加入复制以后，才可以进行数据插入。

检查方式：人工检查

- **操作流程：**

1、停止复制器，要求主备机都要执行。

2、建新表，要求主备机都要执行，示例：

```sql
tt@pr-ocs11[/tt]$ ttisql ocs

command> create table OCS.ACCT_ACM (
        ACCT_ID     TT_INTEGER NOT NULL,
        RESOURCE_ID TT_INTEGER NOT NULL,
        "VALUE"     TT_BIGINT,
primary key (ACCT_ID, RESOURCE_ID));
```

3、修改复制器定义，要求主备机都要执行。

```sql
tt@pr-ocs11[/tt]$ ttisql ocs
command>alter replication OCS.REP_OCS
alter element E_1
    include table OCS.ACCT_ACM
alter element E_2
    include table OCS.ACCT_ACM;
```

说明：此处的OCS.REP_OCS及E_1，E_2根据现场的具体情况修改，可以用tt用户执行ttschema ocs查看。

4、启动复制器，要求主备机都要执行

5、验证复制的同步情况，确认数据已经同步

6、检查新表的增删改同步情况(在主节点更新数据，手工测试同步情况)

7、根据TimesTen双机切换章节，切换双机，使业务用上新增的表；

### 在复制器中取消表复制，并删除表

说明：一般业务上无删表场景，删除时需要确保业务不访问此表，需要联系R&D验证通过。

- **规范：**

【强制】Datastore删除表需要先修改复制器定义，将该表从复制中排除，然后再删除该表，否则会再删除的时候会提示报错，导致该表无法删除。

检查方式：人工检查

- **操作流程：**

1、停止复制器，要求主备机都要执行

2、修改复制器定义，要求主备机都要执行

```sql
tt@pr-ocs11[/tt]$ ttisql ocs
command>alter replication OCS.REP_OCS
alter element E_1
     exclude table OCS.ACCT_ACM
alter element E_2
     exclude table OCS.ACCT_ACM;
```

说明：此处的OCS.REP_OCS及E_1，E_2根据现场的具体情况修改，可以用tt用户执行ttschema ocs查看。

3、删表，要求主备机都要执行

```sql
tt@pr-ocs11[/tt]$ ttisql ocs
command> drop table OCS.ACCT_ACM;
```

4、启动复制器，要求主备机都要执行

5、验证复制的同步情况

## 表碎片整理

说明：TimesTen碎片说明参见《TimesTen 碎片分析及说明v1.0（20191023）.txt》

- **规范：**

【推荐】部分大表使用了OUT-OF-LINE列，同时这类表频繁的插入和删除数据，这类表每天的数据插入和删除量比较大，导致内存碎片发生在具有OUT-OF-LINE列的数据存储上，特别是具有大型DML活动的数据存储上，表中的碎片率非常的高，如果不做处理，查询效率会越来越低，会引起待处理数据积压等故障。推荐每半年或一年进行一次表碎片整理。

说明：对于Inline和Out-of-line碎片的估算方式是不同的，Inline有固定的计算公式，而Out-of-line没有公式计算。Oracle专家建议每半年或者一年做一次表碎片整理。后续集成巡检新增TimesTen碎片特殊巡检。

- **操作流程：**

一、离线碎片整理流程为：

1、停止业务；

2、注释主备机相关crontab等定时任务

3、主机确认没有链接；

4、主机stopserver

5、主备机停止复制器；

6、主机全库备份ttbackup；

7、主机执行call ttckpt三次；

8、主备机备份ttSchema信息

9、主机ttmigrate -c导出；

10、主机清理现有DS；

11、主机ttmigrate -r导入，如果需要整理table partitions，加-relaxedupgrade导入；

12、主机检查数据和用户权限；

13、检查分区是否整理，检查碎片是否整理；

14、清理备机和DR节点DS；

15、主机启动复制器；

16、主机startserver

17、主机检查hugepage使用情况

18、主机启动业务测试；

19、拷贝DS到备机及DR；

20、备机检查数据和用户权限；

21、备机及DR检查hugepage使用情况

22、修改备机及DR的sequence；

23、启动备机复制器；

24、修改DR的复制器路由，如果定义了路由的话；

25、启动DR复制器；

26、验证同步情况；

27、检查TT复制器状态、TT日志、TT复制器策略、TT RAM策略；

28、调整各节点检查点时间，时检查点错开；

29、恢复crontab，考虑补跑任务；

二、在线碎片整理流程为：

1、停止备机业务；

2、注释备机相关crontab等定时任务

3、确认备机没有链接；

4、备机stopserver

5、主备机停止复制器；

6、全库备份ttbackup；

7、备机call ttckpt三次；

8、主备机备份ttSchema信息

9、备机ttmigrate -c 导出；

10、备机清理现有DS；

11、备机ttmigrate -r -relaxedUpgrade导入，如果需要整理table partitions，

加-relaxedupgrade导入；

12、备机检查数据和用户权限；

13、备机检查分区是否整理，检查碎片是否整理；

14、备机startserver

15、备机检查hugepage使用情况

16、主备机启动复制器；

17、验证同步情况；

18、检查备机TT复制器状态、TT日志、TT复制器策略、TT RAM策略；

19、数据同步后，切机，重复步骤操作整理主机碎片；

20、如果现场要求业务必须在主机运行，在数据同步后，按TT切机规范流程，把HA切回主机；

21、调整各节点检查点时间，时检查点错开；

22、恢复crontab，考虑补跑任务；

## 字段维护

### 增加字段

- **规范**：

【强制】增加字段的操作原则上可在线操作，但是如果涉及到业务配置更改，需要停业务的，请先停业务再进行操作；操作时只需在主机操作，复制器会自动将新增字段的操作同步至备机。

检查方式：人工检查

官方语法说明：

**To add one column：**

```sql
ALTER TABLE [Owner.]TableName
	ADD [COLUMN] ColumnName ColumnDataType
    [DEFAULT DefaultVal] [[NOT] INLINE] [UNIQUE] [NULL]
    [COMPRESS (CompressColumns [,...])]
```

**To add multiple columns：**

```sql
ALTER TABLE [Owner.]TableName
    ADD (ColumnName ColumnDataType
    [DEFAULT DefaultVal] [[NOT] INLINE] [UNIQUE] [NULL] [,... ] )
    [COMPRESS (CompressColumns [,...])]
```

**To add a NOT NULL column (note that the DEFAULT clause is required)：**

```sql
ALTER TABLE [Owner.]TableName
    ADD [COLUMN] ColumnName ColumnDataType
    NOT NULL [ENABLE] DEFAULT DefaultVal [[NOT] INLINE] [UNIQUE]
    [COMPRESS (CompressColumns [,...])]
```

**To add multiple NOT NULL columns (note that the DEFAULT clause is required)：**

```sql
ALTER TABLE [Owner.]TableName
    ADD (ColumnName ColumnDataType
    NOT NULL [ENABLE] DEFAULT DefaultVal [[NOT] INLINE] [UNIQUE] [,...])
    [COMPRESS (CompressColumns [,...])]
```

- **操作流程：**

1、主机新增字段；

2、主机检查新增的字段及表定义；

3、备机检查新增的字段及表定义，验证是否同步；

4、根据TimesTen双机切换章节，切换双机，使业务用上新增的字段；

### 删除字段

说明：一般业务上无此操作，需要联系R&D验证通过。

- **规范：**

【强制】删除字段的操作原则上可在线操作，但是如果涉及到业务配置更改，需要停业务的，请先停业务再进行操作；操作时只需在主机操作，复制器会自动将删除字段的操作同步至备机。

检查方式：人工检查

官方语法说明：

**To remove columns：**

```sql
ALTER TABLE [Owner.]TableName
DROP {[COLUMN] ColumnName | (ColumnName [,... ] )}
```

*Note: If removing columns in a compressed column group, allcolumns in the compressed column group must be specified.*

- **操作流程：**

1、主机查看表定义；

2、主机删除表字段；

3、主机验证表字段是否删除；

4、备机验证表字段删除操作是否成功；

### 修改字段

说明：TimesTen的字段的类型不可修改，可修改字段的默认值。一般无此操作，需要联系R&D验证通过

#### 更改字段默认值

说明：一般无此操作，影响业务含义，需要联系R&D验证通过。

- **规范：**

【强制】修改字段的默认值操作需要在主备机分别操作，原则上可在线操作，如涉及到其他业务配置变更，业务侧自行决定是否要停业务。

检查方式：人工检查

- **操作流程：**

1、主机查看表定义；

2、备机修改表字段默认值；

3、备机验证表字段默认值；

4、根据TimesTen双机切换章节，切换双机，使业务用上新增的字段默认值；

5、主机修改表字段默认值；

6、主机验证表字段默认值；

说明：字段number修改默认值后，已经存在的数据不会改变，只会在新加行，对该字段不赋值的情况下使用新的默认值。

#### 增加字段的**唯一**约束

- **规范：**

【强制】增加字段的唯一约束操作需要在主备机分别操作，原则上可在线操作，如涉及到其他业务配置变更，业务侧自行决定是否要停业务。

检查方式：人工检查

- **操作流程：**

1、主机增加字段的唯一约束；

2、主机验证表定义；

3、备机增加字段唯一约束；

4、备机验证表定义；

#### 删除字段的唯一约束

- **规范：**

【强制】删除字段的唯一约束操作需要在主备机分别操作，原则上可在线操作，如涉及到其他业务配置变更，业务侧自行决定是否要停业务。

检查方式：人工检查

- **操作流程：**

1、主机删除字段的唯一约束；

2、主机验证表定义；

3、备机删除字段唯一约束；

4、备机验证表定义；

## 索引维护

### 增加索引

#### 增加T-tree索引

- **规范：**

【强制】生产环境新增索引，推荐通过滚动创建索引。避免索引没有生效导致的业务异常或锁表等情况。T-tree索引不参与复制，需要在主备机分别添加。

检查方式：人工检查

官方语法说明：

**To create a range or bitmap index:**

```sql
CREATE [UNIQUE|BITMAP] INDEX [Owner.]IndexName ON
[Owner.]TableName ({ColumnName [ASC | DESC]}
[,... ] )
```

- **操作流程：**

1、在备机创建T-tree索引；

2、备机验证索引；

3、备机创建完成后，切换双机至备机，确认业务运行正常；

4、在主机创建T-tree索引；

5、主机验证索引；

#### 增加Hash索引

- **规范**

【强制】生产环境新增索引，推荐通过滚动创建索引。避免索引没有生效导致的业务异常或锁表等情况。Hash索引不参与复制，需要在主备机分别添加。Hash索引只能出现在主键上，只能用于等值匹配查询，但占用空间较大；建Hash索引时必须定义Pages值（Rows/100）以避免Hash碰撞或不走索引的情况。

检查方式：人工检查

- **操作流程：**

1、在备机创建Hash索引；

2、备机验证索引；

3、备机创建完成后，切换双机至备机，确认业务运行正常；

4、在主机创建Hash索引；

5、主机验证索引；

PS：

（1）TT7创建Hash索引示例如下（该方法也适用于TT11）：

```sql
Command> alter table OCS.ACCT_ACM use hash index pages = 100;
```

（2）从TT11开始新增了可以直接建立哈希索引的命令，但是这个索引是独立于表结构之外的，并且可以建在普通字段上。示例如下：

```sql
Command> create unique hash index acctindex on ocs.acct_acm
(acct_id，resource_id) pages =100;
```

（3）新建立的哈希索引是独立于表结构之外的，且如果不指定pages的大小，会默认设成1，之后并没有办法直接修改，如果想改大小，需要删掉索引重新建立并指定大小。

### 修改索引类型

说明：一般不执行这个操作。

- **规范：**

  对于表结构中的哈希索引可以修改为T-tree索引或者RANGE(B-tree)索引，主备机分别执行。

- **操作流程：**

1、在备机修改索引类型；

2、备机验证索引；

3、备机修改完成后，切换双机至备机，确认业务运行正常；

4、在主机修改索引类型；

5、主机验证索引；

示例如下

**1、改之前表定义：**

```sql
$ ttschema ocs
-- Database is in Oracle type mode
create table OCS.ACCT_ACM (
         ACCT_ID     TT_INTEGER NOT NULL,
         RESOURCE_ID TT_INTEGER NOT NULL,
         "VALUE"     TT_BIGINT,
primary key (ACCT_ID, RESOURCE_ID))，
unique hash on (ACCT_ID, RESOURCE_ID) pages = 50000;
```

**2、修改索引类型**

**TT7.0：**

```sql
Command> alter table OCS.ACCT_ACM use tree index
```

**TT11：**

```sql
Command> alter table OCS.ACCT_ACM use range index;
```

**3、修改后，表定义：**

```sql
$ ttschema ocs
-- Database is in Oracle type mode
create table OCS.ACCT_ACM (
         ACCT_ID     TT_INTEGER NOT NULL,
         RESOURCE_ID TT_INTEGER NOT NULL,
         "VALUE"     TT_BIGINT,
primary key (ACCT_ID, RESOURCE_ID));
```

### 删除索引

Drop index partsorderedindex which is defined on table orderitems using one of the following:

```sql
DROP INDEX partsorderedindex
FROM purchasing.orderitems;
```

Or:

```sql
DROP INDEX purchasing.partsorderedindex;
```

官方语法说明：

```sql
DROP INDEX [Owner.]IndexName [FROM [Owner.]TableName]
```

#### 删除T-tree索引

- **规范：**

【强制】生产环境删除增索引，推荐通过滚动方式删除索引。避免没有索引导致的业务异常情况。删除索引不参与复制，需要在主备机分别添加。

检查方式：人工检查

- **操作流程：**

1、在备机删除T-tree索引；

2、备机验证索引；

3、备机删除完成后，切换双机至备机，确认业务运行正常；

4、在主机删除T-tree索引；

5、主机验证索引；

#### 删除Hash索引

- **规范：**

【强制】生产环境删除增索，推荐通过滚动方式删除索引。避免没有索引导致的业务异常情况。删除索引不参与复制，需要在主备机分别添加。

检查方式：人工检查

- **操作流程：**

1、在备机删除Hash索引；

2、备机验证索引；

3、备机删除完成后，切换双机至备机，确认业务运行正常；

4、在主机删除Hash索引；

5、主机验证索引；

## Pages值维护

官方文档说是可以直接修改，不必停复制器，直接主备机分别修改即可，但是项目上实践的时候我们建议修改时按照以下原则进行：

- 如果现场允许停业务，将主备机所有的ocs应用全部停掉，然后在主备机分别执行；

- 如果不允许停业务，则按照下面流程进行操作：

（1）首先修改ocs备机的tt pages参数；

（2）然后切双机，把主机业务切换到备机；

（3）再修改ocs主机的tt pages参数；

（4）如果有必要可以再把原有主机业务切换回来。

### Pages参数设定原则和空间预估算法

Pages参数设定原则和空间预估算法：

ROWS是表中可能的总记录数，现场需要根据license用户数（项目合同中规定的系统的用户容量）进行估算。ROWS记录数是预估值，不是实际值。比如刚割接了50万用户，但是目标容量是300万，要按预期系统设计的300万容量来设定pages参数值。

估算方法：ROWS=license用户数\*基数

基数：每个用户在表中大概有几条记录。现场可以按照目前系统中各个表已有的数据量和用户数进行一下估算。

比如BAL表目前已有10000条记录，涉及到1000个用户，那么基数就可以估算为10。Pages参数设置，内存空间预估方法：

1、如果以每pages对应100条记录来计算，约每Pages需要4KByte的内存，也就是说现场假设配置一个有记录数的表的pages值为1000，那么设置pages参数做占用的内存空间为1000\*4Kbyte；

2、如果表中为空，则每pages参数需要约240bytes的内存。

也就是说现场假设配置一个无记录的表的pages值为1000，那么设置pages参数做占用的内存空间为1000\*240bytes；

现场计算出每个表设置pages参数所占用内存空间的值之后，把这些值进行汇总；

汇总之后需要跟PERM_ALLOCATED_SIZE-PERM_IN_USE_SIZE的值进行比较，看看已经分配的内存空闲可用空间是否可以满足pages参数设定需要，否则需要考虑扩展TT的PERM_ALLOCATED_SIZE。

**命令参考：**

```sql
Command> dssize;
  PERM_ALLOCATED_SIZE:      8392704
  PERM_IN_USE_SIZE:         3622131
  PERM_IN_USE_HIGH_WATER:   7128352
  TEMP_ALLOCATED_SIZE:      524288
  TEMP_IN_USE_SIZE:         4817
  TEMP_IN_USE_HIGH_WATER:   6397
```

### 表结构中的pages值修改

- **规范：**

【强制】针对hash索引的pagesize需要根据表的最大记录数进行设置，一般为最大记录数/100，需要在创建初期预估好后期的数据量进行设置；

最大记录数估算方法参见：Pages参数设定原则和空间预估算法章节

检查方式：人工检查

- **操作流程：**

1、流程参见pages维护流程描述；

2、修改方法如下:

```sql
tt@pr-ocs11[/tt]$ ttschema ocs
-- Database is in Oracle type mode
create table OCS.ACCT_ACM (
         ACCT_ID     TT_INTEGER NOT NULL,
         RESOURCE_ID TT_INTEGER NOT NULL,
         "VALUE"     TT_BIGINT,
         "NUMBER"    TT_INTEGER DEFAULT 5,
     primary key (ACCT_ID, RESOURCE_ID))
unique hash on (ACCT_ID, RESOURCE_ID) pages = 100;

tt@pr-ocs11[/tt]$

tt@pr-ocs11[/tt]$ ttisql ocs
command>
Command> alter table OCS.ACCT_ACM set pages=200;
```

### 表结构外的pages值修改

- **规范：**

【强制】针对hash索引的pagesize需要根据表的最大记录数进行设置，一般为最大记录数/100，需要在创建初期预估好后期的数据量进行设置。对于独立在表结构之外的hash索引，如果创建的时候不指定pages的大小，会默认设成1，之后并没有办法直接修改，如果想改大小，需要删掉索引重新建立并指定大小。

最大记录数估算方法参见：Pages参数设定原则和空间预估算法章节

检查方式：人工检查

- **操作流程：**

1、该类型索引修改只能走重建流程，滚动重建，具体流程参见索引重建章节流程；

2、修改报错示例如下:

```sql
tt@pr-ocs11[/tt]$ ttschema ocs
-- Database is in Oracle type mode
create table OCS.ACCT_ACM (
         ACCT_ID     TT_INTEGER NOT NULL,
         RESOURCE_ID TT_INTEGER NOT NULL,
         "VALUE"     TT_BIGINT,
     `primary key (ACCT_ID, RESOURCE_ID));

create unique hash index OCS.ACCTINDEX on OCS.ACCT_ACM (ACCT_ID，resource_id)
         pages = 100;

Command> alter table ocs.acct_acm set pages = 100;
 2783: Alter table to set new pages value is valid only if the table has a hash index on the primary key
```

## Sequence维护

### 创建Sequence

- **规范：**

【推荐】项目上sequence不参与复制，双机环境下创建sequence，需要在主备机分别创建，要注意两边startvalue的数值，sequence的步长应至少要等于现场全部OCS主机数量或者单个域(域指每套OCS含PR、DR，比如PR设备OCS11、OCS12，对应DR OCS11 OCS12，那么这个域就指含4个设备PR_OCS11、PR\_OCS12、DR\_OCS11、DR\_OCS12。)的OCS主机数量（需要和业务版本匹配），如果后期计划扩容，推荐将步长扩大。cycle参数是否需要使用，要看具体的业务程序是否支持。若使用，当达到最大值的时候，会从设定的最小值开始计数。若不使用，当到达最大值的时候，会报错。

说明【国际专用V81分布式】：特别是分布式架构，BAL_ID=TFM_ROUTIND.ID_PREFIX+BAL_ID_SEQ，Sequence取值一定要参见《系统集成FAQ_Oracle TimesTen IMDB duplicate后sequence重建配置指导v1.4(20200717).pdf》规划。

官方语法说明：

```sql
CREATE SEQUENCE [Owner.]SequenceName
        [INCREMENT BY IncrementValue]
        [MINVALUE MinimumValue]
        [MAXVALUE MaximumValue]
        [CYCLE]
        [CACHE CacheValue]
        [START WITH StartValue]
```

- **操作流程：**

1、参考《系统集成FAQ_Oracle TimesTen IMDB duplicate后sequence重建配置指导v1.4(20200717).pdf》规划sequence；

2、主备机分别创建相关sequence；

3、主备机验证sequence定义是否符合要求；

4、切换双机至备机，确认业务使用上新增的sequence，及业务运行正常；

### 删除Sequence

- **规范：**

【强制】项目上sequence不参与复制，双机环境下删除sequence，需要依次在备机删除后，切换双机，再删除另外设备的sequence，禁止在业务运行节点删除sequence后重建；

检查方式：人工检查

- **操作流程：**

  1、备机备份sequence定义；

  2、备机删除sequence；

  3、如果需要重建，备机按照sequence重建规则，重建sequence；

  4、重启备机业务程序；

  5、切换业务至备机，验证业务是否正常；

  6、按照备机重建方法，删除（重建）主机sequence；

### 修改Sequence

Sequence不提供修改选项只能通过删除重新创建。

### 获取sequence

**【强制】取序列时需要及时提交，否则会导致长事务问题**

**说明：**

TimesTen中取序列时，需要及时commit提交，否则会有长事务，导致问题。

参考故障单号：931679

检查方式：工具(Dbtool)

## 主键维护

### 增加主键

说明：一般无此场景

- **规范：**

对于建表时没有指定主键的表，可以增加主键，具体是否增加主键，需要根据业务规范要求配置。需要滚动创建。

官方语法说明：

```sql
ALTER TABLE [Owner.]TableName ADD CONSTRAINT ConstraintName
        PRIMARY KEY (ColumnName [,... ])
[USE HASH INDEX PAGES = RowPages | CURRENT]
```

- **操作流程：**

```sql
tt@pr-ocs11[/tt]$ ttschema ocs
-- Database is in Oracle type mode
create table OCS.TEST (
         AA_ID   TT_INTEGER NOT NULL,
         BB_ID   TT_INTEGER NOT NULL,
         "VALUE" TT_BIGINT);

Command> alter table OCS.TEST add constraint TESTCONST primary key (AA_ID);
```

### 删除主键

已有主键无法删除。

## TimesTen Daemon维护

官方语法说明：

Usage:

```shell
ttDaemonAdmin [-h | -help | -?]
  ttDaemonAdmin [-V | -version]
  ttDaemonAdmin [-force] {-start | -stop | -restart}
  ttDaemonAdmin -startserver
  ttDaemonAdmin [-force] -stopserver
  ttDaemonAdmin –verbose
```

### TimesTen Daemon启动

- **规范：**

【强制】现场生产环境，在sys.odbc.ini配置文件中AutoCreate=1及配置RAM策略为always的情况下，禁止启动TimesTen Daemon，否则很有可能导致现有的DS异常。按规范创建完成DS后，AutoCreate必须修改为0。TimesTen Daemon均为开机默认自动启动。

检查方式：人工检查

- **操作流程：**

1、检查sys.odbc.ini配置文件中AutoCreate配置是否为0；

2、启动TimesTen Daemon：`ttdaemonadmin -start`

### TimesTen Daemon停止

- **规范：**

【强制】禁止在现场在用节点停止TimesTen Daemon，否则会导致业务连不上TT，导致业务异常。停止TimesTen Daemon维护操作，一般是在维护备节点，或者DR节点时使用到。

检查方式：人工检查

- **操作流程：**

1、确认当前节点是否为在用节点；

2、确认该节点上没有业务链接；

3、确认复制器策略修改为manual并停止；

4、确认RAM策略修改为manual并unload；

5、停止TimesTen Daemon：ttdaemonadmin -stop

### TimesTen Daemon强制停止

- **规范：**

【强制】禁止在现场在用节点强制停止TimesTen Daemon，否则会导致业务连不上TT，导致业务异常。强制停止TimesTen Daemon维护操作，一般是在维护备节点，或者DR节点无法正常停止TimesTen Daemon时使用到。

检查方式：人工检查

- **操作流程：**

1、确认当前节点是否为在用节点；

2、确认该节点上没有业务链接；

3、确认复制器策略修改为manual并停止；

4、确认RAM策略修改为manual并unload；

5、确认是否可以正常停止TimesTen Daemon；

6、如不可能正常停止TimesTen Daemon，尝试采用force停止：ttdaemonadmin -stop \-force

### TimesTen Daemon重启

- **规范：**

【强制】禁止在现场在用节点重启TimesTen Daemon，否则会导致业务连不上TT，导致业务异常。重启TimesTen Daemon维护操作，一般是在为了实现快速重启TT时使用到。

检查方式：人工检查

- **操作流程：**

1、确认当前节点是否为在用节点；

2、确认该节点上没有业务链接；

3、确认复制器策略修改为manual并停止；

4、确认RAM策略修改为manual并unload；

5、重启TimesTen Daemon：ttdaemonadmin -restart

## TimesTen Server维护

说明： TimesTen Server类似Oracle数据库的监听。

### TimesTen Server启动

- **规范：**

【强制】现场生产环境，必须保证TimesTen Server为启动状态，不管是主备机还是DR，否则会导致业务无法链接TT，导致业务异常。在涉及TT的启停操作时，必须检查TimesTen Server状态，确保其为启动状态。

检查方式：人工检查

- **操作流程：**

1、检查TimesTen Server状态：ttstatus

2、启动TimesTen Server：`ttdaemonadmin –startserver`

### TimesTen Server停止

- **规范：**

【强制】禁止在现场在用节点停止TimesTen Server，否则会导致业务连不上TT，导致业务异常。停止TimesTen Server维护操作，一般是在维护备节点，或者DR节点时使用到，为了尽快释放链接，保证该节点没有数据更新。同时在异常故障频繁切机时也会使用到。

检查方式：人工检查

- **操作流程：**

1、确认当前节点是否为在用节点；

2、确认该节点上没有业务链接：ttstatus

3、确认TimesTen Server状态：ttstatus

4、停止TimesTen Server：ttdaemonadmin –stopserver

## TimesTen RAM维护

命令参数解释：

```
-ramLoad：Causes the data store to be loaded into RAM. Valid only when ramPolicy is set to                           'manual'.

-ramUnload：Causes the data store to be unloaded from RAM. Valid only when ramPolicy is                            set to 'manual'.
```

### Load TimesTen RAM

- **规范：**

【强制】现场生产环境，必须保证TimesTen RAM为load状态，不管是主备机还是DR，否则会导致业务无法链接TT，导致业务异常。在涉及TT的启停操作时，必须检查TimesTen RAM状态，确保其为load状态。

检查方式：人工检查

- **操作流程：**

1、检查TimesTen RAM状态：ttstatus

2、加载TimesTen RAM：ttadmin -ramload ocs

### Unload TimesTen RAM

- **规范：**

【强制】禁止在现场在用节点Unload TimesTen RAM，否则会导致业务连不上TT，导致业务异常。Unload TimesTen Server维护操作，一般是在维护备节点，或者DR节点时使用到。在DS拷贝的时候，在清理备用节点DS时，需要先Unload RAM。在Unload RAM前需要至少执行

```shell
Command>call ttckpt
```

三次，保证内存中的数据入库到checkpoint文件。

检查方式：人工检查

- **操作流程：**

1、确认当前节点是否为在用节点；

2、确认该节点上没有业务链接：ttstatus

3、确认TimesTen RAM状态：ttstatus

4、unload TimesTen Server：ttadmin -ramunload ocs

## RAM residence policy维护

- **规范：**

【强制】现场生产环境，必须保证RAM residence policy为always，不管是主备机还是DR，否则会导致业务无法链接TT，导致业务异常。在涉及TT的启停操作时，必须检查RAM residence policy策略，确保其策略为always。在unload RAM前，需要修改RAM residence policy为manual。

命令参数解释：

always：The data store should remain in system RAM all the time.

manual：The data store is loaded in system RAM manually by the user

inUse：The data store is loaded in system RAM when in use (i.e., when applications are connected). This is the default.

检查方式：人工检查

- **操作流程：**

1、检查TimesTen RAM residence policy：ttadmin ocs

2、修改TimesTen RAM residence policy为always：ttadmin -ramPolicy always ocs

## TimesTen Replication** **Agent维护

命令参数解释：

\-repStart：Starts the replication agent for the data store.

\-repStop：Stops the replication agent for the data store.

### TimesTen Replication Agent启动

- **规范：**

【强制】现场生产环境，必须保证TimesTen Replication Agent为启动状态，不管是主备机还是DR，否则会导致节点间数据不同步，同步事务日志积压，存在异常风险。在涉及TT的启停操作时，必须检查TimesTen Replication Agent状态，确保其为启动状态。

检查方式：人工检查

- **操作流程：**

1、检查TimesTen Replication Agent状态：

```
ttRepAdmin -showStatus ocs
```

2、启动TimesTen Replication Agent：

```
ttAdmin -repStop ocs
```

### TimesTen Replication Agent停止

- **规范：**

【强制】禁止在现场在用节点停止TimesTen Replication Agent，否则会导致节点间数据不同步，同步事务日志积压，存在异常风险。

检查方式：人工检查

- **操作流程：**

1、确认当前节点是否为在用节点；

2、确认该节点上没有业务链接：ttstatus

3、确认TimesTen Replication Agent状态：

```
ttstatus
```

4、修改Replication policy为Manual

5、停止TimesTen Replication Agent：

```
ttAdmin -repStop ocs
```

## TimesTen Replication Agent Policy维护

- **规范：**

【强制】现场生产环境，必须保证TimesTen Replication Agent Policy为always，不管是主备机还是DR，否则会导致节点间数据不同步，主机或TT异常重启后，复制器未自动启动，存在异常风险。在涉及TT的启停操作时，必须检查TimesTen Replication Agent Policy策略，确保其策略为always。在停止TimesTen Replication Agent前，需要修改TimesTen Replication Agent Policy为manual。

检查方式：人工检查

**命令参数解释：**

always：The agent for the data store should always be running.

manual：The agent is manually started and stopped, but automatically restarted on failures (e.g., data store invalidations). This is the default behavior.

norestart：The agent is manually started and stopped, and not restarted on failures (e.g., data store invalidations).

- **操作流程：**

1、检查TimesTen Replication Agent Policy：

```
ttadmin ocs
```

2、修改TimesTen Replication Agent Policy为always：

```
ttadmin -repPolicy always ocs
```

## TimesTen双机切换操作

- **规范：**

【强制】项目上出现过在业务高峰期，进行了ocs双机的频繁切换，导致业务受到影响。其原因为频繁的双机切换+TT复制延迟，导致主备机tt数据不一致，业务出现了用户余额跳变等问题。同时频繁的切换TT双机，可能因为老的链接得不到及时释放，引起TT链接不足的，而导致业务无法链接TT库的情况。所以TT双机切换需要遵循如下原则：

1、禁止业务高峰期切换：在业务高峰期禁止正常的双机类切换操作，比如升级、刷资费等正常双机切换申请。特殊故障除外，需要严格按照切双机流程检查之后再进行操作。

2、禁止主备机同时操作: 禁止TimesTen的双向Active-Active操作模式，尤其是禁止在备机进行数据增删、变更和数据清理等写操作，读操作不受影响。

3、禁止任何时间频繁切换：禁止频繁的OCS的双机切换，除了高峰期外，在业务低谷期也要避免，尽量的控制在1\~2次之内完成，两次双机切换的时间间隔要至少大于15分钟以上。

检查方式：人工检查

- **操作流程：**

1、切换前检查事项

（1）双机状态

（2）TimesTen复制器状态

（3）长事务锁检查

（4）检查日志积压

（5）检查主备机BAL表数量

（6）系统日志、HA日志、TT日志检查

（7）TT server状态、TT RAM策略、TT 复制器策略检查；

2、切换后检查事项

（1）双机状态

（2）TimesTen复制器状态

（3）长事务锁检查

（4）检查日志积压

（5）检查主备机BAL表数量

（6）系统日志、HA日志、TT日志检查

（7）检查是否能够正常链接数据库，业务系统是否正常，如果没有需要手工重启等人工干预动作。

相关检查详见《TimesTen切换检查指导手册v1.0（20201204）.xls》

## TimesTen Connections参数调优

- **规范：**

【强制】在Linux平台，最新规范内核参数kernel.sem=10240 83886080 4096 8192，满足Connections MAX值需求，同时也满足一台主机多个TT实例的需求。所以在设置Connections的时候，只需要考虑业务需要的最大链接数即可。业务链接TT内存数据库的程序有后台OCS程序、UIP、WEB、APP、CUST、SDP、SelfCare、CRM、BP等，所以TimesTen中Connections的参数要取所有链接TT链接数MAX总和并冗余10%，在冗余后小于1024的，配置Connections=1024，如果大于1024的，取冗余后的值。注意，Connections值，最大为2047。

检查方式：人工检查

- **操作流程：**

由于sys.odbc.ini中Connections参数修改需要重启TimesTen才能生效，所以遵循先DR，后PR，先备机后主机的原则，即：1、DR主备机 > 2、PR备机 > 3、PR主机。

下面给出PR修改Connections参数的大致步骤：

1、检查硬件状态；

2、检查主机状态；

3、检查TT状态；

4、根据上述规则，计算Connections值；

5、修改PR备机sys.odbc.ini 中Connections参数；

6、注释PR备机TT相关crontab

7、停止PR备机网管Agent

8、停止PR备机链接TT的业务会话，包括ttisql登录会话；

9、停止该域TT主机复制器（DR主备机和PR主备机）；

10、ttstatus确认PR备机，除了TT后台进程，没有其他TT会话；

11、PR备机停止tt server：ttDaemonAdmin -stopserver

12、PR备机修改ram策略：ttadmin -ramPolicy manual ocs

13、PR备机卸载内存：ttadmin -ramunload ocs

14、PR备机停止daemon进程：ttdaemonadmin -stop

15、PR备机启动daemon进程：ttdaemonadmin -start

16、PR备机加载ram：ttadmin -ramPolicy always ocs

17、PR备机启动tt server：ttDaemonAdmin -startserver

18、PR备机ttstatus验证TT状态；

19、PR备机验证参数是否生效：Command\> call ttConfiguration;

20、启动该域TT复制器（DR主备机和PR主备机）；

21、验证复制器同步是否正常；

22、验证TT数据同步完成；

23、启动PR备机业务程序，并验证业务是否正常；

24、恢复备机crontab；

25、启动备机网管Agent

26、切换OCS双机，把PR业务切换到PR备机；

27、业务检查，HA检查、TT检查；

28、参见如上步骤，修改PR主机Connections参数；

29、考虑相关crontab、job等补跑；

说明：TimesTen Connections参数及相关问题参见《系统集成FAQ_Oracle TimesTen IMDB Connections参数及相关问题指导手册v1.1(20200401).pdf》详细描述。

## TimesTen表数据维护

根据oracle timesten最佳实践，推荐permsize设置为40g左右。

项目上导致TT访问性能缓慢的主要原因如下：

1、单表记录数过多：

2、个别表包含out-of-line字段；

3、频繁的对表进行大量数据的变动，导致表碎片率过高；

4、没有按时清理过期数据或临时数据；

5、建表后再新增相关字段，导致表存在多个partition；

6、SQL条件不完全匹配，未走索引等

7、PermSize使用率超过80%；

8、未定期进行表统计信息收集。

### TimesTen单表数据量

- **规范：**

【推荐】很多项目上，客户要求保留大于6个月的数据，导致TimesTen单表记录数越来越大，甚至达到了上亿的记录数，导致TT访问性能缓慢。按最新规范，单表数据推荐不大于3000W。现场需要告知客户，当单表数据量超过3000W（项目经验值）时，会存在性能很慢的风险。

### TimesTen表字段类型选择

- **规范：**

【推荐】在规划表字段类型时，尽量不要使用OUT-OF-LINE字段，OUT-OF-LINE字段存在如下缺点：

1、访问数据的速度较慢，因为TimesTen把INLINE的数据和OUT-OF-LINE的数据不是存储在同一个连续内存段中。

2、填充数据比较慢，因为TimesTen生成更多的日志操作（DML活动，如更新和插入）。

3、删除数据速度较慢，因为Timesten执行更多回收和日志记录操作。如果要删除大量行（100000或更多），考虑使用多个较小的delete from语句。

4、truncate table语句的性能与delete from类似，如果表中有任何OUT-OF-LINE列，则它不会具有正常的性能优势。

5、在大的事务回滚的情况下，完成回滚所需的时间比Insert要长得多，因为它必须扫描/渗透所有内存页中的所有日志和分散的OUT-OF-LINE列。

6、很多内存碎片发生在具有OUT-OF-LINE列的数据存储上，特别是具有大型DML活动的数据存储上；

### TimesTen表数据的删除

- **规范：**

【强制】删除数据必须在在用主节点进行，不能在备机或者DR节点删除数据，避免双向同步。删除数据必须加where条件，避免把全表都删除了，删除数据前一定要对现有数据进行备份。

检查方式：人工检查

【推荐】删除数据必须在业务低谷期进行，一般在凌晨。

- **操作流程：**

1、删除数据需要生成根据主键删除的SQL脚本，逐条删除；

2、删除数据只能在主机（当前active节点）删除；

3、中间需要sleep、同时分文件执行，每个文件执行间隔需要sleep 10s，每个文件要求不超过10万条，要不然容易产生长事务；

4、删除数据需要在业务低谷期进行；

5、删除数据先备份到文件；

6、删除数据不一定能释放TT perm空间，TT只会回收连续的空间；

7、删除数据后，建议手工执行空间回收命令：call ttCompact（如果删除数据量很大的情况下，执行此命令可能导致锁表，务必保证闲时执行）;回收连续的内存空间；

8、对文件进行切割后，需要检查文件中sql是否带where条件，现场出现过分割文件异常，导致删除没有带where条件把整个表都删除的情况；

### TimesTen表过期数据清理

- **规范：**

【强制】TT表过期数据的清理需要根据主键字段逐条删除记录。清理方法参考5.16.3

检查方式：人工检查

【推荐】如没特殊需求，表的数据量建议保留三个月即可。

- **操作流程：**

【强制】必须只能在OCS的ACTIVE节点进行删除操作

检查方式：人工检查

### TimesTen表临时数据清理

- **规范：**

【强制】除了特殊情况，不允许在TT库中创建临时表。
检查方式：人工检查

【强制】对于临时创建的TT临时表，需要做好规划及时清理。
检查方式：人工检查

## PermSize维护

### 扩容PermSize

- **规范：**

【推荐】Oracle专家表示dssize使用率超过80%，就可能会对数据库产生影响，导致性能缓慢，当PermSize接近80%的时候需要考虑扩容。扩容一般采用先扩容备机和DR，然后切机，再扩容主节点的模式；特别需要注意：

1、在修改tt的参数时，不能有连接还连接该TT库，要不然，参数修改会不生效，包括ttisql登录的链接。

2、如果使用了hugepage，在permsize扩容的同时，需要先扩容hugepage；

3、PermSzie扩容上去后，如果想缩减，并不是简单的通过减少PermSize来实现，具体参考缩小PermSize章节，所以在扩容的时候不要盲目的加大PermSize；

- **操作流程：**

1、各节点检查数据是否同步，是否存在告警；

2、停止备机及DR节点业务程序；

3、注释备机及DR节点crontab；

4、确认没有链接；

5、修改复制器策略为manual，停止各节点复制器；

6、停止备机及DR节点TT server；

7、修改备机及DR节点RAM策略为manual，unload RAM；

8、停止备机及DR节点ttdaemon；

9、备份备机及DR节点sys.odbc.ini；

10、修改备机及DR节点sys.odbc.ini

11、备机及DR节点扩容hugepage；

12、启动备机及DR节点ttdaemon；

13、备机及DR节点修改RAM和复制器策略为always；

14、验证permsize修改是否生效；

15、启动备机及DR节点TT server

16、是否正常使用hugepage，复制是否同步；

17、切机同理操作主机；

### 缩小PermSize

- **规范：**

【推荐】PemSzie并不是越大约好，permsize越大，在TT加载的时候使用的时间越多，在TT异常重启时，消耗的时间越多。同时在业务不需要这么多permsize的情况下，也会浪费越多过多内存。缩小并不是简单的通过减少PermSize来实现，需要通过ttmigrate工具来实现。缩小一般采用先扩容备机和DR，然后切机，再扩容主节点的模式；

特别需要注意：

1、如果使用了hugepage，在permsize缩小的同时，也需要缩小hugepage，避免内存浪费；

3、ttmigrate时间较长；

- **操作流程：**

1、各节点检查数据是否同步，是否存在告警；

2、停止备机及DR节点业务程序；

3、注释备机及DR节点crontab；

4、确认没有链接；

5、修改复制器策略为manual，停止各节点复制器；

6、备机及DR节点执行3次checkpoint入库；

7、备机及DR节点执行ttmigrate导出；

8、修改备机及DR节点RAM策略为manual，unload RAM；

9、删除备机及DR节点DS

10、停止备机及DR节点ttdaemon；

11、备份备机及DR节点sys.odbc.ini；

12、修改备机及DR节点sys.odbc.ini

13、备机及DR节点缩小hugepage；

14、启动备机及DR节点ttdaemon；

15、备机及DR节点ttmigrate导入；

16、备机及DR节点修改RAM和复制器策略为always；

17、验证permsize修改是否生效；

18、启动备机及DR节点TT server

19、是否正常使用hugepage，复制是否同步；

20、切机同理操作主机；

## 扩容TempSize

- **规范：**

【推荐】当TempSize接近80%的时候需要考虑扩容。扩容一般采用先扩容备机和DR，然后切机，再扩容主节点的模式；特别需要注意：

1、在修改tt的参数时，不能有连接还连接该TT库，要不然，参数修改会不生效，包括ttisql登录的链接。

2、如果使用了hugepage，在Tempsize扩容的同时，需要先扩容hugepage；

- **操作流程：**

1、各节点检查数据是否同步，是否存在告警；

2、停止备机及DR节点业务程序；

3、注释备机及DR节点crontab；

4、确认没有链接；

5、修改复制器策略为manual，停止各节点复制器；

6、停止备机及DR节点TT server；

7、修改备机及DR节点RAM策略为manual，unload RAM；

8、停止备机及DR节点ttdaemon；

9、备份备机及DR节点sys.odbc.ini；

10、修改备机及DR节点sys.odbc.ini

11、备机及DR节点扩容hugepage；

12、启动备机及DR节点ttdaemon；

13、备机及DR节点修改RAM和复制器策略为always；

14、验证Tempmsize修改是否生效；

15、启动备机及DR节点TT server

16、是否正常使用hugepage，复制是否同步；

17、切机同理操作主机；

## Checkpoint调优

说明：

1、TT checkpoint参数上线及测试时一般采用默认推荐值，上线后需要根据实际高峰期情况进行调整。

2、CkptLogVolume和CkptFrequency只要有一个条件满足，tt就会触发检查点动作；

3、该参数支持在线调整，本次有效；

4、永久生效，需要修改sys.odbc.ini；

### CkptFrequency调整

- **规范：**

【推荐】CkptFrequency参数初始化安装时配置为300，单位为秒，系统上线后，根据业务高峰期ttckpthistory返回值配置。因为在TT checkpoint时，会消耗大量的IO资源和CPU等资源。所以CkptFrequency的调整主要是为了错开各个节点的checkpoint时间点，来避免IO争用，也避免主备机同时checkpoint的情况下影响TT性能。

1、如果现场TT均使用本地SSD盘，则CkptFrequency参数配置，只要实现本域中各节点checkpoint时间错开即可；

2、如果现场TT均使用来自同一个存储的盘，则拉长CkptFrequency时间，来错开checkpoint时间点；

- **操作流程：**

1、各节点检查CkptFrequency配置：

```
Command> call ttckptconfig;
```

2、在线修改CkptFrequency配置：

```
Command> call ttckptconfig(ckptFrequency, ckptLogVolume, ckptRate);
```

3、验证是否生效；

4、修改sys.odbc.ini永久生效；

### CkptLogVolume调整

- **规范：**

【推荐】
CkptLogVolume初始化时配置为0，单位为MB，即不启用该参数。在使用本地SSD盘的情况下，系统上线后，推荐根据业务高峰期TT checkpoint情况对CkptLogVolume进行调整。该参数建议原则要高于CkptFrequency时间约束，建议在10分钟（600s）；一方面弥补CkptFrequency出现bug或者异常情况下不做检查点缺陷，另一方面把检查点主导权让位给CkptFrequency来控制。其中该值调整计算方法如下：

若当前CkptLogVolume设置128M，检查点切换频率为1分钟一次，那么合理的值：

CkptLogVolume = 128×10分钟 = 1280M；

- **操作流程：**

1、各节点检查CkptLogVolume配置：

```
Command> call ttckptconfig;
```

2、在线修改CkptLogVolume配置：

```
Command> call ttckptconfig(ckptFrequency, ckptLogVolume, ckptRate);
```

3、验证是否生效；

4、修改sys.odbc.ini永久生效；

说明：在使用存储盘的情况下，由于为了错开各节点的checkpoint时间，会取较大的CkptFrequency值，所以在此场景下，不推荐开启CkptLogVolume属性。

### CkptRate调整

- **规范：**

【推荐】CkptRate参数初始化安装时配置为40，单位为MB，系统上线后，根据业务高峰期ttckpthistory返回值配置。配置公式：

CkptRate=BYTESWRITTEN/((ENDTIME-STARTTIME)\*1.2\*1024\*1024)

```sql
Command> call ttckpthistory;
< 2016-02-22 15:13:21.191828, 2016-02-22 15:13:21.661049, Fuzzy , Completed       , Checkpointer    , <NULL>, 1, 21, 11016, 93927, 5368709120, 93385, 3923512040, 12, 25576512, 25636104, <NULL> >

STARTTIME：2016-02-22 15:13:21.191828
ENDTIME：2016-02-22 15:13:21.661049
BYTESWRITTEN：25636104
```

*1.2为冗余系数；*

- **操作流程：**

1、各节点检查CkptRate配置：

```
Command> call ttckptconfig;
```

2、在线修改CkptRate配置：

```
Command> call ttckptconfig(ckptFrequency, ckptLogVolume, ckptRate);
```

3、验证是否生效；

4、修改sys.odbc.ini永久生效；

## 长事务处理

- **规范：**

【强制】现场出现长事务时，需要根据手册《TimesTen长事务.pdf》定位相关sql，并及时回滚长事务，避免出现同步事务日志积压，导致TT异常的情况。
检查方式：人工检查

- **操作流程：**

参见《TimesTen长事务.pdf》

## TimesTen备份

### TimesTen全库备份

- **规范：**

【强制】每天凌晨均需要对TimeTen库做全库备份，保留最近8份TT全库备份。
检查方式：工具检查（集成脚本生成）

### TimesTen库关键表的备份

- **规范：**

【强制】一般每3小时对TimeTen库做关键表备份，保留最近8份TT库关键表备份，同时关键表备份时间推荐和业务高峰期错开。说明：在国际中心，关键表一般是BAL表。
检查方式：工具检查（集成脚本）

### TimesTen库sys.odbs.ini备份

- **规范：**

【强制】每天凌晨需要对TimeTen库sys.odbc.ini进行备份，保留最近7份备份。
检查方式：工具检查（集成脚本）

## TimesTen备份检查

### TimesTen库备份脚本检查

- **规范：**

【强制】TimesTen全库备份绝对不能使用ttmigrate或ttbulkcp等命令进行，这些命令都会对表做锁定，从而导致呼叫等业务的异常。另外对于单表备份，不能使用ttbulkcp命令，这会导致备份时锁表，从而影响在线业务。
检查方式：人工检查

### TimesTen库全库备份检查

- **规范：**

【强制】查看TimesTen全库备份定时任务获取备份脚本路径,检查备份文件是否正常生成。

备份crontab（TT备份在root用户下）：

```shell
0 2 * * * su - tt -c “/bakcdr/shell/ttbak.sh”
```

检查方式：工具检查（集成脚本生成）

### TimesTen库关键表备份检查

- **规范：**

【强制】查看TimesTen库关键表备份定时任务获取备份脚本路径,检查备份文件是否正常生成。

备份crontab（TT备份在root用户下）：

```shell
0 1,4,7,10,13,16,19,22 * * * su - tt -c “/bakcdr/shell/ttbak_bal.sh”
```

检查方式：工具检查（集成脚本生成）

### TimesTen库sys.odbc.ini备份检查

- **规范：**

【强制】查看TimesTen库sys.odbc.ini备份定时任务获取备份脚本路径,检查备份文件是否正常生成。

备份crontab（TT备份在root用户下）：

```shell
0 2 * * * su - tt -c “/bakcdr/shell/ttbak_dsconf.sh”` 
```

检查方式：工具检查（集成脚本生成）

## TimesTen定时碎片整理

### TimesTen定时碎片整理

- **规范：**

【推荐】每天凌晨均需要对TimeTen库做碎片整理。

碎片整理crontab（TT碎片整理在root用户下），碎片整理的时间点需要和TimsTen的数据删除时间点分离，建议放在数据删除之后再做碎片整理：

```shell
####################TT defragement#############
0 6 * * * su - tt -c "/tt/shell/ttcompact.sh"

============ttcompact.sh
#！/bin/bash
ttisql ocs <<EOF
call ttcompact;
quit;
EOF
```

检查方式：人工检查

# 附录1：TimesTen在线手册

- TimesTen Release 7

Oracle已经不提供在线手册，因为TT7已经EOL，如果需要可以找集成获取或者在如下目录下获取：
/tt/TimesTen/tt11/doc

- Oracle TimesTen In-Memory Database Documentation 11g Release 2 (11.2.2)

https://docs.oracle.com/cd/E21901_01/index.htm

- Oracle TimesTen In-Memory Database Documentation Release 18.1

https://docs.oracle.com/database/timesten-18.1/

# 附录2：TimesTen Lifecycle

参考：

1、HOWTO : Find Oracle TimesTen In-Memory RDBMS Current Release And Support
Policy Information (Doc ID 1305293.1)

2、https://www.oracle.com/support/lifetime-support/

![image](uploads/4068/75b69e0d-e589-4051-92f5-c671f2447015/Release_Status.png)
![image](uploads/4068/70e75782-4e86-4a9b-8d90-6f206b9f229d/key_colors.png)

- Release

For releases up to 7.0 this is the first two digits of the TimesTen version.
From 11.2.1 onwards it is the first three digits.

- Current Patch Set

Oracle does not issue individual patches for TimesTen. Instead patches are
included in patch sets which are full kits, with the fixes fully tested. Each
patch set includes all the fixes from earlier patch sets. Patch sets might be
released for only a subset of the platforms the release is supported on. Patch
sets are indicated by changes to the 4th and 5th digit from release 11.2.1
onwards. Minor new functionality might be included, especially when the 4th
digit changes.

- Next Patch Set

This column shows the version of the next expected Patch Set. Note that this is
not a guarantee that the listed patch set will be released, and if it is
released it may not be produced for all platforms.

"None" indicates no more patch sets are planned.

- Latest All Platform Patch Set

This is the most recent patch set to have been released for all supported
platforms.

- Cache requires

This is a list of the minimum patch set levels for each Oracle Database release
support for use with the IMDB Cache with a particular release of TimesTen.

- Premier Support

The release is fully supported. Fixes for new bugs/issues may be produced.

See Lifetime Support Policy for details.

- Extended Support

This is a purchasable support option which allows fixes to be obtained for
critical issues.

See Lifetime Support Policy for details.

- Sustaining Support

Customers get indefinite assistance with service requests, on a commercially
reasonable basis, 24 hours per day, 7 days a week. See Lifetime Support Policy
for details.

# 附录3：TimesTen商务集锦

## ESL许可

### 总体规则

Oracle DB产品2018协议已经签署. 针对Oracle产品的使用规则，说明如下：

1、公司当前的代码全部为ESL（即嵌入式），所有使用要求需要遵守ESL协议规范。

2、ESL协议中的重点关注点包括：

- 销售合同中的项目或者应用场景应符合协议中的应用程序包（APRF）；

- 销售合同中的Oracle产品的配置数量需要符合硬件或应用场景的配置原则；

- 销售合同中Oracle产品不能单独向客户进行报价，需要随着应用程序包进行报价。

- 销售合同中的条款需要体现《合作伙伴网络嵌入式软件许可分销协议》中16条限制条款的内容，即需要将《End
  User Agreement》作为交付的一部分提供至客户。

3、浩鲸/软创本次也作为ESL协议的成员，需要特别关注以下约定：

（1）Oracle VAD销售到中兴通讯的license不能叠加利润后再次销售给中兴软创/浩鲸。

（2）Oracle VAD销售到中兴软创/浩鲸的license 不能再次转售给中兴通讯。

### Oracle License的种类

1、Full Use(FU)：全权使用

2、Application Specific Full Use(ASFU)：应用程序特定全权使用

3、Embedded Software License(ESL)：嵌入式软件许可

### 售卖渠道

1、Full Use

• Oracle－总代－二级代理商（即：OPBC会员）－最终用户

• Oracle－FUDA合作伙伴－最终用户

2、ASFU：Oracle－（总代）－ASFU合作伙伴－最终用户

3、ESL：Oracle－（总代）－ESL合作伙伴－最终用户

**在ESL协议中，我司的角色就是ESL合作伙伴**

### ESL License的特点

ESL 许可是捆绑了合作伙伴特定硬件/应用，具有最严格限定性的软件许可。
没有CSI，不能获得Oracle的直接服务。

ESL许可 “**三不**”原则

- 不可转移

– 不可以转移应用, 当捆绑的硬件/应用废弃时，ESL许可也同时作废

- 不得到Oracle原厂的直接支持

– ESL代理商提供技术支持(first line support)；

– Oracle不对最终客户提供支持，也不授权第三方提供技术支持

- 不可升级

– ESL许可不可升级为完整使用许可（Fulluse）

## License 配置指导

### 我司oracle License 类型

Oracle Database License 按许可限制性不同，总共分为3 种（Full Use、Application
Specific Full Use、Embedded Software License），**我司默认采购的是ESL（Embedded
Software License）授权。**

ESL 授权商务价格最低，但限制也最多，需要我司在Oracle 数据库方面有一定技术积累。

ESL 授权的主要限制：

1、 最终用户只能再我司提供的应用范围内使用Oracle，不可用于其他应用；

2、Oracle的安装必须作为整个引用安装的一部分执行

3、 最终用户不能直接安装、访问、修改Oracle程序

4、带Oracle的应用软件系统不向最终用户提供仍和直接访问途径

5、 我司提供一线技术支持， Oracle原厂不提供

6、 不得将Oracle产品向最终用户单独报价或者单独销售

### Oracle Database License 计算方式

Oracle Database 有两种License 授权方式：按CPU 物理核心数(Processor)和按用户数(Named User Plus)。前一种方式一般用于用户数不确定或者用户数量很大的情况，典型的如互联网环境；而后一种则通常用于用户数确定或者较少的情况。

我司这两种License授权方式的代码都有发放，产品线根据自己产品的实际情况来判断用哪种授权方式更合适。一般TT均采用按CPU物理核心数(Processor)方式进行采购，示例如下：

Oracle TimesTen In-Memory Database 11gR2 for Linux(x86-64)/1 processor：内存无限制,已含Replication-Timesten to Timesten选项,**一年基本服务**。

#### 按CPU 物理核心数(Processor)计算License 配置原则

**参考：**

**1、How to Find the Oracle Processor Core Factor Multipliers (Doc ID 1330016.1)**

**2、processor-core-factor-table-070634.pdf**

根据安装服务器的CPU 配置来计算License 数量，具体计算规则如下：

1、 确认CPU 的数量和物理核心数。

2、 确认CPU 的类型，不同的CPU 类型对应不同的折算系数，常用的Intel系列CPU折算系数为0.5，其余详见附件processor-core-factor-table-070634.pdf。

3、根据以上信息计算出所需Oracle Database Processor License 数量。

公式：Processor 数量=CPU 数量\*每个CPU 物理核心数\*折算系数。

4、选择对应代码进行配置。

具体配置举例：1 台数据库服务器有2 个Intel silver 4114 CPU，每个CPU 有10个物理核心。

按公式Processor 数量=CPU 数量\*每个CPU 物理核心数\*折算系数，计算：

Processor 数量=2\*10\*0.5=10 processor，由此得出这台数据库服务器需要10Processor的License。

如果选择上表中的（Oracle TimesTen In-Memory Database 11gR2 for Linux(x86-64)/1 processor：内存无限制,已含Replication-Timesten to Timesten选项,**一年基本服务**），本身已经包含了1Processor，所以license需要配置10套。

#### 按用户数(Named User Plus)计算License 配置原则

PS：需要注意的是采用用户数来计算License的前提是：用户数量可以被明确计算清楚的情况下。一般**网管Oracle
DB数据库**以改方式进行购买。

Oracle 用户数的官方定义是每一个访问Oracle数据库的用户，无论是自然人还是设备(如工业环境中的传感器之类)，都算作一个用户(Named User)。

Named User定义为经授权使用安装在一台服务器或多台服务器上程序的人员，而不管此人是否在任何规定时间使用这些程序（OMA）

- 除了所有被授权使用程序的人员之外，不是由人操作的设备如果可以访问这些程序，也要被算作新增指定用户

- 如果使用多路复用硬件或软件（比如TP监视器或网络服务器产品），则必须在多路复用前端测定其数量

按用户数配置要达到每个处理器指定的用户最小数量（若实际用户数小于最低数量，客户需要按最低数量购买使用授权）

Oracle DB EE, 最小购买用户数为 25NUP/Processor

Oracle DBSE/DBSE1, 最小购买用户数为 5NUP

- 适用于用户量小的环境，例如员工休假申请系统

计算过程：

1、 首先确认可以被明确计算清楚的用户数量。

2、 选择对应代码进行配置。

3、 核对是否达到了Oracle 要求的对应版本最小用户数购买数量，参考下表。

4、 如果计算出来的用户数量低于最低购买数量，需按最低购买数量购买

Oracle DB 版本，最低购买数量：

Oracle Database Standard Edition：5 Named User Plus licenses

Oracle Database Enterprise Edition：25 Named User Plus licenses per CPU

**PS：我们一般不按照此类方式进行配置， 因为无法确定系统的使用人员。**

## License常用问题FAQ

**1、Oracle TimesTen IMDB 是否需要进行激活**

答：Oracle TimesTen IMDB
安装使用不需要进行激活，没有序列号，也没有用于激活Oracle TimesTen IMDB的电子License 文件。完成采购后Oracle 会提供PUN 授权文件（电子或纸质）。

**2、购买Oracle TimesTen IMDB 授权后对使用的版次是否有限制？**

答：版次无限制。例如：购买了Oracle TimesTen IMDB的授权，那么无论哪个版次都是可以使用的（TT7、TT11、etc，当然Oracle建议使用当期新版本的数据库。

**3、虚拟化环境下License 计算原则是怎样的？**

答：按虚拟机所在物理机的物理CPU 配置情况计算License 数量。

**4、什么是硬分区和软分区？**

答：分区意味着把服务器上的CPUs划分成多个独立的时间片(sections)作为独立的系统，有时候分区也被称为segmenting.

- 软分区：软分区是用操作系统的的资源管理软件对操作系统划分。

下面是一些典型的软分区：Solaris 9 Resource Container, AIX Workload Manger, HP Process Resource Manager, Affinity Management, Oracle VM, VMware，etc. 以上不是完整的软分区系统列表。

Oracle数据库如果运行在有软分区管理系统的机器上，必须按所在**物理机**的实际CPU数目购买许可证。

- 硬分区：硬分区是对一个服务器做物理划分使之从一个大的服务器分隔成多个独立的小系统。每个分离的小系统作为一个独立的，自我管理的服务器拥有自己的CPU，操作系统，独立的启动区，内存，输入输出子系统和网络。

典型的硬分区包括：Dynamic System Domains, Solaris 10 Containers, LPAR(在AIX5.2中增加了DLPAR),Micro-Partiktions, vPar, nPar, Integrity Virtual Machine，Secure Resource Partiontions，Static Hard partitioning等等。

Oracle认识到Hard Partitioning是目前一种发展趋势，和所谓“Capacity on Demand”和”Pany As you Grow”商业模式密切相关。Oracle允许客户根据Oracle数据库所在的小分区所使用的CPU数目购买许可证。

应该注意的是oracle不允许客户使用硬分区技术把一个多CPU的主机划分成多个小分区，每个小分区最多只有四个处理器插槽（socket），来购买oracle数据库。

硬件处于不断的发展和变化之中，目前这样的许可证政策不是最终的和不变的，另外oracle没有针对所谓”Pay Per Use”或者”Pay Per Forecast”商业模式的特殊的许可证政策。

**PS：分区场景和云计算场景，oracle license计算参见附件：Oracle license-分区场景.pdf、Oracle License-云计算场景.pdf**

**5、ORACEL维保每年都是22%，ESL也是每年22%吗？**

答：是的。ESL的维保也是每年22%。

**6、用系统所运行的Oracle软件不能得到Oracle原厂的直接支持，那么这个支持来自代理吗？**

答：是的，来自合作伙伴，ZTE就是合作伙伴。也就是，Oracle的支持不是针对最终客户的，而是针对合作伙伴（ZTE的）。

**7、软件不具备迁移和扩展系统功能，是不是说，若替换现有系统，现有系统上的ESL都利旧搬迁到新的机器上？**

答：ELS协议里面有一条的不可转移协议：

– 不可以转移应用, 当捆绑的硬件/应用废弃时，ESL许可也同时作废

这里面是硬件或者应用，**是或的关系**。所以我们是这样解读的：如果Oracle是绑定在硬件上，那么硬件废弃，License也是废弃了。如果Oracle是绑定在软件系统上的，那么软件系统废弃，也就废弃了。我们是后者的情况，只要系统一直在用，就可以利旧。

**8、假设出现某局点使用旧版本的ORACLE（ESL），如果相关维保服务在自带的过期后就一直没续，现在想要升级至最新版本的话，是不是：1、不补服务费用的话，需要购买新LICENSE；2、补购过去每年的服务后免费升级。每年服务多少钱？**

答：1，是；2，对维保服务中断的License，补交150%维保费用（其中的50%算作罚金），续服务的费用为每年license费用的22%，具体金额需要根据ZTE和Oracle签署的协议来定。

**9、ORACLE LICENSE （ESL及其他所有类型）都是永久性的？**

答：是，但如果不购买Oracle的服务，但是没法进行更新和升级操作。

**10、ORACLE LICENSE ESL的转移性。什么情况下可转移？是否有主机型号及品牌的限制？CPU核数及类型限制？**

答：跨平台迁移后，原License可以复用。对新平台的License数量，把不够的补齐即可。该规则和新平台的品牌和型号没有关系，只和CPU类型和核算有关。

**11、容灾和TESTBED需要购买正式LICENSE吗？有没有免Oracle license的例外？**

答：容灾和TESTBED是需要正常购买正式License的，具体可以上一题的问答。例外:

生产容灾环境：如果明确一年内Oracle DB运行时间不超过10天，可免License

Testbed：一年运行时间不超过2天，且DB运行不超过4次，可免License

**12、在实际销售过程中，Oracle可否提供一些书面文件，以证明我司具有ESL版本的销售权？如果可以，具体是什么样的证明？时间有效期为多久？**

答：1，本地Oracle
无权要求ZTE的终端用户或ZTE出示这种证明。除非通过Oracle中国。因为协议是在ZTE和ORACLE中国之前签订；2.如果ZTE客户要求，Oracle中国可以协助ZTE证明。

**13、ZTE发货的Oracle ESL数据库，续保能否由浩鲸来续服务？**

答：不可以，必须由ZTE来续服务。谁购买谁续的原则。

**14、运营商被收购的情况，是否违背ESL限制条款？**

答：不违背

**15、ESL能否部署在云平台上？**

答：不可以

**16、Oracle的license能否跨平台进行迁移，比如从IBM Unix平台到x86 linux平台？**

答：Oracle在技术上不做限制license的跨平台迁移；

**17、扩容场景，原有 DB是 FULL USE版本，扩容之后，新增加的ORACLE 是否可以由ZTE来购买ESL版本？**

答：如果扩容的License是跟原有的License部署在同一套主机上，是不行的；如果扩容的部分部署在新的主机上，构成一个新的数据库实例的话，是可以的。

**18、双机备份，备机是否需要购买license？**

答：1.热备份模式(active-active)下的备机需要购买Oracle License。2.冷备模式(active-standby)下的备机不要购买Oracle License。备注：冷备机如果在一年之内开机超过10天，需要购买License.

**19、系统知识产权转移, 是否可以转移给客户？**

答：ESL协议的数据库不能进行知识产权转移，需要客户和Oracle重新签订OPN协议。

**20、第三方的备份软件能否直接访问数据库，比如做数据库的备份操作？另外第三方软件能否直接访问数据库，比方通过数据库表接口的方式？**

答：备份操作也需要通过ESL嵌入系统提供的接口进行；数据库表接口的形式是明确不行的。

# 附录4：Oracle TimesTen

参考：

1、Oracle TimesTen 产品和技术白皮书.pdf

2、Oracle TimesTen基础\&Tips.pdf

3、深入Oracle内存数据库.pdf

4、Oracle TimesTen In-Memory Database 产品中心：
https://www.oracle.com/cn/database/technology/timesten-overview.html

## Oracle TimesTen产品系列

Oracle TimesTen
实时数据管理软件由三个基于内存中数据库、数据复制和高速缓存技术的产品组成。

- Oracle TimesTen In- Memory Database（Product）

Oracle TimesTen In-Memory Database （Oracle TimesTen IMDB）是一个内存优化的关系数据库，它为应用程序提供了当今实时企业和行业（例如电信、资本市场和国防）所需的即时响应性和非常高的吞吐量。Oracle
TimesTen In-Memory Database作为高速缓存或嵌入式数据库被部署在应用程序层中，它利用标准的 SQL
接口对完全位于物理内存中的数据存储区进行操作。

![image](uploads/4068/0ddd8e9e-c2c1-48d8-bdc3-f0701c4516bd/oracle_TimesTen_Database.png)

- Replication – TimesTen to TimesTen（Option）

Replication – TimesTen to TimesTen 是 Oracle TimesTen In-Memory Database的一个选项，它支持服务器间的实时数据复制，以获得高可用性和负载共享。数据复制配置可以是双机热备份(active-standby) 或负载均衡(active-active)，可以使用异步或同步传输，可以包含冲突检测和冲突解决以及在故障服务器恢复后自动重新同步。数据复制与Cache Connect to Oracle 选项完全兼容。

![image](uploads/4068/106e0bc2-f74e-414b-ba3a-f5cea6c2a5e6/oracle_TimesTen_Database_option.png)

- Cache Connect to Oracle（Option）

Cache Connect to Oracle 是 Oracle TimesTen In-Memory Database的一个选项，它为位于应用程序层中的Oracle数据创建实时、可更新的高速缓存。它免除了后端系统的计算负担，并支持反应灵敏且可伸缩的实时应用程序。Cache Connect to Oracle 能够将 Oracle 数据的子集加载到 TimesTen中，能够双向传播更新，能够使对非高速缓存数据的 SQL请求的透传自动化，并能够在故障之后自动重新同步数据。Cache Connect to Oracle与Replication – TimesTen to TimesTen 选项完全兼容。
![image](uploads/4068/1629ec06-7e0e-48f2-9d41-4948dad9c54b/oracle_TimesTen_Database_option2.png)

## 内存中数据库技术

内存中数据库 (IMDB) 技术是 Oracle TimesTen 产品的基础技术。IMDB技术实现了这样一个关系数据库：其所有运行时数据都位于内存中且数据结构和访问算方利用该特性实现了性能突破。与完全高速缓存的RDBMS 相比，IMDB 技术使用的 CPU资源少很多，这是因为它避免了用于管理内存缓冲区并处理多个数据位置（磁盘和内存）的开销。对IMDB 技术而言，磁盘用于实现持久保存和恢复，而不是用作主要的数据库存储位置。

Oracle TimesTen内存优化的性能由提供事务属性功能、持久保存机制以及系统故障恢复所完善。有各种方法可用于锁定、多用户隔离和记录，从而满足了各种应用情形（从临时的查找高速缓存到核心事务交易和计费系统）。

TimesTen通过将已提交事务中的更改记录到磁盘并定期更新数据库的磁盘镜像（称作“检查点”）实现了持久性。应用程序可以对日志写入磁盘的时间进行配置（要么与事务的结束时间同步，要么一直延迟到事务完成之后），从而实现了更高的性能。在许多情况下，高吞吐率要比同步记录重要，尤其是当事务的货币价值很低或事务数据的生存时间较短时（如，当在每几秒种传输一次移动电话位置的网络中跟踪移动电话的位置时）。

Oracle TimesTen产品支持的原生接口符合标准，且一般与任何其他符合标准的关系数据库兼容。应用程序通过
JDBC（Java 数据库连接）或 ODBC（开放数据库连接）接口发出SQL（结构化查询语言）命令。用于定义数据存储区和复制配置的语句也遵守 SQL语法惯例。此外，还使用 SNMP（简单网络管理协议）发出标准化的系统管理警报。

Oracle TimesTen 提供了具有标准 JMS 接口的开放式事务日志 API (XLA)来读取事务日志。它对于创建响应数据库更新的应用程序很有用。在这方面，XLA是一个轻型“触发器”。它还用于构建从 Oracle TimesTen到其他数据库系统的自定义数据复制。

## Oracle TimesTen的物理结构

Oracle TimesTen 产品由以下组合组成：

- 共享库

- 内存中数据结构

- 系统进程（后台程序/子后台程序/代理）

- 管理程序

- 磁盘上的检查点和日志文件

![image](uploads/4068/6626144a-6dd2-424a-8ca8-b989fa4910ca/TimesTen_Structure.png)

### 应用程序层共享库

1、动态链接程序库（Link Library）

2、功能包括：

- 执行SQL语句并返回执行结果

- 往日志缓存中写入日志

实施 SQL操作的例程以及相关函数包含在一组共享库中，开发人员将这些库链接到应用程序并作为应用程序进程的一部分执行。此共享库方法与更常规的RDBMS不同，后者实现为与应用程序连接（通常通过客户端/服务器网络连接）的一组可执行程序。通常，将数据管理器库嵌入到应用程序中可能会使数据存储区在应用程序进程异常终止时容易遭到破坏。OracleTimesTen 解决了这一难题。Oracle TimesTen库使用正在MicroLogging算法保护自身不受应用程序进程故障的影响。内存中数据库保持一致，并且其他应用程序不受影响而继续运行。

![image](uploads/4068/7319987b-db4a-43f4-ae45-40fa3eaa99ff/timesten_ddl1.png)

![image](uploads/4068/74fce833-7978-47c1-a556-d4f56dcc3f99/timesten_ddl2.png)

应用程序还可以使用客户端/服务器连接访问 Oracle TimesTen数据库，但在大多数情况下，使用直接链接的应用程序将实现最佳性能。对于客户端/服务器访问，服务器后台程序（后台进程）将远程用户连接到服务器代理，服务器代理包含代表远程客户端访问数据存储区的共享库。

### 内存中数据结构

1、Data Store：保存所有数据库数据的区域

2、日志缓存：用于暂时存储记录Data Store变更的日志

3、临时数据区域：

- 临时存储执行计划等数据的共享区域

- 排序等等操作临时使用

内存中数据库在操作系统的共享内存段中维护，它包含所有用户数据、索引、系统目录、日志缓冲区、锁表和临时空间。多个应用程序可以共享一个数据存储区，而单个程序可以访问同一系统上的多个数据存储区。

![image](uploads/4068/c8844ada-abf3-4e13-8ab2-361e26033245/Data_Structure1.png)
![image](uploads/4068/3123f7b3-b30d-4da3-8721-2a24568d136d/Data_Structure2.png)

### **系统进程**（后台程序/子后台程序/代理）

1、常驻后台进程

- 主进程(Daemon)

监听功能(Listener)

读取配置文件odbc.ini

分配和监视Sub Daemon

- 子进程(Sub Daemon)

载入/卸载Data Store

将日志缓存写入日志文件

监视和解除死锁(Dead Lock)

执行检查点(Checkpoint)

2、可选后台进程

- Replication代理：实施Replication

- Cache代理：实施Cache Connect

- TimesTen服务器：采用客户端/服务器连接时的服务器进程

后台进程在系统级别为启动、关闭和应用程序故障检测提供服务，并在数据存储区级别为加载、检查点和死锁处理提供服务。每个数据存储区都有一个实例范围的TimesTen后台程序（一个系统可能有多个实例）和一个单独的数据存储区子后台程序。

### 管理程序

用户、脚本或应用程序显式调用实用程序来执行交互式
SQL、批量复制、备份/恢复、数据存储区移植和系统监视等服务。

### 检查点和日志文件等

![image](uploads/4068/bb439cf7-e605-4d11-91e7-84fc77c5d3ca/checkpoint.png)

1、配置文件odbc.ini

- 用于记录各个DSN的参数

2、检查点(Checkpoint)文件

- 保存于磁盘的数据库镜像。

- TimesTen启动时，检查点文件的数据被装载到内存中

- TimesTen运行时，隔一段时间进行一次检查点处理，仅保存改变的数据块，并删除无用的日志文件

- TimesTen关闭时，用于保存Data Store内的数据

- 出于安全考虑，存在两个文件

3、日志文件

- 保存数据库的变更

- 原有文件超过一定的大小后，自动生成新的日志文件

- 与检查点文件一起用于数据库的恢复

定期将数据存储区和事务日志的更改写入磁盘。如果需要恢复数据存储区，Oracle TimesTen将把磁盘上的数据存储区检查点与仍位于日志文件中的已完成事务合并在一起。检查点和日志文件使用普通的磁盘文件系统。在有限情况下，可以将Oracle TimesTen 配置为执行无磁盘操作。

![image](uploads/4068/77ee4ea0-fdbd-4382-be8e-705cf86519da/logfile.png)

Checkpoints把data store的当前状态记录在硬盘上，TimesTen交替的把数据记录在两个checkpoint检查点文件上；有了checkpoint检查点文件和日志文件，Timesten就能保证在任何情况下数据的完整性和一致性，Timesten自动清除log文件。

### 数据复制技术

当需要近乎连续的可用性或负载分配时，可以将数据复制配置为在两个或多个服务器间发送更新。将主服务器配置为发送更新，将用户服务器配置为接收更新，而服务器可以同时用作主服务器和用户服务器来执行双向复制。基于时间的冲突检测和解决用于当同时在多个位置更新同一数据时（这种情况很少出现）建立优先级。

![image](uploads/4068/83d84258-395b-4d92-805a-70676e933fcb/replication.png)

配置复制后，将为每个数据存储区启动复制代理进程。如果为复制而配置了同一服务器上的多个数据存储区，则每个数据存储区将有一个单独的复制代理。每个复制代理能够向一个或多个用户服务器发送更新，并从一个或多个主服务器那里接收更新。这些连接分别在复制代理进程的内部实现为一个单独的执行线程。复制代理通过TCP/IP 流套接字进行通信。

为获得最高性能，复制代理通过监视现有的事务日志检测数据存储区更新，并在可能的情况下向用户服务器发送批量更新。只复制提交的事务。在用户服务器节点上，复制代理通过高效的低级接口更新数据存储区，从而避免了SQL 层的开销。

### 高速缓存技术

当使用 Oracle TimesTen 将 Oracle数据的某些部分高速缓存到内存中数据库时，将创建一个高速缓存组数据库结构来保存高速缓存的数据，应用程序将调用其他共享库例程，同时启动一个系统代理（即高速缓存代理），此代理在高速缓存数据库和Oracle 数据库之间执行所有异步数据传输。

![image](uploads/4068/4743d2a0-9142-426f-8bfc-e3f5ddea5945/highspeed.png)

高速缓存组是由一个或多个通过主键/外键关系以逻辑层次结构排列的表的集合。高速缓存组中的每个表都与
Oracle 数据库表相关。一个高速缓存组表可以包含相关 Oracle表中的所有行和列或行和列的一个子集。可以通过基于高速缓存管理器的浏览器或通过 SQL语句创建和修改高速缓存组。高速缓存组支持以下特性：

- 应用程序可以对高速缓存组执行读取和写入操作

- 可以自动或手动刷新高速缓存组（将 Oracle 数据库数据置于高速缓存组中）

- 可以自动或手动清理高速缓存组（将高速缓存更新传播到 Oracle 表）

- 可以自动跟踪对 Oracle 表或高速缓存组的更改

如果应用程序更新了高速缓存组中的行，则将 Oracle表中的相应行作为同一事务的一部分同步更新，或在事务执行后立即异步更新，具体情况取决于所创建的高速缓存组的类型。异步配置显著提高了吞吐量并缩短了响应时间。

如果在同步提交至 Oracle时因某种原因失败，则回滚事务，从而保持一致性，而异步配置将只记录 Oracle失败，而不是自动回滚 Oracle TimesTen事务（因为该事务已经提交）。而异步配置的优点（除性能外）在于，即使在与 Oracle的连接断开的情况下，它仍将继续运行，并在恢复连接时自动将更新应用于 Oracle。

源自 Oracle表的更改通过高速缓存代理刷新到高速缓存中。对高速缓存数据的更新置于表中，并定期由代理放到高速缓存中。用户在高速缓存外部所定义数据的老化也是由代理执行的异步操作。

## 连接TimesTen的方法

1、直接连接

- ODBC直接驱动器连接（原生API）

- 通过ODBC驱动管理器(Driver Manager)

- 通过JDBC桥接

Direct Driver Connect(直接驱动器连接)说明：

- Oracle推荐的连接方式，具有最佳的性能

- TimesTen数据库与应用程序处于同一台主机上，同处于应用程序层

- 应用程序通过ODBC/JDBC直接对数据库进行访问

- 与传统的客户端/服务器的模式相比，减少了TCP/IP、IPC方面的开销

![image](uploads/4068/5d1c218f-cd08-4e1a-9246-69707732f4d2/directlink.png)

2、C/S模式连接

- 使用ODBC进行客户端/服务器连接

- 使用JDBC进行客户端/服务器连接

Client/Server Connection(客户端/服务器连接)说明：

- 传统的连接方式，性能比直接驱动器连接差

- TimesTen数据库与应用程序处于不同的主机上

- 客户端与服务器一般以TCP/IP方式连接，存在网络开销

![image](uploads/4068/5daeecfc-b7e3-4fd7-8fce-3134d04f3472/cslink.png)

## TimesTen的优点

![image](uploads/4068/af25f3ad-a69f-4dda-9384-2907233c724b/advantage.png)

1、实时性能：高速数据处理，微秒级别的响应时间。TimesTen的数据都在内存中，拥有更优化的算法和更少的CPU开销，所以才这么快！

![image](uploads/4068/82c1733f-7093-440a-aa4f-336a9d58e143/cpucost.png)

2、基于标准：采用标准技术，支持大部分SQL92的功能，包括索引，物化视图。减少开发难度和开发时间，减少维护成本；

![image](uploads/4068/520ed2d3-2f89-4d8a-b307-4e4d1bff304d/basestandard.png)

3、多用户并发

4、高可靠性

![image](uploads/4068/b37a242c-8f2d-48b3-ad65-156bb7732ba6/highreliability.png)

5、无数据丢失

6、几乎无需管理

7、灵活的部署选项，相关的产品和服务:

- Replication -TimesTento TimesTen（选项）

- Cache Connect to Oracle（选项）

# 附录5：深入研究 IMDB 技术

内存中数据库技术通过更改有关数据在运行时所在位置的假设提供了引人注目的性能。通过在内存中管理所有数据并针对该环境进行优化，内存中数据库技术可以更高效地发挥作用，从而显著显著提高响应性和吞吐量。

但这种性能的核心是什么？应用程序能否只通过将其所有 RDBMS数据置于主内存中而获得同一结果？

RDBMS执行的大部分工作都是基于数据主要位于磁盘中这一假设完成的。优化算法、缓冲池管理以及索引化检索技术都有利于此基本假设。

而 Oracle TimesTen知道数据位于主内存中，因此可以更直接地路由数据，从而降低了代码路径长度并简化了算法和结构。

在比较这些体系结构时，有一些重要的差别清楚地说明了如何实现数倍的性能改进。为了进行说明，在查询优化算法、缓冲池管理和索引结构中只提供了其中少数几个差别。

## 查询优化

基于磁盘的系统与基于内存的系统使用不同的查询优化算法。RDBMS优化决策依赖于数据主要位于磁盘上这一假设。在动态的运行时环境中（数据在任何给定时刻都可能位于磁盘上或缓存在主内存中），基于磁盘的系统必须假设最差的情形。由于磁盘I/O 的开销远远高于内存访问，因此基于磁盘的RDBMS必须假设数据位于磁盘上。它们针对减少性能瓶颈点（即磁盘I/O）进行了优化。如果这就是所采用的假设，那么基于磁盘的优化器不会总为主要（或完全）位于主内存中的数据生成最佳计划。

而 IMDB技术知道数据位于主内存中，并基于更简单的假设优化它的查询。它不需要根据磁盘驻留进行最差情形假设，因此它的开销估算可能会更简单并更准确。

## 缓冲池管理

在常规的 RDBMS 体系结构中，必须为已经高速缓存到主内存中的数据维护高速缓冲池。当SQL查询处理器需要一页数据时，访问方法必须先在缓冲池中搜索该内存中数据。即使该数据位于缓冲池中，在许多情况下仍必须将它复制出缓冲池以便随后进行处理。此缓冲池的维护和管理以及额外的数据副本显著增加了将数据提供给应用程序的最初开销。尽管缓冲池在基于磁盘的数据管理解决方案中是必要的，但在基于内存的数据管理中却不是必要的。Oracle TimesTen没有缓冲池。由于数据已经位于主内存中，因此不需要缓冲池。这样便降低了代码路径的长度和引擎的内存需求，避免了复制，简化了算法并更迅速地将数据传输给应用程序。

此外，这些 RDBMS产品不会在运行时动态改变这些基于磁盘的假设。基于磁盘的假设在系统代码库中的交错过于紧密，以至于无法使用几个精心设计的if-then-else语句来简化它们。在以下两个体系结构的索引树结构中可以看到有关这个相互交错、基于磁盘的假设示例。

## 索引结构

### B-Tree

在典型的 RDBMS B-Tree索引页中，键值和数据指针均保存在B-Tree条目中。B-Tree节点（磁盘上的页）由许多B-Tree条目组成，每个条目都保存索引数据值和下一个相应索引节点的页码或保存所搜索到的数据行的磁盘块页码。该结构使得树非常平和宽（非常适于减少磁盘I/O）。在B-Tree结构中，主要的目标是减少完成数据文件索引化查找所需的磁盘 I/O数量。

B-Tree实现此目标的方法是：

1、将键值保存在B-Tree节点本身中（减少磁盘 I/O）；

2、将尽可能多的索引条目保存到节点中（增加可以用单个 I/O提供服务的B-Tree条目数）。

该结构尽管对于磁盘上的数据和索引文件比较适合，但对于内存中的数据则不太适合。将数据保存到内存中以后，索引模式的目标是减少CPU 周期而非 I/O。CPU 周期用于扩展和比较B-Tree中的压缩索引值。大量的 CPU周期还用来管理保存数据的缓冲区以及已经从磁盘读取到内存中的索引。

### T-Tree

在 Oracle TimesTen中，情况要简单一些。T-Tree针对主内存访问进行了优化。就大小和算法而言，它的索引条目比B-Tree的更经济。T-Tree节点之间的连接通过\<= 和 \>=指针实现。这两个指针引用内存位置，而非磁盘上的页。仅仅通过这两个比较，T-Tree搜索算法便知道它正在搜索的值是位于当前节点上还是位于内存中其他位置了。每次使用新的索引节点指针间接运算符都会使搜索区域减半，体现了真正的二分搜索。

![image](uploads/4068/0c9ccaad-e4ad-4594-ae49-19a5cfff7969/T_tree.png)

主内存数据管理的目标是减低空间要求、消除磁盘 I/O以及简化算法、代码路径和内存使用量。T-Tree减少空间要求的方法是不在索引节点本身中保存键值，而是只指向已经位于内存的数据行中的值。由于索引树结构全部位于内存中，因此树没有磁盘I/O。T-Tree是一个非常简单的算法，降低了代码复杂性和代码路径的长度。使用T-Tree将获得基于B-Tree访问的所有优势，并可以大量节省移动操作以及缩小大小。

前面的体系结构差别示例表明，消除磁盘驻留性假设（或数据位置的模糊性）将显著降低复杂性。计算机指令数至少降低十倍，缓冲池管理不复存在，不需要额外的数据副本，索引页减小，并且它们的结构得到简化。当数据的内存驻留性成为基本事实假设时，一切变得更简单、更简洁、更精巧、更快速。

# 附录6：TimesTen复制技术

**PS：项目上，目前采用A-A-A-A复制模式，即各个节点即为主服务器，也为用户服务器，的异步复制模式。**

所谓的复制就是在数据库之间复制数据。Oracle TimesTen复制主要是为了使任务关键的应用程序能够在尽可能不影响性能的情况下连续使用数据。除了在故障恢复中的重要作用外，复制在多个数据库之间分配用户负载从而实现最高性能和简化在线升级和维护方面也很有用。

Oracle TimesTen遵循“主服务器-用户服务器”复制模型，即将提交的更改从它们的源复制到一个或多个用户服务器数据存储区。复制通过SQL语句进行配置，可以应用于指定的表（Table）或整个数据存储区（Datastore）。为提高效率并降低开销，TimesTen使用一个基于事务日志的复制模式。复制使用无磁盘日志记录或基于磁盘的日志记录。

每个主服务器数据存储区和用户服务器数据存储区上的复制都由通过 TCP/IP 流 socket通信的复制代理控制。主服务器数据存储区上的复制代理从其事务日志中读取记录，并将检测到的对复制元素的任何更改转发给用户服务器数据存储区的复制代理。然后，用户数据存储区的复制代理将把更新应用于其数据存储区。如果主服务器复制代理转发更新后，用户服务器复制代理并未运行，则主服务器复制代理将把更新一直保存在它的日志中，直到可以在用户服务器复制代理上应用这些更新。

## 平衡性能和一致性

默认情况下，Oracle TimesTen复制是一个异步机制。当使用异步复制时，一个应用程序将更新主服务器数据存储区并继续工作，而不等待用户服务器数据存储区接收更新。主服务器数据存储区和用户服务器数据存储区使用内部机制确认用户服务器数据存储区已经成功接收和提交更新。这些机制可以确保只在用户服务器数据存储区上应用一次，但它们对于应用程序是完全透明的。

异步复制提供了最高的性能，但应用程序与被复制的元素在用户服务器数据存储上的接收过程完全分离。Oracle TimesTen还为需要对复制的数据在主服务器数据存储区和用户服务器数据存储区上的一致性抱有更高信心的“悲观的”应用程序提供了两个返回服务选项：

- return receipt服务：通过在复制确认用户数据存储区已经接收到了更新前阻止应用程序，使应用程序与复制机制松散耦合或“异步化”

- return twosafe服务：通过在复制确认用户数据存储区上已经收到并提交了更新前阻止应用程序实现完全的同步复制

使用返回服务的应用程序用损失一些性能的方法来确保主服务器数据存储区和用户服务器数据存储区之间具有更高级别的数据完整性和一致性。在主服务器数据存储区发生故障时，应用程序可以在更大程度上确信主服务器数据存储区提交的事务保存在了用户服务器数据存储区中。与return twosafe 复制相比，return receipt复制需要更少的同步，并且对性能的影响也更小。

## 异步复制和同步复制流程

### 异步复制

异步复制流程如下图所示：

![image](uploads/4068/40e87ed2-8979-40e9-bc78-648de0ba0e59/asyn_replication.png)

- 发送方

(1)交易被提交，依据应用系统的设置，交易日志被记录到日志缓冲区或同步写到磁盘日志文件。

(2)当日志缓冲区“满”了，交易日志会被写到磁盘的日志文件里面。

(3)复制代理向接收方发送这批交易信息。

- 接收方

(4)接收方代理在datastore上执行这批交易。

(5)强制写磁盘交易日志文件。

(6)接收方代理向发送方发送确认响应。

- 发送方

(7)发送方代理更新日志文件的Bookmark。

### 同步复制

同步“2-Safe”复制流程如下图所示：

![image](uploads/4068/74713fbd-5e20-4ca1-9d85-edfcbdc37bb3/sync_replication.png)

- 发送方

(1)交易被设置为“Return 2-Safe”并提交，本地交易日志记录PRE-COMMIT日志记录。应用处于‘Commit’阻塞状态。

(2)发送方代理向接收方发送交易信息。

- 接收方

(3)接收方代理在datastore执行交易

(4)并发送确认响应。

- 发送方

(5)发送方代理提交处于等待状态的交易。

- 接收方

(6)接收方代理强制写磁盘交易日志文件，并发送最终确认响应。

- 发送方

(7)发送方代理更新交易日志文件的Bookmark。
![image](uploads/4068/7465ce16-d206-41f0-a715-959e4b6441c0/replication_topo.png)

## 复制拓扑

通过将一个数据存储区同时指定为主服务器和用户服务器，可以配置双向复制此外（A-A），Oracle TimesTen 还允许多节点“N路”复制，从而提供了各种可能的复制拓扑，其中包双机热备份配置和负载均衡配置。后者还可以分成分割式负载（其中的每个复制表只有一个主服务器）和分布式负载（其中的每个表有多个主服务器）。在分布式负载配置中，应用程序负责在两个系统之间进行分工，以避免发生复制冲突。如果发生了冲突，则基于时间戳的冲突检测和解决机制可以防止出现不一致的复制。

还可以定义一个用作传播服务器的用户服务器，该服务器从主服务器接收复制的更新并将其传递给它自身的用户服务器。传播服务器对通过较低带宽的网络连接（如内联网中的服务器之间的连接）优化复制性能很有用。

# 附录7：CheckPoint文件与Trans Log的关系及其原理

## 相关问题

1、Times Ten为什么有两个CheckPoint文件？

2、两个CheckPoint文件之间是什么关系？

3、两个CheckPoint文件与Trans Log之间是什么关系？

4、TimesTen是怎么维护两个CheckPoint文件和Trans Log的？

## TimesTen的内存结构概述

为了很好的理解TimesTen中两个CheckPoint文件与TransLog的关系及其原理，在此再简单介绍一下TimesTen的内存结构。

![image](uploads/4068/cf57b9f1-5ac2-4189-9c12-68c38eef0e3e/memory_structure.png)

1、Data
Store，数据库所有数据的保存区域；加载所有数据的内存区域，TimesTen的所有的运算都是在Data Store中完成的。

2、日志缓存（LogBuffer），用于暂时存储记录Data Store变更的日志缓冲区，由后台进程将缓冲区的数据写入Trans Log，复制进程实时复制到目标端。

3、临时数据区域，临时存储执行计划等数据的共享区域，排序等操作临时使用。

4、检查点(CheckPoint)文件，保存了两个互为备份的DsName.ds0和DsName.ds1，可以理解为Oracle的数据文件，是内存数据库保存于磁盘的数据镜像。

5、事务日志（Transation Log）文件DsName.logNNN，保存Data Store的数据变更到物理设备。

从内存结构图可以看到，TimesTen包含两个检查点(CheckPoint)文件。为什么会存在两个检查点(CheckPoint)文件，这两个文件之间是什么关系？其实这两个文件的关系很简单，就是互为镜像。

## 两个CheckPoint文件与Trans Log的关系及原理

TimesTen为什么会有两个CheckPoint文件，原因其实很简单，互为镜像，至于为什么互为镜像但是又不能存放到不同的路径/存储，这属于设计方面的问题，这里不做讨论。

为了直观的说明两个CheckPoint文件与Trans Log的关系及原理，把CKPT的过程抽象成下面图表，分别对创建DSN开始，到进行4次CKPT进行描述。

![image](uploads/4068/43a1683a-10d4-4883-8c8f-9587b4773a45/mirror_checkpoint.png)

1、创建DSN：首次创建DSN时，TimesTen会生成DSName.log0和DSName.ds0和DSName.ds1三个文件，其中DSName.logN是一个顺序递增的文件名。为了下面描述更加直观，假设每一次CheckPoint时产生2个事务日志（Trans Log）文件。

2、第1次CKPT：由于每次产生两个Trans Log文件，所以第一次CheckPoint时，将DSName.log0/1/2三个事务日志的变化写入检查点文件DSName.ds0，检查点文件DSName.ds1不变。由于DSName.log0/1/2三个事务日志尚未写入检查点文件DSName.ds1，所以此时不会删除任何事务日志文件。

3、第2次CKPT：第二次CheckPoint时，会将DSName.log0/1/2/3/4五个事务日志的变化写入检查点文件DSName.ds1，检查点文件DSName.ds0不变。由于DSName.log0/1/2三个事务日志已经写入检查点文件DSName.ds0和DSName.ds1，所以此时SubDaemon进程会触发删除DSName.log0/1/2事务日志文件。

4、第3次CKPT：第三次CheckPoint时，会将DSName.log3/4/5/6四个事务日志的变化写入检查点文件DSName.ds0，检查点文件DSName.ds1不变。由于DSName.log3/4两个事务日志已经写入检查点文件DSName.ds1和DSName.ds0，所以此时SubDaemon进程会触发删除DSName.log3/4事务日志文件。

5、第4次CKPT：第四次CheckPoint时，会将DSName.log5/6/7/8四个事务日志的变化写入检查点文件DSName.ds1，检查点文件DSName.ds0不变。由于DSName.log5/6两个事务日志已经写入检查点文件DSName.ds0和DSName.ds1，所以此时SubDaemon进程会触发删除DSName.log5/6事务日志文件。后面的CheckPoint对检查点文件的写入和Trans Log事务日志的清理操作以此类推。

# 附录8：TimesTen 常见问题答疑

## Oracle TimesTen

1、什么是 Oracle 内存数据库 TimesTen？

答：Oracle 内存数据库 TimesTen是一个针对内存进行了优化的关系数据库，它为应用程序提供了当今实时企业和行业（如电信、资本市场和国防）所需的即时响应性和非常高的吞吐量。
Oracle 内存数据库 TimesTen 作为缓存或嵌入式数据库部署在应用程序层中，利用标准的SQL 接口对完全位于物理内存中的数据存储进行操作。所包括的复制技术能够在 TimesTen数据库之间进行实时事务复制，以实现高可用性和负载共享。

![image](uploads/4068/30d9d614-dbc7-4501-8c41-0a439ac87c7a/what_is_TT.jpg)

2、Oracle 内存数据库 TimesTen 是否对硬件和软件有特殊要求？

答：Oracle TimesTen 数据库是在假设所有受管理的数据都驻留在物理内存 (RAM)中的前提下构建的。因此，对于硬件，要考虑的最重要的事情是应用程序层中要有足够的RAM。除此之外，TimesTen 要考虑的硬件因素极少。
与所有应用程序一样，具有适当数量的CPU（以相应的时钟速度运行）对于应用程序尽可能快得运行是很重要的。同样，要利用多个CPU，需要运行多个应用程序，或应当将应用程序编写为使用多个线程。此外，事务日志和检查点文件持久保存在磁盘上，磁盘越快，实现的整体性能越好。

3、内存数据库 TimesTen 是 Oracle 11g/12c 数据库的一部分吗？

答：Oracle In-Memory Database Cache 是 Oracle数据库的数据库选件，它包括内存数据库 TimesTen、Cache Connect To Oracle 以及Replication - TimesTen to TimesTen 技术。Oracle 内存数据库 TimesTen是经过专门许可的产品，包括内存数据库 TimesTen 和复制组件。

4、哪些平台支持 Oracle TimesTen 技术？

答：支持以下平台：AIX 32/64 位 (Power)、HP-UX 32/64 位（PA-Risc 和Itanium2）、HP TRU64 64 位 (AlphaChip EV68)、Linux RedHat 和 SUSE 32/64位（x86、x86-64 和 Itanium2）、Linux Oracle、MontaVista CGE 和 Asianux 32/64位（x86 和 x86-64）、Sun Solaris 32/64 位（Sparc 和 x86）和 Windows 32/64位（x86 和 x64）。

## Oracle TimesTen In-Memory Database

1、内存数据库 TimesTen 可以作为独立的数据库使用吗？

答：可以，现在用户将 Oracle 内存数据库 TimesTen (IMDB)作为独立的数据库在应用程序层使用。TimesTen IMDB 为 SQL操作提供了全面的事务处理支持，事务日志持久保存在磁盘上以便于恢复（数据库始终位于内存中）。

2、Oracle 内存数据库 TimesTen 可以作为 Oracle 数据库的内存缓存使用吗？

答：可以，这是 Oracle 数据库选件“Oracle In-Memory DatabaseCache”。该数据库选件包括内存数据库 TimesTen、Cache Connect to Oracle 以及Replication - TimesTen to TimesTen 组件。

![image](uploads/4068/9633a578-b803-4e6d-972e-04c48e61e968/timesten_Cache_Oracle.jpg)

3、内存数据库 TimesTen 的数据访问 API 有哪些？

答：内存数据库 TimesTen 支持标准的 ODBC, JDBC, OCI, ODP.NET等接口，以便应用程序使用 SQL-92 标准连接到数据库。

4、TimesTen 为 32 位和 64 位应用程序提供的接口不同吗？

答：不是，为 32 位和 64 位应用程序提供的应用程序接口是一样的。要利用 64位模式，需要重新编译应用程序并将其链接到 TimesTen 64 位资料库。

5、开发 Oracle TimesTen 应用程序可以使用什么语言？

答：可以使用 C、C++ 、Java 、PL/SQL、PHP以及 R 语言等多种应用程序开发。

![image](uploads/4068/44e93100-944a-4a45-9739-3930042efa3b/TimesTen_Language.jpg)

6、Oracle 内存数据库 TimesTen 是否支持类似 Oracle RDBMS 的索引？

答：是，Oracle 内存数据库 TimesTen支持索引。索引可以提高数据库查询的性能，就像它们在 Oracle 中的作用一样。TimesTen支持两种类型的索引：范围索引，用于涉及等式和不等式范围的查找；和散列索引，提供较范围索引更为快速的主键访问，可精确匹配查找和同等联接。

7、如何在 TimesTen IMDB 中设计和创建数据结构？

答：内存数据库 TimesTen 支持 SQL 标准。要创建数据结构，可使用 SQL DDL 语句，如CREATE TABLE、CREATE INDEX、CREATE SEQUENCE、CREATE VIEW、CREATE MATERIALIZED VIEW、ALTER TABLE 等。用于 RDBMS 的相同数据库设计技术也可用于 TimesTen。在TimesTen 中设计和管理数据库要比在针对磁盘优化的 RDBMS
中简单，因为不需要调整表区域大小或者整理磁盘碎片。

8、TimesTen 是内存数据库，那它如何从节点/电源故障进行恢复？

答：虽然整个数据库驻留在内存中，但事务日志和检查点文件都保存在磁盘上。如果系统重新启动或者出现故障，将从检查点文件和事务日志文件恢复IMDB。此外，可以配置 TimesTen Replication 以向另一个 TimesTen 节点提供事务复制。

![image](uploads/4068/157f31a2-a4de-4851-af6b-0c6b5dbc0246/recover_TT1.gif)
![image](uploads/4068/677252f5-932a-4625-8fad-ef1d8476ad63/recover_TT2.gif)

## TimesTen Replication

1、什么是 TimesTen Replication？

答：TimesTen Replication 是内存数据库 TimesTen 的一个组件。TimesTen Replication技术支持 TimesTen 服务器节点之间的实时数据复制。Replication支持使用同步或异步数据传输进行 active/standby 或 active/active 配置。

2、TimesTen Replication 如何在系统故出现障时确保持续的可用性？

答：可以将 TimesTen Replicaiton 配置为将整个 TimesTen 数据库复制到一个或多个TimesTen节点。发生故障转移后，备用节点将变成活动节点，出现故障的节点可以通过备用（现在为活动）数据库恢复。

3、我可以复制数据库中选定的表吗？

答：可以，表级别的复制和数据库级别的复制均受支持。

4、TimesTen Replication 支持哪些网络协议？

答：TimesTen Replication 在 LAN 或 WAN 上的复制节点间使用持久的流式 TCP/IP套接字。

5、TimesTen Replication 是双向的吗？

答：是的，单向和双向复制均受支持。对于双向复制，建议对负载进行分区，以避免大量冲突。如果在对相同的数据库行进行更新时发生冲突，TimesTen Replication 支持基于时间戳的冲突检测和解决。

6、TimesTen 的Replication 支持 Cache 么？

答：是的，当前TimesTen 内置的高可用复制模式 Active-Standby 支持 TimesTen Cache。

7、选择TimesTen 产品的有点有哪些？

答：当前TimesTen数据库被广泛的应用到实时处理的应用场景当中。选择TimesTen产品来为其OLTP应用提供数据库服务的主要原因有：

对实时事件的响应

微秒级响应时间：一致稳定的响应

快速、一致的响应时间 ，低延时：数据完全加载到内存、且支持直连模式

高峰时段处理超大事务及事件处理：提供持续且不间断的服务

高可用、在线升级：内置的基于复制的Active-Standby + Subscriber 架构，支持TimesTen Cache 以及跨版本升级

标准 SQL/关系型模型、标准 API、缓存 且自动同步 Oracle数据库：极小的应用代码和接口调整即可提升现有应用

![image](uploads/4068/df6659b9-5278-4c1d-8863-1daf1040bc5a/select_advantage.jpg)

![image](uploads/4068/16ce50d4-aec4-43ab-828c-c993e7b511be/select_advantage2.jpg)

# 附录9：Oracle TimesTen 关系型内存数据库 18.1 新版本详解

## TimesTen In-Memory Database Release Notes

参考：https://docs.oracle.com/database/timesten-18.1/TTREL/toc.htm\#BEIDGFAI

## Oracle TimesTen 关系型内存数据库 18.1 新特性

Oracle
TimesTen内存数据库是一个全功能，内存优化的关系型数据库。它主要面向有关系型数据库语义、强一致性和相关功能需求的OLTP应用程序，且具有大规模的水平扩展和超高吞吐量能力。

![image](uploads/4068/ff6d0a29-1471-4040-8b92-78a304821763/feature_18_1.png)

TimesTen 是一款历经20年市场考验的，成熟的关系型内存数据库产品！

TimesTen早在1998年就作为全球首款内存关系型数据库面世。在过去的20多年时间里，TimesTen内存数据库不但为数以千计的企业客户提供高质量的服务，来满足他们对关键业务，核心系统的要求，而且推出了非常多的新版本，新功能来更好的兼容，无缝的集成Oracle数据库和其应用程序。

![image](uploads/4068/fd04d64d-76c2-4c14-acd1-e1c340d6e383/TT_evolution_his.png)

TimesTen利用内存计算优势，在应用层部署可以获得非常快的响应速度，可以在普通商用x86硬件服务器上，轻松达到微秒级的响应速度，以及相应在单位时间内超高的吞吐量。

TimesTen 可以采用两种模式部署：

- TimesTen Classic：数据库在单一节点中部署为非分布式独立数据库，供需要低速、一致的响应速度的应用使用。通过主-备对复制机制实现高可用性，该机制还支持多位只读用户，可扩展大量读取的负载。Classic部署就相当于 TimesTen In-Memory Database早期版本的标准产品功能。各行各业中许多要求提供实时性能（极快响应速度和极高吞吐量）的应用早在多年前便已开始使用此部署模式。

- TimesTen Scaleout：数据库在多节点环境中部署为分布式数据库。具有高吞吐量要求和/或季节性容量需求的应用可通过这种模式获得TimesTen的并发平行跨节点处理、透明数据分发（通过单一数据库映像）和弹性横向扩展功能。TimesTen的 K-safety 特性可自动提供高可用性和容错能力。这是 TimesTen 18.1版中的一个全新特性。

![image](uploads/4068/fbd815da-8445-46a2-a2ec-2555ef8357bf/DeployMethod.png)

Oracle TimesTen In-Memory Database (TimesTen) 18.1 版是业界广泛采用的 TimesTen In-memory
关系数据库的下一代产品。18.1版本的发布是TimesTen产品演进过程中非常重要的一个里程碑，在之前的
TimesTen 版本的基础上，它推出了新的Grid模式：TimesTen Scaleout，即分布式关系型内存数据库。

TimesTen Scaleout 是一个横向扩展的数据库，提供透明数据分布、单一数据库映像、ACID事务处理、自动高可用性、弹性可扩展性以及卓越的性能。它为实时应用提供了大量 OLTP负载所需的即时响应能力和非常高的吞吐量。应用可以使用标准 SQL、PLSQL和标准接口访问 TimesTen Scaleout 数据库，而数据库可根据业务需求进行弹性扩展。

虽然 TimesTen 18.1 同时支持 TimesTen Classic 和 TimesTen Scaleout，但初始版本(18.1.1.1.0) 仅支持 TimesTen Scaleout。初始版本后推出的补丁集中重新引入对TimesTen Classic（包括 Application-Tier Database Cache）的支持

PS：Oracle 内存数据库高速缓存产品名称变更：自2014年6月11日起生效，Oracle数据库企业版下的 Oracle 内存数据库高速缓存（Oracle In-Memory Database Cache）产品组件已经被更名为 Oracle TimesTen应用层数据库高速缓存（Oracle TimesTen Application-Tier Database Cache）。

## Oracle TimesTen In-Memory Database 18.1部署模式

### Classic 模式

#### 独立数据库模式

TimesTen 本身就是一款关系型内存数据库产品。可以为应用程序提供独立的数据库服务

![image](uploads/4068/9e45c7bc-409c-4de1-bf09-7b8192742b63/instance_structure.png)

这种场景下，TimesTen作为数据库独立存储数据并可以结合强大的高可用性解决方案来实现既有高性能，也拥有内置的基于复制技术的高可用性和容灾能力。

![image](uploads/4068/cdc405f2-4bfe-4098-a3d8-d55738cb8560/instance_structure_adv.png)

TimesTen通常建议部署在与应用相同的服务器上，数据库的总容量取决于服务器的物理内存容量。

#### Oracle Database缓存模式

对于已有的Oracle数据库用户也可以通过其高速缓存的配置来加速已有的Oracle数据库的OLTP应用。不同于其他NoSQL缓存需要重写应用程序，对于TimesTen的高速缓存来说，是一套简单的配置过程

![image](uploads/4068/3f8772e9-c41e-4240-a492-4e1b94c98250/flexible_configuration.png)

简单配置完成后，就可以将Oracle数据库中的热点数据子集缓存到一个或者多个 TimesTen数据库中，使得Oracle应用程序充分利用TimesTen 丰富的 Oracle缓存功能，极大的提高应用的响应性能。

TimesTen 的缓存功能提供数据在Oracle数据库和 TimesTen数据库之间的同步。通过TimesTen的高可用和容灾能力，还可以实现真正意义上的多维MAA（最大高可用架构）。

![image](uploads/4068/0cd1618a-f739-4223-aae6-f66871266ce7/readwrite_highseppedcache.png)

### Scaleout模式

#### 分布式数据库模式

在TimesTen 18.1版本中，TimesTen产品家族引入了全新的分布式数据库部署方式 -TimesTen Scaleout。

![image](uploads/4068/f9fc274a-8efe-4646-9d90-dd9469076987/DeployMethod_18.png))

TimesTen Scaleout 是速度最快的、基于SQL的、OLTP优化的分布式关系型内存数据库。基于 TimesTen
内存数据库的行业实力，这款分布式新功能受益于 TimesTen成熟产品的所有的领先功能。例如，TimesTen 横向扩展功能具有复杂的 SQL处理引擎和基于成本的优化器，远比所谓的 "NewSQL" 数据库提供的产品更先进。
TimesTen Scaleout 支持标准的 API，如 JDBC，ODBC，OCI 和 Oracle 数据库兼容的SQL，PL/SQL 和数据类型。另外，与大多数 "NewSQL" 数据库不同，TimesTen Scaleout基于原生引擎、支持完整的 ACID 事务属性、多语句事务、约束和全局二级索引。

这种新的横向扩展体系结构在18.1版本中可在多达64台主机上实现透明扩展，并通过active-active 数据同步的方式实现内置多副本高可用能力。

在 TimesTen Scaleout 中，TimesTen数据库作为分布式数据库部署在多节点环境中。通过利用 TimesTen的并行跨节点处理，透明数据位置和可伸缩性，使得具有高吞吐量要求的应用程序可以在此模式下运行。

- 主要特点

（1）基于成熟、强大和高性能的内存数据库（TimesTen引擎）构建而成

（2）将多台计算机的强大功能整合为一个无共享架构的单一逻辑数据库

（3）为了简单起见，使用单个数据库映像进行透明的自动数据分发

（4）通过 K-safety 提供自动高可用性

（5）完全分布式的高性能 ACID 事务处理可随时提供数据一致性

（6）集中部署以便于管理和监控

（7）使用标准数据库API和标准 SQL

- 架构特点

TimesTen Scaleout的所有安装，配置和管理任务均可方便地集中管理，并可从单个管理实例执行。此实例不参与应用程序SQL 或事务执行，而是存储有关系统配置和拓扑的元数据以及各种组件的状态。它编排跨所有配置主机的TimesTen软件的安装和配置。管理员永远不必登录到其他用户数据存放的主机来执行这些管理操作。为了提高可用性，还可以配置第二个管理实例。

![image](uploads/4068/d871ae31-d4ac-4449-9da7-e1e74d1829a0/structure_adv_18.png)

- 应用开发

对于绝大多数的分布式系统来说，都要求应用程序根据具体分布式产品的要求重新定制开发。而TimesTen Scaleout 的分布式数据库不但支持丰富的开发 API，而且实现了支持 SQL应用的能力！对于应用开发者来说，只需要做极小的代码改造（比如连接串指向变更、failover处理等），即可享受到分布式数据库带来的高并发、高吞吐量的服务！

TimesTen 18.1 在 GitHub 上发布了开源的样例程序。可以看一下基于 JDBC 和 ODBC的样例程序与当前实际运行中的业务系统的 SQL 应用程序有多少区别。

https://github.com/oracle/oracle-timesten-samples/tree/master/quickstart/scaleout/sample_config

- 运维能力

TimesTen Scaleout拥有强大的运维交付能力！它不但推出全新的中控命令行工具，而且还支持通过图形界面工具管理、开发和运维TimesTenScaleout。用户能够通过全新的中控命令行工具来实现一键安装、一键管理的需求！

（1）ttGridRollout 一键安装：\<installation_dir\>/bin/ttGridRollout \<config_file_name\>

（2）ttGridAdmin一键监控：ttGridAdmin 中控（Central Management）命令工具是TimesTen Scaleout 的核心管理工具。用户、DBA 只需要登录管理实例，运行 ttGridAdmin命令，即可实现对分布式内存数据库的监控、配置、管理、问题诊断等一系列操作。这也是真正意义上的可交付、可运维的分布式系统！

（3）图形化工具：用户可以通过 SQL Developer免费工具轻松的来监控、开发、配置和管理数十个节点的分布式数据库！

可以通过下面的链接，直接下载虚拟机OVA镜像文件（内置入门手册实践）。http://www.oracle.com/technetwork/database/database-technologies/timesten/downloads/timesten-181-vm-download-4480199.html

- Oracle TimesTen In-Memory Database 18c Release 1 Software Download

https://www.oracle.com/database/technologies/timesten-downloads.html

- Oracle TimesTen 软件下载

https://www.oracle.com/technetwork/cn/database/database-technologies/timesten/downloads/index.html

**PS：特别的，参见https://docs.oracle.com/database/timesten-18.1/TTGRD/instlgrid.htm\#TTGRD763，目前TimesTen
Scaleout只支持Linux，包括OEL, SUSE和RHEL，支持JDK7,可以运行在JRE8上。**

![image](uploads/4068/44abe8e3-f629-4264-b0a5-6c5a0798bee3/scaleout_limit.png)

------

# 本文件评审、修正记录

| 文件名称 | 数据库运维规范-TimesTen分册 |              |            |        |
| -------- | --------------------------- | ------------ | ---------- | ------ |
| 序号     | 流程                        | 拟制人/审核人       | 审核时间   | 版本号 |
| 1        | 编写                        | 刘海龙，数据库规范组 | 2020/12/18 | V0.1   |
| 2        | 评审、修订                  | 数据库规范组 | 2021/01/15 | V0.2   |
| 3        | 发布                        | 数据库规范组 | 2021/05/30 | V1.0   |
| 4 | 变更字段维护-修改字段中的描述为：“字段类型不可修改” | 数据库规范组 | 2021/06/20 | V1.01 |
| 5 | 增加定时任务ttcompact的说明 | 数据库规范组 | 2021/07/27 | V1.02 |
| 6 | 增加tt表维护部分关于ds推荐40G的说明 | 数据库规范组 | 2021/07/27 | V1.03 |
| 7 | 发布 | 数据库规范组 | 2021/12/30 | V1.1 |
| 8 | 1. 强制条目增加检查方式的说明 <br>2. 适用范围增加规范适配的TT 18版本 <br>3. 修订章节“5.23.1. TimesTen定时碎片整理”，该条目从强制级别修订为推荐级别，修改后：【推荐】每天凌晨均需要对TimeTen库做碎片整理 | 王为 | 2025.9.30 | V1.1.1 |
| 9 | 发布 | 数据库规范组 | 2025/12/23 | V1.2 |
