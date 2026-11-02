![image](uploads/239676/34ad18f0-4eb2-4fd9-af27-d028f442b994/image.png)

## 前言

本规范旨在为其他产品或系统（以下简称“接入方”）与 DMS 产品进行集成时提供明确的指导和规范性要求。遵循本规范，将确保接入方能够稳定、高效、安全地使用 DMS 服务，提高系统稳定性和可维护性。

## 适用对象

* DMS 产品的用户：方案人员、设计人员、开发人员、交付人员。

## 目的

* **统一接入标准**：确保所有接入方以一致的方式与 DMS 进行交互。
* **保障系统稳定**：规范接口调用行为，减少因不当使用 DMS 服务导致的系统故障。
* **优化资源利用**：引导接入方合理使用 DMS 资源，避免资源竞争和性能瓶颈。

## 使用规范

### 强制：根据业务域使用系统预设的用户调用 DMS 接口，禁止使用 admin 用户

DMS 支持将文件和数据存储在云盘或 MongoDB 上。对于用户规模超过 200 万的项目，DBA 通常推荐优先采用 MongoDB。在 MongoDB 存储模式下，现阶段所有业务数据均落在默认租户下，随着生产数据体量持续增长，这种 `单租户存储` 的方式会带来以下问题：

1. 资源竞争与性能瓶颈
   1）MongoDB 的资源隔离粒度为 DB 与 collection。单租户模式下，所有业务共享同一套资源。
   2）热点业务（如集中出账）会直接挤占资源，影响其他业务的读写性能。
2. 运维管理复杂
   1）业务间缺乏物理边界，导致迁移、备份、删除等运维操作执行难度大。
   2）数据持续膨胀后，存储能力主要依赖纵向扩容，难以通过水平扩展提升，进而对系统稳定性带来不可预期风险。

针对上述问题，DMS 对 MongoDB 存储功能做了优化：可依据业务域进行分租户存储，将不同业务域的数据写入独立的 database。

> 说明：与传统关系型数据库不同，MongoDB 本身不提供表空间（table space）与租户（tenant）概念，因此这里提到的“多租户”，本质上是通过创建多个独立的数据库实例 (database) 来实现的。

**强制：DMS 系统预设以下三个用户，业务侧需根据业务划分使用正确的用户调用 DMS 接口。**

| **NO.** | **用户名** | **数据库实例** |
| ------- | ---------- | -------------- |
| 1       | billing    | data_billing   |
| 2       | crm        | data_crm       |
| 3       | recharge   | data_recharge  |

**强制：使用 billing、crm、recharge 之外的用户调用 DMS 需要提前向 DMS 团队备案**

业务如果需要新增用户，需要在业务版本发版之前同步新增用户信息到 DMS 产品，DMS 需针对新增用户执行初始化脚本。**使用未备案的用户调用 DMS 接口会产生异常！**

### 强制：调用文件生成和上传接口，必须传递 shardingKey 参数

使用 MongoDB 存储服务，如果业务调用接口没有设置 `shardingKey` 参数，文件默认会按月分表存储，不同业务数据会存储到同一分表中，而默认的按月分表存储模式无法满足不同业务数据要求不同的存储周期、不同的清理策略要求，导致在运维、性能、存储成本三个维度产生以下问题：

| **维度**        | **根本问题**         | **核心后果**                                   |
| --------------- | -------------------- | ---------------------------------------------- |
| **运维 & 合规** | 无法识别数据业务来源 | 运维无法统一清理超期数据，运维难度大。         |
| **系统性能**    | 数据总量持续膨胀     | 索引效率下降、I/O 压力大、导致业务卡顿。       |
| **存储成本**    | 短期数据被长期保存   | 存储容量浪费、备份成本高昂、无法进行数据分层。 |

因此，业务调用 DMS API 接口存储文件数据时必须传递 `shardingKey` 参数以确保过期数据能够定期清理，保证系统存储数据保持在可控的数据量级，从而保障系统平稳高效运行。

> 反例：NCELL 项目所有业务数据默认按月分表存储。由于运维无法识别并删除过期数据，文件存储已达到 30 TB 量级，并且还在持续增长。

**强制：业务产品调用以下 DMS 接口时必须传递 shardingKey 参数**

| **NO.** | **接口**          | **说明**             |
| ------- | ----------------- | -------------------- |
| 1       | POST /doc/make    | 根据模板生成文档接口 |
| 2       | POST /doc/v2/make | 根据模板生成文档接口 |
| 3       | POST /doc/upload  | 文档上传接口         |
| 4       | POST /file        | 文件上传接口         |

