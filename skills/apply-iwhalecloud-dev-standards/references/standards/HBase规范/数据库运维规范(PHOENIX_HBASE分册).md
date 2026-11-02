![image](uploads/47873/596a9324-700b-4324-a360-1449101cd571/image.png)

# 概述

## 编写目的

* 避免错误的操作导致进程异常或者数据异常
* 避免错误的操作导致性能异常
* 能够及时发现问题并采取相应措施

## 适用范围

所有使用HBASE1.2.0+,PHOENIX4.14.1+的项目以及所内的开发测试环境。

## 角色和职责

运维人员：负责执行HBASE&PHOENIX各种命令、工具和脚本，配置检查，数据检查等。

# 运维规范--PHOENIX

## 命令

### 【强制】stop PHOENIX前必须要停掉业务进程。

**说明**

PHOENIX stop之后，会断掉所有的链接，业务进程无法正常运行。且在start PHOENIX之后业务依然无法正常运行，就算此时重启业务进程，也可能会导致链接异常。 停止之前需要检查PHOENIX中的活跃连接，在部署了PHOENIX的节点上,使用netstst -anp |grep 60020 查看是否还有业务进程连接。

![image](uploads/47873/819ca56c-3ae2-460f-a981-939e6fcde27b/image.png)

图中标红的即为业务连接过来的IP

###  【强制】添加/移除 PHOENIX前必须要stop PHOENIX以及停掉业务进程。

**说明**

PHOENIX不支持动态更新节点,当需要添加或移除PHOENIX节点时,需要先停止业务进程以及PHOENIX组件

### 【推荐】避免使用存在高冲突索引的字段值来查询记录。

**说明**

高冲突索引的索引区分度很低，很多记录的这个字段值（索引所在字段）都一样。通过这种索引来查询记录如果遇上高冲突字段值，会导致耗时较长，严重情况下可能导致业务中断。

### 【强制】禁止单次对百万级别以上记录进行upsert或delete

**说明**

对百万级别以上记录执行的更新删除操作，属于很危险的操作，会占用大量CPU、内存资源，可能会导致业务中断。若实在需要在高峰期执行此类操作,需要少量多次进行。

【故障案例】某现场,表记录数量(50亿),因在入数据时,同时对该表进行了百万级别以上记录的删除操作,导致HBASE挂死且无法启动

### 【强制】业务高峰期禁止对百万级别以上记录的表进行全表扫描

**说明**

对大表进行全表扫描操作，会占用大量CPU、内存资源，可能会导致业务中断。若实在需要在高峰期执行此类操作,需要少量多次进行。

### 【推荐】避免使用OR、Join,子查询等逻辑比较复杂的SQL

**说明**

虽然Phoenix支持各种Join操作，但是Phoenix主要还是定位为在线数据库，复杂Join，比如子查询返回数据量特别大或者大表Join大表，在实际计算过程中十分消耗系统资源，会严重影响在线业务，甚至导致OutOfMemory异常。对在线稳定性和实时性要求高的用户，建议只使用Phoenix的简单查询，且查询都命中主表或者索引表的主键。另外，建议用户在运行SQL前都执行下explain，确认是否命中索引，或者主键。

## 脚本

### 【强制】业务高峰期不得批量执行PHOENIX脚本

**说明**

批量是指一次修改1W或者以上记录
批量执行脚本很容易长时间占用锁，阻塞正常业务，从而引起业务过载。如果需要修复数据，建议少量多次。

## 建库建表

### 【强制】PHOENIX创建的库名需要和HBASE中的库名一致

**说明**

PHOENIX的数据来源为HBASE,只有名称一致才可以映射到相应的库。

### 【强制】**phoenix表名需要大写**

**说明**

在phoenix中，表名等会自动转换为大写,为避免歧义,表名统一大写

### 【强制】PHOENIX创建的表名需要和HBASE中的表名一致

**说明**

PHOENIX的数据来源为HBASE,只有名称一致才可以映射到相应的表中的数据。

## FAQ

### PHOENIX连接不上

PHOENIX无法连接时,可先去集群查看HBASE是否正常。

