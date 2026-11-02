![image](uploads/23632/7b47e396-cdfe-45b0-b094-1ccbf26c6e2e/image.png)

# 前言

编码规范是开发人员之间的共同约定，遵守开发规范会带来几个明显的好处：

- 有利于团队分工合作，相同风格的代码，使得不同的人员开发的代码整合起来更加容易；
- 有利于提升代码质量，减少Bug数，尤其是一些低级Bug，遵守规范会自动规避一些低级错误；
- 有利于技术传承和代码维护，规范的代码可以获得继任者的钦佩而不是相反；
- 遵守代码规范有利于开发人员提升自我修养，对于个人成长也是有利的；

## 适用对象

浩鲸科技 Android APP开发人员（Java）

## 目的

为了持续提升公司APP产品质量和稳定性，特制定本规范，让公司的APP开发人员拥有相同的基础开发话术，促进相互沟通和理解，也便于公司APP技术传承，让继任者能够很容易的维护和升级产品源代码

# 命名风格

## 变量命名

1. 【强制】代码中的命名均不能以下划线或美元符号开始，也不能以下划线或美元符号结束。

> 所属范围： Java代码部分
> 与Java规范差异： 新增

<font color="red">反例</font>：

```java
String _name;

String _name_name;

String __name__name;

String __name __name;

Object $Object;

String name_name_;

String name_;

String name$;

Object object$;

```

2. 【强制】代码中的命名严禁使用拼音与英文混合的方式，更不允许直接使用中文的方式。
   说明：正确的英文拼写和语法可以让阅读者易于理解，避免歧义。
   注意：即使纯拼音命名方式也要避免采用；国际通用的名称，可视同英文。

> 所属范围： Java代码部分
> 与Java规范差异： 新增

正例：

```java
String iwhalecloud;

String taobao;

String youku;

String hangzhou;
```

<font color="red">反例</font>:

```java
double DaZhePromotion;//[打折]

private String getPingfenByName(){return "";}//[评分]

int 某变量 = 3;
```

## 类名命名

1. 【强制】类名都以UpperCamelCase风格编写，类名通常是名词或名词短语。

> 所属范围： Java代码部分
> 与Java规范差异： 新增

| 类                 | 描述                                                                 | 例如                                  |
| ------------------ | -------------------------------------------------------------------- | ------------------------------------- |
| Activity 类        | Activity 后缀标识                                                    | 欢迎页面类 WelcomeActivity            |
| Adapter 类         | Adapter 为后缀标识                                                   | 新闻详情适配器 NewDetailAdapter       |
| 解析类             | Parser 为后缀标识                                                    | 首页解析类 HomePosterParser           |
| 工具方法类         | Util 或 Manager 为后缀标识（与系统或第三方的 Utils 区分）或功能+Util | 打印工具类：PrinterUtil               |
| 数据库类           | 以 DBHelper 后缀标识                                                 | 新闻数据库：NewDBHelper               |
| Service 类         | 以 Service 为后缀标识                                                | 时间服务 TimeService                  |
| Receiver 类        | 以 Receiver 为后缀标识                                               | 推送接收 JPushReceiver                |
| Provider 类        | 以 Provider 为后缀标识                                               | 内容提供方 ContentProvider            |
| 自定义的共享基础类 | 以 Base 开头                                                         | BaseActivity,BaseFragment             |
| 测试类             | 以它要测试的类的名称开始，以 Test 结束                               | 例如：HashTest 或 HashIntegrationTest |
| 接口（interface）  | 命名规则与类一样采用大驼峰命名法，多以 able 或 ible 结尾             | interface Runnable                    |

注意： 如果项目采用 MVP，所有 Model、View、Presenter 的接口都以 I 为前缀，不加后缀，其他的接口采用上述命名规则。

2. 【强制】方法名、参数名、成员变量、局部变量都统一使用lowerCamelCase风格，必须遵从驼峰形式。

> 所属范围： Java代码部分
> 与Java规范差异： 相同

正例：

```java
int localValue;

int getHttpMessage(){return 0;}

int inputUserId;
```

3. 【强制】常量命名全部大写，单词间用下划线隔开，力求语义表达完整清楚，不要嫌名字长。

> 所属范围： Java代码部分
> 与Java规范差异： 相同

正例：

```java
private static final int MAX_STOCK_COUNT = 10;
```

<font color="red">反例</font>：

```java
private static final int MAX_COUNT = 10;
```

4. 【强制】抽象类命名使用Abstract或Base开头；异常类命名使用Exception结尾；测试类命名以它要测试的类的名称开始，以Test结尾。

> 所属范围： Java代码部分
> 与Java规范差异： 新增

正例：

```java
public abstract class AbstractActivity{}

public abstract class BaseActivity{}

public class BusinessException extends Exception{}

public class GetUserTest {}
```

5. 【强制】中括号是数组类型的一部分，数组定义如下, 方括号要放在变量和类之间。

> 所属范围： Java代码部分
> 与Java规范差异： 相同

正例：

```java
String[] args;
```

<font color="red">反例</font>：

```java
String args[];
```

6. 【强制】POJO类中布尔类型的变量，都不要加is，否则部分框架解析会引起序列化错误。

> 所属范围： Java代码部分
> 与Java规范差异： 相同

<font color="red">反例</font>：
定义为基本数据类型 `Boolean isDeleted；`的属性，它的方法也是 `isDeleted()`，RPC 框架在反向解析的时候，“以为”对应的属性名称是 `deleted`，导致属性获取不到，进而抛出异常。

7. 【强制】包名统一使用小写，点分隔符之间有且仅有一个自然语义的英语单词。包名统一使用单数形式，但是类名如果有复数含义，类名可以使用复数形式。

> 所属范围： Java代码部分
> 与Java规范差异： 新增

正例：

```java
//应用工具类包名为：
package com.iwhalecloud.open.util;

public class MessageUtils{}
```

8. 【推荐】杜绝完全不规范的缩写，避免望文不知义。

> 所属范围： Java代码部分
> 与Java规范差异： 相同

正例：

```java
public abstract class AbstractClass{}

int condition;
```

<font color="red">反例</font>：
`AbstractClass`“缩写”命名成 `AbsClass`；`condition`“缩写”命名成 `condi`，此类随意缩写严重降低了代码的可阅读性。

```java
public abstract class AbsClass{}

int condition;
```

9. 【推荐】为了达到代码自解释的目标，任何定义编程元素在命名时使用尽量完整单词组合来表达其意。

> 所属范围： Java代码部分
> 与Java规范差异： 相同

正例：

```java
public class PullCodeFromRemoteRepository{}
```

<font color="red">反例</font>：

```java
int a;
```

10. 【推荐】如果模块、接 口、类、 方法使用了设计模式，在命名时体现出具体模式。
    说明：将设计模式体现在名字中，有利于阅读者快速理解架构设计理念。

> 所属范围： Java代码部分
> 与Java规范差异：新增

正例：

```java
public class OrderFactory;

public class LoginProxy;

public class ResourceObserver;
```

11. 【推荐】接口类中的方法和属性不要加任何修饰符号（public 也不要加），保持代码的简洁性，并加上有效的Javadoc注释。尽量不要在接口里定义变量，如果一定要定义变量，肯定是与接口方法相关，并且是整个应用的基础常量。

> 所属范围： Java代码部分
> 与Java规范差异： 新增

正例：

```java
void f();//接口方法签名

String COMPANY = "iwhale";//接口基础常量量表示
```

<font color="red">反例</font>：

```java
//接口方法定义,JDK8中接口允许有默认实现，那么这个default 方法，是对所有实现类都有价值的默认实现。
public abstract void f();
```

12. 【参考】枚举类名建议带上Enum后缀，枚举成员名称需要全大写，单词间用下划线隔开。 说明：枚举其实就是特殊的常量类，且构造方法被默认强制是私有。

> 所属范围： Java代码部分
> 与Java规范差异： 新增

```java
public enum ProcessStatusEnum{

SUCCESS,

UNKOWN_REASON

}
```

## 常量定义

1. 【强制】不允许任何魔法值（即未经定义的常量）直接出现在代码中。

> 所属范围： Java代码部分
> 与Java规范差异：相同

<font color="red">反例</font>：

```java
String key = "Id#taobao_" + tradeId;

cache.put(key, value);
```

2. 【强制】long或者Long初始赋值时，使用大写的L，不能是小写的l，小写容易跟数字1混淆，造成误解。
   说明：long count = 2l; 写的是数字的21，还是Long型的2?

> 所属范围： Java代码部分
> 与Java规范差异：新增

正例：

```java
long count = 2L;
```

<font color="red">反例</font>：

```java
long count = 2l;
```

3. 【推荐】不要使用一个常量类维护所有常量，按常量功能进行归类，分开维护。 说明：大而全的常量类，非得使用查找功能才能定位到修改的常量，不利于理解和维护。
   参考：缓存相关常量放在类CacheConsts下；系统配置相关常量放在类ConfigConsts下。

> 所属范围： Java代码部分
> 与Java规范差异：新增

4. 【推荐】如果变量值仅在一个范围内变化，且带有名称之外的延伸属性，定义为枚举类。下面正例中的数字就是延伸信息，表示星期几。

> 所属范围： Java代码部分
> 与Java规范差异：新增

正例：

```java
public Enum {

MONDAY(1), TUESDAY(2), WEDNESDAY(3), THURSDAY(4), FRIDAY(5),

SATURDAY(6), SUNDAY(7);

}

```

## 包命名

1. 【强制】包名全部小写，连续的单词只是简单地连接起来，不使用下划线。 采用反域名命名规则，全部使用小写字母。 一级包名为com， 二级包名为xx（可以是公司或则个人的随便），三级包名根据应用进行命名，四级包名为模块名或层级名。

> 所属范围： Java代码部分
> 与Java规范差异：新增

例如：`com.ztesoft.moduleplatform`

| 包名                                                                 | 此包中包含                                          |
| -------------------------------------------------------------------- | --------------------------------------------------- |
| com.xx.moduleplatform.功能名.activity                                | 页面用到的 Activity 类 (activitie 层级名用户界面层) |
| com.xx.moduleplatform.功能名.base                                    | 基础共享的类                                        |
| com.xx.moduleplatform.功能名.adapter                                 | 页面用到的 Adapter 类 (适配器 的类)                 |
| com.xx.moduleplatform.功能名.util                                    | 此包中包含：公共工具方法类（util 模块名）           |
| com.xx.moduleplatform.功能名.bean                                    | 下面可分：vo、po、dto 此包中包含：JavaBean 类       |
| com.xx.moduleplatform.功能名.model                                   | 此包中包含：模型类                                  |
| com.xx.moduleplatform.功能名.db                                      | 数据库操作类                                        |
| com.xx.moduleplatform.功能名.view (或者 com.xx.应用名称缩写.widget ) | 自定义的 View 类等                                  |
| com.xx.moduleplatform.功能名.service                                 | Service 服务                                        |
| com.xx.moduleplatform.功能名.receiver                                | BroadcastReceiver 服务                              |

注意： 如果项目采用 MVP，所有 M、V、P 抽取出来的接口都放置在相应模块的 i 包下，所有的实现都放置在相应模块的 impl 下。

## 资源和文件命名

1. 【推荐】资源布局文件（XML文件（layout布局文件））全部小写，采用下划线命名法

> 所属范围： Android资源文件
> 与Java规范差异：新增

- 1)contentview 命名，使用名词或名词词组所有 Activity 或 Fragment 的 contentView 必须与其类名对应，对应规则为： 将所有字母都转为小写，将类型和功能调换（也就是后缀变前缀） 例如：activity_main.xml
- 2)Dialog 命名：dialog\_描述.xml 例如：dialog_hint.xml
- 3)PopupWindow 命名：ppw\_描述.xml 例如：ppw_info.xml
- 4)列表项命名：item\_描述.xml 例如：item_city.xml
- 5)包含项命名：模块\_(位置)描述.xml 例如 activity_main_head.xml、 activity_main_bottom.xml

2. 【推荐】资源文件（图片drawable文件夹下）全部小写，采用下划线命名法，加前缀区分命名模式：可加后缀_small表示小图, _big表示大图，逻辑名称可由多个单词加下划线组成，采用以下规则：

