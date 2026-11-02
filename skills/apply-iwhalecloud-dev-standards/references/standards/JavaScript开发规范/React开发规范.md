<blockquote class="read-author-info">
<p>文档路径：epg/岗位能力认证/浩鲸在线规范库/JavaScript开发规范/React开发规范<svg class="copy-doc-path" style="cursor: pointer; margin-left: 8px; vertical-align: middle;" title="复制文档路径" data-doc-path="epg/岗位能力认证/浩鲸在线规范库/JavaScript开发规范/React开发规范" width="14" height="14" viewBox="0 0 1024 1024" xmlns="http://www.w3.org/2000/svg"><path fill="currentColor" d="M768 832a128 128 0 0 1-128 128H192A128 128 0 0 1 64 832V384a128 128 0 0 1 128-128v64a64 64 0 0 0-64 64v448a64 64 0 0 0 64 64h448a64 64 0 0 0 64-64h64z"/><path fill="currentColor" d="M384 128a64 64 0 0 0-64 64v448a64 64 0 0 0 64 64h448a64 64 0 0 0 64-64V192a64 64 0 0 0-64-64H384zm0-64h448a128 128 0 0 1 128 128v448a128 128 0 0 1-128 128H384a128 128 0 0 1-128-128V192A128 128 0 0 1 384 64z"/></svg></p>
</blockquote>

![image](uploads/234141/539733a6-ab7a-4067-9d10-7acf85bb0e70/image.png)

# 前言

React 是一个由 Facebook 开发的开源 JavaScript 库，用于构建用户界面。它通过组件化的开发模式，允许开发者高效地创建可复用的 UI 组件，并提供了虚拟 DOM 技术以优化性能。React 的核心优势在于其声明式编程范式，使得代码更易于理解和维护。在现代 Web 开发领域，React 已成为构建高性能、可扩展前端应用的首选框架之一。