如果HBASE运行异常，参考HBASE运维规范中的FAQ。

如果HBASE运行正常，可在后台的SHELL界面连接PHOENIX:

如果无法连接，检查HBASE的连接数是否异常。

如果正常连接，检查防火墙等设置是否异常。

### PHOENIX百万级数据清理到数百后查询依旧缓慢

可检查HBASE中的建表语句，如果其中指定了保留份数，可以指定其中某一份数据进行定向清理

### PHOENIX数据丢失

检查HBASE中表名是否还和PHOENIX一致,若一致则检查HBASE中数据是否被清理

### PHOENIX查询性能变慢

检查HBASE的REGIONSERVER中REGION数,若有超过400的需要进行重分布或REGION清理

# 运维规范--HBASE

## 命令与系统文件

### 【强制】集群中数据节点的可用磁盘空间至少是内存空间的三倍。

**说明**

HBASE数据是存放到HDFS中的,HDFS默认数据保留三份。

考虑到数据导出、文件落地、升级、容灾同步、数据落地持久化等因素，数据节点的磁盘大小至少是内存大小的三倍。

### 【强制】禁止修改管理节点或数据节点下的文件。

**说明**

生产环境的HBASE配置文件默认在CDH/HDP的WEB-UI界面统一管理，禁止手动在后台修改，否则可能导致各节点文件不一致，进而影响任务执行

### 【强制】对数据进行修改前必须手动创建快照。

**说明**

为防止操作失败后无法回滚，必须提前手动创建快照

【故障案例】某现场,操作人员在现场操作时误将表进行删除,因之前有做过快照,才最终将表恢复

### 【建议】生产环境核心表每天做一份快照。

**说明**

为避免重要数据丢失,建议每天做一份快照并定期清理历史快照

### 【强制】对数据进行修改前必须手动创建快照。

**说明**

为防止操作失败后无法回滚，必须提前手动创建快照

### 【强制】生产环境禁止开启定时大合并。

**说明**

Compaction 分为两种，分别是 Minor Compaction 和 Major Compaction。Minor Compaction会将临近的若干个较小的 HFile 合并成一个较大的 HFile，并清理掉部分过期和删除的数据，有系统使用一组参数自动控制，Major Compaction 会将一个 Store 下的所有的 HFile 合并成一个大 HFile，并且会清理掉所有过期和删除的数据。
大合并期间,会消耗集群大量的IO,内存及CPU资源,且会导致部分REGION无法访问,业务繁忙情况下触发大合并可能会导致业务中断。

### 【强制】生产环境禁止修改/tmp及其子目录权限。

**说明**

/tmp下存在HBASE的重要文件,权限修改后会导致HBASE异常挂死
【故障案例】某现场,分析区-CDH大数据集群,因误修改了/tmp下路径权限,导致HBASE挂死,引发了一系列问题,经历三天时间才彻底修复

### 【强制】生产环境对HBASE数据进行迁移,复制,转移等操作只能使用HBASE用户,如开启了KERBEROS则只能使用HBASE的认证文件

**说明**

【故障案例】某现场,BSS-CDH大数据集群,在HBASE彻底无法启动后,采用使用新的HDFS路径的方案进行启动,启动后在进行数据恢复时,因使用HDFS的认证文件进行数据cp迁移到新路径,导致迁移后的数据无法通过hbase hbck -repair进行修复,严重影响了故障的恢复时间

## 巡检

### 【推荐】单台RS上RESION数超过400必须进行处理

**说明**

每个region**server上的region数建议在400以内，越超过此值越可能存在严重性能问题。达到2000左右时业务感知会特别明显。**

巡检说明:

**从CDH前台和master前台以及regionServer的前台都可以巡检到region数量，如master前台：**

![image](uploads/47873/a81cfad1-02a7-4b73-a996-f7a86a64e0b6/image.jpeg)

【故障案例】某现场,HBASE经常出现查询性能不良,且每次重启时都耗费3-4小时,导致操作时业务长期无法恢复,极大程度的影响了客户的使用体验