- 用途_模块名_逻辑名称
- 用途_模块名_颜色
- 用途_逻辑名称  用途_颜色
  说明： 用途也指控件类型（具体见UI控件缩写表）

> 所属范围： Android资源文件
> 与Java规范差异：新增

例如：
btn_main_home.png 按键
divider_maket_white.png 分割线
ic_edit.png 图标
bg_main.png 背景
btn_red.png 红 色按键
btn_red_big.png 红 色 大按键
ic_head_small.png 小头像
bg_input.png 输 入框背景
divider_white.png 白 色分割线
如果有多种形态如按钮等除外如 btn_xx.xml（selector）

| 名称             | 功能                                   |
| ---------------- | -------------------------------------- |
| btn_xx           | 按钮图片使用 btn\_整体效果（selector） |
| btn_xx_normal    | 按钮图片使用 btn\_正常情况效果         |
| btn_xx_pressed   | 按钮图片使用 btn\_点击时候效果         |
| btn_xx_focused   | state_focused 聚焦效果                 |
| btn_xx_disabled  | state_enabled (false)不可用效果        |
| btn_xx_checked   | state_checked 选中效果                 |
| btn_xx_selected  | state_selected 选中效果                |
| btn_xx_checkable | state_checkable 可选效果               |
| bg_head          | 背景图 片使用 bg*功能*说明             |
| def_search_cell  | 默认图片使用 def*功能*说明             |
| ic_more_help     | 图标图片使用 ic*功能*说明              |
| seg_list_line    | 具有分隔特征的图片使用 seg*功能*说明   |
| sel_ok           | 选择图标使用 sel*功能*说明             |

注意：使用 AndroidStudio 的插件 SelectorChapek 可以快速生成 selector，前提是命名要规范。

3. 【推荐】动画文件（anim 文件夹下）全部小写，采用下划线命名法，加前缀区分。
   具体动画采用以下规则： 模块名_逻辑名称，例如： refresh_progress.xml, market_cart_add.xml, market_cart_remove.xml，
   普通的tween动画采用如下表格中的命名方式 // 前面为动画的类型，后面为方向

> 所属范围： Android资源文件
> 与Java规范差异：新增

| 动画命名例子      | 规范写法       |
| ----------------- | -------------- |
| fade_in           | 淡入           |
| fade_out          | 淡出           |
| push_down_in      | 从下方推入     |
| push_down_out     | 从下方推出     |
| push_left         | 推向左方       |
| slide_in_from_top | 从头部滑动进入 |
| zoom_enter        | 变形进入       |
| slide_in          | 滑动进入       |
| shrink_to_middle  | 中间缩小       |

4. 【推荐】values中name命名

> 所属范围： Android资源文件
> 与Java规范差异：新增

| 类别    | 命名                                                                    | 示例                                                                                                                                                                            |
| ------- | ----------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| strings | strings 的 name 命名使用下划线命名法，采用以下规则：模块名+逻辑名称     | main_menu_about 主菜单按键文字 friend_title 好友模块标题栏 friend_dialog_del 好友删除提示 login_check_email 登录验证 dialog_title 弹出框标题 button_ok 确认键 loading 加载 文字 |
| colors  | colors 的 name 命名使用下划线命名法，采用以下规则：模块名+逻辑名称+颜色 | friend_info_bg_transparent friend_bg_gray                                                                                                                                       |
| styles  | styles 的 name 命名使用 Camel 命名法，采用以下规则：模块名+逻辑名称     | main_tabBottom                                                                                                                                                                  |

5. 【推荐】layout中的id命名命名模式为：所在组件_逻辑名称_类型 的模式
   例如： @+id/main_name_tv 、 @id/chat_send_btn

> 所属范围： Android资源文件
> 与Java规范差异：新增

对应组件缩写表

| 组件                   | 缩写              |
| ---------------------- | ----------------- |
| Component 组件         | Abbreviation 缩写 |
| TextView               | tv                |
| ImageView              | iv                |
| Button                 | bt                |
| EditText               | et                |
| LinearLayout           | ll                |
| ReleativeLayout        | rl                |
| normally : FirstSecond | fs                |

# 代码格式

1. 【强制】大括号的使用约定。如果是大括号内为空，则简洁地写成{}即可，不需要换行；

> 所属范围： Java代码部分
> 与Java规范差异：相同

如果是非空代码块则：

- 1）左大括号前不换行。
- 2）左大括号后换行。
- 3）右大括号前换行。
- 4）右大括号后还有else等代码则不换行；表示终止的右大括号后必须换行。

正例：

```java
public class Test {}

public void test ();

public String getUserName() {

    return userName;

}

if (i == 0) {

    Log.i(TAG, "hello iwhale");

} else {

    Log.i(TAG, "hello cloud");

}
```

2. 【强制】左小括号和字符之间不出现空格；同样，右小括号和字符之间也不出现空格。

> 所属范围： Java代码部分
> 与Java规范差异：相同

<font color="red">反例</font>：

```java
if ( a == b )
```

3. 【强制】if/for/while/switch/do等保留字与括号之间都必须加空格。

> 所属范围： Java代码部分
> 与Java规范差异：相同

正例：

```java
if (i == 0) {
    Log.i(TAG, "Hello iWhaleCloud");
}
```

4. 【强制】任何二目、三目运算符的左右两边都需要加一个空格。
   说明：运算符包括赋值运算符=、逻辑运算符&&、加减乘除符号等。

> 所属范围： Java代码部分
> 与Java规范差异：相同

```java
int a = b;

if (i == 0) {

    Log.i(TAG, "Hello iWhaleCloud");

}
```

5. 【强制】采用4个空格缩进，禁止使用tab字符。
   说明： 如果使用tab缩进，必须设置1个tab为4个空格。IDE设置tab为4个空格时，在Android Studio导入CodeStyle 配置文件IwhaleAndroid.xml

> 所属范围： Java代码部分
> 与Java规范差异：相同

正例：（涉及 1-5 点）

```java
public static void main(String[] args) {
    // 缩进4个空格

    // 运算符的左右必须有 一个空格
    int flag = 0;

    // 关键词if与括号之间必须有一个空格，括号内的f与左括号，0与右括号不需要空格
    if (flag == 0) {
        Log.i(TAG, say);
    }

    // 左大括号前加空格且不换行；左大括号后换行
    if (flag == 1) {
        Log.i(TAG, "world");
        // 右大括号前换行，右大括号后有else，不用换行
    } else {
        Log.i(TAG, "ok");
        // 在右 大括号后直接结束，则必须换行
    }
}
```

6. 【强制】注释的双斜线与注释内容之间有且仅有一个空格。

> 所属范围： Java代码部分
> 与Java规范差异：相同

正例：// 注释内容，注意在//和注释内容之间有一个空格。

7. 【强制】单行字符数限不超过120个，超出需要换行，换行时遵循如下原则：

> 所属范围： Java代码部分
> 与Java规范差异：相同

- 1） 第二行相对一缩进4个空格，从第三行开始不再继续缩进参考示例。
- 2） 运算符与下文一起换行。
- 3） 方法调用的点符号与下文一起换行。
- 4） 方法调用时，多个参数，需要换行时，在逗号后进行。
- 5） 在括号前不要换行，见反例。

正例：

```java
StringBuffer sb = new StringBuffer();
// 超过120个字符的情况下，换行缩进4个空格，点号和方法名称一起换行
sb.append("zi").append("xin")...
    .append("huang")...
    .append("huang")...
    .append("huang");
```

<font color="red">反例</font>：

```java
StringBuffer sb = new StringBuffer();
// 超过120个字符的情况下，不要在括号前换行
sb.append("zi").append("xin")...append
    ("huang");

//参数很多的方法调用可能超过120个字符，不要在逗号前换行
method(args1, args2, args3, ...
    , argsX);
```

8. 【强制】方法参数在定义和传入时，多个参数逗号后边必须加空格。
   正例：下例中实参的"a",后边必须要有一个空格。

> 所属范围： Java代码部分
> 与Java规范差异：相同

```java
void method("a", "b", "c");
```

9. 【强制】IDE的text file encoding设置为UTF-8; IDE中文件的换行符使用Unix格式，不要使用Windows格式。

> 所属范围： Java代码部分
> 与Java规范差异：相同

10. 【推荐】没有必要增加若干空格来使某一行的字符与上一行对应位置的字符对齐。

> 所属范围： Java代码部分
> 与Java规范差异：相同

正例：

```java
int a = 3;

long b = 4L;

float c = 5F;

StringBuffer sb = new StringBuffer();
```

说明：增加 sb 这个变量量，如果需要对齐，则给 a、b、c 都要增加几个空格，在变量比较多的情况下，是一种累赘的事情。

11. 【推荐】 方法体内的执行语句组、变量的定义语句组、不同的业务逻辑之间或者不同的语义之间插入一个空行。相同业务逻辑和语义之间不需要插入空行。
    说明：没有必要插入多个空行进行隔开。

> 所属范围： Java代码部分
> 与Java规范差异：相同

# UI 及布局

1. 【强制】设置距离使用dp

> 所属范围： Android布局部分
> 与Java规范差异：新增

2. 【强制】设置字体使用sp

> 所属范围： Android布局部分
> 与Java规范差异：新增

# OOP 规约

1. 【强制】避免通过一个类的对象引用访问此类的静态变量或静态方法，无谓增加编译器解析成本，直接用类名来访问即可。

> 所属范围： Java代码部分
> 与Java规范差异：新增

2. 【强制】所有的覆写方法，必须加@Override注解。
   说明：getObject()与get0bject()的问题， 一个是字母的O， 一个是数字的0，加@Override可以准确判断是否覆盖成功；另外，如果在抽象类中对方法签名进行修改，其实现类会马上编译报错。

> 所属范围： Java代码部分
> 与Java规范差异：新增

3. 【强制】相同参数类型，相同业务含义，才可以使用Java的可变参数，避免使用Object。
   说明：可变参数必须放置在参数列表的最后。（提倡同学们尽量不用可变参数编程）

> 所属范围： Java代码部分
> 与Java规范差异：新增

正例：

```java
public User getUsers(String type, Integer... ids) {}
```

4. 【强制】不能使用过时的类或方法。 说明：java.net.URLDecoder 中的方法 decode(String encodeStr) 这个方法已经过时，应该使用双参数`decode(String source, String encode)`。接口提供方既然明确是过时接口，那么有义务同时提供新的接口；作为调用方来说，有义务去考证过时方法的新实现是什么。

> 所属范围： Java代码部分
> 与Java规范差异：相同

5. 【强制】Object的equals 方法容易抛空指针异常，应使用常量或确定有值的对象来调用equals。

> 所属范围： Java代码部分
> 与Java规范差异：相同

正例：

```java
"test".equals(object);
```

<font color="red">反例</font>：

```java
object.equals("test");
```

说明：推荐使用 java.util.Objects#equals（JDK7 引入的工具类）

6. 【强制】所有的相同类型的包装类对象之间值的比较，全部使用equals方法比较。
   说明：于Integer var = ? 在-128 至127范围内的赋值，Integer对象是在IntegerCache.cache产生，会复用已有对象，这个区间内的Integer值可以直接使用==进行判断，但是这个区间之外的所有数据，都会在堆上产生，并不会复用已有对象，这是一个大坑，推荐使用equals方法进行判断。

> 所属范围： Java代码部分
> 与Java规范差异：相同

7. 【强制】序列化类新增属性时，请不要修改serialVersionUID字段，避免反序列失败；如果完全不兼容升级，避免反序列化混乱，那么请修改serialVersionUID值。
   说明：注意serialVersionUID不一致会抛出序列化运行时异常。

> 所属范围： Java代码部分
> 与Java规范差异：新增

8. 【强制】构造方法里面禁止加入任何业务逻辑，如果有初始化逻辑，请放在init 方法中。

> 所属范围： Java代码部分
> 与Java规范差异：新增

9. 【强制】POJO类必须写toString 方法。使用IDE的中工具：source> generate toString时，如果继承了另一个POJO类，注意在前面加一下super.toString。
   说明：在方法执行抛出异常时，可以直接调用POJO的toString() 方法打印其属性值，便于排查问题。

> 所属范围： Java代码部分
> 与Java规范差异：新增

10. 【推荐】使用索引访问用String的split 方法得到的数组时，需做最后一个分隔符后有无内容的检查，否则会有抛IndexOutOfBoundsException的风险。

