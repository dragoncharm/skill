![image](uploads/259160/339f5d3a-a8b1-4b3b-9141-fc44befd138d/image.png)

## 规范目的

为规范业务侧对 **ZMQ** 的使用方式，规避消息丢失、乱序、重复等问题，同时明确产品适用场景，降低运维成本，提升消息链路的可靠性与稳定性，特制定本规范。

## 适用范围

本规范适用于公司内部（国际域）所有基于 **ZMQ** 进行消息生产与消费的业务产品团队，覆盖消息发送和消费、Topic与分组配置、技术选型等场景。

> **说明**：跟 JAVA 编码规范不同，ZMQ 产品开发规范不属于语言类型的开发规范，没办法提供类似于 PMD、CheckStyle、Findbugs 等代码检查工具进行自动化扫描，需开发人员在编码与 Code Review 时主动遵循。

## 版本基础

本规范基于 **ZMQ Client 9.0.30+** 制定，所有业务产品需确保使用平台统一发布的 ZMQ 客户端版本进行开发，**禁止使用其它未经平台许可的社区版客户端进行开发和对接，否则兼容性和稳定性无法得到保证**。

## 产品适用范围

ZMQ 的核心使用场景为：**削峰填谷、异步解耦、跨系统数据同步、非实时通知下发**。
【强制】：对时效性敏感的核心业务，严禁使用 ZMQ，需优先选择 RPC 调用（如：Dubbo、gRPC）、HTTP 同步请求等点对点实时通信方式。

说明：延迟判断无固定标准，核心判断依据由业务方自主决定是否能接受延迟，而非强求 ZMQ 保证时效。

适用 ZMQ 的场景示例（可接受延迟，需保证最终一致性）：

- 归档完成后触发赠送业务
- 转账结果通知、充值成功提醒
- 非实时数据统计、日志异步上报

此类业务用户无感知或可接受延迟，且能保证最终一致性，即可放心使用 ZMQ。

严禁使用 ZMQ 的场景示例（需秒级响应，不可接受延迟）：

- 实时扣款流程
- 库存锁定、商品秒杀核心环节
- 其他需即时反馈结果的核心业务

核心原则：业务侧根据自身特性，如能接受“延迟响应”，则用 ZMQ；需“秒级实时响应”，则换 RPC 或 HTTP 同步调用。

## 消息发送规范

### 发送方式

【**强制**】：核心业务（如订单、支付等，**消息发送失败将直接影响业务流程并引发投诉**），必须采用**同步发送**方式，且发送后需**严格校验返回结果状态**；若发送结果有异常，即判定为消息发送失败，业务侧需实现消息重发补偿机制，以此应对网络抖动、ZMQ 服务端流量突发等场景下的发送失败问题，确保核心消息不丢失。

> ⚠️ 故障警示！本规范制定源自严重生产故障（单号：3792911）。在此项目故障案例中，因主机hang死触发broker主备切换，切换期间（30秒左右）消息发送失败，业务未做重发导致消息数据丢失，引发CPC卡单，直接影响开通订单的正常流转。

**<font color="red">反例：</font>**

```java
ProduceResult sendResult;
try {
    sendResult = producer.send(mqMsg);
// ❌异常捕获方式有误,应该捕获Exception
} catch (MQClientApiException var9) {
    // ❌ 捕获了消息发送异常，但是没有重处理的逻辑
    MQClientApiException e = var9;
    logger.error("Fail to send MQ message.", e);
    return null;
}
```

上述反例来自于真实业务代码，代码中未对消息发送异常做任何处理，导致消息丢失。

【**推荐**】：建议为发送的消息设置可追溯标识，便于后续问题排查：

1. **核心业务场景**：

   - **设置唯一业务 Key**：建议为每条消息设置包含业务属性的**唯一 Key**（如订单号、交易流水号），并在本地日志中记录。这是在控制台检索消息、排查问题的最快途径。
   - **记录 MsgID**：若场景限制无法设置 Key，则**必须**记录发送结果 `ProduceResult` 中的 `msgid`。
   - **警示**：若业务侧既未记录 Key 也未记录 `msgid`，一旦发生消息丢失或异常，ZMQ 平台将无法进行链路追踪，问题将无法定位。