**强制：shardingKey 名称必须与业务属性及时间相关**

`shardingKey` 应由业务属性名称、时间相关名称两部分组成，业务属性名用于确认分表数据存储周期，时间相关名称用于确认数据分表创建时间，两者缺一不可。如果业务属性名与时间信息拼接时需连接符，必须使用下划线 `_`，**禁止使用其他连接符**。

> 正例：账务产品调用 DMS 生成文档接口 `/doc/make`，请求参数 `shardingKey` 设置为账期 `INV11394`（`INV` 为业务标识，`11394`为账期），生成的文件将存入`document_INV11394` “表”（`INV11394`也可以调整为`INV_11394`）。

### 强制：离线文件/文档上传接口只能用于数据割接

离线上传功能主要用于将已存在的历史账单、用户资料等老系统数据割接到 DMS 系统，DMS 通过扫描文件/文档目录将目录下的文件数据上传至 DMS 存储服务中。

> 文档和文件的区别：文档主要是生成类的文件，比如：合同、账单、发票等；其他类型统称为文件，比如：图片；在DMS中，文档和文件是采用不同的处理方式和存储形式。

**离线文件上传**

通过以下配置开启离线文件扫描上传功能：

```properties
# 开启扫描文件并上传的开关
ftf.dms.batch.fileScanner.enabled=true
# 文件扫描路径
ftf.dms.batch.file-dir=/mnt/dms/file
```

**离线文档上传**

通过以下配置开启离线文档扫描上传功能：

```properties
# 开启扫描文档并上传的开关
ftf.dms.batch.docScanner.enabled=true
# 文件扫描路径
ftf.dms.batch.doc-dir=/mnt/dms/hisfile
# 支持上传的文档格式
ftf.dms.batch.formats=pdf,xlsx
```

**强制：离线文档上传必须配置待上传的文件类型**

离线上传文档类型通过文件后缀名匹配，如 `pdf`、`xlsx`等。DMS 通过 `ftf.dms.batch.formats` 配置项配置支持的文档类型，多个类型使用英文逗号分隔。**未配置的文件类型，不会被 DMS 扫描到。**

**强制：离线文件/文档上传场景，待上传文件名必须符合固定的格式，包含鉴权用户名、分表shardingKey**

待上传文件/文档的文件名必须由鉴权用户名、分表shardingKey、真实文件名，三部分组成，其**固定格式**为：`${authUser}_${shardingKey}_${rawFileName}`

【示例】：

1. 待上传文件`/mnt/dms/his_file/default/crm/crm_subs_1000791.png`
   DMS扫描上传后该文件会写入`data_crm`库 `File_subs`集合
2. 待上传文档`/mnt/dms/his_doc/default/crm/crm_INV10791_bill.pdf`
   DMS扫描上传后该文件会写入`data_crm`库 `Document_INV10791`集合

**强制： 离线上传文件的元数据必须在JSON文件中定义**

除文件写入库、分表、文件名三个元数据外还需要其他元数据的情况下，此时必须在元数据JSON文件中定义，包括文件名[file_name]、鉴权用户名[auth_name], 分表后缀[shardingKey], 其余元数据根据实际情况配置； 元数据JSON文件中包含一组待上传文件的元数据信息，元数据JSON文件格式如下：

```json
[{
    "file_name": "crm_subs_1000791",
    "auth_name": "crm",
    "shardingKey": "subs",
    "labelList": [{
        "labelType": "test_label",
        "labelContent": "sep_tenant"
    }]
}, {
    "file_name": "crm_subs_1000792",
    "auth_name": "crm",
    "shardingKey": "subs",
    "labelList": [{
        "labelType": "test_label",
        "labelContent": "sep_tenant"
    }]
}]
```

**强制：离线上传，单个元数据文件内元数据条目数不能超过 1000 组**

元数据文件中一组元数据对应一个待上传文件，为了避免解析大 JSON 文件时出现 OOM 异常并保证处理效率，元数据条目必须控制在 1000 组以内; 如果超过 1000，需要拆分成多个 JSON。

**强制： 离线上传文档/文件的文件名必须唯一**

离线场景下，DMS系统会使用去除类型后缀的文件名作为数据库ID， 所以在去除文件类型后缀后， 文件、文档的名称必须唯一，避免主键冲突

**反例：**/mnt/dms/his_file/default/crm/ 目录下同时包含 `crm_subs_1000791.png`和`crm_subs_1000791.pdf`两个文件;

### 强制：离线生成文档需要在目录中声明分库信息，在xml元数据文件中声明分表信息