> 所属范围： Java代码部分
> 与Java规范差异：新增

说明：

```java
String str = "a,b,c,,";

String[] ary = str.split(",");

//预期 大于3，结果是3
Log.i(TAG,""+ary.length);
```

11. 【推荐】当一个类有多个构造方法，或者多个同名方法，这些方法应该按顺序放置在一起，便于阅读，此条规则优先于第12条规则。

> 所属范围： Java代码部分
> 与Java规范差异：新增

12. 【推荐】 类内方法定义顺序依次是：公有方法或保护方法 > 私有方法 > getter/setter 方法。
    说明：公有方法是类的调用者和维护者最关心的方法， 首屏展示最好；保护方法虽然只是子类关心，也可能是“模板设计模式”下的核心方法； 而私有方法外部一般不需要特别关心，是一个黑盒实现；因为承载的信息价值较低，所有Service和DAO的getter/setter 方法放在类体最后。

> 所属范围： Java代码部分
> 与Java规范差异：新增

13. 【推荐】setter 方法中，参数名称与类成员变量名称一致，this.成员名 = 参数名。在getter/setter 方法中，不要增加业务逻辑，增加排查问题的难度。

> 所属范围： Java代码部分
> 与Java规范差异：新增

<font color="red">反例</font>：

```java
public Integer getData() {
    if (true) {
        return this.data + 100;
    } else {
        return this.data - 100;
    }
}
```

14. 【推荐】循环体内，字符串的连接方式，使用StringBuilder的append 方法进行扩展。
    说明：反编译出的字节码文件显示每次循环都会new出一个StringBuilder对象，然后进行append操作，最后通过toString 方法返回String对象，造成内存资源浪费。

> 所属范围： Java代码部分
> 与Java规范差异：相同

<font color="red">反例</font>：

```java
String str = "start";
for (int i = 0; i < 100; i++) {
    str = str + "hello";
}

```

15. 【推荐】final可以声明类、成员变量、方法、以及本地变量，下列情况使用final关键字：

> 所属范围： Java代码部分
> 与Java规范差异：新增

- 1）不允许被继承的类，如：String类。
- 2）不允许修改引用的域对象，如：POJO类的域变量。
- 3）不允许被重写的 方法，如：POJO类的setter 方法。
- 4）不允许运行过程中重新赋值的局部变量量。
- 5）避免上下文重复使用一个变量，使用final描述可以强制重新定义一个变量，方便更好地进行重构。

16. 【推荐】慎用Object的clone 方法来拷贝对象。
    说明：对象的clone 方法默认是浅拷贝，若想实现深拷贝需要重写clone 方法实现属性对象的拷贝。

> 所属范围： Java代码部分
> 与Java规范差异：新增

17. 【推荐】类成员与方法访问控制从严：

> 所属范围： Java代码部分
> 与Java规范差异：相同

- 1）如果不允许外部直接通过new来创建对象，那么构造方法必须是private。
- 2）工具类不允许有public或default构造方法。
- 3）类非static成员变量并且与子类共享，必须是protected。
- 4）类非static成员变量并且仅在本类使用，必须是private。
- 5）类static成员变量如果仅在本类使用，必须是private。
- 6）若是static成员变量，必须考虑是否为final。
- 7）类成员方法只供类内部调用，必须是private。
- 8）类成员方法只对继承类公开，那么限制为protected。
  说明：任何类、方法、参数、变量，严控访问范围。过于宽泛的访问范围，不利于模块解耦。
  思考：如果是一个private的方法，想删除就删除，可是一个public的service 方法，或者一个public的成员变量，删除一下，不得手心冒点汗吗？变量像自己的小孩，尽量在自己的视线内，变量作用域太大， 无限制的到处跑，那么你会担心的。

# 集合处理

1. 【强制】关于hashCode和equals的处理，遵循如下规则：

> 所属范围： Java代码部分
> 与Java规范差异：新增

- 1）只要重写equals，就必须重写hashCode。
- 2）因为Set存储的是不重复的对象，依据hashCode和equals进行判断，所以Set存储的对象必须重写这两个方法。
- 3）如果自定义对象做为Map的键，那么必须重写hashCode和equals。 说明：String重写了hashCode和equals方法，所以我们可以非常愉快地使用String对象作为key来使用。

2. 【强制】 ArrayList的subList结果不可强转成ArrayList，否则会抛出ClassCastException异常，即java.util.RandomAccessSubList cannot be cast to java.util.ArrayList. 说明：subList返回的是 ArrayList 的内部类SubList，并不是ArrayList ， 而是ArrayList 的一个视图，对于SubList 子列列表的所有操作最终会反映到原列表上。

> 所属范围： Java代码部分
> 与Java规范差异：新增

3. 【强制】在subList场景中，高度注意对原集合元素个数的修改，会导致子列表的遍历、增加、删除均会产生ConcurrentModificationException 异常。

> 所属范围： Java代码部分
> 与Java规范差异：新增

4. 【强制】使用集合转数组的方法，必须使用集合的toArray(T[]array)，传入的是类型完全一样的数组，大小就是list.size()。
   说明：使用toArray带参方法，入参分配的数组空间不够大时，toArray方法内部将重新分配内存空间，并返回新数组地址；如果数组元素大于实际所需，下标为`[list.size()]`的数组元素将被置为null，其它数组元素保持原值，因此最好将方法入参数组大小定义与集合元素个数一致。

> 所属范围： Java代码部分
> 与Java规范差异：新增

正例：

```java
List<String> list = new ArrayList<String>(2);
list.add("guan");
list.add("bao");
String[] array = new String[list.size()];
array = list.toArray(array);
```

<font color="red">反例</font>：
直接使用 toArray 无参方法存在问题，此方法返回值只能是 Object[]类，若强转其它类型数组将出现 ClassCastException 错误。

5. 【强制】使用工具类Arrays.asList()把数组转换成集合时，不能使用其修改集合相关的方法，它的add/remove/clear 方法会抛出UnsupportedOperationException异常。
   说明：asList的返回对象是一个Arrays内部类，并没有实现集合的修改方法。Arrays.asList体现的是适配器模式，只是转换接口，后台的数据仍是数组。

> 所属范围： Java代码部分
> 与Java规范差异：新增

```java
String[] str = new String[] { "you", "wu" };
List list = Arrays.asList(str);
```

第一种情况：list.add("yangguanbao"); 运行时异常。
第二种情况：str[0] = "gujin"; 那么list.get(0)也会随之修改。

6. 【强制】不要在foreach循环里进行元素的remove/add操作。remove元素请使用Iterator 方式，如果并发操作，需要对Iterator对象加锁。

> 所属范围： Java代码部分
> 与Java规范差异：相同

正例：

```java
Iterator<String> iterator = list.iterator();
while (iterator.hasNext()) {
    String item = iterator.next();
    if (删除元素的条件) {
        iterator.remove();
    }
}
```

<font color="red">反例</font>：

```java
List<String> list = new ArrayList<String>();
list.add("1");
list.add("2");
for (String item : list) {
    if ("1".equals(item)) {
        list.remove(item);
    }
}
```

说明：以上代码的执行结果肯定会出乎大家的意料，那么试 一下把“1”换成“2”，会是同样的结果吗？

7. 【强制】 在JDK7版本及以上，Comparator要满足如下三个条件，不然Arrays.sort，Collections.sort会报IllegalArgumentException异常。

> 所属范围： Java代码部分
> 与Java规范差异：新增

说明：三个条件如下

- 1） x，y的比较结果和y，x的比较结果相反。
- 2） x>y，y>z，则x>z。
- 3） x=y，则x，z 比较结果和y，z 比较结果相同。

<font color="red">反例</font>：
下例中没有处理相等的情况，实际使用中可能会出现异常：

```java
new Comparator<Student>() {
    @Override
    public int compare(Student o1, Student o2) {
        return o1.getId() > o2.getId() ? 1 : -1;
    }
};
```

8. 【推荐】集合初始化时，指定集合初始值大小。 说明：HashMap使用HashMap(int initialCapacity) 初始化。

> 所属范围： Java代码部分
> 与Java规范差异：新增

正例：
initialCapacity = (需要存储的元素个数 / 负载因子) + 1。注意负载因子（即loader factor）默认为 0.75，如果暂时无法确定初始值大小，请设置为 16（即默认值）。
<font color="red">反例</font>：
HashMap需要放置1024个元素，由于没有设置容量初始大小，随着元素不断增加容量7次被迫扩大，resize需要重建 hash表，严重影响性能。

9. 【推荐】使用entrySet遍历Map类集合KV，而不是keySet 方式进行遍历。
   说明：keySet其实是遍历了2次，一次是转为Iterator对象，另一次是从hashMap中取出key所对应的value。 而entrySet只是遍历了一次就把key和value都放到了entry中，效率更高。如果是JDK8，使用Map.foreach 方法。

> 所属范围： Java代码部分
> 与Java规范差异：新增

正例：
values()返回的是V值集合，是一个list集合对象；keySet()返回的是K值集合，是一个Set集合对象；entrySet()返回的是K-V值组合集合。

10. 【推荐】 高度注意Map类集合K/V不能存储null值的情况，如下表格：

> 所属范围： Java代码部分
> 与Java规范差异：新增

如下表格：

| 集合类            | Key           | Value         | Super       | 说明                   |
| ----------------- | ------------- | ------------- | ----------- | ---------------------- |
| Hashtable         | 不允许为 null | 不允许为 null | Dictionary  | 线程安全               |
| ConcurrentHashMap | 不允许为 null | 不允许为 null | AbstractMap | 锁分段技术（JDK8:CAS） |
| TreeMap           | 不允许为 null | 允许为 null   | AbstractMap | 线程不安全             |
| HashMap           | 允许为 null   | 允许为 null   | AbstractMap | 线程不安全             |

<font color="red">反例</font>：由于 HashMap 的干扰，很多人认为 ConcurrentHashMap 是可以置入 null 值，而事实上，存储 null 值时会抛出 NPE 异常。

11. 【参考】合理利用好集合的有序性(sort)和稳定性(order)，避免集合的无序性(unsort)和不稳定性(unorder)带来的负面影响。
    说明：有序性是指遍历的结果是按某种比较规则依次排列的。稳定性指集合每次遍历的元素次序是一定的。

> 所属范围： Java代码部分
> 与Java规范差异：新增

如：ArrayList是order/unsort；HashMap是unorder/unsort；TreeSet是order/sort。

12. 【参考】利用Set元素唯一的特性，可以快速对一个集合进行去重操作，避免使用List的contains 方法进行遍历、对比、去重操作。

> 所属范围： Java代码部分
> 与Java规范差异：新增

# 并发处理

1. 【强制】获取单例对象需要保证线程安全，其中的方法也要保证线程安全。
   说明：资源驱动类、 工具类、单例工厂类都需要注意。

> 所属范围： Java代码部分
> 与Java规范差异：新增

2. 【推荐】创建线程或线程池时请指定有意义的线程名称， 方便出错时回溯。

> 所属范围： Java代码部分
> 与Java规范差异：新增

正例：

```java
public class TimerTaskThread extends Thread {

    public TimerTaskThread() {
        super.setName("TimerTaskThread");
        ...
}
```

3. 【推荐】线程资源必须通过线程池提供，不允许在应用中自行显式创建线程。
   说明：使用线程池的好处是减少在创建和销毁线程上所花的时间以及系统资源的开销，解决资源不足的问题。如果不使用线程池，有可能造成系统创建大量同类线程而导致消耗完内存或者“过度切换”的问题。

> 所属范围： Java代码部分
> 与Java规范差异：新增

4. 【强制】SimpleDateFormat 是线程不安全的类，一般不要定义为static变量，如果定义为static，必须加锁，或者使用DateUtils 工具类。

> 所属范围： Java代码部分
> 与Java规范差异：新增

正例：注意线程安全，使用DateUtils。亦推荐如下处理：

```java
private static final ThreadLocal<DateFormat> df = new ThreadLocal<DateFormat>() {
    @Override
    protected DateFormat initialValue() {
        return new SimpleDateFormat("yyyy-MM-dd");
    }
};
```

说明：如果是JDK8的应用，可以使用Instant代替Date，LocalDateTime代替Calendar，DateTimeFormatter代替SimpleDateFormat，官方给出的解释：simple beautiful strong immutable thread-safe。

