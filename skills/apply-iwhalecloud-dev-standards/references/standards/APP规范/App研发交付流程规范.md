![image](uploads/254091/e8b082ce-19b5-4bbb-8859-b63959e4e2d3/image.png)

# 背景

目前公司的App产品的研发和交付，多数项目都是由研发人员全过程负责，包括从编码到上架，缺少有效的质量管控措施，并由此导致了一些现场故障，因此有必要对整体的研发和交付流程进行梳理。此外，App产品的研发和交付过程虽有其特殊性，例如上架过程基本上由底层平台厂家控制，需要按照平台厂家的规范进行操作，但在整体流程上与公司其他应用的交付过程没有本质上的区别，其研发、测试、交付这些阶段同样存在比较清晰的分界线，主要区别是其中有部分过程阶段需要借助App平台管理厂家所提供的工具来实现，如Apple 公司的App Store提供了一系列的工具用来辅助测试与上架的管理。

# 目的

为了规范App的发布过程，杜绝App在发布和升级过程中的人为故障，特制定本规范。

# 概念和术语

| 概念和术语        | 解释说明                                                                                                                                                                                                                                                                                                                                                                                                                                      |
| ----------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 开发者账号        | 开发者账号是平台厂家（Apple、Google、Huawei）提供的用于用户身份的管理标识，在 Google 平台上的开发者账号相对比较容易申请，在iOS 平台上分为3种：Apple Developer Program、Apple Developer Enterprise Program 或 iOS Developer University Program，目前使用最多的是第一种；第二种企业版账号注册难度较高，并且容易被封号；第三种面向大学生。可以用个人身份或者企业身份注册开发者账号，当以企业身份注册时，则可以管理一个团队，可以向团队里增加其他账号。 |
| 打包              | Android上一般只区分测试包和正式包，测试包带有一些 Debug 信息；对于 iOS平台因为安装的限制及分发渠道不同，会有多种不同的打包方式：App Store Connect，Ad Hoc， Enterprise， Development，其中第一种面向正常上架到 App Store， Ad Hoc常用于开发内部测试，有手机设备号限制，只有定义在清单内的设备才可以安装，Enterprise 用于企业内部分发，适用于企业版账号的开发者。                                                                              |
| App分发           | Android 的分发方式一般有两种：一种是分发到公开的App市场，国际一般是 Google Play Store，国内则是各大手机厂家的自建市场；另一种是私有市场或者自建市场，均无安装限制。iOS 分发渠道常见的有3种：一种是 App Store官方市场，最为常见；另一种基于企业版账号分发，包文件可以部署在企业内私有的服务器上，通过信任企业证书即可实现安装；还有一种也是面向私有分发的模式是 ABM（Apple Business Management），通过兑换码的形式实现安装。                   |
| App Store Connect | App Store Connect是苹果官方提供的用于 App 上架管理的门户工具，在集成了 TestFlight 工具以后，又具备了基本的研发过程管理能力。App Store Connect是面向 App 交付最常见的工具。                                                                                                                                                                                                                                                                    |
| TestFlight        | TestFlight工具是苹果官方提供的面向 App 交付的管理工具，已经被集成在 App Store Connect门户中，也是苹果官方推荐的面向App上架的流程管控工具。                                                                                                                                                                                                                                                                                                    |
| ABM               | 全称Apple Business Management，苹果公司推出的用于私有范围内分发 App 的一种模式，一般使用兑换码来下载安装，也需要通过苹果官方审核才能上架。                                                                                                                                                                                                                                                                                                    |
| 证书和签名        | 证书主要用来标识身份，开发者证书主要用于给 App 签名以识别 App 的开发者及拥有者，开发者证书可以在苹果官方提供的开发者门户网站上下载，由开发人员在代码构建时用于对 App 进行打包和签名                                                                                                                                                                                                                                                           |

# 角色

本规范主要涉及的角色包括：App开发团队、CMO配置管理员及App交付团队。

# App研发交付流程

分别针对 iOS 和 Android 的 App 研发和交付，描述不同角色在整体交付流程中的所从事的具体工作，鉴于App 研发领域之外的人对这块比较陌生，这里也提供了部分操作截图以供参考。

## iOS App研发交付流程

![image](uploads/69709/698124c4-86ab-4c4f-997d-6cbc75a55cce/image.png)

### 研发团队主要工作

#### 编码

> 主要对象：开发团队

1. 根据项目需求编写代码，遵守各类编码规范
2. 根据测试情况，修复各类 Bug

#### CI环境维护

> 主要对象：开发团队

iOS App的CI环境基于Mac系统，具有其特殊性，需要开发团队不定期维护才能保证CI流程顺利进行，主要包括安装证书执行一些账号校验。

#### CI自动打包

> 主要对象：研发云流程，开发团队

1. 开发团队负责完成流程各节点配置，触发流程执行
2. 研发云平台自动完成代码获取，编译打包，安全加固等流程节点。
3. **一个CI流程可能需要输出不同用途的包，需确保相同版本不同用途的包使用了同一份代码进行构建** （仅允许使用的构建脚本不同，构建脚本中仅允许切换证书及修改部分环境变量及参数），如：Debug包文件用于自测调试，UAT包文件用于现场客户验收测试，Release包文件正式分发上架。
4. Debug版本和UAT版本可以使用临时证书打包以方便高频测试和更新，自动对接上架到蒲公英市场；Release版本使用客户证书打包用于最终上架到App Store，App制品存储在预先定义好的研发云云存储的桶中方便CMO获取对应版本。如CMO 使用独立的打包流程，开发团队需要保证测试版本代码和 CMO正式 发布的打包的版本代码无差异。

