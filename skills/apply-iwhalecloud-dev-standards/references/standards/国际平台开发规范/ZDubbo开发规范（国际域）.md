![image](uploads/217530/aecee68c-2703-483e-926f-a1434ed40ed7/image.png)

## 前言

### 规范目的

为规范业务侧对 ZDubbo 的使用方式，解决版本升级中的兼容性、性能故障及配置冲突等问题，降低运维成本，提升产品运行稳定性，特制定本规范。

### 适用范围

本规范适用于公司内部国际域所有基于 ZDubbo 进行服务开发的业务团队，覆盖服务提供者与消费者全链路开发场景。

### 版本基础

本规范基于 **Apache Dubbo 3.x** 内核及 **ZDubbo 9.0.15+** 版本制定，所有业务侧需确保使用此版本及以上进行开发。

## 版本管理规范

### 版本兼容性要求

ZDubbo与Apache Dubbo版本对应关系如下：

| Zdubbo版本              | Apache Dubbo 版本 |
| ----------------------- | ----------------- |
| 9.0.2 ~ 9.0.4           | 2.7.4.x           |
| 9.0.5 ~ 9.0.13.2        | 2.7.8             |
| 9.0.13.3 ~ 9.0.13.3-SEC | 2.7.15            |
| 9.0.13.4-SEC ~ 9.0.13.6 | 2.7.23            |
| 9.0.14 ~ 9.0.16         | 3.2.5             |

ZDubbo不保证跨大版本调用的兼容性，例如：

- 不保证 9.0.2 ~ 9.0.13.6 版本区间与 9.0.14 ~ 9.0.16版本区间的兼容性
- 不保证 5.x 版本与 9.x 版本的兼容性（5.x 已经EOL）

#### **禁止使用 EOL 版本**

严禁使用 `ZDubbo 9.0.13 `及之前版本（内核为 `Dubbo 2.7.x` 及以下），此类版本已于 `2023`年 `3` 月终止支持（`EOL`），组件依赖安全性及功能可靠性无法保障。

#### **升级至最新版本**

当前最新稳定版本为 `ZDubbo 9.0.15`（基于 `Apache Dubbo 3.2` 开发），所有业务系统需跟随`Core`框架完成升级。

