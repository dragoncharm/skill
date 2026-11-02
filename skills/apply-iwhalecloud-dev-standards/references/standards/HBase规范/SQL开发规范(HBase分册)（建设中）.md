![image](uploads/4073/996a79c9-f2c5-496e-b22b-1343c9bc20d7/PG_dev_HBase.png)

# 概述

## 编写目的

本文用于指导浩鲸科技运维人员进行数据库运维和开发工作(HBase部分)。

## 适用范围

浩鲸科技所有使用HBASE数据库的项目。

## 角色和职责

开发人员 : 参考文档对项目HBASE集群进行开发。

# Hbase集群配置事项

## 部署模式

### HBASE数据存储位置

Hbase 是一个分布式的、多版本、面向列的开源 KV 数据库。运行在 HDFS 的基础上，支持
PB 级别、百万列的数据存储。

HBASE的数据实际是存储在HDFS之上的，所以HBASE是完全依赖于HDFS提供的存储服务，和HDFS密不可分，HDFS的性能和稳定性会关系到HBASE的性能和稳定性。

**[注]：必须确保HBASE在HDFS上对应的数据文件目录的数据安全，不可手工随意操作HDFS上的HBASE目录。**

**具体的位置可以参考hbase-site.xml的hbase.rootdir配置项：**

```properties
<property>
	<name>hbase.rootdir</name>
	<value>/apps/hbase/data</value>
</property>
```

### HMaster

HMaster没有单节点问题，HBase中可以启动多个HMaster，通过Zookeeper的Master
Election机制保证总有一个Master在运行，主要负责Table和Region的管理工作。

**[注]：在生产环境下，一般启用2个HMaster。**

### Regionserver

regionServer
其实是hbase的服务，部署在一台物理服务器上，region有一点像关系型数据的分区，数据存放在region中，当然region下面还有很多结构，确切来说数据存放在memstore和hfile中。我们访问hbase的时候，先去hbase
系统表查找定位这条记录属于哪个region，然后定位到这个region属于哪个服务器，然后就到哪个服务器里面查找对应region中的数据。

**[注]：一般一个Regionserver是对应一个HDFS的datanode节点的，这样regionserver一般都能根据HDFS的就近读取数据原则，在自己所属机器的本地节点获取数据，避免需要通过网络远程抓取数据。**

### 内存配置参数

HBASE使用大量的内存进行缓存，数据读写都是通过加载到Memstore中，再刷新到HDFS，内存配置不合理会导致大量的GC停顿，甚至心跳丢失导致无法提供服务。

Regionserver内存：

规划regionserver总内存：根据节点资源尽量进行分配，上限一般是64GB，可以使用机器的一半内存。

HMaster内存：

对于HMaster进程，一般不需要太大内存，2GB
到4GB就可以满足master的工作需求，因为它的对象分配与销毁的频率远小于RegionServer。

# Hbase表设计原则

## 表预分区

### 为什么需要进行预分区

由于HBASE是分布式的数据库，由多台regionserver服务器负责分担读写请求。为了能够有效的提升集群的吞吐量和性能，必须对表进行预分区处理。如果没有进行预分区处理，默认数据只会发往一台regionserver，然后等待数据量上去后，才会自动分裂到多个regionserver中，期间还会出现各种HFILE合并和分裂，会严重影响性能。

**[注]：预分区是针对具体的某个表来说的。**

### 如何确定需要预分区多少

一般来说，预分区的数量至少和REGIONSERVER的数量保持一致，或者是整数倍。

特殊来说，对于超大表，需要设置更多的预分区，并且需要结合后面提到的HFILE配置进行设置。

### 如何进行预分区

通过建表时候的split参数指定：

例子： hbase\> create 't1', 'f1', SPLITS =\> ['10', '20', '30', '40']

这里进行了4个预分区设置，

这里rowkey是10，20，30，40开头的数据，会分别进入到4个分区中。

![image](uploads/4073/01362e05-aa4e-4f7b-a736-dbd179391b9f/dev_HBase_6.1.1.png)

## ROWKEY设计