#### 发布测试版本及UAT版本

> 主要对象：研发云流程，开发团队

1. Debug版本和UAT版本可通过配置CI/CD流程节点自动上架到蒲公英内测市场。

#### 高频自测

> 主要对象：开发团队

1. 开发团队从App内测市场（如蒲公英）中安装app进行测试

### CMO主要工作

#### 发布正式版本（ipa）

> 主要对象：配置管理员（CMO）

1. 由配置管理员（CMO）向现场发布用于正式上架的ipa包文件，其发布流程与其他应用发布流程相同。
2. **推荐由CMO基于测试通过的版本从研发云云存储的桶中获取对应的正式版本发布现场。如单独为 CMO 搭建了 CD 流程，相应的CD 环境由对应的项目团队负责维护。**
3. 流程启用以后，禁止开发团队直接向现场发布用于正式上架的ipa包文件。

### 交付团队的主要工作

1. **App Store Connect 环境管理** ，包括：App 管理（创建），管理项目 App 下用户和角色、管理项目 App 的 TestFlight 环境（用户及 Group，也可以授权测试团队负责）、组织TestFlight测试、将 App提交苹果官方审核，管理App分发（上架到 App Store或者私有ABM）。
2. **开发者门户管理** ，主要包括：下载签名证书发送开发团队用于构建带签名的 IPA 包。
3. 针对ABM 账号执行 ABM形式的 App分发。
4. 针对企业版账号执行企业内部分发。

#### App Store Connect 环境管理

##### App 管理

> 主要使用对象：客户或交付团队

###### 新建 App

一般情况下 App 应由客户提前创建好，并提供相关 App 信息给项目交付团队使用。如果客户不能提供，需要有项目交付团队代表客户对 App 进行初始化。