账单元数据XML中设置分表字段是为了确保生成的账单文件能够正确分表存储， 分库用户使用元数据文件父目录名。

**示例：**

DMS 离线文档生成配置及批量生成文档 XML 元数据配置如下：

- 应用配置

  ```properties
  ftf.dms.batch.xmlScanner.enabled=true
  // 元数据文件存放目录，父目录名为：billing，父目录名会被识别为分库用户信息。
  ftf.dms.batch.xml-dir=/mnt/dms/bill_data/default/billing
  ftf.dms.batch.fileNameElement=/BILL_REPORT/CUSTINFO/FILE_NAME
  ftf.dms.batch.shardKeyElement=/BILL_REPORT/CUSTINFO/SHARDING_KEY
  ```

- 元数据

  ```xml
  <BILL_REPORT>
      <CUST_INFO>
        <FILE_NAME>120004653189</FILE_NAME>
        <SHARDING_KEY>INV10291</SHARDING_KEY> <!-- 分表字段 -->
      </CUST_INFO>
  </BILL_REPORT>
  ```

通过以上配置，批量生成的文档将被写入 `data_billing` 库的 `Document_INV10291` 表。

### 强制：DMS 日志表存放海量日志数据，默认保留 1 个月，超期数据必须定期清理

云盘存储模式下，DMS 日志表存储在关系数据库中，对应用户为 `ftf`，表名为 `DMS_ACCESS_LOG`、`DMS_FAILURE`、`DMS_TASK_RECORD`，这三张表均为按月分区表，分区字段为 `PART_ID`。

MongoDB 存储模式下，DMS 日志表存储在 `tenant_default` 库下，集合为 `AccessLog-${shardingKey}` 或 `AccessLog_${shardingKey}`、`TaskRecord-${shardingKey}` 或 `TaskRecord_${shardingKey}`。其中 shardingKey 为分表键，默认为两位数月份，如： 01, 02, 03 等。

> **⚠️ 故障警示！本规范制定源自严重生产隐患**
>
> 缅甸 OML 项目现网 DMS 接口的操作历史表数据没有及时清理，存储数据超 60 亿，导致 MongoDB CPU 使用率持续增长的告警，存在较大隐患。

### 强制：项目部署 DMS 服务必须关注上传、下载、大账单服务限流配置

生产环境 DMS 产品承载了业务系统文件上传、下载、元数据查询、文档生成等功能。为了保证 DMS 提供可靠的支撑服务，DMS 产品对文件上传、下载、账单生成接口增加了限流控制。具体限流规则如下：

* 文件/文档上传并发线程数：默认 `40`
* 文件/文档下载并发线程数：默认 `40`
* 文件/文档上传并发上传总文件大小：默认 `500MB`
* 文档生成接口并发传递数据源 XML：默认 `50MB`

> **默认配置说明：**
>
> * **上传总大小控制**：DMS Web 服务基于 Tomcat，其上传组件默认会将文件缓冲至系统临时目录（如 `/tmp`）。在 ZCM 等容器化部署中，若 `/tmp` 未挂载独立持久化磁盘，文件将直接消耗容器内部存储。为避免容器存储打满引发雪崩，**并发上传总大小上限（`max-bytes`）建议严格控制在 `300MB ~ 500MB` 之间**。
> * **并发数控制与线程池划分**：DMS 默认 Tomcat 最大工作线程数为 `200`。在评估并发配置时，需结合实际业务场景（如集中出账）进行合理的线程池划分。典型高并发场景下的资源分配参考模型如下：
>   * **文档生成（出账核心）**：预留 80 个线程（包含冗余备份），保障核心业务的高可用性。
>   * **业务查询与 UI 交互**：分配 40 个线程，确保管理端与查询接口不被阻塞。
>   * **文件上传与下载**：各分配 40 个线程，限制非核心 IO 密集型操作对计算资源的挤占。

与以上流控相关的配置如下：

```properties
# 上传操作最大并发线程数
ftf.dms.upload.concurrent.threads=40

# 下载操作最大并发线程数
ftf.dms.download.concurrent.threads=40

# 单请求上传文件大小
spring.servlet.multipart.max-request-size=50MB

# 单个上传文件大小限制
spring.servlet.multipart.max-file-size=50MB

# 同一时刻允许并发上传的文件总大小 (byte)，默认 500MB
ftf.dms.upload.total.max-bytes=524288000

# 文档生成接口请求体大小并发总量限制 (MB)
ftf.dms.web.flowlimit.warning-threshold=50
```

