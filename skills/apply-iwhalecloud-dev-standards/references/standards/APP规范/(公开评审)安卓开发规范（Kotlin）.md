![image](uploads/222705/5f20f380-d933-432c-94f3-2f33fecfd1bd/image.png)

# 前言

编码规范是开发人员之间的共同约定，遵守开发规范会带来几个明显的好处：

* 有利于团队分工合作，相同风格的代码，使得不同的人员开发的代码整合起来更加容易；
* 有利于提升代码质量，减少Bug数，尤其是一些低级Bug，遵守规范会自动规避一些低级错误；
* 有利于技术传承和代码维护，规范的代码可以获得继任者的钦佩而不是相反；
* 遵守代码规范有利于开发人员提升自我修养，对于个人成长也是有利的；

## 适用对象

浩鲸科技 Android APP开发人员（Kotlin）

## 目的

为了持续提升公司APP产品质量和稳定性，特制定本规范，让公司的APP开发人员拥有相同的基础开发话术，促进相互沟通和理解，也便于公司APP技术传承，让继任者能够很容易的维护和升级产品源代码

# 编程规范

## 文件名

### 【强制】如果源文件只包含一个顶级类，则文件名应为该类的名称（区分大小写）加上 .kt 扩展名。

正例

```java
// MyClass.kt
class MyClass { }
```

反例

```java
// YourClass.kt
class MyClass { }
```