HBASE以ROWKEY作为主键，本质上是一个key-value的数据库。所以rowkey是表设计的重要一环。

### 为什么需要进行ROWKEY设计

事实上，regionserver处理数据，是以rowkey排序后，进行循序存储的。也就是说，相隔的rowkey的数据是分布在同一个region里面，也就是说会被同一个regionserver进行处理。如果业务数据没有进行rowkey设计，可能会导致大量的数据读写，都集中到单台的regionserver，造成数据热点，无法正常使用集群的资源。

HBase的RowKey是按照ASCII有序排序的，因此我们在设计RowKey的时候要充分利用这点。

### 如何进行ROWKEY设计

一）号码反转：一般是rowkey是电话号码的情况，比如13812345678,
存储rowkey的时候，存储87654321831。

缺点：利于Get操作，但不利于Scan操作，因为数据在原RowKey上的自然顺序已经被打乱。

\*\*适用的业务场景举例：\*\*需要通过输入用户的号码信息，检索用户的相关信息。由于每个用户的号码是独立的，业务场景也只需要根据用户号码，查询用户的聚合信息。由于号码反转后，号码基本上是均匀分布的，所以rowkey也就保证了能够均匀分布在所有的region里面，能够充分利用HBASE的分布式并行存储能力。

二）Salting（加盐）的原理是在原RowKey的前面添加固定长度的随机数，也就是给RowKey分配一个随机前缀使它和之间的RowKey的开头不同。随机数能保障数据在所有Regions间的负载均衡。

缺点：

因为添加的是随机数，基于原RowKey查询时无法知道随机数是什么，那样在查询的时候就需要去各个可能的Regions中查找，Salting对于读取是利空的。并且加盐这种方式增加了读写时的吞吐量。

\*\*适用的业务场景举例：\*\*使用UID+时间戳作为ROWKEY,并且UID编号比较短，这样会有大量相同的记录会挤到相同的region里面。可以通过在前面添加随机数，让数据均匀分布在不同的region中。当然读取的时候，是需要遍历所有的region的，也就是读取的代价会相对较高。比较适合大量写入，少量读出的业务场景，读取一般使用HBASE的协处理器完成。

三）Hashing

基于 RowKey 的完整或部分数据进行
Hash，而后将Hashing后的值完整替换或部分替换原RowKey的前缀部分。这里说的 hash
包含 MD5、sha1、sha256 或 sha512 等算法。

缺点：

与 Reversing 类似，Hashing 也不利于 Scan，因为打乱了原RowKey的自然顺序

\*\*适用的业务场景举例：\*\*这种方式也适用类似号码的唯一key的业务场景，和反转不同，经过哈希后，数据能够得到绝对均匀的分别，对数据均匀分布要求较高的场景可用这种方式。比如rowkey经过反转后，还是不能做到比较均匀的分布，或者rowkey是通过多个条件组合而成：比如
号码+账期+费用类别，那么可用直接对这个rowkey进行hash存储和读写。

所以rowkey是需要根据业务情况，具体选择哪种策略。

## HFILE

HBASE底层的数据存在在HDFS上以HFILE的形式存在，HFILE的配置合理性，会对HBASE的使用产生影响。

### HFILE是什么

HBASE保存实际数据的物理文件，StoreFile 以 HFile 的形式存储在 HDFS 上。每个 Store
会有一个或多个 StoreFile（HFile），数据在每个 StoreFile 中都是有序的。

### 如何进行HFILE的配置

这个值过大，读写hbase的速度会变慢，因为底层对hdfs的读写操作由于文件数量少，很难做到高并发，高吞吐，过小会发生频繁的文件split,split会使数据短暂offline，会对数据的访问有一定影响，不太稳定，所以这个值不能太小也不能太大.
这个值一般默认大小是10G。

**配置值：hbase.hregion.max.filesize**

一般需要设置在100G以内。

## 列簇

hbase表中的每个列，都归属与某个列族。列族是表的chema的一部分(而列不是)，必须在使用表之前定义。列名都以列族作为前缀。例如courses:history
， courses:math 都属于 courses 这个列族。