1. 使用客户的苹果账号登录 App Store Connect门户，[https://appstoreconnect.apple.com/](https://appstoreconnect.apple.com/)，选择 App，新建
2. 信息录入，App 名称应该是和客户商定以后的名称，主要关注套装 ID 和 SKU

- 套装ID，套件ID（Bundle ID）是一个唯一标识符，用于识别应用程序的唯一性。这里需要从下拉框中选择符合当前 App 的 Bundle ID，如果是第一次，需要在开发者门户中创建 Bundle ID。
- SKU是Stock Keeping Unit的缩写，是一种用于标识不同产品或服务的唯一标识符。可以为应用程序创建多个SKU，以便在App Store中销售不同版本、包装、价格和功能。公司App 一般都是同一种包装，这里建议使用产品名称缩写即可。

![image](uploads/69709/fcbb0a55-c633-4e4c-970a-f0a01a33f61c/image.png)

##### 用户和访问管理

> 主要对象：交付团队

1. 登录App Store Connect门户，[https://appstoreconnect.apple.com/](https://appstoreconnect.apple.com/)

2. 选择用户和访问，配置用户和职能

   ![image](uploads/69709/8ef91d33-35eb-4d96-83ec-55e5122f7c6d/image.png)

3. 重点关注左侧『开发者』和『App 管理』两个类别

   ![image](uploads/69709/e0d78b2b-3dc4-4a13-bb8b-06776811d71a/image.png)

4. 为开发人员定义『开发者』职能，可以将测试人员定义『App 管理』职能，并选择相应的 App 上，**邀请**以后，开发或测试人员将收到相关的邀请邮件。

   ![image](uploads/69709/0ca25c1b-ef5b-4175-8cb4-e1217b88834d/image.png)

   ![image](uploads/69709/8b17ed08-4104-4dd0-8ea5-089fdb9e9491/image.png)

5. 邀请邮件

   ![image](uploads/69709/8e8d4f9a-5371-42ca-9d72-9cfe68f69159/image.png)

6. 点击邮件中的链接接受邀请，登录App Store Connect门户以后，即可查看到相应的App信息

##### TestFlight 环境管理

> 主要对象：交付团队

- TestFlight是苹果官方推出的交付过程管控工具，具有 App 管理角色的账号可以对TestFlight环境进行管理，包括维护内部测试人员群组及人员名单，外部测试人员群组及人员名单，发送邮件邀请等。
- 内部测试人员是从 App Store Connect管理端用户名单中勾选，不超过100人，如下图

![image](uploads/69709/d434783d-38b8-4a07-9164-059fe382c2c5/image.png)

![image](https://dev.iwhalecloud.com/portal/zcm-doc/document/file/common/downloadFile?filePath=document/book-2337/doc/uploads/69905/4c89e918-ff56-4a91-8f15-212af567d750/image.png)

* 外部测试人员通过邮件地址发送测试邀请，不超过10000名，如下图

![image](uploads/69709/7b1c0bf6-d7df-47e1-9352-5f13691de8ae/image.png)

- 提交外部测试 Beta 版到 Apple 官方审核，包括选择 Build 版本，启用公开链接

![image](uploads/69709/ad05bc78-6022-4d16-ab5f-ca8fb6fb9781/image.png)

###### 内部测试

> 主要对象：测试团队

内部测试的主要工作包括：功能测试及终端适应性测试，记录和反馈测试过程中的问题

* 在收到内部测试邀请以后，会收到相关的邮件，点击链接接受邀请，可以进入到App 安装界面
* 如果测试手机上没有安装 TestFlight，根据引导进入 TestFlight 安装，也可以直接从App Store上安装
* 完成 App 安装以后可以执行 App 相关的功能测试
* 除了正常的功能测试，也需要开展终端适应性测试，如不同的iOS 版本，不同尺寸的手机屏幕等等
* 测试问题的反馈可以不通过 TestFlight 平台，可以继续通过公司的内部提单流程进行

###### 外部测试

> 主要对象：测试团队

* 外部测试的App 也可以通过 TestFlight 进行安装测试，也可以通过公开的 URL 地址进入安装界面。
* 正常情况下，外部测试的版本是相对成熟和稳定的版本，也可以邀请客户或者客户代表参与测试。

#### 开发者门户管理

##### 创建套装 ID

套件ID（Bundle ID）是一个唯一标识符，用于识别应用程序的唯一性。套件ID通常遵循反向域名的命名约定，以确保全球范围内的唯一性。一般情况下，Bundle ID定义需要遵循如下原则：

- 反向域名格式命名
- 全部小写
- 每个域名段中只适用字母、数字，
- 一般使用com.公司名缩写.产品名缩写形式，例如：com.pto.clp

操作参考：

- 使用客户账号，登录Apple开发者门户，[https://developer.apple.com](https://developer.apple.com)，找到『Certificates, IDs & Profiles』
- 进入开发者门户管理界面，选择 『Identifiers』，可以查看全部的标识符，根据上面的命名规则，可以为未来上架到App Store的 App创建一个全球唯一标识。

![image](uploads/69709/cfb7a8d5-6f49-4920-a0a7-61c2578dc63f/image.png)

![image](uploads/69709/61343e72-9900-4220-94ac-d7032fd9bf0f/image.png)

##### 证书管理

> 主要对象：交付团队

1. 在App 项目交付上架之前，需要使用客户的开发者账号导出证书，用于对 App 包签名，以便于用户在 App Store上正确识别 App 的归属方

2. 登录Apple 的开发者门户，[https://developer.apple.com/account](https://developer.apple.com/account)

   ![image](uploads/69709/316f6160-ce17-44e6-ac30-ad24c4167c60/image.png)

3. 选择本 App 项目归属方的标识证书，在详情页面，下载证书，发给开发团队用于 App 打包签名

![image](uploads/69709/e0b84211-daa0-4d61-93e2-55926f1175e8/image.png)

![image](uploads/69709/f8ea8ab8-bcfe-40c8-91d3-9902453ff79c/image.png)

#### App 分发管理

##### 公开市场分发 - 上架到App Store

###### 提交审核及App Store上架

> 主要对象：交付团队

1. 登录App Store Connect环境[https://appstoreconnect.apple.com/](https://appstoreconnect.apple.com/)，在主页选择 App，在App列表中选择期望提交审核的App，点击进入详情

2. 添加一个新版本，进入准备提交阶段

   ![image](uploads/69709/c52146ef-c2f3-46fa-b018-7975419a9447/image.png)

3. 准备相关信息，包括：预览截频文件、描述信息、推广文本、本次版本更新的内容描述，大部分信息可以从上一个版本中继承下来

4. **重点**：选择一个合适的 Build 版本

   ![image](uploads/69709/63da8de1-e2ad-462f-96eb-53f44199a668/image.png)

5. **重点**：选择App Store上架时的版本发布模式

   - 建议选择『手动发布此版本』或者定时发布，不建议选择『自动发布此版本』。
   - 自动更新部分可以选择『立即向所有用户发布更新』或使用『分阶段发布』，可以根据项目的实际情况选择，如紧急修复 App故障时，建议 使用『立即向所有用户发布更新』。

   ![image](uploads/69709/1ad9032d-c2f0-4e4d-bfef-473dfbd05b34/image.png)

6. 先点『存储』，随后『提交官方审核』

   ![image](uploads/69709/9ce24d2d-5a79-4b2b-8974-875a011bc8f5/image.png)

注，审核过程如果失败，可能需要根据反馈信息补充一些材料，需要交付人员与开发团队进行沟通并补充相关材料。

##### 私有分发 - ABM

###### ABM 相关概念

* ABM 全程Apple Business Management，只是用于分发的系统，不是开发 App 的系统，开发打包 App 还是要用个人开发者账号或公司开发者账号。
* ABM 是一种私有的分发方式，可以根据自己的需要控制 App分发的范围，用户通过兑换码才能下载安装。
* ABM 模式分发 App 之前也需要通过 App Store Connect提交苹果官方审核。
* 使用 ABM 之前需要先注册 ABM 账户，这个账户必须是企业法人才能注册，正常情况下是由客户提供

当客户选择以ABM 方式分发 App 时，需要我们的交付团队掌握 Apple 官方的相关要求以及分发流程。

###### ABM 分发的两种情况

| 使用方式 | 说明 | 使用场景 |
| ---- | ---- | ---- |
| 客户账号签名APP | 客户需提供开发者证书，浩鲸使用客户提供的证书打包/签名APP，客户登录App Store Connect提交应用，选择“Custom App / Private” 分发到客户自己的ABM组织 | 相当于客户委托浩鲸代表客户提交APP |
| 公司账号签名APP | 使用开发商（浩鲸）的证书打包/签名APP，开发者在自己的App Store Connect门户中提交应用，选择“Custom App / Private” 分发给客户所在的ABM组织 | 客户基于安全考虑，无法提供开发者证书，参见：[3795027](https://zmp.iwhalecloud.com/hppd/queryFauDtl.action?faultId=3795027) |

**注意：上述两种使用ABM私有分发的情形中，所使用的签名证书仅限普通账号（Apple Developer Program），不能是Apple企业账号（Apple Developer Enterprise Program）**

###### ABM 分发模式的正常流程

1. 注册/获取 ABM 账号后，可以登录苹果官方提供的 ABM 门户，[https://business.apple.com/](https://business.apple.com/)，点击左下账号 >> 偏好设置  >> 组织信息，获取组织 ID

   ![image](uploads/69709/8848aa87-c946-495c-b32e-7df00057744a/image.png)

2. 登录App Store Connect门户，[https://appstoreconnect.apple.com/](https://appstoreconnect.apple.com/)，在 App 分发界面，『价格与销售范围』，在 App 分发方式选择『
   **私人 — 在 Apple 商务管理或 Apple 校园教务管理上作为自定 App 提供**』，并录入 ABM 账户中获取的组织 ID 和组织名称。 此时在 ABM管理界面中就可以看到这个App。

   ![image](uploads/69709/d180a8df-ed13-4abd-82c4-57fa933cf3e1/image.png)

3. 再次进入到 ABM 管理门户，选择『自定App』，选择需要分发的 App购买许可，选『兑换码』，输入数量，『获取』，然后可以在兑换码列表中看到新增加的许可，下载后打开 Excel 文件，Excel 文件内部包含有兑换码以及下载链接，可以通过邮件或者消息的方式定点分享给企业相关人员，在苹果手机上，在浏览器URL中输入链接即可进入下载安装的界面。

   ![image](uploads/69709/14a39b95-da54-4611-9868-7aae4f113f02/image.png)

##### 企业版账号分发

> 主要对象：开发团队，交付团队

如果客户有申请自己的企业版账号，则可以在企业内部搭建独立环境来执行iOS App分发，一般流程如下：

- 对 ipa 文件进行企业签名，一般在 CI/CD环境执行，由开发团队负责执行，其中将使用到客户的企业版证书，对该证书需要严格管控，禁止用于与客户无关的 App签名。
- **搭建分发系统或平台**，一般情况下，可以集成在客户的门户网站中。
- 将企业签名的ipa文件上传到分发平台，并生成下载链接和二维码。
- 用户可以通过URL 地址下载或者扫码形式下载 ipa文件，并通过在手机中信任企业证书的形式安装App。

#### Firebase账号管理

> 主要对象：开发团队，交付团队

国际项目中普遍使用  Google Firebase作为消息推送的组件（跨平台组件，可同时用于 Android 和iOS 平台），Firebase有自己的账号管理体系，且开发团队交付团队都会参与到Firebase 账号管理相关流程中。

##### 交付团队的主要工作

1. Firebase 服务配置和功能开通；
   需要在Firebase环境中开通的有关功能和服务，一般情况下由开发团队提供相关清单，需要现场项目经理与所内开发团队进行沟通确认。
2. 创建 Firebase 项目；
   使用客户的 Google账号登录Firebase 管理门户[https://console.firebase.google.com/](https://console.firebase.google.com/)，创建 Firebase 项目，创建项目时需要提供的各种信息也需要与开发团队进行沟通确认。
3. 在Firebase门户界面中注册Apple 应用；
4. 生成并下载Firebase 配置文件（**GoogleService-Info.plist**）；
5. 完整的配置过程参见：[https://firebase.google.cn/docs/ios/setup](https://firebase.google.cn/docs/ios/setup)

##### 开发团队的主要工作

1. 从交付团队获取正式环境的Firebase 配置文件（**GoogleService-Info.plist**）；
2. 将配置文件集成到正式的 CI/CD环境中；
3. 禁止将项目正式环境中的配置文件 （**GoogleService-Info.plist** ）用于开发测试；

##### SSL PINNING配置注意事项

在某些项目中，处于通信安全的考量，客户会提出让客户端固定SSL Pinning证书的方式，防止中间人劫持（Man-In-The-Middle）并篡改报文。由于证书具有过期时间，如果在证书过期时间截止之前未更新证书，将会导致客户端的请求全部失效，造成严重的线上事故。所以建议在启用客户端固定证书的方式校验通信安全的项目中，考虑以下方案防止此等情况的出现：

1 启用备用域名，即同时使用正式域名和备用域名

2 正式域名和备用域名的访问证书有效期有序错开，相差在3~6个月

3 App需要支持正式域名通讯失败以后及时启用备用域名通讯的功能

4 在正式域名通讯失败以后，交付团队应及时下载新的证书，并通知研发团队及时打包新的 App并发布上架

5 正式域名通讯失败以后，如果判断新应用已发布上架，及时通知App用户及时更新和升级到新版本

注：某些云厂商例如AWS，启动证书自动托管功能，会在证书到期时间前一个月自动替换证书。

> 规范来源：严重生产故障[3790271](https://zmp.iwhalecloud.com/hppd/queryFauDtl.action?faultId=3790271)

## Android App研发交付流程

![image](uploads/69709/d61b84d9-c0b8-4e50-a8a0-eca87d003caa/image.png)

### 开发团队主要工作

#### 编码

> 主要对象：开发团队

1. 根据项目需求编写代码，遵守各类编码规范
2. 根据测试的意见，修复各类 Bug

#### 构建、打包、签名、加固

> 主要对象：开发团队

1. 维护 CI/CD环境，执行代码规范及代码检查要求
2. 使用工具生成 App签名文件，在正式发布之前，将签名文件配置到编译环境中，构建正式包。Android 的签名文件由开发人员使用 Java 配套工具生成，生成后的签名文件在源代码中进行管理
3. 正式发布的包文件需执行安全加固流程对 apk/aab 文件执行安全加固。

**apk/aab包的加固策略制定、使用、更新按照[《APP加固策略管理规范(Android)》](https://dev.iwhalecloud.com/doc/bidSU19/didsi76wmJe) 执行**

#### 高频内测

> 主要对象：开发团队

1. 开发团队直接从 CI 流程生成的制品仓库（目前是研发云的云存储）中安装 apk/aab 文件进行测试。
2. 根据测试情况修改相关代码以满足版本发布的质量要求。

### CMO主要工作

#### 发布正式版本（apk/aab）

> 主要对象：配置管理员（CMO）

1. 由配置管理员（CMO）向现场发布用于正式上架的apk/aab包文件，其发布流程与其他应用发布流程相同。
2. **配置管理员需基于测试通过的版本从研发云云存储的桶中获取对应的版本发布现场。**
3. 流程启用以后，禁止开发团队直接向现场发布用于正式上架的apk/aab包文件。

### 交付团队主要工作

Android App与 iOS  App应用不同，iOS App必须发布到 Apple官方提供的环境中才能安装到手机上进行真机测试，而 Android App则不需要，有apk 包文件就可以直接安装到手机中进行测试，因此 Android App的交付流程主要关注如何提交上架申请。

此外，正常情况下，Android App项目中仅2C 项目才需要上架到 Google Play Store公开市场，而国内的 Android App 公开市场则主要由几大手机厂商提供，如华为，小米，Vivo 等；当前公司里多数面向运营商员工的 Android App不需要上架到公开市场，一般可以使用自建私有市场进行 App 分发。因此流程上相对会简单一些。

交付团队的主要工作有两点：App 上架前的验证测试及提交 App上架。

#### App上架前的验证测试

- 从 CMO 发布的版本中获取 App 包文件（apk/aab），可基于 Google Play Store的管理门户执行上架前的『内部测试』，也可以直接安装进行测试，由于大多数情况都是客户进行上架操作，因此我们一般都是自己基于 apk 文件进行安装测试。
- 除了验证基本的业务功能外，需要验证 App 是否可以正常安装和显示操作，安卓版本的兼容性是否存在问题等。

#### App上架到Google Play Store

**目前情况绝大部分项目都是由客户自行操作**，交付团队在完成验证测试以后，将需要上架的apk/aab包文件提交给客户就行了。原则上 App 上架我们优先由客户来实施，确实有个别项目在客户不执行上架操作的话，由交付团队负责执行 App 上架操作，以 Google Play Store上架流程为例，提供相关操作和截图：

##### 上架前的准备工作

除 App Bundle（aab)文件外，其他项只在第一次上架的时候需要准备，后续有重大更新的时候会有少量更新，大部分情况下是复用的。

1. 谷歌开发者账号
2. App Bundle 文件
3. 512 * 512 像素 的 App Logo
4. 1024 * 500 像素 的 置顶大图
5. 4张 以上 APP 屏幕截图
6. 隐私协议地址、应用网站地址

##### Google Play Store上架

- 向客户申请操作账号，登录Google  Play Console 环境 [https://play.google.com/console/u/0/signup](https://play.google.com/console/u/0/signup)，在主页选择 App，在App列表中选择期望提交审核的App，点击进入详情。
- 进入到上架这一步，默认为已经完成了版本测试，因此选择正式版（Production），
- 选择国家和地区
- 创建发布版本, 点击右上角  **创建新的发布版本** ，开始发布应用。

![image](uploads/69709/c267981d-f565-425e-ac13-cf0ebaeede23/image.png)

* 选择签名密钥

首先 Google 生成的应用签名密钥无法下载，将完全由 Google Play 进行 **二次签名** 服务，使用默认值。

![image](uploads/69709/b5cda4bf-1979-4ecc-9b78-1309106fe313/image.png)

* 上传AAB文件（Android App Bundle），点击 Next

从 2021 年 8 月起，新应用需要使用 Android App Bundle，才能在 Google Play 中发布

![image](uploads/69709/5900acd1-ded2-4915-9e09-3b86033d623e/image.png)

* 设置发布版本详情

完成本次 **发布版本名称** 以及  **版本说明** ，并点击  **下一步** 。

- 预览并确认发布

正式发布后，Google play会对 App 进行自动审核，一般审核时间在 1-7 天左右，如果选择『关闭自管式发布模式』审核通过后会自动上架应用市场，反之如果你『开启自管式发布模式』，审核通过后需要手动『确认发布』，App会在几分钟内上架应用市场。可以在 **发布版本预览** 里看到版本最新的状态。

![image](uploads/69709/aa36fb75-9b95-4d4c-8a16-8cc41739a93e/image.png)

#### 其他平台上架

（略）

#### Firebase账号管理

> 主要对象：开发团队，交付团队

国际项目中普遍使用  Google Firebase作为消息推送的组件（跨平台组件，可同时用于 Android 和iOS 平台），Firebase有自己的账号管理体系，且开发团队交付团队都会参与到Firebase 账号管理相关流程中。

##### 交付团队的主要工作

1. Firebase 服务配置和功能开通；
   需要在Firebase环境中开通的有关功能和服务，一般情况下由开发团队提供相关清单，需要现场项目经理与所内开发团队进行沟通确认。
2. 创建 Firebase 项目；
   使用客户的 Google账号登录Firebase 管理门户[https://console.firebase.google.com/](https://console.firebase.google.com/)，创建 Firebase 项目，创建项目时需要提供的各种信息也需要与开发团队进行沟通确认。
3. 在Firebase门户界面中注册Android应用；
4. 生成并下载Firebase 配置文件（**google-services.json**）；
5. 完整的配置过程参见：[https://firebase.google.cn/docs/android/setup](https://firebase.google.cn/docs/android/setup)

##### 开发团队的主要工作

1. 从交付团队获取正式环境的Firebase 配置文件（**google-services.json**）；
2. 将配置文件集成到正式的 CI/CD环境中；
3. 禁止将项目正式环境中的配置文件（**google-services.json** ）用于开发测试；

##### SSL PINNING配置注意事项

在某些项目中，处于通信安全的考量，客户会提出让客户端固定SSL Pinning证书的方式，防止中间人劫持（Man-In-The-Middle）并篡改报文。由于证书具有过期时间，如果在证书过期时间截止之前未更新证书，将会导致客户端的请求全部失效，造成严重的线上事故。所以建议在启用客户端固定证书的方式校验通信安全的项目中，考虑以下方案防止此等情况的出现：

1 启用备用域名，即同时使用正式域名和备用域名

2 正式域名和备用域名的访问证书有效期有序错开，相差在3~6个月

3 App需要支持正式域名通讯失败以后及时启用备用域名通讯的功能

4 在正式域名通讯失败以后，交付团队应及时下载新的证书，并通知研发团队及时打包新的 App并发布上架

5 正式域名通讯失败以后，如果判断新应用已发布上架，及时通知App用户及时更新和升级到新版本

注：某些云厂商例如AWS，启动证书自动托管功能，会在证书到期时间前一个月自动替换证书。

> 参见[3790271](https://zmp.iwhalecloud.com/hppd/queryFauDtl.action?faultId=3790271)

# 附1：App流程执行要点（国际项目举例，限 iOS 平台）

1. 2C 项目（如：数渠 MPT/Libyana项目，在线产品线Vodapay/Claro项目）

* 证书和标识等均由客户提供，App 版权归属于客户。
* **软件分发渠道为 App Store公开市场。**
* 基于CI/CD流程打包.ipa，禁止开发人员基于本人机器打包正式发布的版本。
* 由CMO发版本到现场，禁止现场直接找开发人员拿版本。
* 项目交付团队获取.ipa文件以后，须通过 TestFlight 环境测试（内部测试/外部测试至少完成1个）以后才能提交上架审核，并选择手动更新。
* 项目交付团队成员需熟悉苹果官方提供的几个管理门户的相关操作（App Store Connect门户、开发者门户）。

2. 2B 项目，通过Apple Store发布App : （如数渠GAIA BX/DITO DSCM）

* 证书和标识等均由客户提供，App 版权归属于客户。
* **软件分发渠道为 App Store公开市场。**
* 基于CI/CD流程打包.ipa，禁止开发人员基于本人机器打包正式发布的版本。
* 由CMO发版本到现场，禁止现场直接找开发人员拿版本。
* 项目交付团队获取.ipa文件以后，须通过 TestFlight 环境测试（内部测试/外部测试至少完成1个）以后才能提交上架审核，并选择手动更新。
* 项目交付团队成员需熟悉苹果官方提供的几个管理门户的相关操作（App Store Connect门户、开发者门户）。

3. 2B 项目，通过ABM发布App : （如在线产品线Webe项目）

* 证书和标识等均由客户提供，App 版权归属于客户。
* **软件分发渠道为ABM 私有分发。**
* 基于CI/CD流程打包.ipa，禁止开发人员基于本人机器打包正式发布的版本。
* 由CMO发版本到现场，禁止现场直接找开发人员拿版本。
* 项目交付团队获取.ipa文件以后，须通过 TestFlight 环境测试（内部测试/外部测试至少完成1个）以后才能执行 ABM 分发。
* 项目交付团队成员需熟悉苹果官方提供的几个管理门户的相关操作（App Store Connect门户、开发者门户、 ABM管理门户）。

4. 2B 项目，客户使用EnterPrise自建发布平台，  : （如在线 Dito项目）

* App版权归属客户，EnterPrise账号、相关证书和标识等均由客户提供。
* **通过EnterPrise账号执行APP分发（自建安装网址、通过信任企业证书的形式执行 iOS 终端安装）**
* 由CMO发版本到现场，禁止现场直接找开发人员拿版本。
* 项目交付团队可以基于企业版账号创建单独的App 测试环境。
* 项目交付团队获取.ipa文件以后，先发布到App测试环境，在验证通过以后，再发布到正式环境。
* 项目交付团队成员需熟悉苹果官方提供的几个管理门户的相关操作（App Store Connect门户、开发者门户）。

# 附2：Apple 应用发布技术手册

## 整体概述

iOS应用的发布，会根据**开发者账号**的类型，**打包方式**的类型，**分发渠道**三个而不同。下图是一个整体的示例。
![image](uploads/38505/fb7bcaaa-02e1-48c2-8d8a-4f47df0c00ff/image.png)

## 开发者账号类型介绍

官方说明链接：[https://developer.apple.com/support/roles](https://developer.apple.com/support/roles)

- **Apple Developer Program**

  - **Personal Account （个人开发者，没有 Developer Team的概念）**
  - **Organization Account （公司开发者，可以邀请别的开发者成为自己的Developer Team的成员。例如 Claro，Vodapay）**
  - **发布渠道： ABM(**[**Apple Business Manager**](https://business.apple.com/)**) 和 Apple Store.**
  - **拥有App Store Connect后台权限。**
- **Apple Developer EnterPrise Program**

  - **发布渠道：自建渠道/第三方渠道（Fir.im，蒲公英）**
  - **无App Store Connect后台权限（无法上架苹果商店）**
- **iOS Developer University Program**（苹果公司针对大学生开设的一个计划，旨在帮助大学生们更好地学习 iOS 开发相关的知识）

### 开发者账号操作权限及建议

根据开发者账号操作权限及建议中的说明项目组需要在项目执行开始前，提前准备以下

- 让客户准备好开发者账号（新申请或已存在）。
- 产研开发提供一个开发者的账号，向客户申请对应App的开发者权限
- 项目组提供一个开发者账号，向客户申请对应App的App管理者权限（建议）

## 打包方式介绍

为了保证App的分发平台是可控的，以及保证所有安装到iOS设备上的App都是经过苹果官方允许的，苹果建立了iOS打包机制, 以下是苹果规定的4种打包方式

![image](uploads/38505/0610d5a2-b269-410f-8739-7809c9d8864f/image1.png)

### AppStore Connect

只有使用AppStore签名的包才可以上传到AppStore Connect上, 下面有2个用途

- 用于在TestFlight上分发
- 用于在AppStore上分发 ( 提交AppStore审核 -> 审核通过苹果后台会用Apple私钥对App数据进行加密签名生成ipa包；用户从AppStore下载App后，使用设备内置的Apple公钥解密验证，验证通过安装成功 )
  ![image](uploads/38505/c5cb617a-46eb-4e92-a5c4-8055b635599d/image2.png)

### 其他类型签名

- **Ad Hoc 分发**

AD-Hoc用于内部测试安装, 只能安装于指定设备上 (需要先获取设备UDID并注册，并且有最多100台	设备的限制)

- **Enterprise 分发**

企业内部分发，安装设备数量无限制，**但安装后需用户主动在设置->通用->VPN与设备管理中选择信任证书**

- **Development 分发**

开发调试只安装当前联调的设备

以下流程便是开发调试、AD-Hoc、In-House等方式打包安装App的过程，区别只在于第5步中设备IDs的匹配规则不一致

![image](uploads/38505/11b37577-dd51-469e-8932-24c507dc0d2b/image4.png)

## 分发渠道介绍 （Apple Store，ABM，自建渠道)

### 应用正式分发方式介绍

#### Apple Store

仅用于正式发布

- 适用于个人/公司开发者账号的AppStore Connect证书签名的iPA包
- iPA包通过AppStore下载
- 需要审核 (**每个国家地区都有对应的审核标准, 不同类型的App审核规则也不同**)

#### ABM

- 适用于个人/公司开发者账号的AppStore Connect证书签名的iPA包
- 需要申请一个Apple Business Manager账号
- App通过AppStore上通过兑换码兑换下载
- 适用于定制应用的组织内部员工
- 需要审核
- 分发方式上线后不可更改

### 应用测试分发方式介绍

#### TestFlight (苹果推荐使用)

- 适用于个**人开发者账号(Personal Account)** 或 **公司开发者账号(Organization Account)。**
- 用户可通过iPhone上的AppStore上下载的"**TestFlight**"应用, 在应用中下载对应的App。
- 可以创建多个群组, 每个群组可以添加不同的测试版本

##### 内部测试(Internal Testing)

一般用于功能测试，SIT测试，UAT测试

- 需要邀请对应人员加入账号用户组，赋予对应的角色职责, 详情可以参考官方说明: [https://developer.apple.com/cn/support/roles/](https://developer.apple.com/cn/support/roles/) 《Apple用户与职能》

  **项目组申请对应App的App管理角色**

  **产研开发申请对应App的开发者权限**

  - **需要邀请已经加入到用户组的成员到对应的测试小组。**
  - 可最多指定**100**名团队成员作为beta测试员, 每位成员可以在最多 **30**台设备上快速测试 Beta 构建版本
  - 上传iPA包后**30分钟**左右才能在开发者网站上关联到新的应用
  - **不需要审核**

![image](uploads/38505/3d2febb5-f2a1-4be6-b8a7-bd9ac12a451a/L1VzZXJzL3Rpbmd5dWFubHYvTGlicmFyeS9BcHBsaWNhdGlvbiBTdXBwb3J0L0RpbmdUYWxrTWFjLzM1MzE3NDUwNjNfdjIvSW1hZ2VGaWxlcy8xNjgxNzEzMDQyNTY4X0QwOUJFMjcwLTFCMDYtNDMwNy04QkRDLUEwRTkwOThEMUNBRS5wbmc.png)

##### 外部测试(External Testing)

一般用于UAT测试，内部灰度，外部灰度。PS : 外部灰度的方案由具体的业务需求决定，External Testing 仅仅作为可选方案的一种。

- 可以邀请多达10,000 **名外部测试员来测试你的 App，邀请测试员时，可以通过的**电子邮件**或者**公开链接(Public Link)来公开邀请任何人测试App。
- 生成公开链接时后应用通常需要**审核**, 一般A版本的第一次分发外测都需要审核, 审核时间大概1-2天左右
- 可以限制修改可通过公开链接加入群组的测试员人数

![image](uploads/38505/25fbcf5f-93f1-49f4-bfc7-802169bad644/L1VzZXJzL3Rpbmd5dWFubHYvTGlicmFyeS9BcHBsaWNhdGlvbiBTdXBwb3J0L0RpbmdUYWxrTWFjLzM1MzE3NDUwNjNfdjIvSW1hZ2VGaWxlcy8xNjgxNzEzMTA1MzE2Xzc2OEQ1QUYzLTU5MUQtNENCNC04MTFBLUNCRkIzMTE5RDkzNi5wbmc.png)

#### 第三方平台分发

常见的第三方平台有 **fir.im**、**蒲公英分平台**, 一般用于内部开发测试使用
**重点：强制开启密码访问。**

- 适用于**任意一种**开发者账号的Adhoc证书签名的iPA包
- 需要提前加需要安装的设备UDID(设备唯一标识) 加入到开发账号设备列表中, 每次新增设备都需要打包重新签名 (**不然下载后应用无法打开**)
- 开发账号设备列表上限为**99**, 每一年续费时才能删除不用的设备id (**所以请谨慎添加**)
- 不需要审核

#### 自建分发平台

可用于内部开发测试, 也可用于生产发布

- 仅适用于企业开发者账号(Apple Developer EnterPrise Program)的证书签名的iPA包
- iPA包通过客户的分发平台
- 不需要审核

# 附3：参考资料

[**《Apple用户与职能》**](https://developer.apple.com/cn/support/roles/)- 由 Apple 官方发布的关于苹果账号管理的使用手册，含角色权限定义及操作指南
[**《Apple TestFlight相关介绍》**](https://developer.apple.com/cn/testflight/)- 由Apple 官方发布的关于 TestFlight 测试管理平台的相关使用说明

# 附4：严重生产故障案例

| 故障单                                                                      | 故障时间  | APP 类型 | 复盘结论                    | 说明                                                                                                                                                                                            |
| --------------------------------------------------------------------------- | --------- | -------- | --------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [3063164](https://zmp.iwhalecloud.com/hppd/queryFauDtl.action?faultId=3063164) | 2022-11   | Android     | 账号管理问题                | 现场和Google 申请了一个APP Push 账号用于推送功能的测试使用，产品线和现场同时使用，账号从测试改成正式商用后，产品线继续用该账号进行测试，导致APP终端客户收到了测试消息。                         |
| [3110118](https://zmp.iwhalecloud.com/hppd/queryFauDtl.action?faultId=3110118) | 2022-12   | Android     | 账号管理问题 & 发布流程问题 | Firebase消息推送组件账号没有区分测试环境和商用环境，导致将海量测试消息发送到了客户终端。                                                                                                        |
| [3185617](https://zmp.iwhalecloud.com/hppd/queryFauDtl.action?faultId=3185617) | 2023-03   | iOS      | 发布&升级流程问题           | 开发人员在苹果 ABM平台上进行 APP 预演升级，但终端客户已经安装了该app旧版本，并且打开自动升级，不需要扫描二维码，会自动升级成已经发布的最新APP。                                                 |
| [3635198](https://zmp.iwhalecloud.com/hppd/queryFauDtl.action?faultId=3635198) | 2024-5-20 | iOS      | 发布&升级流程问题           | 技术上为第三方依赖包版本问题导致App闪退，流程上：开发人员正式打包环境（本机）与所内自测打包环境（自建流程）不一致，导致测试阶段未发现问题，此外现场上架阶段未走TestFlight，也没有经过客户测试。 |
| [3790271](https://zmp.iwhalecloud.com/hppd/queryFauDtl.action?faultId=3790271) | 2025-4-30 | iOS/Android      | 技术方案           | SSL PINNING开关打开时，固定客户端证书，证书到期后，客户端必须重新打包和发布新证书的 APP；主要原因在技术方案不完善，对意外情况考虑不足。 |

# 本文件评审、修正记录

| 文件名称 | App研发交付流程规范                                                                 |               |            |        |
| -------- | ----------------------------------------------------------------------------------- | ------------- | ---------- | ------ |
| 序号     | 流程                                                                                | 拟制人/审核人 | 修订时间   | 版本号 |
| 1        | 初版                                                                                | 林伟          | 2023-03-26 | V0.1   |
| 2        | 补充注意事项                                                                        | 林伟          | 2023-03-31 | V0.2   |
| 3        | 补充 开发者账号说明/开发者操作权限                                                  | 吕廷元        | 2023-04-06 | V0.3   |
| 4        | 细化不同类型发布、明确上线基本步骤和人员职责                                        | 林伟          | 2023-04-07 | V0.4   |
| 5        | 文档整体结构调整、文档部分用词规范                                                  | 吕廷元        | 2023-04-14 | V0.5   |
| 6        | 完善签名打包方式、分发渠道介绍补充、<br />ABM分发流程和自建分发渠道发布流程细化补充 | 林伟          | 2023-04-16 | V0.6   |
| 7        | 多份文档合并，结构调整，内容调整                                                    | 杨学书        | 2024-02-21 | V0.7   |
| 8        | 补充操作截图，细化流程活动描述                                                      | 杨学书        | 2024-03-01 | V0.8   |
| 9        | 补充Google Play Store上架描述                                                       | 王小虎        | 2024-03-04 | V0.9   |
| 10       | 修订流程及相关描述                                                                  | 杨学书        | 2024-06-22 | V0.10  |
| 11       | 根据评审意见修订-调整大纲结构，修订部分内容                                         | 杨学书        | 2024-08-21 | V0.11  |
| 12       | 正式发布                                                      | App规范组        | 2025-03-27 | V1.0   |
| 13       | 第5.1章节iOS App研发交付流程 和 第5.2章节Android App研发交付流程 均补充SSL PINNING固定证书开关打开时相应的APP处理建议。详见：<br>5.1.3.4.3. SSL PINNING配置注意事项<br>5.2.3.4.3. SSL PINNING配置注意事项<br>（规范来源：严重生产故障3790271）  | 杨学书        | 2025-08-20 | V1.0.1   |
| 14       | 发布                                                      | App规范组        | 2025-08-22 | V1.1   |
| 15       | 新增章节“5.1.3.3.2.2. ABM 分发的两种情况”（规范来源：严重生产故障3795027）      | 杨学书        | 2026-02-25 | V1.1.1   |
| 16       | 发布                                                      | App规范组        | 2026-03-23 | V1.2   |
| 17       | 更新章节“5.2.1.2. 构建、打包、签名、加固”，补充：apk/aab包的加固策略制定、使用、更新按照[《APP加固策略管理规范(Android)》](https://dev.iwhalecloud.com/doc/bidSU19/didsi76wmJe) 执行| 黄梦诗 | 2026-06-03 |V1.2.1|
| 18       | 发布                                                      | App规范组        | 2026-06-22 | V1.3   |