> **定制化与容量压测要求**：
> DMS 标准出厂部署规格为 `8C/16G`，上述限流参数即基于该规格设定。若业务评估默认配置无法满足实际高并发诉求（如特大容量割接、极端出账高峰等），项目组必须向 DMS 产品团队提交定制化配置申请，并在调整配置后，于测试环境进行严格的容量与性能压测，以验证新配置下服务及底层存储的稳定性。

### 强制：调用 DMS 上传接口必须显式传递有效的 `Content-Length` 请求头

Tomcat 在处理文件上传时，默认会将接收到的文件流先缓冲至操作系统的临时目录。为了避免高并发上传瞬间打满容器的内部存储（DMS 设定了全局并发上传总容量上限 `500MB`），系统必须在接收文件内容前，提前获知该请求所需占用的容量。业务调用方在发起文件上传请求时，**必须在 HTTP Header 中包含准确的 `Content-Length` 值**。若缺失该请求头，DMS 将无法进行有效的前置容量统计。在严格校验模式下，此类请求将被 DMS 直接拒绝（返回 HTTP 411 Length Required）。

> **兼容性过渡说明**：
> 为平滑兼容存量业务，当前版本的 DMS 默认关闭了 `Content-Length` 的严格拦截。当检测到请求头缺失时，系统仅会打印 Warn 级别告警日志并放行。**但所有新接入项目必须严格遵守此规范，未来版本将视情况默认开启强制拦截。**

```properties
# Content-Length 严格校验，默认关闭
ftf.dms.upload.content-length.strict-check=false
```

### 强制：调用 DMS 上传、下载、生成文档接口必须处理流控异常，实施退避重试

上传、下载、生成文档接口发生流控时，DMS 服务端会向客户端返回 `HTTP 4xx` 状态码拒绝请求，客户端必须合理处置 DMS 服务端返回的 `4xx` 响应码的请求。

限流触发时 DMS 返回的响应码如下：

| HTTP 状态码 | 含义 | 场景 |
| :--- | :--- | :--- |
| **429** | 并发数超限或上传总容量超限 (Too Many Requests) | 1. 并发请求数超出阈值限制。<br/>2. 并发上传文件总大小超出阈值限制。 |
| **411** | 文件上传请求缺少 Content-Length 头 (Length Required) | 业务产品请求 DMS 且缺少该 Header 时。 |

### 强制：客户端收到 DMS 返回 429 响应码后必须等待一定时间后再重试，禁止收到 429 后立即无间隔重试

建议采用阶梯型重试间隔（如第一次间隔 2s，第二次间隔 4s，依次递增），且重试需要设置最大重试次数。参考代码实现如下：

```java
int maxRetries = 3;
long waitMs = 2000; // 初始等待 2 秒

for (int i = 0; i <= maxRetries; i++) {
    ResponseEntity<String> response = restTemplate.postForEntity(url, request, String.class);
    if (response.getStatusCodeValue() != 429) {
        return response; // 非 429，正常返回
    }
    if (i < maxRetries) {
        Thread.sleep(waitMs);
        waitMs = Math.min(waitMs * 2, 30000); // 指数退避，最大 30 秒
    }
}
throw new RuntimeException("DMS 服务繁忙，重试 " + maxRetries + " 次后仍失败");
```

## 附录：DMS 对外接口清单

### Restful 接口

#### 接口鉴权说明

DMS API 接口使用 Basic Auth 鉴权，调用 DMS 接口时需要添加 `Authorization: Basic base64_encoded_credentials` 请求头，其中 `base64_encoded_credentials` 字符串的计算逻辑如下（Java 实现）：

```java
import java.util.Base64;

String username = "username";
String password = "password";
String auth = username + ":" + password;
byte[] encodedAuth = Base64.getEncoder().encode(auth.getBytes());
String authHeaderValue = "Basic " + new String(encodedAuth);
```

#### 文档生成: POST /doc/make

* **描述**：生成文档 (账单、合同、报表、信件等)。

