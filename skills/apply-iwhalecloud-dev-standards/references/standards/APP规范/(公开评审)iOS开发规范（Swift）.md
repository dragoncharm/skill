![image](uploads/222703/2297957c-9007-4f45-b058-2238cf5c7387/image.png)

# 前言

编码规范对于程序员而言尤为重要，有以下几个原因：

* 一个软件的生命周期中，80%的花费在于维护。
* 几乎没有任何一个软件，在其整个生命周期中，均由最初的开发人员来维护。
* 编码规范可以改善软件的可读性，可以让程序员尽快而彻底地理解新的代码。
* 如果你将源码作为产品发布，就需要确任它是否被很好的打包并且清晰无误，一如你已构建的其它任何产品。

## 适用对象

浩鲸科技 swift 开发人员

## 目的

为了持续、稳定地开发出高质量，健壮的软件系统，为了保证团队中成员的编码质量，特制定本文档。用于规范团队内部开发过程，增加程序的健壮性，便于后续测试及代码维护，最终提高软件产品的生产力。

## 目录

- [正确性](#正确性)
- [命名规范](#命名规范)
- [代码组织](#代码组织)
- [格式规范](#格式规范)
- [注释指南](#注释指南)
- [类与结构体](#类与结构体)
- [函数设计](#函数设计)
- [闭包表达式](#闭包表达式)
- [类型系统](#类型系统)
- [内存管理](#内存管理)
- [控制流](#控制流)
- [版权声明](#版权声明)

## 正确性

✅ 优先确保代码警告不增加

## 命名规范

描述性且一致的命名能使代码更易阅读和理解。遵循《Swift API设计指南》中的命名规范，核心要点包括：

### 核心原则

- **调用点清晰性**：确保方法调用时的代码清晰可读
- **明确性优先**：明确性高于简洁性
- **命名格式**：
  - 使用驼峰式命名法（禁止使用蛇形命名法 `snake_case`）
  - 类型和协议使用大驼峰（`UpperCamelCase`）
  - 其他所有标识符使用小驼峰（`lowerCamelCase`）

### 命名策略

- **必要词汇**：包含所有必要词汇，省略冗余词汇
- **角色导向**：基于角色而非类型命名（如 `element`而非 `object`）
- **类型补偿**：在类型信息较弱时通过命名补充说明
- **流畅使用**：保持命名语句的语法流畅性

### 方法命名规则

| 类别                 | 规则                                                              |
| ---------------------- | ------------------------------------------------------------------- |
| 工厂方法             | 以`make`开头（`makeIterator()`）                                  |
| 副作用方法           | 通过命名体现副作用（`sort()`表示原地排序）                        |
| 动词方法（非变异版） | 使用`-ed`/`-ing`后缀（`sorted()`/`sorting()`）                    |
| 名词方法（变异版）   | 采用`formX`形式（`formUnion(_:)`）                                |
| 布尔类型             | 命名应像断言（`isEmpty`，`isDescending`）                         |
| 描述性协议           | 读作名词（`Collection`）                                          |
| 能力型协议           | 使用`-able`/`-ible`后缀（`Equatable`，`CustomStringConvertible`） |

### 术语选择

- **目标群体**：使用既不让专家意外也不让新手困惑的术语
- **缩写规范**：通常避免缩写（`initialize`优于 `init`）
- **历史沿用**：遵循既有命名惯例（`distance(to:)`优于 `distanceFrom(_:)`）

### 进阶规范

- **方法优先**：优先使用方法和属性而非自由函数
- **首字母处理**：统一处理首字母缩写（`HTTPResponse`或 `httpResponse`）
- **语义一致性**：相同含义的方法使用相同基名（`addChild(_:)`与 `addChildren(_:)`）
- **返回类型**：避免通过返回类型重载方法
- **参数命名**：选择能作为文档的优质参数名（`func move(from start: Point, to end: Point)`）

### 特殊场景

- **首个参数**：优先命名首个参数而非将其包含在方法名中（`addSubview(_ view: UIView)`）
- **闭包参数**：标注闭包和元组参数（`completion: (result: ResultType) -> Void`）
- **默认参数**：充分利用默认参数简化调用（`func join(_ separator: String = ",")`）

## 书面文档中的方法引用规范

在技术文档中引用方法名称时，必须保持表述无歧义。根据上下文选择适当的引用格式：

### 引用层级

1. **基础形式**（推荐）：仅使用方法名
   ✅ 示例：`addTarget`
2. **带参数标签**：标明参数占位符
   ✅ 示例：`addTarget(_:action:)`
3. **完整签名**：包含参数类型（仅必要时使用）
   ✅ 示例：`addTarget(_: Any?, action: Selector?)`

> 对于类似 `UIGestureRecognizer` 的方法引用场景，方案1既能保证明确性又最简洁。

### Xcode 操作技巧

**方法签名快速获取**：

1. 在Xcode编辑器中定位到目标方法
2. 同时按下 `Shift-Control-Option-Command-C`（四修饰键组合）
3. 系统将自动复制完整方法签名到剪贴板

### 最佳实践示例

```swift
class GestureHandler {
    func configureTap() {
        let recognizer = UITapGestureRecognizer(
            target: self,
            action: #selector(handleTap(_:))
        )
        // 推荐调用写法
        view.addGestureRecognizer(recognizer)
    }
  
    @objc private func handleTap(_ sender: UITapGestureRecognizer) {
        // 手势处理逻辑
    }
}
```

## 类前缀规范

### Swift 模块命名空间机制

✅ **自动命名空间**
Swift 类型通过所属模块自动获得命名空间，无需像 Objective-C 那样手动添加类前缀（如 `RW`）

### 命名冲突处理原则

| 场景               | 解决方案                     | 使用频率     |
| -------------------- | ------------------------------ | -------------- |
| 跨模块类型名冲突   | 使用`模块名.类型名` 格式引用 | 极少数情况   |
| 同模块内类型名重复 | 重构类型命名                 | 推荐优先采用 |

```swift
// 模块引用示例
import SomeModule

// 常规使用（无冲突时）
let normalInstance = UsefulClass()

// 解决命名冲突（当 SomeModule 和当前模块都包含 UsefulClass 时）
let specificInstance = MyModule.UsefulClass()  // 显式指定模块名前缀
```

## 委托方法规范

### 核心原则

✅ **首个参数设计**：
自定义委托方法的第一个未命名参数应为委托源对象（参考 UIKit 的委托设计模式）

#### 推荐模式 ✅

```swift
// 参数结构：委托源 + 事件参数
func namePickerView(_ namePickerView: NamePickerView, didSelectName name: String)

// 返回布尔值的委托方法
func namePickerViewShouldReload(_ namePickerView: NamePickerView) -> Bool
```

#### 不推荐模式 ❌

```swift
// 问题：缺少委托源参数
func didSelectName(namePicker: NamePickerViewController, name: String)

// 问题：未传递委托源对象
func namePickerShouldReload() -> Bool
```

## 类型推断上下文优化

### 核心原则

✅ 优先利用 Swift 的类型推断机制编写简洁代码（参见 [类型推断](https://docs.swift.org/swift-book/documentation/the-swift-programming-language/types/#Type-Inference)）

#### 推荐模式 ✅

```swift
// 选择器推断
let selector = #selector(viewDidLoad)

// 颜色常量简写
view.backgroundColor = .red

// 枚举类型推断
let toView = context.view(forKey: .to)

// 零矩形构造
let view = UIView(frame: .zero)
```

#### 不推荐模式 ❌

```swift
// 冗余类型限定
let selector = #selector(ViewController.viewDidLoad)

// 完整类型声明
view.backgroundColor = UIColor.red

// 显式枚举路径
let toView = context.view(forKey: UITransitionContextViewKey.to)

// 类型重复声明
let view = UIView(frame: CGRect.zero)
```

## 泛型命名规范

### 核心原则

✅ **类型参数命名**：

- 使用**描述性的大驼峰命名法**（当类型具有明确语义时）
- 无明确语义时可采用**单个大写字母**（T/U/V 等传统命名）

#### 推荐模式 ✅

```swift
// 语义明确的泛型参数
struct Stack<Element> { 
    // 元素操作逻辑
}

// 带类型约束的泛型
func write<Target: OutputStream>(to target: inout Target) {
    // 写入逻辑
}

// 传统单字母泛型
func swap<T>(_ a: inout T, _ b: inout T) {
    // 交换操作
}
```

#### 不推荐模式 ❌

```swift
// 无意义单字母命名（当存在语义时）
struct Stack<T> { ... }

// 小写泛型参数违反规范
func write<target: OutputStream>(to target: inout target)

// 无必要的复杂命名
func swap<Thing>(_ a: inout Thing, _ b: inout Thing)
```

## 语言规范

### 核心原则

✅ **统一拼写标准**：始终使用美式英语拼写以与 Apple 官方 API 保持一致

#### 推荐模式 ✅

```swift
// 颜色标识
let color = "red"

// 用户偏好存储
var favoriteColor: UIColor = .blue

// 国际化键值
let localizedString = NSLocalizedString("color_picker_title", comment: "")
```

#### 不推荐模式 ❌

```swift
// 英式拼写
let colour = "red"

// 混合拼写风格
var favouriteColor: UIColor = .green  // "favourite" 为英式拼写

// 非标准术语
let localizedString = NSLocalizedString("colour_picker_title", comment: "")## 代码组织规范
```

## 代码组织

### 核心原则

✅ **模块化扩展**：通过扩展（Extensions）将代码按功能逻辑分块组织，每个扩展使用 `// MARK: -` 注释进行视觉分隔

### 实施规范

| 场景     | 推荐做法               | 代码示例                                                          |
| ---------- | ------------------------ | ------------------------------------------------------------------- |
| 协议遵循 | 为每个协议创建独立扩展 | `extension ViewController: UITableViewDataSource { ... }`         |
| 功能模块 | 按业务逻辑划分扩展     | `// MARK: - 数据加载`<br />`extension FeedViewController { ... }` |
| 视图配置 | 分离UI布局相关代码     | `// MARK: - 界面配置`<br />`extension ProfileView { ... }`        |
| 工具方法 | 聚合工具类方法         | `// MARK: - 格式转换`<br />`extension DateFormatter { ... }`      |
| 生命周期 | 集中管理控制器生命周期 | `// MARK: - 生命周期`<br />`extension HomeViewController { ... }` |

```swift
class NetworkManager {
    // 主类核心属性和初始化
}

// MARK: - 请求处理
extension NetworkManager {
    func fetchData(from endpoint: String) async throws -> Data {
        // 网络请求核心逻辑
    }
}

// MARK: - 缓存管理
extension NetworkManager {
    private func cacheResponse(_ data: Data, forKey key: String) {
        // 缓存处理逻辑
    }
}

// MARK: - 错误处理
extension NetworkManager {
    func handleHTTPError(_ error: URLError) -> NetworkError {
        // 错误类型转换
    }
}


```

## 协议遵循规范

### 核心原则

✅ **分离扩展实现**：为每个协议创建独立扩展，通过 `// MARK: -` 注释明确协议分组

#### 推荐写法 ✅

```swift
class MyViewController: UIViewController {
    // 主类核心属性和方法
}

// MARK: - UITableViewDataSource
extension MyViewController: UITableViewDataSource {
    func tableView(_ tableView: UITableView, numberOfRowsInSection section: Int) -> Int {
        // 数据源方法实现
    }
}

// MARK: - UIScrollViewDelegate
extension MyViewController: UIScrollViewDelegate {
    func scrollViewDidScroll(_ scrollView: UIScrollView) {
        // 滚动代理方法实现
    }
}
```

#### 不推荐模式 ❌

```swift
class MyViewController: UIViewController, UITableViewDataSource, UIScrollViewDelegate {
    // 所有协议方法混杂在主类中
    func tableView(_ tableView: UITableView, numberOfRowsInSection section: Int) -> Int { ... }
    func scrollViewDidScroll(_ scrollView: UIScrollView) { ... }
}
```

## 未使用代码处理规范

### 核心原则

✅ **零容忍策略**：必须删除所有未使用的代码（包括 Xcode 模板代码、占位注释），除非教程明确要求保留

#### 推荐模式 ✅

```swift
// 只保留实际生效的代码
override func tableView(_ tableView: UITableView, numberOfRowsInSection section: Int) -> Int {
    return Database.contacts.count
}
```

#### 不推荐模式 ❌

```swift
// 保留无用的模板方法
override func didReceiveMemoryWarning() {
    super.didReceiveMemoryWarning()
    // 可删除的冗余注释
}

// 未完成的警告占位
override func numberOfSections(in tableView: UITableView) -> Int {
    // #warning Incomplete implementation, return the number of sections
    return 1
}

// 无意义的空实现
override func scrollViewDidEndDecelerating(_ scrollView: UIScrollView) {
    super.scrollViewDidEndDecelerating(scrollView) // 无实际作用的调用
}
```

## 最小化导入规范

### 核心原则

✅ **精准导入**：仅导入当前文件实际需要的模块，避免冗余依赖

#### 场景1：需要UIKit框架 ✅

```swift
import UIKit

var view: UIView        // 正确：UIView属于UIKit
var deviceModels: [String] // 字符串数组无需Foundation
```

#### 场景2：仅需Foundation ✅

```swift
import Foundation

var deviceModels: [String] // Foundation已包含基础类型
```

#### 不推荐模式1 ❌

```swift
import UIKit
import Foundation  // 冗余导入

var view: UIView
var deviceModels: [String]
```

#### 不推荐模式2 ❌

```swift
import UIKit        // 错误导入

var deviceModels: [String] // 字符串数组只需Foundation
```

## 缩进与大括号规范

### 核心规则

✅ **4空格缩进**：使用四个空格进行缩进（禁用制表符）
✅ **大括号同行规则**：控制语句的大括号起始于同一行

### 配置方法

#### Xcode 缩进设置路径：

1. 打开 `Xcode > Preferences > Text Editing`
2. 选择 `Indentation` 标签页
3. 配置选项：
   - 勾选 `Indent with: Spaces`
   - 设置 `Width: 4`
   - 勾选 `Automatically trim trailing whitespace`

### 代码格式示例

#### 推荐写法 ✅

```swift
// if-else 语句
if user.isHappy {
    print("今天心情很好！")
    showCelebrationAnimation()
} else {
    print("需要安慰用户")
    showSupportEmoji()
}

// 方法定义
func loadData(from endpoint: String) async throws -> Data {
    let request = URLRequest(url: endpointURL)
    return try await URLSession.shared.data(for: request).0
}
```

#### 不推荐模式 ❌

```swift
// 大括号换行错误
if user.isHappy
{
  print("错误的格式")
}
// 缩进不一致
else {
   print("缩进混合空格与制表符")
    showError()
}

```

## 空行管理规范

### 核心原则

✅ **视觉层次优化**：通过空行划分代码逻辑单元，提升可读性

### 空行应用规则

| 代码区域         | 空行数量 | 示例说明                                |
| ------------------ | ---------- | ----------------------------------------- |
| 方法/函数之间    | 1行      | `func methodA()`与 `func methodB()`之间 |
| 类型声明之间     | 1行      | 类/结构体/枚举定义之间                  |
| 协议扩展模块之间 | 1行      | `extension A`与 `extension B`之间       |
| 方法内部功能区块 | 按需添加 | 数据解析与UI更新之间                    |

### 代码示例

#### 推荐写法 ✅

```swift
let user = try await getUser(
  for: userID,
  on: connection)
```

#### 不推荐模式 ❌

```swift
// 类型声明间无间隔
let user = try await getUser(
  for: userID,
  on: connection
)
```

## 冒号与行格式规范

### 冒号间距规则

#### 核心原则

- **常规用法**：冒号左侧无空格，右侧单空格
- **例外情况**：
  - 三元运算符 `condition ? a : b`
  - 空字典字面量 `[:]`
  - Selector 语法 `#selector(addTarget(_:action:))`

#### 推荐写法 ✅

```swift
// ✅ 推荐写法
class DataParser: NSObject {
    var timeout: TimeInterval = 30.0
    var headers: [String: String] = ["Content-Type": "application/json"]
}
```

#### 不推荐模式 ❌

```swift
class DataParser : NSObject {
    var timeout :TimeInterval = 30.0
    var headers : [String:String] = ["Content-Type" : "application/json"]
}
```

## 行长与文件格式规范

### 行长控制原则

✅ **推荐换行阈值**：约70字符（根据上下文灵活处理）
✅ **换行策略**：优先在逻辑分隔点换行

#### 推荐写法（参数垂直对齐）✅

```swift
func configureTableView(
  dataSource: UITableViewDataSource,
  delegate: UITableViewDelegate,
  style: TableViewStyle = .plain
) {
  // 配置逻辑
}
```

#### 不推荐模式 ❌

```swift
func configureTableView(dataSource: UITableViewDataSource, delegate: UITableViewDelegate, style: TableViewStyle = .plain) { ... }
```

## 代码注释规范

### 核心原则

✅ **解释性注释**：仅在需要说明代码意图时添加注释，重点说明 **为什么** 而非 **做什么**
✅ **及时维护**：注释需随代码变更同步更新或删除
✅ **注释格式**：优先使用 `//` 或 `///`，禁用 C 风格 `/* ... */`

#### 推荐写法✅

```swift
// 使用哈希加速查找性能（数据集超过10k时）
let lookupTable = Dictionary(uniqueKeysWithValues: data.enumerated())
```

#### 不推荐模式❌

```swift
// 创建字典（冗余注释，代码已自解释）
let dict = [String: Int]()
```

# 类（Class）与结构体（Struct）的选择指南

## 何时使用结构体？

- **值语义**：结构体通过值传递。当数据不需要唯一标识时，应优先使用结构体。
- **示例**：
  包含 `[a, b, c]` 的数组与另一个包含 `[a, b, c]` 的数组完全等价且可互换。它们代表完全相同的内容，因此 Swift 的数组是结构体。
- **适用场景**：
  ✅ 无身份标识的数据（如日期、坐标）
  ✅ 轻量级数据模型（如 `UserProfile` 的姓名、登录时间）

## 何时使用类？

- **引用语义**：类通过引用传递。用于需要唯一标识或有特定生命周期的对象。
- **示例**：
  将 `Person` 建模为类：两个 `Person` 实例即使姓名和生日相同，仍是不同的对象（身份不同）。但 `Person` 的生日应使用结构体（如 `Date`），因为 `1950年3月3日` 的日期对象没有唯一性。
- **适用场景**：
  ✅ 需要身份标识的实体（如数据库连接、用户对象）
  ✅ 需要共享状态或生命周期管理（如 `UIViewController`）

---

## 特殊情况处理

- **历史遗留类型**：某些本应是结构体的类型（如 `NSDate`, `NSSet`）因历史原因以类形式存在。
- **协议约束**：若需遵循 `AnyObject` 协议（如代理模式），必须使用类。

### 示例 ✅

```swift
// 下面是一个样式良好的类定义的例子：

class Circle: Shape {
  var x: Int, y: Int
  var radius: Double
  var diameter: Double {
    get {
      return radius * 2
    }
    set {
      radius = newValue / 2
    }
  }

  init(x: Int, y: Int, radius: Double) {
    self.x = x
    self.y = y
    self.radius = radius
  }

  convenience init(x: Int, y: Int, diameter: Double) {
    self.init(x: x, y: y, radius: diameter / 2)
  }

  override func area() -> Double {
    return Double.pi * radius * radius
  }
}

extension Circle: CustomStringConvertible {
  var description: String {
    return "center = \(centerString) area = \(area())"
  }
  private var centerString: String {
    return "(\(x),\(y))"
  }
}
```

#### 上面的例子演示了以下样式指南：

* **多变量定义** : 如果多个变量或结构有共同的目的/上下文，可以在同一行中定义。
* **属性访问器** : `getter`、`setter` 定义以及属性观察器。
* **修饰符规范** : 不要在已经是默认的情况下添加诸如 `internal` 之类的修饰符。在重写方法时不要重复访问修饰符。
* **拓展组织** : 在扩展中组织额外的功能。
* **隐藏实现细节** : 隐藏非共享的实现细节。

## self的使用规则

### 必须使用 `self` 的场景

#### 逃逸闭包（Escaping Closures）

```swift

class DataLoader {
    var completion: (() -> Void)?
  
    func loadData() {
        // 必须显式使用 self 避免强引用循环
        fetchData { [weak self] in
            self?.handleCompletion()  // ✅ 正确
        }
    }
  
    private func handleCompletion() { ... }
}
```

#### 初始化器歧义消除

```swift
struct User {
    let id: String
    var name: String
  
    init(id: String, name: String) {
        self.id = id   // ✅ 必须使用（参数与属性同名）
        self.name = name.uppercased()
    }
}
```

### 应避免使用 self 的典型场景

```swift
class Counter {
    private var count = 0
  
    func increment() {
        count += 1     // ✅ 正确（直接访问属性）
        print(count)   // 不需要 self.count
    }
  
    func reset() {
        count = 0      // ✅ 直接赋值
    }
}
```

## Swift 计算属性编写规范

### 核心原则

✅ **只读属性省略 `get`**：当计算属性无需 setter 时，直接通过 `return` 返回结果
⛔ **避免冗余代码**：仅在同时需要 `set` 时显式声明 `get`

---

#### 推荐写法 ✅

```swift
var diameter: Double {
  return radius * 2
}

```

#### 不推荐模式 ❌

```swift
var getDiameter: Double {
  return radius * 2
}
```

## `final` 关键字的策略性使用指南

### 核心原则

✅ **聚焦核心逻辑**：教程代码优先保持简洁，默认不强制使用 `final`
🔑 **设计意图表达**：当需要明确禁止继承/重写时，`final` 可作为文档化工具

#### 推荐写法 ✅

```swift
// Turn any generic type into a reference type using this Box class.
final class Box<T> {
  let value: T
  init(_ value: T) {
    self.value = value
  }
}
```

## 函数定义规则

### 核心原则

✅ 保持简短的函数声明在一行，包括开始的大括号：
✅ 对于具有长签名的函数，将每个参数放在新行中，并在后续行中添加额外的缩进：
✅不要使用（Void）来表示缺少输入；只需使用（）。对于闭包和函数输出使用Void而不是（）。

#### 推荐写法 ✅

```swift
func reticulateSplines(spline: [Double]) -> Bool {
  // reticulate code goes here
}

func reticulateSplines(
  spline: [Double], 
  adjustmentFactor: Double,
  translateConstant: Int, 
  comment: String
) -> Bool {
  // reticulate code goes here
}

func updateConstraints() -> Void {
  // magic happens here
}

typealias CompletionHandler = (result) -> Void
```

#### 不推荐模式 ❌

```swift
func updateConstraints() -> () {
  // magic happens here
}

typealias CompletionHandler = (result) -> ()
```

## 函数调用

简短的函数调用一行，复杂的函数调用每个参数放在新行中

#### 推荐写法 ✅

```swift
// 简单函数调用
let success = reticulateSplines(splines)

// 长函数调用
let success = reticulateSplines(
  spline: splines,
  adjustmentFactor: 1.3,
  translateConstant: 2,
  comment: "normalize the display")
```

## 闭包调用

### 只有当参数列表末尾有一个闭包表达式形参时，才使用尾随闭包语法。给出闭包参数的描述性名称。

#### 推荐写法 ✅

```swift
UIView.animate(withDuration: 1.0) {
  self.myView.alpha = 0
}

UIView.animate(withDuration: 1.0, animations: {
  self.myView.alpha = 0
}, completion: { finished in
  self.myView.removeFromSuperview()
})
```

#### 不推荐模式 ❌

```swift
UIView.animate(withDuration: 1.0, animations: {
  self.myView.alpha = 0
})

UIView.animate(withDuration: 1.0, animations: {
  self.myView.alpha = 0
}) { f in
  self.myView.removeFromSuperview()
}
```

### 对于上下文清晰的单表达式闭包，使用隐式返回

#### 推荐写法 ✅

```swift
attendeeList.sort { a, b in
  a > b
}
```

### 使用末尾闭包的链式方法应该在上下文中清晰且易于阅读。

#### 推荐写法 ✅

```swift
let value = numbers.map { $0 * 2 }.filter { $0 % 3 == 0 }.index(of: 90)

let value = numbers
  .map {$0 * 2}
  .filter {$0 > 50}
  .map {$0 + 10}
```

## 类型

### 在可用的情况下，始终使用Swift的本地类型和表达式

#### 推荐写法 ✅

```swift
let width = 120.0                                    // Double
let widthString = "\(width)"                         // String

```

#### 不推荐模式 ❌

```swift
let width: NSNumber = 120.0                          // NSNumber
let widthString: NSString = width.stringValue        // NSString
```

## 宏定义

常量使用let关键字定义，变量使用var关键字定义

可以使用类型属性在类型上定义常量，而不是在该类型的实例上定义常量。要将类型属性声明为常量，只需使用静态let。以这种方式声明的类型属性通常优于全局常量，因为它们更容易与实例属性区分开来

#### 推荐写法 ✅

```swift
enum Math {
  static let e = 2.718281828459045235360287
  static let root2 = 1.41421356237309504880168872
}

let hypotenuse = side * Math.root2
```

#### 不推荐模式 ❌

```swift
let e = 2.718281828459045235360287  // pollutes global namespace
let root2 = 1.41421356237309504880168872

let hypotenuse = side * root2 // what is root2?
```

## 静态方法和变量类型属性

### 核心原则

🔍 **谨慎使用**：优先考虑实例方法和属性，仅在特定场景使用静态成员
🚀 **作用域约束**：当功能与类型强关联且无需实例状态时使用

### 工具方法（无状态操作）

```swift
struct MathUtils {
    // ✅ 与类型强关联的数学工具
    static func clamp(_ value: Int, min: Int, max: Int) -> Int {
        return Swift.max(min, Swift.min(value, max))
    }
}

let validValue = MathUtils.clamp(150, min: 0, max: 100)  // 输出 100
```

### 单例模式实现

```swift
final class AppSettings {
    // ✅ 线程安全单例
    static let shared = AppSettings()
    private init() {}
  
    var themeColor: UIColor = .systemBlue
}

// 使用示例
AppSettings.shared.themeColor = .darkGray
```

### 工厂方法

```swift
class NetworkRequest {
    // ✅ 创建预配置实例
    static func makeJSONRequest(url: URL) -> NetworkRequest {
        let request = NetworkRequest(url: url)
        request.addHeader("Accept", "application/json")
        return request
    }
  
    private func addHeader(_ key: String, _ value: String) { ... }
}
```

### Objective-C 互操作

```swift
@objc class LegacyBridge: NSObject {
    // ✅ @objc 暴露静态方法给 Objective-C
    @objc static func legacyFormat(text: String) -> String {
        return "[\(text)]"
    }
}
```

## 可选值

声明变量和函数返回类型为可选的？其中可以接受nil值。
使用用！声明的隐式未包装类型。只适用于你知道在使用之前要初始化的实例变量，比如将在viewDidLoad（）中设置的子视图。在大多数其他情况下，首选可选绑定而不是隐式取消包装的可选绑定。
当访问一个可选值时，如果该值只被访问一次，或者链中有很多可选值，则使用可选链：

```swift
textContainer?.textLabel?.setNeedsDisplay()
```

当一次展开并执行多个操作更方便时，使用可选绑定：

```swift
if let textContainer = textContainer {
  // do many things with textContainer
}
```

**Notes**: Swift 5.7 introduced new shorthand syntax for unwrapping optionals into shadowed variables:

```swift
if let textContainer {
  // do many things with textContainer
}
```

在命名可选变量和属性时，避免将它们命名为optionalString或maybeView，因为它们的可选性已经在类型声明中了。

对于可选绑定，尽可能隐藏原始名称，而不是使用unwrappedView或actualLabel之类的名称。

#### 推荐写法 ✅

```swift
var subview: UIView?
var volume: Double?

// later on...
if let subview = subview, let volume = volume {
  // do something with unwrapped subview and volume
}

// another example
resource.request().onComplete { [weak self] response in
  guard let self = self else { return }
  let model = self.updateModel(response)
  self.updateUI(model)
}
```

#### 不推荐模式 ❌

```swift
var optionalSubview: UIView?
var volume: Double?

if let unwrappedSubview = optionalSubview {
  if let realVolume = volume {
    // do something with unwrappedSubview and realVolume
  }
}

// another example
UIView.animate(withDuration: 2.0) { [weak self] in
  guard let strongSelf = self else { return }
  strongSelf.alpha = 1.0
}
```

## 懒加载

考虑使用延迟初始化对对象生命周期进行更细粒度的控制。对于延迟加载视图的UIViewController来说尤其如此。您可以使用立即调用{}（）的闭包，也可以调用私有工厂方法

```swift
lazy var locationManager = makeLocationManager()

private func makeLocationManager() -> CLLocationManager {
  let manager = CLLocationManager()
  manager.desiredAccuracy = kCLLocationAccuracyBest
  manager.delegate = self
  manager.requestAlwaysAuthorization()
  return manager
}
```

**Notes**:

[unowned self]在这里是不需要的，因为不会造成循环引用.

## 类型推断

使用类型推断特新来保持代码的简洁性

#### 推荐写法 ✅

```swift
let message = "Click the button"
let currentBounds = computeViewBounds()
var names = ["Mic", "Sam", "Christine"]
let maximumWidth: CGFloat = 106.5
```

#### 不推荐模式 ❌

```swift
let message: String = "Click the button"
let currentBounds: CGRect = computeViewBounds()
var names = [String]()
```

### 对于空数组和字典，使用类型注释。

#### 推荐写法 ✅

```swift
var names: [String] = []
var lookup: [String: Int] = [:]
```

#### 不推荐模式 ❌

```swift
var names = [String]()
var lookup = [String: Int]()
```

## 语法糖

选择类型声明的快捷版本，而不是完整的泛型语法

#### 推荐写法 ✅

```swift
var deviceModels: [String]
var employees: [Int: String]
var faxNumber: Int?
```

#### 不推荐模式 ❌

```swift
var deviceModels: Array<String>
var employees: Dictionary<Int, String>
var faxNumber: Optional<Int>
```

## 函数 vs 方法

### 基本原则

应谨慎使用不依附于类或类型的**自由函数**。在可能的情况下，优先使用方法而不是自由函数。这有助于提升代码的可读性和可发现性。

自由函数最适用于以下场景：

- 不与任何特定类型或实例相关联时

#### 推荐写法 ✅

```swift
let sorted = items.mergeSorted()  // 易于发现
rocket.launch()                  // 作用于模型对象
```

#### 不推荐模式 ❌

```swift
let sorted = mergeSort(items)    // 难以发现
launch(&rocket)

```

## 内存管理

### 基本原则

代码（包括非生产环境代码、教程示例代码）**不应创建循环引用**。请通过以下方式管理对象图：

1. 使用 `weak` 和 `unowned` 引用打破强引用循环
2. 优先使用值类型（struct, enum）从根本上避免循环

### 延长对象生命周期

使用 `[weak self]` 结合 `guard let self = self else { return }` 的惯用写法来显式延长生命周期：

#### 推荐写法 ✅

```swift
resource.request().onComplete { [weak self] response in
  guard let self = self else {
    return
  }
  let model = self.updateModel(response)
  self.updateUI(model)
}
```

#### 不推荐模式 ❌

```swift
resource.request().onComplete { [unowned self] response in
  let model = self.updateModel(response)
  self.updateUI(model)
}

resource.request().onComplete { [weak self] response in
  let model = self?.updateModel(response)
  self?.updateUI(model)
}
```

## 访问控制

### 基本原则

在教程示例代码中**无需完整声明访问控制级别**，但应当：

- 合理使用 `private` 和 `fileprivate` 增强代码清晰度
- 优先选用 `private`，仅在编译器强制要求时使用 `fileprivate`
- 完整声明 `open`/`public`/`internal` 仅在需要明确访问控制时使用

### 访问权限等级

| 修饰符        | 适用场景                             |
| --------------- | -------------------------------------- |
| `open`        | 允许模块外继承/重写                  |
| `public`      | 模块外可见但不可继承                 |
| `internal`    | 模块内默认访问权限（通常不显式声明） |
| `fileprivate` | 文件内可见                           |
| `private`     | 类型或作用域内可见（优先使用）       |

### 修饰符顺序规范

访问控制修饰符**必须作为属性修饰符的首位**，仅允许以下内容前置：

- `static` 修饰符
- 特殊属性标识符（`@IBAction`, `@IBOutlet`, `@discardableResult`）

#### 推荐写法 ✅

```swift
private let message = "Great Scott!"

class TimeMachine {  
  private dynamic lazy var fluxCapacitor = FluxCapacitor()
}
```

#### 不推荐模式 ❌

```swift
// 不推荐写法
fileprivate let message = "Great Scott!"

class TimeMachine {  
  lazy dynamic private var fluxCapacitor = FluxCapacitor()  // 修饰符顺序错误
}
```

## 控制流

### 基本原则

优先使用 `for-in` 循环模式，而非 `while` 条件递增模式。for-in 循环提供更简洁安全的语法，能够避免手动管理循环索引带来的潜在错误。

#### 推荐写法 ✅

```swift
// 基础遍历
for _ in 0..<3 {
  print("循环三次问候")
}

// 带索引遍历（元组解包）
for (index, person) in attendeeList.enumerated() {
  print("\(person) 位于位置 #\(index)")
}

// 步长控制遍历（开区间）
for index in stride(from: 0, to: items.count, by: 2) {
  print("偶数索引: \(index)")
}

// 逆序遍历
for index in (0...3).reversed() {
  print("倒计时: \(index)")
}
```

#### 不推荐模式 ❌

```swift
// 手动管理索引存在越界风险
var i = 0
while i < 3 {
  print("循环三次问候")
  i += 1
}

// 集合遍历应使用更安全的for-in
var j = 0
while j < attendeeList.count {
  let person = attendeeList[j]
  print("\(person) 位于位置 #\(j)")
  j += 1
}
```

## 三元运算符

### 基本原则

三元运算符 `?:` 仅在提升代码可读性或整洁度时使用，遵循以下准则：

- 应仅用于**单一条件判断**
- 多条件逻辑应改用 `if` 语句或通过重构为实例变量实现
- 最佳实践场景：变量赋值时的值选择决策

#### 推荐写法 ✅

```swift
// 简单值选择
let value = 5
result = value != 0 ? x : y

// 布尔值判断
let isHorizontal = true
result = isHorizontal ? viewWidth : viewHeight
```

#### 不推荐模式 ❌

```swift
// 嵌套三元运算符严重降低可读性
result = a > b ? x = c > d ? c : d : y
```

## 黄金路径原则

### 基本原则

编写条件语句时应遵循"黄金路径"（正常流程优先）准则：

- 主逻辑应保持**最左对齐层级**
- 避免嵌套 `if` 语句
- 允许多个 `return`/`throw` 提前退出
- 优先使用 `guard` 语句进行防御性检查

#### 推荐写法 ✅

```swift
func computeFFT(context: Context?, inputData: InputData?) throws -> Frequencies {
  // 前置条件检查
  guard let context = context else {
    throw FFTError.noContext
  }
  guard let inputData = inputData else {
    throw FFTError.noInputData
  }

  // 主逻辑保持最左对齐
  let analyzer = FrequencyAnalyzer(context: context)
  let frequencies = analyzer.process(inputData)
  
  // 结果后处理
  guard !frequencies.isEmpty else {
    throw FFTError.emptyResult
  }
  
  return frequencies
}
```

#### 不推荐模式 ❌

```swift
func computeFFT(context: Context?, inputData: InputData?) throws -> Frequencies {
  if let context = context {
    if let inputData = inputData {
      // 嵌套逻辑影响可读性
      let analyzer = FrequencyAnalyzer(context: context)
      let frequencies = analyzer.process(inputData)
  
      if !frequencies.isEmpty {
        return frequencies
      } else {
        throw FFTError.emptyResult
      }
    } else {
      throw FFTError.noInputData
    }
  } else {
    throw FFTError.noContext
  }
}
```

## 可选值解包规范

### 基本原则

当需要解包多个可选值时，优先使用复合解包模式来最小化代码嵌套：

- 使用 `guard` 语句进行提前退出检查
- 每个解包条件独立成行
- 错误处理块与 `guard` 保持对齐层级
- 仅在需要继续使用解包值时使用 `if let`

#### 推荐写法 ✅

```swift
// 复合解包模式
guard 
    let number1 = number1,
    let number2 = number2,
    let number3 = number3,
    number1 > 0,          // 可组合其他条件
    number2.isValid()
else {
    fatalError("参数不合法")
}

// 正常业务流程（无嵌套）
calculateResult(number1, number2, number3)
```

#### 不推荐模式 ❌

```swift
// 多层嵌套影响可读性
if let number1 = number1 {
    if let number2 = number2 {
        if let number3 = number3 {
            if number1 > 0 {
                if number2.isValid() {
                    calculateResult(number1, number2, number3)
                }
            }
        }
    }
}

// 离散的错误处理
guard let number1 = number1 else {
    fatalError("缺失number1")
}
guard let number2 = number2 else {
    fatalError("缺失number2")
}
guard let number3 = number3 else {
    fatalError("缺失number3")
}
```

## 守卫语句失败处理规范

### 基本原则

守卫语句（Guard）的失败分支必须包含明确的退出操作，遵循以下准则：

- 使用单行退出语句（`return`/`throw`/`break`/`continue`/`fatalError()`）
- 避免在失败分支编写复杂逻辑
- 需要资源清理时使用 `defer` 代码块

#### 推荐写法 ✅

```swift
func processFile(at path: String) throws {
    guard !path.isEmpty else {
        throw FileError.invalidPath  // 单行错误抛出
    }
  
    let fileHandle = try FileHandle(forReadingFrom: URL(fileURLWithPath: path))
    defer {
        fileHandle.closeFile()  // 确保资源释放
    }
  
    guard let data = try fileHandle.readToEnd() else {
        return  // 简单提前返回
    }
  
    // 主处理逻辑
}
```

#### 不推荐模式 ❌

```swift
func validateUser(_ user: User?) -> Bool {
    guard let user = user else {
        print("Error: nil user")  // 副作用操作
        Logger.logError()
        UIApplication.shared.showErrorAlert()  // 视图相关操作
        return false
    }
    // 业务逻辑
}
```

## 分号使用规范

### 基本原则

Swift **不要求**在语句末尾使用分号，仅在以下场景需要：

- 同一行书写多个独立语句时（应尽量避免）
- 编译器要求消除语法歧义的极特殊情况

#### 推荐写法 ✅

```swift
// 单行单语句（无分号）
let language = "Swift"

// 多行语句（自然换行）
let features = [
    "Type Safety",
    "Memory Management",
    "Protocol Oriented"
]
```

#### 不推荐模式 ❌

```swift
// 单行单语句带多余分号
let paradigm = "Multi-Paradigm";

// 多语句挤占单行（应分多行书写）
var count = 0; count += 1; print(count)
```

## 括号使用规范

### 基本原则

在 Swift 条件表达式中**无需添加冗余括号**，仅在以下场景选择性使用：

- 提升复杂表达式的可读性
- 明确运算优先级（当运算符优先级不明显时）

#### 推荐写法 ✅

```swift
// 简单条件判断（无括号）
if username.isEmpty {
    showError("用户名不能为空")
}

// 复合条件保持简洁
guard !isProcessing, let data = cachedData else {
    return
}

// 提升复杂表达式可读性
let scoreMultiplier = (hasBonusLevel && isVIP) ? 3 : 1
```

#### 不推荐模式 ❌

```swift
// 冗余的条件括号
if (temperature > 35) {
    activateCoolingSystem()
}

// 不必要的嵌套括号
while ((attempts < maxAttempts) && !isSuccess) {
    retryConnection()
}
```

## 多行字符串字面量规范

### 基本原则

构建长字符串时应优先使用**三引号多行字面量语法**，遵循以下格式准则：

- 起始三引号与赋值语句保持同行
- 文本内容整体缩进一级（相对于外层代码）
- 使用反斜杠 `\` 消除换行符（需保留行内连续性时）
- 避免使用 `+` 操作符拼接字符串片段

#### 推荐写法 ✅

```swift
let message = """
  您无法使用 9V 电池为时空跃迁装置 \
  供电。必须使用超级电容器进行充能，\
  当前剩余能量单元为 \(energyUnits)。
  """
```

#### 不推荐模式 ❌

```swift
let message = """You cannot charge the flux \
  capacitor with a 9V battery.
  You must use a super-charger \
  which costs 10 credits. You currently \
  have \(credits) credits available.
  """

let message = "You cannot charge the flux " +
  "capacitor with a 9V battery.\n" +
  "You must use a super-charger " +
  "which costs 10 credits. You currently " +
  "have \(credits) credits available."
```

## 图像与颜色资源使用规范

### 基本原则

禁止在代码中直接使用 `#imageLiteral` 和 `#colorLiteral` 语法糖，应使用以下显式初始化方式：

- 颜色资源：通过 `UIColor`/`NSColor` 的初始化方法或资源名称加载
- 图像资源：通过 `UIImage`/`NSImage` 的命名构造器加载

#### 推荐写法 ✅

```swift


// 颜色 - 资源名称加载（需在 Assets 中定义）
let themeColor = UIColor(named: "PrimaryTheme")

// 图像 - 资源名称加载
let iconImage = UIImage(named: "settings_gear")

// 颜色 - RGB 值初始化
let primaryColor = UIColor(
    red: 0.12, 
    green: 0.58, 
    blue: 0.95, 
    alpha: 1.0
)
```

#### 不推荐模式 ❌

```swift
let badColor = #colorLiteral(red: 0.12, green: 0.58, blue: 0.95, alpha: 1.0)
let badImage = #imageLiteral(resourceName: "settings_gear.png")
```