2. **非核心业务场景**（如异步日志记录）：

   - 对消息发送失败容忍度较高，**无需强制校验**发送返回结果，建议按需做好异常捕获与兜底处理即可。

**正例：**

```java
     /**
     * 核心业务发送MQ
     * 规范核心：设置含业务类型的唯一KEY并留存，支撑问题追溯
     */
    public void sendCoreMsg(String orderId, String payResult) {
        // ========== 规范要求：核心业务设置含业务类型的唯一KEY ==========
        // 注：此处businessKey直接使用orderId，orderId本身属于「订单支付业务」的唯一标识
        String businessKey = orderId;
  
        try {
            MQMessage msg = new MQMessage(
                "ORDER_PAY_TOPIC",
                null,
                businessKey, // 核心：设置含业务类型的唯一KEY（orderId关联订单支付业务）
                payResult.getBytes()
            );
            ProduceResult result = producer.send(msg);

            // ========== 规范要求：留存含业务类型的唯一KEY信息 ==========
            // 留存KEY+消息内容，支撑控制台检索/问题定位
            logger.info("[核心业务] MQ发送成功 | 含业务类型的唯一KEY（订单ID）：{} | topic：ORDER_PAY_TOPIC", 
                businessKey, payResult);
            // 若orderId在业务库里面可以追溯，则可以不打印businessKey
            // 记录msgid兜底
            logger.info("[核心业务] MQ发送成功 | msgid：{}，businessKey {},topic {}）", 
                result.getMsgId(), orderId, "ORDER_PAY_TOPIC");
            // 可选：将KEY/msgid留存到数据库（长期追溯/审计场景）
            saveMsgTraceRecord(businessKey, result.getMsgId(), payResult, "SUCCESS");

        } catch (Exception e) {
            // 异常时仍留存KEY，便于定位哪个业务KEY的消息发送失败
            logger.error("[核心业务] MQ发送失败 | 含业务类型的唯一KEY（订单ID）：{},topic ORDER_PAY_TOPIC", businessKey, e);
            // 补全重发逻辑，比如写数据库，定时扫库重发等
            // 写入重发表，支撑定时扫库重发
            xxxDAO.insertResendRecord(resendRecord);
        }
    }
```

### 顺序消息

ZMQ 通过 shardingKey（分区键）实现局部顺序，即保证同一业务主键（如同一订单号）的消息被路由到同一个 MessageQueue 中，从而保证该业务主键下消息的严格先进先出（FIFO）。

【**强制**】：发送顺序消息时，必须配置有效的 `shardingKey`，且需保证其**散列均匀性**。

- **取值建议**：使用具备高离散度的业务唯一标识，如**订单 ID、用户 UID、支付流水号**等。
- **禁止行为**：严禁使用固定值、常量或低离散度字段（如性别、地区码）作为 `shardingKey`。
- **风险警示**：若 `shardingKey` 散列不均，将导致**数据倾斜**，引发个别队列消息严重堆积（热点队列），直接拖垮该队列的消费性能，且不仅影响该业务，还可能因单点瓶颈拖累整个 Topic 的吞吐量。

### 消息体大小限制

【**强制**】：**严禁**将大体积数据（完整业务明细、文件流、批量超大报文、冗余附件等）直接嵌入消息体（Body）。

- **规范要求**：单条消息体大小应控制在 **1KB** 左右，Java客户端最大不可超过 **4MB**,超过 **4MB** 则消息发送失败（C++客户端最大不可超过 **128KB** ，超过 **128KB** 则消息发送失败）。
- **处理方案**：若数据量较大，建议将数据存储至对象存储或数据库，仅在消息中传输数据索引（如 URL 或 ID）。

**超大消息体的危害：**