* **输入参数**：

  | Name            | Type    | Required | Default      | Description                                                                                                                                                   |
  | --------------- | ------- | -------- | ------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------- |
  | data            | String  | false    | null         | 生成文档需要的 XML 字符串。                                                                                                                                   |
  | template        | String  | true     | null         | 模板路径，如 /Template/sample.jasper。                                                                                                                        |
  | version         | String  | false    | null         | 模板的发布版本号，缺省情况下使用最新发布的模板。                                                                                                              |
  | date            | String  | false    | null         | 使用指定时间发布的最新模板，如果指定了 version，则此参数无效。                                                                                                |
  | status          | String  | false    | release      | 模板状态：release、prerelease、draft。                                                                                                                        |
  | local           | String  | false    | 系统默认语言 | 生成文档使用的语言。适用于配置了国际化资源文件的模板。                                                                                                        |
  | format          | String  | false    | pdf          | 文档格式，支持 pdf、html、rtf、xls、ps、csv、docx、txt。                                                                                                      |
  | preview         | boolean | false    | false        | 是否预览模板，如果是，则返回文档流。                                                                                                                          |
  | store           | boolean | false    | true         | 是否在 DMS 系统中保存文档。                                                                                                                                   |
  | parentFolderId  | String  | false    | null         | 父目录 ID，将生成的文档归属于某个目录。注意：此处目录不等价于文件系统中的目录。                                                                               |
  | async           | boolean | false    | false        | 是否异步。如果采用异步方式，DMS 将在后台生成文档，将处理结果通过 MQ 返回给客户端；客户端需要订阅对应的 topic。                                                |
  | transactionCode | String  | false    | null         | 事务号，异步方式必传此参数。                                                                                                                                  |
  | params          | String  | false    | null         | JSON 格式，传入模板的参数，需要在配置模板前约定好。                                                                                                           |
  | crt             | String  | false    | null         | 证书 ID。如果传递证书 ID，则使用该证书对文档进行签名，前提是证书已导入 DMS 系统，并且被启用；如果为 null，则使用 DMS 用户关联的证书进行签名；否则不进行签名。 |
  | id              | String  | false    | null         | 文档 ID。                                                                                                                                                     |
  | fileName        | String  | false    | null         | 文档名称。                                                                                                                                                    |
  | xmlPath         | String  | false    | null         | 大 XML 可以传入 XML 路径由 DMS 直接读取 XML 内容，要确保 DMS 有读取 XML 的权限。                                                                              |
  | cuttingRules    | String  | false    | null         | 大账单切分规则。                                                                                                                                              |
  | jrprintPath     | String  | false    | null         | jrprint 文件存放路径。                                                                                                                                        |
  | textConfig      | String  | false    | null         | 生成 TXT 格式的时字体相关的设置。                                                                                                                             |
  | pdfPassword     | String  | false    | null         | PDF 需要加密时设置密码。                                                                                                                                      |
  | shardingKey     | String  | true     | null         | MongoDB 模式的 DMS 下用于分表的值，防止单表数据太多，详见分表规则。                                                                                           |
  | docSavePath     | String  | false    | null         | 指定文档存放路径。                                                                                                                                            |

* **输出**：

| Condition    | Output Type | Description                                                                                                                                                                                                                                    |
| ------------ | ----------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| default      | String      | 通过 response header "Document-Id" 返回文档 ID。如果使用 MongoDB 作为存储介质，则该 ID 是长度固定为 24 的递增 UUID，如 580827f1e0bef821c32c5f6c；如果使用云盘作为存储介质，则 ID 是经过 Base64 编码的文档在云盘中的保存路径，长度在 150 以内。 |
| preview=true | byte[]      | 通过 response body 返回文档流。                                                                                                                                                                                                                |
| async=true   | Json String | 通过 MQ 发布处理结果，billing、crm、recharge 用户需要分别订阅对应的 topic，具体查看基于 MQ 的异步接口章节。                                                                                                                                    |

#### 文档生成: POST /doc/v2/make

* **描述**：一次生成多个文档接口。
* **输入参数**：

| Name    | Type   | Required | Default | Description                                            |
| ------- | ------ | -------- | ------- | ------------------------------------------------------ |
| docMake | String | true     | null    | 批量生成账单元数据 DocMakeRequest 对象的 JSON 字符串。 |

* **输出**：

| Condition  | Output Type                    | Description                                                                                                 |
| ---------- | ------------------------------ | ----------------------------------------------------------------------------------------------------------- |
| default    | Map<String, DocMakeTaskResult> | 批量生成账单结果，返回 Map 的 Key 为从入参中获取的文档标识，Value 为 DocMakeTaskResult。                    |
| async=true | String(Json)                   | 通过 MQ 发布处理结果，billing、crm、recharge 用户需要分别订阅对应的 topic，具体查看基于 MQ 的异步接口章节。 |

#### 文档查询: POST /query

* **描述**：根据文档标签或文档 ID 查询文档信息。
* **输入参数**：

| Name      | Type         | Required | Default | Description              |
| --------- | ------------ | -------- | ------- | ------------------------ |
| labels    | List<Label>  | false    | null    | 查询条件：文档标签列表。 |
| id        | List<string> | false    | null    | 查询条件：文档 ID 列表。 |
| beginDate | Long         | false    | null    | 查询条件：开始时间。     |
| endDate   | Long         | false    | null    | 查询条件：结束时间。     |
| union     | boolean      | false    | false   | 是否取交集。             |

