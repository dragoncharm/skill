![image](uploads/121313/67eb91d4-c3be-49a7-b897-14bbb1a6a972/image.png)

# 概述

## 前言

本文规定了浩鲸科技数据库模型设计的规范，并明确各角色的工作职责。随着本规范的发布，参考文章《数据模型设计规范及脚本管理流程V1.0》中有关数据库的设计的规定不再有效，以本文为准。

## 编写目的

本文用于指导浩鲸科技运维人员进行PostgreSQL数据库运维的安全操作。

## 适用范围

浩鲸科技所有使用PostgreSQL数据库的项目，适用版本：PG 9.4版本及以后。

## 角色和职责

1.运维人员: 参考文档对项目数据库进行运维。

2.DBA : 负责运维文档的更新并对运维人员进行技术赋能

# PostgreSQL运维规范

### 表维护

#### 死亡元组清理

死亡元组产生原因：在 PostgreSQL 中，由于 MVCC（多版本并发控制）机制和写入操作的特性，会导致数据在磁盘上存在死亡元组。某些表被用作接口表，经常有数据插入和删除操作，这类表每天的数据插入和删除量较大，导致表中的已删除行（即已被标记为  删除但尚未被真正清理的行）数量很大。由于频繁插入和删除，这些表的大小会迅速增大，而且由于死亡元组的存在，扫描表数据时经常需要进行全表扫描，增加了全表扫描的数据量，影响了执行计划的效率。因此，对于这些表，需要定期清理死亡元组。