1. **性能严重衰减**：ZMQ 默认会对超过 **4KB** 的消息体进行压缩，导致客户端和服务端 CPU 负载飙升，显著降低吞吐量。
2. **破坏 PageCache**：ZMQ 的高性能依赖操作系统的 PageCache，默认会缓存最近的消息。大消息会迅速占满页缓存，导致热点消息被置换出内存，迫使 Broker 频繁进行物理磁盘 I/O，使读写性能呈数量级下降。
3. **IO 阻塞与流控**：CommitLog（消息存储文件）写入大消息时，Broker 刷盘耗时变长，极易触发“刷盘繁忙”告警。若请求积压超过 3500ms，将直接触发 Broker 端流控（Flow Control），拒绝写入，甚至阻塞整个 Broker 的处理线程，严重影响同一 Broker 上其他业务的稳定性。

## 消息消费规范

### 幂等

ZMQ 采用 **At-Least-Once**（至少投递一次）投递策略，在网络波动、客户端重平衡（Rebalance）或 Broker 重启等场景下，可能导致消息被重复投递。

【**强制**】：核心业务场景（如支付、订单扣款、资金类操作等不允许重复执行的场景），消费端**在业务层面实现幂等性校验**。

* **核心原则**：对于核心业务的同一条消息（业务唯一标识相同），无论消费多少次，最终的业务结果必须一致，且不能产生副作用（如重复扣款、重复插入数据）；非核心业务可根据场景灵活决策。

* **实现建议**（核心业务参考）：

  * **数据库唯一索引**：利用数据库 Unique Key 约束防止重复插入。
  * **状态机约束**：基于业务单据状态机（如 “待支付”->“已支付”），更新前校验当前状态。
  * **分布式锁 / 缓存记录**：使用 Redis 记录已处理的业务 ID。

【**说明**】：

* 是否需要做幂等校验、采用何种实现方式，由业务方根据自身业务风险、成本及场景特性自主决策；若业务方选择做幂等校验，建议幂等校验数据的有效期覆盖消息的生命周期（参考值不低于 6 小时，具体可结合消费者应用升级周期设定，需不短于升级周期）；
* 有效期设定原因：ZMQ 的默认重试窗口较长，若幂等记录过早过期，当消息在一段时间后触发重试时，可能会绕过幂等校验导致重复消费。

### 重试

【**推荐】**：ZMQ 客户端默认消费重试次数为 **3** 次，针对消费失败场景， **业务侧需额外实现补偿重试机制** ，结合业务特性设置合理重试次数与间隔，避免数据丢失。

### 广播消息

ZMQ 的 `ConsumeFromWhere` 配置项决定了消费者启动时从哪里开始消费消息，该配置对**广播消息**和**集群（普通）消息**的影响截然不同。

- **集群消息（普通模式）**：消费位点由服务端（Broker）持久化管理。即使客户端重启，也会接着上一次记录的位点继续消费，`ConsumeFromWhere` 仅在**首次启动**或**位点丢失**时生效。
- **广播消息（Broadcasting）**：服务端**不存储**广播消息的消费位点，消费进度完全由客户端本地维护（通常在内存或本地文件）。**一旦客户端重启，本地位点丢失，消费者会重新依据 `ConsumeFromWhere` 的配置决定消费起点。**

> ⚠️ 故障警示！本规范基于生产故障（单号：3042689）制定。该故障因 APIG 刷应用配置缓存采用广播消息，且配置为`ConsumeFromFirst`，导致升级时消息从头消费，引发 ZMQ 磁盘 IO 飙升、系统 Hang 死，最终造成生产事故。

【**强制**】：广播消息模式下，必须显式配置为 `ConsumeFromLast`（默认值）。

- **配置含义**：
  - `ConsumeFromLast`：启动后仅消费**最新产生**的消息（忽略历史消息）。
  - `ConsumeFromFirst`：启动后从队列头部开始，全量消费**所有历史消息**（一般的项目现场默认保留 3 天）。