> 附：Apache Dubbo Roadmap [发布地址](https://cn.dubbo.apache.org/en/blog/2022/10/22/focusing-on-stability-dubbo-java-release-plan-announced/#version-specific-maintenance-plan)，含EOL申明。

### 版本升级指引

- 升级前需完成全量单元测试及集成测试，验证核心业务流程兼容性；
- 升级过程中如遇兼容性问题，可提交工单至 ZDubbo 技术支持团队。

## 对象传输规范

### 传输大小限制

- **禁止大对象传输**：服务消费端请求载荷、服务提供端响应载荷**建议不超过 100KB**（指序列化后的数据包大小）。
- 大对象定义：序列化后数据包大小超过 `100KB` 的对象，均视为大对象。

### 大对象传输风险

Dubbo 协议基于单一长连接设计，适用于高并发、小数据量场景，大对象传输可能引发以下问题：

- 接口调用失败：默认载荷阈值为 `8M`，超出时触发 `ExceedPayloadLimitException` 异常；
- 性能下降：高并发场景下，大包传输会占用大量网络带宽，导致接口响应延迟增加；
- 资源耗尽：可能引发 `OOM`（内存溢出）、`CPU `使用率飙升等故障。

> ⚠️ 异常示例：
>
> org.apache.dubbo.remoting.transport.ExceedPayloadLimitException:
> Data length too large: 10710120,
> max payload: 8,388,608,

### 大对象处理方案

若因特殊场景需传输较大数据，优先采用以下方案（按推荐度排序）：

1. **精简消息体**：删除请求/响应中的无用属性，仅保留核心业务字段；
2. **启用压缩**：通过配置 `dubbo.protocol.compression=gzip` 启用载荷压缩；
3. **调整阈值（不推荐）**：通过 `dubbo.protocol.payload` 配置修改阈值（单位：byte），但需知晓此操作会显著降低系统整体性能。

> ⚠️ 注意：压缩会增加 CPU 消耗！出于性能考虑，dubbo默认不起用载荷压缩功能，开启前需评估性能影响。只能应急使用！

## 序列化规范

### 序列化机制要求

`ZDubbo 9.0.15+` 采用 `fastjson2 `作为默认序列化实现，因安全原因 `fastjson2 `默认关闭 `autotype` 自动类型识别功能，需严格遵守以下规范：

- **禁止依赖 autotype 机制**：不得通过开启 autotype 绕过类型校验，避免因服务端与消费端配置不一致导致序列化失败；
- **类型完全一致**：服务提供端与消费端的接口出入参类型（包括类结构、继承关系）必须完全一致。

### 正反例说明

| 场景     | 正例                                                                            | 反例                                                                                 |
| ---------- | --------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------- |
| 类型定义 | 服务端返回`User` 类型，消费端同样定义 `User` 类（属性、getter/setter 完全一致） | 服务端返回`User` 类，消费端用其父类 `Person` 接收；或消费端 `User` 类新增继承关系    |
| 接口声明 | 服务端：`User getUser(Long id)`<br />消费端：`User getUser(Long id)`            | 服务端：`User getUser(Long id)`<br />消费端：`Person getUser(Long id)`（类型不匹配） |

### autotype 风险说明

autotype 机制通过在 JSON 中添加 `@type` 字段存储类名实现动态反序列化，但存在严重安全漏洞（如黑名单绕过攻击）。fastjson2 已默认关闭此功能，强行开启可能导致系统被注入恶意代码。

## 扩展开发规范

### 扩展点使用限制

- **不建议定制扩展点**：Dubbo 官方不保证扩展点接口的版本兼容性；
- 若必须扩展，需在代码中明确标注依赖的 Dubbo 版本，并在升级前完成扩展点适配测试。

> 例如：Dubbo 2.7 中 `Cluster` 接口 `join` 方法在 3.x 版本新增 boolean 类型参数，直接导致升级后编译/运行异常

### 禁止底层 API 调用

- **禁止直接调用 Dubbo 底层 API**：包括但不限于 `com.alibaba.dubbo`、`org.apache.dubbo` 包下的所有公开和非公开接口；

> ⚠️ 风险说明：底层 API 无兼容性承诺，版本升级后可能发生签名变更、逻辑重构，直接导致业务系统崩溃!

## 配置规范

### 版本配置兼容性

`ZDubbo 9.0.15+`（基于 `Dubbo 3.x`）与旧版本（`2.x`）配置格式存在显著差异，需严格遵守以下要求：

- **禁止混合使用 2.x 与 3.x 配置**：升级后必须统一使用 3.x 配置格式，禁止同时存在两个不同版本的配置。

以多协议/多注册中心场景下的配置为例，不同版本格式规范对比如下：

**2.x版本dubbo配置多协议/多注册中心配置格式规范**

```properties
# 协议1配置, 注意 这里的配置是 protocol, 单数
dubbo.protocol.dubbo.name=dubbo 
dubbo.protocol.dubbo.port=20880 

#协议2 配置, 注意 这里的配置是 protocol, 单数
dubbo.protocol.rest.name=rest 
dubbo.protocol.rest.port=8080 

# 多注册中心配置, 注意 这里的配置是 registry, 单数
dubbo.registry.zk1.address=zookeeper://192.168.1.100:2181 
dubbo.registry.zk2.address=zookeeper://192.168.1.101:2181
```

**3.x版本dubbo配置多协议/多注册中心配置格式规范**

```properties
# 协议1配置, 注意 这里的配置是 protocols, 复数
dubbo.protocols.dubbo.name=dubbo 
dubbo.protocols.dubbo.port=20880 

#协议2 配置, 注意 这里的配置是 protocol, 复数
dubbo.protocols.rest.name=rest 
dubbo.protocols.rest.port=8080  

# 多注册中心配置, 注意 这里的配置是 registry, 复数
dubbo.registries.zk1.address=zookeeper://192.168.1.100:2181 
dubbo.registries.zk2.address=zookeeper://192.168.1.101:2181
```

### 实例配置统一性

- **禁止单实例与多实例配置混用**：同一应用中必须统一使用单实例配置或多实例配置，不得同时存在两种格式；

> 单实例：单协议发布和单注册中心的服务部署模式，符合绝大多数业务场景。
>
> 多实例：多协议发布或多注册中心的服务部署模式，极少数业务场景。

正例：（仅包含单实例配置）

```properties
# 单实例/单注册中心配置
dubbo.application.name=demo-provider
dubbo.application.qos-enable=false
dubbo.registry.address=zookeeper://127.0.0.1:2181
dubbo.protocol.name=dubbo
dubbo.protocol.port=-1
```

反例：（同时包含单实例配置和多实例配置）

```properties
# 单实例/单注册中心配置
dubbo.application.name=demo-provider
dubbo.application.qos-enable=false
dubbo.registry.address=zookeeper://127.0.0.1:2181
dubbo.protocol.name=dubbo
dubbo.protocol.port=-1

# 多实例,多注册中心配置, 与单实例配置同时出现在应用配置中
# 协议1配置
dubbo.protocols.dubbo.name=dubbo 
dubbo.protocols.dubbo.port=20880 

#协议2 配置
dubbo.protocols.rest.name=rest 
dubbo.protocols.rest.port=8080  

# 多注册中心配置
dubbo.registries.zk1.address=zookeeper://192.168.1.100:2181 
dubbo.registries.zk2.address=zookeeper://192.168.1.101:2181
```

### API 包内容规范

下游依赖的 API/SDK 包中**禁止包含 Dubbo 配置文件**，避免应用运行时加载冲突：

- 允许包含：接口定义（interface）、序列化对象（DTO/VO）、常量类、枚举类；
- 禁止包含：`dubbo.properties`、`application.yml` 等配置文件。

## 安全开发规范

### 总体要求

所有基于 ZDubbo 发布的服务，需根据业务安全等级启用以下认证与加密机制，尤其针对生产环境及对安全性敏感的业务场景（如支付）：

- 基础安全：必须启用注册中心认证
- 数据安全：必须启用 Token 认证
- 传输安全：必须启用 SSL/TLS 加密通信

### 启用注册中心认证

注册中心认证机制用于保护注册中心的访问安全，防止未授权的服务或客户端非法接入注册中心、篡改服务信息或发起恶意调用。注册中心认证流程：

1. 注册中心预先配置合法的访问账号与密码
2. 服务提供者和消费者启动时需提供正确的认证信息
3. 注册中心验证客户端提交的账号密码合法性
4. 验证通过方可进行服务注册、发现或配置读取等操作，失败则拒绝访问

**服务提供端配置**：

```properties
# dubbo-provider.properties
# 要求1：配置注册中心地址
dubbo.registry.address=zookeeper://127.0.0.1:2181
# 要求2：配置注册中心访问用户名，与注册中心JAAS配置保持一致
dubbo.registry.username=xxxx
# 要求3：配置注册中心访问密码，与注册中心JAAS配置保持一致
dubbo.registry.password=xxxx
```

**服务消费端配置**：

```properties
# dubbo-consumer.properties
# 要求1：配置注册中心地址
dubbo.registry.address=zookeeper://127.0.0.1:2181
# 要求2：配置注册中心访问用户名，与注册中心JAAS配置保持一致
dubbo.registry.username=xxxx
# 要求3：配置注册中心访问密码，与注册中心JAAS配置保持一致
dubbo.registry.password=xxxx
```

> 需要注册中心开启 Java 认证和授权服务(JAAS)。当使用 Zookeeper 作为注册中心时，dubbo.registry.username 需要添加 `-sasl` 的后缀，例如：dubbo.registry.username=dubbo-sasl
> 支持通过环境变量的方式开启，变量名：DUBBO_REGISTRY_USERNAME、DUBBO_REGISTRY_PASSWORD

### 启用 Token 认证

Token 认证用于防止越过注册中心的非法服务调用，实现轻量级身份验证。Token验证流程：

1. 服务提供者启动时生成token并注册到注册中心
2. 消费者从注册中心获取服务信息（包含token）
3. 消费者调用时自动携带token进行验证
4. 提供者验证token有效性，验证失败则拒绝调用

**服务提供端配置**：

```properties
# dubbo-provider.properties
# 要求1：启用token验证（自动生成）
dubbo.provider.token=true
```

> 启用token验证主要是服务提供端配置，服务消费端不需要额外配置。
> 支持通过环境变量的方式开启，变量名：DUBBO_PROVIDER_TOKEN

### 启用 SSL/TLS 加密通信

SSL/TLS配置为ZDubbo服务间通信提供传输层的安全保障，通过加密机制防止数据在传输过程中被窃取或篡改。SSL/TLS 加密流程：

1. 服务提供者与消费者分别配置 SSL/TLS 相关证书
2. 建立连接时进行身份验证和加密算法协商
3. 通信过程中所有数据均通过协商的加密方式传输
4. 确保数据完整性和传输安全性

**服务提供端配置**：

```properties
# dubbo-provider.properties
# 要求1：配置服务提供端证书链、私钥、信任证书集合路径
dubbo.ssl.server-key-cert-chain-path=/app/certs/crt-zdubbo-server.crt
dubbo.ssl.server-private-key-path=/app/certs/crt-zdubbo-server.key
dubbo.ssl.server-trust-cert-collection-path=/app/certs/crt-iwhalecloud-ca.crt
```

**服务消费端配置**：

```properties
# dubbo-consumer.properties
# 要求1：配置服务消费端证书链、私钥、信任证书集合路径
dubbo.ssl.client-key-cert-chain-path=/app/certs/crt-zdubbo-client.crt
dubbo.ssl.client-private-key-path=/app/certs/crt-zdubbo-client.key
dubbo.ssl.client-trust-cert-collection-path=/app/certs/crt-iwhalecloud-ca.crt
```

> SSL/TLS 加密通信需要服务提供端和消费端同时配置对应的证书信息，以实现双向认证和加密传输。
> 支持通过环境变量的方式开启，变量名：（服务端）DUBBO_SSL_SERVER-KEY-CERT-CHAIN-PATH、DUBBO_SSL_SERVER-PRIVATE-KEY-PATH、DUBBO_SSL_SERVER-TRUST-CERT-COLLECTION-PATH （消费端）DUBBO_SSL_CLIENT-KEY-CERT-CHAIN-PATH、DUBBO_SSL_CLIENT-PRIVATE-KEY-PATH、DUBBO_SSL_CLIENT-TRUST-CERT-COLLECTION-PATH

### 安全配置规范

1. 生产环境部署前务必在测试环境充分验证
2. 密钥、证书等敏感信息严禁硬编码，应当使用配置中心或者密钥管理系统(KMS)来管理
3. 应定期审查和更新安全配置

## 功能特性使用限制

### 基本原则：白名单机制

Apache Dubbo 官方版本包含众多功能特性，受技术限制ZDubbo无法对官方发布的功能特性做局部裁剪，为确保 **框架稳定性**、**维护效率** 和 **业务产品可靠性**，需要通过规范指导产品线团队在使用 ZDubbo 框架时，仅使用经过框架团队官方认证和充分测试的核心功能集，避免引入额外的技术风险和维护负担。

ZDubbo 框架的使用必须遵循**白名单机制**，即：

- **只允许**使用本规范中明确列出的功能和配置项（核心功能集）。
- **禁止**使用本规范未提及的所有 Dubbo 原生的高级特性、实验性配置或扩展点。
- 如果产品线确实需要使用白名单以外的功能，必须**事先向框架团队提出申请**，获得批准后方可使用。

### ZDubbo 核心功能集（白名单）

以下功能集已在 ZDubbo 框架内经过全面测试，框架团队承诺对这些功能提供**最高优先级的支持**。

| 类别         | 允许使用的核心功能 (SLI/SLO 保证覆盖)                                                                                                                                     | 详细说明与推荐配置                                                                                                                                                                                                                                           |
| :----------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | :----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **基础服务** | 1.**服务定义:** 通过@DubboService或dubbo:service定义服务。<br/>2.**服务引用:** 通过@DubboReference或dubbo:reference引用服务。<br />3.**同步调用:** 最常用的服务调用方式。 | 1. 支持XML配置方式，但强烈推荐使用 Spring/Spring Boot 集成配置方式。<br />2. 从3.x开始官方已经将@Service、@Reference这两个注解标记为废弃，禁止使用<br />3. 同一个应用中只使用一种配置方式，XML/注解二选一，不要混用<br />4. 禁止使用异步调用方式，避免长事务 |
| **注册中心** | 1.**ZooKeeper**。 2.**Nacos**。                                                                                                                                           | 禁用其他注册中心（如 Consul, Etcd）。                                                                                                                                                                                                                        |
| **通信协议** | 1.**Dubbo 协议**。                                                                                                                                                        | 禁用其他协议（如 HTTP/thrift/Triple 等）。                                                                                                                                                                                                                   |
| **负载均衡** | 1.**加权轮询 (RoundRobin)**。 2.**随机 (Random)**。                                                                                                                       | 仅允许使用这两个最稳定的策略。                                                                                                                                                                                                                               |
| **集群容错** | 1.**Failover** (默认，失败自动切换)。 2. **Failfast** (快速失败)。                                                                                                        | 禁止使用其他容错策略(如：Failsafe,Failback,Forking,Broadcast等)，且**Failover** 重试次数限制在 $1 \sim 2$ 次。                                                                                                                                               |

### 严格限制和禁止使用的高级特性

以下 Dubbo 特性在 ZDubbo 生产环境中 **被禁止使用** 或者 **有条件限制使用**。使用这些特性可能导致服务稳定性问题、难以排查的 Bug，且 **框架团队将不提供任何兜底支持**。

#### **功能限制**

1. **泛化调用 (Generic Service)：** 不推荐生产环境使用。除了 APIG 这类接口机应用可以符合例外情况，其余业务应用均不允许使用泛化调用。

   > **原因：** 绕过接口定义，反射调用成本高，易出错，且难以进行静态检查和接口变更追踪。

2. **参数回调 (Callback)：** 严格禁止使用。

   > **原因：** 引入复杂的双向连接和状态管理，与主流微服务架构模式不符，维护成本极高。

3. **异步化配置：**

   * **禁止使用 `async=true` 或 `future` 模式**。

   > **原因：** 易造成线程池滥用和内存泄漏。统一使用 **消息队列（MQ）** 解决方案来处理异步业务。

#### **配置与扩展点限制**

1. **禁用自定义 Filter/Listener：** 除非得到框架团队授权，否则**禁止产品线自行扩展** Dubbo 的 Filter、Listener 或 Protocol。

   > **原因：** 自定义的扩展点可能破坏框架内部的调用链路和线程模型。且 Dubbo 官方不保证扩展点接口的版本兼容性；例如：Dubbo 2.7 中 `Cluster` 接口 `join` 方法在 3.x 版本新增 boolean 类型参数，直接导致升级后编译/运行异常。

2. **禁止使用 Mock/Force.Mock** 功能。

   > **原因：** 仅限测试环境，生产环境禁用，防止误配置导致服务降级不可用。

3. **集群容错限制：** 禁止使用 `Forking` 和 `Broadcast` 策略。

   > **原因：** `Forking` 消耗大量线程资源；`Broadcast` 不适合高并发场景。

### 兜底支持与责任划分

| 情景                 | 责任方         | 结果                                                                                                     |
| :------------------- | :------------- | :------------------------------------------------------------------------------------------------------- |
| **使用了白名单功能** | **框架团队**   | 承诺最高优先级兜底支持，协助定位和修复问题。                                                             |
| **使用了非白名单以外的其他功能** | **产品线团队** | 框架团队将**拒绝直接介入**定位和修复。产品线需自行解决问题，或按照框架团队要求**立即回滚到白名单配置**。 |

## 本文件评审、修正记录

| 文件名称 | ZDubbo开发规范               |                                                                  |               |        |
| -------- | ---------------------------- | ---------------------------------------------------------------- | ------------- | ------ |
| 序号     | 流程                         | 拟制人/审核人                                                    | 拟制/审核时间 | 版本号 |
| 1        | 编写                         | 沈维建/何永进，BSS产品线所有研发总监，数字渠道产品线所有研发总监 | 2025/08/05    | V0.1   |
| 2        | 发布                         | 国际后端框架SCCB                                                 | 2025/08/26    | V1.0   |
| 3        | 修订，增加章节7 安全开发规范 | 花伟/何永进                                                      | 2025/10/15    | V1.0.1 |
| 4        | 发布                         | 国际后端框架SCCB                                                 | 2025/10/27    | V1.1   |
| 5        | 修订，增加章节8 功能特性使用限制      | 花伟/何永进                                                 | 2026/01/26    | V1.1.1  |
| 6        | 发布                         | 国际后端框架SCCB                                                 | 2026/01/26    | V1.2   |