### 【强制】RS的blockcache命中率如果频繁低于50%必须进行处理

**说明**

缓存命中率对hbase的读有很大的影响，若这个指标低于50%，说明HBASE的读性能严重不良,需要将 BlockCache设置大些，Memstore设置小些，以加大缓存的命中率。

巡检说明:

从regionserver web页面可以看到缓存命中率的情况：

![image](uploads/47873/c65c0d97-ad91-4df9-b6a8-1cb85d25d332/image.jpeg)

### 【强制】RS的request请求差异频繁超过25%需要特别关注

**说明**

通过读写请求数可以大概看出每台regionServer的压力，如果压力分布不均匀，应该检查regionServer上的region以及其它指标

如果读写请求数以及region都十分不均匀,可以考虑进行数据平衡

巡检说明：

从master前台可以查看RS的请求差异

![image](uploads/47873/bccc6fca-6aef-4649-8782-dbfd3b45572c/image.jpeg)

### 【推荐】如果压缩队列有告警,可以对集群中的大表在业务闲时手动触发大合并

**说明**

压缩队列存放的是正在小合并的storefile，compact操作对hbase的读写影响较大

如果业务侧反馈Hbase部分任务读写速度变慢,且此时压缩队列存在告警,可在业务闲时手动触发大合并

**巡检说明:**

**CDH可直接在HBASE状态界面中查看**

![image](uploads/47873/a3d1522a-d63f-45ca-91ff-03eadc9594e5/image.png)

### 【强制】usedHeadp超过90%以上,需要申请扩大RegionServer的内存

**说明**

usedHeadp反应了RS的压力大小,超过90%极易触发OOM等故障

巡检说明:

从region Server的前台可以看到：

![image](uploads/47873/c727b85e-84d0-4593-90c8-8d8fe9ebc06a/image.png)

## FAQ

### MASTER无法启动

进入/var/log/hbase,根据日志排查具体问题

场景1):日志出现out of memory

解决方式:增加MASTER的内存

场景2):日志无明显报错

解决方式:调整超时参数hbase.master.namespace.init.timeout及hbase.master.initializationmonitor.timeout为180000000后再启动

【故障案例】某现场,HBASE-MASTER无法启动

故障现象:HBASE-MASTER的WEB-UI界面打开后一直显示初始化,经过一两个小时都没有状态的改变

场景3):重启时日志不刷新

解决方式:检查/var/log/hbase目录及其下面文件权限,所属用户是否为hbase,若不是则需要修改

### 任务执行变慢

查看压缩队列是否时不时会有告警，查看变慢的任务是否为同一张表

若压缩队列有告警,需要手动在业务闲时触发大合并。

哪些表的任务变慢，则触发哪些表的大合并。

### 使用hbck repair修复出现异常

修复前:需确保所有MASTER以及REGIONSERVER都是启动状态。

如果最近使用distcp迁移了文件到集群，需要确保文件所属用户为HBASE

# 附录

### 数据一致性检查与修复

#### 数据一致性检查

**说明**

数据一致性是指：
1. 每个region都被正确的分配到一台regionserver上，并且region的位置信息及状态都是正确的。

2. 每个table都是完整的，每一个可能的rowkey 都可以对应到唯一的一个region

数据一致性检查常用方式

以下三种方式,按照实际情况进行选择,如无特殊情况可直接选择第一种,检查后按照其中给出的ERROR信息进行修复

1. hbase hbck

注：有时集群正在启动或region正在做split操作，会造成数据不一致

2. hbase hbck -details

加上–details会列出更详细的检查信息，包括所以正在进行的split任务

3. hbase hbck Table1 Table2

如果只想检查指定的表，可以在命令后面加上表名，这样可以节省操作时间

#### 数据一致性修复

**说明**

如果不了解修复机制,可直接使用hbase hbck -repair进行一致性的修复,此为兜底修复手段
直接使用hbase hbck -repair进行一致性的修复时,必须确保所有MASTER与REGIONSERVER都是启动状态,且数据平衡未开启
fix命令执行的时间与你的集群存储大小和region个数相关，请耐心等待。不要kill掉正在执行的fix命令，以免导致其他问题。