本规范旨在《[JavaScript(ES6)语言编码规范](https://docs.iwhalecloud.com/bidjvsL/index?d=5lfy#/didc7dokJ)》基础上，补充 React 特有的开发规范。
在遵循本规范之前，请务必先行学习《[JavaScript(ES6)语言编码规范](https://docs.iwhalecloud.com/bidjvsL/index?d=5lfy#/didc7dokJ)》。

## 适用对象

浩鲸科技 React开发人员

## 目的

为了持续、稳定地开发出高质量，健壮的软件系统，为了保证团队中成员的编码质量，特制定本文档。用于规范团队内部开发过程，增加程序的健壮性，便于后续测试及代码维护，最终提高软件产品的生产力。

# 编程规范

## 基本规范

### 【推荐】使用 React18 及 以上版本

**检查方式**： 人工检查

> React 17已经存在 EOL 风险。目前最低安全支持版本为React 18

### 【推荐】每个文件只写一个模块.

**检查方式**： 工具检查(eslint: [`react/no-multi-comp`](https://github.com/jsx-eslint/eslint-plugin-react/blob/master/docs/rules/no-multi-comp.md)）

> 每个文件只声明一个组件可以提高组件的可读性和可重用性。

**<font color=red>反例</font>**

```javascript
// 两个组件处于同一个文件中
const Hello = ({ name }) => {
  return <div>Hello {name}</div>;
};

const HelloJohn = () => {
  return <Hello name="John" />;
};
```

**正例**

```javascript
import Hello from './components/Hello';

const HelloJohn = () => {
  return <Hello name="John" />;
};
```

### 【推荐】不要使用 React.createElement.

**检查方式**： 人工检查

> 推荐使用JSX语法，除非从一个非JSX的文件中初始化你的app

## 创建组件

### 【强制】将无状态组件编写为纯函数组件

**检查方式**： 工具检查(eslint: [`react/prefer-stateless-function`](https://github.com/jsx-eslint/eslint-plugin-react/blob/master/docs/rules/prefer-stateless-function.md)）

> 无状态功能组件比基于类的组件更简单，并且将受益于针对这些组件的 React 性能优化。

**<font color=red>反例</font>**

```javascript
class HelloComponents extends React.Component {
  render() {
    return <div>Hello {this.props.name}</div>;
  }
}

const Hello2Components = createReactClass({
  render: function() {
    return <div>Hello {this.props.name}</div>;
  }
});
```

**正例**

```javascript
const HelloComponents = (props) => {
  return <div>Hello {props.name}</div>;
};
```

### 【推荐】有状态组件使用函数组件+Hooks写法

**检查方式**： 人工检查

> 自从 React hooks 出现以来，函数组件已经成为在 React中编写组件的首选方法。它们的可读性、可测试性和可维护性使它们成为突出的选择。
> React 在 16.8 版本引入了 Hooks (钩子)。Hooks 允许您在函数组件中“钩入” React 的 state 和生命周期特性，而无需编写类。

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

**<font color=red>反例</font>**

```javascript
class CounterComponent extends React.Component {
  constructor(props) {
    super(props);
    this.state = { count: 0 }; // 类组件的状态管理
  }

  componentDidMount() {
    console.log('Component mounted');
  }

  componentDidUpdate() {
    console.log('Count updated:', this.state.count);
  }

  increment = () => {
    this.setState({ count: this.state.count + 1 }); // 更新状态
  };

  render() {
    return (
      <div>
        <p>Count: {this.state.count}</p>
        <button onClick={this.increment}>Increment</button>
      </div>
    );
  }
}
```

**正例**

```javascript
const CounterComponent = () => {
  const [count, setCount] = useState(0); // 使用 useState 管理状态

  useEffect(() => {
    // 副作用逻辑（如数据获取）
    console.log('Count updated:', count);
  }, [count]); // 依赖项为 count

  const increment = () => {
    setCount(count + 1); // 更新状态
  };

  return (
    <div>
      <p>Count: {count}</p>
      <button onClick={increment}>Increment</button>
    </div>
  );
};
```

## 命名

### 【强制】组件文件名: 文件名使用帕斯卡命名

**检查方式**： 人工检查

**<font color=red>反例</font>**
组件文件名：`reservationCard.jsx`

**正例**
组件文件名：`ReservationCard.jsx`

### 【强制】非组件文件名: 文件名使用驼峰命名法. 如, fetchApi.js

**检查方式**： 人工检查

**<font color=red>反例</font>**
非组件文件名 `FetchApi.js`

**正例**
非组件文件名 `fetchApi.js`

### 【强制】引用命名: React模块名使用帕斯卡命名，实例使用骆驼式命名

**检查方式**： 工具检查(eslint: [`react/jsx-pascal-case`](https://github.com/jsx-eslint/eslint-plugin-react/blob/master/docs/rules/jsx-pascal-case.md))

**<font color=red>反例</font>**

```javascript
  import reservationCard from './ReservationCard';

  const ReservationItem = <ReservationCard />;
```

**正例**

```javascript
import ReservationCard from './ReservationCard';

const reservationItem = <ReservationCard />;
```

### 【强制】模块命名: 模块使用当前文件名一样的名称. 比如 ReservationCard.jsx 应该包含名为 ReservationCard 的模块. 但是，如果整个文件夹是一个模块，使用 index.js(ts) 作为入口文件，然后直接使用 index.js(ts) 或者文件夹名作为模块的名称:

**检查方式**： 人工检查

**<font color=red>反例</font>**

```javascript
  // bad
  import Footer from './Footer/Footer';

  // bad
  import Footer from './Footer/index';
```

**正例**

```javascript
// good
import Footer from './Footer';
```

### 【推荐】 高阶模块命名: 对于生成一个新的模块，其中的模块名 displayName 应该为高阶模块名和传入模块名的组合. 例如, 高阶模块 withFoo(), 当传入一个 Bar 模块的时候， 生成的模块名 displayName 应该为 withFoo(Bar).

**检查方式**： 人工检查

> 为什么？一个模块的 `displayName` 可能会在开发者工具或者错误信息中使用到，因此有一个能清楚的表达这层关系的值能帮助我们更好的理解模块发生了什么，更好的Debug.

**<font color=red>反例</font>**

```javascript
// bad
export default function withFoo(WrappedComponent) {
  return function WithFoo(props) {
    return <WrappedComponent {...props} foo />;
  }
}
```

**正例**

```javascript
// good
export default function withFoo(WrappedComponent) {
  function WithFoo(props) {
    return <WrappedComponent {...props} foo />; // 注入 foo 属性
  }
  const wrappedComponentName = WrappedComponent.displayName
    || WrappedComponent.name
    || 'Component';
  WithFoo.displayName = `withFoo(${wrappedComponentName})`; // 设置 displayName
  return WithFoo;
}
```

### 【强制】 属性命名: 避免使用DOM相关的属性来用作其他的用途。

**检查方式**： 人工检查

> 为什么？对于 `style` 和 `className`这样的属性名，我们都会默认它们代表一些特殊的含义，如元素的样式，CSS class的名称。在你的应用中使用这些属性来表示其他的含义会使你的代码更难阅读，更难维护，并且可能会引起bug。

**<font color=red>反例</font>**

```javascript
// bad  
<MyComponent style="fancy" />
```

**正例**

```javascript
// good
<MyComponent variant="fancy" />
```

### 【强制】  变量命名: 变量名称应使用驼峰命名法。

**检查方式**： 工具检查（eslint: [`camelcase`](https://eslint.org/docs/latest/rules/camelcase)）

**<font color=red>反例</font>**

```javascript
let this_is_my_object = {};
function this_is_my_function() {}
```

**正例**

```javascript
const userName = 'test';
let userType = true;`
```

## 声明模块

### 【强制】 不要使用 require 方式来引用组件 或者 图片，而是使用 es6模块的标准语法

**检查方式**： 人工检查

**<font color=red>反例</font>**

```javascript
const qrCodeImg = require('@/assets/img/enter.png');
<img src={qrCodeImg} alt="" />
```

**正例**

```javascript
import qrCodeImg from '@/assets/img/enter.png';
<img src={qrCodeImg} alt="" />
```

## 代码对齐

### 【推荐】 遵循以下的JSX语法缩进/格式.

**检查方式**： 工具检查（eslint: [`react/jsx-closing-bracket-location`](https://github.com/jsx-eslint/eslint-plugin-react/blob/master/docs/rules/jsx-closing-bracket-location.md) [`react/jsx-closing-tag-location`](https://github.com/jsx-eslint/eslint-plugin-react/blob/master/docs/rules/jsx-closing-tag-location.md)）

**<font color=red>反例</font>**

```javascript
  // bad
  <Foo superLongParam="bar"
       anotherSuperLongParam="baz" />

   
```

**正例**

```javascript
  // good, 有多行属性的话, 新建一行关闭标签
  <Foo
    superLongParam="bar"
    anotherSuperLongParam="baz"
  />

  // 若能在一行中显示, 直接写成一行
  <Foo bar="bar" />

  // 子元素按照常规方式缩进
  <Foo
    superLongParam="bar"
    anotherSuperLongParam="baz"
  >  
```

## 单引号还是双引号

### 【推荐】对于JSX属性值总是使用双引号("), 其他均使用单引号(').

**检查方式**： 工具检查（eslint: [`jsx-quotes`](http://eslint.org/docs/rules/jsx-quotes)）

> 为什么? HTML属性也是用双引号, 因此JSX的属性也遵循此约定.

**<font color=red>反例</font>**

```javascript
// bad
<Foo bar='bar' />   
```

**正例**

```javascript
// good
<Foo bar="bar" />
```

## 空格

### 【推荐】总是在自动关闭的标签前加一个空格，正常情况下也不需要换行.

**检查方式**： 工具检查（eslint: [`no-multi-spaces`](http://eslint.org/docs/rules/no-multi-spaces), [`react/jsx-tag-spacing`](https://github.com/jsx-eslint/eslint-plugin-react/blob/master/docs/rules/jsx-tag-spacing.md)）

**<font color=red>反例</font>**

```javascript
  // bad
  <Foo/>

  // very bad
  <Foo                 />

  // bad
  <Foo
   /> 
```

**正例**

```javascript
// good
<Foo />
```

### 【推荐】不要在JSX {} 引用括号里两边加空格.

**检查方式**： 工具检查（eslint: [`react/jsx-curly-spacing`](https://github.com/jsx-eslint/eslint-plugin-react/blob/master/docs/rules/jsx-curly-spacing.md)）

**<font color=red>反例</font>**

```javascript
// bad  `{}` 引用括号里两边加了空格
<Foo bar={ baz } />
```

**正例**

```javascript
// good
<Foo bar={baz} />
```

### 【推荐】在JSX属性中禁止等号周围的空格.

**检查方式**： 工具检查（eslint: [`react/jsx-equals-spacing`](https://github.com/jsx-eslint/eslint-plugin-react/blob/master/docs/rules/jsx-equals-spacing.md)）

**<font color=red>反例</font>**

```javascript
// bad
<Hello name = {firstname} />;
<Hello name ={firstname} />;
<Hello name= {firstname} />;
```

**正例**

```javascript
// good
<Hello name={firstname} />;
```

## 属性

### 【推荐】JSX属性名使用骆驼式风格 camelCase.

**检查方式**： 人工检查

**<font color=red>反例</font>**

```javascript
// bad
<Foo
  UserName="hello"
  phone_number={12345678}
/>
```

**正例**

```javascript
// good
<Foo
  userName="hello"
  phoneNumber={12345678}
/>
```

### 【推荐】如果属性值为 true, 可以直接省略.

**检查方式**： 工具检查（eslint: [`react/jsx-boolean-value`](https://github.com/jsx-eslint/eslint-plugin-react/blob/master/docs/rules/jsx-boolean-value.md)）

**<font color=red>反例</font>**

```javascript
// bad
<Foo
  hidden={true}
/>
```

**正例**

```javascript
// good
<Foo hidden />
```

### 【强制】禁止使用未知的DOM属性.

**检查方式**： 工具检查（eslint：[`react/no-unknown-property`](https://github.com/jsx-eslint/eslint-plugin-react/blob/master/docs/rules/no-unknown-property.md)）

**<font color=red>反例</font>**

```javascript
// bad
const Hello = <div class="hello">Hello World</div>;
```

**正例**

```javascript
const Hello = <div className="hello">Hello World</div>;
```

### 【推荐】标签总是添加 alt 属性. 如果图片以presentation(以类似PPT方式显示)方式显示，alt 可为空, 或者 <img> 要包含 role="presentation".

**检查方式**： 工具检查（eslint: [`jsx-a11y/alt-text`](https://github.com/evcohen/eslint-plugin-jsx-a11y/blob/master/docs/rules/alt-text.md)）

**<font color=red>反例</font>**

```javascript
// bad
<img src="hello.jpg" />
```

**正例**

```javascript
  // good
  <img src="hello.jpg" alt="Me waving hello" />

  // good
  <img src="hello.jpg" role="presentation" />
```

### 【推荐】不要在 alt 值里使用如 "image", "photo", or "picture"包括图片含义这样的词.

**检查方式**： 工具检查（eslint: [`jsx-a11y/img-redundant-alt`](https://github.com/evcohen/eslint-plugin-jsx-a11y/blob/master/docs/rules/img-redundant-alt.md)）

> 为什么? 屏幕助读器已经把 `img` 标签标注为图片了, 所以没有必要再在 `alt` 里说明了.

**<font color=red>反例</font>**

```javascript
// bad
<img src="hello.jpg" alt="Picture of me waving hello" />
```

**正例**

```javascript
// good
<img src="hello.jpg" alt="Me waving hello" />
```

### 【推荐】使用有效正确的 aria role 属性值

> [ARIA roles](https://www.w3.org/TR/wai-aria/#introroles)

**检查方式**： 工具检查（eslint: [`jsx-a11y/aria-role`](https://github.com/evcohen/eslint-plugin-jsx-a11y/blob/master/docs/rules/aria-role.md)）

**<font color=red>反例</font>**

```javascript
<div role="datepicker"></div> <!-- Bad: "datepicker" is not an ARIA role -->
<div role="range"></div>      <!-- Bad: "range" is an _abstract_ ARIA role -->
<div role=""></div>           <!-- Bad: An empty ARIA role is not allowed -->
<Foo role={role}></Foo>       <!-- Bad: ignoreNonDOM is set to false or not set -->
```

**正例**

```javascript
// good
<div role="button" />
```

### 【强制】不要在标签上使用 accessKey 属性.

**检查方式**： 工具检查（eslint: [`jsx-a11y/no-access-key`](https://github.com/evcohen/eslint-plugin-jsx-a11y/blob/master/docs/rules/no-access-key.md)）

> 为什么? 屏幕助读器在键盘快捷键与键盘命令时造成的不统一性会导致阅读性更加复杂.

**<font color=red>反例</font>**

```javascript
// bad
<div accessKey="h" />
```

**正例**

```javascript
// good
<div />
```

### 【强制】避免使用数组的index来作为属性 key 的值，推荐使用唯一ID

**检查方式**： 人工检查

> [为什么?](https://www.jianshu.com/p/c74624223986)

**<font color=red>反例</font>**

```javascript
// bad
{todos.map((todo, index) =>
  <Todo
    {...todo}
    key={index}
  />
)}
```

**正例**

```javascript
// good
{todos.map(todo => (
  <Todo
    {...todo}
    key={todo.id}
  />
))}
```

### 【推荐】对于所有非必须的属性，总是手动去定义 defaultProps 属性.

**检查方式**： 人工检查

> 为什么? propTypes 可以作为模块的文档说明, 并且声明 defaultProps 的话意味着阅读代码的人不需要去假设一些默认值。更重要的是, 显示的声明默认属性可以让你的模块跳过属性类型的检查.

**<font color=red>反例</font>**

```javascript
// bad
function SFCComponent({ foo, bar, children }) {
  return <div>{foo}{bar}{children}</div>;
}
SFCComponent.propTypes = {
  foo: PropTypes.number.isRequired,
  bar: PropTypes.string,
  children: PropTypes.node,
};
```

**正例**

```javascript
// good
function SFCComponent({ foo, bar, children }) {
  return <div>{foo}{bar}{children}</div>;
}
SFCComponent.propTypes = {
  foo: PropTypes.number.isRequired,
  bar: PropTypes.string,
  children: PropTypes.node,
};
SFCComponent.defaultProps = {
  bar: '',
  children: null,
};
```

### 【推荐】组件传参尽可能少使用扩展运算符

**检查方式**： 人工检查

> 扩展运算符（...）虽然方便，但过度使用可能导致以下问题：
> 性能问题：不必要的属性传递会增加渲染开销。
> 可读性降低：隐藏了组件实际依赖的 props，难以维护。
> 潜在 Bug：可能意外覆盖或传递无关属性。
> 例外情况: - 使用了变量提升的高阶组件

**<font color=red>反例</font>**

```javascript
const ParentComponent = () => {
  const user = { name: "Alice", age: 25, role: "admin" };
  // 使用扩展运算符传递所有属性（不推荐）
  return <ChildComponent {...user} />;
};
const ChildComponent = (props) => {
  return <div>Name: {props.name}, Age: {props.age}</div>;
};
```

**正例**

```javascript
const ParentComponent = () => {
  const user = { name: "Alice", age: 25, role: "admin" };
  // 显式传递需要的属性（推荐）
  return <ChildComponent name={user.name} age={user.age} />;
};
const ChildComponent = ({ name, age }) => {
  return <div>Name: {name}, Age: {age}</div>;
};
```

### 【推荐】当jsx中的props跨越多行时，JSX中单行上的props的最大属性数量 1

**检查方式**： 工具检查（eslint: [`react/jsx-max-props-per-line`](https://github.com/jsx-eslint/eslint-plugin-react/blob/master/docs/rules/jsx-max-props-per-line.md)）

**<font color=red>反例</font>**

```javascript
<HelloComponent
  firstName="John" lastName="Smith"
  tel={5555555}
/>;
```

**正例**

```javascript
<HelloComponent
  firstName="John" 
  lastName="Smith"
  tel={5555555}
/>;
```

### 【强制】禁止在JSX中创建重复的props.

**检查方式**： 工具检查（eslint: [`react/jsx-no-duplicate-props`](https://github.com/jsx-eslint/eslint-plugin-react/blob/master/docs/rules/jsx-no-duplicate-props.md))

**<font color=red>反例</font>**

```javascript
// bad
<HelloComponent
  name="John"
  name="John"
/>;
```

**正例**

```javascript
// good
<HelloComponent
  firstName="John"
  lastName="Smith"
/>;
```

### 【强制】当我们希望使用a标签 target=_blank 来打开一个新标签页时，一定要加上 rel='noreferrer noopener'，否则你的网页就会存在很严重的安全问题.

**检查方式**： 工具检查（eslint: [`react/jsx-no-target-blank`](https://github.com/yannickcr/eslint-plugin-react/blob/ac102885765be5ff37847a871f239c6703e1c7cc/docs/rules/jsx-no-target-blank.md))

**<font color=red>反例</font>**

```javascript
// bad
var Hello = <a target='_blank' href="http://example.com/"></a>
```

**正例**

```javascript
// good
var Hello = <a target='_blank' rel='noopener noreferrer' href="http://example.com"></a>
```

## 引用

### 【强制】通过ref 引用组件实例时，禁止使用字符串 ref（如 ref="hello"）.

**检查方式**： 工具检查（eslint: [`react/no-string-refs`](https://github.com/jsx-eslint/eslint-plugin-react/blob/master/docs/rules/no-string-refs.md))

> 为什么不再使用字符串 ref？
> 性能问题：字符串 ref 需要 React 动态追踪，效率较低。
> 可维护性差：难以静态分析（如 TypeScript 支持）。
> 官方废弃：React 16.3 后推荐使用 createRef 或 useRef。

**<font color=red>反例</font>**

```javascript
  // bad
class MyComponent extends React.Component {
  componentDidMount() {
    // 通过 this.refs 访问 DOM 元素
    const myDiv = this.refs.myDiv;
    console.log(myDiv.textContent); // 输出 "Hello, world!"
    myDiv.style.color = 'red'; // 修改 DOM 样式
  }

  render() {
    return (
      <div ref="myDiv">Hello, world!</div>
    );
  }
}
```

**正例**

```javascript
  // good
const MyComponent = () => {
  const helloRef = useRef(null);

  useEffect(() => {
    const divElement = helloRef.current;
    console.log('Div content:', divElement.textContent); // 输出 "Hello, world."
    divElement.style.color = 'red'; // 修改 DOM 样式
  }, []);

  return <div ref={helloRef}>Hello, world.</div>;
};
```

## 括号

### 【强制】将多行的JSX标签写在 () 里.

**检查方式**： 工具检查（eslint: [`react/jsx-wrap-multilines`](https://github.com/jsx-eslint/eslint-plugin-react/blob/master/docs/rules/jsx-wrap-multilines.md))

**<font color=red>反例</font>**

```javascript
// bad
render() {
  return <MyComponent className="long body" foo="bar">
           <MyChild />
         </MyComponent>;
}
```

**正例**

```javascript
  // good
  render() {
    return (
      <MyComponent className="long body" foo="bar">
        <MyChild />
      </MyComponent>
    );
  }

  // good, 单行可以不需要
  render() {
    const body = <div>hello</div>;
    return <MyComponent>{body}</MyComponent>;
  }
```

## 标签

### 【强制】对于没有子元素的标签来说总是自己关闭标签.

**检查方式**： 工具检查（eslint: [`react/self-closing-comp`](https://github.com/jsx-eslint/eslint-plugin-react/blob/master/docs/rules/self-closing-comp.md))

**<font color=red>反例</font>**

```javascript
// bad
<Foo className="stuff"></Foo>
```

**正例**

```javascript
// good
<Foo className="stuff" />
```

### 【强制】如果模块有多行的属性， 关闭标签时新建一行.

**检查方式**： 工具检查（eslint: [`react/jsx-closing-bracket-location`](https://github.com/jsx-eslint/eslint-plugin-react/blob/master/docs/rules/jsx-closing-bracket-location.md))

**<font color=red>反例</font>**

```javascript
// bad
<Foo
  bar="bar"
  baz="baz" />
```

**正例**

```javascript
// good
<Foo
  bar="bar"
  baz="baz"
/>
```

## 函数

### 【强制】当在 render() 里使用事件处理方法时，提前在构造函数里把 this 绑定上去 或者声明函数时使用箭头匿名函数，箭头函数会自动设置this为当前类

**检查方式**： 工具检查（eslint: [`react/jsx-no-bind`](https://github.com/jsx-eslint/eslint-plugin-react/blob/master/docs/rules/jsx-no-bind.md))

> 为什么? 在每次 `render` 过程中， 再调用 `bind` 都会新建一个新的函数，浪费资源.

**<font color=red>反例</font>**

```javascript
  // bad
  class extends React.Component {
    onClickDiv() {
      // do stuff
    }

    render() {
      return <div onClick={this.onClickDiv.bind(this)} />;
    }
  }
```

**正例**

```javascript
  // good
  class extends React.Component {
    onClickDiv = () => {
      // do stuff
    }

    render() {
      return <div onClick={this.onClickDiv} />
    }
  }
```

### 【强制】在 render 方法中总是确保 return 返回值.

**检查方式**： 工具检查（eslint: [`react/require-render-return`](https://github.com/jsx-eslint/eslint-plugin-react/blob/master/docs/rules/require-render-return.md))

**<font color=red>反例</font>**

```javascript
// bad
render() {
  <div>Hello</div>;
}
```

**正例**

```javascript
// good
render() {
  return <div>Hello</div>;
}
```

### 【强制】禁止在 componentDidUpdate 里面使用 setState.

**检查方式**： 工具检查（ eslint：[`react/no-did-update-set-state`](https://github.com/jsx-eslint/eslint-plugin-react/blob/master/docs/rules/no-did-update-set-state.md))

> 在 componentDidUpdate 步骤期间更新状态可能会导致组件状态不确定，因此是不允许的

**<font color=red>反例</font>**

```javascript
// bad
class Hello extends React.Component {
  componentDidUpdate() {
    this.setState({
      name: this.props.name.toUpperCase()
    });
  },
  render() {
    return <div>Hello {this.state.name}</div>;
  }
};
```

**正例**

```javascript
// good
class Hello extends React.Component {
  componentDidUpdate() {
    this.props.onUpdate();
  },
  render() {
    return <div>Hello {this.props.name}</div>;
  }
};
```

### 【强制】禁止在componentWillUpdate中使用setState.

**检查方式**： 工具检查（ eslint：[`react/no-will-update-set-state`](https://github.com/jsx-eslint/eslint-plugin-react/blob/master/docs/rules/no-will-update-set-state.md))

> 在 componentWillUpdate 步骤期间更新状态可能会导致组件状态不确定，因此是不允许的

**<font color=red>反例</font>**

```javascript
// bad
class Hello extends React.Component {
  componentWillUpdate() {
    this.setState({
      name: this.props.name.toUpperCase()
    });
  },
  render() {
    return <div>Hello {this.state.name}</div>;
  }
};
```

**正例**

```javascript
// good
class Hello extends React.Component {
  componentWillUpdate() {
    this.props.prepareHandler();
  },
  render() {
    return <div>Hello {this.props.name}</div>;
  }
};
```

### 【强制】禁止使用 ReactDOM.render 的返回值.

**检查方式**： 工具检查（eslint: [`react/no-render-return-value`](https://github.com/jsx-eslint/eslint-plugin-react/blob/master/docs/rules/no-render-return-value.md))

**<font color=red>反例</font>**

```javascript
// bad
const inst = ReactDOM.render(<App />, document.body);
doSomethingWithInst(inst);
```

**正例**

```javascript
// good
ReactDOM.render(<App ref={doSomethingWithInst} />, document.body);
ReactDOM.render(<App />, document.body, doSomethingWithInst);
```

### 【强制】禁止直接改变 this.state

**检查方式**： 工具检查（eslint: [`react/no-direct-mutation-state`](https://github.com/jsx-eslint/eslint-plugin-react/blob/master/docs/rules/no-direct-mutation-state.md))

**<font color=red>反例</font>**

```javascript
class Hello extends React.Component {
  state = {
    foo: 'bar',
    count: 0,
  };

  handleClick = () => {
    this.state.count += 1;
    this.state.foo = 'baz';
  };
}
```

**正例**

```javascript
class Hello extends React.Component {
  state = {
    foo: 'bar',
    count: 0,
  };

  handleClick = () => {
    this.setState((prevState) => ({
      count: prevState.count + 1,
    }));
  };
}
```

### 【强制】React18版本及以上 禁止使用ReactDOM.render()，应使用createRoot().render()

**检查方式**： 人工检查

> React18版本及以上 禁止使用 `ReactDOM.render()`，应使用 `createRoot().render()`。

**<font color=red>反例</font>**

```javascript
import ReactDOM from 'react-dom'; 

ReactDOM.render(<App />, rootElement);
```

**正例**

```javascript
import { createRoot } from 'react-dom/client';

const root = createRoot(rootElement);
root.render(<App />);
```

## A11Y

### 【推荐】要求ARIA角色有效且不抽象,如果是开发人员创建的组件则不检测.

**检查方式**： 工具检查（eslint: [`jsx-a11y/aria-role`](https://github.com/infofarmer/eslint-plugin-jsx-a11y/blob/main/docs/rules/aria-role.md))

**<font color=red>反例</font>**

```javascript
// bad
<div role="datepicker"></div> <!-- Bad: "datepicker" is not an ARIA role -->
<div role="range"></div>      <!-- Bad: "range" is an _abstract_ ARIA role -->
<div role=""></div>           <!-- Bad: An empty ARIA role is not allowed -->
<Foo role={role}></Foo>       <!-- Bad: ignoreNonDOM is set to false or not set -->
```

**正例**

```javascript
// good
<div role="button"></div> <!-- Good: "button" is a valid ARIA role -->
<div role={role}></div> <!-- Good: role is a variable & cannot be determined until runtime. -->
<div></div> <!-- Good: No ARIA role -->
<Foo></Foo> <!-- Good: 开发人员创建的组件 -->
```

### 【推荐】要求所有aria-开头的属性都有效.

**检查方式**： 工具检查（eslint: [`jsx-a11y/aria-props`](https://github.com/evcohen/eslint-plugin-jsx-a11y/blob/master/docs/rules/aria-props.md))

**<font color=red>反例</font>**

```javascript
// bad
<div id="address_label">Enter your address</div>
<input aria-labeledby="address_label">
```

**正例**

```javascript
// good
<div id="address_label">Enter your address</div>
<input aria-labelledby="address_label">
```

### 【推荐】要求ARIA状态和属性值有效.

**检查方式**： 工具检查（eslint: [`jsx-a11y/aria-proptypes`](https://github.com/evcohen/eslint-plugin-jsx-a11y/blob/master/docs/rules/aria-proptypes.md))

**<font color=red>反例</font>**

```javascript
// Bad: the aria-hidden state is of type true/false
<span aria-hidden="yes">foo</span>
```

**正例**

```javascript
// Good: the aria-hidden state is of type true/false
<span aria-hidden="true">foo</span>
```

### 【推荐】要求所有需要替代文本的元素都具有有意义的信息

**检查方式**： 工具检查（eslint: [`jsx-a11y/alt-text`](https://github.com/evcohen/eslint-plugin-jsx-a11y/blob/master/docs/rules/alt-text.md)))

> 此规则将检查以下内容替代文本：`<img>，<area>，<input type="image">，和<object>`.

**<font color=red>反例</font>**

```javascript
// Bad
<img src="foo" />
<object {...props} />
<area {...props} />
<input type="image" {...props} />
```

**正例**

```javascript
// Good
<img src="foo" alt="Foo eating a sandwich." />
<object aria-label="foo" />
<area aria-label="foo" />
<input type="image" alt="This is descriptive!" />
```

### 【推荐】禁止img alt文本包含多余的单词，如"image", "picture", "photo".

**检查方式**： 工具检查（eslint:[`jsx-a11y/img-redundant-alt`](https://github.com/evcohen/eslint-plugin-jsx-a11y/blob/master/docs/rules/img-redundant-alt.md))

**<font color=red>反例</font>**

```javascript
// bad
<img src="foo" alt="Photo of foo being weird." />
<img src="bar" alt="Image of me at a bar!" />
<img src="baz" alt="Picture of baz fixing a bug." />
```

**正例**

```javascript
// good
<img src="foo" alt="Foo eating a sandwich." />
<img src="bar" aria-hidden alt="Picture of me taking a photo of an image" /> // Will pass because it is hidden.
<img src="baz" alt={`Baz taking a ${photo}`} /> // This is valid since photo is a variable name.
```

### 【推荐】要求 label 标签具有文本标签和关联控件,可以通过设置label的htmlFor属性为页面上的元素id或者将元素放在label标签里来实现。

**检查方式**： 工具检查（eslint: [`jsx-a11y/label-has-associated-control`](https://github.com/evcohen/eslint-plugin-jsx-a11y/blob/main/docs/rules/label-has-associated-control.md))

**<font color=red>反例</font>**

```javascript
  // bad
  function Foo(props) {
    return <label {...props} />
  }

  <input type="text" />
  <label>Surname</label>
```

**正例**

```javascript
  // good
  <label>
    Surname
    <input type="text" />
  </label>

  <label htmlFor={domId}>Surname</label>
  <input type="text" id={domId} />
```

### 【推荐】对于仅限键盘的用户，要求鼠标onmouseover / onmouseout伴随有onfocus / onblur.

**检查方式**： 工具检查（eslint: [`jsx-a11y/mouse-events-have-key-events`](https://github.com/evcohen/eslint-plugin-jsx-a11y/blob/master/docs/rules/mouse-events-have-key-events.md))

**<font color=red>反例</font>**

```javascript
// bad
<div onMouseOver={ () => void 0 } />
<div onMouseOut={ () => void 0 } />
<div onMouseOver={ () => void 0 } {...otherProps} />
<div onMouseOut={ () => void 0 } {...otherProps} />
```

**正例**

```javascript
// good
<div onMouseOver={ () => void 0 } onFocus={ () => void 0 } />
<div onMouseOut={ () => void 0 } onBlur={ () => void 0 } />
<div onMouseOver={ () => void 0 } onFocus={ () => void 0 } {...otherProps} />
<div onMouseOut={ () => void 0 } onBlur={ () => void 0 } {...otherProps} />
```

### 【推荐】具有交互式角色和交互处理程序（鼠标或按键）的元素必须是可聚焦的.

**检查方式**： 工具检查（eslint: [`jsx-a11y/interactive-supports-focus`](https://github.com/evcohen/eslint-plugin-jsx-a11y/blob/master/docs/rules/interactive-supports-focus.md))

**<font color=red>反例</font>**

```javascript
// bad
// Bad: span with onClick attribute has no tabindex
<span onclick="submitForm();" role="button">Submit</span>
// Bad: anchor element without href is not focusable
<a onclick="showNextPage();" role="button">Next page</a>
```

**正例**

```javascript
// Good: div with onClick attribute is hidden from screen reader
<div aria-hidden onClick={() => void 0} />
// Good: span with onClick attribute is in the tab order
<span onClick="doSomething();" tabIndex="0" role="button">Click me!</span>
// Good: span with onClick attribute may be focused programmatically
<span onClick="doSomething();" tabIndex="-1" role="menuitem">Click me too!</span>
```

### 【推荐】具有ARIA角色的元素必须具有该角色的所有必需属性.

**检查方式**： 工具检查（eslint: [`jsx-a11y/role-has-required-aria-props`](https://github.com/evcohen/eslint-plugin-jsx-a11y/blob/master/docs/rules/role-has-required-aria-props.md))

**<font color=red>反例</font>**

```javascript
// Bad: the checkbox role requires the aria-checked state
<span role="checkbox" aria-labelledby="foo" tabindex="0"></span>
```

**正例**

```javascript
// Good: the checkbox role requires the aria-checked state
<span role="checkbox" aria-checked="false" aria-labelledby="foo" tabindex="0"></span>
```

### 【推荐】要求定义显式或隐式角色的元素仅包含其aria-*支持的属性role.

**检查方式**： 工具检查（eslint: [`jsx-a11y/role-supports-aria-props`](https://github.com/evcohen/eslint-plugin-jsx-a11y/blob/master/docs/rules/role-supports-aria-props.md))

**<font color=red>反例</font>**

```javascript
// Bad: the radio role does not support the aria-required property
<ul role="radiogroup" aria-labelledby="foo">
    <li aria-required tabIndex="-1" role="radio" aria-checked="false">Rainbow Trout</li>
    <li aria-required tabIndex="-1" role="radio" aria-checked="false">Brook Trout</li>
    <li aria-required tabIndex="0" role="radio" aria-checked="true">Lake Trout</li>
</ul>
```

**正例**

```javascript
// Good: the radiogroup role does support the aria-required property
<ul role="radiogroup" aria-required aria-labelledby="foo">
    <li tabIndex="-1" role="radio" aria-checked="false">Rainbow Trout</li>
    <li tabIndex="-1" role="radio" aria-checked="false">Brook Trout</li>
    <li tabIndex="0" role="radio" aria-checked="true">Lake Trout</li>
</ul>
```

### 【推荐】避免使用设置tabIndex>0属性值来同步页面流与键盘选项卡顺序.

**检查方式**： 工具检查（eslint: [`jsx-a11y/tabindex-no-positive`](https://github.com/evcohen/eslint-plugin-jsx-a11y/blob/master/docs/rules/tabindex-no-positive.md))

**<font color=red>反例</font>**

```javascript
// Bad
<span tabIndex="5">foo</span>
<span tabIndex="3">bar</span>
<span tabIndex="1">baz</span>
<span tabIndex="2">never really sure what goes after baz</span>
```

**正例**

```javascript
// Good
<span tabIndex="0">foo</span>
<span tabIndex="-1">bar</span>
<span tabIndex={0}>baz</span>
```

### 【推荐】强制标题元素（h1，h2等）具有内容，并且屏幕阅读器可以访问内容。可访问意味着它不会使用aria-hiddenprop 隐藏.

**检查方式**： 工具检查（ eslint: [`jsx-a11y/heading-has-content`](https://github.com/evcohen/eslint-plugin-jsx-a11y/blob/master/docs/rules/heading-has-content.md))

**<font color=red>反例</font>**

```javascript
// Bad
<h1 />
<h1><TextWrapper aria-hidden />
```

**正例**

```javascript
// Good
<h1>Heading Content!</h1>
<h1><TextWrapper /><h1>
```

### 【推荐】要求HTML元素具有"lang"属性.

**检查方式**： 工具检查（eslint: [`jsx-a11y/lang`](https://github.com/evcohen/eslint-plugin-jsx-a11y/blob/master/docs/rules/html-has-lang.md))

**<font color=red>反例</font>**

```javascript
// Bad
<html>
```

**正例**

```javascript
// Good
<html lang="en">
<html lang="en-US">
<html lang={language}>
```

### 【推荐】scope属性只允许在<th>上使用.

**检查方式**： 工具检查（eslint: [`jsx-a11y/scope`](https://github.com/evcohen/eslint-plugin-jsx-a11y/blob/master/docs/rules/scope.md))

**<font color=red>反例</font>**

```javascript
// Bad
<div scope />
```

**正例**

```javascript
// Good
<th scope="col" />
<th scope={scope} />
```

### 【推荐】确保iframe元素具有唯一标题.

**检查方式**： 工具检查（eslint: [`jsx-a11y/iframe-has-title`](https://github.com/evcohen/eslint-plugin-jsx-a11y/blob/master/docs/rules/iframe-has-title.md))

**<font color=red>反例</font>**

```javascript
// Bad
<iframe />
<iframe {...props} />
<iframe title="" />
<iframe title={''} />
<iframe title={``} />
<iframe title={undefined} />
<iframe title={false} />
<iframe title={true} />
<iframe title={42} />
```

**正例**

```javascript
// Good
<iframe title="This is a unique title" />
<iframe title={uniqueTitle} />
```

### 【推荐】媒体元素推荐写captions属性.

**检查方式**： 工具检查（eslint: [`jsx-a11y/media-has-caption`](https://github.com/evcohen/eslint-plugin-jsx-a11y/blob/master/docs/rules/media-has-caption.md))

**<font color=red>反例</font>**

```javascript
// Bad
<audio {...props} />
<video {...props} />
```

**正例**

```javascript
// Good
<audio><track kind="captions" {...props} /></audio>
<video><track kind="captions" {...props} /></video>
<video muted {...props} ></video>
```

## Hook

### 【强制】确保总是在你的 React 函数的最顶层调用它们，不要在循环，条件或嵌套函数中调用Hook。

**检查方式**： 工具检查（eslint: [`react-hooks/rules-of-hooks`](https://zh-hans.react.dev/reference/rules/rules-of-hooks))

> 遵守这条规则，你就能确保 Hook 在每一次渲染中都按照同样的顺序被调用。这让 React 能够在多次的 useState 和 useEffect 调用之间保持 hook 状态的正确。
> 不支持在其他任何情况下调用以 use 开头的 Hook
>
> 1. 不要在条件语句或循环中调用 Hook
> 2. 不要在条件性的 return 语句之后调用 Hook
> 3. 不要在事件处理函数中调用 Hook
> 4. 不要在类组件中调用 Hook
> 5. 不要在传递给 useMemo、useReducer 或 useEffect 的函数内部调用 Hook
> 6. 不要在 try/catch/finally 代码块中调用 Hook

**<font color=red>反例</font>**

```javascript
function Bad({ cond }) {
  if (cond) {
    // 🔴 错误的：在条件语句内部（要修复这个问题，将其移到外部！）
    const theme = useContext(ThemeContext);
  }
  // ...
}
function Bad() {
  for (let i = 0; i < 10; i++) {
    // 🔴 错误的：在循环语句内部（要修复这个问题，将其移到外部！）
    const theme = useContext(ThemeContext);
  }
  // ...
}
function Bad({ cond }) {
  if (cond) {
    return;
  }
  // 🔴 错误的：在条件性 return 语句之后（要修复这个问题，将其移到 return 之前！）
  const theme = useContext(ThemeContext);
  // ...
}
function Bad() {
  function handleClick() {
    // 🔴 错误的：在事件处理函数内部（要修复这个问题，将其移到 return 之前！）
    const theme = useContext(ThemeContext);
  }
  // ...
}
function Bad() {
  const style = useMemo(() => {
    // 🔴 错误的：在 useMemo 内部调用（要修复这个问题，将其移到外部！）
    const theme = useContext(ThemeContext);
    return createStyle(theme);
  });
  // ...
}
class Bad extends React.Component {
  render() {
    // 🔴 错误的：在类组件内部调用（要修复这个问题，改写为函数组件！）
    useEffect(() => {})
    // ...
  }
}
function Bad() {
  try {
    // 🔴 错误的：在 try、catch、finally 代码块内部调用（要修复这个问题，将其移到外部！）
    const [x, setX] = useState(0);
  } catch {
    const [x, setX] = useState(1);
  }
}
```

**正例**

```javascript
// Good
function Counter() {
  // ✅ 正确的：在函数组件顶层
  const [count, setCount] = useState(0);
  // ...
}
function useWindowWidth() {
  // ✅ 正确的：在自定义 Hooks 顶层
  const [width, setWidth] = useState(window.innerWidth);
  // ...
}
```

### 【推荐】Hook 内使用到的所有外部变量/函数，应该出现在依赖数组里（React 官方建议）。

**检查方式**： 工具检查（eslint: [`react-hooks/exhaustive-deps`](https://zh-hans.react.dev/reference/rules/rules-of-hooks))

> React 的函数组件在每次渲染时都会重新执行。当你在 `useEffect`, `useCallback`, `useMemo` 等 Hook 内部使用一个来自组件作用域的变量（如 state, props）时，你实际上是“捕获”了**那一次渲染中**该变量的值。
>
> 依赖数组告诉 React：“ **只有当这个数组里的值发生变化时，才需要重新执行我的 Effect / 重新创建我的函数 / 重新计算我的值。** ”
>
> 如果一个变量在 Hook 内部被使用了，但没有被放入依赖数组：
>
> 1. Hook 不会因为这个变量的更新而重新执行。
> 2. Hook 内部的代码将继续使用它第一次执行时“捕获”到的那个**旧的、过时**的值。
>    这就是“陈旧的闭包”问题，它会导致难以追踪的 Bug。

**<font color=red>反例</font>**

```javascript
function UserProfile({ userId }) {
  const [user, setUser] = useState(null);
  const [count, setCount] = useState(0);

  // ❌ 错误：useEffect 内部用到了 count，但依赖数组里没有它
  useEffect(() => {
    console.log(`Effect 运行，捕获到的 count 值是: ${count}`);
  
    const intervalId = setInterval(() => {
      // 这里的 count 永远是 effect 第一次运行时捕获到的值（即 0）
      console.log(`定时器 tick，陈旧的 count 值: ${count}`);
    }, 1000);

    return () => {
      clearInterval(intervalId);
    };

  }, [userId]); // <--- 错误：useEffect 内部用到了 count，但依赖数组里没有它

  return (
    <div>
      <h1>用户: {user ? user.name : '加载中...'}</h1>
      <p>计数器: {count}</p>
      <button onClick={() => setCount(c => c + 1)}>增加 count</button>
    </div>
  );
}
```

# 浩鲸科技React开发环境搭建指引

## 安装准备工作

在开始搭建开发环境之前，需要了解下背景，目前公司React-native指定的工具，分别是

- **<font color=red>Eslint：</font>** ESLint 是一款开源的 JavaScript 静态代码分析工具，用于检测代码中的潜在错误、风格问题和逻辑缺陷。它通过预定义或自定义的规则集，帮助开发者统一代码规范、提升可维护性。ESLint 已成为现代前端工程的标准工具
- **<font color=red>Pretieer：</font>** Prettier 是一款流行的代码格式化工具，专注于强制统一代码风格，支持 JavaScript、TypeScript、HTML、CSS、JSON 等多种语言。它通过解析代码并重新输出符合预设规则的格式，彻底消除团队协作中的代码风格争议。Prettier 已成为现代工程化项目的标配工具，尤其适合强调代码一致性的团队。

## 本地配置指导

### 添加公司eslint规则

1. 安装所需要的依赖

```sh
yarn add @whalecloud/react-eslint-config -D
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
  extends: '@whalecloud/react-eslint-config',
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
   ![image](uploads/117923/126c9767-1c26-43b1-8d0b-a0f6757b62d6/image.png)
2. 插件配置
   确保 VSCode 输出面板中 ESlint  ESLint server是处于工作状态的，并且找到npm ESlint
   ![image](uploads/117923/c4d1c124-b7fe-47cd-b281-baf1b7a3ee52/image.png)

VSCode 的 ESLint 插件优先使用安装在当前项目中的 npm ESLint，如果当前项目中没有提供，它会使用全局安装的 npm ESLint。
然后看是否存在 ESLint 配置文件 `.eslintrc`，如果没有的话就不会去校验；如果存在VSCode 会根据你当前项目下的 `.eslintrc` 文件的规则来验证代码

### Vscode中安装Prettier

1. 插件安装
   打开VSCode，在插件扩展商店搜索 `Prettier`，点击安装，并重新加载；
   ![image](uploads/117923/c4e11154-ebcd-4082-b358-5eef522edfd8/image.png)
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
![image](uploads/117923/f1a61ed3-a810-409c-8c15-6e7e57b74253/image.png)

VSCode 的 prettier 插件将使用当前项目本地依赖中的npm prettier，如果当前项目中没有提供，将使用 prettier-vscode 插件捆绑的 prettier。
然后看是否存在 prettier 配置文件 `.prettierrc`，如果存在VSCode 会根据你当前项目下的 `.prettierrc` 文件的规则来格式化代码

# 研发云CI/CD检测流程搭建（React 工程）

1. 进入研发云（https://dev.iwhalecloud.com）并登陆，点击有上角菜单——>开发中心——>持续构建，如下图：

   ![image](uploads/258314/7783aea5-5be8-49d6-807d-cacc6e8e0f29/image.png)

2. 进入持续构建页面后点击新建构建，进入新建页面如下图，配置自己的`应用模块`，在语言模板处选择JS，最后选择要构建的的镜像。根据项目要求一步步创建
   ![image](uploads/258314/408e8d07-d62d-4630-9e9c-c64aad5858f4/image.png)

   注：`Maven 私服` 环节，不使用

3. 在"代码检查"页面打开“是否需要代码分析选项”，之后一直点击`下一步`到最后一步点击`新建构建`
   ![image](uploads/258314/3e32fbc6-f960-4a76-b80c-cd701960e726/image.png)

4. 在`编辑构建`页面中，`代码下载`节点配置自己仓库的信息
   ![image](uploads/234141/53ba0c77-09ac-4d7c-8a97-4e5b97dc2f21/image.png)

5. 在`编辑构建`页面中，添加`执行普通脚本` 配置 `build.sh`编译脚本

   ![image](uploads/258314/65e192a9-ec72-4de6-8c18-540fb58c2b1d/image.png)

   build.sh (注：可以换成 npm 、pnpm等）

   ```sh
   #!/bin/bash
   export NODE_OPTIONS=--openssl-legacy-provider
   yarn config set registry http://npm.iwhalecloud.com:8081/repository/npm-all/
   yarn install
   npm run build
   ```

   注：只进行代码分析，可以不加此 编译节点

6. 在`编辑构建`页面中，`代码分析节点`  JS 语言类型选择`REACT`

   ![image](uploads/234141/59070612-c552-422e-bdc5-ee2af41cd4e8/image.png)

7. 点击“高级配置”可以选择es6编译所使用的node版本号
   ![image](uploads/234141/ea36c93f-1d7d-4bb2-90a6-907169f587d5/image.png)

8. 创建 静态检查例外配置例外文件：

   进入 项目 的根目录下的 `CI_Config` 目录下创建 `.eslintignore` 文件（注：如果没有CI_Config目录需要创建）

   ```bash
   # 格式说明： 每一行都是一个 glob 模式表明哪些路径应该忽略检测
   # glob 模式说明： **配置零个或多个目录及子目录， *匹配除了斜杠(/)之外的所有字符， !排除符
   # 如：**/*.js 将忽略所有的 JavaScript 文件
   # 如：!code/portal-static/src/main/webapp/modules/**/*.js  忽略所有JavaScript 文件，但除去code/portal-static/src/main/webapp/modules下所有js
   # 也就是说 检测code/portal-static/src/main/webapp/modules 目录下所有的 js

   #例外文件需要通过注释的方式说明例外的原因，PQA会不定期对例外的合规性进行审计，被允许的例外场景如下
   #例外场景1：工具误报的情况。允许按照告警类型配置，需要说明误报的告警类型名称。
   #例外场景2：高复杂度函数。业务代码复杂度过高，修改概率极低，同时修改引入缺陷风险高，为避免被同文件中代码修改关联影响而设置例外。如增加设置需要先进行邮件备案审批。
   #例外场景3：外部引入的开源软件。允许目录和文件级例外，需要给出开源代码对应的访问地址。
   #例外场景4：工具自动生成的代码。允许目录和文件级例外，需要给出代码生成工具的名称。
   #例外场景5：测试代码。允许目录和文件级例外，路径或文件名中必须有test字样。
   #例外场景6：特殊场景。框架或平台类代码的特殊处理，例如对 Exception 或者 Throwable 的捕获。如增加设置需要先进行邮件备案审批。


   # 例外场景3：外部引入的开源软件。允许目录和文件级例外，需要给出开源代码对应的访问地址。
   # public目录里是引入的第三方js，开源地址：https://xxx
   public
   # node_modules目录是第三方库，开源地址：https://yyy
   node_modules
   # d.ts是第三方类型文件，开源地址：https://zzz
   **/*.d.ts

   # 例外场景4：工具自动生成的代码。允许目录和文件级例外，需要给出代码生成工具的名称。
   # 压缩后的js文件
   **/*.min.js

   # 例外场景5：测试代码。允许目录和文件级例外，路径或文件名中必须有test字样。
   # tests目录存的是 测试代码
   tests

   ```

9. 找到创建的流程点击构建，等待流程构建完毕，在下方找到对应的检测结果，点击即可查看，如下图：

![image](uploads/234141/4e23f5ea-68b8-4e6c-a14f-f1ea650b46d5/image.png)

# FAQ

# 本文件评审、修正记录

| 文件名称 | React-native语言编码规范 |               |               |        |
| ---------- | -------------------------- | --------------- | --------------- | -------- |
| 序号     | 流程                     | 拟制人/审核人 | 拟制/审核时间 | 版本号 |
| 1        | 编写                     | 王小虎        | 2025/3/20     | V0.1   |
| 2        | 正式发布                   | JavaScript规范组        | 2026/7/7     | V1.0   |
| 3        | 新增章节“2.1.1. 【推荐】使用 React18 及 以上版本”，某局点项目被扫描出来React17 EOL了，有安全合规风险，增加 React 版本的限制。  | 王小虎        | 2026/7/14     | V1.0.1   |
| 4        | 修改章节“2.12.6. 【强制】禁止直接改变 this.state”中的反例、正例       | 王小虎        | 2026/7/16     | V1.0.2   |
| 5        |  新增章节“2.12.7. 【强制】React18版本及以上 禁止使用ReactDOM.render()，应使用createRoot().render()”   | 王小虎        | 2026/7/16     | V1.0.3   |
| 6        | 发布                   | JavaScript规范组        | 2026/7/20     | V1.1   |