5. 【强制】对多个资源、数据库表、对象同时加锁时，需要保持一致的加锁顺序，否则可能会造成死锁。
   说明：线程一需要对表A、B、C依次全部加锁后才可以进行更新操作，那么线程二的加锁顺序也必须是A、B、C，否则可能出现死锁。

> 所属范围： Java代码部分
> 与Java规范差异：新增

6. 【强制】多线程并行处理定时任务时，Timer运行多个TimeTask时，只要其中之一没有捕获抛出的异常，其它任务便会自动终止运行，使用ScheduledExecutorService则没有这个问题。

> 所属范围： Java代码部分
> 与Java规范差异：新增

7. 【推荐】使用CountDownLatch进行异步转同步操作，每个线程退出前必须调用countDown 方法，线程执行代码注意catch异常，确保countDown 方法被执行到，避免主线程无法执行至await 方法，直到超时才返回结果。
   说明：注意，子线程抛出异常堆栈，不能在主线程try-catch到。

> 所属范围： Java代码部分
> 与Java规范差异：新增

8. 【推荐】避免Random实例被多线程使用，虽然共享该实例是线程安全的，但会因竞争同 一seed 导致的性能下降。
   说明：Random实例包括java.util.Random的实例或者 Math.random()的方式。 正例：在JDK7之后，可以直接使用API ThreadLocalRandom， 而在 JDK7之前，需要编码保证每个线程持有一个实例。

> 所属范围： Java代码部分
> 与Java规范差异：新增

9. 【推荐】在并发场景下，通过双重检查锁（double-checked locking）实现延迟初始化的优化问题隐患(可参考 The "Double-Checked Locking is Broken" Declaration)，推荐解决方案中较为简单一种（适用于JDK5及以上版本），将目标属性声明为 volatile型。

> 所属范围： Java代码部分
> 与Java规范差异：新增

<font color="red">反例</font>：

```java
class Singleton {
    private Helper helper = null;
    public Helper getHelper() {
        if (helper == null) {
            synchronized(this) {
                if (helper == null){
                    helper = new Helper();
                }
            }
        }
        return helper;
    }

// other methods and fields...

}
```

10. 【参考】volatile解决多线程内存不可见问题。对于一写多读，是可以解决变量同步问题，但是如果多写，同样无法解决线程安全问题。如果是count++操作，使用如下类实现：AtomicInteger count = new AtomicInteger(); count.addAndGet(1); 如果是JDK8，推荐使用LongAdder对象，比AtomicLong性能更好（减少乐观锁的重试次数）。

> 所属范围： Java代码部分
> 与Java规范差异：新增

# 控制语句

1. 【强制】在一个switch块内，每个case要么通过break/return等来终止，要么注释说明程序将继续执行到哪 一个case为止；在一个switch块内，都必须包含一个default语句并且放在最后，即使它什么代码也没有。

> 所属范围： Java代码部分
> 与Java规范差异：新增

2. 【强制】在if/else/for/while/do语句中必须使用大括号。即使只有一行代码，避免采用单行的编码方式：

> 所属范围： Java代码部分
> 与Java规范差异：新增

<font color="red">反例</font>：

```java
if (condition) statements;
```

3. 【推荐】表达异常的分支时，少用if-else 方式，这种方式可以改写成：

> 所属范围： Java代码部分
> 与Java规范差异：新增

```java
if (condition) {
    ...
    return obj;
}

//接着写else的业务逻辑代码;
```

说明：如果非得使用if()...else if()...else... 方式表达逻辑，【强制】避免后续代码维护困难，请勿超过3层。

正例：超过3层的 if-else 的逻辑判断代码可以使 用卫语句、策略模式、状态模式等来实现，其中卫语句示例如下：

```java
public void today() {
    if (isBusy()) {
        Log.i(TAG,“change time.”);
        return;
    }
    if (isFree()) {
        Log.i(TAG,“go to travel.”);
        return;
    }
    Log.i(TAG,“stay at home to learn iWhaleCloud Java Coding Guidelines.”);
    return;
}
```

4. 【推荐】除常用方法（如getXxx/isXxx）等外，不要在条件判断中执行其它复杂的语句，将复杂逻辑判断的结果赋值给一个有意义的布尔变量名，以提高可读性。
   说明：很多if语句内的逻辑相当复杂，阅读者需要分析条件表达式的最终结果，才能明确什么样的条件执行什么样的语句，那么，如果阅读者分析逻辑表达式错误呢？

> 所属范围： Java代码部分
> 与Java规范差异：新增

正例：

```java
// 伪代码如下
final boolean existed = (file.open(fileName, "w") != null) && (...) || (...);
if (existed) {
    ...
}
```

<font color="red">反例</font>：

```java
if ((file.open(fileName, "w") != null) && (...) || (...)) {
    ...
}
```

5. 【推荐】循环体中的语句要考量性能，以下操作尽量移至循环体外处理，如定义对象、变量、获取数据库连接，进行不必要的try-catch操作（这个try-catch是否可以移至循环体外）。

> 所属范围： Java代码部分
> 与Java规范差异：新增

# 注释规约

1. 【强制】类、类属性、类方法的注释必须使用Javadoc规范，使用/* 内容 */格式，不得使用// xxx 方式。 说明：在IDE编辑窗口中，Javadoc 方式会提示相关注释， 生成Javadoc可以正确输出相应注释；在IDE中， 工程调用方法时，不进入方法即可悬浮提示方法、参数、返回值的意义，提高阅读效率。

> 所属范围： Java代码部分
> 与Java规范差异：新增

2. 【强制】所有的抽象方法（包括接 口中的 方法）必须要用Javadoc注释、除了返回值、参数、异常说明外，还必须指出该方法做什么事情，实现什么功能。

说明：对子类的实现要求，或者调用注意事项，请一并说明。

> 所属范围： Java代码部分
> 与Java规范差异：新增

3. 【强制】所有的类都必须添加创建者和创建日期。

> 所属范围： Java代码部分
> 与Java规范差异：新增

4. 【强制】 方法内部单行注释，在被注释语句上方另起一 行，使用//注释。 方法内部多行注释使用/* */注释，注意与代码对齐。

> 所属范围： Java代码部分
> 与Java规范差异：新增

5. 【强制】所有的枚举类型字段必须要有注释，说明每个数据项的用途。

> 所属范围： Java代码部分
> 与Java规范差异：新增

6. 【推荐】与其“半吊子”英文来注释，不如用中文注释把问题说清楚。专有名词与关键字保持英文原文即可。

<font color="red">反例</font>：“TCP连接超时”解释成“传输控制协议接超时”，理解反而费脑筋。

> 所属范围： Java代码部分
> 与Java规范差异：新增

7. 【推荐】代码修改的同时，注释也要进行相应的修改，尤其是参数、返回值、异常、核心逻辑等的修改。
   说明：代码与注释更新不同步，就像路网与导航软件更新不同步一样，如果导航软件严重滞后，就失去了导航的意义。

> 所属范围： Java代码部分
> 与Java规范差异：新增

8. 【参考】谨慎注释掉代码。在上方详细说明， 而不是简单地注释掉。如果无用，则删除。

> 所属范围： Java代码部分
> 与Java规范差异：新增

说明：代码被注释掉有两种可能性：

- 1）后续会恢复此段代码逻辑。
- 2）永久不用。前者如果没有备注信息，难以知晓注释动机。后者建议直接删掉（代码仓库保存了历史代码）。

9. 【参考】对于注释的要求：第一、能够准确反应设计思想和代码逻辑；第二、能够描述业务含义，使别的程序员能够迅速了解到代码背后的信息。完全没有注释的大段代码对于阅读者形同天书，注释是给自己看的，即使隔很长时间，也能清晰理解当时的思路；注释也是给继任者看的，使其能够快速接替自己的工作。

> 所属范围： Java代码部分
> 与Java规范差异：新增

10. 【参考】好的命名、代码结构是自解释的，注释力求精简准确、表达到位。避免出现注释的一个极端：过多过滥的注释，代码的逻辑一旦修改，修改注释是相当大的负担。

<font color="red">反例</font>：

```java
// put elephant into fridge 
put(elephant, fridge);  
```

方法名put，加上两个有意义的变量量名elephant和fridge，已经说明了这是在干什么，语义清晰的代码不需要额外的注释。

> 所属范围： Java代码部分
> 与Java规范差异：新增

11. 【参考】特殊注释标记，请注明标记人与标记时间。注意及时处理这些标记，通过标记扫描，经常清理此类标记。线上故障有时候就是来源于这些标记处的代码。

> 所属范围： Java代码部分
> 与Java规范差异：新增

- 1） 待办事宜（TODO）:（ 标记人，标记时间，[预计处理时间]） 表示需要实现，但目前还未实现的功能。这实际上是一个Javadoc的标签， 目前的Javadoc还没有实现，但已经被 广泛使用。只能应用于类，接口和方法（因为它是一个Javadoc标签）。
- 2） 错误，不能工作（FIXME）:（标记人，标记时间，[预计处理时间]） 在注释中用FIXME标记某代码是错误的， 而且不能工作，需要及时纠正的情况。

# 异常处理

1. 【强制】Java类库中定义的一类RuntimeException可以通过预先检查进行规避， 而不应该通过catch 来处理， 比如：IndexOutOfBoundsException，NullPointerException，NumberFormatException等等。
   说明： 无法通过预检查的异常除外，如IOException来实现。

> 所属范围： Java代码部分
> 与Java规范差异：新增

正例：

```java
if (obj != null) {...}
```

<font color="red">反例</font>：

```java
try { obj.method() } catch (NullPointerException e) {...}
```

2. 【强制】异常不要用来做流程控制，条件控制，因为异常的处理效率比条件分支低。

> 所属范围： Java代码部分
> 与Java规范差异：新增

3. 【强制】对大段代码进行try-catch，这是不负责任的表现。catch时请分清稳定代码和非稳定代码，稳定代码指的是无论如何不会出错的代码。对于非稳定代码的catch尽可能进行区分异常类型，再做对应的异常处理。

> 所属范围： Java代码部分
> 与Java规范差异：相同

4. 【强制】捕获异常是为了处理它，不要捕获了却什么都不处理而抛弃之，如果不想处理它，请将该异常抛给它的调用者。最外层的业务使用者，必须处理异常，将其转化为 用户可以理解的内容。

> 所属范围： Java代码部分
> 与Java规范差异：相同

5. 【强制】有try块放到了事务代码中，catch异常后，如果需要回滚事务， 一定要注意手动回滚事务。

> 所属范围： Java代码部分
> 与Java规范差异：新增

6. 【强制】finally块必须对资源对象、流对象进行关闭，有异常也要做try-catch。
   说明：如果JDK7及以上，可以使用try-with-resources 方式。

> 所属范围： Java代码部分
> 与Java规范差异：新增

7. 【强制】不能在finally块中使用return，finally块中的return返回后方法结束执行，不会再执行try块中的return语句。

> 所属范围： Java代码部分
> 与Java规范差异：新增

8. 【强制】捕获异常与抛异常，必须是完全匹配，或者捕获异常是抛异常的父类。 说明：如果预期对方抛的是绣球，实际接到的是铅球，就会产生意外情况。

> 所属范围： Java代码部分
> 与Java规范差异：新增

9. 【推荐】方法的返回值可以为null，不强制返回空集合，或者空对象等，必须添加注释充分说明什么情况下会返回null值。调用方需要进行null判断防止NPE问题。
   说明：本手册明确防止NPE是调用者的责任。即使被调用方法返回空集合或者空对象，对调用者来说，也并非高枕无忧，必须考虑到远程调用失败、序列列化失败、运行时异常等场景返回null的情况。

> 所属范围： Java代码部分
> 与Java规范差异：新增

10. 【参考】避免出现重复的代码（Don’t Repeat Yourself），即DRY原则。
    说明：随意复制和粘贴代码，必然会导致代码的重复，在以后需要修改时，需要修改所有的副本，容易遗漏。必要时抽取共性方法，或者抽象公共类，甚至是组件化。

> 所属范围： Java代码部分
> 与Java规范差异：新增

# 检测工具

依据上面规范，Android 编程规范小组，自定义了 Android Lint 的检测规则

