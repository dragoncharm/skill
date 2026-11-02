![image](uploads/4077/3d5f64ac-b714-4994-9789-19696e139d56/java.png)

# 前言

编码规范对于程序员而言尤为重要，有以下几个原因：

- 一个软件的生命周期中，80%的花费在于维护。
- 几乎没有任何一个软件，在其整个生命周期中，均由最初的开发人员来维护。
- 编码规范可以改善软件的可读性，可以让程序员尽快而彻底地理解新的代码。
- 如果你将源码作为产品发布，就需要确任它是否被很好的打包并且清晰无误，一如你已构建的其它任何产品。

## 适用对象

浩鲸科技 JAVA 开发人员

## 目的

为了持续、稳定地开发出高质量，健壮的软件系统，为了保证团队中成员的编码质量，特制定本文档。用于规范团队内部开发过程，增加程序的健壮性，便于后续测试及代码维护，最终提高软件产品的生产力。

# 代码风格(Code Style)

## 文件组织(File Organization)

【强制】一个文件由被空行分割而成的段落以及标识每个段落的可选注释共同组成。超过1500行的程序难以阅读，应该尽量避免。

### Java 源文件(Java Source Files)

【强制】每个Java源文件都包含一个单一的公共类或接口。若私有类和接口与一个公共类相关联，可以将它们和公共类放入同一个源文件。公共类必须是这个文件中的第一个类或接口。

**【强制】IDE的text file encoding设置为UTF-8; IDE中文件的换行符使用Unix格式，不要使用Windows格式。**

### 开头注释(Beginning Comments)

【强制】所有的源文件都应该在开头有一个C语言风格的注释，其中列出类名、版本信息、日期和版权声明。

**正例**

```java
/*
* Classname
*
* Version information
*
* Date
*
* Copyright notice
*/
```

**检查方式**
工具检查

### 包和引入语句(Package and Import Statements)

【强制】在多数Java源文件中，第一个非注释行是包语句。在它之后可以跟引入语句。

**正例**

```java
package java.awt;
import java.awt.peer.CanvasPeer;
```

**检查方式**
工具检查

【强制】不允许 import \*

**<font color="red">反例</font>**

```java
import java.util.function.*;
```

**正例**

```java
import java.util.function.BiConsumer;
import java.util.function.BiFunction;
import java.util.function.Consumer;
import java.util.function.Function;
```

**检查方式**
工具检查

### 类和接口声明(Class and Interface Declarations)

【强制】下表描述了类和接口声明的各个部分以及它们出现的先后次序

|   | 类/接口声明的各部分                         | 注释                                                                                                                                     |
| --- | --------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------ |
| 1 | 类/接口文档注释(/\*\*……\*/)               | 该注释中所需包含的信息                                                                                                                   |
| 2 | 类或接口的声明                              |                                                                                                                                          |
| 3 | 类/接口实现的注释(/\*……\*/)如果有必要的话 | 该注释应包含任何有关整个类或接口的信息，而这些信息又不适合作为类/接口文档注释。                                                          |
| 4 | 类的(静态)变量                              | 首先是类的公共变量，随后是保护变量，再后是包一级别的变量(没有访问修饰符，access modifier)，最后是私有变量。                              |
| 5 | 实例变量                                    | 首先是公共级别的，随后是保护级别的，再后是包一级别的(没有访问修饰符)，最后是私有级别的。                                                 |
| 6 | 构造器                                      |                                                                                                                                          |
| 7 | 方法                                        | 这些方法应该按功能，而非作用域或访问权限，分组。例如，一个私有的类方法可以置于两个公有的实例方法之间。其目的是为了更便于阅读和理解代码。 |

## 排版缩进(Indentation)

### 缩进

**【强制】使用4个空格作为缩进排版的一个单位。如使用tab键，设置tab键的占位符为4，IDEA设置tab为4个空格时，请勿勾选Use tab character；而在eclipse中，必须勾选insert spaces for tabs。**

说明：如果使用tab缩进，必须设置1个tab为4个空格。
正例： （涉及1-5点）

```java
public static void main(String[] args) {
    // 缩进4个空格
    String say = "hello";
    // 运算符的左右必须有一个空格
    int flag = 0;
    // 关键词if与括号之间必须有一个空格，括号内的f与左括号，0与右括号不需要空格
    if (flag == 0) {
        System.out.println(say);
    }
    // 左大括号前加空格且不换行；左大括号后换行
    if (flag == 1) {
        System.out.println("world")
    } 
    else {
        System.out.println("ok");
    // 在右大括号后直接结束，则必须换行
    }
}
```

**检查方式**
工具检查

### 排版

**【强制】避免在一个语句中给多个变量赋值。**

**检查方式**
工具检查

**【强制】参数列表的逗号后面有空格。**

**检查方式**
工具检查

**【强制】除了”.”，任何二目、三目运算符的左右两边都需要加一个空格将之与操作数分开。**

说明：运算符包括赋值运算符`=`、逻辑运算符`&&`、加减乘除符号等。

**检查方式**
工具检查

**【强制】`if/for/while/switch/do`等保留字与括号之间都必须加空格。**

**【强制】for语句中的表达式应该被空格分开。**

**正例**

```java
for (int i = 0; i < requAcctDtoArr.length; i++) {
}
```

**检查方式**
工具检查

**【强制】强制转型后应该跟一个空格。**

**正例**

```java
(ServHistoryDto[]) al.toArray(new ServHistoryDto[0])
```

**检查方式**
工具检查

**【强制】每个类不应超过1500行。**

**检查方式**
工具检查

**【强制】每个方法不应超过200行。**

说明：除注释之外的方法签名、左右大括号、方法内代码、空行、回车及任何不可见字符的总行数不超过200行。

正例：代码逻辑分清红花和绿叶，个性和共性，绿叶逻辑单独出来成为额外方法，使主干代码更加清晰；共性逻辑抽取成为共性方法，便于复用和维护。

**检查方式**
工具检查

**【推荐】没有必要增加若干空格来使变量的赋值等号与上一行对应位置的等号对齐。**

正例：

```java
int one = 1;
long two = 2L;
float three = 3F;
StringBuilder sb = new StringBuilder();
```

说明：增加sb这个变量，如果需要对齐，则给one、two、three都要增加几个空格，在变量比较多的情况下，是非常累赘的事情。

### 行长度(Line Length)

**【强制】尽量避免一行的长度超过150个字符，超出需要换行，换行时遵循如下原则：**

1. 第二行相对第一行缩进4个空格，从第三行开始，不再继续缩进，参考示例。
2. 运算符与下文一起换行。
3. 方法调用的点符号与下文一起换行。
4. 方法调用中的多个参数需要换行时，在逗号后进行。
5. 在括号前不要换行，见反例。

正例：

```java
StringBuilder sb = new StringBuilder();
// 超过150个字符的情况下，换行缩进4个空格，点号和方法名称一起换行
sb.append("Jack").append("Ma")...
    .append("alibaba")...
    .append("alibaba")...
    .append("alibaba");
```

反例：

```java
StringBuilder sb = new StringBuilder();
// 超过150个字符的情况下，不要在括号前换行
sb.append("Jack").append("Ma")...append
("alibaba");

// 参数很多的方法调用可能超过150个字符，不要在逗号前换行
method(args1, args2, args3, ...
, argsX); 
```

**检查方式**
工具检查

### 换行(Wrapping Lines)

**【强制】每行只能有一个声明。**

**检查方式**
工具检查

**【强制】每行只包含一条语句。**

**检查方式**
工具检查

**【强制】两个方法之间使用空行。**

**检查方式**
工具检查

**【强制】当一个表达式无法容纳在一行内时，可以依据如下一般规则进行换行：**

- “{”放在行末，“}”新起一行。
- 在一个逗号后面断开
- 在一个操作符前面断开
- 宁可选择较高级别(higher-level)的断开，而非较低级别(lower-level)的断开
- 新的一行应该与上一行同一级别表达式的开头处对齐
- 如果以上规则导致你的代码混乱或者使你的代码都堆挤在右边，那就代之以缩进8个空格

**检查方式**
工具检查

**【推荐】不同逻辑、不同语义、不同业务的代码之间插入一个空行分隔开来以提升可读性。**
说明：任何情形，没有必要插入多个空行进行隔开。

## 注释(Comments)

程序可以有4种实现注释的风格：块(block)、单行(single-line)、尾端(trailing)和行末(end-of-line)。

### 我们这样注释(Comment Like This)

**【强制】注释不应写在用星号或其他字符画出来的大框里。注释不应包括诸如制表符和回退符之类的特殊字符。**

**检查方式**
工具检查

**【强制】每行只能有一个声明。**

**检查方式**
工具检查

**【强制】使用javadoc注释**

**说明**
对类，接口，公用和保护方法，公用和保护类变量使用javadoc注释，必须包括描述，参数，返回值，异常的说明。

**检查方式**
工具检查

**【强制】方法的内部采用单行注释，不要和代码在同一行，主要用来说明业务逻辑、代码段和临时变量的声明定义。**

**检查方式**
工具检查

**【强制】添加方法注释。**

**说明**
方法需要添加方法功能描述、输入参数说明、返回参数说明、抛出异常。

**正例**

```java
/**
* 根据通知类型、语言类型id获取语言模板
* @param adviceType 通知类型
* @param langId 语言类型id
* @return AdviceTypeLangDto
* @throws BaseAppException
*/
```

**检查方式**
工具检查

**【强制】代码变更注释。**
**说明**
代码受控后，代码变更需要将旧代码注释，并且说明变更原因、涉及任务单号、变更作者、变更时间。
对于代码删除，若是自己模块代码，确认不再需要可直接删除，若不是很明确或是删除他人模块代码，将旧代码注释掉，后面由本模块负责人定期清理被注释的旧代码。
**正例**

```java
代码新增
// add by [your name] at 2009-03-10 for task:URid

代码修改：
// modified by [your name] at 2009-03-10 for reason

代码删除：
// delete by [your name] at 2009-03-10 for reason
```

**检查方式**
工具检查

**【强制】类内部的成员变量必须有单行注释**

**检查方式**
工具检查

**【推荐】if，for，switch关键字后应该有注释，提高可读性**

**检查方式**
无

**【强制】注释的双斜线与注释内容之间有且仅有一个空格。**
正例：

```java
// 这是示例注释，请注意在双斜线之后有一个空格 
String param = new String();
```

### 在 Eclipse 中配置统一模板