* **输出**：

| Condition                | Output Type             | Description                      |
| ------------------------ | ----------------------- | -------------------------------- |
| 通过请求体传递文档标签   | Collection<documentdto> | 返回符合所有标签的文档信息列表。 |
| 通过 URL 参数传递文档 ID | Collection<documentdto> | 返回每个 ID 对应文档信息的合集。 |
| 两者都传递               | Collection<documentdto> | 返回以上两种结果的合集。         |

#### 文档下载: GET /doc/

* **描述**：下载由 DMS 生成并保存的文档或对应的 XML 数据。
* **输入参数**：

| Name       | Type    | Required | Default | Description                                     |
| ---------- | ------- | -------- | ------- | ----------------------------------------------- |
| id         | String  | true     | null    | 文档 ID。                                       |
| regenerate | boolean | false    | false   | 是否重新生成文档。                              |
| data       | boolean | false    | false   | 是否下载文档对应的 XML 数据。                   |
| crt        | boolean | false    | false   | 是否下载文档关联的证书。                        |
| token      | boolean | false    | false   | 值为 true 返回带 token 的文档链接，可直接访问。 |
| template   | boolean | false    | false   | 是否获取文档模板信息。                          |
| format     | String  | false    | null    | 下载时指定文档的格式。                          |

* **输出**：

| Condition       | Output Type      | Description                                      |
| --------------- | ---------------- | ------------------------------------------------ |
| default         | byte[]           | Response Body 返回文档二进制流。                 |
| data=true       | byte[]           | Response Body 返回 XML 数据二进制流。            |
| crt=true        | byte[]           | Response Body 返回经过 Base64 编码的证书字符串。 |
| sign=true       | byte[]           | Response Body 返回经过 Base64 编码的签名字符串。 |
| regenerate=true | byte[]           | 重新生成文档并通过 Response Body 返回二进制流。  |
| template=true   | application/json | 文档模板信息。                                   |

#### 文档删除: DELETE /doc/

* **描述**：删除 DMS 中保存的文档。
* **输入参数**：

| Name | Type   | Required | Default | Description |
| ---- | ------ | -------- | ------- | ----------- |
| id   | String | true     | null    | 文档 ID。   |

* **输出**：

| Condition | Output Type | Description                                                       |
| --------- | ----------- | ----------------------------------------------------------------- |
| default   | Boolean     | Response Body 返回布尔值。true 表示删除成功，false 表示删除失败。 |

#### 文档元数据查询: GET /doc/metadata/

* **描述**：根据文档 ID 查询文档元数据信息。
* **输入参数**：

| Name | Type   | Required | Default | Description         |
| ---- | ------ | -------- | ------- | ------------------- |
| id   | String | true     | null    | 查询条件：文档 ID。 |

* **输出**：

| Condition | Output Type         | Description                                  |
| --------- | ------------------- | -------------------------------------------- |
| default   | Map<string, object> | 元数据信息，包括 Filename，Content-type 等。 |

#### 单文档下载: GET /doc/single

* **描述**：下载由 DMS 批量接口生成或割接的文档。
* **输入参数**：参数名取决于 `ftf.dms.batch.docIdElements` 配置，例如 `BILLING_CYCLE_ID` (String, true), `BILL_NBR` (String, true)。

| Name             | Type    | Required | Default | Description                                     |
| ---------------- | ------- | -------- | ------- | ----------------------------------------------- |
| BILLING_CYCLE_ID | String  | true     | null    | 参数名取决于 ftf.dms.batch.docIdElements 配置。 |
| BILL_NBR         | String  | true     | null    | 参数名取决于 ftf.dms.batch.docIdElements 配置。 |
| crt              | boolean | false    | false   | 是否下载文档关联的证书。                        |
| sign             | boolean | false    | false   | 是否下载文档签名。                              |
| regenerate       | boolean | false    | false   | 是否重新生成文档。                              |
| data             | boolean | false    | false   | 是否下载文档对应的 XML 数据。                   |

* **输出**：

| Condition       | Output Type | Description                                      |
| --------------- | ----------- | ------------------------------------------------ |
| default         | byte[]      | Response Body 返回文档二进制流。                 |
| crt=true        | boolean     | Response Body 返回经过 Base64 编码的证书字符串。 |
| sign=true       | boolean     | Response Body 返回经过 Base64 编码的签名字符串。 |
| regenerate=true | boolean     | 重新生成文档并通过 Response Body 返回二进制流。  |
| data=true       | boolean     | Response Body 返回 XML 数据二进制流。            |