## Android Lint

- Google 官方的支持，会和 Android 开发工具一起升级完善。
- Android Studio、Android Gradle 插件原生支持 Lint 工具。
- 扩展性强，支持开发自定义 Lint 规则（Android 编程规范小组自定义了 Lint 规则 jar 包）。
- Lint 支持 Java 源文件、class 文件、资源文件、Gradle 等文件的检查。
- Lint 专为 Android 设计，原生提供了几百个实用的 Android 相关检查规则。
- 数据流分析。

详细的Android Lint工具使用介绍，参见本文档附录一

# 安全

## 敏感数据

1. 【强制】在设备本地保存数据时，不使用明文存储敏感数据，如果确实需要，应对敏感数据进行加密处理后再保存
   【自动/工具检查手段】暂无

> 源于 11537910 新电gomo app安全问题治理-在Android APP中，诸如手机号码、客户编号、账号、授权承载令牌以及客户套餐详情等敏感信息通过设备日志文件被泄露。

说明：

- 如果将敏感数据存储在 Android 设备中，由于环境是不安全的，这将可能导致存储的敏感数据泄露。攻击者可以使用 adb 命令连接 Android 系统，访问/data/data//目录下的 shared_prefs、 databases 等目录，查看其中存储数据的文件，通常是.xml 或.db 结尾的文件。所以，应用在 Android 设备本地存储敏感数据时，应进行加密存储。
- Shared Preferences 是比较常用的数据存储方法，它通过XML结构将键/值对数据持久存储在文件系统中。下面代码是使用 Shared Preferences 来明文存储账号和密码敏感信息的例子。一旦程序被执行，文件 key.xml就会被创建并存储这些敏感数据，这样会导致账号和密码这样敏感的信息被明文存储在文件/data/data//shared_prefs/key.xml中。
- SQLite 也是 Android 中常用的数据存储方式，Android SDK 内置了 SQLite 数据库支持。以下代码用明文存储像账号和密码这样的敏感信息。一旦程序被执行，数据库文件 privateNotSoSecure 就通过提供的数据被创建，账号密码被明文保存在/data/data//databases/privateNotSoSecure 中。

<font color="red">反例</font>:

```java
// Shared Preferences
SharedPreferences sharedPref = getSharedPreferences("key", MODE_WORLD_READABLE);
SharedPreferences.Editor editor = sharedPref.edit();
editor.putString("username", "administrator");
editor.putString("password", "supersecret");
editor.commit();

// SQLite
SQLiteDatabase notSoSecure = openOrCreateDatabase("privateNotSoSecure",MODE_PRIVATE,null);
notSoSecure.execSQL("CREATE TABLE IF NOT EXISTS Accounts(Username VARCHAR, Password VARCHAR);");
notSoSecure.execSQL("INSERT INTO Accounts VALUES('admin','AdminPass');");
notSoSecure.close();
```

正例：

```java
// Shared Preferences
private static byte[] encrypt( byte[] raw, byte[] clear ) throws Exception {
SecretKeySpec skeySpec = new SecretKeySpec( raw, "AES" );
Cipher cipher = Cipher.getInstance( "AES/CBC/PKCS5Padding" );
cipher.init( Cipher.ENCRYPT_MODE, skeySpec, new IvParameterSpec( new byte[cipher.getBlockSize()] ) ) ；
byte[] encrypted = cipher.doFinal( clear );
return encrypted;
}

//SQLite
public class HelloSQLCipherActivity extends Activity {
  @Override
  public void onCreate(Bundle savedInstanceState) {
    super.onCreate(savedInstanceState);
    setContentView(R.layout.main);
    InitializeSQLCipher();
  }

  private void InitializeSQLCipher() {
    SQLiteDatabase.loadLibs(this); // Step1：初始化 native 库；
    File databaseFile = getDatabasePath("demo.db"); // Step2：选择数据库路径；
    databaseFile.mkdirs();
    databaseFile.delete();
    SQLiteDatabase database = SQLiteDatabase.openOrCreateDatabase(databaseFile, password,null); // Step3：创建有加密密码的数据库。SQLCipher 会使用该密码对数据库进行整体加密。不要硬编码密码。
    database.execSQL("create table t1(a, b)")
    database.execSQL("insert into t1(a, b) values(?, ?)", new Object[]{"one for the money", "two for the show"});
  }
}

```

2. 【强制】禁止将密钥进行硬编码存储
   【自动/工具检查手段】暂无

说明：

- 如果密钥以明文字符串形式存储在代码中，攻击者可以通过反编译的方式获取应用代码和加密密钥，这将导致加密数据被解密还原的风险，密钥需要在AndroidKeyStore 中保存。
- AndroidKeyStore 是在 Android 4.3 引入的特性，如果应用需要支持 Android 4.0，比较安全的保存密钥的方案是使用白盒加密技术，即通过技术把密钥隐藏在代码中，增大攻击者获取密钥的难度，以达到安全保存密钥的目的，鉴于白盒加密技术的难度，建议可以选用已有的成熟的解决方案。如果上述方案不好实现，那么可以将密钥放在 so 文件中，建议将密钥分段放在多处，增大攻击者的分析难度。此外再对 so 文件等源码进行混淆和加固，以增大攻击者对源码内容的分析难度。

<font color="red">反例</font>：

```java
public class AESCoder {
  private static final String KEY_ALGORITHM = "AES";
  private static final String CIPHER_ALGORITHM = "AES/CBC/PKCS5Padding";
  private static final String KEY_STRING = "11zqfOdYzxruZBIY52Azxg==";
  private static final String IV_STRING = "3SXy33DeoYX5Zis1";
  private static final String charset = "UTF-8";
  public static String encrypt( String content ) throws Exception {
    IvParameterSpec iv = new IvParameterSpec( IV_STRING.getBytes() );
    SecretKey secretKey = new SecretKeySpec( KEY_STRING.getBytes(), KEY_ALGORITHM );
    Cipher cipher = Cipher.getInstance( CIPHER_ALGORITHM );
    cipher.init( Cipher.ENCRYPT_MODE, secretKey, iv );
    byte[] outputData = cipher.doFinal( content.getBytes( charset ) );
    return(URLEncoder.encode( new BASE64Encoder().encode( outputData ) ) );
  }

  public static String decrypt( String content ) throws Exception {
    IvParameterSpec iv = new IvParameterSpec( IV_STRING.getBytes() );
    SecretKey secretKey = new SecretKeySpec( KEY_STRING.getBytes(), KEY_ALGORITHM );
    Cipher cipher = Cipher.getInstance( CIPHER_ALGORITHM );
    cipher.init( Cipher.DECRYPT_MODE, secretKey, iv );
    content = URLDecoder.decode( content );
    byte[] outputData = cipher.doFinal( new BASE64Decoder().decodeBuffer( content ) );
    return(new String( outputData, charset ) );
  }
} 
```

正例：

```java
private SecretKey getSecretKey(final String alias) throws NoSuchAlgorithmException, NoSuchProviderException, InvalidAlgorithmParameterException {
  final KeyGenerator keyGenerator = KeyGenerator 
               .getInstance(KeyProperties.KEY_ALGORITHM_AES, ANDROID_KEY_STORE);

  keyGenerator.init(new KeyGenParameterSpec.Builder(alias, 
               KeyProperties.PURPOSE_ENCRYPT|KeyProperties.PURPOSE_DECRYPT) 
               .setBlockModes(KeyProperties.BLOCK_MODE_GCM) 
               .setEncryptionPaddings(KeyProperties.ENCRYPTION_PADDING_NONE) 
               .build());
  return keyGenerator.generateKey();
}
```

3. 【强制】应用记录日志信息时，不应记录任何敏感信息
   【自动/工具检查手段】梆梆可检查是否禁止调试日志输出

说明：

- 通常应用在运行时会将一些运行过程的信息写到日志记录中。如果日志中记录了敏感信息，而这样的日志信息在客户端是不安全，容易导致这些敏感信息泄露。攻击者可以在运行应用的时候使用 logcat 工具查看应用运行时候输出的日志信息，如果其中包含敏感信息，就会导致敏感信息泄露。所以，发布正式版本的时候关闭日志的 debug 开关或者不将敏感信息写到日志中。

<font color="red">反例</font>：

```java
String username = "log_leak";
String password = "log_leak_pwd";
Log.d("MY_APP", "usesname" + username);
Log.d ("MY_APP", "password" + password, new Throwable ());
Log.v ("MY_APP", "send message to server ");
```

正例：

```java
public class LogUtil {
  private static boolean DEBUG =false;
  public static void d(String tag, String msg) {
    if (DEBUG) android.util.Log.d(TAG, msg);
  }
}
```

4. 【建议】在涉及敏感数据输入文本框中，应禁用键盘缓存
   【自动/工具检查手段】暂无
5. 【建议】在涉及敏感数据的文本框中，应停用剪切板功能
   【自动/工具检查手段】梆梆
6. 【建议】当敏感数据需要显示在前端页面时，对敏感信息进行脱敏处理
   【自动/工具检查手段】暂无
7. 【强制】在进行业务查询时，应仅返回满足业务需要的数据，不应返回多余的敏感信息
   【自动/工具检查手段】暂无
8. 【强制】不要广播敏感信息，只能在本应用使用 LocalBroadcast，避免被别的应用收到，或者 setPackage 做限制。
   【自动/工具检查手段】暂无

## 加密强度不足

1. 【建议】不使用弱随机数,使用安全的随机数生成方式
   【自动/工具检查手段】梆梆

通常，使用随机数的场景包括但不限于如下场景：

- 1）生成密钥：对称密码，消息认证
- 2）生成密钥对：公钥密码，数字签名
- 3）生成 IV： 用于分组密码的 CBC，CFB 和 OFB 模式
- 4）生成 nonce: 用于防御重放攻击; 分组密码的 CTR 模式
- 5）生成盐：用于基于口令的密码 PBE 等

说明：

- 由于使用弱随机函数生成随机数时，在相同初始向量的情况下会生存相同的随机数，因此通过这样方式生成的随机数没有足够的随机性，存在被破解的风险。使用相同的种子就可以生成相同的随机数，攻击者如果获得了应用随机数生成的种子，那么攻击者就可以破解应用中使用随机数场景的安全控制。

<font color="red">反例</font>

```java
public static void testRandom(){
  Random random = new Random(1);
  for(int i=0; i<5;i++){
     System.out.print(random.nextInt()+"\t");
  }
  
  System.out.println("");
}
```

正例

```java
import java.security.SecureRandom;
import java.security.NoSuchAlgorithmException;
// ...
public static void main (String args[]) {
  SecureRandom number = new SecureRandom();
  // Generate 20 integers 0..20
  for (int i = 0; i < 20; i++) {
    System.out.println(number.nextInt(21));
  }
}

```

2. 【强制】引入加密算法时使用安全的加密算法
   【自动/工具检查手段】梆梆可检查AES，DES，RSA

说明：

- 不安全的加密算法都是已经被破解的算法，使用它们加密的数据已不再安全，对于不安全的加密算法可以使用暴力破解或者破解工具来对密文数据进行破解。
- 使用以下加密算法时，密钥的长度应满足：AES 256 及以上长度；RSA 2048 及以上长度；ECC 256 及以上长度；SM2 256 及以上长度；SHA256 256；SM3 256。
- 使用 AES/DES/DESede 等加密算法时，不要使用默认的加密模式 ECB，应显示指定使用 CBC 或 CFB 加密模式。

<font color="red">反例</font>：

```java
public void generateKey() throws Exception {
  KeyGenerator keyGen = KeyGenerator.getInstance( "DES" );
  keyGen.init( 56 );
  key = keyGen.generateKey();
}

public byte[] des_encrypt( byte[] plainText ) throws Exception {
  Cipher cipher = Cipher.getInstance( "DES/ECB/PKCS5Padding" );
  cipher.init( Cipher.ENCRYPT_MODE, key );
  byte[] cipherText = cipher.doFinal( plainText );
  return(cipherText);
}

// 密钥长度没有达到安全要求。
public static KeyPair getRSAKey() throws NoSuchAlgorithmException {
  KeyPairGenerator keyGen = KeyPairGenerator.getInstance( "RSA" );
  keyGen.initialize( 512 );
  KeyPair key = keyGen.generateKeyPair();
  return(key);
}

// 不安全的MD5加密算法
MessageDigest md = MessageDigest.getInstance("MD5");
try {
  md.update(toChapter1);
  MessageDigest tc1 = md.clone();
  byte[] toChapter1Digest = tc1.digest();
  md.update(toChapter2);
  …

} catch (CloneNotSupportedException cnse) {
  throw new DigestException("couldn't make digest of partial content");
}
```

