![image](uploads/4078/c4d54e28-3107-4627-b2f1-fcb783135dc5/PG_operation_JVM.png)

## 前言

本运维手册定义用于基于JVM运行的应用关于内存及垃圾回收配置的要求，并对内存及垃圾回收相关内容进行简要阐述，旨在提升现场运维及产品开发测试人员对JVM调优配置的认识，保障产品JVM参数配置的正确性，使应用更加平稳安全运行。

## 概述

### 背景

旨在简要介绍虚拟机相关知识，保障JVM相关参数配置的正确性，使应用平稳高效的运行。

### 使用对象

现场运维人员、应用开发测试人员及性能测试人员。

### 适用范围

该规约适用于 **JDK 1.8** 及 **JDK 21** 版本运行的Java应用。本文档会在相关章节中明确标注版本差异，请在配置时注意区分。

### 术语介绍

| 术语     | 说明                                                                                                                                                                                                                                                                                                                                                                                 |
| ---------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| JVM      | Java Virtual Machine（Java虚拟机）的缩写，JVM是一种用于计算设备的规范，它是一个虚构出来的计算机，是通过在实际的计算机上仿真模拟各种计算机功能来实现的。<br/>引入Java语言虚拟机后，Java语言在不同平台上运行时不需要重新编译。Java语言使用Java虚拟机屏蔽了与具体平台相关的信息，使得Java语言编译程序只需生成在Java虚拟机上运行的目标代码（字节码），就可以在多种平台上不加修改地运行。 |
| GC       | Garbage Collection，有了GC，程序员就不需要再手动的去控制内存的释放。当Java虚拟机（VM）发觉内存资源紧张的时候，就会自动地去清理无用对象（没有被引用到的对象）所占用的内存空间（这里的说法略显粗略，事实上何时清理内存是个复杂的策略）。                                                                                                                                               |
| 年轻代   | 所有新生成的对象都是优先放在年轻代的。年轻代的目标就是尽可能快速的收集掉那些生命周期短的对象。年轻代分三个区。一个Eden区，两个 Survivor区(一般而言)。                                                                                                                                                                                                                                |
| 老年代   | 在年轻代中经历了N次垃圾回收后仍然存活的对象或者一些超大对象，就会被放到老年代中。                                                                                                                                                                                                                                                                                                    |
| STW      | Stop the world，虚拟机在进行垃圾回收时，需要业务应用线程执行到一些“安全点”，在到达“安全点”时就会暂停当前运行的线程，再执行标记和清除，这个过程会停顿业务应用，所以称之为stop the world。                                                                                                                                                                                         |
| CMS      | Concurrent Mark Sweep，是一款划时代的垃圾回收器，它尽可能的优化STW的时机，使GC线程与业务程序线程并行执行，令程序暂停时间大大降低。**(仅适用于 JDK 1.8，JDK 21 已移除)**                                                                                                                                                                                                                                                   |
| G1       | Garbage First，JDK 9 之后的默认垃圾回收器（JDK 8 中也可使用），采用分区（Region）管理内存，兼顾高吞吐量与低延迟，适用于大堆内存场景。                                                                                                                                                                                                                                                   |
| ZGC      | Z Garbage Collector，JDK 11 引入、JDK 15 正式发布（JDK 21 中已非常成熟）的超低延迟垃圾回收器，旨在实现亚毫秒级的停顿时间（<1ms），且停顿时间不随堆大小增加而增加。                                                                                                                                                                                                                                                   |
| 元数据区 | 元数据区的概念出现在Java8以后，在Java8以前称为方法区，元数据区也是一块线程共享的内存区域，主要用来保存被虚拟机加载的类信息、常量、静态变量以及即时编译器编译后的代码等数据。                                                                                                                                                                                                         |

## 虚拟机介绍

### JVM内存模型简介

![image](uploads/4078/98bf2faf-c5d6-4c97-9551-e63a67402cc3/JMM_INTRODUCE.png)

JDK1.8的JVM内存模型中将内存分为本地方法栈、程序计数器、虚拟机栈、堆区、元数据区五大部分，而我们常常所说的设置JVM的内存参数大多关注的是上图中堆区的内存大小，可以简单的理解成：
堆内存 = 老年代 + 年轻代；年轻代 = Eden + S0 + S1。
目前商业虚拟机的垃圾(对象)回收都采用分代收集算法，在年轻代中选择复制算法，而老年代中由于对象存活率高、没有额外空间对它进行分配担保，就必须使用标记-清除或者标记-压缩算法。

- 年轻代复制算法简述：

1、对象分配在Eden区与S0区；
2、对Eden区与S0区进行垃圾回收，存活对象复制到S1区；清理Eden区与S0区，一次新生代GC结束。
3、对象分配在Eden区与S1区；
4、对Eden区与S1区进行垃圾回收，存活对象复制到S0区；清理Eden区与S1区，又一次新生代GC结束。
5、goto 1

- 老年代不同回收器采用的策略都各不相同，更多关于JVM垃圾回收的知识请参考_附录1_：

以下为对象分配与垃圾回收的简要流程图：
![image](uploads/4078/3f0cf98f-fdcf-43a4-963f-0045077fa4f9/OBJECT_ALLOCATE.png)

### 虚拟机参数介绍

#### 查看虚拟机运行时默认参数

查询命令：

```bash
java -XX:+PrintFlagsFinal -version
```

结果样例：

```bash
[Global flags]
    uintx AdaptiveSizeDecrementScaleFactor          = 4                                   {product}
    uintx AdaptiveSizeMajorGCDecayTimeScale         = 10                                  {product}
    uintx AdaptiveSizePausePolicy                   = 0                                   {product}
    uintx AdaptiveSizePolicyCollectionCostMargin    = 50                                  {product}                              {product}
    省略。。。
    bool HeapDumpAfterFullGC                       = false                               {manageable}
    bool HeapDumpBeforeFullGC                      = false                               {manageable}
    bool HeapDumpOnOutOfMemoryError                = false                               {manageable}
    省略。。。
    uintx NewRatio                                  = 2                                   {product}
    uintx NewSize                                  := 441450496                           {product}
    uintx NewSizeThreadIncrease                     = 5320                                {pd product}
    省略。。。
   
```

#### 通用虚拟机参数介绍