【$\color{#ff0000}强制$】禁止在业务高峰期通过vacuum操作进行清理。

#### 分区表

##### 强制分区

【$\color{008000}推荐$】单表记录过千万或超过100GB的量级必须对使用分区表。

检查方式：人工检查

##### 分区数量维护

【$\color{008000}推荐$】按时间分区数量不做限制但是需要定期清理或者转存数据，Hash分区数量建议不超过4个

检查方式：人工检查

##### 分区表删除/清理

【$\color{008000}推荐$】 使用ALTER TABLE tablename drop PARTITION ... 命令来删除/清理分区表

#### 清理临时表

大量无用表会浪费很多存储空间，会导致相关系统视图的查询变慢，会增加数据库备份的时间等，所以必须要将这些表从系统中清理出去。

临时表指的是：

1. 人为创建的一些非应用系统所需要的表，并且不需长期保留的表；
2. 应用系统自己主动生成的一些表，并且有效期很短。

检查方式：人工检查

##### 应用创建的临时表

【$\color{008000}推荐$】应用中创建的临时表由应用自行维护。

检查方式：人工检查

##### 运维人员所建临时表

【$\color{008000}推荐$】运维人员手工创建的临时表，在确定无需保留的情况下，应及时进行清理。

检查方式：人工检查

#### DDL语句执行规范

【$\color{008000}推荐$】部分语句操作需要申请执行窗口时间，停应用执行。

【$\color{#ff0000}强制$】禁止在系统忙时执行，应选择系统最闲时执行，并提前通知客户，得到客户许可。

#### DML语句执行规范

【$\color{#ff0000}强制$】禁止在线对表中大批量数据（>10000条）直接进行update/delete 操作。

【$\color{008000}推荐$】选择系统闲时对所需要update/delete的海量数据，分成多批次操作和提交。

检查方式：人工检查

### 索引维护

#### 重建索引

满足以下条件的需要索引重建，重建索引会阻塞DML操作，不允许在系统繁忙时重建，请在系统闲时操作,需要申请操作时间窗口进行操作。

【注意事项】

1. 不可以在系统忙时重建索引，尤其是事务访问繁忙的表；
2. 重建过程中不可以强制中断重建过程；
3. 重建操作不要通过客户端去执行，请远程到服务器端执行，防止由于网络问题导致连接中断；
4. 在线建立普通索引可以加 concurrently参数否则会阻塞访问索引所在表的事务。

#### 索引碎片整理

【$\color{008000}推荐$】 索引碎片整理是维护索引性能的重要一部分。在操作窗口或者业务低峰期使用 REINDEX 命令来重新构建普通索引，以去除索引中的碎片并提高查询性能。

```sql
REINDEX { INDEX } [CONCURRENTLY] name ;
```

#### 索引监控

【$\color{008000}推荐$】来检查索引的使用情况（建议不超过4个）,可以优化和删除不必要的索引，业务运行正常可以不需要进行清理。

```sql
SELECT relname AS index_name, idx_scan AS scan_count FROM pg_stat_user_indexes ORDER BY idx_scan DESC;
```

检查方式：人工检查

### 数据库权限

#### 用户和密码权限

【$\color{#ff0000}强制$】为每个用户设置满足密码复杂度的密码。

【$\color{008000}推荐$】每个用户的密码需要定期更换。

【$\color{008000}推荐$】定期定理不需要的用户

【$\color{#ff0000}强制$】禁止授予普通用户super权限

#### 访问权限

【$\color{#ff0000}强制$】pg_hba.conf配置认证方式不能使用trust。

【$\color{#ff0000}强制$】超级用户只允许从本地连接，不允许从网络连接。

【$\color{#ff0000}强制$】业务用户访问配置库禁止使用all

### 数据库指标优化

#### 慢SQL监控

在 PostgreSQL 中监控慢 SQL 可以帮助识别数据库性能瓶颈和优化查询，可以修改配置来获取慢SQL。

【$\color{008000}推荐$】 通过修改 PostgreSQL 参数，启用慢查询日志记录。可以设置慢查询的阈值时间，以便记录执行时间超过该阈值的 SQL 查询。

```sql
##查看是否开始慢SQL
show log_statement;
##开启慢SQL
alter system set log_statement='ddl'
#OLTP情况下 超过100毫秒即为慢
#产品SQL慢SQL时间可放大至几秒
alter system set log_min_duration_statement='100'; ## 记录300 毫秒以上的慢SQL$
pg_ctl restart -D 数据库目录的绝对路径
```

检查方式：人工检查

#### 采集更新统计信息

在 PostgreSQL 中，数据库中绝大多数表的数据都在不停的进行变化，尤其数据量的变化比较大，表的执行计划可能由于统计信息不准确 或过期，优化器可能会做出错误的选择，查询未能走最佳的性能导致查询时间变长。

【$\color{#ff0000}强制$】 可以配置定时脚本对相关大表进行统计信息更新。

```sql
vacuum schemaname.tablename;
```

检查方式：工具检查

#### 表年龄采集

PostgreSQL 使用事务 ID 来跟踪事务，当事务 ID 耗尽时，会导致数据库无法继续运行。老化表中的过时数据可能会增加事务的数量，加速事务 ID 的耗尽。因此，为了维护 PostgreSQL 数据库的性能和稳定性，建议定期检查并清理老化表，以确保数据库保持在一个健康的状态。

【$\color{008000}推荐$】表年龄超过 1000000000需要人为进行干预。

```sql
SELECT relname AS table_name, n_live_tup AS live_rows, n_dead_tup AS dead_rows, last_vacuum AS last_vacuum_time, last_autovacuum AS last_autovacuum_time, last_analyze AS last_analyze_time, last_autoanalyze AS last_autoanalyze_time FROM pg_stat_user_tables WHERE n_live_tup > 1000000000 -- 大于10亿行 ORDER BY relname; 
```

检查方式：人工检查

#### 表膨胀处理

在 PostgreSQL 中，由于 MVCC（多版本并发控制）机制和写入操作的特性,表中存在大量过时或无用数据，导致数据库性能下降和磁盘空间占用增加的情况。

【$\color{008000}推荐$】收集死亡元组数量,建议对多死亡元组的表进行清理。

```sql
SELECT relname AS table_name,n_live_tup AS live_rows,n_dead_tup AS dead_rows,CASE WHEN n_live_tup > 0 THEN (n_dead_tup * 100.0) / n_live_tup ELSE 0 END AS bloat_ratio_percentFROM pg_stat_user_tablesORDER BY bloat_ratio_percent DESC;
```

检查方式：工具检查

#### 归档处理

在 PostgreSQL 中，要保持归档开启，通常需要配置 **`archive_mode`** 和 **`archive_command`** 参数，确保日志归档功能正常运行。

#### 归档清理

归档日志（WAL）会随着时间的推移不断积累，因此需要定期清理归档目录，以防止存储空间被占满。

```sql
archive_cleanup_command = 'find /pgdata/pg_archives/ -type f -name "*.backup" -mtime +7 -exec rm {} \;'
```

#### 主备参数检查

在读写分离的业务场景中，部分主备可能存在较大延迟，需要对参数hot_standby_feedback进行开启，帮助保持主库和从库之间的数据一致性，因为防止了主库过早清理对从库仍然重要的数据。

```sql
alter system set hot_standby_feedback = on;
```

检查方式：工具检查

#### 长事务检查

```sql
SELECT 
    pid, 
    usename, 
    application_name, 
    backend_start, 
    xact_start, 
    state, 
    now() - xact_start AS transaction_duration, 
    query 
FROM pg_stat_activity
WHERE state = 'active' 
  AND xact_start IS NOT NULL
  AND now() - xact_start > interval '10 minutes'
ORDER BY transaction_duration DESC;
```

检查方式：人工检查

#### 锁等待检查

```sql
SELECT 
    a.pid,
    a.usename,
    a.query,
    a.state,
    a.query_start,
    l.mode,
    l.granted
FROM 
    pg_stat_activity a
LEFT JOIN 
    pg_locks l ON a.pid = l.pid
WHERE 
    a.state = 'active'
ORDER BY 
    a.query_start;
```

检查方式：人工检查

#### 备份管理

#### 逻辑备份及还原

备份说明: 可备份为二进制、sql 文件、只备份单表、只备份表结构、只备份数据等，根据实际需求进行备份。工具可直接看到选项，命令行使用 pg_dump --help 进行选择。

还原说明：可单独还原某张表、某个表结构、某份数据，根据实际需求进行还原。工具可以直接看到选项，命令行使用 pg_restore --help 进行选择。新环境还原需提前建好原有的数据库用户。

#### 物理备份

备份说明：pg_basebackup支持在线备份，需要确保备份目录有足够的存储空间，物理备份需要一些时间，具体耗时取决于数据库的大小和系统性能。

还原说明：支持本机和异机还原，解压备份文件至指定目录，启动数据库即可。

备份参数：

-F：指定备份文件的格式，可选值为p（普通模式）或t（tar归档模式）。

-z：启用备份文件的压缩。

-P：显示进度信息。

-c：在备份期间允许继续数据库连接。

#### 备份类型选择

pg_dump的备份参数：
-u：username（用户名）
-p：port（端口）
-s：schema-only（仅结构）
-a：data-only（仅数据）
-d：dbname（库名）
-f：filename（导出的文件名）

##### 表级别备份

```sql
table备份
pg_dump -u username -p port -t schamaname.tablename -d databasename -f /pgdata/data/xxx.txt
table备份(仅表结构)
pg_dump -u username -p port -s -t schamaname.tablename -d databasename -f /pgdata/data/xxx.txt
```

##### 模式级别备份

```sql
schema备份
pg_dump -u username -p port -n schamaname -d databasename -f /pgdata/data/xxx.txt
schema备份（仅结构）
pg_dump -u username -p port -s -n schamaname -d databasename -f /pgdata/data/xxx.txt
```

##### 库级别备份

```sql
database备份
pg_dump -u username -p port  databasename -f /pgdata/data/xxx.txt
database（仅结构）
pg_dump -u username -p port -s databasename -f /pgdata/data/xxx.txt
```

##### 实例级别备份

```shell
##推荐pgbasebackup(恢复速度分钟级)
date=`date +"%Y%m%d"`
pg_basebackup -U ${username} -p ${port} -D ${backupdir}/${date} -Ft -z -P
```

### 高危操作

**【$\color{#ff0000}强制$】严禁修改数据目录下文件名，权限，内容不得修改和删除**

说明：postgresql对数据库目录的权限要求很严格。禁止对相关数据目录进行属组和权限进行更改。例如数据库数据目录的权限必须为700。

**【$\color{#ff0000}强制$】严禁删除数据库系统表或系统表数据**

**【$\color{#ff0000}强制$】严禁手动kill 数据库进程和数据库会话进程**

说明: 通过kill -9 来关闭数据库，容易造成实例崩溃和重启，严重情况下会导致长时间无法启动集群。

**【$\color{#ff0000}强制$】严禁通过手动修改参数文件来修改数据库参数**

说明: 所有参数修改必须通过命令行修改,手动修改参数文件容易出现不必要的错误(如格式问题和非法字符等)导致数据库无法正常启动。

**【$\color{#ff0000}强制$】严禁使用DELETE不带条件直接删除整表**

说明：严禁在业务高峰期使用没有where条件的delete from 语句一次性删除所有数据，需分批删除。delete from删掉的大表数据，应选业务空闲期，整理表碎片，回收存储空间。

**【$\color{#ff0000}强制$】严禁在业务高峰期更新统计信息**

说明：禁止业务高峰期对表或者库进行更新统计信息。

# SQL开发规范

内容详见 [SQL开发规范(PostgreSQL分册)](/didxr6QzUDm.md) 。

# 本文件评审、修正记录

| 文件名称 | 数据库运维规范(PostgreSQL分册) |                                                          |               |        |
| -------- | ------------------------------ | -------------------------------------------------------- | ------------- | ------ |
| 序号     | 流程                           | 拟制人/审核人                                            | 拟制/审核时间 | 版本号 |
| 1        | 编写                           | 潘健/徐丹垒                                              | 2025-3-4      | V0.1   |
| 2        | 评审                           | 潘健/徐丹垒/刘伯英/马列/赵长兴/何成君/李广才/王为/盛建华 | 2025-3-12     | V0.2   |
| 3        | 正式发布                       | 数据库规范组 | 2025-6-30     | V1.0   |
| 4        | 完善章节“2.1.2.3 分区表删除/清理”措辞，使其更严谨：<br>【推荐】 使用ALTER TABLE tablename drop PARTITION ... 命令来删除/清理分区表<br>完善章节“2.2.2 索引碎片整理”措辞，使其更严谨：<br>【推荐】 索引碎片整理是维护索引性能的重要一部分。在操作窗口或者业务低峰期使用 REINDEX 命令来重新构建普通索引，以去除索引中的碎片并提高查询性能。<br>完善章节“2.4.13. 备份类型选择”，补充备份参数，完善相关备份命令。<br>                       | 徐丹垒 | 2025-10-22     | V1.0.1   |
| 5        | 正式发布                       | 数据库规范组 | 2025-10-27     | V1.1   |