### 为什么需要进行列簇的设计

列簇一般对应底层的存储是一个HFILE，不同的列簇是分布在不同的文件里面的，所以一般原则上只使用一个列簇，因为多个列簇，会导致进行多次的数据读写，性能会比较差，并且会导致不必要的文件碎片。

### 如何正确使用列簇

原则上只使用1个列簇，尽量避免使用多个列簇，特殊情况下，可以使用两个列簇。触发一个rowkey对应大量的数据，单个列簇读写性能成为瓶颈。

## 表大小设计

HBASE设计是一个超大表，可以作为亿级，百亿级的规模的巨大表使用，但是实际上在超大表的情况下会产生一些问题，如果使用不当，会导致严重的性能问题，甚至出现生产故障。

### 为什么需要进行表大小设计

一般来说，表的数据量不是太大（1T）以内，或者一个regionserver平均承载的数据量在10G以内，可以不用太关注表的大小，但当表规模上去后，或者集群本身的规模不大，这必要进行表规模的设计。

### 表大小设计的原则

表的设计原则，基本上是根据HBASE集群的HFILE大小，结合预分区的配置策略进行，根据预估合理的表数据写入量，设置合理的预分区数，避免频繁出现REGIONSERVER分裂导致的大小合并事件。

举例：

有一个1T的表，regionserver是50台，在数据均匀的情况下，每台regionserver需要处理
1T/50=20G的数据，假定默认的HFILE大小是10G，没有修改，那么每台regionserver的只要分配2个regionserver才能存储完整的1T数据，考虑到后续的扩展，那每台regionserver应该需要有4个region。

所以：预分区数量 = 4\*50=200。

根据合理的预估，结合HFILE的大小和REGIONSERVER的数量，进行合理的预分区策略，是解决大表的关键。

一般来说，需要避免每个REGIONSERVER承载超过4个region，这样性能可能无法满足要求。在集群规模受限的情况下，需要根据业务，对表进行拆分处理。避免一个表过大。

举例2：

现在需要存储用户的话单，假设每用户每天话单数是10， 用户数有100W
每话单大小大概1KB， 估算每天的存储，每月的存储。

每天数据量：10\*100W\*1KB = 10GB

每月数据量：300GB

需要存储10个月，数据量是3TB

如果还是使用50台regionserver进行存储，那么每台regionserver需要存储
3T/50=60G数据，这时候由于HFILE是10G,那需要6个region才能存储，考虑到扩展和数据可能不均衡，一个regionserver需要配置8个region。

由于8个region已经超过了4个region的建议值，所以最后扩充到100台regionserver完成存储。

预分区= 4\*100= 400，regionserver调整到100台。

这个例子也可用初略估算HBASE的服务器数量，基本上可以根据。

# Hbase写入优化

HBAE的写入能够通过一些参数，较大幅度提升性能。

## WAL

WAL(Write-Ahead-Log)预写日志是Hbase的RegionServer在处理数据插入和删除的过程中用来记录操作内容的一种日志。在每次Put、Delete等一条记录时，首先将其数据写入到RegionServer对应的HLog文件中去。

### WAL的作用是什么

WAL的作用是为了防止regionserver出现故障，内存中的数据没有刷写到HFILE里面，导致数据丢失的一种保护机制。所有的操作都会预先写入到HDFS上的WAL日志文件中，在系统出现down机重启后，能够进行恢复。

### 什么时候需要调整WAL的参数

由于每次的读写都要写入WAL，集群的吞吐量会受到很大的限制，关闭WAL后可以大幅度的提升读写性能，这个时候数据都只写入到内存中，然后到达阈值后，再统一写入HFILE。

如果我们的程序有自我保护自己，再额外的地方会进行记录，确保数据不会丢失，比如我们在应用中会进行批量的HBASE数据写入，那么完全可以关闭WAL，由程序自己保证数据能够成功写入，用户自己的程序可以在批量数据写入成功后，自己记录成功的标记。如果发行没有成功写入，用户程序自己再进行重复的写入。也就是说不适用HBASE的自我数据保护机制。