| 参数名                               | 默认值                             | 适用版本       | 说明                                                                                                                                                                                                     |
| -------------------------------------- | ------------------------------------ | ---------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| -Xms                                 | 默认值一般为操作系统可用内存的1/64 | 通用             | 设置对内存初始化大小，非容器环境必须固化，并且与Xmx的值相同；容器环境下不建议使用。                                                                                                                      |
| -Xmn                                 | 默认情况下按照NewRatio分配         | 通用             | 设置新生代的初始值及最大值，对NewSize与MaxNewSize同时设置。必须小于Xmx。容器环境下不建议使用                                                                                                             |
| -Xmx                                 | 默认值一般为操作系统可用内存的1/4  | 通用             | 设置堆内存最大值，非容器环境必须固化；容器环境下不建议使用                                                                                                                                               |
| -Xss                                 | 与环境有关                         | 通用             | 设置线程栈占用内存大小，如-Xss1024K，一般情况无需配置。                                                                                                                                                  |
| -XX:NewSize                          | 与环境有关                         | 通用             | 新生代初始化内存的大小。                                                                                                                                                                                 |
| -XX:MaxNewSize                       | 与环境有关                         | 通用             | 新生代可被分配的最大内存大小。                                                                                                                                                                           |
| -XX:NewRatio                         | 2                                  | 通用             | 设置年轻代与老年代的比例，默认值为2，即年轻代:老年代=1:2                                                                                                                                                 |
| -XX:SurvivorRatio                    | 8                                  | 通用             | 设置年轻代中Eden区与Survivor区的比例，默认值为8，即Eden:S0:S1=8:1:1。                                                                                                                                    |
| -XX:MaxTenuringThreshold             | 不同gc回收器默认值不同             | 通用             | 设置对象在年轻代晋升到老年代时的年龄阈值，Parallel Scavenge时默认15，CMS默认为6，G1默认为15。                                                                                                            |
| -XX:MetaspaceSize                    | 20.8M                              | 通用             | 元数据空间发生扩容时触发FullGC的初始化阈值，如配置-XX:MetaspaceSize=128M，则元数据空间大于128M时会触发FullGC，并按一定算法扩容。                                                                         |
| -XX:MaxMetaspaceSize                 | 无限大                             | 通用             | 元数据空间最大可以使用的空间大小。                                                                                                                                                                       |
| -XX:MinMetaspaceFreeRatio            | 40                                 | 通用             | 最小空闲比，当 Metaspace 发生 GC 后，会计算 Metaspace 的空闲比，如果空闲比(空闲空间/当前 Metaspace 大小)小于此值，就会触发 Metaspace 扩容。默认值是 40 ，也就是 40%，例如 -XX:MinMetaspaceFreeRatio=40。 |
| -XX:+HeapDumpOnOutOfMemoryError      | false                              | 通用             | 开启OOM自动生成DUMP文件的功能。                                                                                                                                                                          |
| -XX:ErrorFile                        |                                    | 通用             | 配置JVM Crash时输出的日志目录，这在容器环境下非常重要。配置如-XX:ErrorFile=$HOME/log/java_error_%p.log，JVM会将%p替换成pid。                                                                             |
| -XX:HeapDumpPath                     | 当前工作目录                       | 通用             | 配置DUMP文件的目录，如-XX:HeapDumpPath=$HOME/log，需要注意的目录的文件夹必须存在，JVM不会自动创建不存在的目录。                                                                                          |
| -XX:+UseConcMarkSweepGC              |                                    | **JDK 1.8**      | 指定使用CMS垃圾回收器。**（JDK 21 中已移除，不可使用）**                                                                                                                                                                                  |
| -XX:+UseCMSInitiatingOccupancyOnly   |                                    | **JDK 1.8**      | 如果未开启JVM第一次cms gc之后就按自己的规则来决定老年代当前的利用率是否会触发gc；如果开启则按照CMSInitiatingOccupancyFraction触发gc。                                                                    |
| -XX:CMSInitiatingOccupancyFraction   | 68                                 | **JDK 1.8**      | 设置CMS垃圾回收器下触发GC的阈值，默认68%，配置如-XX:CMSInitiatingOccupancyFraction=70。                                                                                                                  |
| -XX:+UseCMSCompactAtFullCollection   | true                               | **JDK 1.8**      | 开启Full GC后，进行一次整理的功能。整理过程是独占的，会引起停顿时间变长。                                                                                                                                |
| -XX:+CMSFullGCsBeforeCompaction      | 0                                  | **JDK 1.8**      | 设置进行几次Full GC后进行一次碎片整理。                                                                                                                                                                  |
| -XX:+PrintGC                         | false                              | **JDK 1.8**      | 开启打印GC简单信息功能。**（JDK 21 中已移除，请使用 -Xlog:gc）**                                                                                                                                                                                 |
| -XX:+PrintGCDetails                  | false                              | **JDK 1.8**      | 开启打印GC详细信息功能。**（JDK 21 中已移除，请使用 -Xlog:gc*）**                                                                                                                                                                                 |
| -XX:+PrintGCDateStamps               | false                              | **JDK 1.8**      | 开启GC日志中打印GC发生时具体时间的功能。**（JDK 21 中已移除，请使用 -Xlog:gc*:time）**                                                                                                                                                                 |
| -XX:+PrintGCTimeStamps               | false                              | **JDK 1.8**      | 开启GC日志中打印JVM启动的时候的相对时间的功能。**（JDK 21 中已移除）**                                                                                                                                                          |
| -Xloggc                              | 无                                 | **JDK 1.8**      | 指定GC日志路径，添加此配置默认会激活-XX:+PrintGC。配置格式如-Xloggc:$HOME/log/gc_%p.log，注意路径必须是存在的，JVM不会自动创建目录。**（JDK 21 中已移除，请使用 -Xlog:gc*:file=...）**                                                                     |
| -XX:+UseGCLogFileRotation            | false                              | **JDK 1.8**      | 开启交替在多个文件中循环打印gc日志的功能。**（JDK 21 中已移除，通过 -Xlog:gc*:file=...:filecount=... 实现）**                                                                                                                                                               |
| -XX:NumberOfGCLogFiles               | 0                                  | **JDK 1.8**      | 配置最多交替在几个文件中打印，如在10个文件中打印 -XX:NumberOfGCLogFiles=10。**（JDK 21 中已移除）**                                                                                                                             |
| -XX:GCLogFileSize                    | 8192                               | **JDK 1.8**      | 设置每个GC日志文件的上限大小，超过便触发分割，如-XX:GCLogFileSize=100M。**（JDK 21 中已移除，通过 -Xlog:gc*:file=...:filesize=... 实现）**                                                                                                                                 |
| -XX:+PrintHeapAtGC                   | false                              | **JDK 1.8**      | 开启每次GC后都打印堆信息的功能。**（JDK 21 中已移除）**                                                                                                                                                                         |
| -XX:+PrintClassHistogramBeforeFullGC | false                              | 通用             | 开启Full GC前打印对象实例直方图的功能，生产不建议默认开启，会导致GC日志很多。对性能要求比较高的应用可以开启。                                                                                            |
| -XX:+UseG1GC                         | false                              | 通用             | 指定使用G1垃圾回收器。**（JDK 21 默认即为 G1，但显式指定也是好的实践）**                                                                                                                                                                                   |
| -XX:MaxGCPauseMillis                 | 200                                | 通用             | 设置最大GC停顿时间目标（毫秒），这是一个软目标，JVM会尽力实现。G1 和 ZGC 的核心调优参数。                                                                                                                                                                                   |
| -XX:InitiatingHeapOccupancyPercent   | 45                                 | 通用             | G1 启动并发标记周期的堆占用百分比阈值（IHOP）。降低此值可以更早触发并发回收，避免 Full GC。                                                                                                                                                                                   |
| -XX:+UseZGC                          | false                              | **JDK 21**       | 启用 ZGC 垃圾回收器（JDK 21 推荐用于低延迟场景）。                                                                                                                                                                                   |
| -Xlog:gc*                            |                                    | **JDK 21**       | 统一日志参数，替代了 JDK 8 的 PrintGCDetails 等参数。例如：`-Xlog:gc*:file=gc.log:time,tags:filecount=10,filesize=100M`                                                                                                                                                                                   |
| --add-modules                        |                                    | **JDK 9+**       | 模块化系统参数，用于手动添加模块。例如 `--add-modules java.se`                                                                                                                                                                                   |
| --add-opens                          |                                    | **JDK 9+**       | 模块化系统参数，允许深度反射访问。常用于解决旧版库在 JDK 9+ 上的兼容性问题。例如 `--add-opens java.base/java.lang=ALL-UNNAMED`                                                                                                                                                                                   |
| --add-exports                        |                                    | **JDK 9+**       | 模块化系统参数，导出内部包。                                                                                                                                                                                   |
| -XX:MaxDirectMemorySize              | 0                                  | 通用             | 设置堆外内存的最大空间，一般推荐设置成2G，配置这个参数能有效避免无节制的使用堆外内存导致容器被OOMKilled的问题。                                                                                          |

#### 容器环境下虚拟机参数

