![image](uploads/4083/cb110642-9d78-4dfd-b353-0b794a739e03/PG_ES5.png)

# 命名规则

- [1.1](1.1) <a name="1.1"></a>避免单字母命名。命名应具备描述性。

  **检查方式**：人工检查

  **<font color=red>反例</font>**

    ```javascript
  function q() {
      // ...stuff...
  }
  ```

  **正例**

    ```javascript
  function query() {
      // ..stuff..
  }
  ```

- [1.2](1.2) <a name="1.2"></a>使用驼峰式命名对象、函数和实例。

  **检查方式**：工具检查（eslint: [`camelcase`](https://eslint.org/docs/latest/rules/camelcase)）

  **<font color=red>反例</font>**

    ```javascript
  var this_is_my_object = {};
  function this_is_my_function() {}
  ```

  **正例**

    ```javascript
  var thisIsMyObject = {};
  function thisIsMyFunction() {}
  ```

- [1.3](1.3) <a name="1.3"></a>使用帕斯卡式命名构造函数或类。

  **检查方式**：工具检查（eslint: [`new-cap`](https://eslint.org/docs/latest/rules/new-cap)）

  **<font color=red>反例</font>**

    ```javascript
  var bad = {};
  function user(options) {
      this.name = options.name;
  }
  
  bad = new user({
      name: 'nope'
  });
  ```

  **正例**

    ```javascript
  var good = {};
  function User(options) {
      this.name = options.name;
  }
  
  good = new User({
      name: 'yup'
  });
  ```

- [1.4](1.4) <a name="1.4"></a>如果你的文件导出一个类，你的文件名应该与类名完全相同。

  **检查方式**：人工检查

  **<font color=red>反例</font>**

    ```javascript
  // file contents
  class CheckBox {
    // ...
  }
  module.exports = CheckBox;
  
  // in some other file
  var CheckBox = require('./checkBox');
  
  var CheckBox = require('./check_box');
  ```

  **正例**

    ```javascript
  // file contents
  class CheckBox {
    // ...
  }
  module.exports = CheckBox;
  
  // in some other file
  var CheckBox = require('./CheckBox');
  ```

# 空白

- [2.1](2.1) <a name="2.1"></a>使用 4 个空格作为缩进，并且禁止把空格和tab键混用来进行缩进。

  **检查方式**：工具检查（eslint: [`indent`](https://eslint.org/docs/latest/rules/indent) eslint: [`no-mixed-spaces-and-tabs`](https://eslint.org/docs/latest/rules/no-mixed-spaces-and-tabs)）

  **<font color=red>反例</font>**

    ```javascript
  function bar() {
  ∙∙var name;
  }
  
  function bar() {
  ∙var name;
  }
  ```

  **正例**

    ```javascript
  function bar() {
  ∙∙∙∙var name;
  }
  ```

- [2.2](2.2) <a name="2.2"></a>避免在正则表达式中使用多个空格。

  **检查方式**：工具检查（eslint：[`no-regex-spaces`](https://eslint.org/docs/latest/rules/no-regex-spaces)）

  **<font color=red>反例</font>**

    ```javascript
  var reStr = /foo   bar/;
  var reStr = new RegExp('foo   bar');
  ```

  **正例**

    ```javascript
  var reStr = /foo {3}bar/;
  var reStr = new RegExp('foo {3}bar');
  ```

- [2.3](2.3) <a name="2.3"></a>禁止使用tab键。

  **检查方式**：工具检查（eslint: [`no-tabs`](https://eslint.org/docs/latest/rules/no-tabs)）

# 逗号

- [3.1](3.1) <a name="3.1"></a>行首逗号: **不需要**。

  **检查方式**：工具检查（eslint: [`comma-style`](https://eslint.org/docs/latest/rules/comma-style)）

  **<font color=red>反例</font>**

    ```javascript
  var story = [
      once
      , upon
      , aTime
  ];
  
  var hero = {
      firstName: 'Bob'
      , lastName: 'Parr'
      , heroName: 'Mr. Incredible'
      , superPower: 'strength'
  };
  ```

  **正例**

    ```javascript
  var story = [
      once,
      upon,
      aTime
  ];
  
  var hero = {
      firstName: 'Bob',
      lastName: 'Parr',
      heroName: 'Mr. Incredible',
      superPower: 'strength'
  };
  ```

- [3.2](3.2) <a name="3.2"></a>额外的行末逗号：**不需要**。这样做会在 IE6/7 和 IE9 怪异模式下引起问题。

  **检查方式**：工具检查（eslint: [`comma-dangle`](https://eslint.org/docs/latest/rules/comma-dangle)）

  **<font color=red>反例</font>**

    ```javascript
  var hero = {
      firstName: 'Kevin',
      lastName: 'Flynn',
  };
  
  var heroes = [
      'Batman',
      'Superman',
  ];
  ```

  **正例**

    ```javascript
  var hero = {
      firstName: 'Kevin',
      lastName: 'Flynn'
  };
  
  var heroes = [
      'Batman',
      'Superman'
  ];
  ```

- [3.3](3.3) <a name="3.3"></a>禁止使用多个逗号来声明一个空数组。

  **检查方式**：工具检查（eslint: [`no-sparse-arrays`](https://eslint.org/docs/latest/rules/no-sparse-arrays)）

  **<font color=red>反例</font>**

    ```javascript
  var items = [,];
  var colors = ['red',, 'blue'];
  ```

  **正例**

    ```javascript
  var items = [];
  var colors = ['red', 'blue'];
  ```

- [3.4](3.4) <a name="3.4"></a>避免使用逗号操作符,在for语句的初始化或更新部分或如果表达式序列明确地包含在括号中时可以使用逗号运算符。

  **检查方式**：工具检查（eslint: [`no-sequences`](https://eslint.org/docs/latest/rules/no-sequences)）

  **<font color=red>反例</font>**

    ```javascript
  var testA = 5;
  var testB = 0;
  testA = testB += 5, testA + testB;
  while (testA = next(), testA && testA.length);
  ```

  **正例**

    ```javascript
  foo = (doSomething(), val);
  (0, eval)("doSomething();");
  do {} while ((doSomething(), !!test));
  for (i = 0, j = 10; i < j; i++, j--);
  ```

# 分号

- [4.1](4.1) <a name="4.1"></a> JavaScript 的语句以分号作为结束符，禁止省略分号。

  **检查方式**：工具检查（eslint: [`no-unexpected-multiline`](https://eslint.org/docs/latest/rules/no-unexpected-multiline) eslint: [`semi`](https://eslint.org/docs/latest/rules/semi)）

  **<font color=red>反例</font>**

    ```javascript
  (function () {
      var name = 'Skywalker'
      return name
  }())
  var foo = bar
  ```

  **正例**

    ```javascript
  (function () {
      var name = 'Skywalker';
      return name;
  }());
  
  ;(function () {
      var name = 'Skywalker';
      return name;
  }());
  ```

  *[说明] 防止函数在两个 IIFE 合并时被当成一个参数。*

- [4.2](4.2) <a name="4.2"></a>不允许使用多余的分号。

  **检查方式**：工具检查（eslint: [`no-extra-semi`](https://eslint.org/docs/latest/rules/no-extra-semi)）

  **<font color=red>反例</font>**

    ```javascript
  var item = 5;;
  function foo() {
      // code
  };
  ```

  **正例**

    ```javascript
  var item = 5;
  var foo = function () {
      // code
  };
  function bar () {
      // code
  }
  ```

# 变量

- [5.1](5.1) <a name="5.1"></a>变量的名称采用驼峰法则，首字母小写，后续单词的首字母大写。

  **检查方式**：工具检查（eslint: [`camelcase`](https://eslint.org/docs/latest/rules/camelcase)）

  **<font color=red>反例</font>**

    ```javascript
  var Is_Editable = false;
  ```

  **正例**

    ```javascript
  var isEditable = false;
  ```

- [5.2](5.2) <a name="5.2"></a>总是使用 `var` 来声明变量。不这么做将导致产生全局变量。我们要避免污染全局命名空间。

  **检查方式**：工具检查（eslint：[`no-undef`](https://eslint.org/docs/latest/rules/no-undef)）

  **<font color=red>反例</font>**

    ```javascript
  superPower = new SuperPower();
  ```

  **正例**

    ```javascript
  var superPower = new SuperPower();
  ```

- [5.3](5.3) <a name="5.3"></a>使用 `var` 声明每一个变量，并且每行只声明一个变量。这样做的好处是增加新变量将变的更加容易，而且你永远不用再担心调换错 `;` 跟 `,`。

  **检查方式**：工具检查（eslint: [`one-var`](https://eslint.org/docs/latest/rules/one-var) eslint:[`one-var-declaration-per-line`](https://eslint.org/docs/latest/rules/one-var-declaration-per-line)）

  **<font color=red>反例</font>**

    ```javascript
  var items = getItems(),
      goSportsTeam = true,
      dragonball = 'z';
  var foo = 1, bar = 2;
  
  var items = getItems(),
      goSportsTeam = true;
      dragonball = 'z';
  ```

  *[说明] 跟上面的代码比较一下，看看哪里错了。*

  **正例**

    ```javascript
  var items = getItems();
  var goSportsTeam = true;
  var dragonball = 'z';
  ```

- [5.4](5.4) <a name="5.4"></a>最后再声明未赋值的变量。当你需要引用前面的变量赋值时这将变的很有用。

  **检查方式**：人工检查

  **<font color=red>反例</font>**

    ```javascript
  var i, len, dragonball,
      items = getItems(),
      goSportsTeam = true;
  
  var i;
  var items = getItems();
  var dragonball;
  var goSportsTeam = true;
  var len;
  ```

  **正例**

    ```javascript
  var items = getItems();
  var goSportsTeam = true;
  var dragonball;
  var length;
  var i;
  ```

- [5.5](5.5) <a name="5.5"></a>在作用域顶部声明函数。这将帮你避免函数声明提升相关的问题。保证在代码块的顶部声明函数。

  **检查方式**：工具检查（eslint: [`no-inner-declarations`](https://eslint.org/docs/latest/rules/no-inner-declarations)）

  **<font color=red>反例</font>**

    ```javascript
  function doSomethingElse() {
      if (test) {
          function doAnotherThing() { }
      }
  }
  ```

  **正例**

    ```javascript
  function doAnotherThing() { }
  
  function doSomethingElse() {
      if (test) {
          doAnotherThing();
      }
  }
  ```

- [5.6](5.6) <a name="5.6"></a>禁止重复声明变量。

  **检查方式**：工具检查（eslint: [`no-redeclar`](https://eslint.org/docs/latest/rules/no-redeclar)）（暂未支持）

  **<font color=red>反例</font>**

    ```javascript
  var testA = 3;
  var testA = 10;
  ```

  **正例**

    ```javascript
  var testA = 3;
  testA = 10;
  ```

- [5.7](5.7) <a name="5.7"></a>禁止修改全局对象或只读全局对象。

  **检查方式**：工具检查（eslint: [`no-global-assign`](https://eslint.org/docs/latest/rules/no-global-assign)）

  **<font color=red>反例</font>**

    ```javascript
  Object = null;
  undefined = 1;
  ```

  **正例**

    ```javascript
  var testA = 1;
  var testB = 1;
  testB = 2;
  ```

- [5.8](5.8) <a name="5.8"></a>禁止在循环语句中编写函数。由于函数在循环周围创建闭包的方式，在循环中编写函数往往会导致错误。

  **检查方式**：工具检查（eslint: [`no-loop-func`](https://eslint.org/docs/latest/rules/no-loop-func)）

  **<font color=red>反例</font>**

    ```javascript
  var data = [];
  for (var i = 10; i; i--) {
      data[i] = function() { return i; };
  }
  data[0]();
  data[1]();
  data[2]();
  ```

  **正例**

    ```javascript
  var itemFunc = function (t) { console.log(t) };
  for (var i = 10; i; i--) {
      itemFunc(i);
  }
  ```

- [5.9](5.9) <a name="5.9"></a>禁止使用尤达条件，尤达条件语句就是对象字面量写在比较操作符的左边，而变量应该写在比较操作符的右边。

  **检查方式**：工具检查（eslint: [`yoda`](https://eslint.org/docs/latest/rules/yoda)）

  **<font color=red>反例</font>**

    ```javascript
  if ('red' === color) {
      // ...
  }
  if (true === flag) {
      // ...
  }
  if (5 > count) {
      // ...
  }
  ```

  **正例**

    ```javascript
  if (flag === true) {
      // ...
  }
  if (value === 'red') {
      // ...
  }
  ```

- [5.10](5.10) <a name="5.10"></a>禁止用delete删除var声明的变量，delete运算符的目的是从对象中删除属性。delete在变量上使用运算符可能会导致意外行为。

  **检查方式**：工具检查（eslint: [`no-delete-var`](https://eslint.org/docs/latest/rules/no-delete-var)）

  **<font color=red>反例</font>**

    ```javascript
  var test;
  delete test;
  ```

- [5.11](5.11) <a name="5.11"></a>禁止创建与作用域内的变量共享名称的标签的不良做法。

  **检查方式**：工具检查（eslint: [`no-label-var`](https://eslint.org/docs/latest/rules/no-label-var)）

  **<font color=red>反例</font>**

    ```javascript
  var item = foo;
  function bar() {
    item:
      for (;;) {
          break item;
      }
  }
  ```

  **正例**

    ```javascript
  function foo() {
      var item = 'foo';
  }
  function bar() {
      for (;;) {
          break;
      }
  }
  ```

- [5.12](5.12) <a name="5.12"></a>禁止声明的变量与外层作用域的变量同名。

  **检查方式**：工具检查（eslint: [`no-shadow`](https://eslint.org/docs/latest/rules/no-shadow)）

  **<font color=red>反例</font>**

    ```javascript
  var item = 3;
  function test() {
      var item = 10;
  }
  ```

  **正例**

    ```javascript
  var item = 3;
  function test() {
      var count = 10;
  }
  ```

- [5.13](5.13) <a name="5.13"></a>禁止声明变量时覆盖JavaScript中的保留关键字。

  **检查方式**：工具检查（eslint: [`no-shadow-restricted-names`](https://eslint.org/docs/latest/rules/no-shadow-restricted-names)）

  **<font color=red>反例</font>**

    ```javascript
  function NaN(){}
  !function(Infinity){};
  var undefined = 5;
  try {} catch(eval){}
  ```

  **正例**

    ```javascript
  var test;
  function testFunc(index, val) {}
  ```

- [5.14](5.14) <a name="5.14"></a>禁止使用没有定义的变量。

  **检查方式**：工具检查（eslint: [`no-undef`](https://eslint.org/docs/latest/rules/no-undef)）

  **<font color=red>反例</font>**

    ```javascript
  var testA = 5;
  testB = 10;
  testFunc();
  function testFunc() {}
  ```

  **正例**

    ```javascript
  var testA = 5;
  testA = 10;
  function testFunc() {}
  testFunc();
  ```

- [5.15](5.15) <a name="5.15"></a>禁止将变量初始化为undefined，在JavaScript中，声明但未初始化为任何值的变量会自动获取值undefined，因此不必将变量初始化为undefined。

  **检查方式**：工具检查（eslint: [`no-undef-init`](https://eslint.org/docs/latest/rules/no-undef-init)）

  **<font color=red>反例</font>**

    ```javascript
  var foo = undefined;
  ```

  **正例**

    ```javascript
  var foo;
  ```

- [5.16](5.16) <a name="5.16"></a>不允许定义了的变量但是在后面的代码中没有被使用到。

  **检查方式**：工具检查（eslint: [`no-unused-vars`](https://eslint.org/docs/latest/rules/no-unused-vars)）

  **<font color=red>反例</font>**

    ```javascript
  function foo(item) {
      var count = 10;
      var len = 0;
      console.log(count);
  }
  ```

  **正例**

    ```javascript
  function foo(item) {
      console.log(item);
  }
  ```

- [5.17](5.17) <a name="5.17"></a>禁止使用链式赋值的表达式。

  **检查方式**：工具检查（eslint: [`no-multi-assign`](https://eslint.org/docs/latest/rules/no-multi-assign)）

  **<font color=red>反例</font>**

    ```javascript
  var testA = testB = testC = 5;
  var foo = bar = 'baz';
  ```

  **正例**

    ```javascript
  var testA = 5;
  var testB = 5;
  var testC = 5;
  var foo = 'baz';
  var bar = 'baz';
  ```

- [5.18](5.18) <a name="5.18"></a>禁止在变量定义之前使用它们。

  **检查方式**：工具检查（eslint: [`no-use-before-define`](https://eslint.org/docs/latest/rules/no-use-before-define)）

  > 规范来源：严重生产故障3628566/缺陷10973951

  **<font color=red>反例</font>**

    ```javascript
  alert(testA);
  var testA = 10;
  
  testFunc();
  function testFunc() {}
  ```

  **正例**

    ```javascript
  var testA = 5;
  alert(testA);
  function testFunc() {}
  testFunc();
  ```

# 对象

- [6.1](6.1) <a name="6.1"></a>使用直接量创建对象。

  **检查方式**：工具检查（eslint: [`no-new-object`](https://eslint.org/docs/latest/rules/no-new-object)）

  **<font color=red>反例</font>**

    ```javascript
  var item = new Object();
  ```

  **正例**

    ```javascript
  var item = {};
  ```

- [6.2](6.2) <a name="6.2"></a>在使用长方法链时进行缩进时，使用前面的点 `.` 强调这是方法调用而不是新语句。在使用 `.`号调用对象属性时，应保持 `.`号与属性在同一行。

  **检查方式**：工具检查（eslint：[`dot-location`](https://eslint.org/docs/latest/rules/dot-location) eslint：[`newline-per-chained-call`](https://eslint.org/docs/latest/rules/newline-per-chained-call)）

  **<font color=red>反例</font>**

    ```javascript
  $('#items').find('.selected').highlight().end().find('.open').updateCount();
  var foo = object.
          property;
  
  $('#items').
      find('.selected').
      highlight().
      end().
      find('.open').
      updateCount();
  
  var leds = stage.selectAll('.led').data(data).enter().append('svg:svg').classed('led', true)
      .attr('width', (radius + margin) * 2).append('svg:g')
      .attr('transform', 'translate(' + (radius + margin) + ',' + (radius + margin) + ')')
      .call(tron.led);
  ```

  **正例**

    ```javascript
  $('#items')
      .find('.selected')
      .highlight()
      .end()
      .find('.open')
      .updateCount();
  var foo = object.property;
  
  var leds = stage.selectAll('.led')
      .data(data)
      .enter().append('svg:svg')
      .classed('led', true)
      .attr('width', (radius + margin) * 2)
      .append('svg:g')
      .attr('transform', 'translate(' + (radius + margin) + ',' + (radius + margin) + ')')
      .call(tron.led);
  ```

- [6.3](6.3) <a name="6.3"></a>不允许在使用对象字面量申明对象的时使用相同的键名。

  **检查方式**：工具检查（eslint：[`no-dupe-keys`](https://eslint.org/docs/latest/rules/no-dupe-keys)）

  **<font color=red>反例</font>**

    ```javascript
  var foo = {
      bar: 'baz',
      bar: 'qux'
  };
  ```

  **正例**

    ```javascript
  var foo = {
      bar: 'baz',
      quxx: 'qux'
  };
  ```

- [6.4](6.4) <a name="6.4"></a>禁止将全局对象（Math和JSON)作为函数调用。

  **检查方式**：工具检查（eslint：[`no-obj-calls`](https://eslint.org/docs/latest/rules/no-obj-calls)）

  **<font color=red>反例</font>**

    ```javascript
  var math = Math();
  var json = JSON();
  var reflect = Reflect();
  ```

  **正例**

    ```javascript
  function area(r) {
      return Math.PI * r * r;
  }
  var object = JSON.parse("{}");
  var value = Reflect.get({ x: 1, y: 2 }, "x");
  ```

- [6.5](6.5) <a name="6.5"></a>禁止使用特定对象的指定方法，有arguments的callee方法。

  **检查方式**：工具检查（eslint: [`no-restricted-properties`](https://eslint.org/docs/latest/rules/no-restricted-properties)）

  **<font color=red>反例</font>**

    ```javascript
  function calleeDemo() {
      alert(arguments.callee);
  }
  ```

  **正例**

    ```javascript
  [1, 2, 3, 4, 5].map(function factorial(n) {
      return !(n > 1) ? 1 : factorial(n - 1) * n;
  });
  ```

- [6.6](6.6) <a name="6.6"></a>不要使用[保留字](http://es5.github.io/#x7.6.1)作为键名，它们在 IE8 下不工作。

  **检查方式**：工具检查（eslint: [`no-shadow-restricted-names`](https://eslint.org/docs/latest/rules/no-shadow-restricted-names)）

# 数组

- [7.1](7.1) <a name="7.1"></a>使用直接量创建数组。 禁止使用new创建包装实例，如 new String、new Number，这样会变成初始化一个对象，而不是对应的初始类型。

  **检查方式**：工具检查（eslint: [`no-new-wrappers`](https://eslint.org/docs/latest/rules/no-new-wrappers)）

  **<font color=red>反例</font>**

    ```javascript
  var items = new Array();
  ```

  **正例**

    ```javascript
  var items = [];
  ```

- [7.2](7.2) <a name="7.2"></a>向数组增加元素时使用 Array#push 来替代直接赋值。

  **检查方式**：人工检查

  **<font color=red>反例</font>**

    ```javascript
  someStack[someStack.length] = 'abracadabra';
  ```

  **正例**

    ```javascript
  someStack.push('abracadabra');
  ```

- [7.3](7.3) <a name="7.3"></a>当你需要拷贝数组时，使用 Array#slice。[jsPerf](http://jsperf.com/converting-arguments-to-an-array/7)

  **检查方式**：人工检查

  **<font color=red>反例</font>**

    ```javascript
  var item = [1, 2, 3, 4, 5];
  var len = items.length;
  var itemsCopy = [];
  var i;
  
  for (i = 0; i < len; i++) {
      itemsCopy[i] = items[i];
  }
  ```

  **正例**

    ```javascript
  var item = [1, 2, 3, 4, 5];
  var len = items.length;
  var itemsCopy = [];
  var i;
  
  itemsCopy = items.slice();
  ```

- [7.4](7.4) <a name="7.4"></a>使用 Array#slice 将类数组对象转换成数组。

  **检查方式**：人工检查

  **正例**

    ```javascript
  function trigger() {
      var args = Array.prototype.slice.call(arguments);
    ...
  }
  ```

- [7.5](7.5) <a name="7.5"></a>禁止Array构造函数。

  **检查方式**：工具检查（eslint: [`no-array-constructor`](https://eslint.org/docs/latest/rules/no-array-constructor)）

  **<font color=red>反例</font>**

    ```javascript
  var foo = new Array();
  ```

  **正例**

    ```javascript
  var foo = [];
  ```

- [7.6](7.6) <a name="7.6"></a>禁止使用for-in语句枚举数组。

  **检查方式**：工具检查（eslint: [`no-restricted-syntax`](https://eslint.org/docs/latest/rules/no-restricted-syntax)）

  **<font color=red>反例</font>**

    ```javascript
  var list = [8, 3, 11, 9, 6]
  for (i in list) {
      console.log(list[i]);
  }
  ```

  **正例**

    ```javascript
  var obj={
     one:'first',
     two:'zoo',
     three:'34'
  };
  for (var key in obj) {
      if (Object.prototype.hasOwnProperty.call(obj, key)) {
          console.log(key+':'+obj[key]);
      }
  };
  ```

# 字符串

- [8.1](8.1) <a name="8.1"></a>使用单引号 `''` 包裹字符串。

  **检查方式**：工具检查（eslint: [`quotes`](https://eslint.org/docs/latest/rules/quotes)）

  **<font color=red>反例</font>**

    ```javascript
  var name = "Bob Parr";
  
  var fullName = "Bob " + this.lastName;
  ```

  **正例**

    ```javascript
  var name = 'Bob Parr';
  
  var fullName = 'Bob ' + this.lastName;
  ```

- [8.2](8.2) <a name="8.2"></a>程序化生成的字符串使用 Array#join 连接而不是使用连接符。尤其是 IE 下：[jsPerf](http://jsperf.com/string-vs-array-concat/2)

  **检查方式**：人工检查

  **<font color=red>反例</font>**

    ```javascript
  var items;
  var messages;
  var length;
  var i;
  
  messages = [{
      state: 'success',
      message: 'This one worked.'
  }, {
      state: 'success',
      message: 'This one worked as well.'
  }, {
      state: 'error',
      message: 'This one did not work.'
  }];
  
  length = messages.length;
  
  function inbox(messages) {
      items = '<ul>';
  
      for (i = 0; i < length; i++) {
          items += '<li>' + messages[i].message + '</li>';
      }
  
      return items + '</ul>';
  }
  ```

  **正例**

    ```javascript
  var items;
  var messages;
  var length;
  var i;
  
  messages = [{
      state: 'success',
      message: 'This one worked.'
  }, {
      state: 'success',
      message: 'This one worked as well.'
  }, {
      state: 'error',
      message: 'This one did not work.'
  }];
  
  length = messages.length;
  
  function inbox(messages) {
      items = [];
  
      for (i = 0; i < length; i++) {
          // use direct assignment in this case because we're micro-optimizing.
          items.push('<li>' + messages[i].message + '</li>');
      }
  
      return '<ul>' + items.join('') + '</ul>';
  }
  ```

- [8.3](8.3) <a name="8.3"></a>禁止字符串分两行书写。

  **检查方式**：工具检查（eslint: [`no-multi-str`](https://eslint.org/docs/latest/rules/no-multi-str)）

  **<font color=red>反例</font>**

    ```javascript
  var testStr = 'Line 1 \
           Line 2';
  ```

  **正例**

    ```javascript
  var testStr = 'Line 1\n' +
          'Line 2';
  ```

- [8.4](8.4) <a name="8.4"></a>禁止使用没有必要的字符串拼接。

  **检查方式**：工具检查（eslint: [`no-useless-concat`](https://eslint.org/docs/latest/rules/no-useless-concat)）

  **<font color=red>反例</font>**

    ```javascript
  var testA = 'some' + 'string';
  
  var testB = '1' + '0';
  ```

  *[说明] these are the same as "10".*

  **正例**

    ```javascript
  var testC = a + b;
  var testB = '1' + a;
  var testA = 1 + '1';
  ```

  *[说明] when a non string is included.*

# 函数

- [9.1](9.1) <a name="9.1"></a>永远不要在一个非函数代码块（if、while 等）中声明或赋值一个函数，浏览器允许你这么做，但它们的解析表现不一致，正确的做法是：在块外定义一个变量，然后将函数赋值给它。

  **检查方式**：工具检查（eslint: [`no-inner-declarations`](https://eslint.org/docs/latest/rules/no-inner-declarations)）

  **<font color=red>反例</font>**

    ```javascript
  if (test) {
  function doSomething() { }
  }
  
  function doSomethingElse() {
      if (test) {
          function doAnotherThing() { }
      }
  }
  ```

  **正例**

    ```javascript
  function test() {
          console.log('Yup.');
  };
  ```

- [9.2](9.2) <a name="9.2"></a>永远不要把参数命名为 `arguments`。这将取代函数作用域内的 `arguments` 对象。

  **检查方式**：工具检查（eslint: [`no-shadow-restricted-names`](https://eslint.org/docs/latest/rules/no-shadow-restricted-names)）

  **<font color=red>反例</font>**

    ```javascript
  function nope(name, options, arguments) {
      // ...stuff...
  }
  ```

  **正例**

    ```javascript
  function yup(name, options, args) {
      // ...stuff...
  }
  ```

- [9.3](9.3) <a name="9.3"></a>在函数中有分支时，保证所有的return 语句要么都指定返回值，要么都不指定返回值。

  **检查方式**：工具检查（eslint: [`consistent-return`](https://eslint.org/docs/latest/rules/consistent-return)）

  **<font color=red>反例</font>**

    ```javascript
  function doSomething(condition) {
      if (condition) {
          return true;
      } else {
          return;
      }
  }
  
  function doSomething(condition) {
      if (condition) {
          return true;
      }
  }
  ```

  **正例**

    ```javascript
  function doSomething(condition) {
      if (condition) {
          return true;
      } else {
          return false;
      }
  }
  
  function Foo() {
      if (!(this instanceof Foo)) {
          return new Foo();
      }
  
      this.index = 0;
  }
  ```

- [9.4](9.4) <a name="9.4"></a>禁止出现空函数,如果一个函数包含了一条注释，它将不会被认为有问题，这里允许普通功能函数、对象文字的类方法和方法简写为空。

  **检查方式**：工具检查（eslint: [`no-empty-function`](https://eslint.org/docs/latest/rules/no-empty-function)）

  **<font color=red>反例</font>**

    ```javascript
  function foo() {}
  var foo = function() {};
  var obj = {
      foo: function() {}
  };
  ```

  **正例**

    ```javascript
  function foo() {
      // do nothing.
  }
  
  var foo = function() {
      // any clear comments.
  };
  
  var foo = () => {
      bar();
  };
  
  function* foo() {
      // do nothing.
  }
  
  var foo = function*() {
      // do nothing.
  };
  ```

- [9.5](9.5) <a name="9.5"></a>禁止给函数的参数重新赋值。主要原因有两点，一是对函数参数进行重新赋值操作后最后会搞不清函数参数的初始值，二是如果参数是引用类型的参数在函数内部对参数进行操作会也会同样影响到函数外部此参数的值。正确的做法是：如果函数参数不是引用类型可以在函数内部定义变量并将其赋值给该变量；如果参数为引用类型的参数，如果为对象类型则推荐使用fish的extend方法，如果是数组类型的推荐使用Array的slice方法。

  **检查方式**：工具检查（eslint: [`no-param-reassign`](https://eslint.org/docs/latest/rules/no-param-reassign)）

  **<font color=red>反例</font>**

    ```javascript
  var test = 'test';
  var testObj = { item:'item' };
  var testArr = [1,2,3];
  
  function foo(test) {
      test = 'abc';
  }
  
  function foo(testObj) {
      testobj = { bar: 'abc' };
  }
  ```

  **正例**

    ```javascript
  var test = 'test';
  var testObj = { item:'item' };
  var testArr = [1,2,3];
  
  function foo(test) {
      var bar = test;
  }
  
  function foo(testObj) {
      var test = fish.extend({}, testObj);
  }
  
  function foo(testArr) {
      var test = testArr.slice();
  }
  ```

- [9.6](9.6) <a name="9.6"></a>立即执行函数需要通过圆括号包围。

  **检查方式**：工具检查（eslint: [`wrap-iife`](https://eslint.org/docs/latest/rules/wrap-iife)）

  **<font color=red>反例</font>**

    ```javascript
  var testA = function () { return { y: 1 };}();
  var testB = (function () { return { y: 1 };})();
  ```

  **正例**

    ```javascript
  var testA = (function () { return { y: 1 };}());
  ```

- [9.7](9.7) <a name="9.7"></a>不允许函数参数使用相同的参数名。

  **检查方式**：工具检查（eslint: [`no-dupe-args`](https://eslint.org/docs/latest/rules/no-dupe-args)）

  **<font color=red>反例</font>**

    ```javascript
  function foo(val, index, val) {
      console.log('value of the second a:', val);
  }
  var bar = function (val, index, val) {
      console.log('value of the second a:', val);
  };
  ```

  **正例**

    ```javascript
  function foo(val, index, num) {
      console.log(val, index, num);
  }
  var bar = function (val, index, num) {
      console.log(val, index, num);
  };
  ```

- [9.8](9.8) <a name="9.8"></a>使用函数声明书写的函数，不允许被重写或重新赋值。

  **检查方式**：工具检查（eslint: [`no-func-assign`](https://eslint.org/docs/latest/rules/no-func-assign)）

  **<font color=red>反例</font>**

    ```javascript
  function foo() {}
  function bar() {}
  foo = bar;
  function foo() {
      doSomething();
  }
  ```

  **正例**

    ```javascript
  var foo = function () {}
  var bar = function () {}
  foo = bar;
  function foo(foo) { // `foo` is shadowed.
      foo = bar;
  }
  function foo() {
      var foo = bar;  // `foo` is shadowed.
  }
  ```

- [9.9](9.9) <a name="9.9"></a>在调用不带参的构造函数时必须加圆括号。

  **检查方式**：工具检查（eslint: [`new-parens`](https://eslint.org/docs/latest/rules/new-parens)）

  **<font color=red>反例</font>**

    ```javascript
  var person = new Person;
  ```

  **正例**

    ```javascript
  var person = new Person();
  ```

- [9.10](9.10) <a name="9.10"></a>禁止不严格要求的函数属性名加引号。

  **检查方式**：工具检查（eslint: [`quote-props`](https://eslint.org/docs/latest/rules/quote-props)）

  **<font color=red>反例</font>**

    ```javascript
  var object = {
      'a': 0,
      '0': 0,
      'true': 0,
      'null': 0
  };
  ```

  **正例**

    ```javascript
  var object1 = {
      'a-b': 0,
      '0x0': 0,
      '1e2': 0
  };
  var object2 = {
      foo: 'bar',
      baz: 42,
      true: 0,
      0: 0,
      'qux-lorem': true
  };
  ```

# 属性

- [10.1](10.1) <a name="10.1"></a>直接通过属性名来访问对象属性时，使用 `.` 来访问对象的属性。

  **检查方式**：工具检查（eslint: [`dot-notation`](https://eslint.org/docs/latest/rules/dot-notation)）

  **<font color=red>反例</font>**

    ```javascript
  var luke = {
      jedi: true,
      age: 28
  };
  
  var isJedi = luke['jedi'];
  ```

  **正例**

    ```javascript
  var luke = {
      jedi: true,
      age: 28
  };
  
  var isJedi = luke.jedi;
  ```

- [10.2](10.2) <a name="10.2"></a>当需要通过变量间接访问对象属性时使用中括号 `[]`。

  **检查方式**：人工检查

  **正例**

    ```javascript
  var luke = {
      jedi: true,
      age: 28
  };
  
  function getProp(prop) {
      return luke[prop];
  }
  
  var isJedi = getProp('jedi');
  ```

- [10.3](10.3) <a name="10.3"></a>规定声明对象的属性时只能一行声明所有的属性或者每行声明一个属性。

  **检查方式**：工具检查（eslint: [`object-property-newline`](https://eslint.org/docs/latest/rules/object-property-newline)）

  **<font color=red>反例</font>**

    ```javascript
  var obj1 = { foo: 'foo', bar: 'bar',
      baz: 'baz'
  };
  ```

  **正例**

    ```javascript
  var obj1 = { foo: 'foo', bar: 'bar', baz: 'baz' };
  var obj2 = {
      foo: 'foo',
      bar: 'bar',
      baz: 'baz'
  };
  ```

- [10.4](10.4) <a name="10.4"></a>禁止使用__proto__属性，__proto__属性已从ECMAScript 3.1开始弃用，不应在代码中使用，改用getPrototypeOf方法。

  **检查方式**：工具检查（eslint: [`no-proto`](https://eslint.org/docs/latest/rules/no-proto)）

  **<font color=red>反例</font>**

    ```javascript
  var testA = obj.__proto__;
  var testB = obj['__proto__'];
  ```

  **正例**

    ```javascript
  var testA = Object.getPrototypeOf(obj);
  ```

- [10.5](10.5) <a name="10.5"></a>__iterator__属性是JavaScript的SpiderMonkey扩展，可用于创建与JavaScript for in和for each构造兼容的自定义迭代器。但是，此属性现在已过时，因此不应使用它。

  **检查方式**：工具检查（eslint: [`no-iterator`](https://eslint.org/docs/latest/rules/no-iterator)）

  **<font color=red>反例</font>**

    ```javascript
  Foo.prototype.__iterator__ = function() {
      return new FooIterator(this);
  };
  foo.__iterator__ = function () {};
  foo['__iterator__'] = function () {};
  ```

# 运算符 & 等号

- [11.1](11.1) <a name="11.1"></a> **【警告】** 使用 === 和 !==，禁止使用 == 和 !=。

  **检查方式**：工具检查（eslint: [`eqeqeq`](https://eslint.org/docs/latest/rules/eqeqeq)）（暂未支持）

  - 条件表达式例如 `if` 语句通过抽象方法 `ToBoolean` 强制计算它们的表达式并且总是遵守下面的规则：

    + **对象** 被计算为 **true**
    + **Undefined** 被计算为 **false**
    + **Null** 被计算为 **false**
    + **布尔值** 被计算为 **布尔的值**
    + **数字** 如果是 **+0、-0 或 NaN** 被计算为 **false**，否则为 **true**
    + **字符串** 如果是空字符串 `''` 被计算为 **false**，否则为 **true**

  **正例**

    ```javascript
  if ([0]) {
      // true
  }
  ```

  *[说明] 一个数组就是一个对象，对象被计算为 true。*

- [11.2](11.2) <a name="11.2"></a>使用快捷方式。

  **检查方式**：人工检查

  **<font color=red>反例</font>**

    ```javascript
  if (name !== '') {
     // ...stuff...
  }
  
  if (collection.length > 0) {
      // ...stuff...
  }
  ```

  **正例**

    ```javascript
  if (name) {
      // ...stuff...
  }
  
  if (collection.length) {
      // ...stuff...
  }
  ```

- [11.3](11.3) <a name="11.3"></a>对于绝大多数的使用情况下，结果typeof操作是下列字符串常量之一："undefined"，"object"，"boolean"，"number"，"string"，"function"和"symbol"。将typeof运算符的结果与其他字符串文字进行比较通常是代码编写出现错误。

  **检查方式**：工具检查（eslint: [`valid-typeof`](https://eslint.org/docs/latest/rules/valid-typeof)）

  **<font color=red>反例</font>**

    ```javascript
  typeof foo === undefined;
  typeof bar === Object;
  typeof baz === 'strnig';
  typeof qux === 'some invalid type';
  typeof baz === anotherVariable;
  typeof foo === 5;
  ```

  **正例**

    ```javascript
  typeof foo === 'undefined';
  typeof bar === 'object';
  typeof baz === 'string';
  typeof bar === typeof qux;
  ```

- [11.4](11.4) <a name="11.4"></a>避免出现与本身作比较的语句。

  **检查方式**：工具检查（eslint: [`no-self-compare`](https://eslint.org/docs/latest/rules/no-self-compare)）

  **<font color=red>反例</font>**

    ```javascript
  var item = 10;
  if (item === item) {
      item = 20;
  }
  ```

  **正例**

    ```javascript
  var testA = 10;
  var testB = 10;
  if (testA === testB) {
      testA = 20;
  }
  ```

- [11.5](11.5) <a name="11.5"></a>禁止对关系运算符的左操作数使用否定运算符。

  **检查方式**：工具检查（eslint: [`no-unsafe-negation`](https://eslint.org/docs/latest/rules/no-unsafe-negation)）

  **<font color=red>反例</font>**

    ```javascript
  if (!key in object) {
      // operator precedence makes it equivalent to (!key) in object
      // and type conversion makes it equivalent to (key ? "false" : "true") in object
  }
  if (!obj instanceof Ctor) {
      // operator precedence makes it equivalent to (!obj) instanceof Ctor
      // and it equivalent to always false since boolean values are not objects.
  }
  ```

  **正例**

    ```javascript
  if (!(key in object)) {
      // key is not in object
  }
  if (!(obj instanceof Ctor)) {
      // obj is not an instance of Ctor
  }
  if(('' + !key) in object) {
      // make operator precedence and type conversion explicit
      // in a rare situation when that is the intended meaning
  }
  ```

- [11.6](11.6) <a name="11.6"></a>禁止使用位运算符。

  **检查方式**：工具检查（eslint: [`no-bitwise`](https://eslint.org/docs/latest/rules/no-bitwise)）

  **<font color=red>反例</font>**

    ```javascript
  var test = y | z;
  var test = y & z;
  x |= y;
  x &= y;
  var test = y ^ z;
  var test = ~ z;
  var test = y << z;
  var test = y >> z;
  ```

- [11.7](11.7) <a name="11.7"></a>禁止混合使用不同的运算符，如连续使用不带括号的不同运算符。用括号括起复杂的表达式可以清晰表达开发人员的意图，使代码更具可读性。

  **检查方式**：工具检查（eslint: [`no-mixed-operators`](https://eslint.org/docs/latest/rules/no-mixed-operators)）

  **<font color=red>反例</font>**

    ```javascript
  var foo = a + b * c;
  ```

  **正例**

    ```javascript
  var foo = a + (b * c);
  var foo = (a + b) * c;
  ```

- [11.8](11.8) <a name="11.8"></a>三元运算符禁止嵌套。

  **检查方式**：工具检查（eslint: [`no-nested-ternary`](https://eslint.org/docs/latest/rules/no-nested-ternary)）

  **<font color=red>反例</font>**

    ```javascript
  var thing = foo ? bar : baz === qux ? quxx : foobar;
  foo ? baz === qux ? quxx() : foobar() : bar();
  ```

  **正例**

    ```javascript
  var thing = foo ? bar : foobar;
  if (foo) {
      thing = bar;
  } else if (baz === qux) {
      thing = quxx;
  } else {
      thing = foobar;
  }
  ```

- [11.9](11.9) <a name="11.9"></a>禁止使用没有必要的三元运算符。因为有些三元运算符可以直接使用其他语句替换。

  **检查方式**：工具检查（eslint: [`no-unneeded-ternary`](https://eslint.org/docs/latest/rules/no-unneeded-ternary)）

  **<font color=red>反例</font>**

    ```javascript
  var test = x === 2 ? true : false;
  var test = x === 2 ? false : true;
  ```

  **正例**

    ```javascript
  var test = x === 2;
  var test = x !== 2;
  ```

- [11.10](11.10) <a name="11.1"></a>尽可能的使用赋值运算符的简写形式。

  **检查方式**：工具检查（eslint: [`operator-assignment`](https://eslint.org/docs/latest/rules/operator-assignment)）

  **<font color=red>反例</font>**

    ```javascript
  var testA = 1;
  var testB = 2;
  testA = testA + testB;
  testA[0] = testA[0] / testB;
  ```

  **正例**

    ```javascript
  var testA = 1;
  var testB = 2;
  testA = testB;
  testA += testB;
  testA[0] /= testB;
  ```

# 块

- [12.1](12.1) <a name="12.1"></a>if、for等语句的执行语句部分无论多少句语句都要使用括号{}包裹（只有一句语句时也要使用{}包裹）。

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

- [12.2](12.2) <a name="12.2"></a>如果通过 `if` 和 `else` 使用多行代码块，把 `else` 放在 `if` 代码块关闭括号的同一行。

  **检查方式**：工具检查（eslint: [`brace-style`](https://eslint.org/docs/latest/rules/brace-style)）

  **<font color=red>反例</font>**

    ```javascript
  if (test) {
      thing1();
      thing2();
  }
  else {
      thing3();
  }
  ```

  **正例**

    ```javascript
  if (test) {
      thing1();
      thing2();
  } else {
      thing3();
  }
  ```

- [12.3](12.3) <a name="12.3"></a>避免代码中出现空的代码块。

  **检查方式**：工具检查（eslint: [`no-empty`](https://eslint.org/docs/latest/rules/no-empty)）

  **<font color=red>反例</font>**

    ```javascript
  if (foo) {
  }
  
  while (foo) {
  }
  
  switch(foo) {
  }
  ```

  **正例**

    ```javascript
  if (foo) {
      // empty
  }
  
  while (foo) {
      /* empty */
  }
  ```

- [12.4](12.4) <a name="12.4"></a>不允许重写通过catch代码块捕获到的错误。

  **检查方式**：工具检查（eslint: [`no-ex-assign`](https://eslint.org/docs/latest/rules/no-ex-assign)）

  **<font color=red>反例</font>**

    ```javascript
  try {
      // code
  } catch (e) {
      e = 10;
  }
  ```

  **正例**

    ```javascript
  try {
      // code
  } catch (e) {
      var foo = 10;
  }
  ```

- [12.5](12.5) <a name="12.5"></a>禁止使用带有循环语句或switch语句的标签，并且禁止标签与break和continue一起使用。

  **检查方式**：工具检查（eslint: [`no-labels`](https://eslint.org/docs/latest/rules/no-labels)）

  **<font color=red>反例</font>**

    ```javascript
  label:
      while(true) {
          break label;
      }
  
  label:
      while(true) {
          continue label;
      }
  
  label:
      switch (a) {
      case 0:
          break label;
      }
  ```

  **正例**

    ```javascript
  while (true) {
      break;
  }
  
  while (true) {
      continue;
  }
  ```

- [12.6](12.6) <a name="12.6"></a>禁止不必要的嵌套块。

  **检查方式**：工具检查（eslint: [`no-lone-blocks`](https://eslint.org/docs/latest/rules/no-lone-blocks)）

  **<font color=red>反例</font>**

    ```javascript
  if (foo) {
      bar();
      {
          baz();
      }
  }
  function bar() {
      {
          baz();
      }
  }
  ```

  **正例**

    ```javascript
  while (foo) {
      bar();
  }
  if (foo) {
      if (bar) {
          baz();
      }
  }
  function bar() {
      baz();
  }
  ```

- [12.7](12.7) <a name="12.7"></a>禁止在 finally 语句块中出现控制流语句，如return，throw、break、continue块。它允许间接使用，例如在 function中定义。

  **检查方式**：工具检查（eslint: [`no-unsafe-finally`](https://eslint.org/docs/latest/rules/no-unsafe-finally)）

  **<font color=red>反例</font>**

    ```javascript
  var foo = function() {
      try {
          return 1;
      } catch(err) {
          return 2;
      } finally {
          return 3;
      }
  };
  ```

  **正例**

    ```javascript
  var foo = function() {
      try {
          return 1;
      } catch(err) {
          return 2;
      } finally {
          console.log("hola!");
      }
  };
  ```

- [12.8](12.8) <a name="12.8"></a>此规则不允许将if语句作为else块中的唯一语句。如果if语句是else块中的唯一语句，则使用else if表单通常更清晰。

  **检查方式**：工具检查（eslint: [`no-lonely-if`](https://eslint.org/docs/latest/rules/no-lonely-if)）

  **<font color=red>反例</font>**

    ```javascript
  if (condition) {
      // ...
  } else {
      if (anotherCondition) {
          // ...
      }
  }
  
  if (condition) {
      // ...
  } else {
      if (anotherCondition) {
          // ...
      } else {
          // ...
      }
  }
  ```

  **正例**

    ```javascript
  if (condition) {
      // ...
  } else if (anotherCondition) {
      // ...
  }
  
  if (condition) {
      // ...
  } else if (anotherCondition) {
      // ...
  } else {
      // ...
  }
  ```

- [12.9](12.9) <a name="12.9"></a>要求所有的switch语句都必须要有一个default分支，如果没有则需要有注释说明是开发人员不打算设置默认行为，否则将会检测报错。

  **检查方式**：工具检查（eslint: [`default-case`](https://eslint.org/docs/latest/rules/default-case)）

  **<font color=red>反例</font>**

    ```javascript
  var test = 1;
  switch (test) {
      case 1:
          /* code */
          break;
  }
  ```

  **正例**

    ```javascript
  var testA = 1;
  var testB = 1;
  switch (testA) {
      case 1:
          /* code */
          break;
  
      default:
          /* code */
          break;
  }
  
  switch (testB) {
      case 1:
          /* code */
          break;
  
      // no default
  }
  ```

- [12.10](12.10) <a name="12.10"></a>保证在for-in 循环中使用了if 语句,注意只能遍历对象自身的属性，不能遍历原型链上的属性。

  **检查方式**：工具检查（eslint: [`guard-for-in`](https://eslint.org/docs/latest/rules/guard-for-in)）

  **<font color=red>反例</font>**

    ```javascript
  for (key in foo) {
      console.log(key);
  }
  ```

  **正例**

    ```javascript
  for (key in foo) {
      if (Object.prototype.hasOwnProperty.call(foo, key)) {
          console.log(key);
      }
  }
  ```

- [12.11](12.11) <a name="12.11"></a>尽量不要在case/default语句中使用函数声明，如果要使用请确保函数声明仅适用于当前case子句，将子句使用{}包装在块中。

  **检查方式**：工具检查（eslint: [`no-case-declarations`](https://eslint.org/docs/latest/rules/no-case-declarations)）

  **<font color=red>反例</font>**

    ```javascript
  switch (foo) {
      case 1:
          function f() {}
          break;
  
      // no default
  }
  ```

  **正例**

    ```javascript
  switch (foo) {
      // The following case clauses are wrapped into blocks using brackets
      case 1: {
          function f() {}
          break;
      }
      case 2:
          // Declarations using var without brackets are valid due to function-scope hoisting
          var z = 4;
          break;
      default: {
          /* code */
          break;
      }
  }
  ```

- [12.12](12.12) <a name="12.12"></a>禁止 if 语句中有 return 之后有 else，如果if块包含return语句，则该else块变得不必要，它的内容可以放在块外面。

  **检查方式**：工具检查（eslint: [`no-else-return`](https://eslint.org/docs/latest/rules/no-else-return)）

  **<font color=red>反例</font>**

    ```javascript
  function foo() {
      if (x) {
          return y;
      } else {
          return z;
      }
  }
  ```

  **正例**

    ```javascript
  function foo() {
      if (x) {
          return y;
      }
  
      return z;
  }
  ```

- [12.13](12.13) <a name="12.13"></a>禁止不必要的 .bind() 调用，主要是出现在为函数参数绑定到了特定的对象，但是在你的函数体内并没有用到this值。

  **检查方式**：工具检查（eslint: [`no-extra-bind`](https://eslint.org/docs/latest/rules/no-extra-bind)）

  **<font color=red>反例</font>**

    ```javascript
  var boundGetName = (function getName() {
      return 'ESLint';
  }).bind(this);
  console.log(boundGetName());
  ```

  **正例**

    ```javascript
  var boundGetName = (function getName() {
      return this.name;
  }).bind(this);
  console.log(boundGetName());
  
  var test = function () {
      return this.name;
  }.bind(this);
  console.log(test());
  ```

- [12.14](12.14) <a name="12.14"></a>禁用不必要的标签，如果循环不包含嵌套循环或开关，则不需要标记循环。您可以通过删除标签并使用break或continue不使用标签来获得相同的结果。

  **检查方式**：工具检查（eslint: [`no-extra-label`](https://eslint.org/docs/latest/rules/no-extra-label)）

  **<font color=red>反例</font>**

    ```javascript
  A: while (testA) {
      break A;
  }
  ```

  **正例**

    ```javascript
  while (testA) {
      break;
  }
  ```

- [12.15](12.15) <a name="12.15"></a>禁止 case 语句落空，旨在消除一个case情况对另一个case情况的的无意破坏。

  **检查方式**：工具检查（eslint: [`no-fallthrough`](https://eslint.org/docs/latest/rules/no-fallthrough)）

  **<font color=red>反例</font>**

    ```javascript
  var foo = 1;
  function doSomething() {
      var bar = 1;
  }
  switch (foo) {
      case 1:
          doSomething();
  
      case 2:
          doSomething();
  }
  ```

  **正例**

    ```javascript
  var foo = 1;
  function doSomething() {
      var bar = 1;
  }
  switch (foo) {
      case 1:
          doSomething();
          break;
  
      case 2:
          doSomething();
          break;
  
      default: {
          /* code */
          break;
      }
  }
  ```

- [12.16](12.16) <a name="12.16"></a>要求在使用浮点小数时，不能够省略小数点前面的数或者后面的数，必须写全。

  **检查方式**：工具检查（eslint: [`no-floating-decimal`](https://eslint.org/docs/latest/rules/no-floating-decimal)）

  **<font color=red>反例</font>**

    ```javascript
  var num = .5;
  var num = 2.;
  var num = -.7;
  ```

  **正例**

    ```javascript
  var num = 0.5;
  var num = 2.0;
  var num = -0.7;
  ```

- [12.17](12.17) <a name="12.17"></a>return 语句中不能有赋值表达式。

  **检查方式**：工具检查（eslint: [`no-return-assign`](https://eslint.org/docs/latest/rules/no-return-assign)）

  **<font color=red>反例</font>**

    ```javascript
  function doSomething() {
      return foo = bar + 2;
  }
  ```

  **正例**

    ```javascript
  function doSomething() {
      return foo === bar + 2;
  }
  ```

- [12.18](12.18) <a name="12.18"></a>禁止在代码中使用alert, confirm, and prompt, console, debugger。

  **检查方式**：工具检查（eslint: [`no-alert`](https://eslint.org/docs/latest/rules/no-alert) eslint: [`no-console`](https://eslint.org/docs/latest/rules/no-console) eslint: [`no-debugger`](https://eslint.org/docs/latest/rules/no-debugger)）

- [12.19](12.19) <a name="12.1"></a>禁止在代码中使用 arguments.caller 或 arguments.callee，使用arguments.caller和arguments.callee进行多次代码优化是不可能的。它们在未来的JavaScript版本中已被弃用，并且在严格模式下禁止在ECMAScript 5中使用它们。

  **检查方式**：工具检查（eslint: [`no-caller`](https://eslint.org/docs/latest/rules/no-caller)）

  **<font color=red>反例</font>**

    ```javascript
  [1, 2, 3, 4, 5].map(function (n) {
      return !(n > 1) ? 1 : arguments.callee(n - 1) * n;
  });
  ```

  *[说明] 计算数组中每个元素的阶乘。*

  **正例**

    ```javascript
  [1, 2, 3, 4, 5].map(function factorial(n) {
      return !(n > 1) ? 1 : factorial(n - 1) * n;
  });
  ```

  *[说明] 计算数组中每个元素的阶乘。*

- [12.20](12.20) <a name="12.20"></a>禁止在代码中使用eval()或者类似于eval()的方法，例如使用setTimeout()，setInterval()或者execScript()（仅限Internet Explorer）。

  **检查方式**：工具检查（eslint: [`no-eval`](https://eslint.org/docs/latest/rules/no-eval) eslint: [`no-implied-eval`](https://eslint.org/docs/latest/rules/no-implied-eval)  eslint: [`no-script-url`](https://eslint.org/docs/latest/rules/no-script-url)）

  **<font color=red>反例</font>**

    ```javascript
  var obj = { x: 'foo' };
  var key = 'x';
  var value = eval('obj.' + key);
  location.href = 'javascript:void(0)';
  setTimeout("alert('Hi!');", 100);
  setInterval("alert('Hi!');", 100);
  ```

  *[说明] 在链接地址中使用 javascript: 被认为是 eval 的一种形式。因为在 javascript: 链接中的代码必须由浏览器解析和赋值，其处理方式与 eval 一样。*

  **正例**

    ```javascript
  var obj = { x: 'foo' };
  var key = 'x';
  var value = obj[key];
  setTimeout(function () {
      alert('Hi!');
  }, 100);
  setInterval(function () {
      alert('Hi!');
  }, 100);
  ```

- [12.21](12.21) <a name="12.21"></a>禁止使用void方法。

  **检查方式**：工具检查（eslint: [`no-void`](https://eslint.org/docs/latest/rules/no-void)）

  **<font color=red>反例</font>**

    ```javascript
  void foo;
  var foo = void bar();
  ```

- [12.22](12.22) <a name="12.22"></a>通过throw语句抛出的对象必须是Error对象本身或者通过Error对象定义的对象。

  **检查方式**：工具检查（eslint: [`no-throw-literal`](https://eslint.org/docs/latest/rules/no-throw-literal)）

  **<font color=red>反例</font>**

    ```javascript
  throw 'error';
  throw 0;
  throw undefined;
  throw null;
  ```

  **正例**

    ```javascript
  var e = new Error('error');
  throw e;
  throw new Error();
  throw new Error('error');
  ```

- [12.23](12.23) <a name="12.23"></a>禁止自我赋值。

  **检查方式**：工具检查（eslint: [`no-self-assign`](https://eslint.org/docs/latest/rules/no-self-assign)）

  **<font color=red>反例</font>**

    ```javascript
  var foo = 1;
  var bar = [1, 2, 3];
  foo = foo;
  bar = bar;
  ```

  **正例**

    ```javascript
  var foo = 1;
  var bar = 2;
  foo = bar;
  ```

- [12.24](12.24) <a name="12.24"></a>禁止使用八进制数字和八进制的转义序列。

  **检查方式**：工具检查（eslint: [`no-octal`](https://eslint.org/docs/latest/rules/no-octal)  eslint: [`no-octal-escape`](https://eslint.org/docs/latest/rules/no-octal-escape)）

  **<font color=red>反例</font>**

    ```javascript
  var num = 071;
  var result = 5 + 07;
  var foo = 'Copyright \251';
  ```

  **正例**

    ```javascript
  var num = '0x39';
  var foo = 'Copyright \u00A9';
  ```

- [12.25](12.25) <a name="12.25"></a>代码中禁止出现没有被使用到的表达式、值或标签，常见比如短路表达式是不允许使用的。

  **检查方式**：工具检查（eslint: [`no-unused-expressions`](https://eslint.org/docs/latest/rules/no-unused-expressions)  eslint: [`no-unused-labels`](https://eslint.org/docs/latest/rules/no-unused-labels)）

  **<font color=red>反例</font>**

    ```javascript
  testA && testB();
  testA() || (testB = testC);
  
  A: var foo = 0;
  B: {
      foo();
  }
  ```

  **正例**

    ```javascript
  var foo = true;
  function test() {
      //do something
  }
  if (foo){
      test();
  } else {
      console.log('test');
  }
  ```

- [12.26](12.26) <a name="12.26"></a>禁止不必要的转义。

  **检查方式**：工具检查（eslint: [`no-useless-escape`](https://eslint.org/docs/latest/rules/no-useless-escape)）

  **<font color=red>反例</font>**

    ```javascript
  "\'";
  '\"';
  '\#';
  '\e';
  ```

  **正例**

    ```javascript
  '\'';
  '\\';
  '\n';
  ```

- [12.27](12.27) <a name="12.27"></a>禁止没有必要的return（后面没有语句了）。

  **检查方式**：工具检查（eslint: [`no-useless-return`](https://eslint.org/docs/latest/rules/no-useless-return)）

  **<font color=red>反例</font>**

    ```javascript
  function foo() {
      doSomething();
      return;
  }
  ```

  **正例**

    ```javascript
  function foo() {
      return doSomething();
  }
  ```

- [12.28](12.28) <a name="12.28"></a>规定单行最大长度为150。

  **检查方式**：工具检查（eslint: [`max-len`](https://eslint.org/docs/latest/rules/max-len)）

- [12.29](12.29) <a name="12.29"></a>禁止使用with语句,with语句可能存在问题，因为它将对象的成员添加到当前作用域，从而无法分辨块内的变量实际引用的内容。

  **检查方式**：工具检查（eslint: [`no-with`](https://eslint.org/docs/latest/rules/no-with)）

  **<font color=red>反例</font>**

    ```javascript
  with (point) {
      r = Math.sqrt(x * x + y * y); // is r a member of point?
  }
  ```

# 注释

- [13.1](13.1) <a name="13.1"></a>让注释有意义。重点在解释那些不容易立即明白的逻辑上。不要把读者的时间浪费在阅读类似于:
  i = 0; // 让i 等于0

  **检查方式**：人工检查

- [13.2](13.2) <a name="13.2"></a>函数头注释 使用 `/** ... */` 作为多行注释。包含描述、指定所有参数和返回值的类型和值。

  **检查方式**：人工检查

  **<font color=red>反例</font>**

    ```javascript
  // make() returns a new element
  // based on the passed in tag name
  //
  // @param {String} tag
  // @return {Element} element
  function make(tag) {
  
      // ...stuff...
  
      return element;
  }
  ```

  **正例**

    ```javascript
  /**
   * make() returns a new element
   * based on the passed in tag name
   *
   * @param {String} tag
   * @return {Element} element
   */
  function make(tag) {
  
      // ...stuff...
  
      return element;
  }
  ```

- [13.3](13.3) <a name="13.3"></a>使用 `//` 作为单行注释。在注释对象上面另起一行使用单行注释。并且在块注释前要插入空行。

  **检查方式**：工具检查（eslint: [`lines-around-comment`](https://eslint.org/docs/latest/rules/lines-around-comment)）

  **<font color=red>反例</font>**

    ```javascript
  function getType() {
      console.log('fetching type...'); // This is console.
      /* set the default type to 'no type'*/
      var type = 'no type';
  
      return type;
  }
  ```

  **正例**

    ```javascript
  function getType() {
      // This is console.
      console.log('fetching type...');
  
      /* set the default type to 'no type'*/
      var type = 'no type';
  
      return type;
  }
  ```

- [13.4](13.4) <a name="13.4"></a>给注释增加 `FIXME` 或 `TODO` 的前缀可以帮助其他开发者快速了解这是一个需要复查的问题，或是给需要实现的功能提供一个解决方式。这将有别于常见的注释，因为它们是可操作的，通过检测后对代码相应的注释处将会发出警告。使用 `FIXME -- need to figure this out` 或者 `TODO -- need to implement`。

  **检查方式**：工具检查（eslint: [`no-warning-comments`](https://eslint.org/docs/latest/rules/no-warning-comments)）

- 使用 `// FIXME:` 标注问题。

  **正例**

    ```javascript
  function Calculator() {
  
      // FIXME: shouldn't use a global here
      total = 0;
  
      return this;
  }
  ```

- 使用 `// TODO:` 标注问题的解决方式。

  **正例**

    ```javascript
  function Calculator() {
  
      // TODO: total should be configurable by an options param
      this.total = 0;
  
      return this;
  }
  ```

# 类型转换

- [14.1](14.1) <a name="14.1"></a>在语句开始时执行类型转换。

  **检查方式**：人工检查

- 字符串：

  **<font color=red>反例</font>**

    ```javascript
  //  => this.reviewScore = 9;
  var totalScore = this.reviewScore + '';
  ```

  **正例**

    ```javascript
  //  => this.reviewScore = 9;
  var totalScore = '' + this.reviewScore;
  ```

- [14.2](14.2) <a name="14.2"></a>使用 `parseInt`把字符串解析成数值时需要指定第二个参数：转换时使用的基数（即多少进制）。

  **检查方式**：工具检查（eslint: [`radix`](https://eslint.org/docs/latest/rules/radix)）

  **<font color=red>反例</font>**

    ```javascript
  var inputValue = '4';
  var val = parseInt(inputValue);
  ```

  **正例**

    ```javascript
  var inputValue = '4';
  var val = parseInt(inputValue, 10);
  ```

- [14.3](14.3) <a name="14.3"></a>布尔:

  **检查方式**：人工检查

  **<font color=red>反例</font>**

    ```javascript
  var age = 0;
  var hasAge = new Boolean(age);
  ```

  **正例**

    ```javascript
  var age = 0;
  var hasAge = Boolean(age);
  var hasAge = !!age;
  ```

# 构造函数

- [15.1](15.1) <a name="15.1"></a>给对象原型分配方法，而不是使用一个新对象覆盖原型。覆盖原型将导致继承出现问题：重设原型将覆盖原有原型！

  **检查方式**：人工检查

  **<font color=red>反例</font>**

    ```javascript
  function Jedi() {
      console.log('new jedi');
  }
  
  Jedi.prototype = {
      fight: function fight() {
          console.log('fighting');
      },
  
      block: function block() {
          console.log('blocking');
      }
  };
  ```

  **正例**

    ```javascript
  function Jedi() {
      console.log('new jedi');
  }
  
  Jedi.prototype.fight = function fight() {
      console.log('fighting');
  };
  
  Jedi.prototype.block = function block() {
      console.log('blocking');
  };
  ```

- [15.2](15.2) <a name="15.2"></a>禁止业务代码修改内置对象如Object、Array、Function的原型对象。

  **检查方式**：人工检查

  **<font color=red>反例</font>**

    ```javascript
  Object.prototype = {};
  ```

# 事件

- [16.1](16.1) <a name="16.1"></a>当给事件附加数据时（无论是 DOM 事件还是私有事件），传入一个对象而不是原始值。这样可以让后面的贡献者增加更多数据到事件数据而无需找出并更新事件的每一个处理器。例如，不好的写法：

  **检查方式**：人工检查

  **<font color=red>反例</font>**

    ```javascript
  $(this).trigger('listingUpdated', listing.id);
  
  ...
  
  $(this).on('listingUpdated', function (e, listingId) {
      // do something with listingId
  });
  ```

  **正例**

    ```javascript
  $(this).trigger('listingUpdated', { listingId : listing.id });
  
  ...
  
  $(this).on('listingUpdated', function (e, data) {
      // do something with data.listingId
  });
  ```

# 安全

- [17.1](17.1) <a name="17.1"></a>不要使用Math.random生成随机数，采用Web Crypto API代替
  Math.random() 函数返回一个浮点数, 伪随机数在范围(0, 1), 其生成的不能提供像密码一样安全的随机数字（黑客可以计算出客户端生成的的随机数）。不要使用它们来处理有关安全的事情。使用Web Crypto API中的crypto.getRandomValues()方法。
  [CWE-330: Use of Insufficiently Random Values](https://cwe.mitre.org/data/definitions/330.html)

  **检查方式**：人工检查

  **<font color=red>反例</font>**

    ```javascript
  var randomNumber = Math.random();
  ```

  **正例**

    ```javascript
  // 创建一个长度为1的32位无符号整数类型化数组 
    const randomArray = new Uint32Array(1); 
    // 将随机数填充到数组中 
    crypto.getRandomValues(randomArray); 
    // 获取数组中的随机数 
    var randomNumber = randomArray[0];
  ```

- [17.2](17.2) <a name="17.2"></a> 在HTTP请求的Header（Request Header）中设置X-CSRF-token安全头字段，防止CSRF漏洞，增强Web应用的安全防护能力。

  **检查方式**：人工检查

- [17.3](17.3) <a name="17.3"></a> 确保在项目中使用的 JavaScript、CSS 和其他静态资源文件在更新后能够及时被用户的浏览器获取，避免因浏览器缓存旧文件而导致的访问故障。

  **检查方式**：人工检查

  > 规范来源：严重生产故障3765517

  **正例**

  1. **版本化资源文件**：
  * 所有静态资源文件（如 `.js`、`.css`、图片等）在发布时应采用版本号或哈希值进行命名。例如：
    * `app.v1.0.0.js` 或 `app.abc123.js`
  * 在文件内容发生变化时，更新文件名，以确保浏览器加载最新版本。
  2. **使用查询参数**：
  * 对于静态资源的引用，可以在 URL 中添加版本号作为查询参数。例如：
    * `app.js?v=1.0.0`
  * 每次更新时，修改查询参数的值，以强制浏览器获取新文件。
- [17.4](17.4) <a name="17.4"></a> 强制：所有 HTTP 请求必须设置超时时间，禁止未配置超时的请求，以避免因网络异常、服务端无响应或慢响应导致的前端资源阻塞和用户体验问题。

  **检查方式**：人工检查

  > :warning: 故障警示! 本规范制定源自严重生产故障（单号：2283079 ）。
  > 对http的特性不熟悉，缺乏相应的技术储备

  注意事项：

  1. 超时后应提示用户（如 Toast、Modal）或切换至备用数据源，避免页面“假死”。
  2. 若存在长轮询（Long Polling）或 SSE（Server-Sent Events）等需长连接的场景，需在代码中明确注释原因。
  3. 通过强制要求超时设置，可显著提升前端应用的健壮性和用户体验，避免因不可控的网络或服务端问题导致系统性风险。
- [17.5](17.5) <a name="17.5"></a> 强制：禁止使用 `Date.prototype.toLocaleDateString()`

  **检查方式**：人工检查

  > **兼容性问题**：不同浏览器或环境对 `toLocaleDateString()` 的实现差异较大（如日期分隔符、语言格式），可能导致显示不一致
  > **不可预测性**：依赖用户电脑、浏览器本地化设置（如系统语言），无法保证全局统一的日期格式。

  **<font color=red>反例</font>**

    ```javascript
    var date = new Date();  
    // 输出可能因环境不同而变为 "10/5/2023"、"2023/10/5" 或 "05.10.2023"  
    var stateDate = date.toLocaleDateString();  
  ```

  **正例**
  **使用标准化工具库**

  ```javascript
     var date = new Date();  
     var stateDate = fish.dateutil.format(date, fish.config.get('dateParseFormat.datetime'))
  ```

- [17.6](17.6) <a name="17.6"></a> 强制：对于包含重要信息（如app-signature 数字签名信息等）的前端js文件需要进行混淆加固
  **使用方式**：研发云持续构建混淆加固节点

  > :warning: 故障警示! 本规范制定来源自
  > 产品安全治理-V9系列-数字签名--JS 加固（单号：11109465）安全团队在6月份已经攻破了某项目的数字签名机制，并实现了自动化加载数字签名的方案，证明我们的方案强度还不够，需要进一步加强

  **<font color=red>反例</font>**
  重要信息数字签名暴露
  ![image](uploads/217230/20ad8124-de3b-4ae8-ba2a-381e18a2d4a8/image.png)

  **正例**
  对上面反例中包含重要信息的js文件使用研发云持续构建混淆加固节点
  ![image](uploads/217230/18113dba-e6e4-476e-8c0e-67f2c1a1e239/image.png)

  经过研发云持续构建混淆加固后
  ![image](uploads/214708/f1f6d94d-b8db-411c-81ee-6afb4e15e399/image.png)

- [17.7](17.7) <a name="17.7"></a> 强制：前端应用，主要涉及到nginx的基础镜像，需要使用国际业务运营中心-平台技术部提供的基础安全镜像

  > :warning: 故障警示! 本规范制定来源自
  > 严重生产故障 3791904 某项目前端应用是通过root启动，被局方发现相关的安全隐患

  平台提供的最新基础nginx镜像，已经去除sudo权限

  **正例**
  使用平台维护的最新nginx基础镜像
  地址：https://docs.iwhalecloud.com/doi/c7dbhw/sitsWyoJ/sitsWyoP

  ```
   FROM hub-nj.iwhalecloud.com/public/oraclelinux8-nginx1.28:202603.1
  ```

- [17.8](17.8) <a name="17.8"></a> 强制：禁止在前端 js、css、html 文件中包含物理路径信息、数据库连接信息、SQL语句信息、appKey/accessSecret、对象存储 key/secret、用户名密码及其他敏感信息

  **检查方式**：人工检查

  **<font color=red>反例</font>**
  ![image](uploads/214708/f3f013dd-2bf2-4c9b-afda-61f5c2b4398f/image.png)

# 检测工具和方法

Fish封装的一套自己的代码检测规则，这些规则都是按照以上的编程规范来制定的，你可以在我们的代码文件中可以通过在命令行使用fish lint命令即可以轻松的对JavaScript代码进行检测。

- [18.1](18.1) <a name="18.1"></a>检测工具

  在项目目录中或全局里安装 `fish-cli`，推荐全局安装

    ```shell
  $ npm install @ngweb/fish-cli -g --registry=http://npm.iwhalecloud.com:8081/repository/npm-all/
  ```

  在命令行输入 `fish -v`，出现以下返回为安装成功。

  ![image](uploads/4083/d068272e-a753-418b-b13a-24a3deb93ef2/fishVersion.png)

- 使用方法

  进入到到项目目录下，在命令行终端输入 `fish lint`，就会默认自动检测项目目录下的modules目录下和app目录下的js，并生成错误信息。
  使用 `fish-lint` 检测会默认使用fish-cli内部的默认 `.eslintrc` 配置文件，业务侧配置的 `.eslintrc` 会失效，所以不要扩展 `.eslintrc` 配置项。

  检测你所指定的目录下所有js文件（不递归检测，只检测指定的当前目录下的js），所以确保你指定的目录下存在js文件。

    ```shell
  $ fish lint -dir **/*.js -noCreateFileLog -f xml
  ```

  在zcm构建中，则会执行以下命令：

    ```shell
  node --max-old-space-size=9000 /home/ZCIPClient/tools/fish-cli/bin/fish.js lint -dir **/*.js -noCreateFileLog -f xml>${result.xml}
  ```

  构建容器会事先安装好 `fish-cli`工具，在检测之前会扩大node内存，防止对复杂度较高的项目进行深度遍历时内存不够导致崩溃，然后通过shell脚本执行 `fish lint`检测命令，最后输出xml文件，此命令等效于上方本地命令。

- [18.2](18.2) <a name="18.2"></a>配置忽略检测文件

  使用编辑器在要检测的项目根目录下创建.eslintignore文件，在该文件中配置需要忽略检测的文件路径，一行配置一个路径，例如以下就是忽略检测所有的文件：

    ```
  **/*.js
  ```

  fish-cli内默认忽略的文件如下：

    ```
  frm/**/*.js
  fish.config.js
  **/node_modules
  **/*.min.js
  **/public
  **/build
  **/fish-desktop
  ```

  当 ESlint 运行之前，fish-cli 会将业务配置的.eslintignore 与默认 .eslintignore结合。

  当 ESLint 运行时，在确定哪些文件要检测之前，它会在当前工作目录中查找一个 .eslintignore 文件。如果发现了这个文件，当遍历目录时，将会应用这些偏好设置。一次只有一个 .eslintignore 文件会被使用，所以，不是当前工作目录下的 .eslintignore 文件将不会被用到。该文件的路径写法遵循了glob语法：

  - *:匹配一个路径部分中0或多个字符, 注意不匹配以.开始的路径,比如.a
  - **: 匹配0个或多个子文件夹
  - ?:匹配一个字符
  - {a,b}: 匹配a或者b, a和b也是通配符,可以由其他通配符组成
  - !: 排除文件,如!a.js表示排除文件a.js

  格式规范如下：

  - 以 # 开头的行被当作注释，不影响忽略模式。
  - 路径是相对于 .eslintignore 的位置或当前工作目录。
  - 忽略模式同 .gitignore 规范。
  - 以 ! 开头的行是否定模式，它将会重新包含一个之前被忽略的模式。
  - 除了 .eslintignore 文件中的模式，ESLint总是忽略 /node_modules/* 和 /bower_components/* 中的文件。

  例如以下写法，就是首先忽略所有js,然后去除忽略 `code/portal/src/main/webapp/modules/`下的所有js，最终可以达到指定检测该目录中js的效果：

    ```
  **/*js
  !code/portal/src/main/webapp/modules/**/*.js
  ```

- [18.3](18.3) <a name="18.3"></a>本地校验案例(以ngPortal为例)：

  1. 业务自定义的 `.eslintignore`忽略配置如下：
     ![image](uploads/4083/932a5379-abf3-437e-bf2b-d1e8a97dfc37/ignore_before.png)
  2. 在 `.eslintignore`所在目录下执行以下命令：
    ```
  // 检测所有js文件(排除.eslintignore内忽略项)
  // 不需要在创建文件时打印日志
  // 以xml的形式输出检测结果
  fish lint -dir **/*.js -noCreateFileLog -f xml
  ```

  执行结果如下：
  ![image](uploads/4083/32a84f37-108d-4310-9e03-08d1a261e10d/lint_result1.png)

  3. 可根据实际需求，自行处理lint后的参数，eg：无需输出xml格式
    ```
  fish lint -dir **/*.js
  ```

  执行结果如下：
  ![image](uploads/4083/517a7aa9-6dbf-4df3-86b4-b4f82b74e13c/lint_result2.png)

  4. 检测后的 `.eslintignore`忽略配置如下：
     ![image](uploads/4083/f49c8cc7-c025-4d4b-963f-bb660437d14c/ignore_after.png)

  5. 删除 `.eslintrc`配置文件，再次执行上方命令,执行结果如下：
     ![image](uploads/4083/b6d3d76c-f1f8-43c2-a462-61173c4ebfb5/lint_result2.png)

     <font color=red>`fish lint`检测不以业务侧配置的 `.eslintrc`为标准，而是取内置的 `.eslintrc`校验配置，所以不要扩展 `.eslintrc`，即使本地使用 `eslint`等工具验证通过，在zcm构建中依然使用 `fish lint`作为校验工具，严格按照 `ES5`规范进行校验。</font>

- [18.4](18.4) <a name="18.4"></a>如何创建自己的CI/CD检测流程

  1. 进入ZCM（https://dev.iwhalecloud.com）并登陆，点击有上角菜单——>开发中心——>持续构建，如下图：

     ![image](uploads/4083/35d19646-1167-4b05-a612-bdfad9f02add/cicd1.png)

  2. 进入持续构建页面后点击新建构建，进入新建页面如下图，配置自己的代码归属，在语言模板处选择Java+Js，最后选择要构建的的镜像，点击next

     ![image](uploads/4083/01be7c04-d7e2-401b-b6e2-c07498746cbe/cicd4.png)

  3. 在以下页面选择产品模块，如果没有找到需要的产品则需要创建产品，完成后点击next进行下一步

     ![image](uploads/4083/057ad6e6-b8b2-45f1-a046-9fe9759b4a60/cicd5.png)

  4. 在该页面打开“是否需要代码分析选项”，之后一直点击next到最后一步点击create

     ![image](uploads/4083/ee4c09cd-8b00-46eb-b25a-6da591fc7ef9/cicd6.png)

  5. 在如下界面中的点击“代码下载”选项配置代码下载的类型、路径、用户名、密码和要下载的分支，配置完成后点击“save"保存即创建完成

     ![image](uploads/4083/15e6fe42-1090-4f60-8f22-494aeb4fa724/cicd7.png)

  6. 如果想要配置例外文件，则首先需要在项目的CI_Config目录下创建.eslintignore文件，其写法参见“配置忽略检测文件”部分，然后在如下界面中的点击“代码分析”选项，将其中例外路径配置为CI_Config文件的路径，如果不填默认CI_Config在项目的根目录下，完成后点击“save"保存即创建完成，下面以ngportal为例进行配置：

     - 首先进入ngportal的根目录下的CI_Config目录下创建.eslintignore文件。

     ![image](uploads/4083/ac3a76ed-b6f9-4854-bf39-04bec20364bf/ngportal1.png)

     - 在.eslintignore文件中通过首先忽略检测所有文件，然后指定要检测的文件目录的形式达到指定检测特定目录的代码的效果，注意 `*.js`的写法，一定要告诉检测工具你需要检测的是这个目录下的所有js文件，否则你的设置可能失效。

       ![image](uploads/4083/683cbc88-31be-41c7-a782-8741dbb0e516/ngportal2.png)

     - 由于我们按照CICD的默认设置将CI_Config目录创建在了项目的根目录下，所以在下图中的例外路径这里我们可以默认不填，如果没有将CI_Config目录按照约定设置在根目录下则需要在此重新设置路径

       ![image](uploads/4083/8795cff4-82fc-4f43-9ac8-dfc9b2b3a391/cicd10.png)

  7. 找到创建的流程点击构建，等待流程构建完毕，在下方找到对应的检测结果，点击即可查看，如下图：

     ![image](uploads/4083/b637f1b1-b644-4bb4-91b8-158f0ae21d80/cicd8.png)

     ![image](uploads/4083/8a7f9452-8a78-4309-bf88-279614a239f2/cicd9.png)

# IDE工具配置

## VSCODE ESLINT配置

Visual Studio Code (简称 VSCode / VSC) 是一款免费开源的现代化轻量级代码编辑器，软件跨平台支持 Win、Mac 以及 Linux，运行流畅，并且为我们提供了丰富的扩展工具，推荐使用它作为我们前端开发的工具，接下来我们将介绍如何在VSCode内配置实时检测和一键格式化的功能。

- 实时检测功能配置步骤：

  1. 首先需要进入命令行工具（cmd）全局安装 `fish`的 `eslint`规则包，使用如下命令：
    ```shell
  $ npm i -g @ztesoft/eslint-config eslint@5.16.0 @babel/eslint-parser@7.16.5 --registry http://npm.iwhalecloud.com:8081/repository/npm-all/
  ```

  2. 使用VSCode打开项目，点击VSCode右侧工具栏中的扩展选项，搜索eslint，点击安装

     ![image](uploads/4083/135aba49-d722-4457-bdb8-6d55364d0b63/tool1.png)

  3. 安装完成后重新打开VSCode即可在编写js代码时实时检测不符合规范的写法，并给出标红提示

     ![image](uploads/4083/8ae00bb7-b478-4b6d-a044-1b1604d6f7ee/tool2.png)

- 一键格式化功能配置：

  1. 使用VSCode打开项目，点击VSCode右侧工具栏中的扩展选项，搜索prettier，点击安装

     ![image](uploads/4083/32e0a510-59bb-4072-9470-372cbce504c7/tool3.png)

  2. 重新打开项目找到需要格式化的文件，右键选择格式化文档（快捷键：Shift+Alt+F)，即可一键解决代码中的空格、逗号、引号、单行长度等格式问题

     ![image](uploads/4083/92e968ea-5b42-451c-905a-15821e87d751/tool4.png)

- 温馨提示：以上工具的使用需要在项目的根目录中有 `.eslintrc.js`和 `.prettierrc`文件，如果使用fish-cli创建的项目中都会自动生成这两个文件，当然如果你已经按照上面的工具安装了fish-cli并且使用的 `fish lint`命令对项目进行了检测，这时也会在你相应的目录中生成这两个文件，具体文件内容如下，请确保你的文件与此相同：

  ![image](uploads/4083/76af3369-dce6-42db-a2dc-4fee24035154/tool5.png)

  ![image](uploads/4083/656aa8a0-7c84-4b02-b93b-42cf84bfa242/tool6.png)

  ## IDEA ESLINT 配置

- idea编辑器eslint配置：

  - 前提条件：

    1. 安装node.js(推荐nodejs 12.21.0版本)

    2. 执行如下命令：

              ```shell
       $ npm i -g @ztesoft/eslint-config eslint@5.16.0 @babel/eslint-parser@7.16.5 --registry http://npm.iwhalecloud.com:8081/repository/npm-all/
       ```

  - 配置步骤：

    1. 配置JavaScript语言使用ES5语法

    ![image](uploads/4083/4944a4b7-b38a-4d98-a734-bfc139d922ef/tool7.png)

    2. 配置eslint :
       .eslintrc.js 基本配置：

              ```js
       module.exports = {
         extends: '@ztesoft'
       }
       ```

    注：`fish lint` 检测工具会强制使用内部 `.eslintrc`默认配置，忽略业务配置，所以不要对eslint规则扩充；
    ![image](uploads/71741/a2b658ba-986f-4afb-9115-520f73c9ae13/image.png)

  - 使用方法：
    选择需要检测js的文件或文件夹，右键菜单选择 Analyze -> Inspect Code

    ![image](uploads/4083/a2e35518-e342-4e7e-aec2-a4c7efbdc6c9/tool9.png)

  - 结果示例:

    ![image](uploads/4083/dec16f9c-60ba-4c11-81de-c0d07d8cd9b5/tool10.png)

# FAQ

**Q：我的项目 前端告警数量很多，有没有什么工具可以把ESLint检查出的代码给自动修复的呢？**
A: ESLint有个fix命令能修复ESLint检查出的错误。但ESLint fix命令会改变业务逻辑的，举一个例子 如它会把 == 都换成 ===，导致业务逻辑出了问题。
规范组做了个 `[浩鲸js规范空白格式化工具](https://docs.iwhalecloud.com/bidjefd/share?d=gcb#didqysAxfY)` 对空格、空行、双引号之类不影响业务逻辑的进行格式化。（注：目前只对空格、空行、双引号之类不影响业务逻辑的错误进行修复，因为格式化自动修复涉及到业务代码的修改，要谨慎。）

**Q：eslint效验的规则有相关的文档说明么？我们这边ZCM代码分析的XML错误日志，想参考文档改下代码**
A: 举个例子 `<error line="508" column="11" severity="error" message="'originSwaggerData' is never reassigned. Use 'const' instead. (prefer-const)" source="eslint.rules.prefer-const"/>`

1. 打开 [http://eslint.cn/](http://eslint.cn/)  或者[eslint英文官网](https://eslint.org/)
2. 在顶部输入框中 输入XML中 `source`字段的 prefer-const
3. 即显示出详细的规则说明，正反例，以及如何修复

# 代码检查项

| 规则       | 检查方式             | 以下部分对照《JavaScript(ES5)语言编码规范》              | 严重性 | 处理建议       |
| ---------- | -------------------- | ---------------------------------------- | ------ | -------------- |
| 规则 1.1   | 人工检查             | 代码走查命名                             | 低     | 修改后重新走查 |
| 规则 1.2   | 工具检查             | 研发云eslint进行检查                     | 低     | 修改后重新走查 |
| 规则 1.3   | 工具检查             | 研发云eslint进行检查                     | 低     | 修改后重新走查 |
| 规则 1.4   | 人工检查             | 代码走查文件名与类名                      | 低     | 修改后重新走查 |
| 规则 2.1   | 工具检查             | 研发云eslint进行检查                     | 低     | 修改后重新走查 |
| 规则 2.2   | 工具检查             | 研发云eslint进行检查                     | 低     | 修改后重新走查 |
| 规则 2.3   | 工具检查             | 研发云eslint进行检查                     | 低     | 修改后重新走查 |
| 规则 2.4   | 工具检查             | 研发云eslint进行检查                     | 低     | 修改后重新走查 |
| 规则 2.5   | 工具检查             | 研发云eslint进行检查                     | 低     | 修改后重新走查 |
| 规则 2.6   | 工具检查             | 研发云eslint进行检查                     | 低     | 修改后重新走查 |
| 规则 2.7   | 工具检查             | 研发云eslint进行检查                     | 低     | 修改后重新走查 |
| 规则 2.8   | 工具检查             | 研发云eslint进行检查                     | 低     | 修改后重新走查 |
| 规则 2.9   | 工具检查             | 研发云eslint进行检查                     | 低     | 修改后重新走查 |
| 规则 2.10  | 工具检查             | 研发云eslint进行检查                     | 低     | 修改后重新走查 |
| 规则 2.11  | 工具检查             | 研发云eslint进行检查                     | 低     | 修改后重新走查 |
| 规则 2.12  | 工具检查             | 研发云eslint进行检查                     | 低     | 修改后重新走查 |
| 规则 2.13  | 工具检查             | 研发云eslint进行检查                     | 低     | 修改后重新走查 |
| 规则 2.14  | 工具检查             | 研发云eslint进行检查                     | 低     | 修改后重新走查 |
| 规则 2.15  | 工具检查             | 研发云eslint进行检查                     | 低     | 修改后重新走查 |
| 规则 2.16  | 工具检查             | 研发云eslint进行检查                     | 低     | 修改后重新走查 |
| 规则 2.17  | 工具检查             | 研发云eslint进行检查                     | 低     | 修改后重新走查 |
| 规则 2.18  | 工具检查             | 研发云eslint进行检查                     | 低     | 修改后重新走查 |
| 规则 2.19  | 工具检查             | 研发云eslint进行检查                     | 低     | 修改后重新走查 |
| 规则 2.20  | 工具检查             | 研发云eslint进行检查                     | 低     | 修改后重新走查 |
| 规则 2.21  | 工具检查             | 研发云eslint进行检查                     | 低     | 修改后重新走查 |
| 规则 2.22  | 工具检查             | 研发云eslint进行检查                     | 低     | 修改后重新走查 |
| 规则 2.23  | 工具检查             | 研发云eslint进行检查                     | 低     | 修改后重新走查 |
| 规则 3.1   | 工具检查             | 研发云eslint进行检查                     | 低     | 修改后重新走查 |
| 规则 3.2   | 工具检查             | 研发云eslint进行检查                     | 中     | 修改后重新走查 |
| 规则 3.3   | 工具检查             | 研发云eslint进行检查                     | 低     | 修改后重新走查 |
| 规则 3.4   | 工具检查             | 研发云eslint进行检查                     | 低     | 修改后重新走查 |
| 规则 4.1   | 工具检查             | 研发云eslint进行检查                     | 低     | 修改后重新走查 |
| 规则 4.2   | 工具检查             | 研发云eslint进行检查                     | 低     | 修改后重新走查 |
| 规则 5.1   | 工具检查             | 研发云eslint进行检查                     | 低     | 修改后重新走查 |
| 规则 5.2   | 工具检查             | 研发云eslint进行检查                     | 中     | 修改后重新走查 |
| 规则 5.3   | 工具检查             | 研发云eslint进行检查                     | 低     | 修改后重新走查 |
| 规则 5.4   | 人工检查             | 代码走查未赋值变量的声明位置               | 低     | 修改后重新走查 |
| 规则 5.5   | 工具检查             | 研发云eslint进行检查                     | 中     | 修改后重新走查 |
| 规则 5.6   | 工具检查（暂未支持）   | 代码走查变量是否重复声明                   | 低     | 修改后重新走查 |
| 规则 5.7   | 工具检查             | 研发云eslint进行检查                     | 低     | 修改后重新走查 |
| 规则 5.8   | 工具检查             | 研发云eslint进行检查                     |  高      | 修改后重新走查 |
| 规则 5.9   | 工具检查             | 研发云eslint进行检查                     | 低     | 修改后重新走查 |
| 规则 5.10  | 工具检查             | 研发云eslint进行检查                     | 中     | 修改后重新走查 |
| 规则 5.11  | 工具检查             | 研发云eslint进行检查                     | 低     | 修改后重新走查 |
| 规则 5.12  | 工具检查             | 研发云eslint进行检查                     | 低     | 修改后重新走查 |
| 规则 5.13  | 工具检查             | 研发云eslint进行检查                     | 高     | 修改后重新走查 |
| 规则 5.14  | 工具检查             | 研发云eslint进行检查                     | 低     | 修改后重新走查 |
| 规则 5.15  | 工具检查             | 研发云eslint进行检查                     | 低     | 修改后重新走查 |
| 规则 5.16  | 工具检查             | 研发云eslint进行检查                     | 低     | 修改后重新走查 |
| 规则 5.17  | 工具检查             | 研发云eslint进行检查                     | 低     | 修改后重新走查 |
| 规则 5.18  | 工具检查             | 研发云eslint进行检查                     | 高      | 修改后重新走查 |
| 规则 6.1   | 工具检查             | 研发云eslint进行检查                     | 中     | 修改后重新走查 |
| 规则 6.2   | 工具检查             | 研发云eslint进行检查                     | 低     | 修改后重新走查 |
| 规则 6.3   | 工具检查             | 研发云eslint进行检查                     | 高     | 修改后重新走查 |
| 规则 6.4   | 工具检查             | 研发云eslint进行检查                     | 高     | 修改后重新走查 |
| 规则 6.5   | 工具检查             | 研发云eslint进行检查                     | 高     | 修改后重新走查 |
| 规则 6.6   | 工具检查             | 研发云eslint进行检查                     | 高     | 修改后重新走查 |
| 规则 7.1   | 工具检查             | 研发云eslint进行检查                     | 中     | 修改后重新走查 |
| 规则 7.2   | 人工检查             | 代码走查数组增加元素使用.push              | 中     | 修改后重新走查 |
| 规则 7.3   | 人工检查             | 代码走查复制数组使用.slice                | 中     | 修改后重新走查 |
| 规则 7.4   | 人工检查             | 代码走查将类数组对象转换成数组使用.slice    | 中     | 修改后重新走查 |
| 规则 7.5   | 工具检查             | 研发云eslint进行检查                     | 中     | 修改后重新走查 |
| 规则 7.6   | 工具检查             | 研发云eslint进行检查                     | 中     | 修改后重新走查 |
| 规则 8.1   | 工具检查             | 研发云eslint进行检查                     | 低     | 修改后重新走查 |
| 规则 8.2   | 人工检查             | 代码走查程序化生成字符串的连接方式          | 中     | 修改后重新走查 |
| 规则 8.3   | 工具检查             | 研发云eslint进行检查                     | 低     | 修改后重新走查 |
| 规则 8.4   | 工具检查             | 研发云eslint进行检查                     | 低     | 修改后重新走查 |
| 规则 9.1   | 工具检查             | 研发云eslint进行检查                     |  高      | 修改后重新走查 |
| 规则 9.2   | 工具检查             | 研发云eslint进行检查                     | 高     | 修改后重新走查 |
| 规则 9.3   | 工具检查             | 研发云eslint进行检查                     | 低     | 修改后重新走查 |
| 规则 9.4   | 工具检查             | 研发云eslint进行检查                     | 低     | 修改后重新走查 |
| 规则 9.5   | 工具检查             | 研发云eslint进行检查                     | 高     | 修改后重新走查 |
| 规则 9.6   | 工具检查             | 研发云eslint进行检查                     | 中     | 修改后重新走查 |
| 规则 9.7   | 工具检查             | 研发云eslint进行检查                     | 高     | 修改后重新走查 |
| 规则 9.8   | 工具检查             | 研发云eslint进行检查                     | 高     | 修改后重新走查 |
| 规则 9.9   | 工具检查             | 研发云eslint进行检查                     | 高     | 修改后重新走查 |
| 规则 9.10  | 工具检查             | 研发云eslint进行检查                     | 高     | 修改后重新走查 |
| 规则 10.1  | 工具检查             | 研发云eslint进行检查                     | 低     | 修改后重新走查 |
| 规则 10.2  | 人工检查             | 代码走查通过变量间接访问对象属性的方式       | 低     | 修改后重新走查 |
| 规则 10.3  | 工具检查             | 研发云eslint进行检查                     | 低     | 修改后重新走查 |
| 规则 10.4  | 工具检查             | 研发云eslint进行检查                     | 高     | 修改后重新走查 |
| 规则 10.5  | 工具检查             | 研发云eslint进行检查                     | 高     | 修改后重新走查 |
| 规则 11.1  | 工具检查（暂未支持）   | 代码走查全等和非全等的写法                 | 高     | 修改后重新走查 |
| 规则 11.2  | 人工检查             | 代码走查if条件语句写法                    | 低     | 修改后重新走查 |
| 规则 11.3  | 工具检查             | 研发云eslint进行检查                     | 高     | 修改后重新走查 |
| 规则 11.4  | 工具检查             | 研发云eslint进行检查                     | 低     | 修改后重新走查 |
| 规则 11.5  | 工具检查             | 研发云eslint进行检查                     | 低     | 修改后重新走查 |
| 规则 11.6  | 工具检查             | 研发云eslint进行检查                     | 低     | 修改后重新走查 |
| 规则 11.7  | 工具检查             | 研发云eslint进行检查                     | 中     | 修改后重新走查 |
| 规则 11.8  | 工具检查             | 研发云eslint进行检查                     | 低     | 修改后重新走查 |
| 规则 11.9  | 工具检查             | 研发云eslint进行检查                     | 低     | 修改后重新走查 |
| 规则 11.10 | 工具检查             | 研发云eslint进行检查                     | 低     | 修改后重新走查 |
| 规则 12.1  | 工具检查             | 研发云eslint进行检查                     | 低     | 修改后重新走查 |
| 规则 12.2  | 工具检查             | 研发云eslint进行检查                     | 低     | 修改后重新走查 |
| 规则 12.3  | 工具检查             | 研发云eslint进行检查                     | 低     | 修改后重新走查 |
| 规则 12.4  | 工具检查             | 研发云eslint进行检查                     |  高      | 修改后重新走查 |
| 规则 12.5  | 工具检查             | 研发云eslint进行检查                     |  高      | 修改后重新走查 |
| 规则 12.6  | 工具检查             | 研发云eslint进行检查                     | 低     | 修改后重新走查 |
| 规则 12.7  | 工具检查             | 研发云eslint进行检查                     |  高      | 修改后重新走查 |
| 规则 12.8  | 工具检查             | 研发云eslint进行检查                     | 低     | 修改后重新走查 |
| 规则 12.9  | 工具检查             | 研发云eslint进行检查                     | 低     | 修改后重新走查 |
| 规则 12.10 | 工具检查             | 研发云eslint进行检查                     |   中     | 修改后重新走查 |
| 规则 12.11 | 工具检查             | 研发云eslint进行检查                     |    中    | 修改后重新走查 |
| 规则 12.12 | 工具检查             | 研发云eslint进行检查                     | 低     | 修改后重新走查 |
| 规则 12.13 | 工具检查             | 研发云eslint进行检查                     | 低     | 修改后重新走查 |
| 规则 12.14 | 工具检查             | 研发云eslint进行检查                     | 低     | 修改后重新走查 |
| 规则 12.15 | 工具检查             | 研发云eslint进行检查                     | 中     | 修改后重新走查 |
| 规则 12.16 | 工具检查             | 研发云eslint进行检查                     | 低     | 修改后重新走查 |
| 规则 12.17 | 工具检查             | 研发云eslint进行检查                     | 高     | 修改后重新走查 |
| 规则 12.18 | 工具检查             | 研发云eslint进行检查                     | 高     | 修改后重新走查 |
| 规则 12.19 | 工具检查             | 研发云eslint进行检查                     |  高      | 修改后重新走查 |
| 规则 12.20 | 工具检查             | 研发云eslint进行检查                     |   高     | 修改后重新走查 |
| 规则 12.21 | 工具检查             | 研发云eslint进行检查                     |   高     | 修改后重新走查 |
| 规则 12.22 | 工具检查             | 研发云eslint进行检查                     | 低     | 修改后重新走查 |
| 规则 12.23 | 工具检查             | 研发云eslint进行检查                     | 低     | 修改后重新走查 |
| 规则 12.24 | 工具检查             | 研发云eslint进行检查                     | 低     | 修改后重新走查 |
| 规则 12.25 | 工具检查             | 研发云eslint进行检查                     | 低     | 修改后重新走查 |
| 规则 12.26 | 工具检查             | 研发云eslint进行检查                     | 低     | 修改后重新走查 |
| 规则 12.27 | 工具检查             | 研发云eslint进行检查                     | 低     | 修改后重新走查 |
| 规则 12.28 | 工具检查             | 研发云eslint进行检查                     | 低     | 修改后重新走查 |
| 规则 12.29 | 工具检查             | 研发云eslint进行检查                     |  高      | 修改后重新走查 |
| 规则 13.1  | 人工检查             | 代码走查注释内容                         | 低     | 修改后重新走查 |
| 规则 13.2  | 人工检查             | 代码走查函数头注释格式                    | 低     | 修改后重新走查 |
| 规则 13.3  | 工具检查             | 研发云eslint进行检查                     | 低     | 修改后重新走查 |
| 规则 13.4  | 工具检查             | 研发云eslint进行检查                     | 低     | 修改后重新走查 |
| 规则 14.1  | 人工检查             | 代码走查执行类型转换的位置                 | 低     | 修改后重新走查 |
| 规则 14.2  | 工具检查             | 研发云eslint进行检查                     | 高     | 修改后重新走查 |
| 规则 14.3  | 人工检查             | 代码走查变量转为布尔值方式                 | 低     | 修改后重新走查 |
| 规则 15.1  | 人工检查             | 代码走查对象原型分配方法                   | 高     | 修改后重新走查 |
| 规则 15.2  | 人工检查             | 代码走查内置对象是否被修改                 | 高     | 修改后重新走查 |
| 规则 16.1  | 人工检查             | 代码走查给事件附加数据传入对象              | 低     | 修改后重新走查 |
| 规则 17.1  | 人工检查             | 代码走查随机数生成方式                    |   中     | 修改后重新走查 |
| 规则 17.2  | 人工检查             | 代码走查HTTP请求头中的安全字段             |   高    | 修改后重新走查 |
| 规则 17.3  | 人工检查             | 代码走查静态资源更新后被浏览器及时获取       |   高    | 修改后重新走查 |
| 规则 17.4  | 人工检查             | 代码走查 HTTP 请求必须设置超时时间      |   高    | 修改后重新走查 |
| 规则 17.5  | 人工检查             | 代码走查禁止使用Date.prototype.toLocaleDateString()       |   高    | 修改后重新走查 |
| 规则 17.6  | 人工检查             | 代码走查对于包含重要信息（如app-signature 数字签名信息等）的前端js文件需要进行混淆加固      |   高    | 修改后重新走查 |

# 本文件评审、修正记录

| 文件名称 | Javascript语言编码规范(es5)                                                                                                                                                   |                  |               |         |
| -------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------- | ------------- | ------- |
| 序号     | 流程                                                                                                                                                                          | 拟制人/审核人    | 拟制/审核时间 | 版本号  |
| 1        | 规范发布                                                                                                                                                                      | 王小虎           | 2019/4/19     | V1.0    |
| 2        | 在线化发布                                                                                                                                                                    | 王小虎           | 2021/7/13     | V1.1    |
| 3        | 增加18.2. IDEA ESLINT 配置                                                                                                                                                    | 王小虎           | 2021/12/30    | V1.2    |
| 4        | ESLint升级 同步修改检测工具和方法                                                                                                                                             | 王小虎           | 2021/1/17     | V1.3    |
| 5        | 修复规则“禁止出现空函数”  的举例                                                                                                                                            | 王小虎           | 2022/5/18     | V1.3.1  |
| 6        | 修复Math.pow与**运算符冲突                                                                                                                                                    | 王小虎           | 2022/6/8      | V1.3.2  |
| 7        | 发布                                                                                                                                                                          | JavaScript规范组 | 2022/6/14     | V1.4    |
| 8        | 增加FAQ、调整规则5.5：要求函数声明和变量声明在程序或函数体的顶部 改为 要求函数声明在程序或函数体的顶部                                                                        | 王小虎           | 2023/3/16     | V1.4.1  |
| 9        | 发布                                                                                                                                                                          | JavaScript规范组 | 2023/3/21     | V1.5    |
| 10       | 增加FAQ:如何根据ZCM代码分析日志查找修复方法                                                                                                                                   | 王小虎           | 2023/3/28     | V1.5.1  |
| 11       | 发布                                                                                                                                                                          | JavaScript规范组 | 2023/5/19     | V1.6    |
| 12       | 增加ES5第17章安全章节，不要使用Math.random生成随机数，采用Web Crypto API代替                                                                                                  | 王小虎           | 2023/6/30     | V1.6.1  |
| 13       | 发布                                                                                                                                                                          | JavaScript规范组 | 2023/7/20     | V1.7    |
| 14       | 因gitlab 8月底关闭，修订所有gitlab连接；修订11.1 eqeqeq规则由错误改成警告                                                                                                     | 王小虎           | 2023/8/18     | V1.7.1  |
| 15       | 完善12.20规则描述                                                                                                                                                             | 王小虎           | 2023/9/28     | V1.7.2  |
| 16       | 发布                                                                                                                                                                          | JavaScript规范组 | 2023/11/21    | V1.8    |
| 17       | 增加17.2章节 CSRF安全                                                                                                                                                         | 王小虎           | 2023/12/22    | V1.8.1  |
| 18       | 修复12.20~12.21章节中间插入了12.1章节，错乱的问题                                                                                                                             | 王小虎           | 2024/1/18     | V1.8.2  |
| 19       | 发布                                                                                                                                                                          | JavaScript规范组 | 2024/01/19    | V1.9    |
| 20       | 19.2章节修改idea ESLINT配置相关截图，以适合新的idea版本                                                                                                                       | 王小虎           | 2024/3/18     | V1.9.1  |
| 21       | 发布                                                                                                                                                                          | JavaScript规范组 | 2024/05/22    | V1.10   |
| 22       | 增加5.18禁止在变量定义之前使用它们                                                                                                                                            | 王小虎           | 2024/06/18    | V1.10.1 |
| 23       | 发布                                                                                                                                                                          | JavaScript规范组 | 2024/06/19    | V1.11   |
| 24       | 增加17.3章节 确保在项目中使用的 JavaScript、CSS 和其他静态资源文件在更新后能够及时被用户的浏览器获取，避免因浏览器缓存旧文件而导致的访问故障（规范来源：严重生产故障3765517） | 王小虎           | 2024/11/6     | V1.11.1 |
| 25       | 发布                                                                                                                                                                         | JavaScript规范组 | 2024/11/15    | V1.12   |
| 26       | 每个条款增加检查方式，并增加21章节对检查方式进行汇总便于查阅                                                                                                                                                                     | JavaScript规范组 | 2025/2/20    | V1.12.1   |
| 27       | 发布                                                                                                                                                          | JavaScript规范组 | 2025/2/24    | V1.13   |
| 28       | 增加17.4章节：所有 HTTP 请求必须设置超时时间，禁止未配置超时的请求，以避免因网络异常、服务端无响应或慢响应导致的前端资源阻塞和用户体验问题（规范来源：严重生产故障2283079）                                                                                                                                                        | 王小虎 | 2025/2/24    | V1.13.1   |
| 29       | 发布                                                                                                                                                          | JavaScript规范组 | 2025/3/24    | V1.14   |
| 30       | 增加17.5章节 强制：禁止使用 `Date.prototype.toLocaleDateString()`（规范来源： 故障单21413704）                                                                                                                                                         | JavaScript规范组 | 2025/4/10    | V1.14.1   |
| 31       | 发布                                                                                                                                                          | JavaScript规范组 | 2025/4/21    | V1.15   |
| 32       | 新增章节17.6 【强制】对于包含重要信息（如app-signature 数字签名信息等）的前端js文件需要进行混淆加固（规范来源： 安全治理单11109465）                                                                                                                                                     | JavaScript规范组 | 2025/8/18    | V1.15.1   |
| 33       | 发布                                                                                                                                                          | JavaScript规范组 | 2025/9/22    | V1.16   |
| 34       |  格式类规范条款精简                                                                                                                                                    | JavaScript规范组 | 2025/9/28    | V1.16.1   |
| 35       | 新增章节17.7 【强制】前端应用，主要涉及到nginx的基础镜像，需要使用国际业务运营中心-平台技术部提供的基础安全镜像（规范来源：          严重生产故障3791904）                                                                                                                                                     | JavaScript规范组 | 2025/10/22    | V1.16.2   |
| 36       | 发布                                                                                                                                                          | JavaScript规范组 | 2025/10/27    | V1.17   |
| 37       | 新增章节17.8 【强制】禁止在前端 js、css、html 文件中包含物理路径信息、数据库连接信息、SQL语句信息、appKey/accessSecret、对象存储 key/secret、用户名密码及其他敏感信息                                                                                                                                                     | 王小虎 | 2025/11/12    | V1.17.1   |
| 38       | 发布                                                                                                                                                          | JavaScript规范组 | 2025/11/24    | V1.18   |
| 39       | 更新章节“17.7 强制：前端应用，主要涉及到nginx的基础镜像，需要使用国际业务运营中心-平台技术部提供的基础安全镜像” 中前端安全镜像版本（最新版本，处理了近期前端容器被扫描出的安全问题）                                                                                                                                                   | 王小虎 | 2026/3/15    | V1.18.1   |
| 40       | 发布                                                                                                                                                          | JavaScript规范组 | 2026/03/23    | V1.19   |