#### 批量文档下载: POST /doc/batch

* **描述**：批量下载由 DMS 批量接口生成或割接的文档。
* **输入参数**：Request Body 为一个 JSON 数组，每个元素包含构成文档 ID 的字段，例如 `[{"BILLING_CYCLE_ID": "63222", "BILL_NBR": "S207576090004194867"}, ...]`。
* **输出**：

| Condition | Output Type | Description                         |
| --------- | ----------- | ----------------------------------- |
| default   | byte[]      | Response Body 返回批量文档 ZIP 流。 |

#### 文件上传: POST /file

* **描述**：上传文件。
* **输入参数**：

| Name           | Type          | Required | Default | Description              |
| -------------- | ------------- | -------- | ------- | ------------------------ |
| file           | MultipartFile | true     | null    | 文件流。                 |
| parentFolderId | String        | false    | null    | 父目录 ID。              |
| id             | String        | false    | null    | 文件 ID。                |
| shardingKey    | String        | false    | null    | MongoDB 模式下分表的值。 |

* **输出**：

| Condition | Output Type | Description                                                                                                                                                                                                            |
| --------- | ----------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| default   | String      | Response Body 返回文件 ID。如果使用 MongoDB 作为存储介质，则该 ID 是长度固定为 24 的递增 UUID，如 580827f1e0bef821c32c5f6c；如果使用云盘作为存储介质，ID 是经过 Base64 编码的文件在云盘中的存储路径，长度在 255 以内。 |

#### 文件下载: GET /file/

* **描述**：下载文件。
* **输入参数**：

| Name  | Type    | Required | Default | Description                         |
| ----- | ------- | -------- | ------- | ----------------------------------- |
| id    | String  | true     | null    | 文件 ID。                           |
| token | boolean | false    | false   | 为 true 时返回带 token 的下载链接。 |

* **输出**：

| Condition  | Output Type | Description                |
| ---------- | ----------- | -------------------------- |
| default    | byte[]      | Response Body 返回文件流。 |
| token=true | String      | 文件的下载链接。           |

#### 文件批量下载: POST /file/batch

* **描述**：批量下载文件。
* **输入参数**：

| Name  | Type    | Required | Default | Description                         |
| ----- | ------- | -------- | ------- | ----------------------------------- |
| ids   | List    | true     | null    | 文件 ID 列表。                      |
| token | boolean | false    | false   | 为 true 时返回带 token 的下载链接。 |

* **输出**：

| Condition  | Output Type | Description                      |
| ---------- | ----------- | -------------------------------- |
| default    | byte[]      | Response Body 返回文件压缩包流。 |
| token=true | String      | 文件的下载链接。                 |

#### 文件重命名: PATCH /file/

* **描述**：重命名文件。
* **输入参数**：

| Name | Type   | Required | Default | Description |
| ---- | ------ | -------- | ------- | ----------- |
| id   | String | true     | null    | 文件 ID。   |
| name | String | true     | null    | 新文件名。  |

* **输出**：

| Condition | Output Type | Description                                          |
| --------- | ----------- | ---------------------------------------------------- |
| default   | Boolean     | Response Body 返回 true 表示命名成功，否则表示失败。 |

#### 文件删除: DELETE /file/

* **描述**：删除文件。
* **输入参数**：

| Name | Type   | Required | Default | Description |
| ---- | ------ | -------- | ------- | ----------- |
| id   | String | true     | null    | 文件 ID。   |

* **输出**：

| Condition | Output Type | Description                                          |
| --------- | ----------- | ---------------------------------------------------- |
| default   | Boolean     | Response Body 返回 true 表示删除成功，否则表示失败。 |

#### 文件元数据查询: GET /file/metadata/

* **描述**：根据文件 ID 查询文件元数据信息。
* **输入参数**：

| Name | Type   | Required | Default | Description         |
| ---- | ------ | -------- | ------- | ------------------- |
| id   | String | true     | null    | 查询条件：文件 ID。 |

* **输出**：

| Condition | Output Type         | Description                                  |
| --------- | ------------------- | -------------------------------------------- |
| default   | Map<string, object> | 元数据信息，包括 Filename，Content-type 等。 |

#### 批量查询文档元数据: POST /doc/metadata/

* **描述**：根据文档 ID 列表查询文档元数据列表。
* **输入参数**：

| Name | Type         | Required | Default | Description                            |
| ---- | ------------ | -------- | ------- | -------------------------------------- |
| ids  | List<string> | true     | null    | 文档 ID 列表，通过 Request Body 传递。 |