| 参数名                   | 默认值   | 说明                                                                                                                                                                                                     |
| -------------------------- | ---------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| -XX:+UseContainerSupport | true     | 允许JVM 从主机读取cgroup限制，例如可用的CPU和RAM，并进行相应的配置，默认开启。                                                                                                                           |
| -XX:InitialRAMPercentage | 1.562500 | Java应用程序的初始堆大小。假设配置-XX：InitialRAMPercentage = 25并且总物理内存（或容器内存）为1GB，那么Java应用程序的堆大小将为250MB（即1GB的25％），注意若配置Xms此配置将失效。                         |
| -XX:MinRAMPercentage     | 50       | 仅当物理服务器（或容器）中的总可用内存大小小于250MB（大约）时生效，假设配置-XX：MinRAMPercentage = 50，且整体物理内存（或容器）内存为100MB，那么Java应用程序的最大堆大小将设置为50MB（即100MB的50％）。  |
| -XX:MaxRAMPercentage     | 25       | 仅当物理服务器（或容器）中的总可用内存大小大于250MB（大约）时生效，假设配置-XX：MaxRAMPercentage = 75并且物理服务器（或容器）的整体内存为1GB，那么Java应用程序的最大堆大小将设置为750MB（即1GB的75％）。 |

## 参数配置规范

### 内存分配配置规范

#### 【强制】堆初始化内存与堆最大内存保持一致

这样设置有以下优点：

- 可以让JVM在启动时就直接向OS申请堆最大内存，避免JVM在运行过程中频繁发生FullGC向OS申请内存。
- 减少应用启动初期的GC次数，尽可能的避免使用swap空间。
- 还有一个很重要的是：如果初始与最大不一样并且没有配置年轻代NewSize和NewRatio，JVM会默认取堆最大值的1/3作为NewSize，并优先分配NewSize给年轻代，剩下的初始化堆给老年代。比如-Xmx4g -Xms2g，JVM计算出NewSize为1.2g，此时初始化的年轻代为1.2g、老年代0.8g；同时如果使用的是CMS垃圾回收器的话，很有可能一直只发生cms老年代gc，不发生Full GC导致老年代无法扩容一直为0.8g。如下图中，堆内存一直维持在2g，频繁发生cms old gc，堆内存无法扩容。
  ![image](uploads/4078/66c4c4e1-45b1-4314-a423-d6428063c804/OLD_GEN_NOT_EXPAND.png)

非容器环境下将Xmx、Xms配置成一样大小即可；容器环境下不建议配置Xmx与Xms，将InitialRAMPercentage、MinRAMPercentage与MaxRAMPercentage配置成一样即可。

Oracle官方调优指南里也建议将初始堆大小配置成与最大堆大小一致，参考_附录2_ 中Table 5-2 JRockit JVM Heap Size Options部分。

#### 【强制】配置元数据区空间

JDK8默认的元数据区MetaspaceSize是20.8M，当class、方法等元数据占用的空间大于这个值时会触发Full GC，大部分应用启动发生Full GC一般是这个原因。建议观察应用正常运行时占用的元数据空间大小进行配置，如：

```bash
-XX:MetaspaceSize=256M -XX:MaxMetaspaceSize=512M
```

#### 【强制】配置年轻代与老年代比例

JVM在未配置年轻代老年代比例NewRatio及MaxNewSize等参数时，默认会取1/3堆内存 与 CPU核数*64M中的较小值作为年轻代空间的大小，剩下的作为老年代空间大小，因此核数较少的应用将可能分配到不符合预期的年轻代空间，从而频繁进行young gc。
显式的配置NewRatio则可以触发JVM重新计算老年代的空间(即使配置值为默认值2也能生效)，从而避免一些性能问题

```bash
-XX:NewRatio=2
```

#### 【建议】按需调整年轻代的比例

此处涉及会涉及两个比例:

- 第一个是年轻代与老年代的比例，默认情况下新生代与老年代的比例是1:2(该值可以通过-XX:NewRatio来指定)，即新生代=1/3的堆空间大小；
- 第二个是年轻代中Eden区与Survivor区的比例，默认的Eden:S0:S1=8:1:1(可以通过-XX:SurvivorRatio来设定)，即Eden区=8/10的新生代空间。

当出现应用长时间发生一次FullGC，并且dump文件中对象大部分都为unreachable状态时，可以考虑调大年轻代的大小以及Survivor区的大小，可以减少一些不需要进入老年代的对象(非本地缓存对象)进入老年代。
一般情况下，研发人员可以判断当前应用是否存在使用大量内存作为本地缓存以实现接口查询提速的场景。如果明确清楚应用不存在这种场景时，建议将新生代与老年代的比例改为1:1。

### 垃圾回收配置规范

#### 【建议】默认开启GC日志

GC日志记录对生产服务器性能开销非常小，官方推荐默认开启GC日志，长期记录对于分析应用程序性能绝对至关重要。必须始终启用GC日志记录，以便开发运维人员能够观察GC行为并相应地调整应用程序。

**JDK 1.8 配置：**

```bash
-XX:+PrintGCDateStamps 
-XX:+PrintGCDetails 
-XX:+PrintHeapAtGC 
-Xloggc:$HOME/log/gc_%p.log 
-XX:+UseGCLogFileRotation 
-XX:NumberOfGCLogFiles=10 
-XX:GCLogFileSize=100M 
```

**JDK 21 配置：**

```bash
-Xlog:gc*:file=$HOME/log/gc_%p.log:time,tags:filecount=10,filesize=100M
```

#### 【建议】Web应用优先使用并发垃圾回收器

进行垃圾回收器选型时通常考虑的两个指标是吞吐量和响应时间。

- 吞吐量

可以理解为(总CPU时间-STW时间)/总CPU时间，应用程序的线程执行时间越长，则吞吐量越高。

- 响应时间

可以理解为GC不要导致应用程序太长的停顿，让应用程序能够尽快执行并响应用户。

都希望有吞吐量又高、响应时间又短的垃圾回收器。但这两者是矛盾的：为了提高吞吐量，就要减少GC的运行时间，降低回收频率，扩大空间，但是就会增大每一次的停顿时间；相反需要降低响应时间，就必须提高回收的频率。

目前公司国际业务运营中心V8系列BP与UIP存在2s一次的心跳检查，V9系列使用zookeeper作为注册中心同样有session超时机制，单次停顿时间太长会出现断链或者心跳超时等问题。

**JDK 1.8 建议：**
建议提供在线接口的Java web应用可以优先使用如CMS、G1这样响应时间优先的垃圾回收器。对于离线或纯计算(如jobserver)的Java应用使用JDK8默认的parallel scavenge吞吐量优先的垃圾回收器。

**JDK 21 建议：**
推荐使用默认的 **G1** 垃圾回收器，它在 JDK 21 中经过了大幅优化，足以应对绝大多数 Web 应用场景。对于对延迟极其敏感（如交易系统、网关）的场景，强烈推荐尝试 **ZGC** (`-XX:+UseZGC`)，它可以实现亚毫秒级的停顿。

#### 【强制】关闭UseAdaptiveSizePolicy

该配置作用于JDK8默认垃圾回收器Parallel Scavenge，JVM会优先保证吞吐量来动态调整Eden、S0、S1的空间。线上长时间运行的程序经常会出现S0、S1空间被缩到很小，有的甚至几M，此时大部分对象直接入老年代，导致应用出现FullGC。

关闭方式：在JVM启动参数中添加下面参数

```bash
-XX:-UseAdaptiveSizePolicy
```

#### 【建议】超过16G内存应用优先使用G1或ZGC垃圾回收器

**JDK 1.8 环境：**
G1是一款划时代的垃圾回收器，它将堆区分成若干的region，每个region引入额外的数据结构RememberSet来记录代际间的依赖关系，采用空间换时间的方案来降低GC的停顿时间，同时还动态建立停顿预测模型来保证每次停顿时间满足设定的目标停顿时间。
堆大小配置为16G的应用，发生一次FullGC的耗时是相当恐怖的，并且16G的内存dump很难在本机通过工具打开分析。G1能够尽可能保证每次停顿时间不超过100ms，因此推荐超过16G内存的应用优先选择使用G1垃圾回收器。

Oracle建议满足下面一个或多个特性的应用，使用G1垃圾回收器：
- 超过50%的Java堆被活动数据占用。
- 对象分配率或提升率差异很大。
- 不必要的长时间垃圾收集或压缩暂停(超过0.5到1秒)
- 堆大小约为6G或更大