- **风险警示**：若广播消息误配置为 `ConsumeFromFirst`，每次服务重启（发布、扩容），所有消费实例都会重新拉取并消费最近 3 天的全量历史消息。**后果**：这会导致 Broker 端磁盘 I/O 飙升（读取冷数据），引发严重的性能抖动甚至服务僵死；同时消费端也会因瞬间处理海量重复消息而面临崩溃风险。

【**强制**】：严禁在广播模式下随意配置 `ConsumeFromFirst`。若特殊场景确需全量消费历史广播消息，必须提前通过架构评审并通知 ZMQ 运维团队进行风险评估。

**<font color="red">反例一：</font>**

```java
properties.put(PropertyKey.Consumer_Message_Model,PropertyKey.Consumer_Broadcast_Model_Value);
properties.put(PropertyKey.ConsumeFrom_Where,PropertyKey.ConsumeFrom_First_Value);
```

**<font color="red">反例二：</font>**

```properties
ftf.mq.properties.ConsumerMessageModel=BROADCASTING
ftf.mq.properties.ConsumeFromWhere=CONSUMER_FROM_FIRST
```

### 顺序消息

RocketMQ 原生客户端为保证顺序消息的严格有序（FIFO），默认采用**阻塞式重试**机制：一旦当前消息消费失败，将持续重试直至成功或达到重试上限，期间该队列中后续所有消息均被阻塞。这种机制虽保证了顺序，但在异常场景下极易引发**队列阻塞（Queue Blocking）**，导致业务停滞。

原生客户端的无限重试逻辑在生产环境中存在明显风险，ZMQ 针对该痛点，在 **ZMQ Client 9.0.30** 及后续版本采用了不同的默认策略，业务侧需根据使用的客户端版本进行针对性配置：

**1. ZMQ Client 9.0.30 及以后版本（推荐）**

- **默认行为**：已优化默认重试逻辑。最大重试次数默认为 **3 次**。若重试 3 次仍失败，将**跳过**当前消息，继续消费后续消息，以优先保障业务可用性。

- **【强制】核心有序业务**：对于**无法容忍乱序**的强一致性业务（如账务处理），必须**手动配置无限重试**，以牺牲可用性为代价确保严格顺序。

  ```java
  // 设置为 -1 代表无限重试（恢复原生行为）
  properties.put(PropertyKey.Reconsume_Times, "-1");
  ```

**2. ZMQ Client 9.0.30 之前版本**

- **默认行为**：维持原生无限重试逻辑。若消费返回 `RECONSUME_LATER` 或抛出异常，将无限重试并阻塞队列。
- **【强制】防阻塞控制**：业务代码必须**严格控制重试次数**。建议在本地记录重试计数，当达到阈值（如 3 次）后，捕获异常并主动返回**消费成功**标识（同时告警记录），强制跳过坏消息，防止单一异常阻塞整个队列。

**<font color="red">反例：</font>**

```java
// ❌ 核心错误：消息处理器返回固定失败/挂起状态，无异常兜底+无重试控制
final MQOrderMessageHandler orderMessageHandler = new MQOrderMessageHandler() {
    @Override
    public OrderProcessStatus process(MQMessage message, OrderMessageHandlerContext context) {
        try {
            // 模拟：消费业务逻辑执行失败（如数据库异常、接口调用超时）
            System.out.println("**************");
            System.out.println(message.getTopic() + " " + new String(message.getBody(), Charset.forName("UTF-8")));
            // 模拟业务异常
            int a = 1 / 0;
        } catch (Exception e) {
            // ❌ 错误1：仅打印异常，无任何重试次数控制、无兜底处理
            e.printStackTrace();
        }
        // ❌ 错误2：固定返回挂起状态，触发无限重试
        return OrderProcessStatus.Suspend;
    }
```

**正例：**

```java
// 设置为 10 代表业务消费失败后最多重试10次，重试10次后则跳过此消息
properties.put(PropertyKey.Reconsume_Times, "10");
```

