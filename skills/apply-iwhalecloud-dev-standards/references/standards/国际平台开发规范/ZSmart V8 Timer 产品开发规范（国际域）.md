![image](uploads/236284/2b0cbe17-3839-4ac2-9683-afaea0f8a7d2/image.png)

# 前言

## 规范目的

为规范业务侧对 Timer 定时任务产品的使用方式，提升Timer定时任务执行稳定性与系统可靠性，特制定本规范。

## 适用范围

本规范适用于公司内部所有基于 Timer 处理一次性定时任务的业务团队，覆盖任务设计、接口调用、配置部署等场景。

# 产品简介

## 产品概述

Timer 是平台技术部框架团队设计和研发的一款轻量级定时任务调度类产品，相比于 JobServer 用以处理周期性任务，Timer 主要处理一次性任务，例如：租户欠费提醒。

![image](uploads/77864/66c383b1-9c23-40cb-95fd-6242836e97a7/image.png)

* **TimerClient** : 客户端模块，负责与TimerServer通信，发布和管理任务。
* **TimerServer** : 服务端模块，负责任务的调度、执行和监控。

## 产品特点

1. **轻量级设计** ：Timer作为一款轻量级定时任务调度类产品，旨在提供简洁高效的任务调度能力。
2. **秒级精度调度** ：提供高精度的时间控制能力，能够确保任务在预定的确切时间执行，精度可达秒级。
3. **一次性任务处理** ：与周期性任务调度系统不同，Timer专注于处理一次性任务，例如发送租户欠费提醒等。
4. **任务发布与管理** ：通过TimerClient，用户可以方便地发布新任务和管理现有任务。
5. **故障容错** ：内置容错模块，确保任务在出现异常时能够得到妥善处理，而不影响到业务主流程。
6. **易于集成** ：Timer提供简单的API和客户端库，方便与业务系统进行集成。

## 适用场景

一次性任务，典型场景如：发送用户提醒，如租户欠费提醒、触发停机、短信通知等。

# 任务设计规范

## 任务类型限制

* **仅支持一次性任务**：Timer 专注于处理一次性定时任务，严禁用于周期性任务场景（此类场景需使用 JobServer）。

# 接口开发规范

## 客户端接口开发规范

### 同步接口

* 同步接口（TimerClient）默认超时时间为 10 秒，**禁止在高并发业务场景使用**，避免业务线程阻塞导致系统吞吐量下降。
* 允许场景：低并发、对任务执行结果实时依赖的场景（如同步确认任务是否发布成功）；
* 禁止场景：秒杀、批量任务发布等高并发场景。

同步接口为 `TimerClient `，使用同步接口在超时时间（默认：10秒）抵达前会导致业务线程阻塞，同步等待 Timer 调用的返回结果。

```java
public final class TimerClient {
 /**
 * Description: 发布⼀个定时任务请求到TimerServer <br>
 * 
 * @param taskPublishReq 定时任务<br>
 * @return <br>
 * @throws BaseAppException <br>
 */
 public static Long publish(TaskPublishRequest taskPublishReq) throws BaseAppException {
 // 省略代码细节
 }
 /**
 * 
 * Description: 删除尚未运⾏的定时器任务，通过业务主键删除任务时会删除该业务主键关联的所有未完成的任务 <br> 
 * 
 * @param businessKey 业务主键 <br>
 * @throws BaseAppException <br>
 */
 public static void remove(String businessKey) throws BaseAppException {
 // 省略代码细节
 }
}
```

### 异步接口

* 异步接口（TimerAsyncClient）为推荐使用方式，需严格遵守线程池配置规范，不得随意修改默认核心参数。
* 核心要求：
  1. 线程池核心参数调整需经过性能测试验证，避免核心线程数配置过低或过高；
  2. 队列大小需保持与最大线程数匹配，禁止配置无界队列（防止内存溢出）；
  3. 拒绝策略选择需结合业务容错需求，自定义拒绝策略需实现 RejectedExecutionHandler 接口并标注版本依赖。

异步接口为 `TimerAsyncClient`，使用异步接口不会导致业务线程阻塞，真实的 Timer 调用请求会转交给独立的线程池进行处理，并且调用结果不会对业务线程产生任何影响。

```java
public final class TimerAsyncClient {
 /**
 * Description: 获取客户端实例 <br>
 * 
 * @return 客户端实例<br>
 */
 public static TimerAsyncClient getInstance() {
      return AsyncClientProvider.INSTANCE;
 }
 /**
 * Description: 发布⼀个定时任务请求到TimerServer <br>
 * 
 * @param taskPublishRequest 定时任务<br>
 * @throws BaseAppException <br>
 */
 public void publish(TaskPublishRequest taskPublishRequest) throws BaseAppException {
 // 省略代码细节
 }
 /**
 * 
 * Description: 删除尚未运⾏的定时器任务，通过业务主键删除任务时会删除该业务主键关联的所有未完成的任务
<br> 
 * 
 * @param businessKey 业务主键 <br>
 * @throws BaseAppException <br>
 */
 public void remomve(String businessKey) throws BaseAppException {
 // 省略代码细节
 }
}
```