**JDK 21 环境：**
对于大内存应用（>16G），**ZGC** 是最佳选择。ZGC 的设计目标就是支持 TB 级堆内存且保持亚毫秒级停顿，且停顿时间不随堆大小增加而增加。如果因某些原因无法使用 ZGC，G1 依然是稳健的选择。

### 容器环境下配置规范

#### 【强制】使用感知容器CPU和Memory资源限制的JDK版本

如果JVM不能感知容器的CPU限制，将产生以下问题：

- JVM GC线程以及C2 Compiler线程线程数不正常

  GC线程的计算规则是：如果CPU核数小于等于8，GC线程数会与CPU核数一致；如果CPU核数大于8，前8个核每个核对应一个GC线程，后面每8个核对应5个GC线程。
  当GC线程过多时，会因为上下文切换或者共享资源的争抢反而增大垃圾回收的耗时。

- 诸多中间件初始化线程数不正常

  诸多中间件在创建线程池时会使用JDK提供的Runtime.getRuntime().avaliableProcessors()方法获取当前的CPU个数，从而根据CPU资源情况创建线程池。比如有些项目现场宿主机是80核，此时如果拿到宿主机CPU个数，便会因为GC线程创建过多导致在STW时上下文切换严重降低系统的性能。
  如果JVM不能感知容器的Memory限制时，容器将可能因为未配置堆最大内存被容器OOMkilled。

参考文章：
Java SE 8u131版本之后支持JVM感知docker的Memory限制见_附录3_；
Java SE 8u191版本之后支持JVM感知docker的CPU限制见_附录4_；

目前ZCM已经提供高版本JDK基础镜像，见_附录12_。

#### 【建议】容器环境下堆内存分配优先使用xxxRAMPercentage

容器环境(且jdk版本>8u191)下堆大小的分配应当优先使用InitialRAMPercentage、MinRAMPercentage、MaxRAMPercentage按照容器内存比例分配而非使用Xmx、Xms设置固定大小堆内存。
在ZCM及各种云平台上都可以给Java应用实例分配任意大小的内存上限，当我们的Java应用使用Xmx、Xms这类参数固定JVM内存大小时，则当需要动态调整堆内存大小时便会显得不灵活。同时现场经常因配置原因出现Xms大于容器内存进而Java进程被OOMKiller的故障。

#### 【强制】配置 MALLOC_ARENA_MAX (针对 Linux 环境)

在 Linux 环境下（尤其是容器中），glibc 的内存分配策略可能会导致物理内存占用（RES）持续增长，表现为内存虚高。为了避免 glibc 内存碎片问题，建议配置环境变量 `MALLOC_ARENA_MAX`。

```bash
export MALLOC_ARENA_MAX=2
```

建议值为 2 或 4。此配置能有效控制内存碎片，防止容器因 RES 过高而被 OOM Killed。

### 推荐配置

此章节提供响应时间优先与吞吐量优先的JVM参数配置，吞吐量与响应时间的概念参考_附录13_。注意对于虚拟机或者物理机上运行的Java应用必须通过配置-Xmx限制应用可分配的最大内存。

#### 【推荐】JDK 1.8 响应时间优先的应用配置(CMS垃圾回收器)

```bash
-XX:+UseContainerSupport 
-XX:InitialRAMPercentage=40.0 
-XX:MinRAMPercentage=40.0 
-XX:MaxRAMPercentage=40.0 
-XX:NewRatio=1
//容器环境下的配置

-Xmx4g
-Xms4g
-Xmn2g
//非容器环境下的配置，具体值需要按照实际情况修改

-Xss256K 
-XX:MetaspaceSize=256M 
-XX:MaxMetaspaceSize=512M 
-XX:MinMetaspaceFreeRatio=50 
-XX:+HeapDumpOnOutOfMemoryError 
-XX:ErrorFile=$HOME/log/java_error_%p.log 
-XX:HeapDumpPath=$HOME/log 
-XX:+UseConcMarkSweepGC 
-XX:+UseCMSInitiatingOccupancyOnly 
-XX:CMSInitiatingOccupancyFraction=70 
-XX:+PrintGCDateStamps 
-XX:+PrintGCDetails 
-XX:+PrintHeapAtGC 
-Xloggc:$HOME/log/gc_%p.log 
-XX:+UseGCLogFileRotation 
-XX:NumberOfGCLogFiles=10 
-XX:GCLogFileSize=100M 
-XX:+PrintCommandLineFlags
-XX:MaxDirectMemorySize=2g
```

#### 【推荐】JDK 1.8 响应时间优先的应用配置(G1垃圾回收器)

```bash
-XX:+UseContainerSupport 
-XX:InitialRAMPercentage=40.0 
-XX:MinRAMPercentage=40.0 
-XX:MaxRAMPercentage=40.0 
-XX:NewRatio=1
//容器环境下的配置

-Xmx16g
-Xms16g
-Xmn8g
//非容器环境下的配置，具体值需要按照实际情况修改

-Xss256K 
-XX:MetaspaceSize=256M 
-XX:MaxMetaspaceSize=512M 
-XX:MinMetaspaceFreeRatio=50 
-XX:+HeapDumpOnOutOfMemoryError 
-XX:ErrorFile=$HOME/log/java_error_%p.log 
-XX:HeapDumpPath=$HOME/log 
-XX:+UseG1GC
-XX:MaxGCPauseMillis=200
-XX:+UseStringDeduplication
-XX:+PrintPromotionFailure
-XX:+PrintGCDateStamps 
-XX:+PrintGCDetails 
-XX:+PrintHeapAtGC 
-Xloggc:$HOME/log/gc_%p.log 
-XX:+UseGCLogFileRotation 
-XX:NumberOfGCLogFiles=10 
-XX:GCLogFileSize=100M 
-XX:+PrintCommandLineFlags
-XX:MaxDirectMemorySize=2g
```

#### 【推荐】JDK 1.8 吞吐量优先的应用配置(JDK8默认垃圾回收器)

```bash
-XX:+UseContainerSupport 
-XX:-UseAdaptiveSizePolicy 
-XX:InitialRAMPercentage=40.0 
-XX:MinRAMPercentage=40.0 
-XX:MaxRAMPercentage=40.0
-XX:NewRatio=1
//容器环境下的配置

-Xmx4g
-Xms4g
-Xmn2g
//非容器环境下的配置，具体值需要按照实际情况修改

-Xss256K 
-XX:MetaspaceSize=256M 
-XX:MaxMetaspaceSize=512M 
-XX:MinMetaspaceFreeRatio=50 
-XX:+HeapDumpOnOutOfMemoryError 
-XX:ErrorFile=$HOME/log/java_error_%p.log 
-XX:HeapDumpPath=$HOME/log  
-XX:+PrintGCDateStamps 
-XX:+PrintGCDetails 
-XX:+PrintHeapAtGC 
-Xloggc:$HOME/log/gc_%p.log 
-XX:+UseGCLogFileRotation 
-XX:NumberOfGCLogFiles=10 
-XX:GCLogFileSize=100M 
-XX:+PrintCommandLineFlags
-XX:MaxDirectMemorySize=2g
```

#### 【推荐】JDK 21 通用平衡型配置 (G1, 默认推荐)

适用于大多数微服务、Web 应用。基于 JDK 21 默认行为，精简配置。

```bash
# 内存设置 (容器环境推荐使用 RAMPercentage)
-XX:InitialRAMPercentage=50.0 
-XX:MaxRAMPercentage=50.0 
-XX:MinRAMPercentage=50.0 

# GC 设置 (JDK 21 默认即为 G1，显式指定以防万一)
-XX:+UseG1GC
-XX:MaxGCPauseMillis=200
-XX:+UseStringDeduplication

# 日志设置 (Unified Logging)
-Xlog:gc*:file=$HOME/log/gc_%p.log:time,tags:filecount=10,filesize=100M

# 错误处理
-XX:+HeapDumpOnOutOfMemoryError 
-XX:HeapDumpPath=$HOME/log 
-XX:ErrorFile=$HOME/log/java_error_%p.log 

# 其他优化
-XX:+UseContainerSupport
-XX:MaxDirectMemorySize=2g
-Djava.security.egd=file:/dev/./urandom
```