**【说明】**：ZMQ 顺序消息仅能保障稳定运行状态下的消息局部有序，在 Broker 主备切换、版本升级、集群扩容、Topic 队列数调整、异常重启、网络波动导致 Broker 闪断等场景下，可能出现短暂的消息乱序。该现象并非功能缺陷，而是 ZMQ 架构设计的固有特性，且乱序发生概率极低。

* **适用性评估**：业务需自行判断是否能接受此类极低概率的乱序；若业务场景对消息顺序有极度严苛的要求（即任何情况下的乱序都会导致严重的数据错误且无法通过业务逻辑兼容），则 ZMQ 顺序消息并非最佳解决方案，需要考虑使用分布式锁等强一致性方案替代。
* **监控与排查要求**：ZMQ客户端需针对顺序消息增加专项监控与日志埋点，当 Sharding Key 路由至不同队列时，必须输出清晰的日志信息（含 Sharding Key、目标队列 ID、路由异常标识等），便于业务侧快速定位和排查乱序问题以及做数据恢复。
* **操作规范（强制）**：任何涉及 Broker 升级、Topic 队列数调整、集群扩容 / 缩容等可能影响消息路由的操作执行前，必须停止顺序消息的生产应用，操作完成并确认 Broker 状态稳定后，再恢复业务应用，以此避免操作过程中出现不可控的消息乱序问题。

【**推荐**】：顺序消息 Topic 需合理配置**读写队列数（Write/Read Queue Num）**，以最大化消费并发度。

**核心原理**：
顺序消息的消费模型是 **Lock 粒度为 MessageQueue**，即**一个 MessageQueue 同一时刻只能被一个消费线程处理**。

【**重要结论**】：**在不增加服务端 Topic 队列数的情况下，单纯增加客户端消费线程数或扩容消费节点，可能无法提升消费速度。**

- **现象**：当 `总消费线程数 > 总队列数` 时，多余的消费线程将因抢不到队列锁而处于**永久闲置（Starvation）** 状态。
- **瓶颈**：顺序消息的并发度上限严格受限于 **Topic 的总队列数**。

**优化方案**：
若遇到顺序消息消费堆积，必须采用 **“双向扩容”** 策略：

1. **服务端**：先增加 Topic 的读写队列数。
2. **客户端**：再根据新的队列数，按需增加消费线程数或扩容实例，确保 `总消费线程数 ≈ 总队列数`。

**配置公式参考**：
为避免资源浪费或能力受限，建议按以下公式规划队列数：

$$
\text{Topic队列数} \ge \lceil \frac{\text{单实例消费线程数} \times \text{消费实例数}}{\text{Broker 主节点数}} \rceil
$$

- **场景示例**：假设有 2 个 Broker 主节点，消费端集群有 4 个实例，每个实例配置 20 个消费线程。
  - **总消费线程数** = 4 实例 × 20 线程 = 80。
  - **建议总队列数** = 80。
  - **单 Broker 队列配置** = 80 / 2 = 40。
  - **结论**：每个 Broker 上该 Topic 的读写队列数应配置为 **40**（而非默认的 8），才能保证 80 个消费线程均有活可干。

**避坑指南**：
切勿直接套用普通消息的配置经验（普通消息允许单队列多线程并发消费），顺序消息必须严格满足 **“队列数 ≥ 线程数”** 才能发挥最大性能。

### 订阅关系一致性要求

【**强制**】：同一消费组下存在多个消费实例时， **所有实例必须订阅完全相同的 Topic 列表及 Tag过滤规则** ，禁止出现订阅关系不一致的情况，否则将导致业务消费异常。

原理：Broker 会为消费组下的**每个 Topic**维护**独立的消费进度 Offset**，而非为每个消费实例维护 Offset—— 消费组的 Offset 是全局的，所有实例共享并基于此拉取消息。Broker 在进行**负载均衡（Rebalance）** 时，仅根据**消费组 + Topic**维度划分消息队列（Message Queue），将Topic 的队列均匀分配给组内的消费实例，**Broker 端不感知单个消费实例的订阅规则**，也不会为实例做个性化的消息过滤和分发。