JAVA的关闭WAL的API：

```java
Put p = new Put(ROW_ID)
                .addColumn(FAMILY, NAME, Value)
                .setDurability(Durability.SKIP_WAL)
```

## 表提交

HBASE的提交的概念和关系型数据库有点不一样，这里的提交主要是客户端一次写入数据后，累计到多少数据量后，会通过RPC把数据发送到REGIONSERVER中。由于数据没有提交前是在客户端里面的，所以这部分的数据事实上是还没存在HBASE之上的。

### 什么是表提交

数据写入Hbase这里采用Table.put(putList) 的方式
，数据的格式为Put类型，put方法传参既可以是一个Put对象也可以是一个List\<Put\>集合，集合情况下为批量入库。

入库机制：类似于关系型数据库，如果是一条一条入库，则region每次都会进行一次提交；批量入库，则在数据量达到一定阈值时提交一次，在Table关闭时还会提交一次，批量入库时也可以类似与关系型数据库那样支持手动提交。

### 需要使用什么模式进行表提交

一般是通过使用JAVA的后台API，设置自动提交的参数，进行性能的优化，一次性能够传递较多的数据，减少网络连接。

```java
public boolean put(String tablename, List<Put> putList)
{
    BufferedMutator mutator = null;
    TableName tName = TableName.valueOf(tablename);
    BufferedMutatorParams params = new BufferedMutatorParams(tName);
    params.writeBufferSize(5*1024*1024); // 可以自己设定阈值 5M 达到5M则提交一次
    try
    {
         mutator = conn.getBufferedMutator(params);
         mutator.mutate(putList); // 数据量达到5M时会自动提交一次
         mutator,flush(); // 手动提交一次
    }
    catch(Exception e)
    {
        e.printStackTrace();
        return false;
    }
    finally
    {
        try
        {
            if(mutator != null)mutator.close();  // 提交一次
        }
        catch(Exception e)
        {
            e.printStackTrace();
        }
    }
}
   
```

# REGIONSERVER规划

每台服务器的region个数：20-200个

每个region的大小：10G-30G （hbase.hregion.max.filesize）

一台regionserver的服务器最多可以存储的数据量差不多为200 \* 30G ＊ 3＝ 18T

计算依据：

RegionSize：hbase.hregion.max.filesize (默认：10G)

MemstoreSize：hbase.hregion.memstore.flush.size (默认：128mb)

ReplicationFactor：dfs.replication (HDFS默认3副本)

HeapFractionForMemstore：hbase.regionserver.global.memstore.size/hbase.regionserver.global.memstore.upperLimit（内存堆比例）

10G的REGION配比举例：

```properties
Disk Size:hbase.hregion.max.filesize=10G
MemstoreSize:hbase.hregion.memstore.flush.size = 128M
ReplicationFactor:dfs.replication=3
HeapFractionForMemstore:hbase.regionserver.global.memstore.upperLimit=0.4
10G/128M*3*0.4=96  (128MB是HFILE一次性在内存里面缓存的部分)
比例关系：
1bytes RegionServer Heap:需要96bytes的硬盘
 
**环境规格如下：**
存放1T的数据，需要新增一台32G内存，3T的硬盘的服务器
带宽：万兆 （因为HBase在大量scan以及高吞吐量写入的时候特别耗费网络带宽资源）
```

简单的估算：

对于regionserver来说，数量和内存相关，默认10G的HFILE配置下，分配32G作为jvm内存的regionserver，可以配置3T硬盘，可以实际存储1T的数据

50台机器，就可以存储最多50T的实际数据。

# 本文件评审、修正记录

| 文件名称 | SQL开发规范 –HBase分册 |               |               |        |
|----------|------------------------|---------------|---------------|--------|
| 序号     | 流程                   | 拟制人/审核人 | 拟制/审核时间 | 版本号 |
| 1        | 编写                   | 叶禧辉        | 2020/05/28    | V0.1   |
| 2        | 根据评审意见修改       | 叶禧辉        | 2020/07/23    | V0.2   |