* **输出**：

| Condition              | Output Type               | Description                                  |
| ---------------------- | ------------------------- | -------------------------------------------- |
| 通过请求体传递文档标签 | List<map<string, object>> | 元数据列表，包括 Filename，Content-type 等。 |

#### 批量查询文件元数据: POST /file/metadata/

* **描述**：根据文件 ID 列表查询文件元数据列表。
* **输入参数**：

| Name | Type         | Required | Default | Description                            |
| ---- | ------------ | -------- | ------- | -------------------------------------- |
| ids  | List<string> | true     | null    | 文件 ID 列表，通过 Request Body 传递。 |

* **输出**：

| Condition                 | Output Type               | Description                                  |
| ------------------------- | ------------------------- | -------------------------------------------- |
| List<map<string, object>> | List<map<string, object>> | 元数据列表，包括 Filename，Content-type 等。 |

#### 统一下载接口: GET /material/

* **描述**：根据 ID 下载 File 或 Document。
* **输入参数**：

| Name | Type   | Required | Default | Description     |
| ---- | ------ | -------- | ------- | --------------- |
| id   | String | true     | null    | 文件或文档 ID。 |

* **输出**：

| Condition | Output Type | Description                |
| --------- | ----------- | -------------------------- |
| default   | byte[]      | Response Body 返回文件流。 |

#### 统一元数据查询接口: GET /material/metadata/

* **描述**：根据文档或文件 ID 查询元数据信息。
* **输入参数**：

| Name | Type   | Required | Default | Description               |
| ---- | ------ | -------- | ------- | ------------------------- |
| id   | String | true     | null    | 查询条件：文档或文件 ID。 |

* **输出**：

| Condition | Output Type         | Description                                  |
| --------- | ------------------- | -------------------------------------------- |
| default   | Map<string, object> | 元数据信息，包括 Filename，Content-type 等。 |

#### 统一批量查询文档元数据接口: POST /material/metadata/

* **描述**：根据文档或文件 ID 列表查询元数据列表。
* **输入参数**：

| Name | Type         | Required | Default | Description                                  |
| ---- | ------------ | -------- | ------- | -------------------------------------------- |
| ids  | List<string> | true     | null    | 文档或文件 ID 列表，通过 Request Body 传递。 |

* **输出**：

| Condition                 | Output Type               | Description                                  |
| ------------------------- | ------------------------- | -------------------------------------------- |
| List<map<string, object>> | List<map<string, object>> | 元数据列表，包括 Filename，Content-type 等。 |

### 基于 MQ 的异步接口

#### 描述

* **描述**：生成文档是性能代价较高的任务，DMS 提供通过 MQ 接收文档生成请求和发布请求处理结果的能力，以保持客户端线程通畅。

#### 接口协议 (接收请求/响应请求) (MQ Topic 配置)

* **描述**：客户端通过 MQ 向指定 topic 推送文档生成请求消息，DMS 订阅并处理；DMS 将文档生成结果通过 MQ 发布，客户端订阅对应 topic。
* **请求** MQ 消息字段：

| Name            | Description                                                  |
| --------------- | ------------------------------------------------------------ |
| transactionCode | 事务号。                                                     |
| data            | XML 数据。                                                   |
| template        | 模板路径。                                                   |
| format          | 生成文档的格式，默认为 pdf，还支持 html、rtf、csv、xls、ps。 |
| local           | 生成文档使用的语言，如 en-US，缺省为系统默认语言。           |
| username        | 用户名：billing、crm 或 recharge。                           |

* **响应 MQ 消息字段**：

| Name            | Description                    |
| --------------- | ------------------------------ |
| transactionCode | 事务号。                       |
| status          | 状态：succeeded 或 failed。    |
| docId           | 文档 ID。                      |
| errorMessage    | DMS 服务端生成文档的异常信息。 |

## 本文件评审、修正记录

| 文件名称 | ZSmart R9 DMS产品开发规范 |                                 |               |        |
| -------- | -------------- | ------------------------------- | ------------- | ------ |
| 序号     | 流程           | 拟制人/审核人                   | 拟制/审核时间 | 版本号 |
| 1        | 编写           | 沈维建/何永进，国际后端框架SCCB | 2025/12/18    | V0.1   |
| 2        | 发布           | 国际后端框架SCCB                | 2025/12/22    | V1.0   |
| 3        | 增加关于接口限流相关条目：4.6~4.9   | 沈维建/何永进，国际后端框架SCCB                | 2026/03/31    | V1.1   |
| 4        |发布         | 国际后端框架SCCB                | 2026/04/24    | V2.0   |
