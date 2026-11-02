![image](uploads/4062/623f6778-5935-4e5b-8c6b-2168774ec0ce/PG_OPE_Oracle.png)

# 编写目的

本文用于指导浩鲸科技运维人员进行数据库运维工作(Oracle部分)

# 适用范围

浩鲸科技所有使用Oracle数据库的项目

# 角色和职责

1. 运维人员: 参考文档对项目数据库进行运维；

2. DBA : 负责运维文档的更新并对运维人员进行技术赋能。

# Oracle日常维护事项

## 表维护

### 碎片处理

碎片整理可以提高数据查询性能，释放表空间。

【推荐】有些表作为接口表，频繁的插入和删除数据，这类表每天的数据插入和删除量比较大，表中的碎片率非常的高，且扫描表数据的SQL多为全表扫描，如果不做处理，查询效率会越来越低，会引起待处理数据积压等故障。

*[注]：国际项目可以通过ZMC/ZCM对按天分区的此类表定期对历史分区TRUNCATE来消除碎片。*

### 分区表

#### 分区交换

【强制】对有海量数据且存在全局索引的分区表禁止进行分区交换操作。

分区交换如果不维护全局索引，交换后全局索引会失效。分区交换如果维护全局索引，由于表中数据量较大，维护成本太高，会对表长时间加锁，阻塞表中DML语句的执行。

**检查方式**：人工检查

#### TRUNCATE分区

【强制】对有海量数据且存在全局索引的分区表禁止进行TRUNCATE分区操作。

分区如果不维护全局索引，全局索引会失效。分区如果维护全局索引，由于表中数据量较大，维护成本太高，会对表长时间加锁，阻塞表中DML语句的执行。

**检查方式**：人工检查

### 清理临时表

临时表指的是：

1. 人为创建的一些非应用系统所需要的表，并且不需长期保留的表；

2. 应用系统自己主动生成的一些表，并且有效期很短。

大量无用表会浪费很多存储空间，会导致相关系统视图的查询变慢，会增加数据库备份的时间等，所以必须要将这些表从系统中清理出去。

#### 临时表应符合命名规则

【推荐】首先需要严禁人员私自在数据库中创建表，个别情况需要创建，一定要经过项目组审批，给表上加注释说明并规范这类表的命名规则(推荐格式：**TMP\_创建人标识\_前缀**)。

| 表分类  | 命名要求    | 举例                                |
|---------|-------------|-------------------------------------|
| 临时表  | 以TMP\_开头 | 比如“浩鲸”同学创建的表：TMP_HJ_PROD |

**检查方式**：人工检查

#### 应用创建的临时表

【推荐】应用中创建的临时表由应用自行维护。

#### 运维人员所建临时表

【推荐】运维人员手工创建的临时表，在确定无需保留的情况下，应及时进行清理。

### DDL语句执行规范

【推荐】申请执行窗口时间，停应用执行。

【强制】禁止在系统忙时执行，应选择系统最闲时执行，并提前通知客户，得到客户许可。

**检查方式**：人工检查

### DML语句执行规范

【强制】禁止在线对表中大批量数据直接进行update/delete 操作。

**检查方式**：人工检查

【推荐】选择系统闲时对所需要update/delete的海量数据，分成多批次操作和提交。

**检查方式**：人工检查

## 索引维护

### 重建索引

满足以下条件的需要索引重建，重建索引会阻塞DML操作，不允许在系统繁忙时重建，请在系统闲时操作,最好申请操作时间窗口进行操作。

**【注意事项】**

- 不可以在系统忙时重建索引，尤其是事务访问繁忙的表；

- 重建过程中不可以强制中断重建过程；

- 重建操作不要通过客户端去执行，请远程到服务器端执行，防止由于网络问题导致连接中断；

- 在线重建必须加 online 参数否则会阻塞访问索引所在表的事务。

#### 索引碎片率高

【推荐】索引所在表数据频繁被删除或者索引字段频繁被更新，这种情况下索引碎片率也会比较高，建议定期对此类索引进行重建。