各个修复命令含义介绍

1) 低风险的修复

如果出现数据不一致，修复时要最大限度的降低可能出现的风险，使用以下命令对region进行修复风险较低：

| <br><br>操作命令<br><br> | <br><br>含义<br><br> |
| ---- | ---- |
| <br><br>hbase hbck -fixAssignments<br><br> | <br><br>修复region没有分配(unassigned)，错误分配（incorrectly assigned）以及多次分配（multiply assigned）的问题<br><br> |
| <br><br>hbase hbck -fixMeta<br><br> | <br><br>删除META表里有记录但HDFS里没有数据记录的region,添加HDFS里有数据但是META表里没有记录的region到META表<br><br> |
| <br><br>hbase hbck -fixHdfsHoles<br><br> | <br><br>如果rowkey出现空洞，即相邻的两个region的rowkey不连续，则使用这个参数会在HDFS里面创建一个新的region。创建新的region之后要使用-fixMeta和-fixAssignments参数来使用挂载这个region，所以一般和前两个参数一起使用<br><br> |
| <br><br>hbase hbck -repairHoles<br><br> | <br><br>等价于：hbase hbck -fixAssignments -fixMeta -fixHdfsHoles<br><br> |

2)风险较高的修复

| <br><br>hbase hbck -fixHdfsOrphans<br><br> | <br><br>将文件系统中的没有metadata文件(.regioninfo)的region目录加入到hbase中，即创建.regioninfo目录并将region分配到regionser<br><br> |
| ---- | ---- |
| <br><br>hbase hbck -fixHdfsOverlaps<br><br> | <br><br>通过两种方式将rowkey有重叠的region合并：  <br>1. merge:将重叠的region合并成一个大的region  <br>2. sideline:将region重叠的部分去掉，并将重叠的数据先写入到临时文件，然后再导入进来。  <br>如果重叠的数据很大，直接合并成一个大的region会产生大量的split和compact操作，可以通过以下参数控制region过大：  <br>-maxMerge 合并重叠region的最大数量  <br>-sidelineBigOverlaps 假如有大于maxMerge个数的 region重叠, 则采用sideline方式处理与其它region的重叠.  <br>-maxOverlapsToSideline 如果用sideline方式处理重叠region,最多sideline n个region .<br><br> |
| <br><br>hbase hbck –fixVersionFile<br><br> | <br><br>Hbase的数据文件启动时需要一个version file，如果这个文件丢失，可以用这个命令来新建一个，但是要保证hbck的版本和Hbase集群的版本是一样的<br><br> |
| <br><br>hbase hbck -repair<br><br> | <br><br>以下命令的缩写：hba hbase hbck -fixAssignments -fixMeta -fixHdfsHoles -fixHdfsOrphans -fixHdfsOverlaps -fixVersionFile –sidelineBigOverlaps  <br>可以指定表名：hbase hbck -repair Table1 Table2<br><br> |
| <br><br>hbase org.apache.hadoop.hbase.util.hbck.OfflineMetaRepair<br><br> | <br><br>如果ROOT表和META表都出问题了Hbase无法启动，可以用这个命令来创建新的ROOT和META表。这个命令的前提是Hbase已经关闭，执行时它会从hbase的home目录加载hbase的相关信息（.regioninfo），如果表的信息是完整的就会创建新的root和meta目录及数据<br><br> |
| <br><br>hbase hbck –fixSplitParents<br><br> | <br><br>当region做split操作的时候，父region会被自动清除掉。但是有时候子region在父region被清除之前又做了split。造成有些延迟离线的父region存在于META表和HDFS中，但是没有部署，HBASE又不能清除他们。这种情况下可以使用此命令重置这些在META表中的region为在线状态并且没有split。然后就可以使用之前的修复命令把这个region修复<br><br> |

【故障案例】某现场,大数据BSS-CDH集群,使用hbase hbck -repair时发现表Hbase表EVENT_USAGE_C_QUERY_202209发现存在6个region无法deploy