#### 【推荐】JDK 21 超低延迟型配置 (ZGC)

适用于交易系统、网关等对延迟极其敏感的场景。

```bash
# 内存设置 (ZGC 推荐大堆，但小堆表现依然优秀)
-XX:InitialRAMPercentage=60.0 
-XX:MaxRAMPercentage=60.0 
-XX:MinRAMPercentage=60.0 

# GC 设置 (启用 ZGC)
-XX:+UseZGC
# ZGC 是自适应的，通常不需要额外调优，以下为可选高级配置
# -XX:SoftMaxHeapSize=... (设置软上限，以便在内存紧张时释放给 OS)

# 日志设置
-Xlog:gc*:file=$HOME/log/gc_%p.log:time,tags:filecount=10,filesize=100M

# 错误处理
-XX:+HeapDumpOnOutOfMemoryError 
-XX:HeapDumpPath=$HOME/log 
-XX:ErrorFile=$HOME/log/java_error_%p.log 

# 其他优化
-XX:+UseContainerSupport
-XX:MaxDirectMemorySize=2g
-Djava.security.egd=file:/dev/./urandom
```

## 内存溢出(OOM)处理与自愈机制

### OOM 异常的危害

当 JVM 内存耗尽且垃圾回收（GC）无法释放足够空间时，会抛出 `OutOfMemoryError`（OOM）异常。OOM 异常通常细分为多种场景：
* **堆内存溢出**：`OutOfMemoryError: Java heap space`
* **元空间溢出**：`OutOfMemoryError: Metaspace`
* **直接内存溢出**：`OutOfMemoryError: Direct buffer memory`
* **GC 开销过大**：`OutOfMemoryError: GC overhead limit exceeded`

一旦 JVM 抛出 OOM 异常，意味着当前进程的内存状态已遭到破坏，处于极其不稳定的状态，随时可能发生服务假死或闪崩。在这种状态下，继续让应用“带病运行”可能会导致数据不一致或更严重的级联故障。因此，最佳实践是**快速失败并自动恢复**。

### OOM 自愈配置规范

#### 【强制】配置 OOM 时自动退出进程

为防止应用在 OOM 后处于不可控状态，必须在 JVM 启动参数中添加 `-XX:+ExitOnOutOfMemoryError`。该参数可确保 JVM 在首次抛出 OOM 异常时立即终止进程，从而触发后续的自动拉起机制。

#### 【强制】配置 OOM 自动生成 Heap Dump 快照

为了在进程退出后能够追溯和分析内存泄漏的原因，必须在 JVM 启动参数中添加 `-XX:+HeapDumpOnOutOfMemoryError`，确保在 OOM 发生时自动导出堆内存快照（Heap Dump）。同时，使用 `-XX:HeapDumpPath` 参数明确指定 Dump 文件的存放路径。

配置 Dump 文件存放目录时，必须评估以下风险与要求：
1. **目录必须预先存在**：JVM 不会自动创建不存在的路径，若目录缺失将导致 Dump 失败。
2. **容器环境下的持久化**：对于容器化部署的应用，Dump 目录必须挂载为持久化卷（如 Docker Volume 或 K8s PVC），防止容器重启后丢失现场数据。
3. **磁盘容量规划**：Heap Dump 文件通常极大（经验公式为：存活对象总大小 × 1.5），例如 32G 堆上限的应用可能产生大于 32G 的快照文件。为防止写满根文件系统引发操作系统故障，建议将路径指向挂载的大容量云盘或专用的日志/数据存储卷。

#### 【强制】配置应用存活探针与自动恢复机制

无论是容器化还是传统部署，都必须建立进程状态监控与自动恢复机制。

**容器化部署场景：**
必须为容器配置存活探针（Liveness Probe）和就绪探针（Readiness Probe）。当探针检测到应用服务不可用或多次未就绪时，容器编排平台（如 Kubernetes）将根据策略自动重启容器。

以下为一个通用的探针检测脚本样例逻辑：

```bash 
#!/bin/bash 
APP=( "tomcat" ) 
tomcat=( 
     "$TOMCAT_HOME/bin/catalina.sh run & /app/appStart.sh"    # 启动命令 
     "tomcat"       # 进程关键字 
     "echo $(netstat -lpnt | grep -c -w 8080)"    # 存活检测命令 
     "1"         # 存活检测成功状态码 
     "curl -s --max-time 5 -o /dev/null -w %{response_code} http://localhost:8080/health/readiness"    # 就绪检测命令 
     "200"         # 就绪检测成功状态码 
    ) 
```

配置探针规则时，需关注以下关键参数：
1. **合理设置延迟与间隔**：初次扫描延迟（initialDelaySeconds）必须适度大于应用正常启动所需的时间，避免在启动阶段被误判并反复重启。后续扫描间隔（periodSeconds）不宜过长，以保障故障发现的及时性。
2. **检测方式区分**：存活探针通常采用轻量级的端口监听或进程检查；就绪探针则应调用专门的健康检查接口，验证应用是否已具备处理业务请求的能力。

**非容器化部署场景：**
对于物理机或虚拟机上部署的应用，严禁简单使用 Shell 后台符（如 `&` 或 `nohup`）运行 JVM 进程。建议使用标准的进程管理工具（如 `systemd`、`supervisord`）来托管应用，利用其内置的 `Restart=always` 等策略实现进程的守护与自动拉起。

## 常用工具

### 指标监控

#### ITracing

ITracing是由微服务平台团队研发的一款APM产品，除了对分布式调用进行跟踪外，ITracing还采集了应用各项性能指标(堆内存使用情况、垃圾回收情况、CPU使用情况等)，通过应用巡检与性能分析能够很直观的观测到JVM的运行情况。

##### 性能中心->应用巡检

![image](uploads/4078/3c071340-b9ff-49ae-9643-5fc9e85bdd80/APP_INSPCETION.png)
JVM内存使用监控

##### 性能中心->性能分析

![image](uploads/4078/cc06c563-bc48-4c4f-9176-36495279eb4a/PERF_ANALYSIS.png)
内存、负载、SQL等多维度性能分析

### 运维工具

#### jcmd 多功能命令行工具 (JDK 7+ / 推荐 JDK 21)

`jcmd` 是 JDK 推荐的综合性诊断命令，它整合了 `jps`, `jstack`, `jmap`, `jinfo` 等工具的大部分功能，是 JDK 21 下的“瑞士军刀”。

**常用命令示例：**

```bash
# 列出 Java 进程 (类似 jps)
jcmd

# 打印线程堆栈 (类似 jstack)
jcmd <pid> Thread.print

# 创建堆转储 (类似 jmap -dump)
jcmd <pid> GC.heap_dump <filename>

# 查看堆直方图 (类似 jmap -histo)
jcmd <pid> GC.class_histogram

# 查看系统属性 (类似 jinfo -sysprops)
jcmd <pid> VM.system_properties

# 查看 VM 标志 (类似 jinfo -flags)
jcmd <pid> VM.flags

# 强制执行 GC
jcmd <pid> GC.run
```

#### jps 虚拟机进程状态查看工具

JVM Process Status Tool；与UNIX的ps命令相似，可以列出正在运行的虚拟机进程，并显示虚拟机执行主类(MainClass，main()函数所在的类)名称以及这些进程的本地虚拟机唯一ID，该ID与操作系统进程ID一致，可以用于确定具体应用进程，众多命令的使用都要基于该命令查询到的进程ID

jps命令格式：

```bash
jps [options] [hostid]
```

jps执行样例：

```bash
scp-d766cbb54-xk6m5[/app]#jps -l
20 /app/lib/scp-web-9.0.0-SNAPSHOT.jar
29304 sun.tools.jps.Jps
```