重建方法参考：[索引重建方法](#rebuild_index)

#### 索引失效

【推荐】人工检查或者通过系统监控系统发现失效索引，要尽快对索引进行重建。

### 分析索引结构

【强制】严禁系统在线情况下使用**analyze index idx_t validate structure**分析索引结构，来判断索引是否需要重建，这个命令会对table加一个表级共享锁，会阻塞DML操作。

**检查方式**：人工检查

## 性能报告分析

### AWR报告

AWR 全称**Automatic Workload
Repository**，帮助DBA迅速定位性能问题，oracle10G后出现，是Oracle运行过程中的信息收集工具。表现形式为：html/txt式的数据报告。awr存放在sysaux表空间中，默认保留7天（10G）或者8天(11G以上+)的快照，每隔1小时生成一次快照(采样时间和保留天数是可修改的) 。

#### 商用系统应定期分析AWR报告

【推荐】运维人员每天应该选取一份系统闲时和忙时的AWR报告进行分析。

AWR报告的手工生成文档参考:[如何获取AWR报告](#generate_awr)

AWR 报告阅读文档参考：[如何阅读AWR报告](#read_awr)

### ADDM报告

ADDM是构建在Oracle数据库内部的自我诊断软件，ADDM检查并分析自动工作量仓库（AWR）捕获到的数据，确定Oracle数据库可能存在的性能问题，然后它定位性能问题的根本原因，为纠正这些性能问题提供建议，并量化预计的性能收益，ADDM也可以识别不需要行动的区域(ORACLE 10g 和以后版本才有)。

#### 商用系统应定期分析ADDM报告

【推荐】商用系统应定期分析ADDM报告。

ADDM报告的手工生成文档参考:[获取ADDM报告](#generate_addm)

## 历史无效数据归档

业务数据库基本都会随着数据库的运行时间增加出现数据库占用空间增大的情况，相应的出现数据库SQL执行变慢，特别是由于数据库规划阶段并未提供数据清理手段，一旦出现索引失效等问题，更加重了IO的负荷，最终出现严重的数据库性能故障。因此在数据库设计阶段提供较好的数据清理手段，将数据库数据维护在一定周期的窗口之中，可较好的避免故障，极大的提升数据库运行的稳定性。

### 分区表的数据清理方法

#### 【推荐】分区表的无效数据，采用分区交换方式清理历史数据

分区交换方法参考：[分区交换](#exchange_partition)

表上有全局索引，分区交换命令必须加上 **update global indexes**参数，否则会导致全局索引失效。但是对于有海量数据的大表，并且存在全局索引，执行分区交换要慎重。因为**update global indexes**比较耗时，阻塞DML，比创建索引时间还长，需要停应用来交换，完成后重建索引。

#### 【推荐】分区表的无效数据，采用truncate 分区方式清理历史数据

**TRUNCATE**表分区方法参考：[分区表TRUNCATE分区](#truncate_partition)

表上有全局索引，**TRUNCATE**表分区命令必须加上 **update global indexes**参数，否则会导致全局索引失效。但是对于有海量数据的大表，并且存在全局索引，执行TRUNCATE分区要慎重。因为**update global indexes**
比较耗时，阻塞DML，比创建索引时间还长，需要停应用来交换，完成后重建索引。

### 非分区表的数据清理

#### 【推荐】重建表

当一个表（千万级以上）需要删除的数据过大，比如超过整个表数量的30%。优先考虑用表重建的方式，这种方式 对应用影响小。

重建表的方法参考：[如何重建表](#rebuild_table)

对于表中数据可以只保留N个月的表，建议重建为按时间来分区的分区表，以后可以通过分区交换或者TRUNCATE 分区的方式来处理。

## 采集更新统计信息

统计信息为了让oracle的SQL优化器了解数据信息，包括数据量的多少和分布，以便SQL优化器CBO能够获得较佳的执行计划，较好的执行计划意味着oracle对于不同的SQL使用合理的访问路径和Join方式，简而言之是得到更好的性能。

### 【强制】定期对数据库进行schema级别统计信息采集更新

数据库中绝大多数表的数据都在不停的进行变化，尤其数据量的变化比较大，为了保证所有的SQL都能获得正确的执行计划，每天必须对统计信息失效的表重新收集统计信息。

**检查方式**：工具（部署定期分析脚本）

## 失效索引检查

索引失效是一个非常糟糕的事情，往往会引发严重的故障，导致整个系统瘫痪，除了日常做操作时候避免引起索引失效，平时也要进行检查

### 【强制】定期对数据库的索引进行检查，规避无效索引

【网管监控】安装了部署网管监控的项目，可以配置相应的监控探针进行监控。

【无网管监控】 如果没有相应的网管监控系统，只能手工检查或者自定义脚本定时检查。

脚本检查方法参考：[失效索引查询](#query_invalid_index)

**检查方式**：ZCM/ZMC

## 监控表空间使用率

ORACLE表空间的空间如果耗尽，相关DML操作会失败，相应的应用操作也会失败，所以表空间使用率的检查必须要做。一般表空间使用率超过80%
,就要进行人工干预，扩表空间或者表空间进行瘦身。

**检查方式**：ZCM/ZMC

### 【强制】定期对数据库的空间进行检查，规避空间满导致故障

表空间使用率检查脚本请参考：[表空间使用率查询](#query_tablespace_usage)

**检查方式**：ZCM/ZMC

## 高频率硬解析SQL检查

硬解析即整个SQL语句的执行需要完完全全的解析，生成执行计划。而硬解析，生成执行计划需要耗用CPU资源，以及SGA资源。高频率的SQL硬解析会消耗过多CPU和占用过多的SGA内存中的SHARE POOL。严重的情况下会引发严重的数据库故障。所以需要定期检查数据库是否存在这种SQL语句。硬解析频率不要高于10次/秒。

### 【推荐】定期对数据库硬解析检查，频率不建议过高

查询方法参考：[硬解析SQL查询](#query_hard_parse)

## 表字段长度使用率检查

表中的某些字段的值是取的sequence值（大多数是主键字段），随着数据量的增长，列值越来越大，超出表字段定义长度后就会引发故障，此故障发生率很高，所以有必要定期对字段长度的使用率进行监控。

### 【强制】定期检查数据库表字段长度使用率

查询方法参考：[字段长度使用率查询](#query_field_length_usage)

**检查方式**：ZCM/ZMC

## 序列(sequence)检查

表中的某些字段的值是取的sequence值（大多数是主键字段），当sequence取值到最大值后，由于获取不到新值，会导致应用出错。有必要定期对数据库序列进行检查和监控。

### 【强制】定期检查数据库序列的使用率

查询方法参考：[sequence使用率查询](#query_sequence_usage)

**检查方式**：ZCM/ZMC

## 固化SQL执行计划

SQL的执行速度主要取决于它采用何种执行计划,执行计划改变是常态，变差可能严重影响业务和整体性能。正常的变化：随着统计信息、绑定变量的变化自动适应；不同的绑定变量，使用不同的执行计划；根据数据量、数据分布的变化（统计信息改变），自动调整执行计划。

但有时候个别SQL的执行计划经常会发生无理由的变化（可能是ORACLE本身的缺陷，不然ORACLE不会提供HINT），而引发故障，给运维工作带来不小的麻烦。对于这类SQL在没有其他更好的方法下，建议进行执行计划固化。

### 【推荐】通过SQL加HINT的方式固化执行计划

需要研发人员修改SQL代码。

### 【推荐】通过SQL PROFILE 方式固化执行计划

不需要修改代码，直接数据库上进行操作即可，缺点就是如果执行计划中使用的相关对象属性发生改变，SQL
PROFILE 将失效，比如 修改了索引名称。

方法请参考：[使用SQL PROFILE固定SQL语句的执行计划](#use_profile_fix_execute_plan)

## RAC状态检查

### 【强制】定期检查集群状态。

运维人员应该定期检查集群状态，防止集群状态异常而导致业务异常。

方法参考：[检查集群状态](#check_cluster_state)

**检查方式**: ZCM/ZMC

### 【强制】定期检查所有Oracle实例（数据库状态）

运维人员应该定期检查集群的所有Oracle实例状态，防止数据库实例状态异常而导致业务异常。

方法参考：[所有Oracle实例（数据库状态）](#check_oracle_instance_state)

**检查方式**: ZCM/ZMC

## Oracle启停

### 【强制】双机状态下数据库需要通过双机来启停和切换

生产环境的数据库都是运行在双机或者RAC模式下，严禁手动对数据库进行启动操作。任何涉及到数据库启停的操作，如修改参数、配置等需要重启，都需要使用双机来启停。

方法参考：
- [【强制】Newstart HA启停数据库](#newstart_start_stop_database)
- [【强制】VCS启停数据库](#vcs_start_stop_database)
- [【强制】PowerHA启停数据库](#powerha_start_stop_database)

**检查方式**: 人工检查

## Oracle备份检查

### 【强制】定期检查逻辑备份是否成功，并且需要逻辑备份需要携带METRICS=Y参数

数据库备份一般定时任务部署在root用户下，需要定期查看逻辑备份是否成功。

方法参考：[【推荐】逻辑备份检查](#check_logic_backup)

**检查方式**: 工具(集成脚本)

### 【推荐】定期检查RMAN备份是否成功

RMAN备份一般用于cc库，分为全库备份和归档日志备份，root用户部署两个定时任务，运维人员需要定期检查rman备份是否成功。

方法参考：[【推荐】RMAN备份检查](#check_rman_backup)

### 【推荐】定期检查全库备份是否成功

查看备份定时任务获取备份脚本路径,检查备份文件是否正常生成。

方法参考：[【推荐】全库备份](#check_full_backup)

**检查方式**: 人工检查

### 【推荐】定期检查归档备份是否成功

查看备份定时任务获取备份脚本路径,检查备份文件是否正常生成。

方法参考：[【推荐】归档备份](#check_archive_backup)

**检查方式**: 人工检查

## Dataguard状态查询

### 【推荐】数据库角色查询，主库应该是PRIMARY，备库应该是PHYSICAL STANDBY

方法参考：[数据库角色查询](#query_database_role)

**检查方式**: 人工检查

### 【推荐】查看数据库进程是否正常

主库中ARCH进程传送日志到备库, 备库中，RFS进程负责接收主库传过来的日志，MRP0进程负责将日志写入备库。

方法参考：[查看数据库进程](#check_database_process)

**检查方式**: 人工检查

## 【推荐】定期查看归档日志传送情况是否正常

进入主备库所在服务器的归档目录，一般为/archcc，查看归档日志，主库和备库存在着同样的最新归档日志。

方法参考：[查看归档日志传送情况](#check_archive_log_transfer)

**检查方式**: ZCM/ZMC

### 【推荐】定期查看日志应用情况,主库的归档日志已经在备库成功应用

方法参考：[查看日志应用情况](#check_log_application)

**检查方式**: ZCM/ZMC

# Oracle常用操作指令

## 表空间使用率查询

<span id="query_tablespace_usage"></span>

```sql
SELECT A.TABLESPACE_NAME,
       ROUND(A.USED_SPACE * B.BLOCK_SIZE / 1024 / 1024) AS USED_SPACE_M,
       B.TOTAL_SIZE_M,
       ROUND(A.USED_SPACE * B.BLOCK_SIZE / 1024 / 1024 / TOTAL_SIZE_M * 100,
             1) AS USED_PCT,
       B.AUTOEXT
  FROM DBA_TABLESPACE_USAGE_METRICS A,
       (SELECT TABLESPACE_NAME,
               ROUND(SUM(BYTES) / 1024 / 1024) AS TOTAL_SIZE_M,
               MAX(AUTOEXTENSIBLE) AS AUTOEXT,
               MAX(BYTES / BLOCKS) AS BLOCK_SIZE
          FROM DBA_DATA_FILES
         GROUP BY TABLESPACE_NAME
        UNION ALL
        SELECT TABLESPACE_NAME,
               ROUND(SUM(BYTES) / 1024 / 1024) AS TOTAL_SIZE_M,
               MAX(AUTOEXTENSIBLE) AS AUTOEXT,
               MAX(BYTES / BLOCKS) AS BLOCK_SIZE
          FROM DBA_TEMP_FILES
         GROUP BY TABLESPACE_NAME) B
 WHERE A.TABLESPACE_NAME = B.TABLESPACE_NAME
 ORDER BY 4;
```

查询结果中undo表空间不作为参考，undo使用率请查看下一章节。

## UNDO表空间使用率查询

undo表空间使用率使用如下sql查询：

```sql
SELECT DISTINCT STATUS, SUM(BYTES) / 1024 / 1024, COUNT(*)
  FROM DBA_UNDO_EXTENTS
 GROUP BY STATUS;
```

结果如下，其中unexpired部分是当前的undo使用情况，expired是可以被overwrite的部份。

![image](uploads/4062/1bd316e8-c736-42c6-8b2d-25360d72af8a/1620289596359.png)

## 数据文件使用率查询

```sql
SELECT b.file_name AS 物理文件名,
       b.tablespace_name AS 表空间,
       b.bytes / 1024 / 1024 AS 大小M,
       (b.bytes - SUM(nvl(a.bytes, 0))) / 1024 / 1024 AS 已使用M,
       substr((b.bytes - SUM(nvl(a.bytes, 0))) / b.bytes * 100, 1, 5) AS 利用率
  FROM dba_free_space a, dba_data_files b
 WHERE a.file_id = b.file_id
 GROUP BY b.tablespace_name, b.file_name, b.bytes
 ORDER BY b.tablespace_name;
```

## 扩展表空间

2. 以扩展cc表空间为例，查询当前表空间数据文件路径和大小：

```sql
select file_name, tablespace_name, bytes / 1024 / 1024 / 1024 "SIZE(M)"
  from dba_data_files
 where tablespace_name = 'TAB_CC';
```

![image](uploads/4062/aa37cf1d-3faf-4914-b329-becc785ff122/1620289647383-1621388622607.png)

数据文件路径为/soft/oradata/cc/tab_cc_001.dbf，大小为1M。

2.检查数据库block_size参数值

```sql
su – oracle

export ORACLE_SID=cc

sqlplus '/as sysdba'

show parameter db_block_size;
```

结果示例如下：

![image](uploads/4062/ceaf75bb-af46-458d-88a1-808397631937/1620289680756.png)

db_block_size值为8192 (8K)则数据文件最大为32G，如果值为16384(16K)，则数据文件最大为64G。

​     3.检查文件系统是否有足够的空余空间

使用df -h命令检查数据文件所在的文件系统是否有足够空间，如果有足够空间继续下一步扩展表空间。

​     4.扩展表空间

```sql
su – oracle

sqlplus ‘/as sysdba’

SQL>alter tablespace tab_cc add datafile '/soft/oradata/cc/tab_cc_002.dbf' size 30720m autoextend off;
```

以上示例命令为表空间tab_cc天加一个数据文件/soft/oradata/cc/tab_cc_002.dbf，大小为30720M，关闭自动扩展。

## 数据库alert日志路径查询

```sql
SQL>select value from v$diag_info where name ='DiagTrace';
```

在查询出的目录中查看文件名为alert\_{SID}.log的日志。

## 硬解析SQL查询

<span id="query_hard_parse"></span>

```sql
SQL> WITH T AS
 (SELECT /*+ materialize */
   COUNT(*) cnt, a.plan_hash_value
    FROM v$sql_plan a
   WHERE a.id = 0
     AND a.TIMESTAMP > SYSDATE - 1
   GROUP BY a.plan_hash_value
  HAVING COUNT(*) > 300000
   ORDER BY 1 DESC)
select v.sql_id,
       replace(v.sql_text, '''', chr(38) || 'apos;') sql_text,
       v.module,
       v.parsing_schema_name,
       s.cnt hard_parses,
       'FALSE' STATUS
  from v$sqlarea v,
       (SELECT /*+ materialize */
         (SELECT a.sql_id
            FROM v$sqlarea a
           where a.plan_hash_value = t.plan_hash_value
             and rownum <= 1) sql_id,
         t.cnt
          FROM T
         where t.plan_hash_value <> 0) s
 where s.sql_id = v.sql_id
   and v.MODULE = 'JDBC Thin Client'
```

## 失效索引查询

<span id="query_invalid_index"></span>

```sql
SQL> SELECT A.OWNER, A.INDEX_NAME, I.TABLE_NAME
  FROM (SELECT DISTINCT INDEX_NAME, INDEX_OWNER OWNER
           FROM DBA_IND_PARTITIONS T2
          WHERE T2.STATUS NOT IN ('USABLE', 'N/A')
            AND INDEX_OWNER NOT IN ('SYSTEM',
                                    'SYS',
                                    'OLAPSYS',
                                    'XDB',
                                    'PUBLIC',
                                    'OUTLN',
                                    'DBSNMP')
         UNION ALL
         SELECT INDEX_NAME, OWNER
           FROM DBA_INDEXES T
          WHERE T.PARTITIONED = 'NO'
            AND STATUS <> 'VALID'
            AND OWNER NOT IN ('SYSTEM',
                              'SYS',
                              'OLAPSYS',
                              'XDB',
                              'PUBLIC',
                              'OUTLN',
                              'DBSNMP')
         UNION ALL
         SELECT DISTINCT INDEX_NAME, INDEX_OWNER OWNER
           FROM DBA_IND_SUBPARTITIONS S
          WHERE S.STATUS <> 'USABLE'
            AND INDEX_OWNER NOT IN ('SYSTEM',
                                    'SYS',
                                    'OLAPSYS',
                                    'XDB',
                                    'PUBLIC',
                                    'OUTLN',
                                    'DBSNMP')) A,
        DBA_INDEXES I
 WHERE A.INDEX_NAME = I.INDEX_NAME
   AND A.OWNER = I.OWNER
```

## 获取SQL执行计划

### 获取方法

```sql
DBMS_XPLAN.DISPLAY_CURSOR(
   sql_id           IN  VARCHAR2  DEFAULT  NULL,
   cursor_child_no  IN  NUMBER    DEFAULT  0, 
   format           IN  VARCHAR2  DEFAULT  'TYPICAL');
```

举例：

```sql
SQL> SELECT *
  FROM TABLE(DBMS_XPLAN.DISPLAY_CURSOR('3MKN9T70FQ6C6', NULL, 'ADVANCED'));
```

## 统计信息的采集方式

通过ZMC对表统计信息的采集，一周一次。

### 执行语句

单表方法：

```sql
SQL> BEGIN
        DBMS_STATS.GATHER_TABLE_STATS(ownname          => '<owner>',
                                 tabname          => '<table name>',
                                 DEGREE           => 6,
                                 method_opt       => 'for all indexed columns size auto', 
                                 CASCADE          => TRUE,
                                 ESTIMATE_PERCENT => 10,
                                 no_invalidate    => false);
end;
```

自动收集脚本：

### 非分区索引

```sql
SQL> alter index <index name> rebuild online parallel 4;

SQL> alter index <index name> noparallel;
```

## 获取AWR报告

<span id = "generate_awr"></span>

[如何获取AWR报告](https://docs.iwhalecloud.com/dmz-proxy/cos/download/406/规范附件/数据库/Database_operation_Oracle_如何生成ORACLE_AWR报告V1.0.doc)

## 如何阅读AWR报告

<span id ="read_awr"></span>

[如何阅读AWR报告](https://docs.iwhalecloud.com/dmz-proxy/cos/download/406/规范附件/数据库/Database_operation_Oracle_AWR的关注点.docx)

## 获取ASH报告

<span id ="generate_ash"></span>

[获取ASH报告](https://docs.iwhalecloud.com/dmz-proxy/cos/download/406/规范附件/数据库/Database_operation_Oracle_如何生成ORACLE_ASH报告V1.0.doc)

## 获取ADDM报告

<span id = "generate_addm"></span>

[获取ADDM报告](https://docs.iwhalecloud.com/dmz-proxy/cos/download/406/规范附件/数据库/Database_operation_Oracle_如何生成ORACLE_ADDM报告V1.0.doc)

## 表碎片整理方法

### 表碎片整理方案

#### ALTER TABLE MOVE 方法[不推荐]

语法：

非分区表：

```sql
ALTER TABLE <table name> MOVE;
```

分区表：

```sql
alter table  <table name> move partition <partition name>  update indexes;
```

需要对表进行索引重建：

```sql
ALTER INDEX <index name> REBUILD ONLINE 
```

缺点：会锁表，表上的索引会失效，适合停应用的情况下使用

#### 使用 shrink

整理表的碎片降低高水位：

```sql
Alter Table <table name> Enable Row Movement;
Alter Table <table name> shrink space compact;
Alter Table <table name> shrink space;
Alter Table <table name> Disable Row Movement;
```

索引重建一下：

```sql
ALTER INDEX <index name> REBUILD ONLINE;
```

特点：碎片整理效果不如 MOVE 表空间的方法好，而且耗时，但是不会锁表,索引不会失效

#### TRUNCATE表

<span id="truncate_table"></span>

先将表中数据备份出来，然后对表做一次 TRUNCATE 操作，再将表中数据重新导入。

非分区表：

```sql
SQL>TRUNCATE Table  <table name>;
```

分区表：

- 有全局索引

```sql
SQL> alter table <table name > truncate partition <partition name> update global indexes;
```

- 无全局索引

```sql
SQL> alter table <table name > truncate partition <partition name>;
```

## 索引重建方法

<span id = "rebuild_index"></span>

### 分区索引

分区索引需要按分区进行重建：

```sql
SQL> alter index <index name> rebuild partition <partition name> online parallel 4;

SQL> alter index <index name> noparallel;
```

### 分区表分区交换

<span id = "exchange_partition"></span>

2. 检查表上是否存在非分区索引：

```sql
SQL> select u.table_name, u.index_name
      from user_indexes u
      where 1 = 1
   and not exists
 (select 1 from user_part_indexes p where p.index_name = u.index_name) and u.table_name = upper(< table name >)
```

​    2.创建与分区表表结构一样的目标表。

*[注]不建议用【CREATE AS SELECT】方式建表，这种方式原表字段默认值无法带过来。*

​    3.目标表上创建与分区表分区索引结构一样的索引（全局索引无需创建）：

```sql
SQL> create index <target index name>   on <table name> (column name) tablespace
<tablespace name>
```

​     4.执行分区交换命令。

- 有全局索引：（**表上数据量较大时不可使用会阻塞DML）**

```sql
SQL> alter table <table name > exchange
partition <partition name> with table <target table name> INCLUDING
INDEXES update global indexes;
```

- 无全局索引：

```sql
SQL> alter table <table name > exchange
partition <partition name>) with table <target table name>
INCLUDING INDEXES;
```

## 分区表TRUNCATE分区

<span id="truncate_partition"></span>

1. 检查表上是否存在非分区索引：

```sql
SQL> select u.table_name, u.index_name
      from user_indexes u
      where 1 = 1
   and not exists
 (select 1 from user_part_indexes p where p.index_name = u.index_name) and u.table_name = upper(< table name >)
```

​        2.执行TRUNCATE 分区命令。

- 有全局索引：**（表上数据量较大时不可使用会阻塞DML）**

```sql
SQL> alter table <table name > truncate partition <partition name>  update global indexes;
```

- 无全局索引：

```sql
SQL> alter table <table name > truncate partition <partition name>
```

## 使用SQL PROFILE固定SQL语句的执行计划

<span id="use_profile_fix_execute_plan"></span>

[使用SQL PROFILE固定SQL语句的执行计划](https://docs.iwhalecloud.com/dmz-proxy/cos/download/406/规范附件/数据库/Database_operation_Oracle_使用SQL_PROFILE固定SQL语句的执行计划.docx)

## 查询Active Session中TOP CPU的进程会话信息

SQL语句：

```sql
SQL> SELECT B.USERNAME,
        b.SID,
        b.serial#,
        b.LAST_CALL_ET,
        a.SQL_ID,
        a.SQL_TEXT,
        a.sql_fulltext,
        b.BLOCKING_INSTANCE,
        b.BLOCKING_SESSION,
        b.EVENT "事件",
        a.executions "执行次数",
        round(((a.cpu_time / decode(a.executions, 0, 1, a.executions)) /
              1000000),
              6) "CPU_TIME/EXEC(S)",
        round(((a.ELAPSED_TIME / decode(a.executions, 0, 1, a.executions)) /
              1000000),
              6) "ELAPSED_TIME/EXEC(S)",
        round(cpu_time / 1000000) cpu_time,
        round(a.ELAPSED_TIME / 1000000) ELAPSED_TIME,
        a.DISK_READS,
        round(((a.DISK_READS / decode(a.executions, 0, 1, a.executions)) /
              1000000),
              6) "DISK_READS/EXEC(S)",
        a.BUFFER_GETS,
        round(((a.BUFFER_GETS / decode(a.executions, 0, 1, a.executions)) /
              1000000),
              6) "BUFFER_GETS/EXEC(S)",
        b.MACHINE,
        b.PROGRAM,
        p.spid,
        'alter system kill session ' || '''' || b.sid || ',' || b.serial# || '''' ||
        ' immediate ;' "instance kill session",
        'kill -9 ' || p.spid kill,
        'ps -ef|grep ' || p.spid ps
  From v$sqlarea a, v$session b, v$process p, v$transaction t
 Where a.SQL_ID = b.SQL_ID
   and b.paddr = p.addr
   and b.TADDR = t.ADDR(+)
   and b.status = 'ACTIVE' Order By "CPU_TIME/EXEC(S)" desc;
```

"CPU_TIME/EXEC(S)" – 单次执行所需CPU时长

"ELAPSED_TIME/EXEC(S)" - 单次执行所需时长

"DISK_READS/EXEC(S)" – 单次物理读

"BUFFER_GETS/EXEC(S)" – 单次逻辑读

"instance kill session" - 杀会话的语句，可以执行这个杀掉消耗资源的SQL

样例：

![image](uploads/4062/df95667b-fcd9-4ebe-adb3-0bc340c711cb/1620290117846.png)

## 如何重建表（案例）

<span id ="rebuild_table"></span>

参考步骤：

1. 创建新表，表结构与原表一致。

不要使用CREATE TABLE AS SELECT \* FROM 方式进行创建。

2.使DML语句并行运行：

```sql
SQL> alter session enable parallel dml;
```

3.导入数据到新表中。

4.在新表上创建索引。

- 修改原表索引名为其他名字：

```sql
SQL> alter index <index name> rename to <other index name>;
```

- 创建索引：

```sql
SQL> create index <index name> on <new table> (<column_name>) 
tablespace <tablespace name> parallel (degree 6) nologging;
```

- 改索引为LOGGING 模式 并去除索引的并行度：

```sql
SQL> alter index <index name> noparallel;
SQL> alter index <index name> logging;
```

​     5.新表做表分析。

注意：如果新表无需导入原表数据或者导入的数据极少（几百条左右），请不要做表分析，不然SQL会走全表扫描，当表数据量增长上去后 SQL 性能就逐渐下降：

```sql
SQL> EXEC DBMS_STATS.GATHER_TABLE_STATS(ownname
=>'<user name>', tabname =>'<new_table_name>', DEGREE=>6,
CASCADE=>TRUE,ESTIMATE_PERCENT=>
DBMS_STATS.AUTO_SAMPLE_SIZE,no_invalidate => false);
```

​      6.去除原表上的外键和与他主键关联它表上的外键。

执行下面SQL 生成去除表上外键和与其主键相关的他表外键：

```sql
SQL> select 'alter table ' || table_name || ' drop constraint ' ||
        constraint_name || '; ' as v_sql
  from user_constraints
 where constraint_type in ('r')
   and owner = upper(< user name >)
   and upper(table_name) in (< table name >)
union all
select 'alter table ' || a.table_name || ' drop constraint ' ||
        a.constraint_name || '; ' as v_sql
  from user_constraints a, user_constraints b
 where a.owner = upper(< user name >)
   and a.owner = b.owner
   and a.r_owner = b.owner
   and b.table_name = upper(< table name >)
and a.r_constraint_name = b.constraint_name;
```

​       7.更换表名（rename 方式）：

```sql
SQL> rename <table name> to <other table name>;

SQL> rename <new table> TO <table name>;
```

​        8.补捞数据。

在第三步插数据完成后到rename表名这段时间可能还会有新数据进入原表，所以需要补捞一下这部分新数据。

​        9.其他（如有）：

- 重建触发器；

- 添加权限；

- 观察应用是否正常，如果发生应用报错，需要重启应用程序。

  ## RAC状态检查（案例）

### 检查集群状态

<span id="check_cluster_state"></span>

```
命令：crsctl check cluster

样例：

[grid@rac1 \~]\$ crsctl check cluster

CRS-4537: Cluster Ready Services is online

CRS-4529: Cluster Synchronization Servicesis online

CRS-4533: Event Manager is online
```

### 所有Oracle实例（数据库状态）

```
命令：srvctl status database -d database_name

样例：

[grid@rac1 \~]\$ srvctl status database -d CC

Instance CC is running on node rac1

Instance CC is running on node rac2
```

### 检查单个实例状态

<span id="check_oracle_instance_state"></span>

```
命令：srvctl status instance -d database_name -i instance_name
[，instance_name-list]

样例：

[grid@rac1 \~]\$ srvctl status instance -CC -i CC1

Instance CC1 is running on node rac1

[grid@rac1 \~]\$
```

## Oracle启停和切换操作

### Newstart HA启停数据库

<span id="newstart_start_stop_database"></span>

用 cli 命令进入到双机命令行界面

service-stop：停止资源组

service-start：启动资源组

service-migrate：切换资源组

以下是操作示例：

```
cli:~> service-migrate

Do you want to migrate all services on some node? (yes/no) [no]

Current service(s):

0) oraservice

1) cancel

Select a service: 0

Please select the destination node.

Current node(s):

0) clusternode2

1) cancel

Select a node to do: 0

Migrated service oraservice from clusternode1 to clusternode2 successful.
```

### VCS启停数据库

<span id="vcs_start_stop_database"></span>

查看 vcs 的总体概况：

```
hastatus –sum
```

停止 sg_cc 服务组(假设数据库资源组名为sg_cc,运行在ocs1主机)：

```
hagrp -offline sg_cc -sys ocs1
```

启动sg_cc服务组：

```
hagrp -online sg_cc -sys ocs1
```

切换sg_cc服务组，将数据库切换至ocs2主机：

```
hagrp -switch sg_cc -to ocs2
```

### Power HA启停数据库

<span id="powerha_start_stop_database"></span>

查看双机状态：

首先，可以用/usr/es/sbin/cluster/utilities/cldump 或者 /usr/sbin/cluster/clstat
命令进行双机状态的查看。

其次可以通过smit hacmp进行双机状态的查看

Smitty hacmp -> Problem Determination Tools -> View Current State

![image](uploads/4062/56976a8d-e03a-452c-a1c9-188114ed48cd/1620290382738.png)

![image](uploads/4062/a5f674e2-ecc3-40dd-a7f6-b8b80abe1dde/1620290392385.png)

停止资源组，使用smit工具进行操作：

smit hamcp -\> System Management (C-SPOC) -\> HACMP Resource Group and
Application Management -\> Move a Resource Group to Another Node / Site -\>
bring a resource group offline

然后选择对应的资源组进行停止数据库操作

启动资源组，使用smit工具进行操作：

smit hamcp -\> System Management (C-SPOC) -\> HACMP Resource Group and
Application Management -\> Move a Resource Group to Another Node / Site -\>
bring a resource group online

然后选择对应的资源组和主机进行数据库启动操作

切换资源组，使用smit工具进行操作：

smit hamcp -\> System Management (C-SPOC) -\> HACMP Resource Group and
Application Management -\> Move a Resource Group to Another Node / Site -\> Move
a Resource Group to Another Node / Site -\> Move Resource Groups to Another Node

操作示例如下：

![image](uploads/4062/c2b3ddb8-910d-4ebb-aa22-9b2db759c2a4/1620290440895.png)

![image](uploads/4062/f24c5dfe-85be-4821-bef5-b6d5631731be/1620290447444.png)

![image](uploads/4062/96f03164-f65b-453c-ab7c-5ac7b34f5995/1620290453551.png)

## Oracle备份检查

### 逻辑备份检查

<span id="check_logic_backup"></span>

数据库备份定时任务部署在root用户下，查看定时任务从而确认执行的脚本。

如下定时任务：

```
0 2 * * * su - oracle -c "/expcc/shell/exp_db.sh cc/smart@cc /expcc/cc cc"
```

则备份文件和备份日志保存在/expcc/cc目录下（具体目录以实际项目为准）

查看备份文件是否正常生成，文件大小和之前是否差不多。

![image](uploads/4062/561dd4ff-c54f-41e0-9546-2bd7a9e2c487/1620290489557.png)

检查备份日志，如有successfully completed字样则表明备份成功。

```
[root@cheli bak]# tail -f expdp_cc_cc_20200212.log

Processing object type SCHEMA_EXPORT/TABLE/CONSTRAINT/CONSTRAINT

. . exported "CC"."EXCLUDE_TABLE"                        5.148 KB       8 rows

. . exported "CC"."AOLD"                                     0 KB       0 rows

. . exported "CC"."P_Da"                                     0 KB       0 rows

. . exported "CC"."P_Ma"                                     0 KB       0 rows

Master table "CC"."SYS_EXPORT_SCHEMA_01" successfully loaded/unloaded

******************************************************************************

Dump file set for CC.SYS_EXPORT_SCHEMA_01 is:

  /soft/oradata/bak/expdp_cc_cc_20200212.dmp

Job "CC"."SYS_EXPORT_SCHEMA_01" successfully completed at Wed Feb 12 14:35:50 2020 elapsed 0 00:00:33
```

### RMAN备份检查

<span id="check_rman_backup"></span>

```
0 3,9,15,21 * * * su - oracle -c "/rmancc/shell/rmandb.sh" 1>>/rmancc/shell/rmandb.log 2>>/rmancc/shell/rmandb.err

0 * * * * su - oracle -c "/rmancc/shell/rmanlog.sh" 1>>/rmancc/shell/rmanlog.log

2>>/rmancc/shell/rmanlog.err
```

### 全库备份

<span id="check_full_backup"></span>

查看备份定时任务获取备份脚本路径,标红处为备份文件路径，检查备份文件是否正常生成：

```
cat /rmancc/shell/rmandb.sh

\#! /bin/sh

export ORACLE_SID=cc

rman target / <<EOF

run {

allocate channel 'dev1' type disk;

backup incremental level 0 tag 'dbL0' format '/rmancc/cc/%d_Incr0_%T_%s_%u' database INCLUDE CURRENT CONTROLFILE;

sql 'alter system archive log current' ;

backup format '/rmancc/%d_log_%T_%U' archivelog all delete all input;

release channel 'dev1';

}

quit;

EOF
```

检查全库备份文件，文件命名格式一般为 {实例名}_Incr0_{日期}\_{自动生成的编号}：

![image](uploads/4062/73f9366f-3247-4fb5-bb99-8d5bb4af7303/1620290547605.png)

检查全库备份日志，从定时任务中获取日志路径：

```
tail -f /rmancc/shell/rmandb.log
Finished backup at 12-FEB-20
released channel: dev1
RMAN> 
Recovery Manager complete.
```

如有Recovery Manager complete，说明备份正常，否则查看日志/rmancc/shell/rmandb.err

### 归档备份

<span id="check_archive_backup"></span>

查看备份定时任务获取备份脚本路径,标红处为备份文件路径，检查备份文件是否正常生成：

```
cat /rmancc/shell/rmanlog.sh

\#! /bin/sh

export ORACLE_SID=cc

rman target / <<EOF

run{

sql 'alter system archive log current' ;

backup format '/rmancc/cc/%d_log_%T_%U' archivelog all delete all input ;

delete noprompt obsolete;

}

quit;

EOF
```

检查归档备份文件，命名规则一般为 {实例名}_log_{日期}_{自动生成编号}

![image](uploads/4062/4b6dfb15-7ad4-4400-add4-1d9c5c120d74/1620290604727.png)

检查归档备份日志：

```
tail -f /rmancc/shell/rmanlog.log

using channel ORA_DISK_1

no obsolete backups found

 

RMAN> 

 

Recovery Manager complete.
```

如有Recovery Manager complete，说明备份正常，否则查看日志/rmancc/shell/rmanlog.err

## Dataguard状态查询

### 数据库角色查询

<span id ="query_database_role"></span>

主库状态应该为：

```
SQL> select database_role from v$database;

DATABASE_ROLE

----------------

PRIMARY
```

备库状态应该为：

```
SQL> select database_role from v$database;

DATABASE_ROLE

----------------

PHYSICAL STANDBY
```

### 查看数据库进程

<span id ="check_database_process"></span>

主库进程示例：

```
SQL>  select process,block#,blocks ,status ,sequence# from v$managed_standby;

PROCESS       BLOCK#     BLOCKS STATUS        SEQUENCE#

--------- ---------- ---------- ------------ ----------

ARCH               1          1 CLOSING              45

ARCH               0          0 CONNECTED             0
```

主库中ARCH进程传送日志到备库。

备库进程示例：

```
SQL>  select process,block#,blocks ,status ,sequence# from v$managed_standby;

PROCESS       BLOCK#     BLOCKS STATUS        SEQUENCE#

--------- ---------- ---------- ------------ ----------

ARCH               0          0 CONNECTED             0

ARCH               0          0 CONNECTED             0

MRP0               0          0 WAIT_FOR_LOG         48

RFS                0          0 IDLE                  0
```

备库中，RFS进程负责接收主库传过来的日志，MRP0进程负责将日志写入备库。

### 查看归档日志传送情况

<span id ="check_archive_log_transfer"></span>

进入主备库所在服务器的归档目录，一般为/archcc，查看归档日志。

主库：

![image](uploads/4062/1cfb31f2-4bd5-41cf-9749-199bf302cdb9/1620290682985.png)

备库：

![image](uploads/4062/5a25185c-4d06-48ec-ac63-8122ea565acc/1620290689234.png)

若最新的归档日志在备库归档目录中没有，说明日志传送有问题。

### 查看日志应用情况

<span id="check_log_application"></span>

使用dba用户登录备库

export ORACLE_SID=cc

sqlplus ‘/as sysdba’

查看日志应用情况

```sql
SQL> select
RECID,NAME,THREAD#,SEQUENCE#,ARCHIVED,APPLIED,DELETED,STATUS,CREATOR,REGISTRAR
from v$archived_log where applied='YES';
```

![image](uploads/4062/5dd8e731-62f9-472c-b6d8-22b2820873f2/1620290731840.png)

和上一章节检查归档日志对比，1_48_1031680564.dbf归档已经成功在备库被应用，说明dataguard是同步的。

## 表字段长度使用率检查

<span id="query_field_length_usage"></span>

**创建FUNCTION**

```sql
CREATE OR REPLACE FUNCTION "FUNC_CHECK_COLUMN_RATIO"(v_col_name in varchar2, v_tab_name in varchar2)
  return integer is
  v_result         integer;
  v_cur_namx_value number(20);
  v_sql            varchar(100);
begin
  v_sql := 'select max(' || v_col_name || ') from ' || v_tab_name;
  execute immediate v_sql
     into v_cur_namx_value;
  v_result := v_cur_namx_value;
```

**执行SQL**

```sql
 with t as
 (select /*+ MATERIALIZE */
   b.COLUMN_NAME,
   b.TABLE_NAME,
   nvl(FUNC_CHECK_COLUMN_RATIO(b.COLUMN_NAME, b.TABLE_NAME), 0) /
   substr('99999999999999999999999999', 0, b.DATA_PRECISION) v_use_radio
     from user_indexes s, user_ind_columns a, user_tab_columns b
   where s.index_type = 'NORMAL'
      and s.index_name = a.INDEX_NAME
      and a.COLUMN_POSITION = 1
      and a.COLUMN_NAME = b.COLUMN_NAME
      and s.table_name = b.TABLE_NAME
      and b.DATA_TYPE = 'NUMBER'
      and b.DATA_SCALE = 0
      and b.DATA_PRECISION is not null
      and s.index_name in (select index_name
                             from (select count(1) v_total, INDEX_NAME
                                     from user_ind_columns
                                    group by INDEX_NAME
                                   having count(1) <= 2))
      AND s.TABLE_NAME NOT LIKE 'BIN$%'
      AND s.TABLE_NAME NOT LIKE 'TMP/_%' escape '/'
      AND s.TABLE_NAME NOT LIKE 'TEMP/_%' escape '/'
      AND s.TABLE_NAME NOT LIKE 'BAK/_%' escape '/'
      AND s.TABLE_NAME NOT LIKE '%DWH%'
      AND s.TABLE_NAME NOT LIKE '%BAK'
      AND s.TABLE_NAME NOT LIKE 'SO/_%' escape '/'
      AND s.TABLE_NAME NOT LIKE 'P_D/_%' escape '/'
      AND s.TABLE_NAME NOT LIKE 'P_M/_%' escape '/'
      AND s.TABLE_NAME NOT LIKE 'MIG/_%' escape '/'
      AND s.TABLE_NAME NOT LIKE 'TEMABR_SUBS_INFO/_%' escape '/'
      AND NOT REGEXP_LIKE(s.TABLE_NAME, '[[:digit:]]'))
select * from T where v_use_radio > 0.8
```

## 序列(sequence)使用率检查

<span id="query_sequence_usage"></span>

```sql
SELECT A.SEQUENCE_NAME,
        A.MAX_VALUE,
        A.LAST_NUMBER,
        LENGTH(A.MAX_VALUE),
        LENGTH(A.LAST_NUMBER),
        ROUND(A.LAST_NUMBER / A.MAX_VALUE, 2) * 100 COL_1,
        DECODE(trunc((ROUND(A.LAST_NUMBER / A.MAX_VALUE, 2)) * 100 / 80),
               0,
               'normal',
               'warning') status,
        round((A.LAST_NUMBER / A.MAX_VALUE) * 100, 2) "percent%"
  FROM USER_SEQUENCES A
 WHERE LENGTH(A.MAX_VALUE) - LENGTH(A.LAST_NUMBER) <= 1
   and CYCLE_FLAG = 'N'
```

# SQL开发规范

内容详见 [SQL开发规范(Oracle分册)](/didc7db6N.md) 。

# 本文件评审、修正记录

| 文件名称 | 数据库运维规范 – Oracle分册 |                      |            |        |
| -------- | --------------------------- | -------------------- | ---------- | ------ |
| 序号     | 流程                        | 拟制人/审核人               | 审核时间   | 版本号 |
| 1        | 编写                        |韩国富，陆文龙，王可心，数据库规范组 | 2020/01/13 | V0.1   |
| 2        | 评审、修订                  | 王可心，数据库规范组 | 2020/03/26 | V0.2   |
| 3        | 评审、修订、标准化          | 王为，数据库规范组 | 2020/04/02 | V0.3   |
| 4        | 评审、修订、标准化          | 王可心，数据库规范组 | 2020/06/28 | V1.0   |
| 5        | 修改5.6章节代码块错误       | 王为，数据库规范组 | 2021/09/30 | V1.01   |
| 6        | 发布       | 数据库规范组 | 2021/12/30 | V1.1  |
| 7        | 增加章节，引用SQL开发规范       | 朱颖 | 2022/06/02 | V1.1.1  |
| 8        | 发布     | 数据库规范组 | 2022/06/14 | V1.2  |
| 9        | 增加强制规范条款检查方式     | 王为 | 2025/11/19 | V1.2.1  |
| 10        | 发布     | 数据库规范组 | 2025/12/23 | V1.3  |
