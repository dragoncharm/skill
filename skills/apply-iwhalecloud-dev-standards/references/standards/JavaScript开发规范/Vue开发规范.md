<blockquote class="read-author-info">
<p>文档路径：epg/岗位能力认证/浩鲸在线规范库/JavaScript开发规范/Vue开发规范<svg class="copy-doc-path" style="cursor: pointer; margin-left: 8px; vertical-align: middle;" title="复制文档路径" data-doc-path="epg/岗位能力认证/浩鲸在线规范库/JavaScript开发规范/Vue开发规范" width="14" height="14" viewBox="0 0 1024 1024" xmlns="http://www.w3.org/2000/svg"><path fill="currentColor" d="M768 832a128 128 0 0 1-128 128H192A128 128 0 0 1 64 832V384a128 128 0 0 1 128-128v64a64 64 0 0 0-64 64v448a64 64 0 0 0 64 64h448a64 64 0 0 0 64-64h64z"/><path fill="currentColor" d="M384 128a64 64 0 0 0-64 64v448a64 64 0 0 0 64 64h448a64 64 0 0 0 64-64V192a64 64 0 0 0-64-64H384zm0-64h448a128 128 0 0 1 128 128v448a128 128 0 0 1-128 128H384a128 128 0 0 1-128-128V192A128 128 0 0 1 384 64z"/></svg></p>
</blockquote>

![image](uploads/261071/0378f791-2a7d-40ce-b8ed-958195647de7/image.png)

## 前言

Vue 是一个由尤雨溪开发的开源 JavaScript 框架，用于构建用户界面。它采用组件化的开发模式，允许开发者高效地创建可复用的 UI 组件，并基于响应式数据系统实现视图与状态的自动同步，从而简化开发流程。其核心优势在于简洁易用的 API 和渐进式设计理念，使开发者可以根据项目需求逐步引入功能。在现代 Web 开发领域，Vue 已成为构建高性能、可扩展前端应用的重要框架之一。

本规范旨在《 [JavaScript(ES6)语言编码规范](/didc7dokJ.md) 》基础上，补充 Vue 特有的开发规范。
在遵循本规范之前，请务必先行学习《 [JavaScript(ES6)语言编码规范](/didc7dokJ.md) 》。

### 适用对象

浩鲸科技 Vue 开发人员

### 目的

为了持续、稳定地开发出高质量，健壮的软件系统，为了保证团队中成员的编码质量，特制定本文档。用于规范团队内部开发过程，增加程序的健壮性，便于后续测试及代码维护，最终提高软件产品的生产力。

## 编程规范

### 组件命名与组织

#### 【强制】组件名必须为多单词