jps可以通过RMI协议查询开启了RMI服务的远程虚拟机进程状态，hostid为RMI注册表中注册的主机名。其他常用选项见下表：

| 选项 | 作用                                               |
| ------ | ---------------------------------------------------- |
| -q   | 只输出LVMID，省略主类的名称                        |
| -m   | 输出虚拟机进程启动时传递给主类main()函数的参数     |
| -l   | 输出主类的全名，如果进程执行的是Jar包，输出Jar路径 |
| -v   | 输出虚拟机进程启动时JVM参数                        |

#### jstack 虚拟机堆栈跟踪工具

Stack Trace for Java；用于生成虚拟机当前时刻的线程快照(一般称为threaddump或者javacore文件)。线程快照就是当前虚拟机内每一条线程正在执行的方法堆栈的集合，生成线程快照的主要目的是定位线程出现长时间停顿的原因，如线程间死锁、死循环、请求外部资源导致的长时间等待都是导致长时间停顿的常见原因。线程出现停顿的时候通过jstack来查看各个线程的调用堆栈，就可以知道没有响应的线程到底在后台做什么事情，或者等待着什么资源。

jstack命令格式：

```bash
jstack [option] vmid
```

option选项的合法值与具体含义见下表：

| 选项 | 作用                                         |
| ------ | ---------------------------------------------- |
| -F   | 当正常输出的请求不被响应时，强制输出线程堆栈 |
| -l   | 除堆栈外，显示关于锁的附加信息               |
| -m   | 如果调用到本地方法的话，可以显示C/C++的堆栈  |

肉眼分析jstack快照比较费力，推荐使用IBM的jca工具分析，执行java -jar jca457.jar即可打开，效果如下
![image](uploads/4078/e9414ded-e13d-4263-b97e-689ba9b77e99/JCA457.png)

介绍链接见_附录5。_

下载链接见_附录6_。

#### jinfo 虚拟机配置信息工具

Configuration Info For Java，实时查看和调整虚拟机各项参数；该命令最大作用是可以显示未被显示指定的参数的系统默认值，可以通过jinfo -flags pid查看所有jvm参数。

命令格式：

```bash
jinfo [option] <pid>
```

option选项

| 选项        | 作用             |
| ------------- | ------------------ |
| -flag<name> | 显示指定参数的值 |
| -flags      | 显示所有JVM参数  |

执行样例:

```bash
scp-d766cbb54-xk6m5[/app]#jinfo -flags  20
Attaching to process ID 20, please wait...
Debugger attached successfully.
Server compiler detected.
JVM version is 25.212-b04
Non-default VM flags: -XX:CICompilerCount=3 -XX:CMSInitiatingOccupancyFraction=70 -XX:CompressedClassSpaceSize=528482304 -XX:ErrorFile=null -XX:GCLogFileSize=52428800 -XX:+HeapDumpOnOutOfMemoryError -XX:HeapDumpPath=null -XX:InitialHeapSize=6442450944 -XX:InitialRAMPercentage=null -XX:MaxHeapSize=6442450944 -XX:MaxMetaspaceSize=536870912 -XX:MaxNewSize=348913664 -XX:MaxRAMPercentage=null -XX:MaxTenuringThreshold=6 -XX:MetaspaceSize=536870912 -XX:MinHeapDeltaBytes=196608 -XX:MinMetaspaceFreeRatio=50 -XX:MinRAMPercentage=null -XX:NewSize=348913664 -XX:NumberOfGCLogFiles=5 -XX:OldPLABSize=16 -XX:OldSize=6093537280 -XX:+PrintClassHistogramBeforeFullGC -XX:+PrintGC -XX:+PrintGCDateStamps -XX:+PrintGCDetails -XX:+PrintGCTimeStamps -XX:ThreadStackSize=256 -XX:-UseAdaptiveSizePolicy -XX:+UseCMSInitiatingOccupancyOnly -XX:+UseCompressedClassPointers -XX:+UseCompressedOops -XX:+UseConcMarkSweepGC -XX:+UseContainerSupport -XX:+UseGCLogFileRotation -XX:+UseParNewGC 
Command line:  -XX:+UseContainerSupport -XX:-UseAdaptiveSizePolicy -XX:InitialRAMPercentage=40.0 -XX:MinRAMPercentage=40.0 -XX:MaxRAMPercentage=40.0 -Xss256K -XX:MetaspaceSize=256M -XX:MaxMetaspaceSize=512M -XX:MinMetaspaceFreeRatio=50 -XX:+HeapDumpOnOutOfMemoryError -XX:HeapDumpPath=/tmp/zcore -XX:+PrintGC -XX:+PrintGCDateStamps -XX:+PrintGCTimeStamps -XX:+PrintGCDetails -Xloggc:/tmp/log/gc.log -XX:+UseGCLogFileRotation -XX:NumberOfGCLogFiles=10 -XX:GCLogFileSize=50M -javaagent:/APM/pinpoint-agent/pinpoint-bootstrap-1.7.3.jar -Dpinpoint.agentId=010045004064_41574_1 -Dpinpoint.applicationName=zcm_scp -Dpinpoint.dockerId=876c9204971d -Dpinpoint.localhostIp=10.45.4.64 -XX:InitialRAMPercentage=75.0 -XX:MinRAMPercentage=75.0 -XX:MaxRAMPercentage=75.0 -XX:MetaspaceSize=512m -XX:MaxMetaspaceSize=512m -XX:+HeapDumpOnOutOfMemoryError -XX:ErrorFile=/log/java_error_%p.log -XX:HeapDumpPath=/log -XX:+UseConcMarkSweepGC -XX:+UseCMSInitiatingOccupancyOnly -XX:CMSInitiatingOccupancyFraction=70 -XX:+PrintGCDateStamps -XX:+PrintGCTimeStamps -XX:+PrintGCDetails -Xloggc:/log/gc_%p.log -XX:+UseGCLogFileRotation -XX:NumberOfGCLogFiles=5 -XX:GCLogFileSize=50M -XX:InitialRAMPercentage=75.0 -XX:MinRAMPercentage=75.0 -XX:MaxRAMPercentage=75.0 -XX:MetaspaceSize=512m -XX:MaxMetaspaceSize=512m -XX:+HeapDumpOnOutOfMemoryError -XX:ErrorFile=/log/java_error_%p.log -XX:HeapDumpPath=/log -XX:+UseConcMarkSweepGC -XX:+UseCMSInitiatingOccupancyOnly -XX:CMSInitiatingOccupancyFraction=70 -XX:+PrintGCDateStamps -XX:+PrintGCTimeStamps -XX:+PrintGCDetails -Xloggc:/log/gc_%p.log -XX:+UseGCLogFileRotation -XX:NumberOfGCLogFiles=5 -XX:GCLogFileSize=50M -Dspring.config.location=/app/ZSMART_HOME/application.properties
```

jinfo有一个比较好用的场景是：当我们生产上的应用很久发生一次full gc，并且启动时没有显式配置HeapDumpBeforeFullGC时，我们可以通过下面命令来使下次full gc自动生成堆内存dump，这在分析生产上full gc问题比较好用，但注意dump文件生成后需要关闭自动dump，防止磁盘被占满。

开启自动dump:

```bash
jinfo -flag +HeapDumpBeforeFullGC <pid>
```

关闭自动dump:

```bash
jinfo -flag -HeapDumpBeforeFullGC <pid>
```

#### jstat 虚拟机统计信息监视工具

JVM Statistics Monitoring Tool；是用于监视虚拟机各种运行状态信息的命令行工具。它可以显示本地或者远程虚拟机进程中类装载、内存、垃圾回收、JIT编译等运行数据。

命令格式：

```bash
jstat [ option vmid [interval[s|ms]] [count]]
```

对于命令格式中的VMID与LVMID需要特别说明一下：如果是本地虚拟机进程，VMID与LVMID是一致的，如果是远程虚拟机进程，那VMID的格式应当是：