### 消费时长控制

ZMQ 默认设置了 **15 分钟** 的消费超时阈值。客户端会启动后台线程定时扫描正在处理的消息，若发现某条消息**超过 15 分钟**仍未返回消费结果（ACK），将判定为**消费超时**。

【**强制**】：**合理配置超时时间**。

- **默认机制**：一旦判定超时，该消息会被自动重新放入**重试队列**，服务端会将这条未确认的消息再次分发给消费组内的实例（可能是原实例、也可能是其他实例）进行二次消费。

- **配置建议**：

  - **常规业务**：保持默认 15 分钟即可，避免因代码死锁导致消息永久堆积。
  - **长耗时业务**：若业务逻辑确实需要运行超过 15 分钟（如大数据处理、文件生成），**必须显式调大** `ConsumerTimeout` 参数，防止业务还在正常运行时被强制重试。
  ```java
  // 示例：将超时时间调整为 120 分钟
  properties.put(PropertyKey.Consumer_Timeout, "120");
  ```

- **风险警示**：若未合理配置，长任务将陷入 **“执行中 -> 超时被重试 -> 再次执行 -> 再次超时被重试”** 的死循环，不仅浪费计算资源，还可能导致严重的业务数据重复。

> 注：消费时长的配置仅适用于 Java 客户端，C++客户端不具备此功能。

### 消费模式统一性要求

ZMQ 支持 **集群消费（Clustering）** 和 **广播消费（Broadcasting）** 两种消费模式，但这两种模式的底层位点管理机制完全不同。

【**强制**】：**“单一组单一模式”原则**。同一消费组（Consumer Group）下的所有消费实例，必须配置**完全一致的消息消费模式**。

- **禁止行为**：
  - 实例 A 配置为集群模式，实例 B 配置为广播模式。
- **后果警示**：
  混合配置会导致 Broker 端位点管理逻辑错乱，引发**不可预测**的消费异常：
  - **消息丢失**：集群模式的 Offset 覆盖了广播模式的本地进度。
  - **重复消费**：广播模式的消费干扰了集群模式的 Rebalance。
  - **分发异常**：部分实例无法拉取到消息，或收到不该处理的消息。

## 配置和命名规范

### Topic名称设计

【**推荐**】：**“三段式”命名法**。
采用 `application_businessdomain_event` 的格式，使用全大写字母，单词间用下划线 `_` 分隔。此命名方式兼顾了可读性、可管理性和防止命名冲突。

- **Application（应用名）**：Topic 所属的系统或产品名称（如 CRM, BILLING, O2C）。
- **BusinessDomain（业务域）**：消息所属的具体业务模块（如 ORDER, ACCOUNT, EMAIL）。
- **Event/Action（动作/事件）**：消息代表的具体业务事件（如 CREATED, PAY_SUCCESS, SENT）。

**正例：**（层级清晰，语义明确）：

```properties
BILLING_INVOICE_GENERATED      # 计费系统_发票模块_生成事件
O2C_ORDER_PAY_COMPLETED        # O2C系统_订单模块_支付完成
CRM_CUSTOMER_PROFILE_UPDATED   # CRM系统_客户档案_更新事件
UCC_SMS_SEND_REQUEST           # 统一通信_短信模块_发送请求
```

**<font color="red">反例：</font>**（无产品前缀，语义模糊）：

```properties
TEST                           # 无任何业务含义
EMAIL_SEND                     # 缺少归属系统，易与其他系统冲突
USER                           # 范围太广，不知是用户创建还是删除
ORDER_PAY                      # 缺少系统前缀
```

**【强制】：需要包含英文字母，并且不要包含特殊字符**