#### 默认线程池配置

`TimerAsyncClient `提供了默认的线程池实现，核心线程数默认为：`20`，最大线程数默认为：`60`，线程存活时间为 `60`秒，默认使用有界队列 `ArrayBlockingQueue`存放待执行的任务，队列大小默认为 `60`，当线程池和队列都满时，默认丢弃最旧未处理的任务，并尝试重新提交新任务，也就是默认采用 `DiscardOldestPolicy `的拒绝策略。

> 可以通过修改配置的方式调整上述默认值，相关配置参考本文后续章节。

# 配置规范

## 配置说明

### 通用配置

#### RMI配置

RMI作为通用配置在客户端和服务端都需要配置。以下配置用于配置服务端信息，例如：IP和端口；如果配置错误，客户端将无法与服务端正常通信。

```properties
# timer.propertites
#server host ip
timer.rmi.registryHost=127.0.0.1
#server rmi port
timer.rmi.registryPort=8000
#server rmi registry name
timer.rmi.registryname=RMI_TIMER_SERVICE
```

### 客户端配置

#### Socket超时配置

用于配置客户端的超时时间，如果不配置，则默认为10秒；该值根据实际业务需要进行调整，不建议配置过大，以免导致业务线程的长时间阻塞（同步接口的情况下）。

> 同步接口和异步接口都适用。

```properties
# timer.propertites
# Socket timeout, unit: milliseconds, default value: 10000
timer.rmi.socketTimeout=10000
```

#### 异步接口线程池配置

> 本配置仅对异步接口生效。

框架为异步接口提供了默认的线程池，并且提供了默认的线程池大小，队列和拒绝策略，默认配置如下。

***特别说明下线程池的拒绝策略，除了提供默认的四种拒绝策略外，业务侧可以通过配置的方式指定自定义的拒绝处理策略**。*

- `DiscardOldestPolicy`（**默认策略**）：如果线程池满了，并且任务队列也满了，那么丢弃队列中最老的任务（即最早进入队列但尚未执行的任务），然后尝试再次提交当前任务。这种策略适用于那些可以容忍丢失一些旧任务的场景。
- `DiscardPolicy`：当任务被拒绝时，直接丢弃该任务，不会抛出异常。这种策略下，任务的丢失是无声无息的，可能不适用于所有场景。
- `AbortPolicy`：当任务太多，无法被线程池及时处理时，会抛出 `RejectedExecutionException`。
- `CallerRunsPolicy`：如果线程池无法处理任务，那么调用 `execute` 方法的线程（提交任务的线程）将尝试自己执行这个任务，相当于同步执行。
- `自定义`：除了上述四种标准拒绝策略外，开发者还可以通过实现 `RejectedExecutionHandler` 接口来定义自己的拒绝策略，以满足特定的业务需求。

```properties
# timer.propertites
# the number of threads to keep in the pool, even if they are idle
timerClient.publisTask.threadPool.coreSize=20
# the maximum number of threads to allow in the pool
timerClient.publisTask.threadPool.maxSize=60
# when the number of threads is greater than the core, this is the maximum time that excess idle threads will wait 
for new tasks before terminating. unit: seconds.
timerClient.threadPool.thread.keepAlive.time=60
# the capacity of this queue
timerClient.threadPool.queue.size=60
# the handler to use when execution is blocked because the thread bounds and queue capacities are reached
# you can configure: DiscardOldestPolicy, DiscardPolicy, AbortPolicy, or CallerRunsPolicy. 
# you can also configure your custom Handler, such as: com.iwhalecloud.bss.TimerRejectPolicy.
timerClient.threadPool.rejectedExecutionHandler=DiscardOldestPolicy
```

### 服务端配置

服务端提供了扫描间隔、业务处理线程池大小等相关配置，默认配置如下。

#### Worker线程池配置

服务端用于执行定时任务的核心线程池，直接决定 Server 端的任务执行能力；线程数不足会导致任务延迟，队列过小会导致任务被丢弃。

```properties
# timer.propertites
# worker thread pool size
timer.threadPool.threadCount=20
# worker thread pool queue size
timer.threadPool.queueSize=20
```

#### 加载周期配置