```bash
[protocol:][//]lvmid[@hostname[:port]/servername]
```

参数interval和count表示查询间隔和次数，如果省略这两个参数，说明只查询一次。假设需要每2000ms查询一次进程20的垃圾收集情况，一共查询5次，那命令和效果如下：

```bash
scp-d766cbb54-xk6m5[/app]#jstat -gcutil 20 2000 5
  S0     S1     E      O      M     CCS    YGC     YGCT    FGC    FGCT     GCT   
  0.00 100.00  91.20  66.69  94.36  92.61   1873  305.322     4    1.144  306.466
  0.00 100.00  91.22  66.69  94.36  92.61   1873  305.322     4    1.144  306.466
  0.00 100.00  91.25  66.69  94.36  92.61   1873  305.322     4    1.144  306.466
  0.00 100.00  94.98  66.69  94.36  92.61   1873  305.322     4    1.144  306.466
 70.60   0.00   6.43  66.90  94.36  92.61   1874  305.436     4    1.144  306.580
```

选项option代表着用户希望查询的虚拟机信息，主要分为3类：类装载、垃圾收集和运行期编译情况，具体选项及作用见下表：

| 选项              | 作用                                                                                                                                                                                                            |
| ------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| -class            | 监视类装载、卸载数量、总空间以及类装载所耗费的时间                                                                                                                                                              |
| -gc               | 监视Java堆状况，包括Eden区、两个survivor区、老年代、元数据区的容量、已用空间、GC时间合计信息。如果JVM运行期间出现较长的停顿问题，可以根据该命令大致判断是否由于GC导致，并可以结合gc日志调整堆区中各区域的占比。 |
| -gccapacity       | 监视内容与-gc基本相同，但输出主要关注Java堆各个区域使用到的最大、最小空间                                                                                                                                       |
| -gcutil           | 监视内容与-gc基本相同，但输出主要关注已使用空间占总空间的百分比                                                                                                                                                 |
| -gccause          | 与-gcutil功能相同，但是会额外输出上一次导致GC产生的原因                                                                                                                                                         |
| -gcnew            | 监视新生代GC状况                                                                                                                                                                                                |
| -gcnewcapacity    | 监视内容与-gcnew基本相同，输出主要关注使用到的最大、最小空间                                                                                                                                                    |
| -gcold            | 监视老年代GC状况                                                                                                                                                                                                |
| -gcoldcapacity    | 监视内容与-gcold基本相同，输出主要关注使用到的最大、最小空间                                                                                                                                                    |
| -gcmetacapacity   | 输出元数据区使用的状况                                                                                                                                                                                          |
| -compiler         | 输出JIT编译器编译过的方法、耗时等信息                                                                                                                                                                           |
| -printcompilation | 输出已经被JIT编译的方法                                                                                                                                                                                         |

由于该命令打印内容比较多，篇幅有限更多详细信息可以参考官方文档，链接见_附录7_。

#### jmap 虚拟机内存映像工具

Memory Map for Java；用于生成堆转存快照(一般称为heapdump或dump文件)或查询finalize执行队列、Java堆和元数据区的详细信息。

命令格式:

```bash
jmap [option] pid
```

option选项的合法值与具体含义

| 选项           | 作用                                                                                                        |
| ---------------- | ------------------------------------------------------------------------------------------------------------- |
| -dump          | 生成Java堆转存快照。格式为：-dump:[live,]format=b,file=<filename>，其中live子参数说明是否只dump出存活的对象 |
| -finalizerinfo | 显示在F-Queue中等待执行finalize方法的对象                                                                   |
| -heap          | 显示Java堆详细信息，如使用哪种回收器、参数配置、分代状况等                                                  |
| -histo[:live]  | 以histogram的形式展示堆中对象统计信息，包括类、实例数量、合计容量，其中live子参数说明只统计存活的对象       |
| -clstats       | 以ClassLoader为统计口径显示类加载的状态                                                                     |
| -F             | 当虚拟机进程对-dump选项没有响应时，可使用这个选项强制生成dump快照                                           |

常用命令(如生成dump文件)

```bash
jmap -dump:format=b,file=<filename> <pid>
```

更多详细信息参考官方文档，链接见_附录8_。

#### jvisualvm 多合一故障处理工具

All-in-One Java Troubleshooting Tool；是随JDK发布的功能最强大的免费的运行监视和故障处理程序(jmc只有oracle jdk才能使用)，它除了运行监视、故障处理外还支持性能分析功能，并且不需要监视的程序基于特殊Agent运行，因此它对应用程序的实际性能影响更小，它同样支持远程分析任意一个JVM实例。

**注意：** 在高版本 JDK (如 JDK 9+) 中，VisualVM 可能不再默认捆绑，需要单独下载或使用 VisualVM 的开源版本。同时，推荐尝试 **JDK Mission Control (JMC)** 作为更专业的替代方案。

使用起来比较方便，直接执行jvisualvm命令即可打开，效果如下：
![image](uploads/4078/9809ab6d-6bdd-4aaa-9add-a9583f96b13f/JVISUALVM.png)

官方文档见_附录9_。

#### JDK Mission Control (JMC) 实时监控与分析工具

JDK Mission Control (JMC) 是一个先进的生产级 Java 监控和诊断工具套件。它最初是 Oracle JDK 的商业特性，自 JDK 11 起开源（OpenJMC）。JMC 以极低的性能开销著称，非常适合生产环境的实时监控和历史数据分析。

**核心功能：**

1. **Java Flight Recorder (JFR) 飞行记录器**：

   * **低开销记录**：JFR 深度集成在 JVM 内部，开启后对应用性能影响极小（通常 < 1%），适合在生产环境常态化开启。
   * **黑盒分析**：能够记录 JVM 的各种事件（GC、锁竞争、IO、线程、CPU 热点等），并将数据保存到文件中，用于事后回放和分析。
   * **事件详情**：提供比普通 Profiler 更深度的 JVM 内部视角，如 TLAB 分配、Code Cache 状态、Safepoint 原因等。
2. **JMX 控制台**：

   * 提供实时的 MBean 浏览、属性修改、触发器设置等功能，类似于 VisualVM 的 MBean 插件但更强大。

**使用场景：**

* **生产环境故障排查**：通过分析生产环境导出的 JFR 文件，定位偶发的性能抖动、内存泄漏或 CPU 飙升问题。
* **性能调优**：利用热点方法分析（Method Profiling）和内存分配分析，优化代码执行效率。

**如何使用：**

1. **启动 JMC**：

   * 下载并解压 JMC（JDK 11+ 通常需要单独下载）。
   * 运行 `jmc` 命令启动图形化界面。
2. **开启 JFR 记录**：

   * **启动时开启**：在 JVM 启动参数中添加 `-XX:StartFlightRecording=disk=true,dumponexit=true,filename=recording.jfr`。
   * **运行时开启**：使用 `jcmd <pid> JFR.start name=my_recording filename=my_recording.jfr duration=60s`。
3. **分析记录**：

   * 在 JMC 界面中选择 "File" -> "Open File" 打开 `.jfr` 文件。
   * 利用左侧的 "Automated Analysis Results"（自动分析结果）快速发现潜在问题（如死锁、热点方法、GC 停顿过长）。

**注意：** 建议在 JDK 11 及以上版本配合使用 JMC 和 JFR，体验最佳。JDK 8 (u262+) 虽然也反向移植了 JFR 功能，但可能需要额外的商业授权（Oracle JDK）或使用特定发行版（如 Zulu, Corretto 等 OpenJDK 下游版）。

更多信息参考_附录15_中的官方使用文档。

#### Eclipse MAT 堆内存分析工具

Memory Analysis Tool；是一种JVM堆内存镜像分析工具，该工具可以解析内存镜像文件，提供多种展示方式查看所有对象实例信息，支持OQL对象查询语句以及展示GCRoot Unreachable的对象实例，是内存泄漏的诊断首选工具，使用方法参考官方文档见_附录10_。
![image](uploads/4078/f71497ec-0e95-4c3c-a948-1fbf6cecb2a7/MAT.png)