解决过程：

hbase hbck 发现大量lingering reference file 文件

```html
ERROR: Found lingering reference file hdfs://nameservice1/hbase_bss_n/data/BSS/EVENT_USAGE_C_QUERY_202209/845bec0a19f22e0ea3158679df321ee2/0/4d66fd9bed9244668252aa36ad6d2b6c.3debc7fa9ab89153fe801768e2a10584

ERROR: Found lingering reference file hdfs://nameservice1/hbase_bss_n/data/BSS/EVENT_USAGE_C_QUERY_202209/f4fa04435ee1115f0f2039ed344f5f20/0/4a7007a924ab410db46102999560dc0e.3b95e27df4650c8630e043f4ddc7abd7

ERROR: Found lingering reference file hdfs://nameservice1/hbase_bss_n/data/BSS/EVENT_USAGE_C_QUERY_202209/59a65d3ef1fa87e5a0297594f1357f3c/0/1e6bb1553c1a4f95892fd8b8fa03b325.30b516cbfef783388fe7e19b47a346dc

ERROR: Found lingering reference file hdfs://nameservice1/hbase_bss_n/data/BSS/EVENT_USAGE_C_QUERY_202209/845bec0a19f22e0ea3158679df321ee2/0/d0ca995886844064810b54a6021ada1b.3debc7fa9ab89153fe801768e2a10584

ERROR: Found lingering reference file hdfs://nameservice1/hbase_bss_n/data/BSS/EVENT_USAGE_C_QUERY_202209/59a65d3ef1fa87e5a0297594f1357f3c/0/9a836d023ab846ac82685cb9867e6a46.30b516cbfef783388fe7e19b47a346dc

ERROR: Found lingering reference file hdfs://nameservice1/hbase_bss_n/data/BSS/EVENT_USAGE_C_QUERY_202209/f4fa04435ee1115f0f2039ed344f5f20/0/a8242acd401045a8bc736e922d00bfcd.3b95e27df4650c8630e043f4ddc7abd7

ERROR: Found lingering reference file hdfs://nameservice1/hbase_bss_n/data/BSS/EVENT_USAGE_C_QUERY_202209/845bec0a19f22e0ea3158679df321ee2/0/f1941ca3cf294e8a9f546f1e49443aab.3debc7fa9ab89153fe801768e2a10584

ERROR: Found lingering reference file hdfs://nameservice1/hbase_bss_n/data/BSS/EVENT_USAGE_C_QUERY_202209/59a65d3ef1fa87e5a0297594f1357f3c/0/33ef5417ebfe4a64b853e1611faec500.30b516cbfef783388fe7e19b47a346dc

ERROR: Found lingering reference file hdfs://nameservice1/hbase_bss_n/data/BSS/EVENT_USAGE_C_QUERY_202209/f4fa04435ee1115f0f2039ed344f5f20/0/c22cff99fc5a405ea65f0baed791c2de.3b95e27df4650c8630e043f4ddc7abd7

ERROR: Found lingering reference file hdfs://nameservice1/hbase_bss_n/data/BSS/EVENT_USAGE_C_QUERY_202209/845bec0a19f22e0ea3158679df321ee2/0/a800b1d3bb5f43c59ecffa4ce5f080d7.3debc7fa9ab89153fe801768e2a10584

ERROR: Found lingering reference file hdfs://nameservice1/hbase_bss_n/data/BSS/EVENT_USAGE_C_QUERY_202209/59a65d3ef1fa87e5a0297594f1357f3c/0/83ec680aa38d4b719e928760d4dfd1bf.30b516cbfef783388fe7e19b47a346dc

ERROR: Found lingering reference file hdfs://nameservice1/hbase_bss_n/data/BSS/EVENT_USAGE_C_QUERY_202209/f4fa04435ee1115f0f2039ed344f5f20/0/79c49be4ebdf4d10b14b716f94346507.3b95e27df4650c8630e043f4ddc7abd7

ERROR: Found lingering reference file hdfs://nameservice1/hbase_bss_n/data/BSS/EVENT_USAGE_C_QUERY_202209/f4fa04435ee1115f0f2039ed344f5f20/0/faefef954961462b8e2e87fcecf9595e.3b95e27df4650c8630e043f4ddc7abd7

ERROR: Found lingering reference file hdfs://nameservice1/hbase_bss_n/data/BSS/EVENT_USAGE_C_QUERY_202209/845bec0a19f22e0ea3158679df321ee2/0/34ccef1f66d443f097775cbeedf8dfe8.3debc7fa9ab89153fe801768e2a10584

ERROR: Found lingering reference file hdfs://nameservice1/hbase_bss_n/data/BSS/EVENT_USAGE_C_QUERY_202209/59a65d3ef1fa87e5a0297594f1357f3c/0/41234094e51a480980edd6465935135c.30b516cbfef783388fe7e19b47a346dc

ERROR: Found lingering reference file hdfs://nameservice1/hbase_bss_n/data/BSS/EVENT_USAGE_C_QUERY_202209/f4fa04435ee1115f0f2039ed344f5f20/0/1b74c913f0574df9a0136293278f34d3.3b95e27df4650c8630e043f4ddc7abd7

ERROR: Found lingering reference file hdfs://nameservice1/hbase_bss_n/data/BSS/EVENT_USAGE_C_QUERY_202209/f4fa04435ee1115f0f2039ed344f5f20/0/bf166e90bd984cce80a49a224621f68f.3b95e27df4650c8630e043f4ddc7abd7

ERROR: Found lingering reference file hdfs://nameservice1/hbase_bss_n/data/BSS/EVENT_USAGE_C_QUERY_202209/59a65d3ef1fa87e5a0297594f1357f3c/0/c676ca05462e4795a8dfc9c69589db87.30b516cbfef783388fe7e19b47a346dc

ERROR: Found lingering reference file hdfs://nameservice1/hbase_bss_n/data/BSS/EVENT_USAGE_C_QUERY_202209/845bec0a19f22e0ea3158679df321ee2/0/4ca5c49cfd3c430ba537cfef3919588f.3debc7fa9ab89153fe801768e2a10584

ERROR: Found lingering reference file hdfs://nameservice1/hbase_bss_n/data/BSS/EVENT_USAGE_C_QUERY_202209/f4fa04435ee1115f0f2039ed344f5f20/0/dd3c8bab8fe1403cb3d14e123347233c.3b95e27df4650c8630e043f4ddc7abd7

ERROR: Found lingering reference file hdfs://nameservice1/hbase_bss_n/data/BSS/EVENT_USAGE_C_QUERY_202209/f4fa04435ee1115f0f2039ed344f5f20/0/161548006db749169ab204fa71715117.3b95e27df4650c8630e043f4ddc7abd7

ERROR: Found lingering reference file hdfs://nameservice1/hbase_bss_n/data/BSS/EVENT_USAGE_C_QUERY_202209/845bec0a19f22e0ea3158679df321ee2/0/c77e5a29a20549e198d84e1e073622bb.3debc7fa9ab89153fe801768e2a10584
```

region在split异常导致的残留文件存在与老的pararent regoin中

参考文献：[https://issues.apache.org/jira/browse/HBASE-8502](https://issues.apache.org/jira/browse/HBASE-8502)

修复方法：

1.删除文件，后-fix,反复确认

2.hbase hbck -fixReferenceFiles EVENT_USAGE_C_QUERY_202209

# 本文件评审、修正记录

| 文件名称| 数据库运维规范(PHOENIX/HBASE分册) |  |  |  |
| ---- | ---- | ---- | ---- | ---- |
| 序号 | 流程 | 拟制人/审核人 | 拟制/审核时间 | 版本号 |
| 1 | 编写 | 王文举/马列 | 2023-02-15 | V0.1 |
| 2 | 评审内容修改 | 王文举/马列 | 2023-03-16 | V0.2 |
| 3 | 评审内容修改 | 王文举/马列 | 2023-06-14 | V0.3 |
| 4 | 发布 | 数据库规范组 | 2023-07-20 | V1.0 |