- 字符限制：仅字母a~z或A~Z、数字0~9和下划线（_）。
- 长度限制：1~64个字符。
- 保留字符：ZMQ系统内部使用的TOPIC，业务避免使用：
  - TBW102
  - BenchmarkTest
  - SELF_TEST_TOPIC
  - OFFSET_MOVED_EVENT
  - SCHEDULE_TOPIC_XXXX
  - RMQ_SYS_TRANS_HALF_TOPIC
  - RMQ_SYS_TRACE_TOPIC
  - RMQ_SYS_TRANS_OP_HALF_TOPIC

**特殊前缀**：ZMQ系统内部使用的Topic前缀，业务避免使用：

- rmq_sys_
- %RETRY%_
- %DLQ%_
- rocketmq-broker-

Topic命名应该尽量使用简短、常用的字符，避免使用特殊字符。特殊字符会导致系统解析出现异常，字符过长可能会导致消息收发被拒绝。

### 订阅组名称设计

【**推荐**】：**标准化命名格式**。
采用 `CID_application_businessidentifier` 的格式，统一以 `CID_` 开头，全大写字母，单词间用下划线 `_` 分隔。

- **CID_**：ZMQ 消费组的标准前缀（Consumer ID）。
- **Application（应用名）**：消费端所属的系统或产品名称。
- **BusinessIdentifier（业务标识）**：该消费组的具体用途或所消费的业务模块。

**正例：**（标准前缀，归属明确）：

```properties
CID_CRM_SMS_SENDER           # CRM系统_短信发送消费组
CID_BILLING_INVOICE_PROCESS  # 计费系统_发票处理消费组
CID_O2C_ORDER_STATUS_SYNC    # O2C系统_订单状态同步消费组
```

**<font color="red">反例：</font>**（无前缀，命名随意）：

```properties
GoodsSells                   # 缺少 CID_ 前缀，且无应用标识
stcBranch20                  # 命名风格混乱（驼峰/小写混用）
CID_RC                       # 业务描述过于简略，无法识别用途
```

**【强制】：需要包含英文字母，并且不要包含特殊字符**

字符限制：支持字母a~z或A~Z、数字0~9以及下划线（_）、短划线（-）。

长度限制：1~64个字符。

ZMQ系统内部系统保留字符：ConsumerGroup不允许使用以下保留字符或含有特殊前缀的字符命名。

**保留字符**：

- DEFAULT_CONSUMER
- DEFAULT_PRODUCER
- TOOLS_CONSUMER
- FILTERSRV_CONSUMER
- __MONITOR_CONSUMER
- CLIENT_INNER_PRODUCER
- SELF_TEST_P_GROUP
- SELF_TEST_C_GROUP
- CID_ONS-HTTP-PROXY
- CID_ONSAPI_PERMISSION
- CID_ONSAPI_OWNER
- CID_ONSAPI_PULL
- CID_RMQ_SYS_TRANS

**特殊前缀**：

- CID_RMQ_SYS_
- CID_HOUSEKEEPING

### 生产组名称设计

【**推荐**】：**标准化命名格式**。
采用 `PID_application_businessidentifier` 的格式，统一以 `PID_` 开头，全大写字母，单词间用下划线 `_` 分隔。

- **PID_**：ZMQ 生产组的标准前缀（Producer ID）。
- **Application（应用名）**：生产端所属的系统或产品名称。
- **BusinessIdentifier（业务标识）**：该生产组的具体用途或所生产的业务模块。

**正例：**（标准前缀，归属明确）：

```properties
PID_CRM_ORDER_EVENT          # CRM系统_订单事件生产者
PID_BILLING_CDR_GENERATOR    # 计费系统_话单生成生产者
PID_O2C_PAYMENT_NOTIFIER     # O2C系统_支付通知生产者
```

**<font color="red">反例：</font>**（格式错误，易混淆）：

```properties
GoodsSells                   # 缺少 PID_ 前缀
stcBranch20                  # 命名风格混乱
CID_RC                       # 错误使用了 CID 前缀（这是消费组前缀）
```

**【强制】：字符与长度限制**

- **字符限制**：仅允许使用字母（a~z, A~Z）、数字（0~9）和下划线（_）。禁止使用短横线（-）或其他特殊字符。
- **长度限制**：1~64 个字符。