正例

```java
private static byte[] encrypt( byte[] raw, byte[] clear ) throws Exception {
  SecretKeySpec skeySpec= new SecretKeySpec( raw, "AES" );
  Cipher cipher = Cipher.getInstance( "AES/CBC/PKCS5Padding" );
  cipher.init( Cipher.ENCRYPT_MODE, skeySpec, new IvParameterSpec( new byte[cipher.getBlockSize()] ) ) ；
  byte[] encrypted = cipher.doFinal( clear ); return(encrypted);
}

private static byte[] decrypt( byte[] raw, byte[] encrypted ) throws Exception {
  SecretKeySpec skeySpec= new SecretKeySpec( raw, "AES" );
  Cipher cipher = Cipher.getInstance( "AES/CBC/PKCS5Padding" );
  cipher.init( Cipher.DECRYPT_MODE, skeySpec, new IvParameterSpec( new byte[cipher.getBlockSize()] ) );
  byte[] decrypted = cipher.doFinal( encrypted ); 
  return(decrypted);
}

//使用 RSA 加密，密钥长度为 2048 位。
public static KeyPair getRSAKey() throws NoSuchAlgorithmException {
  KeyPairGenerator keyGen = KeyPairGenerator.getInstance( "RSA" );
  keyGen.initialize( 2048 );
  KeyPair key = keyGen.generateKeyPair();
  return(key);
}

// 使用 SHA256 哈希算法。
MessageDigest md = MessageDigest.getInstance("SHA-256");
try {
  md.update(toChapter1);
  MessageDigest tc1 = md.clone();
  byte[] toChapter1Digest = tc1.digest(); md.update(toChapter2);
  …
} catch (CloneNotSupportedException cnse) {
  throw new DigestException("couldn't make digest of partial content");
}
```

## 通信安全

1. 【强制】通信过程需要使用HTTPS加密传输
   【自动/工具检查手段】梆梆

说明：

- 应用使用 HTTP 协议进行网络数据交互，由于 HTTP 是明文传输数据，在不可信的网络环境下，网络请求可能被中间人攻击（Man-in-the-MiddleAttack）， 导致传输的敏感信息被中间人获取或篡改。攻击者可以通过工具对网络中传输的数据进行嗅探，如果应用使用 HTTP 明文传输数据，那么传输的敏感数据将会被泄露。所以，应用在通过网络传输数据时，需要使用HTTPS加密。

<font color="red">反例</font>

```java
// HttpURLConnection
URL url = new URL("http://www.baidu.com");
connection = (HttpURLConnection) url.openConnection();
connection.setRequestMethod("GET");
connection.setConnectTimeout(5000);
connection.setReadTimeout(5000);
InputStream in = connection.getInputStream();
connection.disconnect()

// OKHttp 
OkHttpClient client = new OkHttpClient();
Request request = new Request.Builder().url("http://www.baidu.com").build();
try {
  Response response = client.newCall(request).execute();
  String result = response.body().string();
  Log.d(TAG, "result: "+result); show(result);
} catch (IOException e) {
  e.printStackTrace();
}

```

正例

```java
// HttpURLConnection
URL url = new URL("https://www.baidu.com");
connection = (HttpURLConnection) url.openConnection();
connection.setRequestMethod("GET");
connection.setConnectTimeout(5000);
connection.setReadTimeout(5000);
InputStream in = connection.getInputStream(); connection.disconnect();

// OKHttp
Uri uri = Uri.parse("https://www.example.com")
  .buildUpon()
  .appendQueryParameter("name", query)
  .appendQueryParameter("category", "student")
  .build();
URL url = buildURL(uri);
Request request = buildRequest(url).build();
```

2. 【强制】HTTPS通信过程中需要对服务器证书进行验证
   【自动/工具检查手段】梆梆

说明：

- 应用在使用证书时，如果没有对服务端提交的证书进行安全检查，就可能导致在不可信的网络环境中的数据请求被进行中间人攻击，导致传输的敏感信息被中间人获取或篡改。使用假的证书冒充服务端与客户端通信，由于客户端未对正式进行恰当的安全验证，就可以导致用假证书冒充与客户端通信成功。所以应用在网络通信使用自签名证书时，需要进行正确验证。

<font color="red">反例</font>:

```java
// 没有校验证书
TrustManager tm = new X509TrustManager() {
  public void checkClientTrusted( X509Certificate[] chain, String authType )throws CertificateException {
    /* do nothing */
  }

  public void checkServerTrusted( X509Certificate[] chain, String authType )throws CertificateException {
   /* do nothing*/
  }

  public X509Certificate[] getAcceptedIssuers() {
    return(null);
  }
};

sslContext.init( null, new TrustManager[] { tm }, null );


// 忽略证书异常校验。
webview.setWebViewClient (new WebViewClient() {
  @Override
  public void onReceivedSslError( WebView view, SslErrorHandler handler, SslError error ) {
    /* 接受所有网站的证书，忽略 SSL 错误 */
    handler.proceed();
  }
}

```

正例

```java
try {
  CertificateFactory cf = CertificateFactory.getInstance( "X.509" );
  /* uwca.crt 打包在 asset 中 */
  InputStream caInput = new BufferedInputStream( getAssets().open( "uwca.crt" ) );
  final Certificate ca;
  try {
    ca = cf.generateCertificate( caInput );
    Log.i( "Longer", "ca=" + ( (X509Certificate) ca).getSubjectDN() );
    Log.i( "Longer", "key=" + ( (X509Certificate) ca).getPublicKey() );
  } finally {
     caInput.close();
  }

  /* Create an SSLContext that uses our TrustManager */

  SSLContext context = SSLContext.getInstance( "TLSv1.2", "AndroidOpenSSL" );
  context.init( null, new TrustManager[] {new X509TrustManager() {
    @Override
    public void checkClientTrusted( X509Certificate[] chain, String authType )throws CertificateException {

    }

    @Override
    public void checkServerTrusted( X509Certificate[] chain, String authType )throws CertificateException {
      for ( X509Certificate cert: chain ) {
        /* Make sure that it hasn't expired. */
        cert.checkValidity();
        /* Verify the certificate's public key chain. */
        try {
          cert.verify(((X509Certificate) ca).getPublicKey() );
        } catch ( NoSuchAlgorithmException e ) {
          e.printStackTrace();
        } catch ( InvalidKeyException e ) {
          e.printStackTrace();
        } catch ( NoSuchProviderException e ) {
          e.printStackTrace();
        } catch ( SignatureException e ) {
          e.printStackTrace();
        }
      }
    }
    @Override
    public X509Certificate[] getAcceptedIssuers() {
      return(new X509Certificate[0]);
    }
  }
}, null );

  URL url = new URL( "https://certs.cac.washington.edu/CAtest/" );
  HttpsURLConnection urlConnection = (HttpsURLConnection) url.openConnection();
  urlConnection.setSSLSocketFactory( context.getSocketFactory() );
  InputStream in = urlConnection.getInputStream();
  copyInputStreamToOutputStream( in, System.out );
} catch ( CertificateException e ) {
  e.printStackTrace();
} catch ( IOException e ) {
  e.printStackTrace();
} catch ( NoSuchAlgorithmException e ) {
  e.printStackTrace();
} catch ( KeyManagementException e ) {
  e.printStackTrace();
} catch ( NoSuchProviderException e ) {
  e.printStackTrace();
}

//处理证书校验异常，以下示例对证书校验异常进行处理。
public void onReceivedSslError( WebView view, SslErrorHandler handler, SslError error ) {
  paramSslErrorHandler.cancel();
}

```

3. 【强制】HTTPS通信过程中，需要进行主机名校验
   【自动/工具检查手段】梆梆

说明：

- 在实现的 HostnameVerifier 子类中，使用 verify 函数效验服务器主机名的合法性，否则会导致恶意程序利用中间人攻击绕过主机名效验。

<font color="red">反例</font>

```java
final static HostnameVerifier NO_VERIFY = new HostnameVerifier() {
  public boolean verify(String hostname, SSLSession session) {
    return true;
  }
}

```

正例

```java

final HostnameVerifier hostnameverifier = new HostnameVerifier() {
  public boolean verify(String hostname, SSLSession session) {
    HostnameVerifier hv = HttpURLConnection.getDefaultHostnameVerifier();
    Boolean result = hv.verify("*.example.com",session) return result;
  }
};

```

4. 【强制】在 HTTPS 通信中，验证策略需要改成严格模式
   【自动/工具检查手段】梆梆

说明：

- Android APP 在 HTTPS 通信中，使用 ALLOW_ALL_HOSTNAME_VERIFIER 关闭 host 验证，表示允许和 所有的 HOST 建立 SSL 通信，这会存在中间人攻击的风险，最终导致敏感信息可能会被劫持，以及其他形式的攻击，需要使用 STRICT_HOSTNAME_VERIFIER 模式。

<font color="red">反例</font>

```java
SSLSocketFactory sf = new MySSLSocketFactory(trustStore);
sf.setHostnameVerifier(SSLSocketFactory.ALLOW_ALL_HOSTNAME_VERIFIER);
```

正例

```java
SSLSocketFactory sf = new MySSLSocketFactory(trustStore);
sf.setHostnameVerifier(SSLSocketFactory.STRICT_HOSTNAME_VERIFIER);
```

## 异常处理

1. 【强制】对异常进行恰当的处理，并不暴露敏感信息
   【自动/工具检查手段】暂无

说明

- 如果应用未对异常进行恰当的处理，不仅可能会影响应用的正常使用，而且其暴露的内部异常提示信息也可能被攻击者利用来攻击应用。

<font color="red">反例</font>

```java
try {
  //...
} catch (IOException ioe) {
  ioe.printStackTrace();
}

// 暴露敏感信息
try {
  FileInputStream fis = new FileInputStream(System.getenv("APPDATA") + args[0]);
} catch (FileNotFoundException e) {
  // Log the exception
  throw new IOException("Unable to retrieve file", e);
}
```

## 组件使用安全

1. 【强制】对应用组件的访问进行限制
   【自动/工具检查手段】梆梆可检查 Activity组件导出风险，Service组件导出风险，Broadcast Receiver组件导出风险，Content Provider组件导出风险

说明：

- 在 AndroidManifest.xml 配置文件中配置应用组件（activity、service、 content provider 或 broadcast receiver）是否可被其他应用访问时。如果敏感组件的导出属性（android:exported）没有被恰当的设置，可能导致敏感组件可以被外部应用访问，那么就可能存在恶意应用访问这样的敏感组件， 这将可能导致严重的安全问题。
- 不能在毫无权限控制的情况下，将 android:exported 设置为 true。对于内部使用的组件，显示设置组件的"android:exported"属性为 false

<font color="red">反例</font>

```xml
<service android:exported="true" android:name=".AuthService" android:process=":remote"/>
```

正例

```xml
<service android:exported="false" android:name=".AuthService" android:process=":remote"/>
```

2. 【强制】禁止使用空intent，禁止intent组件隐式调用
   【自动/工具检查手段】梆梆

说明：

- Intent通常用于Activity、Service、Broadcast Receiver等组件之间进行信息传递，包括发送端和接收端。当使用隐式的Intent调用时，并未对intent消息接收端进行限制，因此可能存在该消息被未知的第三方应用劫持的风险。Intent消息被劫持，可能导致用户的敏感数据泄露，或者恶意程序执行等风险，故需要采用显式方式调用Intent组件，使用指定Intent消息接收方。

3. 【强制】接受intent数据时，应用需要进行安全检查
   【自动/工具检查手段】暂无

说明：

- 应用之间可以非常方便的使用 intent 来传递数据，但是如果应用未对其接受的数据进行恰当的验证就直接进行处理，那么应用在接受到攻击者通过 intent 发送的恶意数据时，就可能导致应用拒绝服务，被注入等风险。在接受或处理其它应用 intent 发送的消息时，不要响应恶意 intent。