#### Arthas 性能诊断工具

Arthas是阿里巴巴开源的一款诊断工具，它支持以下强大功能：

- JVM中类搜索、类反编译
- ognl表达式对静态变量修改
- 监控JVM的实时运行状态
- 快速定位应用的热点方法，生成火焰图
- 跟踪方法观察方法的成功失败率、耗时、出入参数等信息

![image](uploads/4078/4d6822fa-daf5-491d-b9d7-53212d581aa8/ARTHAS.png)

更多信息参考_附录11_中的官方使用文档。

#### GCViewer GC日志分析工具

GCViewer是一款开源的GC日志可视化分析工具。项目的 GitHub 主页对各项指标进行了完整的描述，使用该工具可以帮助开发人员发现jvm垃圾回收中的潜在问题。

![image](uploads/4078/97d34136-5be3-4762-9c6c-92c3a445ac39/GCVIEW_1.png)
![image](uploads/4078/6525641e-bb84-4fd6-9947-c7c9e84cd780/GCVIEW_2.png)

下载及更多详细信息见_附录14_。

#### 其他工具

其他常用工具有JProfiler、JITWatch、NMT（Native Memory Tracking）等，可自行网上查阅资料了解。

## 常见问题

### 使用CMS垃圾回收器之后怎么看到的FullGC变多了？

CMS垃圾回收器会对老年代进行concurrent gc，它不是Full GC。但是由于JVM代码演进的问题，会将old gc也算成fgc。这点通过JMX或者jstat去分析时会造成很大困扰。这种情况下判断是否真实发生Full GC则需要在gc日志中使用'Full GC'作为关键字搜索，如果仅有'CMS Initial Mark'等字样则仅仅是老年代gc。一般真正需要放到老年代的数据为一些缓存对象，如果明确清楚不会有大量缓存的话，出现cms old gc也需要进行分析。一般是晋升年龄问题，CMS下默认晋升年龄是6，可以适当调大。

### 配置了一些虚拟机参数但是不生效？

ZCM的基础镜像中提供了一些虚拟机参数，出现这种问题时可以进入容器中通过ps -ef|grep java命令查看完整的参数，OpenJDK下排在后面的参数会覆盖之前的参数，出现这种问题可能需要调整基础镜像解决。

## 附录

### 附录1 JVM基础知识

参考资料：
1)、国外GC Handbook的翻译版
[https://bdgg4p.yuque.com/docs/share/f4b59b2d-511e-40cf-a906-db13e770543e?#](https://bdgg4p.yuque.com/docs/share/f4b59b2d-511e-40cf-a906-db13e770543e?#)
2)、JAVA规范组推荐丛书《码出高效》第四章 "走进JVM"

### 附录2 官方jvm调优手册

[https://docs.oracle.com/cd/E15523_01/web.1111/e13814/jvm_tuning.htm#PERFM164](https://docs.oracle.com/cd/E15523_01/web.1111/e13814/jvm_tuning.htm#PERFM164)

### 附录3 JDK8u131支持感知容器Memory文档

[https://blogs.oracle.com/java-platform-group/java-se-support-for-docker-cpu-and-memory-limits](https://blogs.oracle.com/java-platform-group/java-se-support-for-docker-cpu-and-memory-limits)

### 附录4 JDK8u191支持感知容器CPU文档

[https://www.oracle.com/java/technologies/javase/8u191-relnotes.html](https://www.oracle.com/java/technologies/javase/8u191-relnotes.html)

### 附录5 jstack分析工具官方文档

[https://www.ibm.com/support/pages/java-core-debugging-using-ibm-thread-and-monitor-dump-analyzer-java](https://www.ibm.com/support/pages/java-core-debugging-using-ibm-thread-and-monitor-dump-analyzer-java)

### 附录6 jstack分析工具下载地址

ftp://public.dhe.ibm.com/software/websphere/appserv/support/tools/jca/jca457.jar

### 附录7 jstat官方文档

[https://docs.oracle.com/javase/8/docs/technotes/tools/windows/jstat.html](https://docs.oracle.com/javase/8/docs/technotes/tools/windows/jstat.html)

### 附录8 jmap官方文档

[https://docs.oracle.com/javase/8/docs/technotes/tools/windows/jmap.html](https://docs.oracle.com/javase/8/docs/technotes/tools/windows/jmap.html)

### 附录9 jvisualvm官方文档

[https://docs.oracle.com/javase/8/docs/technotes/tools/windows/jvisualvm.html](https://docs.oracle.com/javase/8/docs/technotes/tools/windows/jvisualvm.html)

### 附录10 Eclipse MAT官方文档

[https://help.eclipse.org/2021-06/index.jsp?topic=/org.eclipse.mat.ui.help/welcome.html](https://help.eclipse.org/2021-06/index.jsp?topic=/org.eclipse.mat.ui.help/welcome.html)

### 附录11 Arthas官方文档

[https://arthas.aliyun.com/doc/](https://arthas.aliyun.com/doc/)

### 附录12 ZCM JDK基础镜像信息

目前ZCM提供了带JVM参数的基础镜像10.45.80.1/public/centos7.6-java8-tomcat9-zcmex:1.8.0.272_9.0.43与不带JVM参数的基础镜像10.45.80.1/public/centos7.6-java8-tomcat9-base:1.8.0.272_9.0.43，具体参考下面链接。
[https://dev.iwhalecloud.com/doc/bidYNy/didnjC](https://dev.iwhalecloud.com/doc/bidYNy/didnjC)

### 附录13 GC中的吞吐量与响应时间

吞吐量：用户代码时间/(用户代码时间+垃圾回收时间)
响应时间：STW越短，响应时间越少

当产生垃圾的速度不变时，堆内存越大，垃圾回收时间便会越长。
举个例子：一个服务原本是10s收集一次，每次停顿100ms；然后通过优化(比如减小堆内存)，5s收集一次，停顿时间70ms。然后通过计算，响应时间降低了，但是吞吐量却下降了，因为10s内真正的工作时间下总的停顿时间上去了。再以写代码与答疑作为场景举个例子，把写代码当成业务线程执行，把答疑当成GC的STW，不停的有人来问问题，每个小时答复一次消息与每5分钟回复一次消息带来的上下文切换的损耗也是不一样的，最终写出来的代码数量和质量也不一样。
而CMS便是一种追求低响应时间的垃圾回收器，它会提前对老年代进行回收，并且尽可能让gc线程与用户线程能够真正的并行工作，但结果是增加了STW的频率降低了吞吐量。JDK8默认的Parallel Scavenge则相反，它会将GC工作都积压到最后处理。

### 附录14 GCViewer相关信息

简易教程：[https://www.jdkdownload.com/gcviewer_tutorials.html](https://www.jdkdownload.com/gcviewer_tutorials.html)
下载地址：[https://github.com/chewiebug/GCViewer/tags](https://github.com/chewiebug/GCViewer/tags)

### 附录15 JMC官方文档

[https://www.oracle.com/java/technologies/jdk-mission-control.html](https://www.oracle.com/java/technologies/jdk-mission-control.html)

# 本文件评审、修正记录

| 文件名称 | Java虚拟机运维规范                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    |               |               |         |
| -------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------- | ------------- | ------- |
| 序号     | 流程                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                | 拟制人/审核人 | 拟制/审核时间 | 版本号  |
| 1        | 编写                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                | 何永进/刘林        | 2018/10/20    | V1.0    |
| 2        |  增加 JDK 9+，JDK 21 相关内容，包括模块化、G1GC调优、MALLOC_ARENA_MAX配置等<br>新增章节 5. 内存溢出(OOM)处理与自愈机制                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       | 何永进        | 2026/03/19    | V1.0.1    |
| 3        | 发布                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                | Java规范组    | 2026/03/23    | V1.1    |