## 客户端配置列表

| 参数                                         | 类型    | 说明                                                                                                                                                                   | 默认配置                   |
| -------------------------------------------- | ------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------- |
| ftf.mq.properties.ProducerId                 | String  | 生产组ID                                                                                                                                                               | 必填                       |
| ftf.mq.properties.ConsumerId                 | String  | 消费组ID                                                                                                                                                               | 必填                       |
| ftf.mq.properties.ConsumerMessageModel       | String  | 消费模式，取值为：CLUSTERING ，集群消费模式；BROADCASTING，广播消费模式，默认值为CLUSTERING                                                                            | CLUSTERING                 |
| ftf.mq.properties.ConsumeFromWhere           | String  | 设置一个消费组首次消费时起始位置，取值为：CONSUMER_FROM_FIRST，从队列头开始消费；CONSUMER_FROM_LAST，从队列尾开始消费，只消费最新到达的消息，默认值是CONSUME_FROM_LAST | CONSUMER_FROM_LAST         |
| ftf.mq.properties.ConsumeMessageBatchMaxSize | String  | 每次消费消息的数目，该配置项只对消息批量消费生效，默认值为32                                                                                                           | 32                         |
| ftf.mq.properties.pullInterval               | String  | 拉取消息时的时间间隔，单位是ms，即前次拉取完成后立即发起下次拉取操作                                                                                                   | 0                          |
| ftf.mq.properties.ProducerSendTimeout        | String  | 发送消息的超时时间，单位为ms                                                                                                                                           | 5000                       |
| ftf.mq.properties.ProducerMaxMessageSize     | String  | 消息的最大长度，单位是MB                                                                                                                                               | 4                          |
| ftf.mq.properties.ConsumerWorkerSize         | String  | 消费线程池的大小                                                                                                                                                       | 20                         |
| ftf.mq.properties.ConsumerTimeout            | String  | 消费消息的超时时间，单位为分钟                                                                                                                                         | 15                         |
| ftf.mq.zmq.enableMsgTrace                    | boolean | 是否开启消息轨迹功能，ZMQ特定配置项默认值是true，即默认是开启了消息轨迹功能                                                                                            | true                       |
| ftf.mq.zmq.ZMQ_NAMESPACE                     | String  | namespace名称，ZMQ特定配置项，使用了多租户功能实现数据隔离的ZMQ集群需要配置该项                                                                                        | 默认为空，表示非多租户集群 |
| ftf.mq.zmq.ReconsumeTimes                    | String  | 消费失败后默认重试的次数，最大为16                                                                                                                                     | 3                          |
| ftf.mq.zmq.compressMsgBodyOverHowmuch        | String  | ZMQ 客户端默认以消息体大小 4KB 为消息压缩阈值：消息体≥4KB 触发自动压缩，若<4KB 不压缩。                                                                               | 4 * 1024                   |

## 本文件评审、修正记录

| 文件名称 | ZMQ开发规范 |                                                                                                           |                 |        |
| -------- | ----------- | --------------------------------------------------------------------------------------------------------- | --------------- | ------ |
| 序号     | 流程        | 拟制人 / 审核人                                                                                           | 拟制 / 审核时间 | 版本号 |
| 1        | 编写        | 王礼吉 / 曾力耕、叶建敏、张南雨、周晓宇、陈逢俊、王晓成、齐微、周云、许显财、芦祥、卞晓宇、司俊恒         | 2026/01/06      | V0.1   |
| 2        | 修订        | 王礼吉 / 何永进                                                                                           | 2026/02/26      | V0.2   |
| 3        | 修订        | 王礼吉 / 何永进、曾力耕、叶建敏、张南雨、周晓宇、陈逢俊、王晓成、齐微、周云、许显财、芦祥、卞晓宇、司俊恒 | 2026/03/05      | V0.3   |
| 4        | 正式发布    | 国际后端框架SCCB | 2026/03/31      | V1.0   |