<font color="red">反例</font>

```java
Intent intent = new Intent(this, NextActivity.class);
intent.putExtra("URL", url);
startActivity(intent);
...
Intent intent = getIntent();
String user_name = intent.getStringExtra("URL");
```

4. 【强制】对 URL Schemes 接收数据进行检查，限制应用调用
   【自动/工具检查手段】梆梆

说明：

- 如果应用没有正确验证 URL 及其参数的情况下，处理对其 URL schemes 的调用，以及在触发重要操作之前未提示用户进行确认。当恶意应用在 URL schemes 中发送了恶意数据， 就可能会对正常应用产生安全影响。

5. 【强制】将所需要动态加载的文件放置在 apk 内部，或应用私有目录中，如果应用必须要把所加载的文件放置在可被其他应用读写的目录中(比如 sdcard)，建议对不可信的加载源进行完整性校验和白名单处理，以保证不被恶意代码注入
   【自动/工具检查手段】暂无
6. 【强制】使用参数化查询防 SQL 注入，也可以对输入数据进行检查，不接受非法字符，防御 Content Provider SQL 注入
   【自动/工具检查手段】暂无

说明：

- 如果某个 provider 被设置为外部应用可访问，那么只要知道其访问数据的地址就可以在外部请求数据。如果应用对接收到的数据没有进行验证，那么攻击者发送精心构造的恶意数据时就可能导致注入攻击。

<font color="red">反例</font>

```java
// 使用拼接 SQL 的方式
String sql = "select * from user where id=‘" + userInputID +"‘"; Cursor curALL = db.rawQuery(sql, null);
```

正例

```java
//参数化查询
DatabaseHelper dbhelper = new DatabaseHelper(SqliteActivity.this,"sqliteDB");
SQLiteDatabase db = dbhelper.getReadableDatabase();
String[] selectionArgs = new String[]{userInputID , userInputName };
String sql = "select * from user where id=? and name=?";
Cursor curALL = db.rawQuery(sql, selectionArgs);

//非法字符检查
public boolean isAlphaNumeric(String s){
  String pattern= "^[a-zA-Z0-9]*$";
  return s.matches(pattern);
}
```

7. 【建议】使用 ContentProvider.openFile()之前调用 Uri.decode()对路径参数进行处理，防御 Content Provider 本地文件遍历。
   【自动/工具检查手段】暂无

说明：

- 当代码中访问的文件来自于用户传递的参数，而程序又未对此参数进行任何检查，如果攻击者提交恶意数据，那么就可能导致访问更改访问目录，遍历系统中所有文件。

<font color="red">反例</font>

```java
private static String IMAGE_DIRECTORY = localFile.getAbsolutePath();
public ParcelFileDescriptor openFile( Uri paramUri, String paramString ) throws FileNotFoundException {
  File file = new File( IMAGE_DIRECTORY, paramUri.getLastPathSegment() );
  return(ParcelFileDescriptor.open( file, ParcelFileDescriptor.MODE_READ_ONLY ) );
}

```

正例

```java
private static String IMAGE_DIRECTORY = localFile.getAbsolutePath();
public ParcelFileDescriptor openFile( Uri paramUri, String paramString ) throws FileNotFoundException {
  String decodedUriString = Uri.decode( paramUri.toString() );
  File file = new File( IMAGE_DIRECTORY, Uri.parse( decodedUriString ).getLastPathSegment() );
  if ( file.getCanonicalPath().indexOf( localFile.getCanonicalPath() ) != 0 ) {
    throw new IllegalArgumentException();
  }
  return(ParcelFileDescriptor.open( file, ParcelFileDescriptor.MODE_READ_ONLY ) );
}
```

## WebView安全

Android 中的 WebView 和我们平常使用的浏览器类似，因此浏览器面临的一些问题，在 WebView 中也可能出现。

1. 【强制】禁止WebView启用JavaScript，如果需要启用，需要进行相关的安全防护
   【自动/工具检查手段】梆梆

说明

- API level>=17，允许 js 被调用的函数必须以@JavascriptInterface 进行注解；
- 对于 API level < 17，可能会使用到 addJavascriptInterface，addJavascriptInterface 方法允许暴露 Java 对象给 WebView，Android 可以在 WebView 中执行 JavaScript 来调用 Android 的 native 方法。默认所有 Java 方法都暴露给 JavaScript，这就可能会导致非常严重的安全问题。如果一定要用到，

建议：

- 1)使用 https 协议加载 URL，使用证书校验，防止访问的页面被篡改挂马；
- 2)对加载 URL 做白名单过滤、完整性校验等防止访问的页面被篡改；
- 3)如果加载本地 html,应该会 HTML 内置在 APK 中，以及对 HTML 页面进行完整性校验。

2. 【建议】对WebView访问本地资源文件进行限制
   【自动/工具检查手段】梆梆

说明：

- 应用可以通过 WebView 来访问本地资源或文件，如果没有对访问的文件位置进行检查，那么就可能导致访问任意本地文件的问题。防御 WebView 访问本地任意文件可以停用本地文件访问操作，如果确实需要访问本地文件，则应该只允许访问指定的本地文件，不允许对访问的文件及文件路径进行任何修改。

<font color="red">反例</font>

```java
webview.loadUrl("file:///" + Environment.getExternalStorageDirectory().getPath() + filename);
```

正例

```java
webView.getSettings().setAllowFileAccess(false); 
webView.getSettings().setAllowFileAccessFromFileURLs(false); 
webView.getSettings().setAllowUniversalAccessFromFileURLs(false); 
webView.getSettings().setAllowContentAccess(false);
```

## 发布安全

1. 【强制】在对应用进行签名时，应使用有效的证书进行签名
   【自动/工具检查手段】梆梆，证书管理

2. 【强制】在应用发布前应将其调试模式设置为不可调试 android:debuggable=false
   【自动/工具检查手段】梆梆

3. 【强制】应用发布前，调试符号应从原生二进制文件中删除，调试代码应进行删除
   【自动/工具检查手段】人工检查

4. 【强制】将 android:allowbackup 属性设置为 false，防止 adb backup 导出数据，避免本地数据泄露
   【自动/工具检查手段】梆梆

5. 【强制】正式发布的包文件需执行安全加固流程对apk/aab文件执行安全加固

   > 补充要求 ：执行安全加固后，研发所内的出厂测试、CD，以及现场的UAT、BRT，都必须测试安全加固后的版本，充分验证加固后APP的兼容性
   > 规范来源：故障单号：3796792

   【自动/工具检查手段】发布流程控制

6. 【强制】应用加固后，应进行重签
   采用绑绑加固后，应进行重新加签。
   研发云已经在加固节点上，支持加签
   ![image](uploads/214660/d6d3be14-594f-455f-91c0-fc48b1ccb081/image.png)
   ![image](uploads/214660/70ffb2a6-4698-4adc-875b-406e379ba1d4/image.png)

   【自动/工具检查手段】发布流程控制

   > 规范来源：严重生产故障3789946

## Android版本安全

1. 禁止APP在低版本Android系统运行，推荐支持最低版本为10.0（android API 29）

> 源于 11546904 新电gomo app安全问题治理-  can be installed in unpatched android version

说明：Android低版本漏洞较多，并且已经过时，可以结合客户需求定义支持的Android版本，如客户没有要求最低版本为10.0（android API 29）
![image](uploads/218815/c031ea9a-7869-4e32-bceb-1da43143b14a/image.png)

## 应用自身防护

1. 禁止使用URL Schemes唤醒应用

   > 源于 11546904 新电gomo app安全问题治理- Abuse of URL Schemes

   说明：可以结合客户需求考虑是否支持URL Schemes唤醒

2. 应用在申请用户权限时只申请必要的权限，申请的权限需要用户授予后才能使用

   > 源于 | 11547236 新电gomo app安全问题治理- Excessive Application Permissions

3. 禁止应用程序允许另一个应用程序在其之上运行

   > 源于 | 11537910 新电gomo app安全问题治理- No Tapjacking Protection

   说明：非常规安全要求，影响用户体验

4. 应用切换到后台时，应该对界面敏感数据进行模糊化处理

   > 源于 | 11537913 新电gomo app安全问题治理- Sensitive Information Included in Snapshots

   说明：可以结合客户需求考虑

5. 对于包含敏感数据页面应该禁止截图

   > 源于 | 11537913 新电gomo app安全问题治理- Sensitive Information Included in Snapshots

   说明：可以结合客户需求考虑

# 其它

1. 【强制】在使用正则表达式时，利用好其预编译功能，可以有效加快正则匹配速度。
   说明：不要在 方法体内定义：Pattern pattern = Pattern.compile(规则);

> 所属范围： Java代码部分
> 与Java规范差异：新增

2. 【强制】注意 Math.random() 这个方法返回是double类型，注意取值的范围0≤x<1（能够取到零值，注意除零异常），如果想获取整数类型的随机数，不要将x放大10的若干倍然后取整，直接使用Random对象的nextInt或者nextLong 方法。

> 所属范围： Java代码部分
> 与Java规范差异：新增

3. 【强制】获取当前毫秒数System.currentTimeMillis();  而不是new Date().getTime();
   说明：如果想获取更加精确的纳秒级时间值，使用System.nanoTime()的方式。在JDK8中，针对统计时间等场景，推荐使用Instant类。

> 所属范围： Java代码部分
> 与Java规范差异：新增

4. 【推荐】及时清理不再使用的代码段或配置信息。 说明：对于垃圾代码或过时配置，坚决清理干净，避免程序过度臃肿，代码冗余。

