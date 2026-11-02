![image](uploads/222708/985092ab-41bf-43e3-be09-58db3f6037de/image.png)

# 前言

React Native 是一个由 Facebook 开发的开源移动应用框架，允许开发者使用 JavaScript 和 React 创建跨平台（iOS 和 Android）移动应用。其核心优势在于“一次学习，随处编写”，通过渲染原生 UI 组件，提供接近原生应用的性能与体验。在国际数字渠道与国际OSS等业务领域，React Native已广泛应用于众多APP项目。

本规范旨在《JavaScript(ES6)语言编码规范》基础上，补充React Native特有的开发规范。
在遵循本规范之前，请务必先行学习《JavaScript(ES6)语言编码规范》。

## 适用对象

**浩鲸科技 React-Native 开发人员**

## 目的

为了持续、稳定地开发出高质量、健壮的软件系统，保证团队成员的编码质量，特制定本文档。本文档旨在规范团队内部开发过程，增强程序的健壮性，便于后续测试及代码维护，最终提高软件产品的生产力。

# 编程规范

## 代码风格

### 【强制】缩进采用2个空格，禁止使用tab字符；

**检查方式**：工具检查（eslint: [`indent`](https://eslint.org/docs/latest/rules/indent) eslint: [`no-mixed-spaces-and-tabs`](https://eslint.org/docs/latest/rules/no-mixed-spaces-and-tabs)）

**<font color=red>反例</font>**

```json
function bar() {
∙∙∙∙let name;
}

function bar() {
∙let name;
}
```

**正例**

```javascript
function bar() {
∙∙let name;
}
```

### 【强制】单行字符数限制不超过120个，超出需要换行

**检查方式**：工具检查（eslint: [`max-len`](https://eslint.org/docs/latest/rules/max-len)）

> 限制单行不超过 120 字符、超出需换行，可以让代码更易读、更好协作、更规范统一，同时提升开发和维护效率

### 【强制】不允许出现任何魔法值（即未经定义的常量）直接出现在代码中

> 允许在特定上下文中使用魔法值，但需添加明确注释说明

**检查方式**：工具检查（eslint: [`no-magic-numbers`](https://eslint.org/docs/latest/rules/no-magic-numbers)）

> 禁止魔法值直接出现在代码中，有助于代码可读性、可维护性、降低错误率、增强语义性和统一管理
>
> 1. 提升代码可读性
>    直接写数字、字符串等魔法值，别人（甚至自己过几天）很难一眼看懂其具体意义。
>    用具名常量（如MAX_RETRY_COUNT），即使不看其赋值，也能明白用途和含义。
> 2. 便于维护和修改
>    魔法值出现在多处时，如果需求变动（比如75要改成100），需要逐处手动修改并担心遗漏。统一用常量，只需改一处即可。
>    避免了批量替换时意外更改无关代码。
> 3. 减少出错概率
>    魔法值容易写错或混淆（如60表示1分钟、还是一小时？）。
>    统一用常量名，能防止误用或误改，提高代码的健壮性和可维护性。
> 4. 增强语义性与自文档化
>    常量名体现业务含义（如USER_STATUS_ACTIVE），无需注释或文档也能看懂，代码本身即是文档。
>    对团队新成员更友好，上手更快。
> 5. 便于统一管理和配置
>    可以将常量集中管理（如constants.js），便于配置、拓展、自动化测试等。

**<font color=red>反例</font>**

```js
if (userStatus === 1) { // 1 是什么意思？
  // do something
}
```

**正例**

```js
// 定义常量
const USER_STATUS_ACTIVE = 1;
const USER_STATUS_INACTIVE = 0;

// 代码中使用常量 团队成员一眼就能理解“1”代表什么，同时后期修改也简单安全 
if (userStatus === USER_STATUS_ACTIVE) {
  // do something
}
```

### 【强制】if／for／while／switch／do 等保留字后要放一个空格。在函数调用时，不在函数的参数列表前加空格

**检查方式**：工具检查（eslint：[`keyword-spacing`](https://eslint.org/docs/latest/rules/keyword-spacing) eslint: [`func-call-spacing`](https://eslint.org/docs/latest/rules/func-call-spacing) eslint: [`no-spaced-func`](https://eslint.org/docs/latest/rules/no-spaced-func)）

**<font color=red>反例</font>**

```javascript
const isJedi = true;
function fight() {
  console.log ('Swooosh!');
}
if(isJedi) {
  fight ();
}
```

**正例**

```javascript
const isJedi = true;
function fight() {
  console.log('Swooosh!');
}
if (isJedi) {
  fight();
}
```

### 【强制】使用空格把运算符隔开

**检查方式**：工具检查（eslint：[`space-infix-ops`](https://eslint.org/docs/latest/rules/space-infix-ops)）

说明：运算符包括赋值运算符＝、逻辑运算符＆＆、加减乘除符号、三目运算符等

**<font color=red>反例</font>**

```javascript
const testA=testB+5;
```

**正例**

```javascript
const testB = testA + 5;
```

### 【强制】方法参数在定义和传入时，多个参数逗号后边必须加空格

**检查方式**：工具检查（eslint：[`no-multi-spaces`](https://eslint.org/docs/latest/rules/no-multi-spaces)）

**<font color=red>反例</font>**

```javascript
onMsgByCa1lAndMsg = (msq,title,type) => {
    this.setState({callMsgAndMsg:msg})
  }
```

**正例**

```js
onMsgByCa1lAndMsg = (msq, title, type) => {
    this.setState({callMsgAndMsg:msg})
  }
```

### 【推荐】方法体内的执行语句组、变量的定义语句组、不同的业务逻辑之间或者不同的语义之间插入一个空行。相同业务逻辑和语义之间不需要插入空行。

**检查方式**：人工检查

> 空行像自然段一样划分代码，让逻辑区块一目了然。 可以快速区分变量声明、初始化、流程控制、不同业务处理部

**正例**

```js
function example(user) {
  // 变量定义
  let age = user.age;
  let name = user.name;

  // 数据校验
  if (!name) {
    throw new Error('Invalid name');
  }

  // 业务处理
  if (age > 18) {
    // ...
  } else {
    // ...
  }

  // 结果输出
  return { name, status: 'done' };
}
```

### 【推荐】不要使用一个常量类维护所有常量，应该按常量功能进行归类，分开维护

**检查方式**：人工检查

**正例**
缓存相关的常量放在类：CacheConsts下；
系统配置相关的常量放在类：ConfigConsts下；
说明：大而全的常量类，非得使用查找功能才能定位到修改的常量，不利于理解和维护

## 命名

### [推荐] UI组件命名以 View 结尾; 容器组件命名以 Container 结尾; 页面组件命名以 Page 结尾

**检查方式**：人工检查

> 这种组件命名约定（View, Container, Page）的好处是极大地提高了项目的可读性和维护性
> 它能让团队成员一眼识别组件的职责：
>
> 1. Page： 定义路由和整体布局，是应用页面的入口。
> 2. Container： 负责数据逻辑、状态管理和 API 调用。
> 3. View： 仅负责 UI 渲染，是纯粹的展示组件。

**正例**

```js
UI组件: ButtonView、UserCardView
容器组件： UserContainer
页面组件：HomePage、LoginPage
```

### 【强制】项目自定义变量命名不能以下划线或美元符号开始，也不能以下划线或美元符号结束

**检查方式**：人工检查

> 只对项目自定义变量强制执行命名规范，对框架/环境保留变量（如__DEV__）不作限制

**<font color=red>反例</font>**

```js
let $Object;
let name_;
let name$;
let Object$
```

**正例**

```js
let thisIsMyObject
```

### 【强制】类名使用 UpperCamelCase 风格，必须遵从驼峰形式，第一个字母必须大写

**检查方式**：工具检查（eslint: [`camelcase`](https://eslint.org/docs/latest/rules/camelcase)）

**<font color=red>反例</font>**

```js
class login_page
class msgPage
```

**正例**

```js
class LoginPage
class MsgPage
```

### 【强制】方法名、参数名、成员变量、局部变量都统一使用 lowerCamelCase风格，必须遵从驼峰形式，第一个字母必须小写

**检查方式**：工具检查（eslint: [`camelcase`](https://eslint.org/docs/latest/rules/camelcase)）

**<font color=red>反例</font>**

```js
let this_is_my_object = {};
function this_is_my_function() {}
```

**正例**

```js
let localValue
function getHttpMessage() 
let inputUserId
```

### 【强制】常量命名全部大写，单词间用下划线隔开，力求语义表达完整清楚，不要嫌名字长

**检查方式**：人工检查

**正例**

```js
const MAX_STOCK_COUNT = 100
```

### 【强制】文件夹命名统一小写

**检查方式**：人工检查

**正例**

```js
img // 存放图片
assert //存放资产
component //存放组件
```

### 【强制】代码中命名严禁使用拼音与英文混合的方式，更不允许直接使用中文的方式

**检查方式**：人工检查

> 正确的英文拼写和语法可以让阅读者易于理解，避免歧义。注意，即使纯拼音命名方式也要避免采用

**<font color=red>反例</font>**

```js
let wangluoqingqiu = {};
function bianliShuju() 
const ZUI_DA_CHONGSHI_CI_SHU
```

**正例**

```js
let totalAmount
function calculateTotalPrice() 
const ERROR_CODE_NETWORK_FAILURE
```

### 不要使用保留字作为变量名、键名

**检查方式**：工具检查（eslint: [`no-shadow-restricted-names`](https://eslint.org/docs/latest/rules/no-shadow-restricted-names)）

> 保留字是语言自身预留的单词（如 for、while、class、function 等），它们有特殊用途，不能用作普通变量名、对象的键名、函数名等。
>
> 不遵循这一规范会导致语法错误，或者产生不可预期的行为，严重影响代码的可维护性和可靠性。

**<font color=red>反例</font>**

```js
// 错误：用保留字作为变量名
let for = 1;          // SyntaxError: Unexpected token 'for'
const class = 'A';    // SyntaxError: Unexpected token 'class'

// 错误：用保留字作为对象键名（在严格模式下会报错）
let obj = {
  function: 123,      // 不推荐，严格模式下会报错
  return: 456,        // 不推荐，严格模式下会报错
};
```

**正例**

```js
// 正确：使用非保留字作为变量名
let count = 1;
const studentClass = 'A'; 

// 正确：对象键名使用非保留字
let obj = {
  fn: 123,
  result: 456,
};
```

## 控制语句

### 【强制】在一个switch块内，每个case要么通过break／return 等来终止，要么注释说明程序将继续执行到哪一个case为止；在一个switch块内，都必须包含一个default 语句并且放在最后，即使它什么代码也没有

**检查方式**：工具检查（eslint: [`default-case`](https://eslint.org/docs/latest/rules/default-case)）

**<font color=red>反例</font>**

```javascript
let test = 1;
switch (test) {
    case 1:
        /* code */
        break;
}
```

**正例**

```javascript
let testA = 1;
let testB = 1;
switch (testA) {
  case 1:
    /* code */
    break;

  default:
    /* code */
    break;
}
```

### 【推荐】在if／else／for／while／do 语句中必须使用大括号，即使只有一行代码

**检查方式**：工具检查（eslint: [`curly`](https://eslint.org/docs/latest/rules/curly)）

**<font color=red>反例</font>**

```javascript
function foo() {
  if (test)
    return false;
}
```

**正例**

```javascript
function foo() {
  if (test) {
    return false;
  }
}
```

### 【推荐】使用三目运算，替换if else结构，精简代码

**检查方式**：人工检查

**<font color=red>反例</font>**

```js
let account = 5;
if (account > 10){  
  return true;
}else{
  return false;
}
```

**正例**

```js
let isMsg = account > 10 ? true: false;
```

### 【推荐】除常用方法（如getXxx／isXxx）等外，不要在条件判断中执行其它复杂的语句，将复杂逻辑判断的结果赋值给一个有意义的布尔变量名，以提高可读性。

**检查方式**：人工检查

说明：很多if语句内的逻辑相当复杂，阅读者需要分析条件表达式的最终结果，才能明确什么样的条件执行什么样的语句

**<font color=red>反例</font>**

```js
// 反例 1：条件中出现嵌套的复杂表达式
if ((user.age > 18 && user.isActive && user.roles.includes('admin')) || user.isSuperUser) {
  // ...
}
// 反例 2：条件里包含运算、函数调用、逻辑组合等
if ((data.status === 'success' && (Date.now() - data.timestamp < 10000)) || isFromCache(data)) {
  // ...
}
```

**正例**

```js
// 正例 1：将复杂判断抽取为有意义的变量名
const hasAdminPermission = (user.age > 18 && user.isActive && user.roles.includes('admin')) || user.isSuperUser;
if (hasAdminPermission) {
  // ...
}
// 正例 2：变量名表达具体含义
const isFreshData = data.status === 'success' && (Date.now() - data.timestamp < 10000);
const canUseData = isFreshData || isFromCache(data);
if (canUseData) {
  // ...
}
```

## 编码约定

### 【推荐】建立统一主题配置，包含颜色、间距、文字样式等

**检查方式**：人工检查

> 1. 保证视觉一致性： 确保产品在所有页面和组件上都遵循统一的颜色、排版和间距规范，提供连贯的品牌体验。
> 2. 提升开发效率： 开发者无需硬编码样式值，而是引用主题变量。这极大地简化了新功能的开发和样式的调整。
> 3. 简化维护和迭代： 需要进行品牌升级或添加深色模式时，只需修改少数几个主题变量，即可全局同步更新，大大降低维护成本和出错风险。
> 4. 易于扩展： 为设计系统或组件库的未来扩展奠定坚实基础。

### 【推荐】为了多分辩率适配要求， 提供@1x@2x@3x图片

**检查方式**：人工检查

> 要求提供 @1x, @2x, @3x 图片 是 React Native 推荐的、用于确保静态图片在高分辨率设备上显示清晰的标准方法。

### 【推荐】强烈建议网络图片指定resizeMode属性

**检查方式**：人工检查

**<font color=red>反例</font>**

```javascript
<Image
  source={{ uri: 'https://example.com/2x1_image.jpg' }}
  style={{ width: 100, height: 100 }}
  resizeMode="contain" // 正确设置
/>
```

**正例**

```javascript
// 场景：想完整展示 Logo (200x100)，容器是正方形 (100x100)
<Image
  source={{ uri: 'https://example.com/2x1_logo.jpg' }}
  style={{ width: 100, height: 100 }}
  // 没设置 resizeMode 
/>
```

### 【推荐】安装npm包，推荐～来标记版本号

**检查方式**：人工检查

说明：～和＾的作用和区别：～会匹配最近的小版本依赖包，比如～1.2.3会匹配所有1.2.x版本，但是不包括1.3.0

＾会匹配最新的大版本依赖包，比如＾1.2.3会匹配所有1.x.x的包，包括1.3.0，但是不包括2.0.0。那么该如何选择呢？当然你可以指定特定的版本号，直接写1.2.3，前面什么前缀都没有，这样固然没问题，但是如果依赖包发布新版本修复了一些小bug，那么需要手动修改package.json文件；～和＾则可以解决这个问题。但是需要注意＾版本更新可能比较大，会造成项目代码错误，旧版本可能和新版本存在部分代码不兼容。所以推荐使用～来标记版本号，这样可以保证项目不会出现大的问题，也能保证包中的小bug可以得到修复。

### 【强制】所有的常量类型字段必须要有注释，说明每个值的用途

**检查方式**：人工检查

**正例**

```js
const MAX_ATTEMPTS = 3;  //最大重试次数;
```

### 【推荐】所有的组件或类都必须添加创建者信息，以及类的说明

**检查方式**：人工检查

**正例**

```js
/**
 * @Author: JohnDoe
 * @Date: 2025-05-26
 * @Description: A reusable React component that displays a list of items.
 * It supports pagination and a loading state indicator.
 * Items are fetched asynchronously from an API endpoint.
 *
 * @param {string} title - The title to display above the list.
 * @param {Array<Object>} items - The data items to render in the list.
 * @param {boolean} isLoading - Indicates if the data is currently being loaded.
 * @param {Function} onPageChange - Callback function triggered when the page changes.
 */
import React from 'react';
```

### 【推荐】方法内部单行注释，在被注释语句上方另起一行，使用//注释；方法内部多行注释使用/* */注释，注意与代码对齐。

**检查方式**：人工检查

**<font color=red>反例</font>**

```javascript
function getType() {
  console.log('fetching type...'); // This is console.
  // set the default type to 'no type'
  // 'no type' value
  let type = 'no type';

  return type;
}
```

**正例**

```javascript
function getType() {
  // This is console.
  console.log('fetching type...');

  /* set the default type to 'no type'
     'no type' value
  */
  let type = 'no type';

  return type;
}
```

### 【推荐】代码中过多使用console.log()会消耗性能

**检查方式**：工具检查（eslint: [`no-console`](https://eslint.org/docs/latest/rules/no-console) eslint: [`no-console`]

### 【推荐】对所有变量，对象的引用，使用const，不要使用var（只有当你明确知道一个变量在声明后需要被重新赋值时，才使用 let）

**检查方式**：工具检查（eslint: [`prefer-const`](https://eslint.org/docs/latest/rules/prefer-const) eslint: [`prefer-const`]

- 先使用 const： 这是现代 JavaScript 的最佳实践。它能确保你的变量引用不可变，使得代码更易于理解、维护和调试，并能有效减少 Bug。
- 谨慎使用 let： 只有当你明确知道一个变量在声明后需要被重新赋值时，才使用 let。
- 永远避免使用 var： var 存在函数作用域、变量提升和可重复声明等问题，这些都可能导致难以追踪的 Bug，已被 let 和 const 完全取代。
- 遵循此规范，你的 JavaScript 代码将更健壮、更清晰、更符合现代编程范式。

### 【强制】使用import / export来做模块加载导出，不使用非标准模块写法

**检查方式**：人工检查

**正例**

```js
import { lightRed } from './colors';
export default lightRed;
```

**<font color=red>反例</font>**

```js
const colors  = require('./colors');
module.exports = color.lightRed;
```

## 组件编写

### 【推荐】代码中函数绑定this，使用箭头函数

**检查方式**： 人工检查

**<font color=red>反例</font>**

```javascript
function foo() {
  const self = this;
  return function() {
    console.log(self);
  };
}

function foo() {
  const that = this;
  return function() {
    console.log(that);
  };
}
```

**正例**

```javascript
function foo() {
  return () => {
    console.log(this);
  };
}
```

### 【强制】代码中使用定时器或者DeviceEventEmitter，必须在组件卸载时进行销毁或者清除

**检查方式**： 人工检查

> 说明：如果定时器或事件监听器在组件卸载后仍然活跃，它们可能会尝试更新已经不存在的组件状态，导致应用崩溃或行为异常。

遵循原则：

- 使用 useEffect Hook (函数组件) 或 componentDidMount/componentWillUnmount 生命周期方法 (类组件) 来管理定时器和监听器的生命周期。

- 在组件挂载时 (useEffect 的依赖数组为空或 componentDidMount) 创建/注册它们。

- 在组件卸载时 (useEffect 返回的清理函数或 componentWillUnmount) 销毁/清除它们。

  **正例**

  ```javascript
  import React, { useState, useEffect } from 'react';
    import { View, Text, DeviceEventEmitter, Button } from 'react-native';

    const MyTimerAndEventEmitterComponent: React.FC = () => {
      const [count, setCount] = useState(0);
      const [eventData, setEventData] = useState<string>('No event yet');

      useEffect(() => {
        // ---- 定时器示例 ----
        let timerId: NodeJS.Timeout | null = null;

        // 1. 设置定时器
        timerId = setInterval(() => {
          setCount(prevCount => prevCount + 1);
        }, 1000);

        // ---- DeviceEventEmitter 示例 ----
        // 2. 注册 DeviceEventEmitter 监听器
        const eventListener = DeviceEventEmitter.addListener(
          'myCustomEvent',
          (data: string) => {
            setEventData(`Received: ${data}`);
          }
        );

        // ---- 清理函数 (组件卸载时执行) ----
        return () => {
          console.log('组件卸载，执行清理...');

          // 1. 清除定时器
          if (timerId) {
            clearInterval(timerId);
            console.log('定时器已清除');
          }

          // 2. 移除 DeviceEventEmitter 监听器
          if (eventListener) {
            eventListener.remove();
            console.log('DeviceEventEmitter 监听器已移除');
          }
        };
      }, []); // 依赖数组为空，表示只在组件挂载和卸载时执行一次

      const sendEvent = () => {
        DeviceEventEmitter.emit('myCustomEvent', `Data at ${new Date().toLocaleTimeString()}`);
      };

      return (
        <View style={{ padding: 20 }}>
          <Text>Timer Count: {count}</Text>
          <Text>Event Data: {eventData}</Text>
          <Button title="Emit Custom Event" onPress={sendEvent} />
          <Text style={{ marginTop: 20, color: 'gray' }}>
            当你离开此屏幕或组件被卸载时，定时器和监听器将被清除。
          </Text>
        </View>
      );
    };

    export default MyTimerAndEventEmitterComponent;
  ```

### 【强制】禁止使用内联样式，必须使用StyleSheet来创建样式属性并进行引用

**检查方式**： 工具检查(eslint：[`no-inline-styles`](https://github.com/Intellicode/eslint-plugin-react-native/blob/master/docs/rules/no-inline-styles.md))

**反例</font>**

```javascript
// DemoComponent.js
const DemoComponent = () => {
  return (
    <View style={styles.container}>
      <View style={{ flex: 1, backgroundColor: '#fff', padding: 10 }} />
      <Text style={{ color: '333', backgroundColor: '#fff', fontSize: 16 }}> Hello, World!</Text>
      // 上述代码到处是单独的 flex: 1、backgroundColor: '#fff' 等，容易造成冗余和维护困难。
    </view>
  )};
```

**正例**

```js
const styles = StyleSheet.create({
  container:{
    flex:1,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor:'#F5FCFF',
    marginTop:10,
  },
  bgview: {
    flex: 1, 
    backgroundColor: '#fff',
    padding: 10,
  },
  text:{
    color: '333', 
    backgroundColor: '#fff', 
    fontSize: 16,
  },
});

const DemoComponent = () => {
  return (
    <View style={styles.container}>
      <View style={styles.c} />
      <Text style={styles.text}>Hello, World!</Text>
    </view>
  )};
```

### 【推荐】当使用单一属性，或者全局样式属性时，推荐使用公共样式类

**检查方式**： 人工检查

> 作用：减少样式冗余、易于维护、统一风格、代码更简洁。
> 开发建议：单一属性或全局通用属性，优先抽取到公共样式类中，避免每个页面/组件单独写同样的样式。

**反例</font>**

```javascript
// DemoComponent.js
const DemoComponent = () => {
  return (
    <View style={styles.container}>
      <View style={{ flex: 1, backgroundColor: '#fff', padding: 10 }} />
      <Text style={{ color: '333', backgroundColor: '#fff', fontSize: 16 }} />
      <TouchableOpacity style={{ marginTop: 20 }} />
      // 上述代码到处是单独的 flex: 1、backgroundColor: '#fff' 等，容易造成冗余和维护困难。
    </view>
  )};
```

**正例**

```js
// commonStyles.js
import { StyleSheet } from 'react-native';
export const commonStyles = StyleSheet.create({
  flex: { flex: 1 },
  bgWhite: { backgroundColor: '#fff' },
  mt20: { marginTop: 20 },
  textDefault: { color: '333', fontSize: 16 },
});

// DemoComponent.js
import { commonStyles } from './commonStyles';
const DemoComponent = () => {
  return (
    <View style={styles.container}>
      <View style={[commonStyles.flex, commonStyles.bgWhite]} />
      <Text style={[commonStyles.textDefault, commonStyles.bgWhite]} />
      <TouchableOpacity style={commonStyles.mt20} />
    </view>
  )};
```

### 【强制】React Native 中的所有字符串都应该用 Text 组件包裹

**检查方式**： 工具检查(eslint：[`no-raw-text`](https://eslint.org/docs/latest/rules/no-unused-vars))

**<font color=red>反例</font>**

```javascript
const DemoComponent = () => {
  return (
    <View>some text</View>
  )};
```

**正例**

```javascript
const DemoComponent = () => {
  return (
    <View><Text>some text</Text></View>
  )};
```

### 【推荐】render()函数代码行请勿超过五十行，超过之后，请适当进行拆分为页面内组件，提高可读性

**检查方式**： 人工检查

### 【强制】对组件引用，变量初始化等，在整个页面或组件内未使用，应去除相关代码

**检查方式**： 工具检查(eslint：[`no-unused-vars`](https://eslint.org/docs/latest/rules/no-unused-vars))

**<font color=red>反例</font>**

```javascript
function foo(d) {
  const y = 10;
  const z = 0;
  console.log(z);
}
```

**正例**

```javascript
function foo(d) {
  console.log(d);
}
```

### 【推荐】React 组件中未使用的 StyleSheet 样式，建议进行删除

**检查方式**： 工具检查(eslint：[`no-unused-styles`](https://github.com/Intellicode/eslint-plugin-react-native/blob/master/docs/rules/no-unused-styles.md))

**<font color=red>反例</font>**

```javascript
const styles = StyleSheet.create({
  container: {
    marginTop: 50,
  },  
  text: {color: 'red'}     // text样式 未使用，建议进行删除
});

const DemoComponent = () => {
  return (
    <View style={styles.container}>
      <Text>Hello</Text>
    </View>
  );
};

export default DemoComponent;
```

**正例**

```javascript
const styles = StyleSheet.create({
  container: {
    marginTop: 50,
  }
});

const LotsOfStyles = () => {
  return (
    <View style={styles.container}>
      <Text>Hello</Text>
    </View>
  );
};

export default LotsOfStyles;
```

### 【强制】使用ListView或者FaltList的renderRow时，需对renderRow里面的组件需进行抽取，使用一个单独组件进行包裹

**检查方式**： 人工检查

将渲染单个列表项的逻辑抽取到一个单独的组件中, 是 React Native (和 React) 中处理列表渲染的推荐最佳实践，因为它同时兼顾了代码的可维护性、可读性和重要的运行时性能。

这主要有以下几个优点：

- 可读性提升： 列表组件的代码更简洁，专注于数据管理和列表配置，而单个项的渲染逻辑则封装在独立的组件中。
- 代码复用： 提取出的项组件可以在应用的其他地方复用。
- 性能优化： 最重要的优点之一，当项组件是独立的并且没有不必要的重新渲染时（尤其是在配合 React.memo 或 PureComponent 使用时），FlatList 的性能会得到显著提升，因为只有实际发生变化的项才会被重新渲染。
- 职责分离： 每个组件只负责自己的职责，提高代码的模块化。

### 【推荐】文案提取：所有界面文字提取到翻译文件

**检查方式**： 人工检查

> 便于国际化，也能有效减少魔法值支持

## Hook

### 【强制】只能在顶层调用Hook。不要在循环，条件或嵌套函数中调用Hook。

**检查方式**： 工具检查(eslint：[`react-hooks/rules-of-hooks`]())

> 说明：确保总是在你的 React 函数的最顶层调用他们。遵守这条规则，你就能确保 Hook 在每一次渲染中都按照同样的顺序被调用。这让 React 能够在多次的 useState 和 useEffect 调用之间保持 hook 状态的正确。

**<font color=red>反例</font>**

```javascript
// We're breaking the first rule by using a Hook in a condition
if (name !== '') {
  useEffect(function persistForm() {
    localStorage.setItem('formData', name);
  });
}
```

**正例**

```javascript
useEffect(function persistForm() {
  // We're not breaking the first rule anymore
  if (name !== '') {
    localStorage.setItem('formData', name);
  }
});
```

### 【强制】只在 React 函数或自定义 Hook中调用 Hook，不要在普通的 JavaScript 函数中调用 Hook

**检查方式**： 人工检查

> Hook 只能直接在函数组件或自定义 Hook（以 use 开头的函数）中调用。
> 避免在普通工具函数、事件回调、条件语句、循环或嵌套函数中调用 Hook。

**<font color=red>反例</font>**

```javascript
// 普通的 JS 函数中错误地调用 Hook
function useCustomLogic() {
  // 这里不是组件、也不是自定义 Hook
  const [count, setCount] = useState(0);
  return count;
}

// 在组件中调用该函数
export default function MyComponent() {
  const result = useCustomLogic(); // 实际这里没有正确响应 Hook 规则
  return <Text>{result}</Text>
}
```

**正例**

```javascript
// 正确写法：自定义 Hook
function useCustomLogic() {
  // 仅在自定义 Hook 内部调用其他 Hook
  const [count, setCount] = useState(0);
  return { count, setCount };
}

// 或直接在函数组件里调用Hook
export default function MyComponent() {
  const { count, setCount } = useCustomLogic();
  
  return (
    <View>
      <Text>{count}</Text>
      <Button onPress={() => setCount(count + 1)} title="Add" />
    </View>
  );
}
```

## 性能优化

### 【推荐】使用react-native-fast-image替代Image组件

**检查方式**： 人工检查

> 用 react-native-fast-image 替代 React Native 的默认 Image 组件是一个非常好的性能优化策略，特别是在处理大量网络图片时（例如社交媒体动态、商品列表）
> react-native-fast-image 是对原生图片库（iOS 使用 SDWebImage，Android 使用 Glide/Fresco）的封装。它直接利用了原生库在图片处理上的高性能优势，解决了默认 Image 组件的诸多痛点：

### 【强制】使用函数组件

**检查方式**： 人工检查

自从 React hooks 出现以来，函数组件已经成为在 React Native 中编写组件的首选方法。它们的可读性、可测试性和可维护性使它们成为突出的选择。

### 【强制】有状态组件，使用Hook

**检查方式**： 人工检查

React 在 16.8 版本引入了 Hooks (钩子)。Hooks 允许您在函数组件中“钩入” React 的 state 和生命周期特性，而无需编写类。

要求：

- 所有新的有状态组件，以及在条件允许下，逐步将现有的类组件重构为函数组件并使用 Hooks 来管理状态和副作用。
- 避免在新的代码中使用类组件，除非有非常特定的理由（例如，需要 componentDidCatch 进行错误边界）。

优势：

- 更简洁的代码： 函数组件配合 Hooks 使得组件逻辑更简洁，代码量通常更少。
- 更清晰的逻辑分离：
  - useState：用于管理组件的局部状态。
  - useEffect：用于处理组件的副作用（side effects），如数据获取、订阅、手动改变 DOM、定时器等。它将相关的逻辑（挂载时的操作和卸载时的清理）聚合在一起，提高了可读性。
  - useContext：用于在组件之间共享数据，避免逐层传递 Props (Prop Drilling)。
  - useCallback/useMemo：用于性能优化，避免不必要的重新渲染。
- 更强的逻辑复用性： Hooks 使得提取和复用有状态逻辑变得前所未有的简单，通过自定义 Hook (Custom Hooks)，您可以将复杂的、可复用的逻辑封装起来，供多个组件共享。
- 告别 this 的困扰： 函数组件没有 this 关键字，避免了 this 上下文的复杂性。
- 更好的性能优化潜力： 结合 React.memo 和 useCallback/useMemo，函数组件可以实现非常精细的性能优化，减少不必要的组件重新渲染。
- 更易于测试： 纯函数和独立的 Hooks 逻辑通常比复杂的类组件更容易编写单元测试。

### 【推荐】通过require引入图片等资源，不引入动态变量

**检查方式**： 人工检查

**<font color=red>反例</font>**

```js
const icon = this.props.active ? 'icon-innofied-active' : 'icon-innofied-inactive';
<Image source={require('./' + icon + '.png')} />;
```

**正例**

```js
const icon = this.props.active
   ? require('./icon-innofied-active.png')
   : require('./icon-innofied-inactive.png');
  <Image source={icon} />;
```

### 【推荐】图像资源添加到项目中之前使用压缩和调整图像大小

**检查方式**： 人工检查

在开发移动应用时，必须意识到APP中包含的图像资源。如果它们得到优化，它们可以积极影响应用的性能。建议在将图像添加到项目中之前使用压缩和调整图像大小的工具。此外，React Native 的‘Image’组件是缓存和高效加载具有各种选项的图像的绝佳资源。

### 【推荐】谨慎使用第三方库

**检查方式**： 人工检查

在开发应用程序时，第三方库可以帮助加速开发过程。然而，使用它们时数量要少，以避免使应用膨胀并导致冲突或性能问题。在包含库之前，有必要考虑其相关性并确保它正在定期维护和更新。此外，要密切关注应用的包大小，以防止添加新库时产生不必要的额外APP体积大小。

### 【推荐】启用Hermes

**检查方式**： 人工检查

Hermes 是一个为 Android 上的 React Native 优化的 JavaScript 引擎。如果你的应用在 Android 上运行缓慢，启用 Hermes 可以显著减少加载时间和内存使用。

### 【强制】数据列表如'FlatList'，必须提供提供唯一的 'keyExtractor' 属性

**检查方式**： 人工检查

> 说明：显示大量数据列表时，'FlatList' 是高效渲染的理想组件。然而，正确的使用可以带来良好的性能。为了确保 React 能够准确识别项目，提供唯一的 'keyExtractor' 属性是至关重要的。为了优化长列表的渲染过程，可以考虑使用 'getItemLayout' 属性或 'initialNumToRender'。

**<font color=red>反例</font>**

```js
<View style={styles.badContainer}>
      <Text style={styles.badHeader}>Bad Example: No keyExtractor</Text>
      <FlatList
        data={DATA_NO_KEY}
        renderItem={renderItem}
        // 反例：缺少 keyExtractor 属性
        // React Native 会发出警告，且列表性能可能不佳
      />
    </View>
```

**正例**

```js
<View style={styles.container}>
      <Text style={styles.header}>Product Catalog</Text>
      <FlatList
        data={PRODUCTS}
        renderItem={renderProductItem}
        // 正例：使用数据项中唯一且稳定的 'id' 字段作为 key
        keyExtractor={(item: Product) => item.id}
        contentContainerStyle={styles.listContent}
      />
    </View>
```

# 浩鲸科技React-native开发环境搭建指引

## 安装准备工作

在开始搭建开发环境之前，需要了解下背景，目前公司React-native指定的工具，分别是

- **<font color=red>Eslint：</font>** ESLint 是一款开源的 JavaScript 静态代码分析工具，用于检测代码中的潜在错误、风格问题和逻辑缺陷。它通过预定义或自定义的规则集，帮助开发者统一代码规范、提升可维护性。ESLint 已成为现代前端工程的标准工具
- **<font color=red>Pretieer：</font>** Prettier 是一款流行的代码格式化工具，专注于强制统一代码风格，支持 JavaScript、TypeScript、HTML、CSS、JSON 等多种语言。它通过解析代码并重新输出符合预设规则的格式，彻底消除团队协作中的代码风格争议。Prettier 已成为现代工程化项目的标配工具，尤其适合强调代码一致性的团队。

## 本地配置指导

### 添加公司eslint规则

1. 安装所需要的依赖

```sh
yarn add @whalecloud/rn-eslint-config -D
```

2. 去掉package.json 里面的eslintConfig字段

```diff
- "eslintConfig": {
-    ...
-  }
```

3. 项目根目录增加.editorconfig .prettierrc .eslintrc.js 文件
   .eslintrc.js 配置文件（模板默认为js）

```javascript
module.exports = {
  extends: '@whalecloud/rn-eslint-config',
};
```

.prettierrc配置文件:

```json
{
  "singleQuote": true,
  "trailingComma": "all",
  "printWidth": 120,
  "overrides": [
    {
      "files": ".prettierrc",
      "options": { "parser": "json" }
    }
  ]
}
```

.editorconfig配置文件:

```javascript
# http://editorconfig.org
root = true

[*]
indent_style = space
indent_size = 2
end_of_line = lf
charset = utf-8
trim_trailing_whitespace = true
insert_final_newline = true

[*.md]
trim_trailing_whitespace = false

[Makefile]
indent_style = tab
```

4. 配置[.eslintignore]
   在项目根目录新建CI_Config目录，在CI_Config目录中创建.eslintignore配置文件
   .eslintignore配置文件

```js
# 例外场景3：外部引入的开源软件。允许目录和文件级例外，需要给出开源代码对应的访问地址。
# node_modules目录里是第三方npm地址，开源地址：https://xxx
/node_modules
# 例外场景4：工具自动生成的代码。允许目录和文件级例外，需要给出代码生成工具的名称。
# 压缩后的js文件
/build
# 例外场景3：外部引入的开源软件。允许目录和文件级例外，需要给出开源代码对应的访问地址。
# public目录里是引入的第三方js，开源地址：https://xxx
**/public
```

注：各个项目根据自己项目实际情况，进行eslintignore的配置。
ZCM构建的时候会找CI_Config下的.eslintignore配置文件，建议根目录也放一份相同内容的的.eslintignore配置文件，用于本地检测

5. package.json里面增加 eslint命令

```json
"scripts": {
    ...
+   "eslint": "eslint --ext=.js,.jsx ./"
  },
```

运行 `npm run eslint`进行本地单独检测。检查结果与ci代码检查结果一致

## vscode编辑器中配置

### Vscode中安装eslint

1. 插件安装
   打开VSCode，在插件扩展商店搜索 `eslint`，点击安装，并重新加载；
   ![image](uploads/222708/8b085a69-cabb-4622-8f1d-89115f290e74/image.png)
2. 插件配置
   确保 VSCode 输出面板中 ESlint  ESLint server是处于工作状态的，并且找到npm ESlint
   ![image](uploads/222708/e30da98a-60ad-4227-a52d-040456388dae/image.png)

VSCode 的 ESLint 插件优先使用安装在当前项目中的 npm ESLint，如果当前项目中没有提供，它会使用全局安装的 npm ESLint。
然后看是否存在 ESLint 配置文件 `.eslintrc`，如果没有的话就不会去校验；如果存在VSCode 会根据你当前项目下的 `.eslintrc` 文件的规则来验证代码

### Vscode中安装Prettier

1. 插件安装
   打开VSCode，在插件扩展商店搜索 `Prettier`，点击安装，并重新加载；
   ![image](uploads/222708/ce55b6fc-dca6-4754-9d03-ed78175d40cb/image.png)
2. 插件配置
   通过 VSCode -> 首选项 -> 设置（settings.json），可配置 VSCode 编辑器的默认格式化工具，也可根据语言设置其对应的默认格式化工具。

```json
{
  "editor.defaultFormatter": "esbenp.prettier-vscode", // 设置编辑器的默认格式化工具为 prettier
  "[javascript]": { // 根据语言设置其对应的默认格式化工具
      "editor.defaultFormatter": "esbenp.prettier-vscode", // 设置 javascript 的默认格式化工具为 prettier
      "editor.formatOnSave": true, // 保存的时候自动格式化
  },
}
```

在项目根目录添加自定义配置文件.prettierrc
确保VSCode 输出面板中 Prettier  处于工作状态的。
![image](uploads/222708/879d7a51-705e-4a92-b282-a63c17bff7e1/image.png)

VSCode 的 prettier 插件将使用当前项目本地依赖中的npm prettier，如果当前项目中没有提供，将使用 prettier-vscode 插件捆绑的 prettier。
然后看是否存在 prettier 配置文件 `.prettierrc`，如果存在VSCode 会根据你当前项目下的 `.prettierrc` 文件的规则来格式化代码

# FAQ

# 本文件评审、修正记录

| 文件名称 | React-native语言编码规范                                   |               |               |        |
| -------- | ---------------------------------------------------------- | ------------- | ------------- | ------ |
| 序号     | 流程                                                       | 拟制人/审核人 | 拟制/审核时间 | 版本号 |
| 1        | 编写                                                       | 王小虎        | 2025/3/20     | V1.0   |
| 2        | 根据公开评审中提的意见，增加6条项目推荐的规则，修改2条规则 | 王小虎        | 2025/10/20    | V1.1   |