服务端不会实时查询所有待执行任务，而是**提前加载未来一个 “加载周期” 内的任务到内存**（如加载未来 4 小时的任务），避免频繁查询数据库；“加载周期” 就是这个 “提前加载的时间范围”。

```properties
# timer.propertites
# task load cycle, unit default hour
timer.task.loadCycle=4
# load unit : 11-HOUR_OF_DAY 12-MINUTE 13-SECOND
timer.task.loadUnit=11
```

#### 恢复时长配置

“恢复时长”是指当前加载周期的前一个周期，为了避免前一个周期有任务执行异常或者执行遗漏，Timer会补全加载当前周期时间点之前的未执行任务。

```properties
# timer.propertites
# Recovery cycle duration value: Used to specify the length of the time range for TimerServer to supplementarily load "unexecuted/failed tasks from the previous cycle". The unit is defined by timer.task.recoveryUnit.
# Default value: 4; 
timer.task.recoveryCycle=4
# Recovery cycle time unit: 11-HOUR_OF_DAY 12-MINUTE 13-SECOND
timer.task.recoveryUnit=11
```

#### 容量配置

> 为避免加载过量的数据导致Timer Server内存溢出，框架从 `ZSmart_CORE_R8.0.94`版本起引入容量限制机制；配置前请先确定版本，过低的版本不会生效；

“容量”指 `Timer Server`单个加载周期（默认4小时，可配）能够加载的定时任务数量上限。如果下个加载周期的定时任务数量大于容量上限，则跳过此次加载，同时发送critical的告警。功能默认关闭，推荐单周期容量在 50000 以内。

> 告警是通过 Mon.log 输出，需要配合ZMC的日志告警功能才能正常发送。

```properties
# timer.propertites
# enable or disable the "capacity limit" feature.
timer.task.limitEnable=false
# The capacity limit for one loading cycle of the timer . 50,000 by default. If this limit is exceeded, the timer will skip the current load and send a alarm.
timer.task.limit=50000
```

# 技术规格

## 容量评估准则

- **以最大用户量和业务峰值为基准**：容量配置需考虑 **未来最大用户量 / 业务峰值** 为基准，禁止仅依据当前用户量或任务量估算（如当前 100 万用户对应 50 万任务 / 周期，若规划未来用户量增至 300 万，需按 “300 万用户对应的任务峰值” 估算容量，而非维持当前 50 万上限）。
- **业务突发场景的应对**：若业务存在促销、会员日等可能引发任务量激增的场景（如促销活动需给 100 万用户发送定时短信提醒，远超日常 50 万任务量），需提前完成容量评估，即使调整配置。
- **容量冗余预留**：所有环境的容量配置需预留 **20% 冗余**（即实际配置的任务上限 = 估算最大任务量 × 1.2），避免因业务波动（如促销活动参与率超预期）导致容量不足。

## 内存配置基线

Timer Server 的高效运作依赖于其能够预先加载周期性任务列表的能力。这一机制对服务器的内存容量提出了较高的要求。内存配置不仅决定了Timer Server能够处理的任务数量，而且还直接影响到整体的性能和稳定性。

为了确保Timer Server能够满足您的业务需求，我们建议用户在部署前进行详尽的评估。请根据任务的复杂性、预期的并发量以及所需的任务调度频率，合理规划内存资源。

我们提供了不同内存配置下的容量参考基线，以帮助用户做出更加明智的决策。适当的内存配置可以避免因超出容量限制而导致的OutOfMemoryError（OOM）问题，确保Timer Server的持续稳定运行。

> 不推荐单周期容量上线配置超 50000，如果超过这个阈值，需要做性能测试，同时参考下面的基线设置内存（最终内存配置要以性能测试结果为准）。

| 内存配置 | 单周期容量 |
| -------- | ---------- |
| -Xmx4G   | 5万        |
| -Xmx8G   | 10万       |
| -Xmx16G  | 20万       |
| -Xmx32G  | 30万       |

# 本文件评审、修正记录

| 文件名称 | Timer开发规范 |                                     |               |        |
| -------- | ------------- | ----------------------------------- | ------------- | ------ |
| 序号     | 流程          | 拟制人/审核人                       | 拟制/审核时间 | 版本号 |
| 1        | 编写，输出《ZSmart V8 Timer产品用户手册.pdf》,并面向干系单位发起隐患整改单     | 沈维建、韩瑞卿/何永进、国际后端框架SCCB       | 2024/06/21    | V0.1   |
| 2        | 根据《ZSmart V8 Timer产品用户手册.pdf》 进行规范在线化，完善容量评估等内容     | 何永进/国际后端框架SCCB        | 2025/11/18    | V0.2   |
| 3        | 在线版规范发布     | 国际后端框架SCCB        | 2025/11/20    | V1.0   |