正例：对于暂时被注释掉，后续可能恢复使用的代码片断，在注释代码上方，统一规定使用三个斜杠(///)来说明注释掉代码的理由。

> 所属范围： Java代码部分
> 与Java规范差异：新增

5. 【建议】AdapterViewChildren  AdapterViews 如 ListViews 必须设置Adapter 如 ListAdapter。

> 所属范围： Java代码部分
> 与Java规范差异：新增

6. 【建议】对于versionCode属性，必须指定一个实际的整数不能将间接调用与@ dimen / name资源。

> 所属范围： Android资源文件
> 与Java规范差异：新增

7. 【强制】TextView布局文件中硬编码text，应该使用@string。

> 所属范围： Android资源文件
> 与Java规范差异：新增

8. 【建议】调用String＃toLowerCase（）或#toUpperCase（）需指定语言环境。

> 所属范围： Java代码部分
> 与Java规范差异：新增

9. 【建议】ImageView需要设置 contentDescription属性。

> 所属范围： Android资源文件
> 与Java规范差异：新增

10. 【强制】任何时候不要硬编码文件路径，如/sdcard，请使用 Android 文件系统 API 访问。

> 所属范围： Java代码部分
> 与Java规范差异：新增

11. 【强制】android:allowbackup 属性必须设置为 false，阻止应用数据被导出。

> 所属范围： Android资源文件
> 与Java规范差异：新增

12. 【强制】不能使用过时的类或方法。

> 所属范围： Java代码部分
> 与Java规范差异：新增

13. 【强制】ScrollView子view需要设置layout_width 或者layout_height 为wrap_content而不是fill_parent、 match_parent。

> 所属范围： Android资源文件
> 与Java规范差异：新增

14. 【强制】上传照片或附件时，需要进行文件大小的限制校验

> 源于严重生产故障 3566083 esale APP 客户注册上传照片有两种方式，一种是拍照上传，另一种是直接手动上传拍好的照片。直接手动上传的时候做了10M大小的限制，但是在拍照上传的场景下没有做大小限制，针对拍照上传的场景，会直接调用后端的压缩接口来压缩照片，由于图片大小没有限制，导致图片压缩开源插件的使用没有考虑循环压缩会出现的性能问题，CPU和内存资源被耗尽

# 附录

## 附录一 研发云Android CI流程代码分析工具Lint

### Lint介绍

Lint工具是Google提供的Android静态代码检查工具，可以扫描并发现代码中潜在的问题。除了提供的几百个lint规则，还可以开发自定义lint规则以满足定制化需求。通过分析可以生成html和xml两种格式的报告文件，以便您可以快速确定需要优先进行的关键改进

### 使用默认的Lint规则扫描使用

在集成的Android Studio中菜单方式的显示操作 或 以命令行(gradle lint)方式执行

### 使用前提

JAVA + AndroidSDK + Gradle (windows/Linux/Mac)

### 研发云Lint的扫描规则文件

位于镜像：/home/ZCIPClient/tools/appCheck/config 目录

```shell
cd app/src/main
/opt/android_sdk/cmdline-tools/bin/lint --config /home/ZCIPClient/tools/appCheck/config/lint.xml --xml AppCheck_Result.xml ./
```

注：与项目lint配置无关，使用公司统一lint规则文件。

Lint最终生成的文件 html/xml 图示

- Html格式的扫描报告

![image](uploads/46176/9b4c19d4-62dc-4fbc-9a24-dff549930cc7/image.png)

![image](uploads/46176/c113af48-e896-437d-a0b2-f75b600bd4bd/image.png)

- Xml格式扫描报告

![image](uploads/46176/741d3972-ff56-4fc2-909c-be1c0f639ddf/image.png)

## 附录二 研发云Android CI流程配置说明

### 流程创建及环境选择

![image](uploads/46176/e0baed8d-c0b5-441e-8028-3116b926a61d/image.png)

- 语言模板选择APP
- 基础镜像选择后两个多SDK版本的

#### 目前基础镜像已支持的组件版本如下

| Gradle版本   | 基础镜像中的绝对路径                | Android SDK版本 | JDK版本 |
| ------------ | ----------------------------------- | --------------- | ------- |
| gradle-4.4   | /home/ZCIPClient/tools/gradle-4.4   | android-26      | JDK 8   |
| gradle-4.8   | /home/ZCIPClient/tools/gradle-4.8   | android-27      | JDK 11  |
| gradle-4.8.1 | /home/ZCIPClient/tools/gradle-4.8.1 | android-28      |         |
| gradle-5.1.1 | /home/ZCIPClient/tools/gradle-5.1.1 | android-29      |         |
| gradle-5.4.1 | /home/ZCIPClient/tools/gradle-5.4.1 | android-30      |         |
| gradle-5.6.4 | /home/ZCIPClient/tools/gradle-5.6.4 | android-31      |         |
| gradle-6.1.1 | /home/ZCIPClient/tools/gradle-6.1.1 | android-32      |         |
| gradle-6.5.1 | /home/ZCIPClient/tools/gradle-6.5.1 | android-33      |         |
| gradle-6.7.1 | /home/ZCIPClient/tools/gradle-6.7.1 |                 |         |
| gradle-7.2   | /home/ZCIPClient/tools/gradle-7.2   |                 |         |
| gradle-7.5   | /home/ZCIPClient/tools/gradle-7.5   |                 |         |
| gradle-7.6   | /home/ZCIPClient/tools/gradle-7.6   |                 |         |

### 三方包开源仓库

![image](uploads/46176/5ab99a16-f727-41c2-83a4-289043ae330f/image.png)

注：App CI所涉及的三方包下载，暂时不走公司的SCOP系统三方包管理流程，已单独搭建app专用的私服（仅限app团队使用），统一引用地址：[http://10.10.193.208:8081/repository/maven-public/](http://10.10.193.208:8081/repository/maven-public/)。
参考配置项：

```java
        maven {
            url 'http://10.10.193.208:8081/repository/maven-public/'
            allowInsecureProtocol = true
        }
```

### 完整流程节点参考

![image](uploads/46176/acd3640e-6b02-428e-856d-bf2c4e1f6808/image.png)

### Gradle版本切换

目前基础镜像中默认使用的是Gradle 6.5，如果自己的代码工程中使用的Gradle版本与默认不一致，需要切换版本，目前推荐的是使用修改自定义脚本文件的方式实现。

![image](uploads/45810/7cf26810-526b-421b-a84e-b42cd4eeccd9/image.png)

打开这个pkg.sh脚本文件，查看编译脚本如下

```
./gradlew -DVERSION_NAME=${VERSION_NAME} -DPRODUCT_HOST_TYPE=${PRODUCT_HOST_TYPE} -DProductFlavors=${ProductFlavors} -DBUILD_TYPE=${BUILD_TYPE} -DVERSION_CODE=${VERSION_CODE}   -PVERSION_NAME=${VERSION_NAME} -PPRODUCT_HOST_TYPE=${PRODUCT_HOST_TYPE} -PProductFlavors=${ProductFlavors} -PBUILD_TYPE=Debug -PVERSION_CODE=${VERSION_CODE}   clean assemble${ProductFlavors}${BUILD_TYPE}
```

修改环境变量定义

> export  GRADLE_HOME="/home/ZCIPClient/tools/gradle-6.5"

这里路径修改为自己对应版本的路径，参考上面的表格，例如：

```
export GRADLE_HOME=/home/ZCIPClient/tools/gradle-6.5
export PATH=$GRADLE_HOME/bin:$PATH
source /etc/profile

gradle -v

gradle -DVERSION_NAME=${VERSION_NAME} -DPRODUCT_HOST_TYPE=${PRODUCT_HOST_TYPE} -DProductFlavors=${ProductFlavors} -DBUILD_TYPE=${BUILD_TYPE} -DVERSION_CODE=${VERSION_CODE}   -PVERSION_NAME=${VERSION_NAME} -PPRODUCT_HOST_TYPE=${PRODUCT_HOST_TYPE} -PProductFlavors=${ProductFlavors} -PBUILD_TYPE=Debug -PVERSION_CODE=${VERSION_CODE}   clean assemble${ProductFlavors}${BUILD_TYPE}
```

### Android SDK（NDK）切换

【强制】项目中使用的版本，必须使用CI镜像中已安装的SDK（NDK）版本

说明

- 保证构建的稳定， 如果不匹配会导致构建时SDK Mananger到google下载匹配不到的SDK版本，因公司网络访问google不稳定，极易构建失败
- 避免因访问外部服务流量大被封禁（此前清华源就对公司有过限制）
- 如果发现现有CI镜像中SDK（NDK）不满足要求，请提单给研发云集成对应版本的SDK（NDK）

当前持续构建镜像中 支持的Android SDK版本如下：

| SDK 平台（androidCompileSdkVersion） | 构建工具（androidBuildToolsVersion） | NDK          | CMAKE  |
| ------------------------------------ | ------------------------------------ | ------------ | ------ |
| 26                                   | 26.0.3                               | 20.0.5594570 | 3.22.1 |
| 27                                   | 27.0.3                               | 20.1.5948944 |        |
| 28                                   | 28.0.3                               | 23.1.7779620 |        |
| 29                                   | 29.0.3                               |              |        |
| 30                                   | 30.0.3                               |              |        |
| 31                                   | 31.0.0                               |              |        |
| 32                                   | 32.1.0-rc1                           |              |        |
| 33                                   | 33.0.2                               |              |        |
| 34                                   | 33.0.0                               |              |        |
| 35                                   | 35.0.0                               |              |        |

在各自项目代码中的找到 build.gradle 文件中的 compileSdkVersion、buildToolsVersion、ndkVersion 配置项，修改成上面的版本。
参考示例：

```groovy
android {
    // 推荐的 NDK 版本配置 
    ndkVersion "23.1.7779620"
    // 编译时的使用SDK版本
    compileSdkVersion 35
    // 配置构建工具版本
    buildToolsVersion '35.0.0'

    defaultConfig {
        applicationId "com.example.myapplication"
        minSdkVersion 24      // 客户要求禁用Android5，6
        targetSdkVersion 34   // 自2024年8月31日起，API级别必须为34，才能提交给 Google Play
        versionCode 1
        versionName "1.0"

        ndk {
            if (BUILD_TYPE == "Debug") {
                abiFilters "armeabi-v7a", "arm64-v8a", "x86", "x86_64"
            } else {
                abiFilters "armeabi-v7a", "arm64-v8a"
            }
        }

        // 配置 CMake 版本
        externalNativeBuild {
            cmake {
                version "3.22.1"
            }
        }
    }
}
```

# 本文件评审、修正记录

| 文件名称 | 安卓开发规范（Java）                                                                                                                                 |                 |               |        |
| -------- | ---------------------------------------------------------------------------------------------------------------------------------------------------- | --------------- | ------------- | ------ |
| 序号     | 流程                                                                                                                                                 | 拟制人/审核人   | 拟制/审核时间 | 版本号 |
| 1        | 编写                                                                                                                                                 | 王小虎等        | 2023/04/06    | V0.1   |
| 2        | 增加附录，介绍代码分析工具Lint和云雀CI流程配置说明                                                                                                   | 杨学书等        | 2023/06/13    | V0.2   |
| 3        | 首次发布                                                                                                                                             | APP规范组(安卓) | 2023/06/16    | V1.0   |
| 4        | 1. 2.3常量定义章节增加示例；2. 删除原12.4数据溢出问题章节。                                                                                          | 王小虎          | 2023/10/18    | V1.0.1 |
| 5        | 1. 修订10异常处理章节第一条说明内容。                                                                                                                | 王小虎          | 2023/10/19    | V1.0.2 |
| 6        | 发布                                                                                                                                                 | APP规范组(安卓) | 2023/11/21    | V1.1   |
| 7        | 1. 修订10异常处理章节第一条,预先检查进行规避异常处理增加NumberFormatException异常                                                                    | 王小虎          | 2024/1/18     | V1.1.0 |
| 8        | 发布                                                                                                                                                 | APP规范组(安卓) | 2024/01/19    | V1.2   |
| 9        | 1. 增加13.14规则，上传照片或附件时需要进行文件大小的限制校验。（规范来源：严重生产故障3566083）<br> 2. 修改第14章节，增加研发云代码分析执行的命令 。 | APP规范组(安卓) | 2024/08/20    | V1.2.1 |
| 10       | 发布                                                                                                                                                 | APP规范组(安卓) | 2024/08/21    | V1.3   |
| 11       | 修正3-5 、6-10章节文本描述的笔误                                                                                                                     | 王小虎          | 2024/09/13    | V1.3.1 |
| 12       | 发布                                                                                                                                                 | APP规范组(安卓) | 2024/10/14    | V1.4   |
| 13       | 完善章节12.7 发布安全章节，增加规范：【强制】应用加固后，应进行重签。（规范来源：严重生产故障3789946）                                               | 王小虎          | 2025/7/31     | V1.4.1 |
| 14       | 发布                                                                                                                                                 | APP规范组(安卓) | 2025/08/22    | V1.5   |
| 15       | 1. 完善章节14.2.2 “三方包开源仓库”，补充app专用私服配置参考<br>2. 新增章节14.2.5 Android SDK（NDK）切换                                            | 王小虎          | 2025/09/04    | V1.5.1 |
| 16       | 发布                                                                                                                                                 | APP规范组(安卓) | 2025/09/22    | V1.6   |
| 17       | 新增章节“12.8. Android版本安全”：<br>新增规范“禁止APP在低版本Android系统运行，推荐支持最低版本为10.0（android API 29）”（规范来源：安全治理单11546904）                                           | 王小虎          | 2025/12/19    | V1.6.1 |
| 18       | 新增章节“12.9. 应用自身防护”：<br>新增规范“禁止使用URL Schemes唤醒应用”（规范来源：安全治理单11546904）<br>新增规范“应用在申请用户权限时只申请必要的权限，申请的权限需要用户授予后才能使用”（规范来源：安全治理单11547236）<br>新增规范“禁止应用程序允许另一个应用程序在其之上运行”（规范来源：安全治理单11537910）<br>新增规范“应用切换到后台时，应该对界面敏感数据进行模糊化处理” （规范来源：安全治理单11537913）<br>新增规范“对于包含敏感数据页面应该禁止截图”（规范来源：安全治理单11537913）    | 王小虎          | 2026/3/10    | V1.6.2 |
| 19       | 发布                                                                                                                                                 | APP规范组(安卓) | 2026/03/23    | V1.7   |
| 20       | 补充章节12.7第5条“【强制】正式发布的包文件需执行安全加固流程对apk/aab文件执行安全加固 ”后的具体验证要求，补充要求 ：执行安全加固后，研发所内的出厂测试、CD，以及现场的UAT、BRT，都必须测试安全加固后的版本，充分验证加固后APP的兼容性。（规范来源：故障单号：3796792）   | 王小虎          | 2026/5/20    | V1.7.1 |
| 21       | 发布                                                                                                                                                 | APP规范组(安卓) | 2026/05/25    | V1.8   |