**检查方式**： 工具检查(eslint: [`vue/multi-word-component-names`]()）

> 目的：避免和 HTML 原生标签冲突，提高组件语义清晰度
> 说明：除根组件 App 外，组件名称必须使用多个单词组成。

**<font color=red>反例</font>**

```js
app.component('Todo', {
  // ...
})
```

```js
<script>
  export default {
    name: 'Todo',
    // ...
  }
</script>
```

**正例**

```js
app.component('todo-item', {
  // ...
})
```

```js
<script>
  export default {
    name: 'TodoItem',
    // ...
  }
</script>
```

**要求**

- 禁止使用：`Item`、`Card`、`Button`
- 推荐使用：`UserCard`、`OrderButton`、`TodoItem`

#### 【强制】禁止保留字和保留标签作为组件名

**检查方式**： 工具检查(eslint: [`vue/no-reserved-component-names`](), [`vue/no-reserved-keys`]()）

> 避免与 Vue 内置能力冲突

**<font color=red>反例</font>**

```
<script setup lang="ts">
defineOptions({
  name: 'Transition'
})
</script>
```

**正例**

```
<script setup lang="ts">
defineOptions({
  name: 'UserTransitionPanel'
})
</script>
```

#### 【推荐】 单文件组件文件名统一使用 PascalCase

**检查方式**： 工具检查(eslint: [`vue/match-component-file-name`](), [`vue/component-definition-name-casing`]()）

> **相关官方风格**：SFC 文件名统一大小写风格
> 统一组件识别方式，提高可读性

**<font color=red>反例</font>**

```js
usercard.vue
userCard.vue
```

**正例**

```js
UserCard.vue
OrderSearchForm.vue
```

#### 【推荐】 强耦合子组件必须带父组件前缀

**检查方式**：人工检查

> **相关官方风格**：Tightly coupled component names
> 让文件结构更清晰

**正例**

```js
UserList.vue
UserListItem.vue
UserListToolbar.vue
```

#### 【强制】 禁止未使用的注册组件

**检查方式**：工具检查(eslint: [`vue/no-unused-components`]()）

> 减少冗余代码，避免误导

**正例**

```js
<script>
import UserCard from './UserCard.vue'

export default {
  components: {
    UserCard
  }
}
</script>

<template>
  <UserCard />
</template>
```

#### 【推荐】组件职责单一，避免“大而全”

**检查方式**： 人工检查

> 一个组件只做一件事。
> 如果一个页面里同时包含查询、表格、弹窗、表单、上传逻辑，应该拆分。
> 建议：一个文件不能超过 500行

### Props 与组件接口

#### 【推荐】Props 必须显式定义类型

**检查方式**： 工具检查(eslint: [``vue/require-prop-types``]()）

> 每个 prop 都必须声明类型；不能只写字段名，不写类型。
> 增强组件 API 清晰度，减少错误使用

**<font color=red>反例</font>**

```js
<script setup lang="ts">
const props = defineProps({
  status: {}
})
</script>
```

**正例**

```js
<script setup lang="ts">
interface Props {
  status: 'init' | 'loading' | 'success' | 'error'
}
const props = defineProps<Props>()
</script>
```

#### 【强制】非必填 Props 必须给默认值或明确可选

**检查方式**： 工具检查(eslint: [`vue/require-default-prop`]()）

> 对于非必传 props，应明确默认值；若使用 TS 泛型写法，也应清楚标注可选性。
> 避免组件接收 `undefined` 造成行为不明确

**<font color=red>反例</font>**

```js
<script setup lang="ts">
const props = defineProps({
  pageSize: Number
})
</script>
```

**正例**

```js
<script setup lang="ts">
const props = withDefaults(defineProps<{
  pageSize?: number
}>(), {
  pageSize: 10
})
</script>
```

#### 【强制】禁止直接修改 Props

**检查方式**： 工具检查(eslint: [`vue/no-mutating-props`]()）

> 保证单向数据流，避免组件行为不可预测

**<font color=red>反例</font>**

```js
<script setup lang="ts">
const props = defineProps<{
  visible: boolean
}>()

props.visible = false
</script>
```

**正例**

```js
<script setup lang="ts">
const props = defineProps<{
  visible: boolean
}>()

const emit = defineEmits<{
  (e: 'update:visible', value: boolean): void
}>()

const close = () => {
  emit('update:visible', false)
}
</script>
```

#### 【推荐】尽可能少地使用扩展运算符

**检查方式**： 人工检查

> 扩展运算符（...）虽然方便，但过度使用可能导致以下问题：
> 性能问题：不必要的属性传递会增加渲染开销。
> 可读性降低：隐藏了组件实际依赖的 props，难以维护。
> 潜在 Bug：可能意外覆盖或传递无关属性。
> 例外情况: - 使用了变量提升的高阶组件

### 模板与样式

#### 【强制】v-for必须绑定稳定的key

**检查方式**： 工具检查(eslint: [`vue/require-v-for-key`]()）

> 保证列表渲染稳定，避免状态错乱和 diff 异常
> **<font color=red>反例</font>**

```js
<template>
  <div v-for="item in list">
    {{ item.name }}
  </div>
</template>
```

**正例**

```js
<template>
  <div v-for="item in list" :key="item.id">
    {{ item.name }}
  </div>
</template>
```

**要求**

- 禁止优先使用索引 `index` 作为 key
- 必须优先使用业务唯一标识，如 `id`、`code`

#### 【强制】禁止在同一元素上同时使用 v-if和v-for

**检查方式**： 工具检查(eslint: [`vue/no-use-v-if-with-v-for`]()）

> 应先过滤数据，再循环渲染；或者将 `v-if` 提到外层容器。
> 避免逻辑歧义和渲染错误

**<font color=red>反例</font>**

```js
<template>
  <div
    v-for="user in users"
    v-if="user.enabled"
    :key="user.id"
  >
    {{ user.name }}
  </div>
</template>
```

**正例**

```js
<template>
  <div v-if="showUsers">
    <div v-for="user in users" :key="user.id">
      {{ user.name }}
    </div>
  </div>
</template>
```

#### 【强制】 模板中禁止重复属性

**检查方式**：工具检查(eslint: [`vue/no-duplicate-attributes`]()）

> 避免覆盖和歧义

**<font color=red>反例</font>**

```js
<template>
  <input class="input" class="active" />
</template>
```

**正例**

```js
<template>
  <input :class="['input', 'active']" />
</template>
```

#### 【推荐】属性书写顺序保持一致

**检查方式**：  工具检查(eslint: [`vue/attributes-order`]()）

> 模板结构更可读

##### 推荐顺序

1. 定义类：`is`、`v-is`
2. 列表渲染：`v-for`
3. 条件判断：`v-if` / `v-else-if` / `v-else`
4. 渲染修饰：`v-show`、`v-cloak`
5. 全局感知：`id`、`ref`、`key`
6. 双向绑定：`v-model`
7. 其他属性与事件

**<font color=red>反例</font>**

```js
<BaseInput @blur="handleBlur" v-model="name" ref="inputRef" />
```

**正例**

```js
<BaseInput ref="inputRef" v-model="name" @blur="handleBlur" />
```

#### 【推荐】模板缩进统一2个空格

**检查方式**： 工具检查(eslint: [`vue/html-indent`]()）

> 减少 review 中无意义格式争论

**<font color=red>反例</font>**

```js
<template>
<div>
  <span>text</span>
</div>
</template>
```

**正例**

```js
<template>
  <div>
    <span>text</span>
  </div>
</template>
```

#### 【推荐】v-html、v-text场景下不要再写子节点内容

**检查方式**： 工具检查(eslint: [`vue/no-child-content`]()）

> 避免内容被覆盖导致误解

**<font color=red>反例</font>**

```js
<div v-html="content">
  默认内容
</div>
```

**正例**

```js
<div v-html="content" />
```

#### 【推荐】 模板中禁止写复杂表达式

**检查方式**： 人工检查

> 模板只负责展示，不要写复杂计算、三层三元表达式、长链式调用。
> 复杂逻辑应放到 `computed` 或方法中。

**<font color=red>反例</font>**

```js
{{ user && user.info && user.info.name ? user.info.name.toUpperCase() : '-' }}
```

**正例**

```js
<script setup>
const userName = computed(() => {
return user.value?.info?.name?.toUpperCase() || '-'
})
</script>

<template>
{{ userName }}
</template>
```

#### 【推荐】样式作用域明确，优先使用 scoped 或约定命名空间

**检查方式**： 人工检查

> 组件样式要避免污染全局。
> 页面级样式可局部作用域，公共主题变量统一放全局。

**<font color=red>反例</font>**

```js
<style>
  .title {
    color: red;
  }
</style>
```

**正例**

```js
<style scoped>
  .page-title {
    color: red;
  }
</style>
```

#### 【强制】禁止内联样式滥用

**检查方式**： 人工检查

**<font color=red>反例</font>**

```javascript
// bad
<div style="color: red; font-size: 16px;">标题</div>
```

**正例**

```javascript
// good
<div class="page-title">标题</div>

<style scoped>
.page-title {
  color: red;
  font-size: 16px;
}
</style>
```

### 响应式与脚本约束

#### 【强制】禁止在 computed 中写异步逻辑

**检查方式**： 工具检查(eslint: [``vue/no-async-in-computed-properties``]()）

> `computed` 应该是纯计算，不应承担异步副作用

**<font color=red>反例</font>**

```js
<script setup lang="ts">
import { computed } from 'vue'

const userInfo = computed(async () => {
  const res = await fetch('/api/user')
  return await res.json()
})
</script>
```

#### 【强制】禁止在 computed 中产生副作用

**检查方式**： 工具检查(eslint: [`vue/no-side-effects-in-computed-properties`]()）

> 保证计算属性可预测、可缓存

**<font color=red>反例</font>**

```js
<script setup lang="ts">
import { ref, computed } from 'vue'

const count = ref(0)

const doubleCount = computed(() => {
  count.value++
  return count.value * 2
})
</script>
```

**正例**

```js
<script setup lang="ts">
import { ref, computed } from 'vue'

const count = ref(0)

const doubleCount = computed(() => count.value * 2)
</script>
```

#### 【推荐】 禁止在script setup中导出export

**检查方式**： 工具检查(eslint: [`vue/no-export-in-script-setup`]()）

> 保持 `<script setup>` 语义纯净，避免错误写法

**<font color=red>反例</font>**

```
<script setup lang="ts">
export const name = 'demo'
</script>
```

#### 【强制】ref在脚本中参与运算时必须使用.value

**检查方式**： 工具检查(eslint: [`vue/no-ref-as-operand`]()）

> 避免把 ref 对象当值使用

**<font color=red>反例</font>**

```js
const count = ref(1)
const total = count + 1
```

**正例**

```js
const count = ref(1)
const total = count.value + 1
```

#### 【推荐】watch 中不要使用箭头函数绑定错误上下文

**检查方式**： 工具检查(eslint: [`vue/no-arrow-functions-in-watch`]()）

> 避免 `this` 指向异常

**<font color=red>反例</font>**

```js
export default {
  watch: {
    value: (val) => {
      console.log(this)
    }
  }
}
```

**正例**

```js
export default {
  watch: {
    value(val) {
      console.log(this)
    }
  }
}
```

#### 【强制】不要把计算属性当函数调用

**检查方式**： 工具检查(eslint: [`vue/no-use-computed-property-like-method`]()）

> 避免错误心智

**<font color=red>反例</font>**

```js
<template>
  <div>{{ fullName() }}</div>
</template>
```

**正例**

```js
<template>
  <div>{{ fullName }}</div>
</template>
```

#### 【强制】页面销毁时清理副作用

**检查方式**： 人工检查

> 定时器、事件监听、轮询、WebSocket 等必须清理，避免内存泄漏。

**正例**

```javascript
let timer = null

onMounted(() => {
  timer = setInterval(() => {
    getList()
  }, 5000)
})

onUnmounted(() => {
  clearInterval(timer)
})
```

### 工程与业务实践

#### 页面请求逻辑要统一封装，禁止到处直接写 axios

**检查方式**： 人工检查

> 接口请求统一走 `api` 层或 `service` 层，便于：
>
> * 统一拦截

> * 错误处理

> * 权限控制

> * Mock / 维护

**<font color=red>反例</font>**

```js
<script setup>
import axios from 'axios'

const getList = async () => {
const res = await axios.get('/api/user/list')
tableData.value = res.data
}
</script>
```

**正例**

```js
<script setup>
import { fetchUserList } from '@/api/user'

const getList = async () => {
const res = await fetchUserList(queryForm.value)
tableData.value = res.data
}
</script>
```

#### 【强制】 常量统一抽离，禁止魔法值散落

**检查方式**： 人工检查

> 重复出现的状态码、默认值、枚举值必须提取成常量或枚举配置。

**<font color=red>反例</font>**

```js
if (status === 1) {}
if (status === 2) {}
if (status === 3) {}
```

**正例**

```js
export const ORDER_STATUS = {
PENDING: 1,
PAID: 2,
CANCELED: 3
}

if (status === ORDER_STATUS.PAID) {}
```

#### 【强制】禁止在组件中写死接口地址、权限码、字典值

**检查方式**： 人工检查

> 这类内容要统一放配置或常量中，避免后期难维护。

**<font color=red>反例</font>**

```javascript
await request.get('/api/v1/order/list')
const canEdit = permission.includes('ORDER_EDIT_001')
```

**正例**

```javascript
import { API_ORDER_LIST, PERMISSION_ORDER_EDIT } from '@/constants'

await request.get(API_ORDER_LIST)
const canEdit = permission.includes(PERMISSION_ORDER_EDIT)
```

#### 【推荐】列表页查询条件变更后，页码重置为第一页

**检查方式**： 人工检查

> 这是典型业务规范。
> 查询条件一变，必须把 `pageNum` 重置为 1，避免查不到数据。

**<font color=red>反例</font>**

```js
const handleSearch = () => {
  getList()
}
```

**正例**

```js
const handleSearch = () => { 
  pageNum.value = 1
  getList()
}
```

#### 【推荐】 删除、提交、导出等操作必须有明确反馈

**检查方式**： 人工检查

> 用户触发关键动作时，要有：
>
> * 确认提示
> * 成功提示
> * 失败提示
> * loading / 禁用态

**<font color=red>反例</font>**

```js
const handleDelete = async (id) => {
  await deleteUser(id)
  getList()
}
```

**正例**

```js
const handleDelete = async (id) => {
  try {
    await ElMessageBox.confirm('确认删除该记录吗？', '提示')
    await deleteUser(id)
    ElMessage.success('删除成功')
    getList()
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('删除失败')
    }
  }
}
```

### A11Y

#### 【推荐】要求图片、对象、区域等非文本内容具有可替代文本。

**检查方式**： 工具检查（eslint: [`vuejs-accessibility/alt-text`]())

**<font color=red>反例</font>**

```javascript
// bad
<template>
  <img src="/logo.png" />
</template>
```

**正例**

```javascript
// good
<template>
  <img src="/logo.png" alt="公司 Logo" />
</template>
```

#### 【推荐】要求所有aria-开头的属性都有效.

**检查方式**： 工具检查（eslint: [`vuejs-accessibility/aria-props`]())

**<font color=red>反例</font>**

```javascript
// bad
<template>
  <button aria-labl="关闭">×</button>
</template>
```

**正例**

```javascript
// good
<template>
  <button aria-label="关闭">×</button>
</template>
```

#### 【推荐】要求ARIA状态和属性值有效.

**检查方式**： 工具检查（eslint: [`vuejs-accessibility/aria-proptypes`]())

**<font color=red>反例</font>**

```javascript
// Bad: the aria-hidden state is of type true/false
<template>
  <button aria-hidden="maybe">提交</button>
</template>
```

**正例**

```javascript
// Good: the aria-hidden state is of type true/false
<template>
  <button aria-hidden="true">提交</button>
</template>
```

#### 【推荐】有点击事件的可见非交互元素，应同时提供键盘事件支持

**检查方式**： 工具检查（eslint: [`vuejs-accessibility/click-events-have-key-events`]())

**<font color=red>反例</font>**

```javascript
// bad
<template>
  <div @click="submit">提交</div>
</template>
```

**正例**

```javascript
// good
<template>
  <div
    role="button"
    tabindex="0"
    @click="submit"
    @keydown.enter="submit"
    @keydown.space.prevent="submit"
  >
    提交
  </div>
</template>
```

#### 【推荐】要求 label 通过 for 正确关联表单控件

**检查方式**： 工具检查（eslint: [`vuejs-accessibility/label-has-for`]())

**<font color=red>反例</font>**

```javascript
// bad
<template>
  <label>邮箱</label>
  <input placeholder="请输入邮箱" />
</template>
```

**正例**

```javascript
// good
<template>
  <label for="email">邮箱</label>
  <input id="email" placeholder="请输入邮箱" />
</template>
```

#### 【推荐】要求 iframe 具备 title，帮助用户理解嵌入内容

**检查方式**： 工具检查（eslint: [`vuejs-accessibility/iframe-has-title`]())

**<font color=red>反例</font>**

```javascript
// bad
<template>
  <iframe src="https://example.com"></iframe>
</template>
```

**正例**

```javascript
<template>
  <iframe
    src="https://example.com"
    title="帮助中心页面"
  ></iframe>
</template>
```

#### 【推荐】禁止使用 accessKey，因为容易和浏览器/系统快捷键冲突。

**检查方式**： 工具检查（eslint: [`vuejs-accessibility/no-access-key`]())

**<font color=red>反例</font>**

```javascript
<template>
  <button accesskey="s">保存</button>
</template>
```

#### 【推荐】非交互元素不应随意设置 tabindex

**检查方式**： 工具检查（eslint: [`vuejs-accessibility/no-noninteractive-tabindex`]())

**<font color=red>反例</font>**

```javascript
<template>
  <div tabindex="0">普通说明文字</div>
</template>
```

#### 【推荐】避免只依赖 change 事件触发关键操作，因为这可能让交互时机不明确，影响可用性。

**检查方式**： 工具检查（eslint: [`vuejs-accessibility/no-onchange`]())

**<font color=red>反例</font>**

```javascript
<template>
  <select @change="submitImmediately">
    <option>选项1</option>
    <option>选项2</option>
  </select>
</template>
```

**正例**

```javascript
<template>
  <select v-model="selected">
    <option>选项1</option>
    <option>选项2</option>
  </select>
  <button @click="submit">提交</button>
</template>
```

### 安全

#### 【强制】`v-html` 安全约束：`v-html` 默认禁用，确有业务必要时走例外流程并说明来源、净化方式、允许标签范围

> 只要把不可信、未经恰当验证或转义的数据拼进 HTML/脚本上下文，就会产生 XSS 风险。
>
> 这件事为什么重要：
>
> * `{{ content }}` 默认是安全的，因为 Vue 会转义
> * `<div v-html="content" />` 则是放弃这层保护
> * 风险不只来自 `<script>` 标签
> * 还包括 `onerror`、`onclick`、`javascript:` URL、恶意样式、表单诱导等内容

**<font color=red>反例</font>**

```javascript
// bad 用户提供的html是不可信的  
<div v-html="userProvidedHtml"></div>
```

## 浩鲸科技Vue开发环境搭建指引

### 安装准备工作

在开始搭建开发环境之前，需要了解下背景，目前公司Vue指定的工具，分别是

- **<font color=red>Eslint：</font>** ESLint 是一款开源的 JavaScript 静态代码分析工具，用于检测代码中的潜在错误、风格问题和逻辑缺陷。它通过预定义或自定义的规则集，帮助开发者统一代码规范、提升可维护性。ESLint 已成为现代前端工程的标准工具
- **<font color=red>Prettier：</font>** Prettier 是一款流行的代码格式化工具，专注于强制统一代码风格，支持 JavaScript、TypeScript、HTML、CSS、JSON 等多种语言。它通过解析代码并重新输出符合预设规则的格式，彻底消除团队协作中的代码风格争议。Prettier 已成为现代工程化项目的标配工具，尤其适合强调代码一致性的团队。

### 本地配置指导

#### 添加公司eslint规则

1. 安装所需要的依赖

```sh
yarn add @whalecloud/vue-eslint-config -D
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
  extends: '@whalecloud/vue-eslint-config',
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
+   "eslint": "eslint --ext=.vue,.ts,.js ./"
  },
```

运行 `npm run eslint`进行本地单独检测。检查结果与ci代码检查结果一致

### vscode编辑器中配置

#### Vscode中安装eslint

1. 插件安装
   打开VSCode，在插件扩展商店搜索 `eslint`，点击安装，并重新加载；
   ![image](uploads/117923/126c9767-1c26-43b1-8d0b-a0f6757b62d6/image.png)
2. 插件配置
   确保 VSCode 输出面板中 ESlint  ESLint server是处于工作状态的，并且找到npm ESlint
   ![image](uploads/117923/c4d1c124-b7fe-47cd-b281-baf1b7a3ee52/image.png)

VSCode 的 ESLint 插件优先使用安装在当前项目中的 npm ESLint，如果当前项目中没有提供，它会使用全局安装的 npm ESLint。
然后看是否存在 ESLint 配置文件 `.eslintrc`，如果没有的话就不会去校验；如果存在VSCode 会根据你当前项目下的 `.eslintrc` 文件的规则来验证代码

#### Vscode中安装Prettier

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

## 研发云CI/CD检测流程搭建（Vue工程）

1. 进入研发云（https://dev.iwhalecloud.com）并登陆，点击有上角菜单——>开发中心——>持续构建，如下图：

   ![image](uploads/261071/5bac3b45-dc0a-4a52-8533-45a358fb417b/image.png)

2. 进入持续构建页面后点击新建构建，进入新建页面如下图，配置自己的`应用模块`，在语言模板处选择JS，最后选择要构建的的镜像。根据项目要求一步步创建
   ![image](uploads/261071/ebf05919-9fcf-4cba-b49d-7d7e2289d473/image.png)

   注：`Maven 私服` 环节，不使用

3. 在"代码检查"页面打开“是否需要代码分析选项”，之后一直点击`下一步`到最后一步点击`新建构建`
   ![image](uploads/261071/b1aad47c-05b3-471e-af01-1214a3516796/image.png)

4. 在`编辑构建`页面中，`代码下载`节点配置自己仓库的信息

   ![image](uploads/261071/c85f8e4d-6443-410a-a3e5-2053a0c8ac2e/image.png)

5. 在`编辑构建`页面中，添加`执行普通脚本` 配置 `build.sh`编译脚本

   ![image](uploads/261071/d8e7d7fd-18be-4ab9-8f7b-64e7bde2d3ab/image.png)

   build.sh (注：可以换成 npm 、pnpm等）

   ```sh
   #!/bin/bash
   export NODE_OPTIONS=--openssl-legacy-provider
   yarn config set registry http://npm.iwhalecloud.com:8081/repository/npm-all/
   yarn install
   npm run build
   ```

   注：只进行代码分析，可以不加此 编译节点

6. 在`编辑构建`页面中，`代码分析节点`  JS 语言类型选择`VUE`

   ![image](uploads/261071/b93ec316-5b9b-42f0-9550-1f685bded0a9/image.png)

7. 点击“高级配置”可以选择es6编译所使用的node版本号

   ![image](uploads/261071/c58abb2f-0120-4800-985c-7ca02aa612f1/image.png)

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

   ![image](uploads/261071/f775de3f-9074-400e-94ae-d62f8410055b/image.png)

## FAQ

## 本文件评审、修正记录

| 文件名称 | Vue语言编码规范 |               |               |        |
| -------- | --------------- | ------------- | ------------- | ------ |
| 序号     | 流程            | 拟制人/审核人 | 拟制/审核时间 | 版本号 |
| 1        | 编写            | 王小虎        | 2026/3/20     | V0.1   |
| 2        | 根据丁向阳的评审意见，修改二级标题命名以及分类            | 王小虎        | 2026/4/14     | V0.2   |
| 3        | 根据马进云的评审意见，修改单词拼写 以及 命令调整            | 王小虎        | 2026/4/14     | V0.3   |
| 4        | 根据王彬宇的评审意见，修改章节 单文件组件文件名统一使用 PascalCase; 修改章节：避免只依赖 change 事件触发关键操作 ; 修改章节：组件名必须为多单词 ; 增加章节 安全：`v-html` 安全约束           | 王小虎        | 2026/4/14     | V0.4   |
| 5        | 正式发布            | JavaScript规范组        | 2026/7/7     | V1.0   |
| 6        | 修改章节“2.6.5. 【推荐】要求 label 通过 for 正确关联表单控件”中的反例，规避歧义            | 王小虎        | 2026/7/15     | V1.0.1   |
| 7        | 发布            | JavaScript规范组        | 2026/7/20     | V1.1   |