**说明**
在Eclipse中window/Perferences/Java/Code Style/Code Template中可以配置模板，设置版权信息、说明、作者、创建时间等注释信息，可以修改成统一模板，每次新建类时自动创建这些注释信息，保持代码统一风格。附：[最新注释模板地址](https://docs.iwhalecloud.com/dmz-proxy/cos/share/406/检查工具和规则文件/Java/rules/tempalte/)
**检查方式**
无

## 声明(Declarations)

### 每行声明变量的数量(Number Per Line)

**【强制】一行一个声明**

**说明**
这样利于写注释。
**<font color="red">反例</font>**

```java
// indentation level and size of table
int level,size;
```

**正例**

```java
// indentation level
int level;
// size of table
int size;
```

**检查方式**
工具检查

**【强制】不要将不同类型变量的声明放在同一行**
**<font color="red">反例</font>**

```java
int foo, fooarray[];
```

**正例**

```java
int foo, 
int[] fooarray;
```

**检查方式**
工具检查

**【强制】类型和标识符之间可以用空格或者制表符分隔**
**正例**

```java
// indentation level
int level;
// size of table
int size;
// currently selected table entry
Object currentEntry;
```

**检查方式**
工具检查

### 初始化(Initialization)

**【强制】尽量在声明局部变量的同时初始化。**

**说明**
唯一不这么做的理由是变量的初始值依赖于某些先前发生的计算。
**检查方式**
工具检查

### 布局(Placement)

**【强制】一般情况下在代码块的开始处声明变量，将局部变量的作用域最小化。**

**说明**
块是指任何被包含在大括号"{"和"}"中间的代码。
该规则的一个例外是for循环的索引变量

```java
for (int i = 0; i < maxLoops; i++) { ... }
```

**正例**

```java
void myMethod() {
    // beginning of method block
    int int1 = 0; 
    if (condition) {
        // beginning of "if" block
        int int2 = 0; 
        ...
    }
}
```

**检查方式**
工具检查

**【强制】避免声明的局部变量覆盖上一级声明的变量**
**说明**
不要在内部代码块中声明相同的变量名
**<font color="red">反例</font>**

```java
int count;
public void myMethod() {
    if (condition) {
        // 避免这样
        int count = 0; 
        ...
    }
}
```

**检查方式**
工具检查

### 类和接口的声明(Class and Interface Declarations)

**【强制】当编写类和接口时，应该遵守以下格式规则：**

- 在方法名与其参数列表之前的左括号"("间不要有空格
- 左大括号"{"位于声明语句同行的末尾
- 右大括号"}"另起一行，与相应的声明语句对齐，除非是一个空语句，"}"应紧跟在"{"之后
- 方法与方法之间以空行分隔

**正例**

```java
class Sample {
    int ivar1;
    int ivar2;

    Sample(int i, int j) {
        ivar1 = i;
        ivar2 = j;
    }

    int emptyMethod() {}
    ...
}
```

**检查方式**
工具检查

**【推荐】在JDK16以上，推荐使用record关键字定义不可变的数据结构，它可以自动生成构造方法、equals()、hashCode()、toString()方法以及访问字段的方法。**

**正例：**

```java
public record RecordExample(String name, Integer age, String address) {
}
```

Record类已经帮我们写好了以下这些方法：
* 构造方法
* equals() 方法
* hashCode() 方法
* toString() 方法
* 读取不可变数据的方法

## 语句(Statements)

### 简单语句(Simple Statements)

**【强制】每行至多包含一条语句**

**<font color="red">反例</font>**

```java
argv++; argc--;
```

**正例**

```java
argv++; 
argc--; 
```

**检查方式**
工具检查

### 复合语句(Compound Statements)

复合语句是包含在大括号中的语句序列，形如"{ 语句 }"。
**【强制】被括其中的语句应该较之复合语句缩进一个层次**

**检查方式**
工具检查

**【强制】左大括号"{"应位于复合语句起始行的行尾；右大括号"}"应另起一行并与复合语句首行对齐。**

**检查方式**
工具检查

**【强制】大括号可以被用于所有语句，包括单个语句，只要这些语句是诸如if-else或for控制结构的一部分。**

**说明**
这样便于添加语句而无需担心由于忘了加括号而引入bug。

**检查方式**
工具检查

### 返回语句(return Statements)

**【强制】一个带返回值的return语句不使用小括号"()"，除非它们以某种方式使返回值更为显见。**
**正例**

```java
return;
return myDisk.size();
return (size ? size : defaultSize);
```

**检查方式**
工具检查

### 块语句

**【强制】if,else,while,for语句必须有{}。**

**检查方式**
工具检查

**【强制】“｛”必须在一行之末，“｝”在一行之头。**
**正例**

```java
Connection conn = ConnectionFactory.getConnection();
if (...) {
	...
}
else {
	...
}
```

**检查方式**
工具检查

**【强制】如果是大括号内为空，则简洁地写成{}即可，大括号中间无需换行和空格；如果是非空代码块则：**

1. 左大括号前不换行。
2. 左大括号后换行。
3. 右大括号前换行。
4. 表示终止的右大括号后必须换行。

**【强制】switch必须有default。**
**检查方式**
工具检查

### if，if-else，if else-if else 语句(if, if-else, if else-if else Statements)

**【强制】if-else语句应该具有如下正例所示格式：**
**正例**

```java
// example1
if (condition) {
    statements;
}

// example2
if (condition) {
    statements;
}
else {
    statements;
}

// example3
if (condition) {
    statements;
}
else if (condition) {
    statements;
}
else{
    statements;
}
```

**<font color="red">反例</font>**

```java
// 注意：if语句总是用"{"和"}"括起来，避免使用如下容易引起错误的格式：
if (condition) 
    statement;
```

**【强制】 `if`语句的嵌套深度不得超过3层。对于超过3层的条件判断，建议使用卫语句、策略模式、状态模式等来实现。**

**检查方式**
工具检查

### for 语句(for Statements)

**【强制】一个for语句应该具有如下正例所示格式：**
**正例**

```java
for (initialization; condition; update) {
    statements;
}
```

**【强制】 `for`循环的嵌套深度不得超过2层。对于超过2层的循环嵌套，建议重构循环逻辑，以减少嵌套。**

**检查方式**
工具检查

**【强制】一个空的for语句(所有工作都在初始化，条件判断，更新子句中完成）应该具有如下正例所示格式：**
**正例**

```java
for (initialization; condition; update);
```

**检查方式**
工具检查

**【强制】当在for语句的初始化或更新子句中使用逗号时，避免因使用三个以上变量，而导致复杂度提高。若需要，可以在for循环之前(为初始化子句)或for循环末尾(为更新子句)使用单独的语句。**
**检查方式**
工具检查

### while 语句(while Statements)

**【强制】一个while语句应该具有如下正例所示格式：**
**正例**

```java
while (condition) {
    statements;
}
```

**检查方式**
工具检查

**【强制】一个空的while语句应该具有如下正例所示格式：**
**正例**

```java
while (condition);
```

**检查方式**
工具检查

### do-while 语句(do-while Statements)

**【强制】一个do-while语句应该具有如下正例所示格式：**
**正例**

```java
do {
    statements;
} while (condition);
```

**检查方式**
工具检查

### switch 语句(switch Statements)

**【强制】一个switch语句应该具有如下正例所示格式：**
**正例**

```java
switch (condition) {
    case ABC:
        statements;
        break;
    case DEF:
        statements;
        break;
    case XYZ:
        statements;
        break;
    default:
        statements;
}
```

**检查方式**
工具检查

**【强制】每当一个case顺着往下执行时(因为没有break语句)，通常应在break语句的位置添加注释。**
**正例**

```java
switch (condition) {
    case ABC:
        statements;
        /* falls through */
    case DEF:
        statements;
        break;
    case XYZ:
        statements;
        break;
    default:
        statements;
```

**检查方式**
工具检查

**【推荐】在JDK14以上，在处理switch语句时，使用开关表达式(Switch Expressions)来简化代码和提高可读性。**
**正例：**

```java
boolean isRGB = switch(color) {
    case RED, GREEN, BLUE -> true;
    case YELLOW, BLACK, WHITE -> false;
    default -> false;
};
```

### try-catch 语句(try-catch Statements)

**【强制】一个try-catch语句应该具有如下正例所示格式：**
**说明**
一个try-catch语句后面也可能跟着一个finally语句，不论try代码块是否顺利执行完，它
都会被执行。

```java
try {
    statements;
}
catch (ExceptionClass e) {
    statements;
}
finally {
    statements;
}
```

**正例**

```java
try {
    statements;
}
catch (ExceptionClass e) {
    statements;
}
```

**【强制】 `try-catch`块的嵌套深度不得超过2层。对于超过2层的异常处理嵌套，建议简化catch块中的逻辑，避免不必要的再次抛出异常或者使用try-with-resources语句自动管理资源。**

**检查方式**
工具检查

## 空白(White Space)

### 空行(Blank Lines)

**【强制】空行将逻辑相关的代码段分隔开，以提高可读性。下列情况应该总是使用一个空行：**

- 两个方法之间
- 方法内的局部变量和方法的第一条语句之间
- 块注释或单行注释之前
- 一个方法内的两个逻辑段之间，用以提高可读性

**检查方式**
工具检查

### 空格(Blank Spaces)

**【强制】一个紧跟着括号的关键字应该被空格分开。**
**说明**
空格不应该置于方法名与其左括号之间。这将有助于区分关键字和方法调用。
**正例**

```java
while (true) {
    ...
}
```

**检查方式**
工具检查

**【强制】方法参数在定义和传入时，多个参数逗号后边必须加空格。**
**正例**

```java
List list = Arrays.asList(1, 2, 3);
```

**检查方式**
工具检查

**【强制】所有的二元运算符，除了"."，应该使用空格将之与操作数分开。一元操作符和操作数之间不应该加空格，比如：负号("-")、自增("++")和自减("--")。**
**正例**

```java
a += c + d;
a = (a + b) / (c * d);
while (d++ = s++) {
    n++;
}
printSize("size is " + foo + "\n");
```

**检查方式**
工具检查

**【强制】for语句中的表达式应该被空格分开。**
**正例**

```java
for (expr1; expr2; expr3)
```

**检查方式**
工具检查

**【强制】强制转型后应该跟一个空格。**
**正例**

```java
myMethod((byte) aNum, (Object) x);
myMethod((int) (cp + 5), ((int) (i + 3)) + 1);
```

**检查方式**
工具检查

**【强制】左小括号和字符之间不出现空格；同样，右小括号和字符之间也不出现空格；而左大括号前需要空格。**
反例：if (空格`a == b`空格)

## 命名规范(Naming Conventions)

命名规范使程序更易读，从而更易于理解。它们也可以提供一些有关标识符功能的信息，以助于理解代码，例如，不论它是一个常量、包还是类。

### 命名规则说明

**【强制】** 杜绝完全不规范的缩写，避免望文不知义。

```java
反例：AbstractClass“缩写”命名成AbsClass；condition“缩写”命名成 condi，此类随意缩写严重降低了代码的可阅读性。
```

**【推荐】** 为了达到代码自解释的目标，任何自定义编程元素在命名时，使用尽量完整的单词组合来表达其意。

```java
正例：在JDK中，表达原子更新的类名为：AtomicReferenceFieldUpdater。 
反例：int a的随意命名方式。
```

**【强制】** 代码中的命名严禁使用拼音与英文混合的方式，更不允许直接使用中文的方式。 说明：正确的英文拼写和语法可以让阅读者易于理解，避免歧义。注意，纯拼音命名方式更要避免采用。

```java
正例：renminbi/alibaba/taobao/youku/hangzhou 等国际通用的名称，可视同英文。 
反例：DaZhePromotion[打折]/getPingfenByName()[评分]/int 某变量 = 3
```

**【参考】** 各层命名规约：

```
A) Service/DAO层方法命名规约
```

```
1） 获取单个对象的方法用get做前缀。
```

```
2） 获取多个对象的方法用list做前缀，复数形式结尾如：listObjects。
```

```
3） 获取统计值的方法用count做前缀。
```

```
4） 插入的方法用save/insert做前缀。
```

```
5） 删除的方法用remove/delete做前缀。
```

```
6） 修改的方法用update做前缀。
```

```
B) 领域模型命名规约
```

```
1） 数据对象：xxxDO，xxx即为数据表名。
```

```
2） 数据传输对象：xxxDTO，xxx为业务领域相关的名称。
```

```
3） 展示对象：xxxVO，xxx一般为网页名称。
```

```
4） POJO是DO/DTO/BO/VO的统称，禁止命名成xxxPOJO。
```

常见的命名规则如下，我们推荐使用第二种Camel大小写的命名规则。

| 命名规则                         | 规则说明                                                                                                                                                         |
| :--------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Pascal大小写                     | 所有单词第一个字母大写，其他字母小写。<br>例如：PascalCase                                                                                                       |
| Camel大小写                      | 除了第一个单词，<br>所有单词第一个字母大写，其他字母小写。<br>例如：camelCase                                                                                    |
| 匈牙利命名法(Hungarian Notation) | 属性 + 类型 + 对象描述<br>属性： g\_(全局变量)、c\_(常量)、m\_(类成员变量)、返回值 <br>类型：h(句柄)、b(布尔)、n(整形) <br>对象描述：Src(源对象)、Dest(目的对象) |

### 具体规范(Specified Conventions)

【强制】代码中的命名均不能以下划线或美元符号开始，也不能以下划线或美元符号结束。 反例：\_name / \_\_name / \$name / name\_ / name\$ / name\_\_

#### Package(包)

**【强制】** 包名统一使用小写，点分隔符之间有且仅有一个自然语义的英语单词。包名统一使用单数形式，但是类名如果有复数含义，类名可以使用复数形式。

```java
正例：应用工具类包名为com.alibaba.ai.util、类名为MessageUtils（此规则参考spring的框架结构）
```

采用完整的英文描述符，应该都是由小写字母组成。

```java
正例：com.iwhalecloud.zsmart.bss.cust.service
```

#### Interface(接口)、Class(类)

- 类名应该是名词，或者是名词+动词。
- 采用完整的英文描述符说明接口封装，所有单词的第一个字母大写。(当使用Pascal命名规范)
- 通常由多个单词合成一个类名，要求每个单词的首字母也要大写。
- 接口首字母为"I"。

**【强制】** 类名使用UpperCamelCase风格，但以下情形例外：DO/BO/DTO/VO/AO/PO/UID等。

```java
正例：JavaServerlessPlatform/UserDO/XmlService/TcpUdpDeal/TaPromotion 
反例：javaserverlessplatform/UserDo/XMLService/TCPUDPDeal/TAPromotion
```

**【强制】** 抽象类命名使用Abstract或Base开头；异常类命名使用Exception结尾；测试类命名以它要测试的类的名称开始，以Test结尾。

**【强制】** 类型与中括号紧挨相连来表示数组。 正例：定义整形数组int[] arrayDemo; 反例：在main参数中，使用String args[]来定义。

**【强制】** POJO类中布尔类型变量都不要加is前缀，否则部分框架解析会引起序列化错误。说明：在本文MySQL规约中的建表约定第一条，表达是与否的值采用is_xxx的命名方式，所以，需要在<resultMap>设置从is_xxx到xxx的映射关系。

```log
反例：定义为基本数据类型Boolean isDeleted的属性，它的方法也是isDeleted()，RPC框架在反向解析的时候，“误以为”对应的属性名称是deleted，导致属性获取不到，进而抛出异常。
```

**【强制】** 避免在子父类的成员变量之间、或者不同代码块的局部变量之间采用完全相同的命名，使可读性降低。 说明：子类、父类成员变量名相同，即使是public类型的变量也是能够通过编译，而局部变量在同一方法内的不同代码块中同名也是合法的，但是要避免使用。对于非setter/getter的参数名称也要避免与成员变量名称相同。

```java
反例： 
public class ConfusingName { 
    public int age; 
    // 非setter/getter的参数名称，不允许与本类成员变量同名 
    public void getData(String alibaba) { 
        if(condition) { 
            final int money = 531;
            // ... 
        } 
        for (int i = 0; i < 10; i++) { 
            // 在同一方法体中，不允许与其它代码块中的money命名相同 
            final int money = 615; 
            // ... 
        } 
    } 
} 
class Son extends ConfusingName { 
    // 不允许与父类的成员变量名称相同 
    public int age; 
}
```

**【推荐】** 如果模块、接口、类、方法使用了设计模式，在命名时需体现出具体模式。 说明：将设计模式体现在名字中，有利于阅读者快速理解架构设计理念。

```java
正例： 
public class OrderFactory; 
public class LoginProxy; 
public class ResourceObserver;
```

**【推荐】** 接口类中的方法和属性不要加任何修饰符号（public 也不要加），保持代码的简洁性，并加上有效的Javadoc注释。尽量不要在接口里定义变量，如果一定要定义变量，肯定是与接口方法相关，并且是整个应用的基础常量。

```java
正例：接口方法签名 void commit(); 接口基础常量 String COMPANY = "alibaba"; 
反例：接口方法定义 public abstract void f(); 
说明：JDK8中接口允许有默认实现，那么这个default方法，是对所有实现类都有价值的默认实现。
```

**【强制】** 对于Service和DAO类，基于SOA的理念，暴露出来的服务一定是接口，内部的实现类用Impl的后缀与接口区别。

```java
正例：CacheServiceImpl实现CacheService接口。
```

**【推荐】** 如果是形容能力的接口名称，取对应的形容词为接口名（通常是–able的形容词）。

```java
正例：AbstractTranslator实现 Translatable接口。
```

#### Enum(枚举)

**【参考】** 枚举类名带上Enum后缀，枚举成员名称需要全大写，单词间用下划线隔开。 说明：枚举其实就是特殊的类，域成员均为常量，且构造方法被默认强制是私有。

```java
正例：枚举名字为 ProcessStatusEnum 的成员名称：SUCCESS/UNKNOWN_REASON。
```

#### Function(方法)

**【强制】** 方法名、参数名、成员变量、局部变量都统一使用lowerCamelCase风格，必须遵从驼峰形式。

```java
正例： localValue/getHttpMessage()/inputUserId
```

- 方法名首字母小写；(Camel命名)
- 在每个方法名内，大写字母将词分隔并限制使用下划线。
- 方法名最好是一个动词或者动词短语，与参数或参数名共同组成动宾短语，即动词 + 名词。
- 参数的名字必须和变量的命名规范一致。
- 使用有意义的参数命名，如果可能的话，使用和要赋值的字段一样的名字。
- 数据访问层方法，建议使用insert/update/delete/selectxxxxxx作为方法名称前缀。
- 业务层方法：建议使用 add/mod/del/qryxxxxxx作为方法名称前缀。

#### 数组

**【强制】** 类型与中括号紧挨相连来表示数组。

```java
正例：byte[] buffer
反例：byte buffer[]
```

原则：务必区分清楚单个对象还是多个数组或者列表对象

#### 变量

**【强制】** 变量的命名应当采用Camel命名方式

示例代码：

```java
StringBuffer userDetailBuffer;
ArrayList acctItemDtoList;
HashMap servHistoryMap;
int length;
```

#### 非静态属性

非静态属性第一个单词的首字母小写，非开始单词第一个字母大写，不使用前缀。

#### Dto属性(映射表字段)

Dto属性(映射表字段) Camel命名，与数据库字段对应。

#### Constant(常量)

**【强制】** 常量命名全部大写，要使用关键字final，单词间用下划线隔开，力求语义表达完整清楚，不要嫌名字长。

```java
正例：MAX_STOCK_COUNT/CACHE_EXPIRED_TIME 
反例：MAX_COUNT/EXPIRED_TIME
```

**例外：** logger也是常量，可以使用小写命名，示例如下：

```java
public static final ZSmartLogger logger = ZSmartLogger.getLogger(AdviceManagement.class);
```

**【推荐】** 在常量与变量的命名时，表示类型的名词放在词尾，以提升辨识度。

```java
正例：startTime / workQueue / nameList / TERMINATED_THREAD_COUNT 
反例：startedAt / QueueOfWork / listName / COUNT_TERMINATED_THREAD
```

#### 命名长度限制

避免长型名称(小于15个字符比较合适)，巧妙节俭地使用缩写，将标准首字母缩写词的第一个字母大写。

名称会经常包含标准缩写，如有标准缩写，请使用标准缩写。一切以简便为准。

#### 使用适用于领域内的术语

如果用户将他们的客户称为顾客，则对这个类使用术语Customer来代替Client。此条适用于所有命名。

# 编程惯例

## 集合处理

**【强制】** 关于 hashCode 和 equals 的处理，遵循如下规则：

* 只要覆写 equals，就必须覆写 hashCode。
* 因为 Set 存储的是不重复的对象，依据 hashCode 和 equals 进行判断，所以 Set 存储的对象必须覆写这两个方法。
* 如果自定义对象作为 Map 的键，那么必须覆写 hashCode 和 equals。

**说明** ：String 已覆写 hashCode 和 equals 方法，所以我们可以愉快地使用 String 对象作为 key 来使用。

**【强制】** ArrayList 的 subList 结果不可强转成 ArrayList，否则会抛出ClassCastException 异 常，即 java.util.RandomAccessSubList cannot be cast to java.util.ArrayList。

**说明** ：subList 返回的是 ArrayList 的内部类 SubList，并不是 ArrayList 而是 ArrayList 的一个视图，对

于 SubList 子列表的所有操作最终会反映到原列表上。

**【强制】** 使用 Map 的方法 keySet()/values()/entrySet()返回集合对象时，不可以对其进行添加元素操作，否则会抛出 UnsupportedOperationException 异常。

**【强制】** Collections 类返回的对象，如：emptyList()/singletonList()等都是 immutable list，不可对其进行添加或者删除元素的操作。

**反例**： 如果查询无结果，返回 Collections.emptyList()空集合对象，调用方一旦进行了添加元素的操作，就会触发  UnsupportedOperationException 异常。

**【强制】** 在 subList 场景中，高度注意对原集合元素的增加或删除，均会导致子列表的遍历、增加、删除产生 ConcurrentModificationException 异常。

**【强制】** 使用集合转数组的方法，必须使用集合的 toArray(T[] array)，传入的是类型完全一致、长度为 0 的空数组。
**反例**：直接使用 toArray 无参方法存在问题，此方法返回值只能是 Object[]类，若强转其它类型数组将出现 ClassCastException 错误。
**正例**：

```java
List<String> list = new ArrayList<>(2);
list.add("guan");
list.add("bao");
String[] array = list.toArray(new String[0]);
```

**说明** ：使用 toArray 带参方法，数组空间大小的 length：

* 等于 0，动态创建与 size 相同的数组，性能最好。
* 大于 0 但小于 size，重新创建大小等于 size 的数组，增加 GC 负担。
* 等于 size，在高并发情况下，数组创建完成之后，size 正在变大的情况下，负面影响与上相同。
* 大于 size，空间浪费，且在 size 处插入 null 值，存在 NPE 隐患。

**【强制】** 在使用 Collection 接口任何实现类的 addAll()方法时，都要对输入的集合参数进行NPE 判断。

**说明**：在 ArrayList#addAll 方法的第一行代码即 Object[] a = c.toArray(); 其中 c 为输入集合参数，如果为 null，则直接抛出异常。

**【强制】** 使用工具类 Arrays.asList()把数组转换成集合时，不能使用其修改集合相关的方法，它的 add/remove/clear 方法会抛出 UnsupportedOperationException 异常。

**说明**：asList 的返回对象是一个 Arrays 内部类，并没有实现集合的修改方法。Arrays.asList 体现的是适配器模式，只是转换接口，后台的数据仍是数组。

```java
String[] str = new String[] { "yang", "hao" };
List list = Arrays.asList(str);
```

第一种情况：list.add("yangguanbao"); 运行时异常。
第二种情况：str[0] = "changed"; 也会随之修改，反之亦然。

**【强制】** 泛型通配符<? extends T>来接收返回的数据，此写法的泛型集合不能使用 add 方 法，而<? super T>不能使用 get 方法，作为接口调用赋值时易出错。

**说明**：在集合类中存取数据时往往需要进行强制类型转换，而应用泛型后类型转换从运行期转移到了编译期，为较大的性能优化带来了可能。扩展说一下 PECS(Producer Extends Consumer Super)原则：第一、频繁往外读取内容的，适合用<? extends T>。第二、经常往里插入的，适合用<? super T>

**【强制】** 在无泛型限制定义的集合赋值给泛型限制的集合时，在使用集合元素时，需要进行instanceof 判断，避免抛出 ClassCastException 异常。

**说明**：毕竟泛型是在 JDK5 后才出现，考虑到向前兼容，编译器是允许非泛型集合与泛型集合互相赋值。

**反例**：

```java
List<String> generics = null;
List notGenerics = new ArrayList(10);
notGenerics.add(new Object());
notGenerics.add(new Integer(1));
generics = notGenerics;
// 此处抛出 ClassCastException 异常
String string = generics.get(0);
```

**【推荐】在JDK16以上，使用instanceof模式匹配可以简化类型检查和转换的代码。**
这种模式匹配方式减少了代码的冗余，并使得类型检查更加直观。

**正例：**

```java
AbstractObject obj = origin;
if (obj instanceof InheritanceObject inheritance) {
    // TODO 此时inheritance对象已经是InheritanceObject了
}
```

**【强制】** 不要在列表遍历的循环里进行元素的 remove/add 操作。remove 元素请使用Iterator 方式，如果并发操作，需要对 Iterator 对象加锁。

**正例**：

```java
List<String> list = new ArrayList<>(); 
list.add("1"); 
list.add("2"); 
Iterator<String> iterator = list.iterator(); 
while (iterator.hasNext()) { 
	String item = iterator.next(); 
	if (删除元素的条件) { 
		iterator.remove(); 
	} 
}
```

**反例**:

```java
for (String item : list) { 
	if ("1".equals(item)) { 
		list.remove(item); 
	} 
}
```

**说明**：以上代码的执行结果肯定会出乎大家的意料，那么试一下把“1”换成“2”，会是同样的结果吗？

**【强制】** 在 JDK7 版本及以上，Comparator 实现类要满足如下三个条件，不然 Arrays.sort，Collections.sort 会抛 IllegalArgumentException 异常。

**说明** ：三个条件如下

1） x，y 的比较结果和 y，x 的比较结果相反。

2） x>y，y>z，则 x>z。

3） x=y，则 x，z 比较结果和 y，z 比较结果相同。

**反例** ：下例中没有处理相等的情况，交换两个对象判断结果并不互反，不符合第一个条件，在实际使用中

可能会出现异常。

```java
new Comparator<Student>() { 
    @Override 
    public int compare(Student o1, Student o2) { 
        return o1.getId() > o2.getId() ? 1 : -1; 
    } 
};
```

**【推荐】** 集合泛型定义时，在 JDK7 及以上，使用 diamond 语法或全省略。

**说明** ：菱形泛型，即 diamond，直接使用<>来指代前边已经指定的类型。

**正例** :

```java
// diamond 方式，即<>
HashMap<String, String> userCache = new HashMap<>(16);
// 全省略方式
ArrayList<User> users = new ArrayList(10);
```

**【推荐】** 集合初始化时，指定集合初始值大小。

**说明** ：HashMap 使用 HashMap(int initialCapacity) 初始化, Arraylist使用ensureCapacity()方法设置ArrayList的容量,在处理已知容量的较大数组时可以避免ArrayList自动扩容带来的性能消耗。

**正例** ：initialCapacity = (需要存储的元素个数 / 负载因子) + 1。注意负载因子（即 loader factor）默认为 0.75，如果暂时无法确定初始值大小，请设置为 16（即默认值）。

**反例** ：HashMap 需要放置 1024 个元素，由于没有设置容量初始大小，随着元素不断增加，容量 7 次被迫扩大，resize 需要重建 hash 表，严重影响性能。

**【推荐】** 使用 entrySet 遍历 Map 类集合 KV，而不是 keySet 方式进行遍历。

**说明** ：keySet 其实是遍历了 2 次，一次是转为 Iterator 对象，另一次是从 hashMap 中取出 key 所对应的 value。而 entrySet 只是遍历了一次就把 key 和 value 都放到了 entry 中，效率更高。如果是 JDK8，使用 Map.forEach 方法。

**正例** ：values()返回的是 V 值集合，是一个 list 集合对象；keySet()返回的是 K 值集合，是一个 Set 集合对象；entrySet()返回的是 K-V 值组合集合。

【推荐】高度注意 Map 类集合 K/V 能不能存储 null 值的情况，如下表格：

| 集合类            | Key           | Value         | Super       | 说明                   |
| ------------------- | --------------- | --------------- | ------------- | ------------------------ |
| Hashtable         | 不允许为 null | 不允许为 null | Dictionary  | 线程安全               |
| ConcurrentHashMap | 不允许为 null | 不允许为 null | AbstractMap | 锁分段技术（JDK8:CAS） |
| TreeMap           | 不允许为 null | 允许为 null   | AbstractMap | 线程不安全             |
| HashMap           | 允许为 null   | 允许为 null   | AbstractMap | 线程不安全             |

**反例** ：由于 HashMap 的干扰，很多人认为 ConcurrentHashMap 是可以置入 null 值，而事实上，存储

null 值时会抛出 NPE 异常。

【推荐】不涉及多线程同步问题时，尽量选用非线程安全的集合类

**说明** :在多线程的环境下使用线程安全的集合类（例如Vector）代码会比较简洁、安全；但是不涉及多线程同步问题时，使用非线程安全的集合类（例如ArrayList）会具有更好的性能。

【参考】合理利用好集合的有序性(sort)和稳定性(order)，避免集合的无序性(unsort)和不稳定性(unorder)带来的负面影响。

**说明**：有序性是指遍历的结果是按某种比较规则依次排列的。稳定性指集合每次遍历的元素次序是一定的。如：ArrayList 是 order/unsort；HashMap 是 unorder/unsort；TreeSet 是 order/sort。

【参考】利用 Set 元素唯一的特性，可以快速对一个集合进行去重操作，避免使用 List 的contains 方法进行遍历、对比、去重操作。

【参考】在列表中进行随机查找，使用ArrayList速度更快；在列表任意位置进行插入、删除，使用LinkedList速度更快。如果预先可以知道数据大小，则尽量使用数组。

**【推荐】在JDK9以上，推荐使用List.of()、Set.of()、Map.of()和Map.ofEntries()等工厂方法创建不可变集合。这种方式可以使代码更加简洁，并且提高性能。**

**正例：**

java

```java
Set<String> languages = Set.of("java", "python", "c++", "go", "rust");
```

【说明】不可变集合意味着程序不能向集合中添加元素，也不能从集合中删除元素。

## 并发处理

**【强制】 获取单例对象需要保证线程安全，其中的方法也要保证线程安全。说明：资源驱动类、工具类、单例工厂类都需要注意。**

> :warning: 故障警示! 本规范制定源自严重生产故障（单号：3786355）。
> - 在3786355故障案例中，在核心业务类的static代码块中调用单例工厂类获取缓存对象，因为单例工厂类没有保证线程安全，导致static代码块获取到尚未完成初始化的单例缓存对象，导致业务配置读取失败的故障。

**<font color="red">反例</font>**

```java
public static ConfigItemCache instance() {  
    if (null == instance) {  
        synchronized (ConfigItemCache.class) {  
            if (null == instance) {  
                instance = new ConfigItemCache();  // 此处，instance 对象尚未完成初始化，可能会被其它线程获取到，产生数据错误
                instance.init();  
                instance.registerCacheRefreshListener();  
            }  
        }  
    }  
    return instance;  
}
```

**<font color="red">正例</font>**

```java
public static ConfigItemCache instance() {  
    if (null == instance) {  
        synchronized (ConfigItemCache.class) {  
            if (null == instance) {  
                ConfigItemCache tempInstance = new ConfigItemCache();  
                tempInstance.init();  
                tempInstance.registerCacheRefreshListener();  
                instance = tempInstance;  // 此处，instance 对象已经完成初始化
            }  
        }  
    }  
    return instance;  
}
```

**【强制】创建线程或线程池时请指定有意义的线程名称，方便出错时回溯**

**正例**

```java
	public class TimerTaskThread extends Thread {  
        public TimerTaskThread() {  
              super.setName("TimerTaskThread");   
              ... 
        }
    }

```

**【强制】线程资源必须通过线程池提供，不允许在应用中自行显式创建线程**

说明：使用线程池的好处是减少在创建和销毁线程上所花的时间以及系统资源的开销，解决资源不足的问题。如果不使用线程池，有可能造成系统创建大量同类线程而导致消耗完内存或者“过度切换”的问题。

**【强制】线程池不允许使用Executors去创建，而是通过ThreadPoolExecutor的方式**

说明：这样的处理方式让写的同学更加明确线程池的运行规则，从而规避资源耗尽的风险。

Executors返回的线程池对象的弊端如下：
1）FixedThreadPool和SingleThreadPool:   允许的请求队列长度为Integer.MAX_VALUE，可能会堆积大量的请求，从而导致OOM。
2）CachedThreadPool和ScheduledThreadPool:   允许的创建线程数量为Integer.MAX_VALUE，可能会创建大量的线程，从而导致OOM。

【强制】SimpleDateFormat 是线程不安全的类，一般不要定义为static变量，如果定义为static，必须加锁，或者使用DateUtils工具类

正例：注意线程安全，使用`DateUtils`。亦推荐如下处理：

```java
private static final ThreadLocal<DateFormat> df = new ThreadLocal<DateFormat>() {  
    Override  
    protected DateFormat initialValue() {   
        return new SimpleDateFormat("yyyy-MM-dd");  
    }  
};
```

说明：如果是JDK8的应用，可以使用`Instant`代替`Date`，`LocalDateTime`代替`Calendar`，`DateTimeFormatter`代替`SimpleDateFormat`，官方给出的解释：

> simple beautiful strong immutable thread-safe。

**【强制】高并发时，同步调用应该去考量锁的性能损耗**

说明：尽可能使加锁的代码块工作量尽可能的小，避免在锁代码块中调用RPC方法。能用无锁数据结构，就不要用锁；能锁区块，就不要锁整个方法体；能用对象锁，就不要用类锁。

举例：以synchronized为例，要使被synchronized包含{...}的操作尽可少，且同步的对象尽可能小。

**【强制】对多个资源、数据库表、对象同时加锁时，需要保持一致的加锁顺序，否则可能会造成死锁**

说明：线程一需要对表A、B、C依次全部加锁后才可以进行更新操作，那么线程二的加锁顺序也必须是A、B、C，否则可能出现死锁。

**【强制】并发修改同一记录时，避免更新丢失，需要加锁。要么在应用层加锁，要么在缓存加锁，要么在数据库层使用乐观锁，使用version作为更新依据**

说明：如果每次访问冲突概率小于20%，推荐使用乐观锁，否则使用悲观锁。乐观锁的重试次数不得小于3次。

**【强制】禁止使用 Timer 和 TimerTask 调度多任务，避免因未捕获单个任务异常而导致所有任务终止**

> :warning: 故障警示! 本规范制定源自严重生产故障（单号：3787793）。
> - 在3787793故障案例中，通过 Timer 提交了多个任务，包含了内存清理的任务，当应用繁忙内存资源不足的时候，会导致某些定时任务失败以及整个Timer定时任务的退出，数据无法得到及时清理，引发了OOM的故障。

1. **禁止直接使用 `Timer` 调度任务**

   * **原因**：`Timer` 单线程执行所有 `TimerTask`，若任一任务抛出未捕获异常，整个 `Timer` 线程终止，**其他任务将不再执行**。

   * **替代方案**：使用 `ScheduledExecutorService`（基于线程池），其任务异常仅影响当前任务，不扩散至其他任务。

2. **正例：使用 `ScheduledExecutorService`**

```java
    // 创建线程池（支持多线程并行）
    ScheduledExecutorService executor = Executors.newScheduledThreadPool(4);
    
    // 提交任务，即使 task2 抛出异常，task1 仍正常执行
    executor.scheduleAtFixedRate(this::task1, 0, 1, TimeUnit.SECONDS);
    executor.scheduleAtFixedRate(this::task2, 0, 2, TimeUnit.SECONDS);
```

3. **反例：`Timer` 导致任务链式终止**

```java
    Timer timer = new Timer();
    timer.schedule(new TimerTask() {
        @Override
        public void run() {
            throw new RuntimeException("Task1 异常"); // 未捕获异常，Timer 线程终止
        }
    }, 0, 1000);
    
    timer.schedule(new TimerTask() { // 此任务永远不会执行
        @Override
        public void run() { /* ... */ }
    }, 0, 1000);
```

4. **异常处理要求**

   * **强制**：在任务逻辑内部捕获所有异常，并记录日志，禁止异常抛出至线程池。

   * **推荐**：通过 `try-catch` 包裹任务代码，结合监控告警：

```java
    executor.scheduleAtFixedRate(() -> {
        try {
            // 业务逻辑
        } catch (Exception e) {
            logger.error("定时任务执行失败", e); // 记录异常，任务继续运行
        }
    }, 0, 1, TimeUnit.SECONDS);
```

5. **线程池配置**

   * **必须**根据任务类型（CPU 密集型/IO 密集型）合理设置线程池大小，避免资源耗尽：

```java
        // 正例：指定线程池大小（建议 CPU 核数 + 1）
        ScheduledExecutorService executor = Executors.newScheduledThreadPool(
            Runtime.getRuntime().availableProcessors() + 1
        );

```

**【强制】使用Lock类加锁时，必须确保锁范围内的所有代码都受到 try-finally 的保护，以确保在必要时释放锁。建议在try代码块之前调用lock方法，避免由于加锁失败导致finally调用unlock抛出异常。**

**正例**

```java
Lock l = ...;
l.lock();
try {
  // access the resource protected by this lock
} finally {
  l.unlock();
}
```

**【强制】 HashMap在容量不够进行resize时由于高并发可能出现死循环，导致CPU飙升，在多线程访问Map的场景下可以使用其它数据结构或加锁来规避此风险。**

说明：此问题在JDK8之前一直存在，在多线程访问Map的场景下，应使用ConcurrentHashMap。

**【推荐】使用`CountDownLatch`进行异步转同步操作，每个线程退出前必须调用countDown方法**

说明：线程执行代码注意catch异常，确保countDown方法被执行到，避免主线程无法执行至await方法，直到超时才返回结果。注意，子线程抛出异常堆栈，不能在主线程try-catch到。

**【推荐】避免Random实例被多线程使用**

说明：虽然共享该实例是线程安全的，但会因竞争同一seed 导致的性能下降。其中Random实例包括java.util.Random 的实例或者 Math.random()的方式。
**正例**在JDK7之后，可以直接使用API ThreadLocalRandom，而在 JDK7之前，需要编码保证每个线程持有一个实例。

**【推荐】在并发场景下，通过双重检查锁（double-checked locking）实现延迟初始化的优化问题隐患(可参考 The "Double-Checked Locking is Broken" Declaration)，推荐解决方案中较为简单一种（适用于JDK5及以上版本），将目标属性声明为 volatile型。**

**反例**

```java
class Singleton {   
      private Helper helper = null;  
      public Helper getHelper() {  
        if (helper == null) 
        synchronized(this) {  
          if (helper == null)  
          helper = new Helper();  
        }  
        return helper;  
      }  
      // other methods and fields...  
}
```

**【参考】volatile解决多线程内存不可见问题。对于一写多读，是可以解决变量同步问题，但是如果多写，同样无法解决线程安全问题**

说明：如果是count++操作，使用如下类实现：

```java
AtomicInteger count = new AtomicInteger(); 
count.addAndGet(1); 
```

如果是JDK8，推荐使用`LongAdder`对象，比`AtomicLong`性能更好（减少乐观锁的重试次数）。

**【参考】`ThreadLocal`无法解决共享对象的更新问题，`ThreadLocal`对象建议使用static修饰**

说明：这个变量是针对一个线程内所有操作共享的，所以设置为静态变量，所有此类实例共享此静态变量 ，也就是说在类第一次被使用时装载，只分配一块存储空间，所有此类的对象(只要是这个线程内定义的)都可以操控这个变量。

## 控制语句

【强制】在一个 switch 块内，每个 case 要么通过 continue/break/return 等来终止，要么注释说明程序将继续执行到哪一个 case 为止；在一个 switch 块内，都必须包含一个default 语句并且放在最后，即使它什么代码也没有。

**说明**：注意 break 是退出 switch 语句块，而 return 是退出方法体。

【强制】当 switch 括号内的变量类型为 String 并且此变量为外部参数时，必须先进行 null判断。

**反例**：以下代码会抛出NPE异常

```java
public class SwitchString {
    public static void main(String[] args) {
        method(null);
    }
    public static void method(String param) {
        switch (param) {
                // 肯定不是进入这里
            case "sth":
                System.out.println("it's sth");
                break;
                // 也不是进入这里
            case "null":
                System.out.println("it's null");
                break;
                // 也不是进入这里
            default:
                System.out.println("default");
        }
    } 
}
```

【强制】在 if/else/for/while/do 语句中必须使用大括号。

**说明**：即使只有一行代码，避免采用单行的编码方式：if (condition) statements;

【强制】在高并发场景中，避免使用”等于”判断作为中断或退出的条件。

**说明**：如果并发控制没有处理好，容易产生等值判断被“击穿”的情况，使用大于或小于的区间判断条件

来代替。

**反例**：判断剩余奖品数量等于 0 时，终止发放奖品，但因为并发处理错误导致奖品数量瞬间变成了负数，

这样的话，活动无法终止。

【强制】如果一个包含二元运算符的表达式出现在三元运算符" ? : "的"?"之前，那么应该给表达式添上一对圆括号。
**正例**:

```java
(x >= 0) ? x : -x; 
```

空引用判断
以下编码场景需要进行变量空引用判断

* 对于方法传入参数，需要进行必要的空引用判断。
* 获取配置信息时，进行空引用判断，建议获取配置值方法提供返回默认值方法
* 对List、Array等进行操作时（特别是判断size、length时）先进行空引用判断
* Map、List等动态集合对象，建议在创建时初始化，在函数返回时若集合为空，返回一个空的对象，而不是null。数组也是如此，返回零长度的数组而不是null。
  **【推荐】** 若一个查询方法查询的记录数为0时，不要返回null,而是返回一个空的List，因为大家已经习惯获取List时不对它进行空引用判断，而直接遍历它。

**正例**

```java
// 获取配置项为空，使用初始值为默认值，防止因没有配置项而抛空引用异常
// 100 为默认值
channelId = clientContext.params.getStr(SMPPConstants.BSS_CHANNEL_ID, "100");

// 调用List size()方法前,先进行空引用判断
List subsList = subsDAO.selectSubsList();
if(subsList!=null && subsList.size()>0){  
	// ... ...
}

```

【推荐】表达异常的分支时，少用 if-else 方式，这种方式可以改写成：

```java
if (condition) { 
    // ... 
 	return obj; 
} 
// 接着写 else 的业务逻辑代码; 
```

**说明**：如果非要使用 if()...else if()...else...方式表达逻辑，为避免后续代码维护困难，***【强制】*** 请勿超过 3 层。

正例：超过 3 层的 if-else 的逻辑判断代码可以使用卫语句、策略模式、状态模式等来实现，其中卫语句即代码逻辑先考虑失败、异常、中断、退出等直接返回的情况，以方法多个出口的方式，解决代码中判断分支嵌套的问题，这是逆向思维的体现。

**示例如下**：

```java
public void findBoyfriend(Man man) {
	if (man.isUgly()) {
     	System.out.println("本姑娘是外貌协会的资深会员");
     	return;
    }
    if (man.isPoor()) {
    	System.out.println("贫贱夫妻百事哀");
    	return;
    }
    if (man.isBadTemper()) {
    	System.out.println("银河有多远，你就给我滚多远");
     	return;
    }
    System.out.println("可以先交往一段时间看看");
}
```

【推荐】除常用方法（如 getXxx/isXxx）等外，不要在条件判断中执行其它复杂的语句，将复杂逻辑判断的结果赋值给一个有意义的布尔变量名，以提高可读性。

**说明**：很多 if 语句内的逻辑表达式相当复杂，与、或、取反混合运算，甚至各种方法纵深调用，理解成本非常高。如果赋值一个非常好理解的布尔变量名字，则是件令人爽心悦目的事情。

**正例**:

```java
// 伪代码如下
final boolean existed = (file.open(fileName, "w") != null) && (...) || (...);
if (existed) {
	...
}
```

**反例**:

```java
public final void acquire(long arg) {
 	if (!tryAcquire(arg) &&
 		acquireQueued(addWaiter(Node.EXCLUSIVE), arg)) {
 		selfInterrupt();
 	} 
}
```

【推荐】不要在其它表达式（尤其是条件表达式）中，插入赋值语句。

**说明**：赋值点类似于人体的穴位，对于代码的理解至关重要，所以赋值语句需要清晰地单独成为一行。

**反例**:

```java
public Lock getLock(boolean fair) {
    // 算术表达式中出现赋值操作，容易忽略 count 值已经被改变
 	threshold = (count = Integer.MAX_VALUE) - 1;
 	// 条件表达式中出现赋值操作，容易误认为是 sync==fair
	 return (sync = fair) ? new FairSync() : new NonfairSync();
}
```

【推荐】循环体中的语句要考量性能，以下操作尽量移至循环体外处理，如定义对象、变量、获取数据库连接，进行不必要的 try-catch 操作（这个 try-catch 是否可以移至循环体外）。

【推荐】避免采用取反逻辑运算符。

**说明**：取反逻辑不利于快速理解，并且取反逻辑写法必然存在对应的正向逻辑写法。

**正例**：使用 if (x < 628) 来表达 x 小于 628。

**反例**：使用 if (!(x >= 628)) 来表达 x 小于 628。

【推荐】接口入参保护，这种场景常见的是用作批量操作的接口。

【参考】下列情形，需要进行参数校验：

* 调用频次低的方法。
* 执行时间开销很大的方法。此情形中，参数校验时间几乎可以忽略不计，但如果因为参数错误导致 中间执行回退，或者错误，那得不偿失。
* 需要极高稳定性和可用性的方法。
* 对外提供的开放接口，不管是 RPC/API/HTTP 接口。
* 敏感权限入口。

【参考】下列情形，不需要进行参数校验：

* 极有可能被循环调用的方法。但在方法说明里必须注明外部参数检查要求。

* 底层调用频度比较高的方法。毕竟是像纯净水过滤的最后一道，参数错误不太可能到底层才会暴露问题。一般 DAO 层与 Service 层都在同一个应用中，部署在同一台服务器中，所以 DAO 的参数校验，可以省略。

* 被声明成 private 只会被自己代码所调用的方法，如果能够确定调用方法的代码传入参数已经做过检

  查或者肯定不会有问题，此时可以不校验参数。

## 注释规约

**【强制】类、类属性、类方法的注释必须使用Javadoc规范，使用\/\*\*内容\*\/格式，不得使用// xxx方式**

说明：在IDE编辑窗口中，Javadoc方式会提示相关注释，生成Javadoc可以正确输出相应注释；在IDE中，工程调用方法时，不进入方法即可悬浮提示方法、参数、返回值的意义，提高阅读效率。

**【强制】所有的抽象方法（包括接口中的方法）必须要用Javadoc注释、除了返回值、参数、异常说明外，还必须指出该方法做什么事情，实现什么功能**

说明：对子类的实现要求，或者调用注意事项，请一并说明。

**【强制】所有的类都必须添加创建者和创建日期**

**【强制】方法内部单行注释，在被注释语句上方另起一行，使用`//`注释。方法内部多行注释使用`/* */`注释，注意与代码对齐**

**【强制】所有的枚举类型字段必须要有注释，说明每个数据项的用途**

**【推荐】与其“半吊子”英文来注释，不如用中文注释把问题说清楚。专有名词与关键字保持英文原文即可**

反例：“TCP连接超时”解释成“传输控制协议连接超时”，理解反而费脑筋。

**【推荐】代码修改的同时，注释也要进行相应的修改，尤其是参数、返回值、异常、核心逻辑等的修改**

说明：代码与注释更新不同步，就像路网与导航软件更新不同步一样，如果导航软件严重滞后，就失去了导航的意义。

**【参考】谨慎注释掉代码。在上方详细说明<，而不是简单地注释掉。如果无用，则删除**

说明：代码被注释掉有两种可能性：

1）后续会恢复此段代码逻辑。

2）永久不用。前者如果没有备注信息，难以知晓注释动机。后者建议直接删掉（代码仓库保存了历史代码）。

**【参考】对于注释的要求**

说明：

1）能够准确反应设计思想和代码逻辑；

2）能够描述业务含义，使别的程序员能够迅速了解到代码背后的信息。完全没有注释的大段代码对于阅读者形同 天书，注释是给自己看的，即使隔很长时间，也能清晰理解当时的思路；注释也是给继任者看的，使其能够快速接替自己的工作。

**【参考】好的命名、代码结构是自解释的，注释力求精简准确、表达到位**

说明：避免出现注释的一个极端：过多过滥的注释，代码的逻辑一旦修改，修改注释是相当大的负担。

**反例**

```java
// put elephant into fridge  
put(elephant, fridge);  
方法名put，加上两个有意义的变量名elephant和fridge，已经说明了这是在干什么，语义清晰的代码不需要额外的注释。 
```

**【参考】特殊注释标记，请注明标记人与标记时间。注意及时处理这些标记，通过标记扫描，经常清理此类标记。线上故障有时候就是来源于这些标记处的代码**

说明：

1） 待办事宜（**TODO**）:（ 标记人，标记时间，[预计处理时间]） 表示需要实现，但目前还未实现的功能。这实际上是一个Javadoc的标签，目前的Javadoc还没有实现，但已经被广泛使用。只能应用于类，接口和方法（因为它是一个Javadoc标签）。
2） 错误，不能工作（**FIXME**）:（标记人，标记时间，[预计处理时间]） 在注释中用FIXME标记某代码是错误的，而且不能工作，需要及时纠正的情况。

## 异常处理

**强制：Java 类库中定义的可以通过预检查方式规避的 RuntimeException 异常不应该通过 catch 的方式来处理，比如：NullPointerException，IndexOutOfBoundsException 等等。**

<br><span style="color:orange">说明</span>：无法通过预检查的异常除外，比如，在解析字符串形式的数字时，可能存在数字格式错误，不得不通过 catch NumberFormatException 来实现。
**<font color="red">正例</font>**

```java
if (obj != null) {...}
```

**<font color="red">反例</font>**

```java
try { 
    obj.method(); 
} 
catch (NullPointerException e) {
    // xxx
}
```

**强制：异常不要用来做流程控制，条件控制。**

<span style="color:orange">说明</span>：异常设计的初衷是解决程序运行中的各种意外情况，且异常的处理效率比条件判断方式要低很多。

**强制： catch 时请分清稳定代码和非稳定代码，稳定代码指的是无论如何不会出错的代码。对于非稳定代码的 catch 尽可能进行区分异常类型，再做对应的异常处理。**

<span style="color:orange">说明</span>：对大段代码进行 try-catch，使程序无法根据不同的异常做出正确的应激反应，也不利于定位问题，这是一种不负责任的表现。
**<font color="red">正例</font>**
用户注册的场景中，如果用户输入非法字符，或用户名称已存在，或用户输入密码过于简单，在程序上作出分门别类的判断，并提示给用户。

**强制：捕获异常是为了处理它，不要捕获了却什么都不处理而抛弃之，如果不想处理它，请将该异常抛给它的调用者。最外层的业务使用者，必须处理异常，将其转化为用户可以理解的内容。**

**强制：有 try 块放到了事务代码中，catch 异常后，如果需要回滚事务，一定要注意手动回滚事务。**

**强制：finally 块必须对资源对象、流对象进行关闭，有异常也要做 try-catch。**

> :warning: 故障警示! 严重生产故障：[30999068](https://dev.iwhalecloud.com/portal/zcm-devspace/spa/task/pc/30999068)。某项目应用因为没有合理控制线程的创建和销毁，产生线程数量过多引发内存溢出（java.lang.OutOfMemoryError: native memory exhausted），导致核心系统无法登录的严重生产故障。在故障复盘时同时发现findbugs检查出代码中有不少资源泄漏类的问题（[ODR_OPEN_DATABASE_RESOURCE](https://spotbugs.readthedocs.io/en/stable/bugDescriptions.html#odr-method-may-fail-to-close-database-resource-odr-open-database-resource)），存在数据库连接泄露的隐患。

<span style="color:orange">说明</span>：如果 JDK7 及以上，可以使用 try-with-resources 方式。

> 关于`ODR_OPEN_DATABASE_RESOURCE`更多细节，请参考规范最后章节的FAQ。

**强制：不要在 finally 块中使用 return。**

<span style="color:orange">说明</span>：try 块中的 return 语句执行成功后，并不马上返回，而是继续执行 finally 块中的语句，如果此处存
在 return 语句，则在此直接返回，无情丢弃掉 try 块中的返回点。
**<font color="red">反例</font>**

```java
private int x = 0;
public int checkReturn() {
    try {
        // x 等于 1，此处不返回
        return ++x;
    } 
    finally {
        // 返回的结果是 2
        return ++x;
    }
}
```

**【推荐】在JDK9以上，使用try-with-resources语句时，无需在try语句中声明新变量，直接使用已有资源变量即可。**

**正例：**

```java
InputStream resource = new FileInputStream(filepath);
try (resource) {
    // TODO
}
```

**强制：捕获异常与抛异常，必须是完全匹配，或者捕获异常是抛异常的父类。**

<span style="color:orange">说明</span>：如果预期对方抛的是绣球，实际接到的是铅球，就会产生意外情况。

**推荐：在调用 RPC、二方包、或动态生成类的相关方法时，捕捉异常建议使用 Throwable类来进行拦截。**

<span style="color:orange">说明</span>：通过反射机制来调用方法，如果找不到方法，抛出 NoSuchMethodException。什么情况会抛出NoSuchMethodError 呢？二方包在类冲突时，仲裁机制可能导致引入非预期的版本使类的方法签名不匹配，或者在字节码修改框架（比如：ASM）动态创建或修改类时，修改了相应的方法签名。这些情况，即使代码编译期是正确的，但在代码运行期时，会抛出 NoSuchMethodError。

**推荐：方法的<span style="color:blue">返回值可以为 null</span> ，不强制返回空集合，或者空对象等，必须添加注释充分说明什么情况下会返回 null 值。**

<span style="color:orange">说明</span>：本手册明确防止 NPE 是调用者的责任。即使被调用方法返回空集合或者空对象，对调用者来说，也并非高枕无忧，必须考虑到远程调用失败、序列化失败、运行时异常等场景返回 null 的情况。

**推荐：防止 NPE ，是程序员的基本修养，注意 NPE 产生的场景：**

1） 返回类型为基本数据类型，return 包装数据类型的对象时，自动拆箱有可能产生 NPE。
**<font color="red">反例</font>** public int f() { return Integer 对象}， 如果为 null，自动解箱抛 NPE。
2） 数据库的查询结果可能为 null。
3） 集合里的元素即使 isNotEmpty，取出的数据元素也可能为 null。
4） 远程调用返回对象时，一律要求进行空指针判断，防止 NPE。
5） 对于 Session 中获取的数据，建议进行 NPE 检查，避免空指针。
6） 级联调用 obj.getA().getB().getC()；一连串调用，易产生 NPE。
**<font color="red">正例</font>**：使用 JDK8 的 Optional 类来防止 NPE 问题。

**推荐：定义时区分 unchecked / checked 异常，避免直接抛出 new  RuntimeException() ，更不允许抛出 Exception 或者 Throwable，应使用有业务含义的自定义异常。推荐业界已定义过的自定义异常，如：DAOException / ServiceException 等。**

**参考：对于公司外的 http/api 开放接口必须使用“错误码”；而应用内部推荐异常抛出；跨应用间 RPC 调用优先考虑<span style="color:blue">使用 Result 方式</span>，封装 isSuccess()方法、“错误码”、“错误简短信息”。**

<span style="color:orange">说明</span>：关于 RPC 方法返回方式使用 Result 方式的理由：
1）使用抛异常返回方式，调用方如果没有捕获到就会产生运行时错误。
2）如果不加栈信息，只是 new 自定义异常，加入自己的理解的 error message，对于调用端解决问题
的帮助不会太多。如果加了栈信息，在频繁调用出错的情况下，数据序列化和传输的性能损耗也是问题。

**参考：避免出现重复的代码 （Don ' t Repeat Yourself） ，即 DRY 原则。**

<span style="color:orange">说明</span>：随意复制和粘贴代码，必然会导致代码的重复，在以后需要修改时，需要修改所有的副本，容易遗
漏。必要时抽取共性方法，或者抽象公共类，甚至是组件化。
**<font color="red">正例</font>** 一个类中有多个 public 方法，都需要进行数行相同的参数校验操作，这个时候请抽取：

```java
private boolean checkParam(DTO dto) {...}
```

**强制：应避免在静态块（static block）中执行复杂逻辑，并妥善处理静态块内代码在执行时可能出现的异常，避免因未捕获的异常导致类加载失败，产生 NoClassDefFoundError 错误。例如：静态块中打开资源（如文件、网络连接等），确保即使在发生异常时也能正确进行异常处理和资源关闭。**

> :warning: 故障警示! 本规范制定源自两起严重生产故障（单号：3611738、3786355）。
> - 在3611738故障案例中，由于核心类的静态初始化逻辑中没有对可预见的异常进行处理，导致关键服务启动失败，进而引发了 NoClassDefFoundError 错误，致使服务中断。
> - 在3786355故障案例中，在核心业务类的static代码块中进行关键业务配置项的读取，没有对可预见的异常进行处理，导致业务配置读取失败的故障。

**<font color="red">正例</font>**

```java
static {
	SomeResource tempResource = null;
	try {
		tempResource = new SomeResource();
		tempResource.open();
		// 进行一些初始化操作
	} catch (Exception e) {
		// 处理异常，例如记录日志等
	} finally {
		if (tempResource != null) {
			try {
				tempResource.close();
			} catch (Exception e) {
				// 处理异常，例如记录日志等
			}
		}
	}
	resource = tempResource;
}
```

**<font color="red">反例</font>**

```java
static {
	try {
		resource = new SomeResource();
		resource.open(); // 如果这里抛出异常，后续的资源关闭将不会执行
		// 进行一些初始化操作
	} catch (Exception e) {
		throw new RuntimeException("初始化失败", e);
	}
}
```

## 资源管理

**强制：使用 HttpClient 时必须显式关闭响应资源，确保连接归还至连接池**

> :warning: 故障警示! 本规范制定源自严重生产故障（单号：3787588）。
> - 在3787588故障案例中，业务逻辑在处理HTTP请求时，当服务端正常返回（HttpStatus = 200）时则正常读取response流，自动释放HTTP连接；如果相应状态码非200的时候，则直接抛出异常，导致HTTP连接没有被释放引发泄露，导致后续请求无法获取连接的故障。

1. **显式关闭响应流和连接**

   * **必须**在请求完成后调用 `CloseableHttpResponse.close()` 或通过 `try-with-resources` 自动关闭，确保底层 TCP 连接释放。

   * **必须**完全读取或消费响应体（`HttpEntity`），否则连接无法复用。若仅需关闭流而不处理内容，调用 `EntityUtils.consume(entity)`。

2. **优先使用 try-with-resources**

   * Java 7+ 环境中，`CloseableHttpClient` 和 `CloseableHttpResponse` **必须**通过 `try-with-resources` 管理资源，避免手动关闭遗漏。

```java
    // 正例：自动关闭资源
    try (CloseableHttpClient httpClient = HttpClients.createDefault();
         CloseableHttpResponse response = httpClient.execute(request)) {
        HttpEntity entity = response.getEntity();
        String result = EntityUtils.toString(entity);
    } // 自动关闭 response 和 httpClient
```

3. **禁止未关闭响应直接丢弃**

   * **禁止**以下写法，未关闭的 `response` 会导致连接泄漏：

```java
// 反例：未关闭响应，连接泄漏！
CloseableHttpResponse response = httpClient.execute(request);  
if (HttpStatus.SC_OK == response.getStatusLine().getStatusCode()) {  
    HttpEntity entity = response.getEntity();  
    if (entity != null) {  
        String result = EntityUtils.toString(entity);  
        EntityUtils.consume(entity);  
        return JSON.parseObject(result, access);  
    } else {  
        throw new RuntimeException("请求失败"); //未关闭响应，连接泄漏！
    }  
}
```

4. **配置连接池参数**

   * **必须**为 `PoolingHttpClientConnectionManager` 设置合理的最大连接数和超时时间，防止资源耗尽：

```java
    PoolingHttpClientConnectionManager cm = new PoolingHttpClientConnectionManager();
    cm.setMaxTotal(100);                  // 最大连接数
    cm.setDefaultMaxPerRoute(50);         // 单路由最大连接数
    cm.setValidateAfterInactivity(5000);  // 空闲连接校验间隔（毫秒）
    CloseableHttpClient httpClient = HttpClients.custom().setConnectionManager(cm).build();
```

5. **防御性关闭流**

   * 即使已读取响应内容，**必须**在 `finally` 块中显式关闭流，确保异常时资源释放：

```java
    CloseableHttpResponse response = null;
    try {
        response = httpClient.execute(request);
        HttpEntity entity = response.getEntity();
        String result = EntityUtils.toString(entity);
    } finally {
        if (response != null) {
            EntityUtils.consume(response.getEntity()); // 确保流关闭
            response.close();
        }
    }
```

## 日志规约

**强制：应用中不可直接使用日志系统 （Log 4 j 、 Logback） 中的 API ，而应依赖使用日志框架SLF 4 J 中的 API ，使用门面模式的日志框架，有利于维护和各个类的日志处理方式统一。**
**<font color="red">正例</font>**

```java
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
private static final Logger logger = LoggerFactory.getLogger(Test.class);
```

**强制：所有日志文件至少保存 15 天，因为有些异常具备以“周”为频次发生的特点。网络运行状态、安全相关信息、系统监测、管理后台操作、用户敏感操作需要留存相关的网络日志不少于 6 个月。**
**强制：应用中的扩展日志 （ 如打点、临时监控、访问日志等 ） 命名方式：appName_logType_logName.log。**
logType:日志类型，如 stats/monitor/access 等；
logName:日志描述。
这种命名的好处：通过文件名就可知道日志文件属于什么应用，什么类型，什么目的，也有利于归类查找。
<br><span style="color:orange">说明</span>：推荐对日志进行分类，如将错误日志和业务日志分开存放，便于开发人员查看，也便于通过日志对
系统进行及时监控。
**<font color="red">正例</font>**  force-web 应用中单独监控时区转换异常，如：force_web_timeZoneConvert.log

**强制：在日志输出时，字符串变量之间的拼接使用占位符的方式。**
<span style="color:orange">说明</span>：使用占位符，是为了能够根据日志级别动态决定是否进行输出字符串拼装，减少不必要的拼装性能损耗。
**<font color="red">正例</font>**

```java
// 如下debug日志输出，在Error日志级别，不会进行字符串模版+变量的拼装。
logger.debug("Processing trade with id: {} and symbol: {}", id, symbol);
```

**强制：对于 trace / debug / info 级别的日志输出，如果日志输出方法的入参存在方法调用，外部必须进行日志级别的开关判断。**
<span style="color:orange">说明</span>：虽然在 debug(参数)的方法体内第一行代码 isDisabled(Level.DEBUG_INT)为真时（Slf4j 的常见实现 Log4j 和 Logback），就直接 return，但是参数可能会进行字符串拼接运算。此外，如果debug(getName())这种参数内有 getName()方法调用，无谓浪费方法调用的开销。
**<font color="red">正例</font>**

```java
// 如果判断为真，那么可以输出 trace 和 debug 级别的日志。
if (logger.isDebugEnabled()) {
    // 该日志输出方法的入参存在方法调用getName()
    logger.debug("Current ID is: {} and name is: {}", id, getName());
}
```

**强制：避免重复打印日志，浪费磁盘空间，务必在 log4j.xml或者logback.xml 中设置 additivity = false 。**
**<font color="red">正例</font>**

```Xml
<logger name="com.taobao.dubbo.config" additivity="false"> 
```

**强制：异常信息应该包括两类信息：案发现场信息和异常堆栈信息。如果不处理，那么通过关键字 throws 往上抛出。**
**<font color="red">正例</font>**  logger.error(各类参数或者对象 toString() + "_" + e.getMessage(), e);

**强制：国际化团队或海外部署的服务器由于字符集问题，使用全英文来注释和描述日志错误信息。**
<br>

**推荐：谨慎地记录日志。生产环境禁止输出 debug 日志 ； 有选择地输出 info 日志 ； 如果使用 warn 来记录刚上线时的业务行为信息，一定要注意日志输出量的问题，避免把服务器磁盘撑爆，并记得及时删除这些观察日志。**
<br><span style="color:orange">说明</span>：大量地输出无效日志，不利于系统性能提升，也不利于快速定位错误点。记录日志时请思考：这些日志真的有人看吗？看到这条日志你能做什么？能不能给问题排查带来好处？

**推荐：可以使用 warn 日志级别来记录用户输入参数错误的情况，避免用户投诉时，无所适从。如非必要，请不要在此场景打出 error 级别，避免频繁报警。**
<br><span style="color:orange">说明</span>：注意日志输出的级别，error 级别只记录系统逻辑出错、异常或者重要的错误信息。

**推荐：尽量用英文来描述日志错误信息，如果日志中的错误信息用英文描述不清楚的话使用中文描述即可，否则容易产生歧义。**
<br>

## 其他

**推荐：Long 或 long 类型变量赋值时，数值后使用大写 L，不能是小写 l ，小写容易跟数字混淆，造成误解。**

**强制：在使用正则表达式时，利用好其预编译功能，可以有效加快正则匹配速度。**

<br><span style="color:orange">说明</span>：不要在方法体内定义：Pattern pattern = Pattern.compile(“规则”);

**强制：velocity 调用 POJO 类的属性时，直接使用属性名取值即可，模板引擎会自动按规范调用 POJO 的 getXxx() ，如果是 boolean 基本数据类型变量 （boolean 命名不需要加 is 前缀 ） ，会自动调用 isXxx() 方法。**

<br><span style="color:orange">说明</span>：注意如果是 Boolean 包装类对象，优先调用 getXxx()的方法。

**强制：注意  Math . random() 这个方法返回是 double 类型，注意取值的范围 0≤ x <1 （ 能够取到<span style="color:blue">零</span>值，注意除零异常 ） ，如果想获取整数类型的随机数，不要将 x 放大 10 的若干倍然后取整，直接使用 Random 对象的 <span style="color:blue">nextInt</span> 值 或者 <span style="color:blue">nextLong</span> 方法。**

<br>

**强制：获取当前毫秒数用System.currentTimeMillis(); 而不是 new Date() . getTime();**

<br><span style="color:orange">说明</span>：如果想获取更加精确的纳秒级时间值，使用 System.nanoTime()的方式。在 JDK8 中，针对统计时间等场景，推荐使用 Instant 类。

**强制：日期格式化时，传入 pattern 中表示年份统一使用小写的 y。**

<br><span style="color:orange">说明</span>：日期格式化时， yyyy 表示当天所在的年，而大写的 YYYY 代表是 week in which year
（JDK7 之后引入的概念），意思是当天所在的周属于的年份，一周从周日开始，周六结束，
只要本周跨年，返回的 YYYY 就是下一年。另外需要注意：

- 表示月份是大写的 M
- 表示分钟则是小写的 m
- 24 小时制的是大写的 H
- 12 小时制的则是小写的 h

**<font color="red">正例</font>**
表示日期和时间的格式如下所示：

```java
new SimpleDateFormat("yyyy-MM-dd HH:mm:ss"); 
```

**推荐：不要在视图模板中加入任何复杂的逻辑。**

<br><span style="color:orange">说明</span>：根据 MVC 理论，视图的职责是展示，不要抢模型和控制器的活。

**推荐：任何数据结构的构造或初始化，都应指定大小，避免数据结构无限增长吃光内存。**

<br>

**推荐：及时清理不再使用的代码段或配置信息。**

<br><span style="color:orange">说明</span>：对于垃圾代码或过时配置，坚决清理干净，避免程序过度臃肿，代码冗余。
**<font color="red">正例</font>**
对于暂时被注释掉，后续可能恢复使用的代码片断，在注释代码上方，统一规定使用三个斜杠(///)来说明注释掉代码的理由。

**提供对实例以及类变量的访问控制(Providing Access to Instance and Class Variables)**

类成员与方法访问控制从严，若没有足够理由，不要把实例或类变量声明为公有。通常，实例变量无需显式的设置(set)或获取(gotten)，通常这作为方法调用的边缘效应(side effect)而产生。

一个具有公有实例变量的恰当例子，是类仅作为数据结构，没有行为。
<br>1） 如果不允许外部直接通过new来创建对象，那么构造方法必须是private。
<br>2） 工具类不允许有public或default构造方法。
<br>3） 类非static成员变量并且与子类共享，必须是protected。
<br>4） 类非static成员变量并且仅在本类使用，必须是private。
<br>5） 类static成员变量如果仅在本类使用，必须是private。
<br>6） 若是static成员变量，必须考虑是否为final。
<br>7） 类成员方法只供类内部调用，必须是private。
<br>8） 类成员方法只对继承类公开，那么限制为protected。
<br><span style="color:orange">说明</span>：任何类、方法、参数、变量，严控访问范围。过于宽泛的访问范围，不利于模块解耦。思考：如果是一个private的方法，想删除就删除，可是一个public的service成员方法或成员变量，删除一下，不得手心冒点汗吗？变量像自己的小孩，尽量在自己的视线内，变量作用域太大，无限制的到处跑，那么你会担心的。

**【强制】引用类变量和类方法(Referring to Class Variables and Methods)**

避免用一个对象访问一个类的静态变量和方法。无谓增加编译器解析成本，直接用**类名**来访问即可。

**常量(Constants)**

位于for循环中作为计数器值的数字常量，除了-1、0和1之外，不应被直接写入代码。

**将局部变量的作用域最小化**

最有力的方法是在第一次使用它的地方声明变量，但结合【代码风格 -> 声明 -> 布局】这一节，实际上应该灵活处理变量声明的位置。

如下这种情况在代码块的开始处将具有关联性的变量集中声明比较好：

```java
function getDimension() {
  int width = 0;
  int height = 0;
  
  //这里计算宽度
  ......
  
  
  //这里计算高度
  ......
  
  //返回值
  return ......;
}
```

如下这种情况在第一次使用它的地方声明变量比较好：

```java
function validateData() {
  boolean isSameDataExist = false;
  
  //验重
  ......
  
  if (isSameDataExist) {
  
  }
  
  boolean isExpiry = false;
  //验证有效期
  ......
  
  if (isExpiry) {
  
  }
  
  return true;
}
```

**变量赋值(Variable Assignments)**

避免在一个语句中给多个变量赋相同的值。它很难读懂。例如：

```java
fooBar.fChar = barFoo.Ichar = 'c'; //避免这样！
```

不要使用内嵌(embedded)赋值运算符试图提高运行时的效率，这是编译器的工作。例如：

```java
d = (a = b + c) + r; //避免这样！
```

应该写成

```java
a = b + c;
d = a + r;
```

**圆括号(Parentheses)**

一般而言，在含有多种运算符的表达式中使用圆括号来避免运算符优先级问题，是个好方法。即使运算符的优先级对你而言可能很清楚，但对其他人未必如此。你不能假设别的程序员和你一样清楚运算符的优先级。

```java
if (a == b && c == d) //避免这样！
  
if ((a == b) && (c == d)) //推荐这样
```

**为switch语句的每一个case加上break**

如果不是特殊原因(多个case对应同一结果)，应该为switch语句的每一个case都加上break。

**返回值(Returning Values)**

设法让你的程序结构符合目的。例如：

```java
if (booleanExpression) {
  return true;
}
else {
  return false;
}
```

应该代之以如下方法：

```java
return booleanExpression;
```

类似地：

```java
if (condition) {
  return x;
}
return y;
```

应该写做：

```java
return (condition ? x : y);
```

**条件运算符"?"前的表达式(Expressions before '?' In the Conditional Operator)**

如果一个包含二元运算符的表达式出现在三元运算符"?:"的"?"之前，那么应该给表达式添加上一对圆括号。例如：

```java
(x >= 0) ? x : -x;
```

**特殊注释(Special Comments)**

在注释中使用XXX来标识某些未实现(bogus)的但可以工作(works)的内容。用FIXME来标识某些未实现(bogus)的且不能正常工作(broken)的内容。

**空引用判断**

- 对于方法传入参数，需要进行必要的空引用判断。

- 获取配置信息时，进行空引用判断，建议获取配置值方法提供返回默认值方法：

  例如：

```java
//获取配置项为空，使用初始值为默认值，防止因没有配置项而抛空引用异常
channelId = clientContext.params.getStr(SMPPConstants.BSS_CHANNEL_ID, channelId);
```

- 对List、Array等进行操作时(特别是判断size、length时)先进行空引用判断

  例如：

```java
List subsList = subsDAO.selectSubsList();
if (subsList != null && subsList.size() > 0) {
  ......
}
```

- Map、List等动态集合对象，建议在创建时初始化，在函数返回时若集合为空，返回一个空的对象，而不是null。数组也是如此，返回零长度的数组而不是null。

  例如：若一个查询方法查询的记录数为0时，不要返回null，而是返回一个空的List，因为大家已经习惯获取List时不对它进行空引用判断，而直接遍历它。

**将反复使用的字符串、数字等定义成常量**

- 对于一些所有模块都共用的字符串，定义到公共常量类中去。
- 对于模块内共用的一些字符串，定义到模块内部常量类里面去。
- 不要使用一个常量类维护所有常量，要按常量功能进行归类，分开维护。

**覆盖equals()方法时总要覆盖hashCode()方法**

如果不这样做的话，就会违反Object.hashCode的通用约定，从而导致类无法跟所有基于散列的集合一起正常运行。

且，equals()的结果要和hashCode()保持一致，避免hash算法失效。

**尽量通过接口引用对象**

优先使用接口而不是类来引用对象。如果有合适的接口类型存在，那么对于参数、返回值、变量和域来说，都应该使用接口类型进行声明。

例如：

```java
List<String> nameList = new ArrayList<String>();
```

如果实现类提供了某个特殊功能不是接口通用约定的，且代码中会依赖这个特殊功能，本规则就不适用。

**不使用float和double进行精确数值计算**

float和double只能进行 *<u>较为精确</u>* 的 *<u>快速近似</u>* 的计算，并不能提供 *<u>完全精确</u>* 的结果，尤其不适用于 *<u>货币</u>* 计算，因为它们不能精确地表示0.1或者10的任何其它负次方。

要进行精确计算就使用 *BigDecimal*、*int* 或者*long* 。

**尽量避免在循环体内进行try/catch**

除非逻辑需要或者特殊原因，将try/catch放在循环体外。

**尽量减少不必要的synchronized**

尽量减少不必要的synchronized，如果有必要，也要使得被synchronized包含{...}的操作尽可能少，且同步的对象尽可能小。

**Object的equals方法容易抛空指针异常，应使用常量或确定有值的对象来调用equals。**
<br><span style="color:green">正例</span>："test".equals(object);
<br><span style="color:red">反例</span>：object.equals("test");
<br><span style="color:orange">说明</span>：推荐使用java.util.Objects#equals（JDK7引入的工具类）

避免比较的String对象是null而引起空指针异常。

```java
String orgName = orgDAO.selName();
if (orgName.equals(CN_NJ)) { //可能引发NullPointerException，避免这样！
  
}

if (orgName != null && orgName.equals(CN_NJ)) { //OK，但是代码不简洁
  
}

if (CN_NJ.equals(orgName)) { //安全又简洁，推荐这样！
  
}
```

**调用String.subString()时先进行长度判断**

避免引起IndexOutOfBoundsException异常。

**将数据库表数值类型主键对应的属性定义成Long类型**

数据库表数值类型主键一般为NUMBER(6)或者NUMBER(9)，当是后者时，如果主键值足够大，会超出Integer能够表示的范围，所以要求统一使用Long来定义对应的属性。

**不要使用MD2、MD4、MD5算法**

由于MD2、MD4、MD5已被认为是不安全的hash算法，因此应禁止使用它们。建议使用SHA256来对密码进行hash处理。

对于非加密的场景，例如仅用于后台使用、构造hash环，可以例外处理。

**使用框架封装的HttpClient请求网络资源**

网络请求时如果没有设定超时时间会导致长时间的等待，引发严重故障。通常我们通过 Apache HttpClient 组件来请求网络资源，该组件提供了SDK用于设置超时时间，参考代码如下：

```java
CloseableHttpClient httpClient = HttpClients.createDefault();

RequestConfig requestConfig = RequestConfig.custom()

			.setSocketTimeout(1000)

			.setConnectTimeout(1000)

			.build();


HttpGet httpGet = new HttpGet("http://localhost/1");

httpGet.setConfig(requestConfig);

CloseableHttpResponse response = httpClient.execute(httpGet, context);

try {

	HttpEntity entity = response.getEntity();

} 
finally {

	response.close();

}


HttpGet anotherHttpGet = new HttpGet("http://localhost/2");

CloseableHttpResponse anotherResponse = httpClient.execute(anotherHttpGet, context);

try {

	HttpEntity anotherEntity = anotherResponse.getEntity();

} 
finally {
  anotherResponse.close();
}
```

通常我们要关注以下3个超时时间：

- http.socket.timeout：套接字超时时间，默认0表示无限期等待。

- http.connection.timeout：建立连接超时时间，默认0表示无限期等待。

- http.connection-manager.timeout：从连接池获取连接的等待时间，默认0表示无限期等待。

  如果没有设置超时时间，线程会一直阻塞，引发故障。为此框架进行了简单的封装，屏蔽了超时时间的设置细节，同时提供了默认值。

  发送GET请求：HttpRequestGet

  发送POST请求：HttpRequestPos

**默认超时配置：**

```java
ftf.httpclient.socket-timeout=2000
ftf.httpclient.connection-timeout=6000
```

**参考样例：**

```java
HttpRequestGet httpRequestGet = new HttpRequestGet();

Map<String, Object> params = new HashMap<>();

params.put("BIZ_P_0","0");

params.put("ftf.httpclient.socket-timeout", 2000);

params.put("ftf.httpclient.connection-timeout", 6000);

httpRequestGet.execute("https://xxx.xxx.xxx/s", params);
```

> 参考：https://hc.apache.org/httpcomponents-client-ga/tutorial/html/index.html

**内存数据库的事务应当优先提交**

当在一个全局事务中有访问多数据库的业务需要时，内存数据库的DML操作应当被放在事务的最后。同时，在最终事务提交(commit)时内存数据库连接应当被优先处理，以此来保证避免产生内存数据库长事务。(常见内存数据库如：Times ten、QMDB等)

**建议：返回boolean值的方法，方法名能够明确表示检验结果，避免只是一个检查动作的说明**

比如checkMptClubMember就没有明确表示结果，方法名不能帮助直观的理解返回true和false分别代表什么含义，而isMptClubMember则是更好的命名方式。

**强制：用户输入的SQL参数严格使用参数绑定或者METADATA字段值限定，防止SQL注入，禁止字符串拼接SQL访问数据库**

注意：ZSMART V8 框架针对like和in的宏处理方式是采用的SQL字符串拼接的方式，会产生硬解析。细节和规避方案：http://10.45.5.222:9050/svn/Product_Documentation/02_解决方案/ZSmart_FTF_R9.0/03.学习总结/框架中LIKE与IN注入风险.docx

**强制：不能将静态变量赋值给局部变量**
静态变量作为进程内共享的状态，全局可见，如果赋值给局部变量，对这个局部变量进行操作会产生全局影响，破坏了局部变量的约定。

**强制： 所有的覆写方法，必须加@Override注解。**
<br><span style="color:orange">说明</span>：getObject()与get0bject()的问题。一个是字母的O，一个是数字的0，加@Override可以准确判断是否覆盖成功。另外，如果在抽象类中对方法签名进行修改，其实现类会马上编译报错。

**强制： 相同参数类型，相同业务含义，才可以使用Java的可变参数，避免使用Object。**
<br><span style="color:orange">说明</span>：可变参数必须放置在参数列表的最后。（提倡同学们尽量不用可变参数编程）
<br><span style="color:green">正例</span>：

```java
public User getUsers(String type, Integer... ids) {...} 
```

**强制：外部正在调用或者二方库依赖的接口，不允许修改方法签名，避免对接口调用方产生影响。接口过时必须加`@Deprecated`注解，并清晰地说明采用的新接口或者新服务是什么。**

**强制：不能使用过时的类或方法。**
<br><span style="color:orange">说明</span>：java.net.URLDecoder 中的方法decode(String encodeStr) 这个方法已经过时，应该使用双参数decode(String source, String encode)。接口提供方既然明确是过时接口，那么有义务同时提供新的接口；作为调用方来说，有义务去考证过时方法的新实现是什么。

**强制：浮点数之间的等值判断，基本数据类型不能用==来比较，包装数据类型不能用equals 来判断**
<br><span style="color:orange">说明</span>：浮点数采用“尾数+阶码”的编码方式，类似于科学计数法的“有效数字+指数”的表示方式。二进制无法精确表示大部分的十进制小数，具体原理参考《码出高效》
<br><span style="color:red">反例</span>：

```java
float a = 1.0f - 0.9f;
float b = 0.9f - 0.8f;
if (a == b) {
    // 预期进入此代码快，执行其它业务逻辑
    // 但事实上 a==b 的结果为 false
}
Float x = Float.valueOf(a);
Float y = Float.valueOf(b);
if (x.equals(y)) {
    // 预期进入此代码快，执行其它业务逻辑
    // 但事实上 equals 的结果为 false
}
```

<br><span style="color:green">正例</span>：

```java
(1) 指定一个误差范围，两个浮点数的差值在此范围之内，则认为是相等的。
float a = 1.0f - 0.9f;
float b = 0.9f - 0.8f;
float diff = 1e-6f;
if (Math.abs(a - b) < diff) {
    System.out.println("true");
}
(2) 使用 BigDecimal 来定义值，再进行浮点数的运算操作。
BigDecimal a = new BigDecimal("1.0");
BigDecimal b = new BigDecimal("0.9");
BigDecimal c = new BigDecimal("0.8");
BigDecimal x = a.subtract(b);
BigDecimal y = b.subtract(c);
if (x.equals(y)) {
    System.out.println("true");
}
```

**强制：所有的相同类型的包装类对象之间值的比较，全部使用equals方法比较。(浮点数的包装类除外)**
<br><span style="color:orange">说明</span>：对于Integer var = ?  在-128至127范围内的赋值，Integer对象是在IntegerCache.cache产生，会复用已有对象，这个区间内的Integer值可以直接使用==进行判断，但是这个区间之外的所有数据，都会在堆上产生，并不会复用已有对象，这是一个大坑，推荐使用equals方法进行判断。

**强制：定义数据对象 DO 类时，属性类型要与数据库字段类型相匹配。**
<br><span style="color:red">反例</span>：某个案例的数据库表 id 字段定义类型 bigint unsigned，实际类对象属性为 Integer，随着 id 越来越大，超过 Integer 的表示范围而溢出成为负数。
<br><span style="color:green">正例</span>：数据库字段的 bigint 必须与类属性的 Long 类型相对应。

**强制：为了防止精度损失，禁止使用构造方法 BigDecimal(double) 的方式把 double 值转化为 BigDecimal 对象。**
<br><span style="color:orange">说明</span>：BigDecimal(double)存在精度损失风险，在精确计算或值比较的场景中可能会导致业务逻辑异常。如：BigDecimal g = new BigDecimal(0.1f); 实际的存储值为：0.10000000149
<br><span style="color:green">正例</span>：优先推荐入参为 String 的构造方法，或使用 BigDecimal 的 valueOf 方法，此方法内部其实执行了Double 的 toString，而 Double 的 toString 按 double 的实际能表达的精度对尾数进行了截断。

```java
BigDecimal recommend1 = new BigDecimal("0.1");
BigDecimal recommend2 = BigDecimal.valueOf(0.1);
```

**关于基本数据类型与包装数据类型的使用标准如下：**
<br>1） 【强制】所有的POJO类属性必须使用包装数据类型。
<br>2） 【强制】RPC方法的返回值和参数必须使用包装数据类型。
<br>3） 【推荐】所有的局部变量使用基本数据类型。
<br><span style="color:orange">说明</span>：POJO类属性没有初值是提醒使用者在需要使用时，必须自己显式地进行赋值，任何NPE问题，或者入库检查，都由使用者来保证。
<br><span style="color:green">正例</span>：数据库的查询结果可能是null，因为自动拆箱，用基本数据类型接收有NPE风险。
<br><span style="color:red">反例</span>：比如显示成交总额涨跌情况，即正负x%，x为基本数据类型，调用的RPC服务，调用不成功时，返回的是默认值，页面显示为0%，这是不合理的，应该显示成中划线。所以包装数据类型的null值，能够表示额外的信息，如：远程调用失败，异常退出。

**强制：定义DO/DTO/VO等POJO类时，不要设定任何属性<span style="color:blue">默认值</span>。**
<br><span style="color:red">反例</span>：POJO类的gmtCreate默认值为new Date();但是这个属性在数据提取时并没有置入具体值，在更新其它字段时又附带更新了此字段，导致创建时间被修改成当前时间。

**强制：序列化类新增属性时，请不要修改serialVersionUID字段，避免反序列失败；如果完全不兼容升级，避免反序列化混乱，那么请修改serialVersionUID值。**
<br><span style="color:orange">说明</span>：注意serialVersionUID不一致会抛出序列化运行时异常。

**强制：构造方法里面禁止加入任何业务逻辑，如果有初始化逻辑，请放在init方法中。**
<br><span style="color:orange">说明</span>：框架在调用属性 xxx 的提取方法时，并不能确定哪个方法一定是被优先调用到。

**强制：POJO类必须写toString方法。使用IDE中的工具：source> generate toString时，如果继承了另一个POJO类，注意在前面加一下super.toString。**
<br><span style="color:orange">说明</span>：在方法执行抛出异常时，可以直接调用POJO的toString()方法打印其属性值，便于排查问题。

**强制：禁止在 POJO 类中，同时存在对应属性 xxx 的 isXxx()和 getXxx()方法。**

**推荐：使用索引访问用String的split方法得到的数组时，需做最后一个分隔符后有无内容的检查，否则会有抛IndexOutOfBoundsException的风险。**
<br><span style="color:orange">说明</span>：

```java
String str = "a,b,c,,";  
String[] ary = str.split(",");  
// 预期大于3，结果是3 System.out.println(ary.length);
```

**推荐：当一个类有多个构造方法，或者多个同名方法，这些方法应该按顺序放置在一起，便于阅读，此条规则优先于下一条规则。**

**推荐：类内方法定义的顺序依次是：公有方法或保护方法 > 私有方法 > getter/setter方法。**
<br><span style="color:orange">说明</span>：公有方法是类的调用者和维护者最关心的方法，首屏展示最好；保护方法虽然只是子类关心，也可能是“模板设计模式”下的核心方法；而私有方法外部一般不需要特别关心，是一个黑盒实现；因为承载的信息价值较低，所有Service和DAO的getter/setter方法放在类体最后。

**推荐：setter方法中，参数名称与类成员变量名称一致，this.成员名 = 参数名。在getter/setter方法中，不要增加业务逻辑，增加排查问题的难度。**
<br><span style="color:red">反例</span>：

```java
public Integer getData() {  
    if (condition) {  
      return this.data + 100;  
    } else { 
      return this.data - 100; 
    }  
}
```

**推荐：final可以声明类、成员变量、方法、以及本地变量，下列情况使用final关键字：**
<br>1） 不允许被继承的类，如：String类。
<br>2） 不允许修改引用的域对象，如：POJO类的域变量。
<br>3） 不允许被重写的方法，如：POJO类的setter方法。
<br>4） 不允许运行过程中重新赋值的局部变量。
<br>5） 避免上下文重复使用一个变量，使用final描述可以强制重新定义一个变量，方便更好地进行重构。

**【推荐】在JDK17以上，使用封闭类（Sealed Classes）来限制类的继承，提高代码的安全性和可维护性。**

**正例：**

```java
public sealed class Shape permits Circle, Rectangle, Square {}

public final class Circle extends Shape {}
public final class Rectangle extends Shape {}
public abstract class Square extends Shape {}
```

【说明】封闭类可以指定哪些其他类可以继承它，有助于避免不相关的类继承导致的代码混乱。

**推荐：慎用Object的clone方法来拷贝对象。**
<br><span style="color:orange">说明</span>：对象的clone方法默认是浅拷贝，若想实现深拷贝需要重写clone方法实现属性对象的拷贝。

**【推荐】在JDK15以上，推荐使用字符串文本块（Text Blocks）来编写多行字符串，提高代码的可读性和维护性。【说明】字符串文本块通过三个双引号（"""）包围，允许字符串跨多行而无需转义。**

**正例：**

```java
String json = """
                {
                  "url": "http://127.0.0.1:8444/emergency/recovery/packageconfigurationerror/confirmCostAccuracy", 
                  "data": {},
                  "output_instructions": ""
                }
                """;
```

# 常见不良习惯（Common Bad Practices）

这一章列出的是应该避免的写法。

## 过于庞大的类、函数

对于逻辑较复杂的代码，建议重构，对代码进行逻辑划分，分散到多个类/函数中去，提高代码复用，避免代码冗余。

建议一个文件里的代码不超过1500行。

对于函数要尽可能限制其大小，尽量不要超过200行；对于特别复杂的逻辑，比如某个语句块{...}跨越了一屏幕的大小，应在 } 后注明其起始语句。

## 代码里出现System.out和printStackTrace

如果不是特殊原因，应该使用封装的Logger来输出各种信息，而不是使用System.out和printStackTrace。

## 空try/catch/finally语句块

如果不是特殊情况，不要在捕获异常后什么都不做。同样，不要写一个空的finally块。

## 定义从未使用的局部变量、参数、私有方法

如果不是特殊原因，不要定义从未使用的局部变量、参数、私有方法。如果以后可能会使用到，可以先注释掉，并加以说明。

## 使用 "==" 或 "!=" 进行字符串比较

非常常见的低级错误，特别是在同时写JavaScript和Java时，很容易犯这个错误。

## 在条件判断表达式里面使用 "=" 进行相等比较

这是个比较隐蔽的错误，例如：

```java
if (willDelete = true)
  
while (isEnd = false)
```

## 方法没有关闭流、数据库连接

数据库连接一般由框架管理，问题会少些。但是文件读写、网络通信时一定要正确、安全地关闭流。必须在finally块中处理。

## 调用静态的Calendar、DateFormat

以SimpleDateFormat为例，代码经常创建一个静态全局的SimpleDateFormat实例供所有线程使用它的format方法，而实际上SimpleDataFormat的format方法是非线程安全的，这样使用会出现问题。除SimpleDateFormat类外，还有不少 XXXFormat类、XXXCalendar类等对应方法都是非线程安全的。

## 未检测的类型转换

在进行类型转换前应当先检测期待的数据类型。

## 数据类型转换导致溢出或者损失精度

在进行数据类型转换时，必须谨慎对待可能的溢出和精度损失问题。为了避免这些问题，通常可以采取以下措施：
1. **类型检查**：在转换前检查值是否在目标类型的范围内，例如将一个超出 `int` 范围的 `long` 类型数值转换为 `int` 类型时，会发生溢出。
2. **使用合适的数据类型**：根据应用场景，选择能够满足需求的数据类型，避免不必要的转换。
3. **使用高精度数据类型**：在需要高精度计算时，尽量使用 `BigDecimal` 或者其他高精度类型。

## 写换行符时使用"\\n"

写文件时经常需要写入换行符，应该使用System.getProperty("line.separator")以兼容不同的操作系统，而不是直接写"\\n"。

注：

- \n Linux/Unix以及部分新版本Mac OS下文本换行符
- \r Mac OS 下文本换行符
- \r\\n Windows 下文本文件换行符

## 内外层循环使用相同的遍历变量

```java
for (int i=0; i\<list1.size(); i++){
	for( i=0; i\<list2.size(); i++){
		// do something…
	}
}
```

## 避免在循环体内对队列进行remove操作

避免在循环体内部直接把队列值给remove掉，这样的方式可能跟我们正常处理逻辑的思路有偏差。建议循环体内部处理时用新copy 的队列进行实际的处理。

## 避免变量在使用前被另一个赋值覆盖(Unused assignment)

此项检查指出了变量值在赋值后从不使用的情况，即：

- 变量在赋值后从不被读取
- 值总是在下一个变量读取前被另一个赋值覆盖
- 变量初始值设定项是冗余的（出于上述两个原因之一）

**<font color="red">反例</font>**

```java
public class UnusedAssignmentDemo {
    private static final ZSmartLogger LOGGER = ZSmartLogger.getLogger(UnusedAssignmentDemo.class);
    public static void main(String[] args) {
        String greeting;
        if ("1".equals(String.valueOf(3 - 2))) {
            // 下面一行的赋值会被后面的赋值覆盖，要避免这样
            greeting = "This line is unused Assignment!";
        }
        greeting = "Hello world!";
        LOGGER.debug(greeting);
    }
}

```

## 禁止使用字符串或者数字运算的方式处理日期

对日期的处理应当使用成熟的工具包，例如 java.util.Calendar ,org.apache.commons.lang3.time.DateUtils ,禁止使用自定义算法，避免由于没有充分考虑夏令时或者闰年因素导致的问题。
例如：因为2000年是闰年，所以2000/02/29是一个合法的日期，如果增加一年，通过年份增加再拼接的方式会得到
2001/02/29，这是一个非法的日期，在某些场景下会导致解析失败。

**正例**

```java
int year = 2000;
// 月份从0开始计算，month = 1 表示 2月
int month = 1;
int date = 29;
int yearAmount = 1;
calendar = Calendar.getInstance();
calendar.set(year,month,date);
Date yearAmountDate = DateUtils.addYears(calendar.getTime(), yearAmount);
```

# 性能优化 (Performance Optimization)

## 内存管理

### 尽早释放无用对象的引用

一般情况下都是让对象在退出活动域（scope）后自动设置成null被回收，但对一些复杂的对象，例如数组、队列、树等，可能存在较为复杂的引用关系，GC回收效率一般较低，尽早将其赋值为null可以加速内存回收。

### 尽量避免在循环体内创建对象

除非特殊情况，默认定义在循环外面：

```java
DynamicDict supServiceBO = null;//推荐这样
for (int i = 0; i <size; i++) {
    supServiceBO = (DynamicDict) supServiceList.get(i);
    ......
}

for (int i = 0; i <size; i++) {//不推荐这样
    DynamicDict supServiceBO = (DynamicDict) supServiceList.get(i);
    ......
}
```

### 尽量少用finalize函数

finalize函数会加大GC工作量。

### 尽量避免强制内存回收（System.gc()）

这会增加系统内存回收的最终时间，降低系统性能。

### 尽量避免在类的构造器中创建、初始化大量对象

主要是为了避免在调用其子类的构造器时造成不必要的内存消耗。

### JDBC结果集大小应当加以限制

> :warning: 故障警示! 严重生产故障：[3713022](https://zmp.iwhalecloud.com/hppd/queryFauDtl.action?faultId=3713022)。某项目应用一次性加载了超400万的结果集，引发了OOM，导致核心业务积压。

默认情况JDBC不限制返回的结果集大小，这可能会导致内存波动，严重时甚至出现内存溢出(OOM)的现象。可以采用SQL的LIMIT子句(MySQL)或rownum子句(Oracle)限定行数的最大值，也可以通过数据访问框架提供的能力加以限制。

例如：

- Spring JdbcTemplate的 setMaxRows方法

  (参考: https://docs.spring.io/spring-framework/docs/3.2.0.M1_to_3.2.0.M2/Spring%20Framework%203.2.0.M2/org/springframework/jdbc/core/JdbcTemplate.html#setMaxRows(int))

- ZSmart CORE (R9) 框架的 ftf.sql.limit-result-set=150

  (参考: http://ftf-r9-coredocuments.ftf.svc.tb.zsmart.com/07/Development_Specification/06/)

- ZSmart CORE (V8) 框架的 db_fetch_limit

  (参考: ZSMART_HOME/etc/defined/system.def)

### 避免将过大的文件一次性加载到内存中

> :warning: 故障警示! 严重生产故障：[3695958](https://zmp.iwhalecloud.com/hppd/queryFauDtl.action?faultId=3695958)。某项目应用因为处理大文件时，将整个文件读取到内存中的 List 导致内存占用过高，引发订单处理性能下降的严重生产故障。

在处理文件时，应预先检查文件的大小，避免将过大的文件一次性加载到内存中。建议设置一个合理的文件大小阈值，具体的阈值应根据应用场景和服务器配置进行调整。

如果不可避免有超大文件的处理场景，应采用流式处理方式，逐行或分块读取文件内容，避免一次性将整个文件加载到内存中。同时在文件处理过程中，应妥善处理可能发生的异常情况，如文件读取失败、内存溢出等，并提供相应的错误日志和恢复策略。在文件处理完成后，应及时释放相关资源，如关闭文件流、释放缓存等，以避免资源泄露。在开发过程中，应对文件处理功能进行性能测试，确保在处理大文件时系统的性能和稳定性。在用户界面上，应提供明确的提示信息，告知用户文件大小的限制，并在用户尝试上传或处理超过限制的文件时给予警告。

### 确保 SQL 拼装时查询条件有效性，避免大表扫描

> :warning: 故障警示! 严重生产故障：3544304、31154605。国际与国内项目均出现过因 SQL 拼装时查询条件处理不当，致使全表扫描、慢 SQL，甚至内存溢出的严重生产故障，虽实现机制有所差异，但故障现象一致。

在使用数据持久化框架（如：Mybatis、或者国际V8 CORE的SQL服务）时，若涉及拼装 SQL 语句：
1. 针对使用了一个或多个条件参数的场景，务必提前考量所有条件参数均不生效的状况，因为这极有可能引发对大表的全表扫描，或是产生超大结果集，最终导致内存溢出等生产事故。开发人员需要进行严谨的测试与验证，模拟各种条件参数的组合情况，确认是否存在潜在风险。
2. 倘若仅有一个参数，且该参数为必传参数，切勿将其设置为条件参数。这种做法能从根源上杜绝因参数缺失而导致意外全表查询的隐患。

在代码评审环节，需着重关注此类 SQL 拼装代码；单元测试用例也应覆盖各种条件参数的生效与失效场景，以此保障代码质量，避免出现类似的性能瓶颈与故障，维护系统稳定高效运行。

## 集合类

### 不涉及多线程同步问题时，尽量选用非线程安全的集合类

在多线程的环境下使用线程安全的集合类（例如Vector）代码会比较简洁、安全；但是不涉及多线程同步问题时，使用非线程安全的集合类（例如ArrayList）会具有更好的性能。

### ArrayList和LinkedList

在列表中进行随机查找，使用ArrayList速度更快；在列表任意位置进行插入、删除，使用LinkedList速度更快。
优先使用ArrayList，然后再考虑使用LinkedList。但如果预先可以知道数据大小，则尽量使用数组。

### 设置ArrayList的初始化容量

在处理已知容量的较大数组时，尽量提前调用ensureCapacity()方法设置ArrayList的容量，可以避免ArrayList自动扩容带来的性能消耗。

### 应用泛型

在集合类中存取数据时往往需要进行强制类型转换，而应用泛型后类型转换从运行期转移到了编译期，为较大的性能优化带来了可能。

## String的优化

### 字符串连接

* 对于一次性初始化且后面不需要修改的较长字符串**直接使用**+操作符连接。例如：

```java
String tag = "a" + "b" + "c"; //这样是OK的
```

* 对于中间夹有变量的、需要动态连接的字符串，尤其是在循环内部连接字符串或者存在大量的连接操作时，**必须使用**StringBuilder或者StringBuffer而不是+操作符。使用+操作符进行大量的连接操作会非常慢。

```java
String tag = "a" + varB + "c"; //避免这样！
    String text = "";
for(int i=0; i<size; i++){
    	text += …………; //避免这样
}
```

Java 1.5发行版本中新增加了非同步的StringBuilder类，用于补充同步的StringBuffer类，在多线程环境下推荐使用StringBuffer类。一般情况下两者性能差异不大，在100万次循环下，StringBuilder也只快了几十毫秒。

PS:注意的是**不要混用** StringBuilder/StringBuffer 和+操作符：

```Java
StringBuilder builder = new StringBuilder(10);
for(int i=0; i<size; i++) {
                                                                                                                     builder.append("line " + i);			//避免这样
                                                                                             builder.append("line ").append(i);		//推荐这样
}
```

<span style="color:orange">说明</span>：反编译出的字节码文件显示每次循环都会new出一个StringBuilder对象，然后进行append操作，最后通过toString方法返回String对象，造成内存资源浪费。

### 优先使用toCharArray()遍历字符

可以使用charAt()方法取得某个特定位置的字符。但若想遍历所有字符，通过toCharArray()方法先取得字符数组，在对数组进行遍历会有更好的性能。

### 字符串转化为数字

将字符串转化为数字类型是比较耗时的，例如将”3.67”转换成Double。尽量直接将数字转换成数字类型：

```java
Double d = new Double("3.67"); //避免这样
Double d = new Double(3.67); //优先这样
```

一个基本原则是：如果其它类型更适合，尽量避免使用字符串

### 避免重复创建字符串对象

重复使用同一个对象，而不是重复创建。如果一个对象是非可变的对象，那么它总是可以被重用。例如：

```java
String str = new String("Hello")； //避免这样
String str = "Hello"; //而是这样
```

## 系统I/O

### 通过缓冲流类提高I/O操作效率

* 采用默认的数据I/O方式（直接读取/写入）会导致系统性能下降
* 采用系统数据缓冲流类读取/写入数据将会提升系统性能
* 采用自定制合理缓冲区读取/写入数据将会更大程度地提升系统性能

# RESTful接口开发规范

## 设计要求

### 一切皆资源

所有要给API操作的对象都只能是资源 **（Resource）** 。不管实际上存在的，还是抽象上的。所有资源都会有一个不变的标识（ID），对资源的任何API操作都不应该改变资源的标识。资源和其他资源会有关系，资源与资源的关系通过资源的标识来引用。
资源所指的并不是数据，而是数据+特定的表现形式（representation），这也是为什么REST的全名是Representational State Transfer的原因。举个例子来说，“本月卖得最好的10本书”和“你最喜欢的10本书”在数据上可能有重叠（有一本书即卖得好，你又喜欢），甚至完全相同。但是它们的representation不同，因此是不同的resource。

### 使用标准的HTTP方法

![image](uploads/4077/c79226c6-9f23-430c-b367-300a866d31d5/352d0e75d97042589be1625491a3a90c.png)
Rest提出的要求是，对资源的操作都应该是统一的，不管是操作哪种类型的资源，API都应该是一致的。这样当调用API的客户端知道某种资源的时候，它不需要去学习对这个资源该怎么操作，因为对所有资源的操作都是一致的，它们都应该支持CRUD操作，以及一些其他操作，比如list（用来查找，或者列出所有资源）。

### 规范URL的使用

#### URI的设计应该遵循可寻址性原则

具有自描述性，需要在形式上给人以直觉上的关联。下面是一些例子：

```properties
GET /zoos：列出所有动物园
POST /zoos：新建一个动物园
GET /zoos/1：获取某个指定动物园的信息
PUT /zoos/1：更新某个指定动物园的信息（提供该动物园的全部信息）
PATCH /zoos/1：更新某个指定动物园的信息（提供该动物园的部分信息）
DELETE /zoos/1：删除某个动物园
GET /zoos/1/animals：列出某个指定动物园的所有动物
DELETE /zoos/1/animals/2：删除某个指定动物园的指定动物
```

#### 使用名词而不是动词

**正例**

```properties
GET /cars
DELETE /cars/911
PUT /cars/911
POST /cars
```

**<font color="red">反例</font>**

```properties
GET /getAllCars
DELETE /deleteAllCars
```

#### 使用/来表示资源的层级关系

例如

```properties
GET /zoos/1/animals：列出某个指定动物园的所有动物
GET /blog/345/reply/456：这个博客的标识是345，获取博客的某个回复
```

#### 参数传递

有三种方式可以将参数传给API操作：
第一种是通过URL的地址传递，如前面的例子中把标识放在URL里；

```properties
GET /zoos/1/animals
```

第二种是通过URL的参数，比如，对于一个查找请求，可以把查找的过滤条件放在参数里；

```properties
GET /zoos/1/animals?sortOrder=asc&sortField=age&fields=name,age`
GET /zoos/1/animals?page=5&pagesize=50`
```

第三种是PUT或者POST请求的时候，把内容放在HTTP body里面；

### 实现请求的无状态

Rest是无状态的。Rest的请求之间不应该有依赖，在调用一个请求前，不需要一定要去提前调用另外一个请求。Rest里面不应该有session，特别是Rest请求不应该保存信息在session里，以便在后面的调用中使用。甚至包括安全验证，客户端不应该需要提前登录，然后把权限信息保存在session里，后面的请求用同一个session来调用。

实现无状态的方法就是，把所有信息都包含在当前的请求中，包括验证信息。HTTP是无状态的，HTTP里有一个Authorization头，HTTP的要求是在每次请求的时候都把验证信息放在里面，服务器每次处理请求前都去验证这个信息。为了安全，我们可以提供一个生成token的Rest
API，客户端调用这个API生成token（可以附上用户名/密码来生成token）。在后面的所有请求中都把这个token放在Authentication头中。

## 编程惯例(Programming Practices)

**这一章列出的是推荐的写法。**

### Rest API的URL，采用小写开头的驼峰命名法。

![image](uploads/4077/80e1c8d9-61ce-41c8-a790-bd24933f0afa/0828c07862dae4a7d941c1924344f8f9.png)

### 对于查询接口，通过主键查询和通过过滤条件查询分别对应2个不同的接口。

![image](uploads/4077/74f0f4cf-aee3-4a1a-9c80-250ae64a1c31/0c2c82206d9a729022f77d239f34d6c3.png)

### 更新部分字段属性使用PATCH。

![image](uploads/4077/0199b403-f2c0-4248-99c6-a87bdc3ffcc1/cfdd52410f15982a4fe5f51e876178ff.png)
![image](uploads/4077/5bc0f51e-6391-463d-a367-8dd015a673d1/786f6b0f9497c67a05ec460da8dee3a2.png)

### 更新对象属性的时候，主键要在URL里传递，然后在服务层设置到对象里。

![image](uploads/4077/8bd7ee6d-e864-4c28-ba5e-69b1b59fa08b/799588c5a9810d4d5ce2dce779e2b78f.png)

### 更新对象属性的时候，除非必要，不要在业务逻辑里再查询一次返回完整对象信息。

### 创建对象使用POST方法，数据放到http body里传递。

![image](uploads/4077/d7adc15e-e771-427e-b0cd-3e7e3402c0f3/cc3b0122960bc2c26b8171cfe4920ab5.png)

### 删除操作统一返回受影响行数。

![image](uploads/4077/09f1a880-c9f4-467e-85c2-d22aea0266d9/63cd5c08c0196c624de3f7abb1ded8e5.png)

### 如果有层级关系，父级的id必须传入，后台代码和SQL中也要使用，使用父级资源和自己的id来唯一确定当前的资源。

![image](uploads/4077/7a319638-3743-458c-a2f6-11f4e60c3ad0/25e7159970d90a6746787faf48f23168.png)

### 主键应该通过URL地址传递，其他参数通过URL参数传递。

Controller层通过注解的方式来获取参数

```
@PathVariable 用于获取路径中的内容   
@RequestParam 用于获取请求参数的内容，如果Controller层使用对象映射字段的话，也可不加该注解
@RequestBody  用于获取HTTP body里面内容
```

![image](uploads/4077/dd32b82b-7be7-41a7-8db0-4d50b41f218e/a7351e7663f2a3d84a0514d57ba42386.png)
![image](uploads/4077/5b6d0ae9-ba56-4a7b-bb7d-8feecf0fd3b2/789f16126a6ced2f66c18491acaf7270.png)
![image](uploads/4077/dafe27a9-aa42-4dd6-858d-719fe009fd9b/646e95e9213027256c766e815f716a09.png)

### 重复性校验尽量使用查询接口，查询无数据即校验通过。

### Controller接口建议使用注解给接口方法和参数添加说明，方便通过swagger来查看具体接口

```
常用注解如下：
    @Api(description = "接口类Controller描述")
    @ApiOperation(value = "接口方法说明")
    @ApiParam(required = "是否必须参数", value = "方法参数具体描述")
    @ApiModel(value = "对象描述")
    @ApiModelProperty(value = "对象字段描述")
```

### 保护程序免遭非法输入数据的破坏：需要检查所有来源于外部数据的值和子程序所有输入参数的值

**规则说明：**

《代码大全2》中提到，防御式编程的主要思想是：子程序应该不被传入错误的数据而被破坏，哪怕是由其他子程序产生的错误数据。需要将“垃圾进，垃圾出”缺乏安全性的差劲程序做到“垃圾进，什么都不出”、“进来垃圾，出去时出错提示”或者“不许垃圾进来”。对已形成产品的软件而言：不管进来的数据如何，都不应该产生垃圾数据。

**通常处理垃圾方法：**

对于非法输入数据，至少选择如下一种处理方法，其中当非法输入会导致程序后续无法正常运行时，必须关闭程序。

1. **检查所有来源于外部数据的值**。当从文件、用户、网络或其他外部接口中获取数据时（不限于配置文件、数据文件、网络消息、数据库等外部输入场景），应检查所获得的数据值，严格按照契约进行校验以确保它在允许的范围内。例如整型是不是在可接受范围内，字符串是不是合乎用途，包括企图令缓冲溢出的数据、注入的SQL命令、注入的HTML或XML代码等等。

   **异常数据的建议合理处理方法：**

   * 可立即显示出错信息，把警告信息记录到日志文件中
   * 返回一个错误码。如果和外部有错误约定，就需要返回错误码和错误消息给外部
   * 可以正常处理下一个正确的数据
   * 或调用错误处理子程序或对象集中处理错误
   * 换用最接近的合法值。如果输入数据超出范围时，可以根据值修改为支持的最大值或者最小值。以提高交互的友好性
   * 关闭程序
2. **检查子程序所有输入参数的值**。例如命令行启动参数。

   **异常参数的建议合理处理方法：**

   * 立即显示出错信息，把警告信息记录到日志文件中或者界面上
   * 关闭程序
   * 修改最接近的合法值。如果输入参数超出范围时，可以根据值修改为支持的最大值或者最小值。以提高交互的友好性

## 常见不良习惯 (Common Bad Practices)

**这一章列出的是应该避免的写法。**

### URL使用了动词

![image](uploads/4077/77aa6c5c-6c8e-4624-8469-88ac458a7620/bc43e1b834b0eb3e757826c8bfb58765.png)

### 更新部分属性使用了PUT

![image](uploads/4077/21315cee-d2d6-4d87-b4be-4ea17015f67d/219204567a84f1409594f0cd45bfa3e9.png)

# 浩鲸科技Java开发环境搭建指引

## 安装准备工作

在开始搭建开发环境之前，需要了解下背景，目前公司Java代码规范指定的代码分析工具一共有4种，分别是

- `PMD`：PMD(Programming Mistake Detector)是一种开源分析Java代码错误的工具。与其他分析工具不同的是，PMD通过静态分析获知代码错误。也就是说，在不运行Java程序的情况下报告错误。PMD附带了许多可以直接使用的规则，利用这些规则可以找出Java源程序的许多问题。此外，用户还可以自己定义规则，检查Java代码是否符合某些特定的编码规范。[百度百科](https://baike.baidu.com/item/PMD/23680951)
- `NCSS`：JavaNCSS 是一个开源的度量工具，提供圈复杂度的方法级的值。
- `FindBugs`：FindBugs 是一个静态分析工具，它检查类或者 JAR 文件，将字节码与一组缺陷模式进行对比以发现可能的问题。[百度百科](https://baike.baidu.com/item/FindBugs/4111190?fr=aladdin)
- `SpotBugs`: FindBugs停止维护后的的替代品，规则相比Findbugs更加完整。[官方网站](https://spotbugs.github.io/)
- `CheckStyle`：CheckStyle是SourceForge下的一个项目，提供了一个帮助JAVA开发人员遵守某些编码规范的工具。它能够自动化代码规范检查过程，从而使得开发人员从这项重要，但是枯燥的任务中解脱出来。[百度百科](https://baike.baidu.com/item/Checkstyle)
- `Lizard`：Lizard 是一个可扩展的圈复杂度分析器（Cyclomatic Complexity Analyzer），适用于许多编程语言，包括 Java/C/C++/JavaScript/Python等。[官方网站](https://github.com/terryyin/lizard)

ZCM 持续构建流程已经默认支持这几个代码分析工具，我们需要在本地开发环境将这4个工具搭建起来，以免不符合规范的代码导致持续集成的失败。

![image](uploads/10836/f7d4f91a-f436-4355-a340-a41c46527a78/image.png)

这四个规范检查工具默认提供了一些检查规则，我们对这些规则做了一些本地化的修改，删除了一些不必要的检查规则，以确保检查范围在公司Java编码规范的范围内。大家可以把规则文件[下载](https://docs.iwhalecloud.com/dmz-proxy/cos/share/406/检查工具和规则文件/Java/rules/)到本地，后续在安装工具的过程中引用。

| 组件 | 版本 | 配置文件地址 |
| ---- | ---- | ---- |
| PMD | 5.4.6 |  [https://docs.iwhalecloud.com/dmz-proxy/cos/share/406/检查工具和规则文件/Java/rules/PMD/](https://docs.iwhalecloud.com/dmz-proxy/cos/share/406/检查工具和规则文件/Java/rules/PMD/) |
| JavaNCSS| 33.54.01 | [https://docs.iwhalecloud.com/dmz-proxy/cos/share/406/检查工具和规则文件/Java/rules/JavaNCSS/](https://docs.iwhalecloud.com/dmz-proxy/cos/share/406/检查工具和规则文件/Java/rules/JavaNCSS/) |
| FindBugs | 3.0.1 | [https://docs.iwhalecloud.com/dmz-proxy/cos/share/406/检查工具和规则文件/Java/rules/Findbugs/](https://docs.iwhalecloud.com/dmz-proxy/cos/share/406/检查工具和规则文件/Java/rules/Findbugs/) |
| CheckStyle | 8.3 | [https://docs.iwhalecloud.com/dmz-proxy/cos/share/406/检查工具和规则文件/Java/rules/CheckStyle/](https://docs.iwhalecloud.com/dmz-proxy/cos/share/406/检查工具和规则文件/Java/rules/CheckStyle/) |
| SpotBugs | 4.7.3 | [https://docs.iwhalecloud.com/dmz-proxy/cos/share/406/检查工具和规则文件/Java/rules/SpotBugs/](https://docs.iwhalecloud.com/dmz-proxy/cos/share/406/检查工具和规则文件/Java/rules/SpotBugs/) |

## IDEA 安装 PMD

目前ZCM CI流程静态检查工具中PMD的版本已经升级到5.4.6版本，对应IDEA插件的版本是1.7.7([下载地址](https://plugins.jetbrains.com/plugin/1137-pmdplugin/versions))

![image](uploads/10836/e45c0d2f-177d-47f1-9ab2-3cd0c99dd443/lQLPJxaD8uCU21DNA1XNCFewJ38gHRK-UBgC2UBI5EBUAA_2135_853.png)

下载时，界面会弹出安装向导，参考向导即可轻松完成安装

![image](uploads/10836/57f9d3cd-179e-4157-9152-b497a37c8c03/image.png)
![image](uploads/10836/eb3a37ca-31bf-4a62-a1e8-bb3ed02e6dfe/image.png)

安装完成后，需要重启IDEA生效，重启完成后，在settings 界面可以看到 PMD的配置界面，通过PMD的配置界面添加自定义规则文件(`pmd4.0-ruleset-base.xml`)：

> 如果看不到，说明IDEA版本比较新，可以在plugins页面升级下PMD版本。

![image](uploads/10836/64c340ff-6d8b-4c6e-9add-0c2c9c705c46/image.png)

安装配置完成后，就可以在代码区右击 `Run PMD` 进行代码的检查

![image](uploads/10836/3f37f6a1-6d84-43bd-b028-cd3d6388f9cf/image.png)

## IDEA 安装 NCSS

IDEA没有圈复杂度的插件，所以我们需要借助一些小技巧来实现圈复杂度的检查。

首先将 javancss-33.54.01.zip 解压到本地，打开`IDEA`->`Preference`->`External Tools`，点“`+`”号，创建一个Tool，配置如下：

> 如果遇到` C:\Program' 不是内部或外部命令，也不是可运行的程序或批处理文件。` 的报错，说明JAVA_HOME存在空格，解决完空格即可。或者参考[这篇](https://blog.csdn.net/aitangyong/article/details/49978135)博文解决。

![image](uploads/10836/5711bdef-4ac8-4da3-9f5f-5d33302e7901/image.png)

安装完成后，就可以在代码区域右击 `External Tools` -> `javancss` 进行代码圈复杂度的检查。

![image](uploads/10836/6f0adb3b-c91a-450c-aa75-8f4413da8acd/image.png)
![image](uploads/24587/63db9383-152a-4a3b-a13e-1ea6dd440771/image.png)

- NCSS：Non Commenting Source Statements，除了注释和空行外的java有效代码行数。
- CNN：Cyclomatic Complexity Number (McCabe metric)，函数的圈复杂度，就是if、while、for、catch等逻辑控制语句的分支个数。
- JVDC：Javadoc comments，是否编写了符合javadoc规范的注释。0代表无javadoc，1代表有javadoc。

目前CI要求，方法圈复杂度不超过10，也就是CNN不超过10。

> - java静态代码检查工具：JavaNCSS的使用：[https://blog.csdn.net/aitangyong/article/details/49978135](https://blog.csdn.net/aitangyong/article/details/49978135)
> - 降低圈复杂度的10种重构技术：[https://www.jianshu.com/p/c2e1e304cab2](https://www.jianshu.com/p/c2e1e304cab2)

## IDEA 安装 Lizard

JavaNCSS 最高只支持到JDK1.7，对于类似lambda的新语法规则不支持，导致误报率较高，并且已经停更多年，因此经规范组研究讨论解决启用`Lizard`。

> [Lizard](https://github.com/terryyin/lizard) 是一个可扩展的圈复杂度分析器（Cyclomatic Complexity Analyzer），适用于许多编程语言，包括 Java/C/C++/JavaScript/Python等。

> Lizard 本地使用不是太便利，日常开发时我们可以使用IDEA自带的工具进行检查，启用方法参考下一章节：IDEA 启用圈复杂度检测插件。如果选择继续安装Lizard请继续阅读当前章节。

- 安装 Python
  Lizard 依赖 `python `环境来运行，所以我们首先要安装`python`环境，需要`python`的版本 >= 2.7 , 点击[这里](https://www.python.org/downloads/)下载，下载后点击安装即可。

- 安装 Lizard

```shell
# 安装lizard 1.17.10 版本，与研发云版本保持一致
pip install lizard==1.17.10 
# 安装jinja2，这是一个用于 Python 的模板引擎，lizard 生成html的报告需要依赖这个组件
pip install jinja2
```

- 使用 Lizard

**方法一：直接执行命令**

```shell
lizard D:\code\your-project -m -C 10 -H -o report.html -l java
```

参数说明：
1. 源码路径：D:\code\your-project，lizard 默认递归检测文件夹下的所有文件，如需要指定扫描某个文件可以将该参数替换成具体的文件路径。
2. -m 开启将switch/case语句中多个case统计成一个圈复杂度的开关，保持默认值即可。
3. -C 设置圈复杂度阈值，超过阈值的方法在报告中将展示为告警，保持默认即可。
4. -H -o 设置输出报告并将格式设置为html格式，保持默认即可。
5. -l 设置扫描的方法的语言类型，目前支持以下类型的语言`cpp, java, csharp,javascript, python, objectivec, ttcn, ruby, php, swift, scala, GDScript,go, lua, rust, typescript`，此处我们设置为java即可。

**方法二：执行批处理程序**
我们提供了一个批处理程序，下载[地址](https://docs.iwhalecloud.com/dmz-proxy/cos/download/406/检查工具和规则文件/Java/rules/lizard/run_lizard.bat)，执行这个批处理，按照要求输入需要扫描的代码路径即可在当前路径下生产报表。

```shell
PS C:\Local\Code\> .\run_lizard.bat
Please enter the file path:C:\Local\Code\xxl-job\xxl-job-core
Warning: overriding output file extension.
```

两种方法产生的报表内容完全一致，结果为红色，则表示该方法复杂度不合格。

![image](uploads/46541/d66e74f2-afa8-4bf1-a3cb-cf35166a0e87/image.png)

## IDEA 启用圈复杂度检测插件

IDEA 有一个圈复杂度检测插件，但默认没有开启，开启后，可以实时检测方法的圈复杂度，开启方式 `Settings | Editor | Inspections -> Overly complex method` 。 （不同版本可能路径稍有差异，可以检索下。）

> 建议将级别设置为 Error，阈值设置为 10。

![image](uploads/50498/94e7c414-bc87-470e-95b4-4f9cf4270ced/image.png)

启用后，当方法圈复杂度超过 10 ，IDEA 会现一个错误告警。

![image](uploads/50498/d23d7607-d1fe-45c3-88f7-ff9b308bc701/image.png)

## IDEA 安装 FindBugs

目前FindBugs最新版本是3.0.1，官方在2015年之后就没有更新过，最高支持的IDEA版本是2020.1，所以如果要安装Findbugs-IEDA插件的话，需要确保IDEA的版本低于2020.1，安装步骤很简单，直接在插件市场搜索 `FindBugs-IDEA` 插件，然后install后重启即可。

![image](uploads/24587/ec097628-ff65-4b64-a670-ccfca0bf6b97/image.png)

重启后，重新返回settings 页面，在 Other Settings -> FindBugs-IDEA 的 General-Plugs 区域添加 Find Security Bugs 开启针对安全问题的侦测。

至此就安装配置完成了，可以在代码区域右击 Analysis -> Analysis Code 进行代码漏洞检查。

## IDEA 安装 SpotBugs

Findbugs于2015年3月6日最后一次发布 3.0.1后就不再维护，并且IDEA2020.1版本开始也弃用了Findbug-IDEA插件，所以我们改用SpotBugs。安装过程很简单，在插件市场检索 `SpotBugs`，然后点击 `Install`即可，安装后重启IDEA。
![image](uploads/24587/b667d35f-d48c-459a-a72e-694053e0c6c0/image.png)

重启后，重新返回settings 页面，在 Tools -> SpotBugs 菜单开启 Find Security Bugs插件，这个插件是做安全漏洞检查。
![image](uploads/24587/601e45e5-01c9-45b0-b0d0-ab7a27345db2/image.png)

接下来导入spotbugs的配置，点击import 按钮，选择提前下载好的spotbugs.xml，导入即可。
![image](uploads/24628/4c508083-6a9a-4949-8b8c-ee3b7b441c1b/image.png)

至此就安装配置完成了，可以在代码区域右击 SpotBugs -> Analysis Current File 进行代码漏洞检查。
![image](uploads/24587/7c4b3902-9d1e-4976-848f-6ce89bb79496/image.png)

## IDEA 安装 CheckStyle

目前ZCM 持续集成使用的`CheckStyle8.3`版本，我们还是通过IDEA Settings->Plugin 来安装 CheckStyle-IDEA 插件，安装过程很简单直接install即可，然后重启IDEA。

![image](uploads/10836/a9e70317-cfd8-4078-b71e-fd087087b1e4/image.png)

安装完成后就是配置了，打开settings -> Tools -> CheckStyle 页面，如下图配置，添加自定义的规则文件 `checkstyle8.3-base.xml`：

> 注意：这里选择checkstyle版本不要选错，否则会导致规则文件导入失败，应该是选择`8.3`，不要选成`8.30`！

![image](uploads/10836/7683c2eb-13bc-4e76-97f9-ca77c063e8d4/image.png)

至此就安装配置完成了，可以在代码区域右击进行代码样式的检查。

> 注意要选择我们自己添加的规则文件。

![image](uploads/10836/e03834df-3f59-4e4d-a0f3-42a633b6ed4c/image.png)

## IDEA 安装 Eclipse Code Formatter

CheckStyle 检查出来的代码格式问题，可以通过 code formatter 完成一键格式化，提高效率。

插件安装过程与上文中插件安装方式相同，插件名称：Adapter for Eclipse Code Formatter

![image](uploads/10836/cb56d238-991c-473d-b0b3-31c2cd2d7f93/image.png)

安装完成后，如下图配置即可完成启用，使用快捷方式 `ctrl + alt + L`

![image](uploads/10836/da428605-ff55-41b6-9763-d3725ba61607/image.png)

# FAQ

## Q1：关于 ODR_OPEN_DATABASE_RESOURCE 告警的专项治理说明

### ODR_OPEN_DATABASE_RESOURCE 告警是什么？

`ODR_OPEN_DATABASE_RESOURCE `表示打开了数据库资源（比如 `Connection`, `Statement`），但没有在适当的地方关闭它们，这可能会导致资源泄漏（连接不能复用、内存不能释放），最终可能导致程序运行时资源耗尽或性能问题。

### 哪些数据库资源需要关闭？

* `java.sql.Connection`
* `java.sql.Statement`
* `java.sql.PreparedStatement`
* `java.sql.CallableStatement`

注意: `java.sql.ResultSet` 也需要关闭，虽然不会触发 `ODR_OPEN_DATABASE_RESOURCE `告警，但会触发 `OBL_UNSATISFIED_OBLIGATION `告警。

### 怎么正确关闭数据库资源？

使用 `try-with-resources` 或 `try-finally` 确保在所有场景下都会关闭资源。

使用 `try-finally` 关闭多个资源时应注意捕获关闭资源的异常，避免关闭前面的资源报错导致后面的资源不会关闭。

另外推荐使用上层框架封装好的工具而非直接使用底层的 JDBC 接口，比如 spring-jdbc 的 `JdbcTemplate`, 既能简化代码，又能避免手动管理资源的麻烦。

示例：

  ```java
// try-with-resource, 可以在一个 try 中打开多个资源  try (Connection connection = DriverManager.getConnection(url, username, password);  
     PreparedStatement statement = connection.prepareStatement("SELECT 1");  
     ResultSet rs = statement.executeQuery()) {  
    while (rs.next()) {  
        System.out.println(rs.getInt(1));  
    }  
}  
  
// try-finally, 不推荐使用，资源比较多时很繁琐  Connection connection = null;  
PreparedStatement statement = null;  
ResultSet rs = null;  
try {  
    connection = DriverManager.getConnection(url, username, password);  
    statement = connection.prepareStatement("SELECT 1");  
    rs = statement.executeQuery();  
    while (rs.next()) {  
        System.out.println(rs.getInt(1));  
    }  
}  
finally {  
    // 关闭顺序一般与打开顺序相反    
// 注意需要捕获关闭资源的异常，否则出现异常时后面的资源将不会被关闭    
if (rs != null) {  
        try {  
            rs.close();  
        }  
        catch (Exception e) {  
            // 记录日志    
}  
    }  
    if (statement != null) {  
        try {  
            statement.close();  
        }  
        catch (Exception e) {  
            // 记录日志    
}  
    }  
    if (connection != null) {  
        try {  
            connection.close();  
        }  
        catch (Exception e) {  
            // 记录日志    
}  
    }  
}
```

## Q2：为什么我本地的SpotBugs检查结果和研发云试飞构建的检查结果不一致？

在使用`Analyze Current File`时，默认只能检测出单个当前文件的问题，无法检测出多个文件关联导致的问题，而研发云既检查单个文件，又会检测各文件间关联。所以本地不仅要检查当前文件，还需要扩大检查范围到包、模块甚至整个工程。
![image](uploads/93026/29ea9ee3-cf17-494b-9ac2-987676a31f8e/image.png)
示例：
![image](uploads/93026/f353fa58-4c9d-498a-9222-a47ddaee266b/image.png)
上图属于关联性问题，`controller`调用`service`传入了`userName`，在日志输出时，会存在问题 `When data from an untrusted source is put into a logger and not neutralized correctly`。类似这种问题，`Analyze Current File`是检测不出来的，需要`Analyze Package/Module/Project Files`才可以检测出来。

## Q3：关于 STCAL_INVOKE_ON_STATIC_CALENDAR_INSTANCE、STCAL_INVOKE_ON_STATIC_DATE_FORMAT_INSTANCE 告警的专项治理说明

### 专项背景

规范要求禁止调用静态的`Calendar`、`DateFormat` 。以`SimpleDateFormat`为例，这是线程不安全的类，在高并发下使用会出现非预期的日期格式化异常，一般不要定义为`static`变量，如果定义为`static`，必须加锁，或者使用`DateUtils`工具类。除`SimpleDateFormat`类外，还有不少 XXXFormat类、XXXCalendar类等对应方法都是非线程安全的。

### 整改建议

#### 局部变量

最简单的方案就是将 `SimpleDateFormat`对象定义为方法内局部变量。适用于并发量较小的场景，对于超大并发场景不推荐，超大并发场景下此种方式会创建大量的`SimpleDateFormat` 临时对象，对内存和性能会产生影响。（单个`SimpleDateFormat`对象大约占用1KB内存）

#### 加锁

将`SimpleDateFormat`类对象定义成全局静态变量，此时所有线程共享`SimpleDateFormat`类对象，此时在调用格式化时间的方法时，对`SimpleDateFormat`对象进行加锁调用。

```java
synchronized (simpleDateFormat){
    simpleDateFormat.parse("2024-10-01");
}
```

适用于并发量较小的场景，对于超大并发场景也不推荐，超大并发场景下因为排他锁会影响程序的执行性能。

#### ThreadLocal（推荐）

使用`ThreadLocal`存储每个线程拥有的`SimpleDateFormat`对象的副本，能够有效的避免多线程造成的线程安全问题。

```java
private static final ThreadLocal<DateFormat> df = new ThreadLocal<DateFormat>() {
    @Override
    protected DateFormat initialValue() {
        return new SimpleDateFormat("yyyy-MM-dd");
    }
};
```

推荐在高并发业务场景的生产环境使用。

#### 使用DateTimeFormatter（推荐）

`DateTimeFormatter`是`Java8`提供的新的日期时间API中的类，`DateTimeFormatter`类是线程安全的，可以在高并发场景下直接使用。

```java
private static DateTimeFormatter formatter = DateTimeFormatter.ofPattern("yyyy-MM-dd");

// 获取当前日期
LocalDate today = LocalDate.now();

// 格式化日期
String formattedDate = today.format(formatter);

// 解析日期
LocalDate parsedDate = LocalDate.parse("2024-10-01", formatter);
```

### 相关告警

Spotbugs 针对本条规范提供了检查规则，对应告警码分别为：`STCAL_INVOKE_ON_STATIC_CALENDAR_INSTANCE`、`STCAL_INVOKE_ON_STATIC_DATE_FORMAT_INSTANCE`。

官方说明：
[https://spotbugs.readthedocs.io/en/stable/bugDescriptions.html#stcal-call-to-static-calendar-stcal-invoke-on-static-calendar-instance](https://spotbugs.readthedocs.io/en/stable/bugDescriptions.html#stcal-call-to-static-calendar-stcal-invoke-on-static-calendar-instance)
[https://spotbugs.readthedocs.io/en/stable/bugDescriptions.html#stcal-call-to-static-dateformat-stcal-invoke-on-static-date-format-instance](https://spotbugs.readthedocs.io/en/stable/bugDescriptions.html#stcal-call-to-static-dateformat-stcal-invoke-on-static-date-format-instance)

# 本文件评审、修正记录

| 文件名称 | Java语言编码规范                                                                                              |               |               |        |
| ---------- | --------------------------------------------------------------------------------------------------------------- | --------------- | --------------- | -------- |
| 序号     | 流程                                                                                                          | 拟制人/审核人 | 拟制/审核时间 | 版本号 |
| 1        | 编写                                                                                                          | 何永进        | 2018/10/20    | V1.0   |
| 2        | 增加“避免变量在使用前被另一个赋值覆盖”章节                                                                  | 何永进        | 2019/01/17    | V1.1   |
| 3        | 修订                                                                                                          | 何永进        | 2020/03/24    | V1.2   |
| 4        | 补充第3章22，23节，对HTTPClient的封装，以及对内存数据库事务的要求。                                           | 何永进        | 2020/09/14    | V1.3   |
| 5        | 补充第6章，Restful接口规范。                                                                                  | 何永进        | 2020/09/15    | V1.4   |
| 6        | 补充常见不良习惯第14节，对日期运算的要求                                                                      | 何永进        | 2020/11/09    | V1.4.1 |
| 7        | 补充编程惯例第3章24节，对返回bool类型方法命名的建议。   补充编程惯例第3章25节，强制：JDBC结果集大小应当加以限 | 何永进        | 2021/03/01    | V1.4.2 |
| 8        | 补充编程惯例第3章26节，增加对SQL注入的防范要求。                                                              | 何永进        | 2021/04/29    | V1.4.3 |
| 9        | 合并《Java开发手册》v1.5.0                                                                                    | 何永进        | 2022/01/18    | v1.5   |
| 10       | 发布                                                                                                          | Java规范组    | 2022/05/12    | V2.0   |
| 11       | 编程惯例章节添加关于“保护程序免遭非法输入数据的破坏”的规范要求                                              | 何永进        | 2022/05/19    | V2.0.1 |
| 12       | 发布                                                                                                          | Java规范组    | 2022/06/14    | V2.1   |
| 13       | 增加第7章 浩鲸科技Java开发环境搭建指引                                                                        | 何永进        | 2022/08/23    | V2.1.1 |
| 14       | 发布                                                                                                          | Java规范组    | 2022/09/16    | V2.2   |
| 15       | 修正2.7.2章节反例的格式问题                                                                                                          | 何永进    | 2022/11/21    | V2.2.1   |
| 16       | 更新Java开发环境搭建指引增加SpotBugs的安装指引                                                                                                        | 何永进    | 2022/12/16    | V2.2.2   |
| 17       | 发布                                                                                                          | Java规范组    | 2022/12/20    | V2.3   |
| 18       | 修订"3.2 并发处理" 章节，增加通过Lock类加锁时的相关要求和使用规范。                                                                                                        | 何永进    | 2023/05/18    | V2.3.1   |
| 19       | 发布                                                                                                          | Java规范组    | 2023/05/19    | V2.4   |
| 20       | 修订"3.2. 并发处理" 章节，在多线程访问Map场景下的相关要求从【参考】 改为【强制】 。                                                                        | 何永进    | 2023/05/25    | V2.4.1   |
| 21       | 发布                                                                                                          | Java规范组    | 2023/06/25    | V2.5   |
| 22       | 修订"7.浩鲸科技Java开发环境搭建指引" 章节，增加圈复杂度检测工具Lizard的安装使用说明 。                                                                        | 何永进    | 2023/06/26    | V2.5.1   |
| 23       | 发布                                                                                                          | Java规范组    | 2023/07/20    | V2.6   |
| 24       |  3.1章节修改规范：不要在列表遍历的循环里进行元素的 remove/add 操作。remove 元素请使用Iterator 方式，如果并发操作，需要对 Iterator 对象加锁。<br>3.5章节修改规范：在调用 RPC、二方包、或动态生成类的相关方法时，捕捉异常建议使用 Throwable类来进行拦截。<br>3.7章节修改规范：强制：所有的相同类型的包装类对象之间值的比较，全部使用equals方法比较。(浮点数的包装类除外) <br>6.2.11章节修改规范：Controller接口建议使用注解给接口方法和参数添加说明，方便通过swagger来查看具体接口。                                                                                                    | Java规范组    | 2024/04/30    | V2.6.1   |
| 25       |  2.7.2.4章节增加规范：方法名最好是一个动词或者动词短语，与参数或参数名共同组成动宾短语，即动词 + 名词。 <br>3.7章节增加规范：推荐：Long 或 long 类型变量赋值时，数值后使用大写 L，不能是小写 l ，小写容易跟数字混淆，造成误解。 <br>3.7章节增加规范：不要使用一个常量类维护所有常量，要按常量功能进行归类，分开维护。<br>4.10章节增加规范：数据类型转换导致溢出或者损失精度。                                                                                                  | Java规范组    | 2024/05/20    | V2.6.2   |
| 26       | 发布                                                                                                          | Java规范组    | 2024/05/22    | V2.7   |
| 27       | 修订3.5 异常处理章节，增加了关于在静态块中妥善处理异常的规范，以避免类加载失败的问题。                                                                                                         | Java规范组    | 2024/06/06    | V2.7.1   |
| 28       | 发布                                                                                                          | Java规范组    | 2024/06/19    | V2.8   |
| 29       | 1. 增加部分规范条目对应的“故障警示! ”。<br> 2. 修订2.5章节，增加for，if-else，try-cache语句的嵌套深度要求。 <br> 3. 增加第8章节，补充常见FAQ信息    | Java规范组    | 2024/08/20    | V2.8.1   |
| 30       | 发布                                                                                                          | Java规范组    | 2024/08/21    | V2.9   |
| 31       | 1. "JDBC结果集大小应当加以限制" 相关内容迁移到 5.1 内存管理章节<br>2. 添加 “5.1.7. 避免将过大的文件一次性加载到内存中” 章节内容          （规范来源：严重生产故障3695958）                                                                                            | Java规范组    | 2024/10/11    | V2.9.1   |
| 32       | 发布                                                                                                          | Java规范组    | 2024/10/21    | V2.10   |
| 33       |  1、新增文本块TextBlock、模式匹配的instanceof、Record类型、封闭类Sealed Class、开关表达式等JDK8~JDK17新特性相关规范条目及示例：<br>【推荐】在JDK9以上，推荐使用List.of()、Set.of()、Map.of()和Map.ofEntries()等工厂方法创建不可变集合。这种方式可以使代码更加简洁，并且提高性能。<br>【推荐】在JDK9以上，使用try-with-resources语句时，无需在try语句中声明新变量，直接使用已有资源变量即可。<br>【推荐】在JDK14以上，在处理switch语句时，使用开关表达式(Switch Expressions)来简化代码和提高可读性。<br>【推荐】在JDK15以上，推荐使用字符串文本块（Text Blocks）来编写多行字符串，提高代码的可读性和维护性。【说明】字符串文本块通过三个双引号（"""）包围，允许字符串跨多行而无需转义。<br>【推荐】在JDK16以上，推荐使用record关键字定义不可变的数据结构，它可以自动生成构造方法、equals()、hashCode()、toString()方法以及访问字段的方法。<br>【推荐】在JDK16以上，使用instanceof模式匹配可以简化类型检查和转换的代码。<br>【推荐】在JDK17以上，使用封闭类（Sealed Classes）来限制类的继承，提高代码的安全性和可维护性。<br>2、增加8.3章节：关于STCAL_INVOKE_ON_STATIC_CALENDAR_INSTANCE、STCAL_INVOKE_ON_STATIC_DATE_FORMAT_INSTANCE 专项告警治理FAQ        | Java规范组    | 2024/11/12    | V2.10.1   |
| 34       | 发布                                                                                                          | Java规范组    | 2024/11/15    | V2.11   |
| 35       | 添加 “5.1.8. 确保 SQL 拼装时查询条件有效性，避免大表扫描” 章节内容          （规范来源：严重生产故障3544304,31154605）                                                                                            | Java规范组    | 2024/12/24    | V2.11.1   |
| 36       | 增加严重生产故障3786355相关故障警示，涉及3.2章节、3.5章节                                                                                              | Java规范组    | 2025/01/02   | V2.11.2    |
| 37       | 发布                                                                                                          | Java规范组    | 2025/01/20    | V2.12   |
| 38       | 第3章编程惯例中增加3.6章节资源管理相关规范内容，对HttpClient的使用提出规范化要求。（规范来源：严重生产故障3787588）                                                                                                          | Java规范组    | 2025/02/12    | V2.12.1   |
| 39       | 完善3.2章节并发处理中【禁止使用 Timer 和 TimerTask 调度多任务，避免因未捕获单个任务异常而导致所有任务终止】的规范细节，补充故障案例和示例。（规范来源：严重生产故障3787793）                                       | Java规范组    | 2025/02/12    | V2.12.2   |
| 40       | 发布                                                                                                          | Java规范组    | 2025/02/24    | V2.13   |