> [standard:filename](https://pinterest.github.io/ktlint/latest/rules/standard/#file-name)

### 【推荐】如果源文件包含多个顶级声明，则应选择一个可描述文件内容的名称（采用驼峰风格形式）并加上 .kt 扩展名。

正例

```java
// Bar.kt
class Bar { }
fun Runnable.toBar(): Bar = // …
```

反例

```java
// XXX.kt
class Bar { }
fun Runnable.toBar(): Bar = // …
```

> [standard:filename](https://pinterest.github.io/ktlint/latest/rules/standard/#file-name)

## 包名

### 【强制】包名称全部为小写字母.

正例

```java
package com.example.data
```

反例

```java
package com.example.Data
```

> [standard:package-name](https://pinterest.github.io/ktlint/latest/rules/standard/#package-name)

### 【推荐】通常不鼓励使用多个词的名称，但是如果确实需要使用多个词，可以将连续的单词直接连接在一起（没有下划线）.

正例

```java
package com.example.deepspace
```

反例

```java
package com.example.deepSpace

package com.example.deep_space
```

## 类、对象和接口名

### 【强制】类、对象和接口名采用首字母大写, 驼峰风格形式编写

通常是名词或名词短语。例如，Character 或 ImmutableList。接口名称也可以是名词或名词短语（例如 List），但有时还可以是形容词或形容词短语（例如 Readable）。

测试类的命名方式是以测试的类的名称开头且以 Test 结尾。例如，HashTest 或 HashIntegrationTest。

正例

```java
class UserRepository
interface ClickListener
object DatabaseHelper
```

反例

```java
class userRepository
```

> [standard:class-naming](https://pinterest.github.io/ktlint/latest/rules/standard/#class-naming)

### 【强制】函数和方法名称采用首字母小写, 驼峰风格形式编写，通常是动词或动词短语。

正例

```java
fun sendMessage(){}

fun stop(){}
```

反例

```java
fun SendMessage(){}
```

允许在测试函数名称中出现下划线，用于分隔名称的逻辑组成部分。

```java
@Testfun pop_emptyStack(){
    // …
}
```

> [standard:function-naming](https://pinterest.github.io/ktlint/latest/rules/standard/#function-naming)

### 【强制】带有 @Composable注解且返回 Unit 的函数都采用 PascalCased 大小写形式并以名词形式命名，就像它们是某种类型。

正例

```java
@Composable
fun NameTag(name:String){
    // …
}
```

反例

```java
@Composable
fun nameTag(name:String){}
```

### 【强制】函数名称不应包含空格，因为并非所有平台都支持函数名称包含空格（值得注意的是，Android 不支持函数名称包含空格）。

正例

```java
fun testEveryPossibleCase(){}
```

反例

```java
fun`test every possible case`(){}
```

## 变量和属性名

### 【强制】使用首字母小写, 驼峰风格形式编写, 变量名通常是名词或名词短语。

正例

```java
var itemCount: Int
val userName: String = "name"
val mutableCollection: MutableSet = HashSet()
```

反例

```java
var ItemCount: Int
```

> [standard:property-naming](https://pinterest.github.io/ktlint/latest/rules/standard/#property-naming)

## 常量名

### 【强制】常量名称使用全部为大写字母形式，单词用下划线分隔。

常量是没有自定义 get 函数的 val 属性，其内容绝对不可变。这包括不可变类型和不可变类型的不可变集合，以及标量和字符串（如果标记为 const）。

正例

```java
val NAMES = listOf("Alice","Bob")
val AGES = mapOf("Alice" to 35,"Bob" to 32)
val COMMA_JOINER =Joiner.on(',')// Joiner is immutable
val EMPTY_ARRAY = arrayOf()
```

反例

```java
val Names = listof("Alice","Bob")
```

### 【强制】作为标量值的常量必须使用 const 修饰符。

正例

```java
const val NUMBER = 5
```

反例

```java
val NUMBER = 5
```

## 后备属性名

### 【强制】需要后备属性时，其名称应与实际属性的名称完全匹配，只不过带有下划线前缀。

正例

```java
//后备属性
private var _table: Int = 3
//对外暴露属性
val table: Int = _table
```

反例

```java
//后备属性
private var table: Int = 3
//对外暴露属性
val tableEx: Int = table
```

> [standard:backing-property-naming](https://pinterest.github.io/ktlint/latest/rules/standard/#backing-property-naming)

## 泛型变量名称

### 【强制】可以采用以下两种样式之一对每个泛型变量命名：

一个大写字母，可选择在其后跟一个数字（例如 E、T、X 和 T2）

用于类的形式的名称，后跟大写字母 T（如 RequestT 和 FooBarT）

正例

```java
class Box<T>(t: T) {
    var value: T = t
}
```

反例

```java
class Box<a>(t: a) {
    var value: a = t
}
```

## 枚举类

### 【强制】枚举项的名称应使用大写下划线分隔格式。

正例

```java
enum class Bar {
    FOO,
    Foo,
    FOO_BAR,
    FooBar,
}
```

反例

```java
enum class Bar {
    foo,
    bAr,
    Foo_Bar,
}
```

> [standard:enum-entry-name-case](https://pinterest.github.io/ktlint/latest/rules/standard/#enum-entry)

### 【推荐】枚举（enum）应写在单行中，或者每个枚举项需要单独占一行。如果枚举中既包含枚举项又包含其他声明（如方法或属性），则枚举项和声明之间需要用一个空行分隔。

正例

```java
enum class Foo { A, B, C, D }

enum class Foo {
    A,
    B,
    C,
    D,
    ;

    fun foo() = "foo"
}
```

反例

```java
enum class Foo {
    A,
    B, C,
    D
}

enum class Foo {
    A;
    fun foo() = "foo"
}
```

> [standard:enum-wrapping](https://pinterest.github.io/ktlint/latest/rules/standard/#enum-wrapping)

## 驼峰式大小写

有时，有多种合理的方法可将英语短语转换为驼峰命名法，例如，当存在首字母缩写词或者诸如“IPv6”或“iOS”之类不寻常的构造时。要提高可预测性，请使用以下方案。

从名称的普通形式入手：

1. 将短语转换为纯 ASCII 并移除所有撇号。例如，“Müller’s algorithm”可能会变为“Muellers algorithm”。
2. 将此结果分成单词，在空格和其余所有标点符号（通常是连字符）处分割。建议：如果任何单词在常见用法中已有惯用的驼峰式大小写外观，请将其分成各个组成部分（例如，“AdWords”将变为“ad words”）。请注意，诸如“iOS”之类的单词实际上本身并未采用驼峰命名法；它违反了任何惯例，所以此建议不适用。
3. 现在，将所有内容（包括首字母缩写词）小写，然后执行以下某项操作：
   * 将每个单词的第一个字符大写。
   * 将除第一个单词之外的每个单词的第一个字符大写，以生成驼峰命名法。
4. 最后，将所有单词连接成一个标识符。

请注意，原始单词的大小写几乎完全被忽略。

| **普通形式**       | **正确**    | **不正确**  |
| ------------------------ | ----------------- | ----------------- |
| “XML Http Request”     | XmlHttpRequest    | XMLHTTPRequest    |
| “new customer ID”      | newCustomerId     | newCustomerID     |
| “inner stopwatch”      | innerStopwatch    | innerStopWatch    |
| “supports IPv6 on iOS” | supportsIpv6OnIos | supportsIPv6OnIOS |
| “YouTube importer”     | YouTubeImporter   | YoutubeImporter*  |

（* 可接受，但不建议。）

3. 代码格式

## 缩进

### 【强制】使用 4 个空格缩进。不要使用 tab。

### 【推荐】对于花括号，将左花括号放在结构起始处的行尾，而将右花括号放在与左括结构横向对齐的单独一行。

正例

```java
if (elements != null) {
    for (element in elements) {
        // ……
    }
}
```

> 在 Kotlin 中，分号是可选的，因此换行很重要。语言设计采用 Java 风格的花括号格式，如果尝试使用不同的格式化风格，那么可能会遇到意外的行为。

反例

```java
if (elements != null) 
{
    for (element in elements) 
    {
        // ……
    }}
```

> [standard:indent](https://pinterest.github.io/ktlint/latest/rules/standard/#indentation)

## 空格

### 【强制】除了缩进和 KDoc 中允许使用的空格外，代码中不允许出现多个连续空格。

正例

```java
fun main() {
    x(1, 3)
}
```

反例

```java
fun  main()  {
    x(1,  3)
}
```

> [standard:no-multi-spaces](https://pinterest.github.io/ktlint/latest/rules/standard/#no-multi-spaces)

### 【推荐】在二元操作符左右留空格: a + b, 例外：不要在“range to”操作符（0..i）左右留空格。

正例

```java
val foo1 = (1..12 step 2).last
val foo2 = (1..12 step 2).last
val foo3 = (1..12 step 2).last
```

反例

```java
val foo1 = (1.. 12 step 2).last
val foo2 = (1 .. 12 step 2).last
val foo3 = (1 ..12 step 2).last
```

> [standard:op-spacing](https://pinterest.github.io/ktlint/latest/rules/standard/#operator-spacing)[standard:range-spacing](https://pinterest.github.io/ktlint/latest/rules/standard/#range-spacing)

### 【强制】在使用泛型类型（<>）时，角括号内不允许有空格 。

正例

```java
val a: Map<Int, String> = mapOf()
val b: Map<Int, String> = mapOf()
val c: Map<Int, String> = mapOf()
```

反例

```java
val a: Map< Int, String> = mapOf()
val b: Map<Int, String > = mapOf()
val c: Map <Int, String> = mapOf()
```

> [standard:spacing-around-angle-brackets](https://pinterest.github.io/ktlint/latest/rules/standard/#angle-bracket-spacing)

### 【推荐】不要在一元运算符左/右留空格a++。

正例

```java
fun foo1(i: Int) = i++

fun foo2(i: Int) = ++i

fun foo3(i: Int) = ++i
```

反例

```java
fun foo1(i: Int) = i ++

fun foo2(i: Int) = ++ i

fun foo3(i: Int) = ++
    i
```

> [standard:unary-op-spacing](https://pinterest.github.io/ktlint/latest/rules/standard/#unary-operator-spacing)

### 【推荐】在控制流关键字（if、when、for 以及 while）与相应的左括号之间留空格。

### 【推荐】在修饰符列表和函数类型之间保留一个空格。

正例

```java
val foo: suspend () -> Unit = {}

suspend fun bar(baz: suspend () -> Unit) = baz()
```

反例

```java
val foo: suspend() -> Unit = {}

suspend fun bar(baz: suspend   () -> Unit) = baz()
```

> [standard:function-type-modifier-spacing](https://pinterest.github.io/ktlint/latest/rules/standard/#function-type-modifier-spacing)

### 【推荐】不要在主构造函数声明、方法声明或者方法调用的左括号之前留空格。

```java
class A(val x: Int)

fun foo(x: Int) { …… }

fun bar() {
    foo(1)
}
```

* 不在 ( 和 [ 之后, 或者]和 ) 之前留空格
* 不在. 或者 ?. 左右留空格：foo.bar().filter { it > 2 }.joinToString(), foo?.bar()
* 在 // 之后留一个空格：// 这是一条注释
* 不要在用于泛型参数的尖括号前后留空格：class Map<K, V> { …… }
* 不要在 :: 前后留空格：Foo::class、 String::length
* 不要在用于标记可空类型的** ? **前留空格：String?

  > [standard:nullable-type-spacing](https://pinterest.github.io/ktlint/latest/rules/standard/#nullable-type-spacing)

作为一般规则，避免任何类型的水平对齐。将标识符重命名为不同长度的名称不应该影响声明或者任何用法的格式。

## 冒号/分号/括号

### 【推荐】在以下场景中的 : 之前留一个空格：

当它用于分隔类型与超类型时

当委托给一个超类的构造函数或者同一类的另一个构造函数时

在 object 关键字之后

正例

```java
abstract class Foo<out T : Any> : IFoo {
    abstract fun foo(a: Int): T
}

class FooImpl : Foo() {
    constructor(x: String) : this(x) { /*……*/ }

    val x = object : IFoo { /*……*/ } 
}
```

反例

### 【推荐】当分隔声明与其类型时，不要在 : 之前留空格, 在 : 之后总要留一个空格。

正例

```java
abstract class Foo<out T : Any> : IFoo {
    abstract fun foo(a: Int): T
}

class FooImpl : Foo() {
    constructor(x: String) : this(x) { /*……*/ }

    val x = object : IFoo { /*……*/ } 
}
```

反例

### 【推荐】避免在Lambda表达式之前使用多余的括号

正例

```java
val foo = "some-string".count { it == '-' }
```

反例

```java
val foo = "some-string".count() { it == '-' }
```

> [standard:unnecessary-parentheses-before-trailing-lambda](https://pinterest.github.io/ktlint/latest/rules/standard/#unnecessary-parenthesis-before-trailing-lambda)

## 修饰符

### 【强制】强制要求修饰符按照一致的顺序排列

正例

```java
abstract class A {
    protected open val v = ""

    internal open suspend fun f(v: Any): Any = ""

    protected lateinit var lv: String
}
```

反例

```java
abstract class A {
    open protected val v = ""

    open suspend internal fun f(v: Any): Any = ""

    lateinit protected var lv: String
}
```

> [standard:modifier-orde](https://pinterest.github.io/ktlint/latest/rules/standard/#modifier-order)

## 空行

### 【推荐】不要在列表的以下位置使用空行：第一个元素之前；元素之间；最后一个元素之后。

正例

```java
class FooBar :
    Foo,
    Bar {
    // body
}

val foobar: FooBar<
    Foo,
    Bar,
    > = FooBar(Foo(), Bar())

class BiAdapter<C : RecyclerView.ViewHolder, V1 : C, V2 : C, out A1, out A2>(
    val adapter1: A1,
    val adapter2: A2,
) : RecyclerView.Adapter<C>()
    where A1 : RecyclerView.Adapter<V1>, A1 : ComposableAdapter.ViewTypeProvider,
          A2 : RecyclerView.Adapter<V2>, A2 : ComposableAdapter.ViewTypeProvider {
    // body
}
```

反例

```java
class FooBar :

    Foo,

    Bar

{
    // body
}

val foobar: FooBar<

    Foo,

    Bar,

    > = FooBar(Foo(), Bar())

class BiAdapter<C : RecyclerView.ViewHolder, V1 : C, V2 : C, out A1, out A2>(
    val adapter1: A1,
    val adapter2: A2
) : RecyclerView.Adapter<C>()
    where
          A1 : RecyclerView.Adapter<V1>, A1 : ComposableAdapter.ViewTypeProvider,

          A2 : RecyclerView.Adapter<V2>, A2 : ComposableAdapter.ViewTypeProvider
{
    // body
}
```

> [standard:no-blank-line-in-list](https://pinterest.github.io/ktlint/latest/rules/standard/#no-blank-lines-in-list)

### 【推荐】方法块头部不应出现空行

正例

```java
fun bar() {
   val a = 2
}
```

反例

```java
fun bar() {

   val a = 2
}
```

> [standard:no-empty-first-line-in-method-block](https://pinterest.github.io/ktlint/latest/rules/standard/#no-leading-empty-lines-in-method-blocks)

### 【推荐】在任何类或函数声明之前都需要一个空行。类签名和类中的第一个声明之间不需要空白行。以类似的方式，在任何顶级或类属性列表之前都需要一个空行。在本地属性之前或连续属性之间不需要空白行。

正例

```java
const val FOO_1 = "foo1"

class FooBar {
    val foo2 = "foo2"
    val foo3 = "foo3"

    fun bar1() {
        val foo4 = "foo4"
        val foo5 = "foo5"
    }

    fun bar2() = "bar"

    val foo6 = "foo3"
    val foo7 = "foo4"

    enum class Foo
}
```

反例

```java
const val FOO_1 = "foo1"

class FooBar {
    val foo2 = "foo2"
    val foo3 = "foo3"
    fun bar1() {
        val foo4 = "foo4"
        val foo5 = "foo5"
    }
    fun bar2() = "bar"
    val foo6 = "foo3"
    val foo7 = "foo4"
    enum class Foo
}
```

> [standard:blank-line-before-declaration](https://pinterest.github.io/ktlint/latest/rules/standard/#blank-line-before-declarations)

### 【推荐】在 } 之前不要有空行

正例

```java
fun main() {
    fun a() {
    }

    fun b()
}
```

反例

```java
fun main() {
    fun a() {

    }
    fun b()

}
```

> [standard:no-blank-line-before-rbrace](https://pinterest.github.io/ktlint/latest/rules/standard/#no-blank-lines-before)

### 【推荐】在链式调用中不要有空行

正例

```java
fun foo(inputText: String) {
    inputText
        .lowercase(Locale.getDefault())
}
```

反例

```java
fun foo(inputText: String) {
    inputText

        .lowercase(Locale.getDefault())
}
```

> [standard:no-blank-lines-in-chained-method-calls](https://pinterest.github.io/ktlint/latest/rules/standard/#no-blank-lines-in-chained-method-calls)

### 【强制】代码中禁止出现连续空行

正例

```java
package com.test

import com.test.util

val a = "a"

fun b() {
}

fun c()
```

反例

```java
package com.test


import com.test.util


val a = "a"


fun b() {
}


fun c()
```

> [standard:no-consecutive-blank-lines](https://pinterest.github.io/ktlint/latest/rules/standard/#no-blank-lines-in-chained-method-calls)

### 【强制】在申明和注解之间保留一个空行； 在带有注释的声明之间保留一个空行；在多个注解之间保留一个空行。

正例

```java
fun a()

@Bar
fun b()
```

反例

```java
fun a()
@Bar
fun b()
```

正例

```java
// some comment 1
bar()

/*
 * some comment 2
 */
foo()
```

反例

```java
// some comment 1
bar()
/*
 * some comment 2
 */
foo()
```

正例

```java
@JvmField
fun foo() {}

/**
 * block comment
 */
@Foo @Bar
class FooBar {
}
```

反例

```java
@JvmField

fun foo() {}

@Foo @Bar
/**
 * block comment
 */
class FooBar {
}
```

> [standard:annotation-spacing](https://pinterest.github.io/ktlint/latest/rules/standard/#annotation-spacing)[standard:spacing-between-declarations-with-comments](https://pinterest.github.io/ktlint/latest/rules/standard/#blank-line-between-declaration-with-comments)

## 类布局

### 【推荐】按照以下顺序定义类成员：

属性

初始化块

次构造函数

方法

伴生对象

正例

```java
class User(
    val name: String,
    val age: Int
) {
    var email: String = ""

    init {
        // 初始化逻辑
    }

    constructor(name: String) : this(name, 0)

    fun sendEmail() {
        // ...
    }

    companion object {
        const val DEFAULT_NAME = "Guest"
    }
}
```

反例

```java
class User(
    val name: String,
    val age: Int
) {
  
    fun sendEmail() {
        // ...
    }

    companion object {
        const val DEFAULT_NAME = "Guest"
    }

    var email: String = ""

    init {
        // 初始化逻辑
    }

    constructor(name: String) : this(name, 0)
}
```

### 【强制】当类或函数的签名无法放在一行时，每个参数必须单独占一行。

正例

```java
// 如果 ktlint_class_signature_rule_force_multiline_when_parameter_count_greater_or_equal_than 的值为 unset，
// 那么只要参数能够放在单行中，它们就不会被换行
class ClassA(paramA: String, paramB: String, paramC: String)

class ClassA(
    paramA: String,
    paramB: String,
    paramC: String
)

// 如果 ktlint_class_signature_rule_force_multiline_when_parameter_count_greater_or_equal_than 的值为 unset，
// 那么只要参数能够放在单行中，它们就不会被换行
fun f(a: Any, b: Any, c: Any)

fun f(
    a: Any,
    b: Any,
    c: Any
)

fun foo(
    @Bar fooBar: FooBar
)
```

反例

```java
class ClassA(
    paramA: String, paramB: String,
    paramC: String
)

fun f(
    a: Any,
    b: Any, c: Any
)

fun foo(@Bar fooBar: FooBar)
```

> [standard:parameter-list-wrapping](https://pinterest.github.io/ktlint/latest/rules/standard/#parameter-list-wrapping)

### 【强制】函数、类/对象体或其他块体中的语句必须与块体的大括号分开，放在不同的行上。

正例

```java
fun foo() {
    if (true) {
        // do something
    }
}

class A {
    val a = 0
    val b = 1
}

enum class FooBar1 { FOO, BAR }

enum class FooBar2 {
    FOO,
    BAR,
}
```

反例

```java
fun foo() { if (true) {
        // do something
    }
}

class A { val a = 0
    val b = 1 }
```

> [standard:statement-wrapping](https://pinterest.github.io/ktlint/latest/rules/standard/#statement-wrapping)

## 类定义

### 【推荐】具有少数主构造函数参数的类可以写成一行：

正例

```java
class Person(id: Int, name: String)
```

反例

```java
class Person(id: Int,
    name: String)
```

> [standard:class-signature](https://pinterest.github.io/ktlint/latest/rules/standard/#class-signature)

### 【推荐】具有较长类头的类应该格式化，以使每个主构造函数参数都在带有缩进的独立的行中。 另外，右括号应该位于一个新行上。如果使用了继承，那么超类的构造函数调用或者所实现接口的列表应该与右括号位于同一行。

正例

```java
class Person(
    id: Int,
    name: String,
    surname: String
) : Human(id, name) { /*……*/ }
```

对于多个接口，应该将超类构造函数调用放在首位，然后将每个接口应放在不同的行中：

```java
class Person(
    id: Int,
    name: String,
    surname: String
) : Human(id, name),
    KotlinMaker { /*……*/ }
```

对于具有很长超类型列表的类，在冒号后面换行，并横向对齐所有超类型名：

```java
class MyFavouriteVeryLongClassHolder :
    MyLongHolder<MyFavouriteVeryLongClass>(),
    SomeOtherInterface,
    AndAnotherOne {

    fun foo() { /*……*/ }
}
```

为了将类头与类体分隔清楚，当类头很长时，可以在类头后放一空行 （如上例所示）或者将左花括号放在独立行上：

```java
class MyFavouriteVeryLongClassHolder :
    MyLongHolder<MyFavouriteVeryLongClass>(),
    SomeOtherInterface,
    AndAnotherOne 
{
    fun foo() { /*……*/ }
}
```

### 【推荐】构造函数参数使用常规缩进（4 个空格）。

这确保了在主构造函数中声明的属性与 在类体中声明的属性具有相同的缩进。

### 【推荐】代码中不应出现空的类体 {}。

正例

```java
class C

data class DC(val v: Any)

interface I

object O
```

反例

```java
class C {}

data class DC(val v: Any) { }

interface I {
}

object O{}
```

> [standard:no-empty-class-body](https://pinterest.github.io/ktlint/latest/rules/standard/#no-empty-class-bodies)

## 数据类

### 【强制】使用 data class 表示纯数据结构, 避免在数据类中添加业务逻辑。

正例

```java
data class User(
    val id: Int,
    val name: String,
    val email: String
)
```

反例

```java
data class User(
    val id: Int
){
    fun testUser(){
    }
}
```

## 单例对象

### 【推荐】使用 object 关键字来定义单例对象。

正例

```java
object MySingleton {
    fun myMethod() {
        // 方法内容
    }
}
```

反例

```java
class Singleton private constructor() {
    companion object {
        val INSTANCE: Singleton = Singleton()
    }

    fun doSomething() {
        println("Doing something...")
    }
}
```

## 函数参数及返回值

### 【推荐】如果函数参数较多不适合单行，请使用以下语法

正例

```java
fun longMethodName(
    argument: ArgumentType = defaultValue,
    argument2: AnotherArgumentType,
): ReturnType {
    // 函数体
}
```

反例

```java
fun longMethodName(argument: ArgumentType = defaultValue, argument2: AnotherArgumentType): ReturnType {
    // 函数体
}
```

### 【推荐】函数参数使用常规缩进（4个空格）。有助于确保与构造函数参数一致

### 【推荐】不要使用 Unit 作为函数返回类型

正例

```java
fun fn() {}
```

反例

```java
fun fn(): Unit {}
```

> [standard:no-unit-return](https://pinterest.github.io/ktlint/latest/rules/standard/#no-unit-as-return-type)

### 【推荐】将函数的上下文接收器列表换到单独的一行，无论最大行长度如何。如果配置了最大行长度并且超出限制，则应将上下文接收器及其投影类型分别换到单独的行。

正例

```java
// 始终换行上下文接收器列表，无论是否设置了最大行长度
context(Foo)
fun fooBar()

// 当整个上下文接收器列表无法放在同一行时,
// 将每个上下文接收器换到单独的一行
context(
    Fooooooooooooooooooo1,
    Foooooooooooooooooooooooooooooo2
)
fun fooBar()

// 当整个上下文接收器列表无法放在同一行时，将每个上下文接收器换到单独的一行。
// 此外，如果某个上下文接收器在换行后仍然无法适应单行，则应将其投影类型也分别换到单独的行.
context(
    Foooooooooooooooo<
        Foo,
        Bar,
        >
)
fun fooBar()
```

反例

```java
// 始终换行上下文接收器列表，无论是否设置了最大行长度。
context(Foo) fun fooBar()

// 如果整个上下文接收器列表无法放在单行内，则应进行换行。
context(Fooooooooooooooooooo1, Foooooooooooooooooooooooooooooo2)
fun fooBar()

// 当整个上下文接收器列表无法适应单行时，应该换行。
// 换行后，如果某个上下文接收器过长，仍然无法适应单行，则还需要将其投影类型分别换行
context(Foooooooooooooooo<Foo, Bar>)
fun fooBar()
```

> [standard:context-receiver-wrapping](https://pinterest.github.io/ktlint/latest/rules/standard/#context-receiver-wrapping)

## 默认参数

### 【推荐】使用默认参数减少重载函数。

正例

```java
fun greet(name: String = "Guest") {
    println("Hello, $name!")
}
```

反例

```java
fun greet(name: String){
    println("Hello, $name!")
}
```

## 变量

### 【推荐】优先使用 val 声明不可变变量, 仅在必要时使用 var

正例

```java
fun greet() {
    val a = 1 //不可变变量
    println("Hello, $a!")
}
```

反例

```java
fun greet(){
    var a = 1 //可变变量
    println("Hello, $a!")
}
```

### 【推荐】避免空指针, 可显式声明可空类型（如** **String?），配合安全调用符（?.）和 Elvis 操作符（?:）处理空值

正例

```java
fun printLength(s: String?) {
    val length = s?.length ?: 0
    println("Length of '$s' is $length.")
}
```

反例

```java
fun printLength(s: String) {
    val length = s.length
    println("Length of '$s' is $length.")
}
```

## 字符串模板

### 【强制】字符串模板中应保持一致的格式：使用 $v 而不是 ${v}，使用 ${p.v} 而不是 ${p.v.toString()}。

正例

```java
val foo = "$foo hello"
```

反例

```java
val foo = "${foo} hello"
```

> [standard:string-template](https://pinterest.github.io/ktlint/latest/rules/standard/#string-template)

### 【强制】强制多行字符串模板在使用 .trimIndent() 后保持一致的缩进格式。开头和结尾的 """ 应分别放在独立的行上，模板内容的缩进应与 """ 对齐。

正例

```java
val foo =
    """
    line1
    line2
    """.trimIndent()

fun foo() {
    // The opening """ can not be wrapped to next line as that would result in a compilation error
    return """
        line1
        line2
        """.trimIndent()
}
```

反例

```java
val foo = """
          line1
          line2
          """.trimIndent()

fun foo() {
    return """
        line1
        line2
    """.trimIndent()
}
```

> [standard:string-template-indent](https://pinterest.github.io/ktlint/latest/rules/standard/#string-template-indent)

## 表达式函数体格式化

### 【推荐】如果函数的表达式函数体与函数声明不适合放在同一行，那么将 = 留在第一， 并将表达式函数体缩进 4 个空格。

正例

```java
fun f(x: String, y: String, z: String) =
    veryLongFunctionCallWithManyWords(andLongParametersToo(), x, y, z)
```

> [standard:function-expression-body](https://pinterest.github.io/ktlint/latest/rules/standard/#function-expression-body)

### 【推荐】对于由单个表达式构成的函数体，优先使用表达式形式。

正例

```java
fun foo() = 1
```

反例

```java
fun foo(): Int {
    return 1
}
```

> [standard:function-expression-body](https://pinterest.github.io/ktlint/latest/rules/standard/#function-expression-body)

### 【推荐】多行表达式在赋值语句的右侧时，必须从新的一行开始。

> 对于 `return` 语句中的表达式则不受此限制，因为那样会导致编译错误。

正例

```java
val foo =
    foo(
        parameterName =
            "The quick brown fox "
                .plus("jumps ")
                .plus("over the lazy dog"),
    )
```

反例

```java
val foo = foo(
    parameterName = "The quick brown fox "
        .plus("jumps ")
        .plus("over the lazy dog"),
)
```

> [standard:multiline-expression-wrapping](https://pinterest.github.io/ktlint/latest/rules/standard/#multiline-expression-wrapping)

## 属性格式化

### 【推荐】对于非常简单的只读属性，请考虑单行格式：

正例

```java
val isEmpty: Boolean get() = size == 0
```

反例

```java
val isEmpty: Boolean get(){
    return size == 0
}
```

### 【推荐】对于更复杂的属性，总是将 get  与 set 关键字放在不同的行上：

正例

```java
val foo: String
    get() { /*……*/ }
```

### 【推荐】对于具有初始化的属性，如果初始化很长，那么在 = 号后增加一个换行并将初始化器缩进四个空格：

正例

```java
private val defaultCharset: Charset? =
    EncodingRegistry.getInstance().getDefaultCharsetForPropertiesFiles(file)
```

反例

```java
private val defaultCharset: Charset? = EncodingRegistry.getInstance().getDefaultCharsetForPropertiesFiles(file)
```

## 注解

### 【强制】带参数的注解不允许与被注解的结构体写在同一行，通常将注解放在单独的行上，在它们所依附的声明之前，并使用相同的缩进。

正例

```java
@Target(AnnotationTarget.PROPERTY)
annotation class JsonExclude
```

反例

```java
@Target(AnnotationTarget.PROPERTY) annotation class JsonExclude
```

> [standard:annotation](https://pinterest.github.io/ktlint/latest/rules/standard/#annotation-formatting)

### 【推荐】无参数的多个注解可以放在同一行， 但不要与结构体或者申明放在同一行。

正例

```java
@JsonExclude @JvmField
var x: String
```

反例

```java
@JsonExclude
@JvmField
var x: String
```

[standard:annotation](https://pinterest.github.io/ktlint/latest/rules/standard/#annotation-formatting)

### 【推荐】无参数的单个注解可以与相应的声明放在同一行。

正例

```java
@Test fun foo() { /*……*/ }
```

反例

```java

```

> [standard:annotation](https://pinterest.github.io/ktlint/latest/rules/standard/#annotation-formatting)

### 【推荐】类或函数的参数可以在同一行上带有一个带参数的注解

正例

```java
class Foo(
    @Path("fooId") val fooId: String,
    @NotNull("bar") bar: String,
)
```

反例：

```java

```

> [standard:annotation](https://pinterest.github.io/ktlint/latest/rules/standard/#annotation-formatting)

### 【推荐】一个由无参数注解组成的数组可以与被注解的结构写在同一行。

正例

```java
@[Foo Bar] class FooBar2 {
    @[Foo Bar] var foo: String

    @[Foo Bar] fun bar() {}
}
```

> [standard:annotation](https://pinterest.github.io/ktlint/latest/rules/standard/#annotation-formatting)

## 方法调用格式化

### 【推荐】在较长参数列表的左括号后添加一个换行符。按 4 个空格缩进参数。 将密切相关的多个参数分在同一行。

正例

```java
drawSquare(
    x = 10, y = 10,
    width = 100, height = 100,
    fill = true
)
```

在分隔参数名与值的 = 左右留空格。

反例

```java

```

## 链式调用

### 【推荐】当对链式调用换行时，将 . 字符或者 ?. 操作符放在下一行，并带有单倍缩进：

正例

```java
val anchor = owner
    ?.firstChild!!
    .siblings(forward = true)
    .dropWhile { it is PsiComment || it is PsiWhiteSpace }
```

调用链的第一个调用通常在换行之前，当然如果能让代码更有意义也可以忽略这点。

反例

```java
val anchor = owner?.firstChild!!.
    siblings(forward = true).
    dropWhile { it is PsiComment || it is PsiWhiteSpace }
```

> [standard:chain-method-continuation](https://pinterest.github.io/ktlint/latest/rules/standard/#chain-method-continuation)

正例

```
val foo =
    listOf(1, 2, 3)
        .filter { it > 2 }!!
        .takeIf { it.count() > 100 }
        ?.sum()
val foobar =
    foo()
        ?: bar
```

反例

> [standard:chain-wrapping](https://pinterest.github.io/ktlint/latest/rules/standard/#chain-wrapping)

## 条件语句

### 【推荐】优先使用 if 与 when 的表达形式。

正例

```java
return when(x) {
    0 -> "zero"
    else -> "nonzero"
}
```

反例

```java
if (x)
    return foo()
else
    return bar()
```

### 【推荐】如果 if 语句的条件有多行，那么在语句体外边总是使用大括号。

将该条件的每个后续行相对于条件语句起始处缩进 4 个空格。 将该条件的右圆括号与左花括号放在单独一行：

正例

```java
if (!component.isSyncing &&
    !hasAnyKotlinRuntimeInScope(module)
) {
    return createKotlinNotConfiguredPanel(module)
} else {
    // else 部分
}
```

反例

```java
if (!component.isSyncing &&
    !hasAnyKotlinRuntimeInScope(module)) 
    return createKotlinNotConfiguredPanel(module)
```

> [standard:binary-expression-wrapping](https://pinterest.github.io/ktlint/latest/rules/standard/#binary-expression-wrapping)

### 【推荐】如果 if-else 语句或 if-else-if 语句的至少一个分支使用了大括号 {} 包裹，则所有分支都应使用大括号 {} 包裹。

正例

```java
fun foo(value: Int) {
    if (value > 0) {
        doSomething()
    } else if (value < 0) {
        doSomethingElse()
    } else {
        doSomethingElse2()
    }
}
```

反例

```java
fun foo(value: Int) {
    if (value > 0)
        doSomething()
    else if (value < 0) {
        doSomethingElse()
    } else
        doSomethingElse2()
}
```

> [standard:if-else-bracing](https://pinterest.github.io/ktlint/latest/rules/standard/#if-else-bracing)
> [standard:multiline-if-else](https://pinterest.github.io/ktlint/latest/rules/standard/#multiline-if-else)

### 【推荐】禁止在 else 关键字之后换行，以避免可能导致的混淆。

正例

```java
fun funA() {
    if (conditionA()) {
        doSomething()
    } else if (conditionB()) {
        doAnotherThing()
    }
}
```

反例

```java
fun funA() {
    if (conditionA()) {
        doSomething()
    } else
    if (conditionB()) {
        doAnotherThing()
    }
}
```

> [standard:no-line-break-after-else](https://pinterest.github.io/ktlint/latest/rules/standard/#no-line-break-after-else)

### 【推荐】在多行条件中，将每个操作数换到单独的一行。

正例

```java
val foo = bar || baz
if (bar1 ||
    bar2 ||
    baz1 ||
    (baz2 && baz3)
) {
   // do something
}
```

反例

```java
val foo =
  multiLineOperand(
      "bar"
  ) || baz
if (bar1 || bar2 ||
    baz1 || (baz2 && baz3)
) {
   // do something
}
```

> [standard:condition-wrapping](https://pinterest.github.io/ktlint/latest/rules/standard/#condition-wrapping)

### 【推荐】单行的 if 语句应该保持简单。它最多只能包含一个 else 分支，并且分支中不能使用大括号包裹代码块。

正例

```java
fun foobar() {
    if (true) foo()
    if (true) foo() else bar()
}
```

反例

```java
fun foobar() {
    if (true) if (false) foo() else bar()
    if (true) bar() else if (false) foo() else bar()
    if (true) { foo() } else bar()
    if (true) bar() else { if (false) foo() else bar() }
}
```

> [standard:if-else-wrapping](https://pinterest.github.io/ktlint/latest/rules/standard/#if-else-wrapping)

## 循环

### 【推荐】对于多行的 for、while 和 do 循环，应使用大括号 {}。

正例

```java
for (i in 1..10) {
    println(i)
}
```

反例

```java
for (i in 1..10)
    println(i)
```

> [standard:multiline-loop](https://pinterest.github.io/ktlint/latest/rules/standard/#multiline-loop)

## when表达式

### 【推荐】在 when 语句中，如果一个分支不止一行，可以考虑用空行将其与相邻的分支块分开：

正例

```java
private fun parsePropertyValue(propName: String, token: Token) {
    when (token) {
        is Token.ValueToken ->
            callback.visitValue(propName, token.value)

        Token.LBRACE -> { // ……
        }
    }
}
```

反例

```java
private fun parsePropertyValue(propName: String, token: Token) {
    when (token) {
        is Token.ValueToken ->
            callback.visitValue(propName, token.value)
        Token.LBRACE -> { // ……
        }
    }
}
```

### 【推荐】将短分支放在与条件相同的行上，无需花括号。

正例

```java
when (foo) {
    true -> bar()
    false -> baz()
}
```

反例

```java
when (foo) {
    true -> bar()
    false -> { baz() } 
}
```

## Try catch finanlly语句

### 【推荐】在 try { .. } catch { .. } finally { .. } 中应保持一致的间距。

正例

```java
fun foo() =
    try {
        // do something
    } catch (exception: Exception) {
        // handle exception
    } finally {
        // clean up
    }
```

反例

```java
fun foo1() = try { /* ... */ } catch (exception: Exception) { /* ... */ } finally { /* ... */ }
fun foo2() = 
    try {
        // do something
    }
    catch (exception: Exception) {
        // handle exception
    }
    finally {
        // clean up
    }
```

> [standard:try-catch-finally-spacing](https://pinterest.github.io/ktlint/latest/rules/standard/#try-catch-finally-spacing)

## 可空类型

### 【强制】明确声明变量是否可空，避免 NullPointerException

正例

```java
var myVariable: String? = null
```

反例

```java
var myVariable: String
```

## 安全调用操作符

### 【强制】使用 ?. 来安全地调用方法或访问属性

正例

```java
myVariable?.length
```

反例

```java
myVariable.length
```

## 导入

### 【强制】禁止导入从未使用的包。

> [standard:no-unused-imports](https://pinterest.github.io/ktlint/latest/rules/standard/#no-unused-imports)【

### 【推荐】不要使用通配符导入（*），除非是明确允许的白名单导入。

正例

```java
import foobar.Bar
import foobar.Foo
```

反例

```java
import foobar.*
```

> [standard:no-wildcard-imports](https://pinterest.github.io/ktlint/latest/rules/standard/#no-wildcard-imports)

## 注释

### 【推荐】单行注释：使用 // 进行单行注释

正例

```java
// 计算总和
val total = sum + tax
```

反例

```java
/** 计算总和 */
val total = sum + tax
```

### 【推荐】多行注释：对于较长的文档注释，将开头 /** 放在一个独立行中，并且后续每行都以星号开头：

正例

```java
/**
 * 这是一条多行
 * 文档注释。
 */
```

反例

```java
/**
  这是一条多行
  文档注释。
 */
```

### 【推荐】使用 /** ... */ 进行文档注释，用于为类、函数、属性等生成文档，遵循 KDoc 规范。

正例

```java
/**
 * 表示一个用户对象
 * @property name 用户的姓名
 * @property age 用户的年龄
 */
class User(val name: String, val age: Int)
```

反例

```java
/**
 * 表示一个用户对象
 * name 用户的姓名
 * age 用户的年龄
 */
class User(val name: String, val age: Int)
```

> [standard:kdoc-wrapping](https://pinterest.github.io/ktlint/latest/rules/standard/#kdoc-wrapping)

### 【推荐】块注释：在块注释中，每一行的（不包括缩进部分）应该与块注释开头的对齐。块注释的开始和结束应位于不包含任何其他元素的独立行上。

正例

```java
/*
 * This comment is formatted well.
 */
```

反例

```java
/*
      * This comment is not formatted well.
    */
```

> [standard:block-comment-initial-star-alignment](https://pinterest.github.io/ktlint/latest/rules/standard/#block-comment-initial-star-alignment)

正例

```java
// Some comment 1
val foo1 = "foo1"
val foo2 = "foo" // Some comment
val foo3 = { /* no-op */ }
```

反例

```java
/* Some comment 1 */ val foo1 = "foo1"
val foo2 = "foo" /* Block comment instead of end-of-line comment */
val foo3 = "foo" /* Some comment
                  * with a newline
                  */
```

> [standard:comment-wrapping](https://pinterest.github.io/ktlint/latest/rules/standard/#comment-wrapping)

### 【推荐】不推荐使用连续KDoc注释

在以下情况下禁止连续注释：

1. 任意组合的连续 KDoc、块注释或行尾注释（EOL 注释），除非它们之间有一个空行分隔。
2. 连续的 KDoc（即使它们之间有空行分隔）。
3. 连续的块注释（即使它们之间有空行分隔）。

正例

```java
// An EOL comment
// may be followed by another EOL comment
val foo = "foo"

// Different comment types (including KDoc) may be consecutive ..

/*
 * ... but do need to be separated by a blank line ...
 */

/**
  * ... but a KDoc can not be followed by an EOL or a block comment or another KDoc
  */
fun bar() = "bar"
```

反例

```java
/*
 * Block comments can not be consecutive ...
 */
/*
 * ... even not when separated by a new line.
 */
val bar = "bar" 

/**
  * A KDoc can not be followed by a block comment or an EOL comment or another KDOC
  */

// ... even not when separated by a new line.
```

> [standard:no-consecutive-comments](https://pinterest.github.io/ktlint/latest/rules/standard/#no-consecutive-comments)

### 【推荐】禁止在类型参数内部的某些位置添加注释。

正例

```java
fun Foo<
    /* some comment */ 
    out Any
    >.foo() {}
fun Foo<
    // some comment 
    out Any
    >.foo() {}
```

反例

```java
fun Foo<out /* some comment */ Any>.foo() {}
fun Foo<
    out Any, // some comment
    >.foo() {}
```

> [standard:type-argument-comment](https://pinterest.github.io/ktlint/latest/rules/standard/#type-argument-comment)

# Kotlin Lint代码检测

## ‌基础检测方法

### ‌通过 IDE 直接运行 Lint

* 在 Android Studio 菜单栏选择 ‌**Analyze > Inspect Code**‌，选择检测范围（如整个项目或当前文件）即可启动扫描‌**1**2。
* 结果会在 ‌**Inspection Results**‌ 窗口中分类显示（如警告、错误、建议优化项），支持直接跳转到问题代码位置‌**1**6。

### 通过命令行运行 Lint

在终端执行** `./gradlew lint` 命令，对整个项目执行 Lint 检测‌。

检测完成后，报告会生成在** **`app/build/reports/lint/` 目录下，支持 HTML 和 XML 格式‌。

## 配置 Lint 规则

### Gradle 配置

在 `build.gradle` 中调整 Lint 行为：

```
android {
    lintOptions {
        abortOnError = true    // 发现错误时终止构建
        warningsAsErrors = true // 将警告视为错误
        ignoreWarnings = false  // 不忽略警告
    }
}
```

支持过滤特定规则或文件（如 `disable 'UnusedResources'`）

### 自定义检测范围

创建 `lint.xml` 文件定义规则优先级和排除路径，例如：

```
<lint>
    <issue id="UnusedResources" severity="ignore" />
    <issue id="HardcodedText" severity="error" />
</lint>
```

可配置路径、规则级别及例外文件

### 注册辅助检查

使用 `androidx.annotation` 库添加注解（如 `@NonNull`、`@StringRes`），帮助 Lint 识别潜在类型错误或空指针问题

## 检测结果处理

‌**查看和修复问题**‌

* 在 ‌**Inspection Results**‌ 窗口中双击问题项可直接跳转到代码位置，IDE 提供快速修复建议（如自动删除未使用变量）‌。
* 对于误报或无需处理的警告，使用 `@SuppressLint("警告类型")` 注解临时忽略‌。

‌**生成详细报告**‌

Lint 生成的 HTML 报告会按模块和问题类型分类，包含问题描述、位置及修复建议，便于团队协作分析‌。

## 高级选项

1. ‌**自定义 Lint 规则**‌
   * 继承 `Detector` 类编写自定义规则，通过 `IssueRegistry` 注册后集成到构建流程，适用于特定项目规范（如禁止直接使用 `!!` 非空断言符）‌。
   * 示例场景：强制要求 `LiveData` 通过后备属性暴露‌。
2. ‌**集成第三方工具**‌
   * ‌**ktlint**‌：专注于 Kotlin 代码风格检查（如缩进、分号），可通过 Gradle 插件 `org.jlleitschuh.gradle.ktlint` 集成‌。
   * ‌**Detekt**‌：支持复杂代码异味检测（如过长函数、嵌套过深），配置文件 `detekt.yml` 可自定义规则阈值‌。

