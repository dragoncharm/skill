![image](uploads/4082/fe9f3d2f-17cc-4a9b-919e-da620516afb4/image-20210818140426058.png)

# 总则

## 目的与范围

本规范源于CERT，适用于浩鲸云计算科技股份有限公司（简称浩鲸科技）所有的产品团队，用于指导C/C++开发人员的安全编码工作。

<table><tr><td bgcolor=yellow><font color=red>备注</font>：当前代码规范考试命题范围是规范标题中带有✪符号的</td></tr></table>

## 定义与分类

C/C++安全编码规范按照来源分为C安全编码规范和C++安全编码规范。

### C安全编码规范

| 类别                | 编码    | 条目                                                         |
| ------------------- | ------- | ------------------------------------------------------------ |
| 预处理器  (PRE)     | PRE31-C | <font style="background: yellow">✪ 避免不安全宏的参数出现副作用</font> |
| 声明和初始化(DCL)   | DCL30-C | <font style="background: yellow">✪ 声明具有正确存储持续期的对象</font> |
| 声明和初始化(DCL)   | DCL36-C | 不要声明具有冲突链接属性的标识符                             |
| 声明和初始化(DCL)   | DCL40-C | <font style="background: yellow">✪ 不要创建与同一个函数或对象不兼容的声明</font> |
| 表达式（EXP）       | EXP34-C | 不要对null指针进行解引用                                     |
| 表达式（EXP）       | EXP37-C | 调用函数时使用正确的参数数目和类型                           |
| 表达式（EXP）       | EXP40-C | 不要修改常量对象                                             |
| 表达式（EXP）       | EXP46-C | 不要在布尔类的操作数上使用位运算符                           |
| 整数（INT）         | INT30-C | <font style="background: yellow">✪ 保证无符号整型数操作不会出现回绕</font> |
| 整数（INT）         | INT31-C | <font style="background: yellow">✪ 保证整型转换不会丢失或错误解释数据</font> |
| 整数（INT）         | INT32-C | <font style="background: yellow">✪ 保证有符号整数的运算不会溢出</font> |
| 整数（INT）         | INT33-C | <font style="background: yellow">✪ 保证除法和取余运算不会导致除零错误</font> |
| 数组(ARR)           | ARR30-C | <font style="background: yellow">✪ 不要使用超出边界的指针或超出边界的数组下标</font> |
| 数组(ARR)           | ARR36-C | 不要将两个不同数组的指针做减法或者进行比较                   |
| 数组(ARR)           | ARR39-C | 不要向指针中添加或减去缩放的整数                             |
| 字符和字符串（STR） | STR30-C | <font style="background: yellow">✪ 不要试图修改字符串常量</font> |
| 字符和字符串（STR） | STR31-C | <font style="background: yellow">✪ 保证字符串的存储具有足够的空间容纳字符数据和null结尾符</font> |
| 字符和字符串（STR） | STR32-C | 不要将非null结尾的字符序列当做字符串传递给库函数             |
| 字符和字符串（STR） | STR34-C | 在转换为更大的整数长度时把字符转换为无符号类型               |
| 内存管理（MEM）     | MEM31-C | 释放不再需要的动态分配的内存                                 |
| 内存管理（MEM）     | MEM34-C | 只释放动态分配的内存                                         |
| 内存管理（MEM）     | MEM35-C | <font style="background: yellow">✪ 为对象分配足够的内存</font> |

### C++安全编码规范

| 分析              | 编码      | 标题                                                         |
| ----------------- | --------- | ------------------------------------------------------------ |
| 声明及初始化(DCL) | DCL54-CPP | 成对重载allocation与deallocation函数并置于相同作用域中       |
| 声明及初始化(DCL) | DCL55-CPP | <font style="background: yellow">✪ 避免跨信任边界传递类对象时发生信息泄露</font> |
| 声明及初始化(DCL) | DCL59-CPP | 不要在头文件中定义匿名的命名空间                             |
| 表达式(EXP)       | EXP50-CPP | 不要依赖求值顺序  （EXP30-C）                                |
| 表达式(EXP)       | EXP51-CPP | 不要通过不正确类型指针删除一个数组                           |
| 表达式(EXP)       | EXP52-CPP | 不要依赖不求值的操作数  （EXP44-C）                          |
| 表达式(EXP)       | EXP53-CPP | 不要读取未初始化的内存（EXP33-C）                            |
| 表达式(EXP)       | EXP54-CPP | 不要访问在其生命周期之外的对象                               |
| 表达式(EXP)       | EXP57-CPP | 不要强制转换或删除指向不完整类的指针                         |
| 表达式(EXP)       | EXP62-CPP | 不要访问对象中非对象值部分的bits （EXP42-C）                 |
| 整型(INT)         | INT50-CPP | 不要做超过枚举值范围的枚举类型转换                           |
| 内存管理(MEM)     | MEM50-CPP | 禁止访问已释放的内存（MEM30-C）                              |
| 内存管理(MEM)     | MEM52-CPP | 检测并捕捉内存分配错误                                       |
| 内存管理(MEM)     | MEM53-CPP | 手动管理对象的生命周期时，显式的构造和析构对象               |
| 面向对象编程(OOP) | OOP50-CPP | 禁止在构造函数或析构函数中调用虚函数                         |
| 面向对象编程(OOP) | OOP51-CPP | 禁止切割子类对象                                             |
| 面向对象编程(OOP) | OOP52-CPP | 禁止删除没有虚拟析构函数的多态对象                           |
| 面向对象编程(OOP) | OOP53-CPP | 规范化成员初始化列表的顺序                                   |
| 面向对象编程(OOP) | OOP58-CPP | 拷贝操作不允许修改原对象                                     |
| 杂项(MSC)         | MSC52-CPP | 带返回值的函数必须在每个路径中返回返回值                     |

# C安全编码规范

## 预处理器 (PRE)

### <font style="background: yellow">✪ PRE31-C 避免不安全宏的参数出现副作用</font>

一个不安全的函数宏会在展开时多次使用或根本不使用某个参数。绝对不要调用包含赋值、增量、减量、volatile访问、输入/输出等具有副作用（包括含有副作用的函数调用）参数的不安全宏。

若文档中涉及不安全宏的时候，应当对使用含有副作用的参数调用进行警告，但是责任根源在于程序员使用了某个不安全宏。由于在使用中会伴随风险，应避免定义不安全的函数宏。

**<font color=red>不合规代码</font>**

不安全宏的问题之一是其宏参数含有副作用，正如下面这段不合规代码示例：

```cpp
#define ABS(x) (((x) < 0) ? -(x) : (x))  
void func(int  n)   
{  
    /* Validate that n is within the desired range */  
    int  m = ABS(++n);  
    /* ... */  
}
```

上面的`ABS()`宏调用展开后如下：

```cpp
m = (((++n) < 0)? -(++n):(++n));
```

生成的代码是明确的，但会导致n递增两次而不是一次。

**合规代码**

在这个合规解决方案中，增量操作`++n`在宏调用之前得到执行。

```cpp
#define ABS(x) (((x) < 0) ? -(x) : (x))  /* UNSAFE */  
void  func(int  n)   
{  
    /* Validate that n is within the desired range */  
    ++n;  
    int  m = ABS(n);  
    /* ... */  
}
```

注意上述代码在注释中警告了程序员该宏是不安全的，该宏也可以改名为`ABS_UNSAFE()`以明确告知宏是不安全的。正如本规则的所有兼容解决方案，如果`ABS()`的参数等于最小的有符号整型值（最负值），那么这个解决方案也具有未定义的行为。

**合规代码**

本合规解决方案遵守规范**PRE00-C 以内联函数或静态函数代替类函数的宏**。不像`ABS()`宏，在对任何类型的操作数进行操作时，`iabs()`函数将截断比int类型更宽的参数，这些参数的值范围不在**int**类型的范围内。

```cpp
#include <complex.h>  
#include <math.h>  
static  inline int  iabs(int  x)  
{  
    return  (((x)   < 0) ? -(x) : (x));  
}  
void   func(int  n)  
{  
    /* Validate that n is within the desired range */  
    int  m = iabs(++n);  
    /* ... */  12.	
}  
```

**合规代码**

更具有弹性的合规解决方案是让`ABS()`宏使用`_Generic`选项。为了支持所有的数据类型，此解决方案使用内联函数来计算整数绝对值。

```cpp
#include <complex.h>
#include <math.h>

static inline long llabs(long long v) {
    return v < 0 ? -v : v;
}
static inline long labs(long v) {
    return v < 0 ? -v : v;
}
static inline int iabs(int v) {
    return v < 0 ? -v : v;
}
static inline int sabs(short v) {
    return v < 0 ? -v : v;
}
static inline int scabs(signed char v) {
    return v < 0 ? -v : v;
}
#define ABS(v) _Generic(v, signed char : scabs, \
    short : sabs, \
    int : iabs, \
    long : labs, \
    long : llabs, \
    float : fabsf, \
    double : fabs, \
    long double : fabsl, \
    double complex : cabs, \
    float complex : cabsf, \
    long double complex : cabsl)(v)
void func(int n) {
    /* Validate that n is within the desired range */
    int m = ABS(++n);
    /* ... */
}
```

## 声明和初始化(DCL)

### <font style="background: yellow">✪ DCL30-C 声明具有正确存储持续期的对象</font>

每个对象都有一个确定其生命周期的存储持续期：**static**、**thread**、**automatic**或者**allocated**。

根据C标准6.2.4章节第2段【**ISO/IEC 9899:2011**】

> *对象的生命周期就是能够保证存储持续有效的程序执行期间的部分时间，一个对象在它的生命周期内，具有一个常量地址，并且保留着最近一次所存储的值。如果对象在其生命周期之外被引用，则该行为是未定义的。当指针指向的对象生命周期结束时，指针的值变得不确定。*
>
> *访问超出生命周期之外的对象是未定义的行为，可导致产生可被利用的漏洞。*

**<font color=red>不合规代码（不同的存储持续期）</font>**

在这个不合规代码示例中，变量 `c_str` 是 **automatic** 类型存储持续时间，被赋值给 **static** 类型存储持续时间变量 `p` ，赋值本身是有效的，但是 `c_str` 在超出 `dont_do_this` 函数之外就无效了，而 `p` 还保存着它的地址。

```cpp
const char *p;
dont_do_this(void)   
{  
      const char c_str[] = "This will change";  
      p = c_str; /* Dangerous */  
}  
void  innocuous(void)   
{  
      printf("%s\n",  p);  
}  
int  main(void)   
{  
      dont_do_this();  
      innocuous();  
      return  0;  
}
```

**合规代码（相同的存储持续期）**

在这个解决方案中，`p` 被声明为和 `c_str` 一样的存储持续期，这样就防止了 `p`在 `this_is_OK` 函数之外值的不确定性。

```cpp
void  this_is_OK(void)   
{  
      const char  c_str[] = "Everything OK";  
      const char *p = c_str;  
  /* ... */  
}  
/* p is inaccessible outside the scope of string c_str */  
```

可替换方案，`p`和`c_str`都声明为**static**类型存储持续期。

**合规代码（不同的存储持续期）**

如果 `p` 必须被声明为 **static** 类型存储持续期，而 `c_str` 为受限制的存储持续期，那么可以将`p` 在 `c_str` 被销毁前设置为 `NULL`。这样可以防止 `p` 取不确定值，但是任何引用`p`的地方都需要检查 `p` 是否为空。

```cpp
const char *p;  
void  is_this_OK(void)   
{  
      const char  c_str[] = "Everything OK?";  
      p   = c_str;  
      /* ... */  
      p   = NULL;  
} 
```

**<font color=red>不合规代码（返回值）</font>**

在这个示例中，函数 `init_array()` 返回了一个指向字符数组的 **automatic** 类型存储持续期的指针。

```cpp
char *init_array(void)   
{  
      char  array[10];  
      /* Initialize array */  
      return  array;  
}  
```

当函数返回 **automatic** 类型存储持续期的指针时，一些编译器会产生一个诊断告警，程序员应当在高告警级别上编译代码，并解决所有告警。

**合规代码（返回值）**

在这个例子中，这个解决方案取决于程序员的意图。如果程序员的意图是修改 `array` 的值，并且让这个修改在 `init_array()` 函数作用域之外仍然得以保持，可以通过在其他地方声明 `array`，并把它作为参数传递给 `init_array()` 来实现这个目的。

```cpp
#include <stddef.h>  
void  init_array(char *array,  size_t  len)   
{  
      /* Initialize array */  
      return;  
}  
int  main(void)   
{  
      char  array[10];  
      init_array(array,  sizeof(array)   / sizeof(array[0]));  
      /* ... */  
      return  0;  
} 
```

**<font color=red>不合规代码（输出参数）</font>**

在这个例子中，函数 `squirrel_away()` 存储了一个指向本地变量`local`的指针，并将该指针赋值给函数入参 `ptr_param`，在 `squirrel_away()` 返回后，`ptr_param`指向的变量已经超出了生命周期。

```cpp
void  squirrel_away(char **ptr_param)   
{  
      char  local[10];  
      /* Initialize array */  
      *ptr_param   = local;  
}  
void  rodent(void)   
{  
      char *ptr;  
      squirrel_away(&ptr);  
	  /* ptr is live but invalid here */  
}
```

**合规代码（输出参数）**

在这个例子中，变量 `local` 具有 **static** 类型存储持续期，所以 `ptr` 可以在 `rodent()` 函数中引用 `local` 数组。

```cpp
char  local[10];  
void  squirrel_away(char **ptr_param)   
{  
      /* Initialize array */  
      *ptr_param   = local;  
}  
void  rodent(void)   
{  
      char *ptr;  
      squirrel_away(&ptr);  
  /* ptr is valid in this scope */  
}  
```

### DCL36-C 不要声明具有冲突链接属性的标识符

在不同的作用域声明或同一个作用域中声明多次的标识符可以通过链接属性表示同一个对象或函数。标识符的链接属性可以分为外部链接、内部链接、无链接。这三种链接属性有以下特性：

- **外部链接**：具有外部链接属性的标识符在整个程序空间（即在所有编译单元和库中）表示相同的对象或函数。标识符对链接器有效。当具有外部链接属性的相同标识符声明第二次出现时，链接器会把这个标识符与同一个对象或函数相关联。

- **内部链接**：具有内部链接属性的标识符在一个给定的翻译单元中表示同一个对象或函数。链接器没有内部链接属性标识符相关的信息，因此，这类标识符是属于翻译单元内部的。

- **无链接**：如果标识符的链接属性为无链接，则使用这个标识符的所有未来声明都是新的，如新变量或新类型。

根据**C11**标准6.2.2节，链接属性是按照下面方式确定的：

> *如果一个具有文件作用域的表示对象或函数的标识符声明中包含了存储类指示符**static**，这个标识符就具有内部链接属性。*
>
> *如果一个标识符在声明时使用了存储类型指示符 **extern**，并且在它的作用域中已经有了这个标识符的以前声明，如果以前声明指定了内部或外部链接属性，这个标识符后来的声明的链接属性就与之前声明的相同。如果作用域中没有这个标识符的以前声明，或者它以前声明的链接属性为无链接，这个标识符就具有外部链接属性。*
>
> *如果一个表示函数的标识符声明没有使用存储类型指示符 **extern**，它的链接属性就像使用了存储类型指示符 **extern** 声明的一样，如果一个表示对象的标识符具有文件作用域，并且没有存储类型指示符，它的链接属性就是外部链接。*
>
> *下面这类标识符的链接属性为无链接：被声明为不是函数或对象的标识符、被声明为函数形参的标识符、被声明为对象但没有使用存储类型指示符 **extern**的代码块作用域中的标识符。*

在一个翻译单元内部，一个标识符既具有内部链接属性又具有外部链接属性将会导致未定义的行为。 (见未定义行为8) 翻译单元包括通过预处理指令 `#include` 包含的所有头文件和源文件。

下面这个表说明了在一个翻译单元内一个对象在被第二次声明时的链接属性。列代表第一次声明，行代表重复声明。

**<font color=red>不合规代码</font>**

在这个不合规例子中，`i2` 和 `i5` 被定义为同时具有内部和外部链接属性，使用这两个标识符将会导致未定义的行为。

```cpp
int i1 = 10;         /* Definition, external linkage */  
static int i2 = 20;  /* Definition, internal linkage */  
extern int i3 = 30;  /* Definition, external linkage */  
int i4;              /* Tentative definition, external linkage */  
static int i5;       /* Tentative definition, internal linkage */  
int i1;  /* Valid tentative definition */  
int i2;  /* Undefined, linkage disagreement with previous */  
int i3;  /* Valid tentative definition */  
int i4;  /* Valid tentative definition */  
int i5;  /* Undefined, linkage disagreement with previous */  
int main(void)   
{  
  /* ... */  
  return 0;  
}
```

微软 **Visual Studio 2013** 对上述情况不会产生告警，即便是设置了最高告警级别。

**GCC** 编译器会为 `i2` 和 `i5` 定义冲突产生一个致命诊断信息。

**合规代码**

```cpp
int i1 = 10;         /* Definition, external linkage */  
static int i2 = 20;  /* Definition, internal linkage */  
extern int i3 = 30;  /* Definition, external linkage */  
int i4;              /* Tentative definition, external linkage */  
static int i5;       /* Tentative definition, internal linkage */  
int main(void)   
{  
  /* ... */  
  return 0;  
} 
```

### <font style="background: yellow">✪ DCL40-C 不要创建与同一个函数或对象不兼容的声明</font>

同一个函数或对象的两个或多个不兼容的声明不能出现在同一程序中，因为可能导致未定义的行为。在 C 标准6.2.7节中提到了两种类型可能不同但是是兼容的，这种情况可以被准确处理。

C标准确定，由于相同函数或对象的不兼容声明，可能导致四种情况未定义行为出现：

| **未定义行为** | **描述**                                                     | **示例代码**                                                 |
| -------------- | ------------------------------------------------------------ | ------------------------------------------------------------ |
| **15**         | 同一对象或函数的两个声明类型是不兼容的                       | 本指南中的所有不合规的示例代码                               |
| **31**         | 两个标识符仅在无效字符中不同                                 | 不合规代码示例（超长标识符）                                 |
| **37**         | 使用除了被允许的类型之外的其他类型获取对象数据               | 不合规代码示例（不兼容的对象声明）  不合规代码示例（不兼容的数组声明） |
| **41**         | 函数定义的类型与调用函数的表达式所指向的类型（表达式）不兼容。 | 不合规代码示例（不兼容的函数声明）  不合规代码示例（超长标识符） |

虽然出现在同一程序里两个不兼容的声明在大多数应用里可能是良性的，但是通过与函数定义类型不兼容的表达式调用，函数会产生灾难性的后果。同样，用与对象类型不兼容的类型访问对象可能导信息泄露、内存覆盖或硬件陷阱。

**<font color=red>不合规代码（不兼容的对象声明）</font>**

在这个不合规的代码示例中，变量 `i` 在文件 **a.c** 中声明为 **int** 类型，但在文件 **b.c** 中却定义为**short** 类型。这两个声明是不兼容的，会导致未定义行为15。此外，在函数 `f()` ，使用不兼容的左值类型获取对象数据，会导致未定义行为37，有可能导致信息暴露、内存覆盖或硬件陷阱。

```cpp
/* In a.c */  
extern int i;   /* UB 15 */  
int f(void) {  
  return ++i;   /* UB 37 */  
}  
/* In b.c */  
short i;   /* UB 15 */ 
```

**合规代码（不兼容的对象声明）**

```cpp
/* In a.c */  
extern int i;     
int f(void) {  
  return ++i;     
}  
/* In b.c */  
int i;  
```

**<font color=red>不合规代码（不兼容的数组声明）</font>**

在这个不合规的代码示例中，变量 `a` 在文件 **a.c** 中被声明为指针类型，但在文件 **b.c** 中却定义为数组类型。这两个声明是不兼容的，导致了未定义行为15。像之前一样，在函数 `f()`中访问对象会导致未定义行为37，有可能导致信息暴露、内存覆盖或硬件陷阱。

```cpp
/* In a.c */  
extern int *a;   /* UB 15 */  
int f(unsigned int i, int x)  
{  
  int tmp = a[i];   /* UB 37: read access */  
  a[i] = x;         /* UB 37: write access */  
  return tmp;  
}  
/* In b.c */  
int a[] = { 1, 2, 3, 4 };   /* UB 15 */  
```

**合规代码（不兼容的数组声明）**

```cpp
/* In a.c */  
extern int a[];     
int f(unsigned int i, int x)   
{  
  int tmp = a[i];     
  a[i] = x;           
  return tmp;  
}  
/* In b.c */  
int a[] = { 1, 2, 3, 4 }; 
```

**<font color=red>不合规代码（不兼容的函数声明）</font>**

在这个不合规代码示例中，函数 `f()` 在文件 **a.c** 中声明的原型与在 **b.c** 中定义的类型不一致。这两个原型是不兼容的，导致未定义行为15。此外，调用该函数是未定义行为41，通常具有灾难性的后果。

```cpp
/* In a.c */  
extern int f(int a);   /* UB 15 */  
int g(int a)   
{  
  return f(a);   /* UB 41 */  
}  
/* In b.c */  
long f(long a)   
{  
  return a * 2;   /* UB 15 */  
}
```

**合规代码（不兼容的函数声明）**

```cpp
/* In a.c */  
extern int f(int a);     
int g(int a)   
{  
  return f(a);     
}  
/* In b.c */  
int f(int a)   
{     
  return a * 2;  
}  
```

**<font color=red>不合规代码（不兼容的可变函数声明）</font>**

在这个不合规代码示例中，函数 `buginf()` 被定义为含有可变数量的参数，并期望它们都是有符号整数，并以 ­1 结尾。

```cpp
/* In a.c */  
void buginf(const char *fmt, ...)  
{  
   /* ... */  
}  
/* In b.c */  
void buginf();  
```

虽然这段代码中 `buginf()` 函数定义好像没有问题，只是函数原型声明中缺少了些信息，但按照 **C11** 标准6.7.6.3节第15段该代码会表现出未定义行为。

两个函数类型如果是兼容的，两者应指定兼容的返回类型。此外，如果两者都有参数列表，应该在参数个数和省略终止符上一致，对应参数类型应该互相兼容。

**合规代码（不兼容的可变函数声明）**

```cpp
/* In a.c */  
void buginf(const char *fmt, ...)  
{  
   /* ... */  
}  
/* In b.c */  
void buginf(const char *fmt, ...);  
```

**<font color=red>不合规代码（超长标识符）</font>**

在这个不合规代码示例中，在文件 **bashline.h** 中声明函数指针的标识符 `bash_groupname_completion_function()` 长度超过了外部标识符最长为31的限制。

这引入了与在 **b.c** 中定义的整型变量 `bash_groupname_completion_funct` 碰撞的可能性，它的长度恰好是31个字符。对于恰好满足此限制的应用，这属于[未定义行为31]。这是同一个函数的两个不兼容的声明。此外，调用该函数将导致未定义行为41，产生典型的灾难性结果。

```cpp
/* In bashline.h */  
/* UB 15, UB 31 */  
extern char * bash_groupname_completion_function(const char *, int);  
/* In a.c */  
#include "bashline.h"  
void f(const char *s, int i)
{  
  bash_groupname_completion_function(s, i);  /* UB 41 */  
}  
/* In b.c */  
int bash_groupname_completion_funct;  /* UB 15, UB 31 */ 
```

**注**：标识符 `bash_groupname_completion_function` 是从 **GNU Bash** 3.2 版本中引用的。

**合规代码（超长标识符）**

在这个合规解决方案中，在 **bashline.h** 中声明的函数指针标识符 `bash_groupname_completion()` 长度少于32个字符。因此，它不会与 `bash_groupname_completion_funct` 在任何兼容平台上产生冲突。

```cpp
/* In bashline.h */  
extern char * bash_groupname_completion(const char *, int);     
/* In a.c */  
#include "bashline.h"  
void f(const char *s, int i)  
{  
  bash_groupname_completion(s, i);    
}  
/* In b.c */  
int bash_groupname_completion_funct;  
```

## 表达式（EXP）

### EXP34-C 不要对null指针进行解引用

对 `null` 指针进行解引用是未定义行为（**undefined behavior**）。在许多平台上，解引用 `null` 指针会导致程序异常终止，但是标准中没有明确要求这一点。

见**Clever Attack Exploits Fully­Patched Linux Kernel [Goodin 2009]**。

**<font color=red>不合规代码</font>**

该不合规代码示例来自于一个真实的例子，原为部署于某种 **ARM** 手机上的 **libpng** 库漏洞版本。 **libpng** 库允许应用读取、创建和操作 PNG 图片文件。该库使用自己封装的`malloc()` 函数，当遇到长度为 0 或者其他错误时返回 `null` 指针。该代码同时也违反了**ERR33­-C** 检查和处理标准库错误。

```cpp
#include <png.h> /* From libpng */  
#include <string.h>  
void func(png_structp png_ptr, int length, const void *user_data)   
{  
  png_charp chunkdata;  
  chunkdata = (png_charp)png_malloc(png_ptr, length + 1);  
  /* ... */  
  memcpy(chunkdata, user_data, length);  
  /* ... */  
}  
```

如果 `length` 的值为 ­1，加法的得数为 0， `png_malloc()` 将返回 `null` 指针并赋值给`chunkdata` 。随后 `chunkdata` 作为 `memcpy()` 的目的参数，导致用户定义的数据覆盖地址 0 开始的内存。在 **ARM** 和 **XScale** 的架构中，0x0 地址映射到内存中并作为异常向量表，因此，解引用 0x0 不会导致程序异常终止。

**合规代码**

该例中的解决方案是确保 `png_malloc()` 返回的指针不为 `null`，同时还通过使用无符号**size_t** 来传递 `length` 参数，确保不会向 `func()` 传递负值。

```cpp
#include <png.h> /* From libpng */  
#include <string.h>  
void func(png_structp png_ptr, size_t length, const void *user_data)   
{  
  png_charp chunkdata;  
  if (length == SIZE_MAX) {  
    /* Handle error */  
  }  
  chunkdata = (png_charp)png_malloc(png_ptr, length + 1);  
  if (NULL == chunkdata) {  
    /* Handle error */  
  }  
  /* ... */  
  memcpy(chunkdata, user_data, length);  
  /* ... */  
}
```

**<font color=red>不合规代码</font>**

在该不合规代码示例中， `input_str` 被拷贝到 `c_str` 指向的动态分配内存。如果`malloc()` 失败，那 `c_str` 被赋值为`null`指针。当 `memcpy()` 解引用 `c_str` 时，程序出现未定义行为。另外，如果 `input_str` 是`null`指针，调用 `strlen()` 解引用`null`指针，也会导致未定义行为。这段代码同时还违反了**ERR33-C** 检查和处理标准库错误。

```cpp
#include <string.h>  
#include <stdlib.h>  
void f(const char *input_str)   
{  
  size_t size = strlen(input_str) + 1;  
  char *c_str = (char *)malloc(size);  
  memcpy(c_str, input_str, size);  
  /* ... */  
  free(c_str);  
  c_str = NULL;  
  /* ... */  
}
```

**合规代码**

该合规解决方案是要确保 `input_str` 和 `malloc()` 返回的指针不是 `null`：

```cpp
#include <string.h>  
#include <stdlib.h>  
void f(const char *input_str)   
{  
  size_t size;  
  char *c_str;  
  if (NULL == input_str)   
   {  
    /* Handle error */  
  }  
  size = strlen(input_str) + 1;  
  c_str = (char *)malloc(size);  
  if (NULL == c_str)   
    {  
    /* Handle error */  
  }  
  memcpy(c_str, input_str, size);  
  /* ... */  
  free(c_str);  
  c_str = NULL;  
  /* ... */  
}
```

**<font color=red>不合规代码</font>**

该不合规代码示例来自于 **drivers/net/tun.c** 的某个版本，并且对 **Linux Kernel 2.6.30** 造成了影响。

```cpp
static unsigned int tun_chr_poll(struct file *file, poll_table *wait)  
{  
  struct tun_file *tfile = file->private_data;  
  struct tun_struct *tun = __tun_get(tfile);  
  struct sock *sk = tun->sk;  
  unsigned int mask = 0;  
  if (!tun)  
    return POLLERR;  
  DBG(KERN_INFO "%s: tun_chr_poll\n", tun->dev->name);  
  poll_wait(file, &tun->socket.wait, wait);  
  if (!skb_queue_empty(&tun->readq))  
    mask |= POLLIN | POLLRDNORM;  
  if (sock_writeable(sk) ||  
     (!test_and_set_bit(SOCK_ASYNC_NOSPACE, &sk->sk_socket->flags) &&  
     sock_writeable(sk)))  
    mask |= POLLOUT | POLLWRNORM;  
  if (tun->dev->reg_state != NETREG_REGISTERED)  
    mask = POLLERR;  
  tun_put(tun);  
  return mask;  
} 
```

指针 `sk` 在检查 `tun` 是否为空之前就被初始化为 `tun->sk` 。由于解引用 `null` 指针是未定义行为，编译器（在该场景下为 **GCC**）可能在优化中去掉 `if (!tun)` 检查，因为它在 `tun->sk` 之后才执行，这也就意味着 `tun` 是非空的。因此，这段代码示例容易遭到`null`指针解引用攻击，因为在多个平台上可能允许 `null` 解引用，例如在 **Linux** 和 **Mac OS X** 上使用带有 `MAP_FIXED` 标志的 `mmap(2)` ，或者使用带有 `SHM_RND` 标志的 `_shmat()` **POSIX**函数。

**合规代码**

将 `sk` 的初始化放在 `null` 指针检查之后。

```cpp
static unsigned int tun_chr_poll(struct file *file, poll_table *wait)    
{  
  struct tun_file *tfile = file->private_data;  
  struct tun_struct *tun = __tun_get(tfile);  
  struct sock *sk;  
  unsigned int mask = 0;  
  if (!tun)  
    return POLLERR;  
  sk = tun->sk;  
  /* The remaining code is omitted because it is unchanged... */ 
} 
```

### EXP37-C 调用函数时使用正确的参数数目和类型

不要用错误的参数数目或类型来调用函数。

C 语言标准确定了 5 种不同情况，在这 5 种情况中，调用函数声明与其定义不符、提供参数类型或者数量错误可能造成未定义行为（**undefined behavior**，**UB**）：

| **未定义行为** | **描述**                                                     |
| -------------- | ------------------------------------------------------------ |
| **26**         | 使用指针调用类型与指针引用类型不兼容的函数                   |
| **38**         | 调用函数时没有使用作用域中的原型，实参数量不等于形参数量     |
| **39**         | 调用函数时，没有使用定义函数原型的作用域中的函数原型，原型以括号结束或者提升之后的实参类型与形参类型不兼容 |
| **40**         | 调用函数时，没有使用函数未定义原型的作用域中的函数原型，提升后的实参类型与提升后的形参类型不兼容，有某些例外情况 |
| **41**         | 函数定义类型与表示被调用函数的表达式指向的（表达式）类型不兼容 |

正常声明的函数如果得到错误数量或者类型的参数，通常会产生一条编译程序诊断消息。然而，有些情况下向函数提供不正确的参数最多只会产生编译程序警告。尽管这些警告应该得到解决，但是它们不会阻止程序编译。（参见 **MSC00­-C. Compile cleanly at high warninglevels**）

**<font color=red>不合规代码</font>**

`<tgmath.h>` 头文件为数学函数提供泛型宏。尽管头文件 `<math.h>` 中的大部分函数在 <complex.h> 中有等价的复数版本，但是仍有部分函数没有。使用复数来调用下表中的泛型函数就是未定义行为。

**Functions That Should Not Be Called with Complex Values**

| **atan2()**   | **erf()**   | **fdim()**  | **fmin()**  | **ilogb()**  | **llround()** | **logb()**      | **nextafter()**  | **rint()**    | **tgamma()** |
| ------------- | ----------- | ----------- | ----------- | ------------ | ------------- | --------------- | ---------------- | ------------- | ------------ |
| **cbrt()**    | **erfc()**  | **floor()** | **fmod()**  | **ldexp()**  | **log10()**   | **lrint()**     | **nexttoward()** | **round()**   | **trunc()**  |
| **ceil()**    | **exp2()**  | **fma()**   | **frexp()** | **lgamma()** | **log1p()**   | **lround()**    | **remainder()**  | **scalbn()**  |              |
| **copysgn()** | **expm1()** | **fmax()**  | **hypot()** | **llrint()** | **log2()**    | **nearbyint()** | **remquo()**     | **scalbln()** |              |

该示例中试图用 `log2()` 函数对复数进行计算，导致了未定义行为：

```cpp
#include <tgmath.h>  
void func(void)   
{  
  double complex c = 2.0 + 4.0 * I;  
  double complex result = log2(c);  
}  
```

**合规代码**

如果函数 `clog2()` 不能扩展到复数，程序员可以使用 `log()` 来代替 `log2()` 实现对复数求对数，因为 `log()` 可以使用复数作为参数，例如下面的代码：

```cpp
#include <tgmath.h>  
void func(void)   
{  
  double complex c = 2.0 + 4.0 * I;  
  double complex result = log(c)/log(2);  
}
```

**合规代码（Real Number）**

如果程序员的意图是对复数的实数部分求以 2 为底的对数，可以使用下面的方案：

```cpp
#include <tgmath.h>  
void func(void)   
{  
  double complex c = 2.0 + 4.0 * I;  
  double complex result = log2(creal(c));  
} 
```

**<font color=red>不合规代码</font>**

在该不合格示例中，通过函数指针 `fp` 来调用 C 语言标准库函数 `strchr()` ，但是 `fp` 声明的原型中参数类型不正确。根据 C 标准 6.3.2.3 第 8 段 [**ISO/IEC 9899:2011**]：

> *指向某个类型的函数的指针可能转换为指向另一个类型函数的指针，然后复原，其结果应该与原始指针相同。如果转换后的指针用来调用与引用类型不符的函数，其行为就是未定义的。*

见未定义行为26（**undefined behavior 26**）。

```cpp
#include <stdio.h>  
#include <string.h>  
char *(*fp)();  
int main(void)   
{  
  const char *c;  
  fp = strchr;  
  c = fp('e', "Hello");  
  printf("%s\n", c);  
  return 0;  
}
```

**合规代码**

在该合规解决方案中，函数指针 `fp` 指向 C 语言标准库函数 `strchr()` ，声明了正确的参数，并且用正确数量和类型的实际参数调用：

```cpp
#include <stdio.h>  
#include <string.h>  
char *(*fp)(const char *, int);  
int main(void)   
{  
  const char *c;  
  fp = strchr;  
  c = fp("Hello",'e');  
  printf("%s\n", c);  
  return 0;  
}
```

**<font color=red>不合规代码</font>**

在该示例中，函数 `f()` 定义为使用 **long** 类型的参数，但是在另一文件中调用 `f()` 时使用了 **int** 类型的参数：

```cpp
/* In another source file */  
long f(long x)   
{  
  return x < 0 ? -x : x;  
}  
/* In this source file, no f prototype in scope */  
long f();  
long g(int x)   
{  
  return f(x);  
}
```

**合规代码**

在该合规解决方案中，函数 `f()` 的原型包含在被调用的作用域的源文件中，而且用 **long**类型的参数正确调用函数：

```cpp
/* In another source file */  
long f(long x) {  
  return x < 0 ? -x : x;  
}  
/* f prototype in scope in this source file */  
long f(long x);  
long g(int x) {  
  return f((long)x);  
}
```

**<font color=red>不合规代码（POSIX）</font>**

**POSIX** 函数 `open()`  [**IEEE Std 1003.1:2013**]是可变参数函数，原型如下：

```cpp
int open(const char *path, int oflag, ... );
```

`open()` 函数接受的第三个参数，用来确定新创建文件的访问模式。如果 `open()` 用于创建新文件，且第三个参数被忽略，则创建的文件可能具有意外的访问权限。（参见 **FIO06­-C. Create files with appropriate access permissions**）该示例来自 **CVE­-2006-­1174** **shadow­utils** 包的 `useradd()` 函数中的一个漏洞， `open()` 的第三个参数被意外地忽略了：

```cpp
fd = open(ms, O_CREAT | O_EXCL | O_WRONLY | O_TRUNC);  
```

**注意**：从技术上说，在不创建新文件时（也就是不设置 `O_CREAT` 标志），向 `open()` 传递第三个参数是不正确的。

**合规代码（POSIX）**

在该解决方案中，调 `open()` 时指定第三个参数：

```cpp
#include <fcntl.h>  
void func(const char *ms, mode_t perms)   
{  
  /* ... */  
  int fd;  
  fd = open(ms, O_CREAT | O_EXCL | O_WRONLY | O_TRUNC, perms);  
  if (fd == -1) {  
    /* Handle error */  
  }  
} 
```

### EXP40-C 不要修改常量对象

C 标准 6.7.3 第 6 段[**ISO/IEC 9899:2011**]，规定：

> *如果试图通过非 `const`* *限定的左值来修改 `const`* *限定的对象，其行为就是未定义的。*

见未定义行为64（**undefined behavior 64**）。

有些编译器允许修改 `const` 限定的对象，而不会产生告警。

要避免转换掉 `const` 限定符，因为这会导致修改 `const` 限定的对象而不产生诊断告警。（更多细节见 **EXP05­-C. Do not cast away a const qualification**，以及 **STR30­-C. Do not attemptto modify string literals** ）

**<font color=red>不合规代码</font>**

该不合规代码示例允许修改常量对象：

```cpp
const int **ipp;  
int *ip;  
const int i = 42;  
void func(void)   
{  
  ipp = &ip; /* Constraint violation */  
  *ipp = &i; /* Valid */  
  *ip = 0;   /* Modifies constant i (was 42) */  
}
```

第一条赋值语句是不安全的，因为它允许后续的代码尝试修改常量对象 `i` 的值。

如果 `ipp` ， `ip` 和 `i` 声明为自动变量，该例在 **Microsoft Visual Studio 2013** 环境下以 C 模式编译不产生告警，且程序结果是修改了 `i` 的值。**GCC 4.8.1** 编译时产生了告警，但程序结果还是修改了 `i` 的值。

如果 `ipp` ， `ip` 和 `i` 声明为静态存储变量，该程序在 **Microsoft Visual Studio 2013** 环境中不会产生告警并异常终止，在 **GCC 4.8.1** 中编译产生告警并异常终止。

**合规代码**

合规解决方案取决于程序员的意图。如果认为 `i` 是可修改的，则解决方案是不应把 `i` 声明为常量：

```cpp
int **ipp;  
int *ip;  
int i = 42;  
void func(void) {  
  ipp = &ip; /* Valid */  
  *ipp = &i; /* Valid */  
  *ip = 0; /* Valid */  
}
```

如果认为`i`不能被修改，则就不应该编写试图修改 `i` 的代码。

### EXP46-C 不要在布尔类的操作数上使用位运算符

在一个完整表达式中混用位运算符和关系运算符，可能是表达式逻辑错误的标志，其中逻辑运算符通常是有意的运算符。不要在 `_Bool` 类型，或者关系表达式、相等表达式的结果上使用位运算符**AND**（`&`），**OR**（`|`），或**XOR**（`^`）。如果位运算符是有意的，就应该用括号来表示出来。

**<font color=red>不合规代码</font>**

在该示例中，在相等表达式的结果上使用位运算符 `&` ：

```cpp
if (!(getuid() & geteuid() == 0))   
{  
  /* ... */  
}   
```

**合规代码**

该解决方案在条件表达式中使用 `&&` 运算符来进行逻辑操作：

```cpp
if (!(getuid() && geteuid() == 0))   
{  
  /* ... */  
}
```

## 整数（INT）

### <font style="background: yellow">✪ INT30-C 保证无符号整型数操作不会出现回绕</font>

根据 C 语言标准 6.2.5 节第 9 段 **ISO/IEC 9899:2011** 所述：

> *涉及无符号整数的计算不会溢出，因为无法由最终的无符号整数类型表示的结果将会根据这种最终类型可以表示的最大值加1执行求模操作。*

以上行为更为正式的名称是无符号整数回绕（**unsigned interger wrapping**）。如果结果值无法由整数的底层表示形式表示，就会产生回绕。下表中给出了哪些操作符可能会产生回绕。

| **Operator** | **Wrap** | **Operator** | **Wrap** | **Operator** | **Wrap** | **Operator** | **Wrap** |
| ------------ | -------- | ------------ | -------- | ------------ | -------- | ------------ | -------- |
| +            | Yes      | ­-=           | Yes      | <<           | Yes      | <            | No       |
| -            | Yes      | *=           | Yes      | >>           | No       | >            | No       |
| *            | Yes      | /=           | No       | &            | No       | >=           | No       |
| /            | No       | %=           | No       | \|           | No       | <=           | No       |
| %            | No       | <<=          | Yes      | ^            | No       | ==           | No       |
| ++           | Yes      | >>=          | No       | ~            | No       | !=           | No       |
| --           | Yes      | &=           | No       | !            | No       | &&           | No       |
| =            | No       | \|    =      | No       | unary +      | No       | \|\|         | No       |
| +=           | Yes      | ^=           | No       | unary ­       | Yes      | ?:           | No       |

下面各节讨论了可能会产生无符号整数回绕的特定操作。对小整数类型（小于 **int** ）进行操作时，会发生整型提升。另外，在执行运算之前，也可能会发生算术转换，即将操作数（隐式的）转换为相同的类型。因此，在实现安全的算术运算之前，要确保理解整数转换规则（参见 **INT02­-C. Understand integer conversion rules**）。

以下列方式使用整数时，尤其不应该出现整数回绕的情况：

- 在任何指针运算中，包括作为数组索引

- 用于声明变长数组时

- 通过自增或自减运算得到数组起始地址，或用于指定数组下标的表达式

- 作为 **size_t** 或 **rsize_t** 类型的实参（比如内存分配函数的参数）

- 在安全关键的代码中

C语言标准对于原子整数类型的算术运算，定义了与普通整数类型同样的表示方式。因此，对于原子整数类型，也应该如同普通整数类型一样对回绕的情况进行检查和预防。

#### 加法

加法是在两个算术类型的操作数之间或一个指向对象的指针和一个整数类型之间执行的。本规则只应用于两个算术类型相加的情况（指针加法的规则参见 **ARR37­C. Do not add orsubtract an integer to a pointer to a non­array object** 及 **ARR30­-C. Do not form or use out­of­bounds pointers or array subscripts**）。

此外，自增运算等同于加 1 运算。

**<font color=red>不合规代码</font>**

在以下的不合规代码示例中，无符号的算子 `ui_a` 和 `ui_b` 相加时可能会产生无符号整型回绕。如果回绕行为是非预期的（**unexpected**），那么就可能会导致诸如分配了不足额的内存供后续操作使用，或易受攻击的安全漏洞（**vulnerability**）。

```cpp
void func(unsigned int ui_a, unsigned int ui_b)   
{  
    unsigned int usum = ui_a + ui_b;  
    /* ... */   
}
```

**合规代码**

这种， `void func(unsigned int ui_a)` 方案对参与相加的操作数进行了前置条件测试，以保证不会出现回绕。

```cpp
#include <limits.h>  
void  func(unsigned int  ui_a,  unsigned int  ui_b)  
{  
    unsigned int  usum;  
    if (UINT_MAX - ui_a < ui_b)   
    {  
        /* Handle error */  
    }   
    else   
    {  
        usum = ui_a + ui_b;  
    }  
    /* ... */  
}
```

**合规代码（后置条件测试）**

这种方案对相加运算进行了后置条件测试，如果相加后得到的 `usum` 不小于第一个操作数，则说明没有发生回绕。

```cpp
void  func(unsigned int  ui_a,  unsigned int  ui_b)   
{  
    unsigned int  usum = ui_a   + ui_b;  
    if (usum < ui_a)   
    {  
           /* Handle error */  
    }  
        /* ... */  
} 
```

#### 减法

减法是在两个算术类型的操作数之间，两个指向兼容对象类型的限定或未限定版本的指针之间，或一个指向一种对象类型的指针与一个整数类型的值之间执行的。本规则只应用于两个算术类型的操作数之间的减法（关于指针运算参见 **ARR36­-C. Do not subtract or compare two pointers that do not refer to the same array**，**ARR37­-C. Do not add or subtract an integer to a pointer to a non­array object** 及 **ARR30­-C. Do not form or use out­of­bounds pointers or array subscripts**）。

此外，自减运算等同于减 1 运算。

**<font color=red>不合规代码</font>**

在以下的不合规代码示例中，无符号的算子 `ui_a` 和 `ui_b` 相减时可能会产生无符号整数回绕。如果回绕行为是非预期的，那么就可能导致易受攻击的安全漏洞。

```cpp
void func(unsigned int ui_a, unsigned int ui_b)   
{  
    unsigned int udiff = ui_a - ui_b;  
    /* ... */   
} 
```

**合规代码**

这种方案对参与相减的操作数进行了前置条件测试，以保证不会出现回绕。

```cpp
#include <limits.h>  
void  func(unsigned int  ui_a,  unsigned int  ui_b)  
{  
    unsigned int  udiff;  
    if (ui_a < ui_b)   
    {  
        /* Handle error */  
    }   
    else   
    {  
         udiff = ui_a - ui_b;  
    }  
    /* ... */  
}   
```

**合规代码（后置条件测试）**

这种方案对减法运算进行了后置条件测试，如果相减的结果 `udiff` 不大于被减数，则说明没有发生回绕。

```cpp
void  func(unsigned int  ui_a,  unsigned int  ui_b)   
{  
     unsigned int udiff = ui_a - ui_b; 
    if (udiff > ui_a)   
    {  
         /* Handle error */  
    }  
        /* ... */  
}
```

#### 乘法

乘法是在两个算术类型的操作数之间执行的。

**<font color=red>不合规代码</font>**

在 **Mozilla Scalable Vector Graphics (SVG)** 的查看程序中曾经存在一个堆缓冲区溢出的漏洞，这是由于 **signed int** 类型的值 `pen­>num_vertices` 与 **size_t** 类型的值 `sizeof(cairo_pen_vertex_t)` 相乘造成的**VU551436**]。在进行乘法运算之前， **signed int** 类型的操作数首先会被转换成无符号的 **size_t** 类型（参见 **INT02­-C. Understand integer conversion rules**）。

```cpp
pen->vertices = malloc( pen->num_vertices * sizeof(cairo_pen_vertex_t) );  
```

无符号整数回绕可能会导致分配到的内存不足。

**合规代码（后置条件测试）**

合规解决方案是测试乘法的操作数，以保证不会出现回绕。

```cpp
if (pen->num_vertices > SIZE_MAX / sizeof(cairo_pen_vertex_t))   
{  
    /* Handle error */  
}  
pen->vertices = malloc( pen->num_vertices * sizeof(cairo_pen_vertex_t) );
```

#### 例外

**INT30-­C­-EX1**：在符合程序执行的需要时，无符号整数也可以表现出取模（回绕）行为。建议对于支持取模行为的整数，在声明变量以及对它的每一次操作时，都使用注释明确说明。

**INT30-­C-­EX2**：当在编译期就能够确定不会发生回绕行为时，那么就可以省略掉对回绕的检查。比如以下对无符号整数的运算操作就可以免去回绕检查：

- 两个编译期常量之间的运算

- 变量与 0 之间的运算（除了除 0 或对 0 取余的运算之外）

- 减法运算中，以减数的类型的最大值作为被减数时；比如，从 `UINT_MAX` 减去任意的**unsigned int** 类型的数都是安全的

- 任何变量与 1 相乘

- 因子非 0 时的除法和取余运算

- 向右移位的位数不超过被操作的整数的精度时；比如对于 `UNIT_MAX >> x` 操作，只要 `x` 满足 `0 <= x < 32` 就是安全的（假设 **unsigned int** 类型的精度是 32 位）。

**INT30­-C-­EX3**： 两个整数之间的向左移位操作。对无符号整数的左移操作 `<<` 可以有取模（回绕）行为。之所以允许这种例外，是因为通常情况下这是程序员本身所期望的，并且移位操作也有明确的规范定义（参见 **INT34­-C** 不要将表达式移动负数位或移动大于等于操作数中存在的位数）。

### <font style="background: yellow">✪ INT31-C 保证整型转换不会丢失或错误解释数据</font>

整型转换（包括隐式转换和显示转换）必须保证不会丢失或错误解释数据。对于来自不信任来源并且按以下方式使用的数据，这一点尤其重要：

- 在任何指针运算中，包括作为数组索引

- 用于声明变长数组时

- 通过自增或自减运算得到数组起始地址，或用于指定数组下标的表达式

- 作为 **size_t** 或 **rsize_t** 类型的实参（比如内存分配函数的参数）

本规则也被应用于传递给以下标准库函数的参数，这些参数会被转换为 **unsigend char** 类型：

- `memset()`

- `memset_s()`

- `fprintf()` 及类似函数 (对于格式化修饰符 %c  ，在不与修饰符 %l 组合使用时，整数参数会被转换为一个 **unsigned char** 类型的值，并且作为一个字符写入目标流中）

- `fputc()`

- `ungetc()`

- `memchr()`

此外，传递给以下库函数的参数会被转换为 **char** 类型:

- `strchr()`

- `strrchr()`

- `<ctype.h>` 中列举的所有函数

对于所有的数据值以及所有遵循标准的编译器，唯一能保证安全的整数类型转换是将一个整数值转换为一种具有相同符号的更宽的类型。C语言标准 6.3.1.3 **ISO/IEC 9899:2011** 表示：

> *当一个整数类型的值被转换为除 _Bool* *以外的另一种整数类型时，如果这个值能够用新类型表示，它就不会被修改。*
>
> *否则，如果新类型是无符号的，这个值就反复加上或减去**这种新类型可以表示的最大值加 1**，直到这个值位于新类型的范围之内。*
>
> *否则，这种新类型是有符号的并且这个值无法被新类型表示，此时它的结果是由编译器定义的，或者产生一个基于编译器实现的信号。*

一般情况下，将一个整数类型转换为一个更小的类型会导致高位被截断。

**<font color=red>不合规代码（无符号转为有符号）</font>**

从一种无符号类型的转换为一种有符号类型时，可能会发生类型范围错误，包括数据丢失（截断）和符号位丢失（符号错误）。下面的不合规代码在大多数的编译器中都会产生一个截断错误：

```cpp
#include <limits.h> 
void func(void)  
{  
    unsigned long int u_a = ULONG_MAX;  
    signed char sc;  
    sc = (signed char)u_a; /* Cast eliminates warning */  
    /* ... */  
} 
```

**合规代码（无符号转为有符号）**

从一种无符号类型转换为一种有符号类型时对范围进行验证。例如以下的代码可以用于从**unsigned long int** 类型转换为 **signed char** 类型：

```cpp
#include <limits.h>  
void func(void)   
{  
    unsigned long int u_a = ULONG_MAX;  
    signed char sc;  
    if (u_a <= SCHAR_MAX)   
    {  
        sc = (signed char)u_a; /* Cast eliminates warning */  
    }  
    else   
    {  
        /* Handle error */  
    }  
}  
```

**<font color=red>不合规代码（有符号转为无符号）</font>**

从一种有符号类型的转换为一种无符号类型时，可能会发生类型范围错误，包括数据丢失（截断）和符号位丢失（符号错误）。下面的不合规代码会导致符号位丢失：

```cpp
#include <limits.h>  
void func(void)   
{  
    signed int si = INT_MIN; /* Cast eliminates warning */  
    unsigned int ui = (unsigned int)si;  
    /* ... */  
}
```

**合规代码（有符号转为无符号）**

从一种有符号类型转换为一种无符号类型时对范围进行验证。例如以下的代码可以用于从**signed int** 类型转换为 **unsigned char** 类型：

```cpp
#include <limits.h>  
void  func(void)   
{  
    signed int  si = INT_MIN;  
    unsigned int  ui;  
    if (si < 0)   
    {  
        /* Handle error */  
    }   
    else   
    {  
        ui = (unsigned int)si; /* Cast eliminates warning */  
    }  
    /* ... */  
}
```

根据C语言标准 **ISO/IEC 9899:2011** 6.2.5 第 9 段的条款，遵循标准的编译器实现（**conforming implementation**）能够保证以上的方案有效。

> *有符号整数类型的非负值的范围是相应的无符号整数类型的子范围，并且两种类型中相同值的表示是相同的。*

**<font color=red>不合规代码（有符号数转换，精度损失）</font>**

从一种有符号整数类型转换为另一种精度更小的有符号类型时，可能会发生数据损失（截断）。以下的不合规代码在大多数编译器上都会发生数据截断错误：

```cpp
#include <limits.h>  
void func(void)   
{  
    signed long int s_a = LONG_MAX;  
    signed char sc = (signed char)s_a; /* Cast eliminates warning */  
    /* ... */  
}
```

**合规代码（有符号数转换，精度损失）**

从一种有符号类型转换为一种精度更小的有符号类型时，对范围进行验证。例如以下的代码可以用于从 **signed long int** 类型转换为 **signed char** 类型：

```cpp
#include <limits.h>  
void  func(void)   
{  
    signed long int  s_a = LONG_MAX;  
    signed char  sc;  
    if (s_a < SCHAR_MIN || s_a > SCHAR_MAX)   
    {  
        /* Handle error */  
    }   
    else   
    {  
        sc = (signed char)s_a; /* Cast eliminates warning */  
    }  
     /* ... */  
} 
```

从有符号整数类型转换为精度更小的另一种有符号类型时，上边界和下边界需要检查。

**<font color=red>不合规代码（无符号数转换，精度损失）</font>**

从一种无符号整数类型转换为另一种精度更小的无符号类型时，可能会发生数据损失（截断）。以下的不合规代码在大多数编译器上都会发生数据截断错误：

```cpp
#include <limits.h>  
void func(void)   
{  
    unsigned long int u_a = ULONG_MAX;  
    unsigned char uc = (unsigned char)u_a; /* Cast eliminates warning */  
    /* ... */  
} 
```

**合规代码（有符号数转换，精度损失）**

从一种无符号类型转换为一种精度更小的无符号类型时，对范围进行验证。例如以下的代码可以用于从 **unsigned long int** 类型转换为 **unsigned char** 类型：

```cpp
#include <limits.h>  
void  func(void)   
{  
    unsigned long int  u_a = ULONG_MAX;  
    unsigned char  uc;  
    if (u_a > UCHAR_MAX)   
    {  
        /* Handle error */  
    }   
    else   
    {  
        uc = (unsigned char)u_a; /* Cast eliminates warning */  
    }  
     /* ... */  
}    
```

从无符号整数类型转换为精度更小的另一种无符号类型时，只有上边界需要检查。

**<font color=red>不合规代码（time_t 类型作为返回值）</font>**

`time()` 函数在表示当前日历时间无效时，会将-1 转换为 **time_t** 类型后的值（即 `(time_t)(-1)` ）返回。C 语言标准只要求 **time_t** 类型是一个能够表示时间的实数类型（整数和实数浮点数类型统称为实数类型）。具体采用哪种实数类型表示时间，交由编译器实现来决定。如果 **time_t** 被实现为一个精度小于 **signed int** 的无符号整数类型，那么 `time()` 的返回值将永远不会与整型字面常量 -1 相等。

```cpp
#include <time.h>  
void func(void)   
{  
    time_t now = time(NULL);  
    if (now != -1)   
       {  
        /* Continue processing */  
    }  
}
```

**合规代码（time_t** **类型作为返回值）**

为了确保比较正确执行， `time()` 的返回值应该与 -1 被转换成 **time_t** 类型以后的值比较：

```cpp
#include <time.h>  
void func(void)   
{  
    time_t now = time(NULL);  
    if (now != (time_t)-1)   
    {  
        /* Continue processing */  
    }  
}  
```

这个解决方案同样也符合 **INT18­-C. Evaluate integer expressions in a larger size before comparing or assigning to that size** 的规定。

**<font color=red>不合规代码（memset()）</font>**

因为历史原因，某些 C 标准库函数可以接受一个 **int** 类型的参数并将其转换为 **unsigned char** 类型或普通的 **char** 类型。如果参数的值无法被更小的类型表示，这种转换可能会导致非预期的行为。以下的不合规代码会将数组置为全 0,这显然是不符合预期的：

```cpp
#include <string.h>  
#include <stddef.h>  
int *init_memory(int *array, size_t n)   
{  
    return memset(array, 4096, n);  
}  
```

**合规代码（memset()）**

一般来说， `memeset()` 函数不应该用于初始化整数数组，除非是希望将整个数组置 0:

```cpp
#include <string.h>  
#include <stddef.h>  
int *init_memory(int *array, size_t n)   
{  
    return memset(array, 0, n);  
} 
```

**例外：**

**INT31-C-EX1**: C 语言标准定义了标准整数类型的最小范围。例如， **unsigned short int** 类型对象的最小范围是 0 ~ 65,535，而 int 类型的最小范围是 ­32,767 ~ +32,767。这意味着 **unsigned short int** 类型的值并不都能够用 **int** 来表示。但是，在 **IA-­32** 架构中，实际的整数范围是 −2,147,483,648 ~ +2,147,483,647 ，这意味着在这种架构下所有的 **unsigned short in**t 值都可以用 **int** 类型来表示。因此，在 **IA-­32** 架构下对这种转换进行测试就是不必要的。而在不知道底层类型的精度的情况下，无法对转换行为作出假设。如果未提供对转换的测试，就必须明确记录与精度有关的假设。在这些假设无效的系统中，这些代码就无法安全的移植。记录这些假设的一种较好的方式是使用静态断言（参见**DCL03­-C. Use a static assertion to test the value of a constant expression**）。

**INT31-­C-­EX2**: 只要值表示一个字符，而不是一个整数，允许从任何整数类型转换为值为 `SCHAR_MIN` 和 `UCHAR_MAX` 之间的字符类型。

转换为无符号字符类型由 C 定义为模块化行为。字符的值不会由于符号的丢失或转换为负数而被曲解。例如，欧元符号 € 有时由位模式 0x80 表示，根据类型的符号性，其可以具有数值 128 或 -127 。

转换为有符号字符类型更容易出现问题。C 标准 6.3.1.3 第 3 段（**ISO/IEC 9899:2011**）的条款表示，关于有符号类型转换：

> *否则，这种新类型是有符号的并且这个值无法被新类型表示，此时它的结果是由编译器定义的，或者产生一个基于编译器实现的信号。*

此外，6.2.6.2 第 2 段的条款表示，关于此时的整型变换：

> *如果符号位是 1，这个值应该按以下的方式之一进行变换：*
>
> - *符号位 0* *表示负值（原码）*
> - *符号位的值为* *­(2M)（补码）*
> - *符号位的值为* *­(2M* *­ 1)* *（反码）*
>
> *以上情况中，当符号位为 1* *而其它位为 0* *时（对于前两种情况），或者当符号位和其它位都为 1* *时（对于反码的情况），由编译器实现来决定属于正常值还是异常表示。*
>
> *因此，标准允许以下代码陷入系统中断：*

```cpp
int i = 128; /* 1000 0000 in binary */ 
assert(SCHAR_MAX == 127);  
signed char c = i; /* can trap */  
```

但是，会将这段代码处理为异常或者产生一个无法预料的值的平台是很少见的。根据 **DerkJones** 在 **The New C Standard: An Economic and Cultural Commentary** 中所述：

> *具有这种处理方式的实现过去被认为是存在的，但是无法找到任何描述这类处理器的文档。*

### <font style="background: yellow">✪ INT32-C 保证有符号整数的运算不会溢出</font>

有符号整数的溢出是一种未定义行为，这意味着编译器在处理有符号整数的溢出时有多种选择（参见 **MSC15-­C. Do not depend on undefined behavior**）。例如，将有符号整数类型定义为具有取模行为的编译器就不需要检查整数溢出。编译器也可以捕捉有符号算术溢出，或者简单的假设溢出永远不会发生，并相应的生成代码。同一个遵循标准的编译器在不同的场景下生成具有不同行为的代码，也同样是可能的。例如，一个编译器可能判定在局部范围声明的有符号整型的循环控制变量不可能溢出，并基于这一点来生成有效的代码；而同一个编译器也可能判定在类似场景下使用的全局变量将会捕捉到异常。

基于这些理由，保证有符号整型运算不会导致溢出是非常重要的。尤其是来自于不信任源（**tainted source**）的数据按照以下方式被使用时：

- 在任何指针运算中，包括作为数组索引

- 用于声明变长数组时

- 通过自增或自减运算得到数组起始地址，或用于指定数组下标的表达式

- 作为 **size_t** 或 **rsize_t** 类型的实参（比如内存分配函数的参数）

如果结果值无法由整数的底层表示形式表示，整数运算就会发生溢出。下表中给出了哪些操作符可能会产生溢出。

| **Operator** | **Wrap** | **Operator** | **Wrap** | **Operator** | **Wrap** | **Operator** | **Wrap** |
| ------------ | -------- | ------------ | -------- | ------------ | -------- | ------------ | -------- |
| +            | Yes      | ­-=           | Yes      | <<           | Yes      | <            | No       |
| -            | Yes      | *=           | Yes      | >>           | No       | >            | No       |
| *            | Yes      | /=           | Yes      | &            | No       | >=           | No       |
| /            | Yes      | %=           | Yes      | \|           | No       | <=           | No       |
| %            | Yes      | <<=          | Yes      | ^            | No       | ==           | No       |
| ++           | Yes      | >>=          | No       | ~            | No       | !=           | No       |
| --           | Yes      | &=           | No       | !            | No       | &&           | No       |
| =            | No       | \|=          | No       | unary +      | No       | \|\|         | No       |
| +=           | Yes      | ^=           | No       | unary ­       | Yes      | ?:           | No       |

下面各节讨论了可能会产生有符号整数溢出的特定操作。对小整数类型（小于 **int** ）进行操作时，会发生整型提升。另外，在执行运算之前，也可能会发生算术转换，即将操作数（隐式的）转换为相同的类型。因此，在实现安全的算术运算之前，要确保理解整数转换规则（参见 **INT02­-C. Understand integer conversion rules**）。

#### 实现细节

使用 `-fwrapv` 命令行选项调用的 **GNU GCC** 编译器为无符号的和有符号的整数定义了同样的取模算法。

当一个有符号整数溢出时，使用 `-ftrapv` 命令行选项调用的**GNU GCC** 编译器会产生一个陷阱，这很有可能导致异常退出。在 **UNIX** 系统上，这个事件可能会产生一个发送到进程的信号。

既没有 `-fwrapv` 选项也没有 `-ftrapv` 选项调用的 **GNU GCC** 编译器，只是简单的假设有符号整数绝对不会溢出，并生成相应的目标代码。

#### 原子整数

C 标准定义了有符号原子整数的算术行为，以便在溢出时使用静默回绕的补码表示。尽管有定义，但是这些结果仍然可能是非期望的，并且会因此带来与无符号整数回绕类似的风险（参见 **INT30-­C 保证无符号整型数操作不会出现回绕**）。一般来说，原子整数类型的有符号整型溢出行为也应该被检查和预防。

#### 加法

加法是在两个算术类型的操作数之间或一个指向对象的指针和一个整数类型之间执行的。本规则只应用于两个算术类型相加的情况（指针加法的规则参见 **ARR37-­C. Do not add or subtract an integer to a pointer to a non­array object** 和 **ARR30­-C. Do not form or use out­of­bounds pointers or array subscripts**）。

此外，自增运算等同于加 1 运算。

**<font color=red>不合规代码</font>**

在以下的不合规代码示例中，有符号的算子 `si_a` 和 `si_b` 相加时可能会导致有符号整型溢出：

```cpp
void func(signed int si_a, signed int si_b)   
{  
    signed int sum = si_a + si_b;  
    /* ... */   
}  
```

**合规代码**

这种方案保证了加法操作不可能溢出，而无需考虑底层表示：

```cpp
#include <limits.h>  
void  f(signed int  si_a,  signed int  si_b)   
{  
    signed int  sum;  
    if (((si_b > 0) && (si_a > (INT_MAX - si_b))) ||  
        ((si_b < 0) && (si_a < (INT_MIN - si_b))))   
    {  
        /* Handle error */  
    }   
    else   
    {  
        sum = si_a + si_b;  
    }  
    /* ... */  
} 
```

#### 减法

减法是在两个算术类型的操作数之间，两个指向兼容对象类型的限定或未限定版本的指针之间，或一个指向一种对象类型的指针与一个整数类型的值之间执行的。本规则只应用于两个算术类型的操作数之间的减法（关于指针运算参见 **ARR36­-C. Do not subtract or compare two pointers that do not refer to the same array**，**ARR37­-C. Do not add or subtract an integer to a pointer to a non­array object** 和 **ARR30-­C. Do not form or use out-of­-bounds pointers or array subscripts**）。

此外，自减运算等同于减 1 运算。

**<font color=red>不合规代码</font>**

在以下的不合规代码示例中，无符号的算子 `ui_a` 和 `ui_b` 相减时可能会产生无符号整数回绕。如果回绕行为是非预期的，那么就可能导致易受攻击的安全漏洞。

```cpp
void func(signed int si_a, signed int si_b)   
{  
    signed int diff = si_a - si_b;  
    /* ... */   
} 
```

**合规代码**

这种方案对参与相减的操作数进行了前置条件测试，以保证不会出现回绕。

```cpp
#include <limits.h>  
void func(signed int si_a, signed int si_b)   
{  
    signed int diff;  
    if ((si_b > 0 && si_a < INT_MIN + si_b) ||  
        (si_b < 0 && si_a > INT_MAX + si_b))   
    {  
        /* Handle error */  
    }   
    else   
    {  
        diff = si_a - si_b;  
    }  
    /* ... */  
} 
```

#### 乘法

乘法是在两个算术类型的操作数之间执行的。

**<font color=red>不合规代码</font>**

在以下的不合规代码示例中，有符号的算子 `si_a` 和 `si_b` 相乘时可能会导致有符号整型溢出：

```cpp
void func(signed int si_a, signed int si_b)   
{  
    signed int result = si_a * si_b;  
    /* ... */  
} 
```

**合规代码**

两个操作数的乘积可以总是使用比两个操作数中的较大者的位数多两倍的位来表示。以下的合规方案在 **long long** 类型长度至少为 **int** 类型长度的两倍的系统上，消除了有符号整型溢出的情况：

```cpp
#include <stddef.h>  
#include <assert.h>  
#include <limits.h>  
#include <inttypes.h>  
extern size_t popcount(uintmax_t);  
#define PRECISION(umax_value) popcount(umax_value)  
void func(signed int si_a, signed int si_b)   
{  
    signed int result;  
    signed long long tmp;  
    assert(PRECISION(ULLONG_MAX) >= 2 * PRECISION(UINT_MAX));  
    tmp = (signed long long)si_a * (signed long long)si_b;  
    /* 
     * If the product cannot be represented as a 32-bit integer, 
     * handle as an error condition. 
     */  
    if ((tmp > INT_MAX) || (tmp < INT_MIN))   
    {  
        /* Handle error */  
    }   
    else   
    {  
        result = (int)tmp;  
    }  
    /* ... */  
}
```

如果 **long long** 的长度小于 **int** 的精度长度的 倍，则断言会失败。其中，宏`PRECISION()` 和函数 `popcount()` 能够计算任何整数类型的正确精度（参见 **INT35­-C 使用正确的整数精度**）。

**合规代码**

以下的可移植的合规解决方案能够应用于任何符合标准的编译器，即使这些编译器并不存在任何精度为 **int** 类型两倍的整数类型：

```cpp
#include <limits.h>  
void func(signed int si_a, signed int si_b) {  
    signed int result;  
    if (si_a > 0) {/* si_a is positive */  
        if (si_b > 0) { /* si_a and si_b are positive */  
            if (si_a > (INT_MAX / si_b)) {  
                /* Handle error */  
            }  
        } else { /* si_a positive, si_b nonpositive */  
            if (si_b < (INT_MIN / si_a)) {  
                /* Handle error */  
            }  
        } /* si_a positive, si_b nonpositive */  
    } else { /* si_a is nonpositive */  
        if (si_b > 0) { /* si_a is nonpositive, si_b is positive */  
            if (si_a < (INT_MIN / si_b)) {  
                /* Handle error */  
            }  
        } else { /* si_a and si_b are nonpositive */  
            if ( (si_a != 0) && (si_b < (INT_MAX / si_a))) {  
                /* Handle error */  
            }  
        } /* End if si_a and si_b are nonpositive */  
    } /* End if si_a is nonpositive */  
    result = si_a * si_b;  
}
```

#### 除法

除法是在两个算术类型之间执行的。在补码表示的有符号整数除法中，当有符号整数类型的最小值（负值）除以 -1 时，就会发生溢出。除法运算还可能导致除零错误（参见 **INT33-­C保证除法和取余运算不会导致除零错误**）。

**<font color=red>不合规代码</font>**

以下的不合规代码防止了除零错误（**INT33­-C 保证除法和取余运算不会导致除零错误**），但是却没有防止补码表示下的有符号整型溢出错误。

```cpp
void func(signed long s_a, signed long s_b)   
{  
    signed long result;  
    if (s_b == 0)   
    {  
        /* Handle error */  
    }   
    else   
    {  
        result = s_a / s_b;  
    }  
    /* ... */  
} 
```

在 **x86-32** 架构下，溢出产生的错误很容易导致拒绝服务攻击。

**合规代码**

以下的合规解决方案消除了除零错误和有符号整型溢出的可能性：

```cpp
void func(signed long s_a, signed long s_b)   
{  
    signed long result;  
    if ((s_b == 0) || ((s_a == LONG_MIN) && (s_b == -1)))  
    {  
        /* Handle error */  
    }   
    else   
    {  
        result = s_a / s_b;  
    }  
    /* ... */  
}    
```

#### 取余

取余运算符用于计算两个整型值相除时的余数。由于很多平台都使用相同的指令实现取余和除法运算，因此取余操作也同样容易导致算术溢出和除零错误（参见 **INT33­-C 保证除法和取余运算不会出现除零错误**）。

**<font color=red>不合规代码</font>**

以下的不合规代码防止了除零错误（**INT33-­C 保证除法和取余运算不会导致除零错误**），但是却没有防止补码表示下的有符号整型溢出错误。

```cpp
void func(signed long s_a, signed long s_b)   
{  
    signed long result;  
    if (s_b == 0)   
    {  
        /* Handle error */  
    }   
    else   
    {  
        result = s_a % s_b;  
    }  
    /* ... */  
}  
```

在 **x86-­32** 架构下，有符号整型的取余操作符是使用 `idiv` 指令代码与除法操作符一起实现的。既然 `LONG_MIN / -1` 会溢出并导致软件异常， `LONG_MIN % −1` 也同样如此。

**合规代码**

以下的合规解决方案对取余运算的操作数进行了测试，保证不会出现溢出：

```cpp
void func(signed long s_a, signed long s_b)   
{  
    signed long result;  
    if ((s_b == 0) || ((s_a == LONG_MIN) && (s_b == -1)))  
    {  
        /* Handle error */  
    }   
    else   
    {  
        result = s_a % s_b;  
    }  
    /* ... */  
} 
```

#### 左移位操作符

左移位运算是在两个整数操作数之间执行的。`E1 << E2` 的结果是 `E1` 向左移动 `E2` 个 bit位，其中空位填充零。C 标准 6.5.7 第 4 段（**ISO/IEC 9899:2011**）表示：

> *如果 E1是一个有符号类型的非负值，并且 E1×2E2能够被结果类型所表示，则就以其作为结果值；否则，该行为是未定义的。*
>
> *在几乎所有情况下，试图移动负数个 bit位或者移动超出操作数位数的 bit位数，都会导致逻辑错误。这一点在 INT34-C 不要将表达式移动负数位或移动大于等于操作数中存在的位数中进行说明。*

**<font color=red>不合规代码</font>**

以下的不合规代码进行左移操作时，对移位数非负，以及移位的数目为有效值的要求进行了验证。其中，宏 `PRECISION()` 和 函数 `popcount()` 能够计算任何整数类型的正确精度（参见 **INT35­-C 使用正确的整数精度**）。但是，由于代码中未进行溢出检查，因此结果仍然有可能得到一个无法表示的值。

```cpp
#include <limits.h>  
#include <stddef.h>  
#include <inttypes.h>  
extern size_t popcount(uintmax_t);  
#define PRECISION(umax_value) popcount(umax_value)  
void func(signed long si_a, signed long si_b)   
{  
    signed long result;  
    if ((si_a < 0) || (si_b < 0) ||  
        (si_b >= PRECISION(ULONG_MAX))   
    {  
        /* Handle error */  
    }   
    else   
    {  
        result = si_a << si_b;  
    }  
    /* ... */  
} 
```

**合规代码**

以下的合规解决方案消除了左移位运算中溢出的可能:

```cpp
#include <limits.h>  
#include <stddef.h>  
#include <inttypes.h>  
extern size_t popcount(uintmax_t);  
#define PRECISION(umax_value) popcount(umax_value)  
void func(signed long si_a, signed long si_b)   
{  
    signed long result;  
    if ((si_a < 0) || (si_b < 0) ||  
        (si_b >= PRECISION(ULONG_MAX) ||
         (si_a > (LONG_MAX >> si_b)))   
    {  
        /* Handle error */  
    }   
    else   
    {  
        result = si_a << si_b;  
    }  
    /* ... */  
}   
```

### <font style="background: yellow">✪ INT33-C 保证除法和取余运算不会导致除零错误</font>

C 标准认为在以下条件下进行除法或取余运算将会导致未定义行为：

| UB   | Description                              |
| ---- | ---------------------------------------- |
| 45   | / 或 % 运算符的第二个操作数为零（6.5.5） |

因此，必须保证除法和取余运算不会导致除零错误。

参考**INT32-C 保证有符号证书的运算不会溢出**中[除法](#除法)和[取余](#取余)的例子。

## 数组(ARR)

### <font style="background: yellow">✪ ARR30-C 不要使用超出边界的指针或超出边界的数组下标</font>

**<font color=red>不合规代码（构造越界指针）</font>**

这个不合规代码示例中，函数`f()`使用`index`作为一个偏移量来访问静态分配的整数表，并在使用之前验证`index`，但是函数未拒绝负`index`索引值。

当`index`小于零时，在函数的返回语句中的表达式的行为是不确定的。在一些实现中，仅仅是一个加法行为就可能触发硬件陷阱。在其他实现中，在解除引用时，加法可能触发硬件陷阱。其他实现方式中仍可能会产生一个不同于表的解除引用的指针，使用这种指针访问对象可能导致信息暴露或导致错误对象被修改。

```cpp
enum { TABLESIZE = 100 };  
static int table[TABLESIZE];  
int *f(int index)   
{  
  if (index < TABLESIZE)   
  {  
    return table + index;  
  }  
  return NULL;  
}  
```

**合规代码**

一个合规解决方案是检测并拒绝无效值`index`，这些无效值会导致指针运算时产生无效指针：

```cpp
enum { TABLESIZE = 100 };  
static int table[TABLESIZE];  
int *f(int index)   
{  
  if (index >= 0 && index < TABLESIZE)   
  {  
    return table + index;  
  }  
  return NULL;  
}  
```

**合规代码**

另一个稍微简单，而且可能更高效的合规解决方案是使用一个无符号类型，这样不仅可以检查负值索引，还同时可避免超出边界正值索引：

```cpp
enum { TABLESIZE = 100 };  
static int table[TABLESIZE];  
int *f(size_t index)   
{  
  if (index < TABLESIZE)   
  {  
    return table + index;  
  }  
  return NULL;  
} 
```

**<font color=red>不合规代码（索引超出范围的访问）</font>**

这段不合规代码示例声明一个7行5列的`matrix`数组。该函数`init_matrix`在迭代35次将参数x赋给每个成员，在第一次迭代过程中，`j`的值达到`COLS`，此时程序尝试存取元素`matrix[0][5]`，但实际已超出数组`matrix[7][5]`列的范围，这时就会导致未定义行为。

```cpp
#include <stddef.h>  
#define COLS 5  
#define ROWS 7  
static int matrix[ROWS][COLS];  
void init_matrix(int x)   
{  
  for (size_t i = 0; i < COLS; i++)   
  {  
    for (size_t j = 0; j < ROWS; j++)   
    {  
      matrix[i][j] = x;  
    }  
  }  
} 
```

**合规代码**

该标准的解决方案避免了使用初始化超出范围的指数`matrix`在同一行主顺序元素作为多维对象是用C语言声明：

```cpp
#include <stddef.h>  
#define COLS 5  
#define ROWS 7  
static int matrix[ROWS][COLS];  
void init_matrix(int x)   
{  
  for (size_t i = 0; i < ROWS; i++)   
  {  
    for (size_t j = 0; j < COLS; j++)   
    {  
      matrix[i][j] = x;  
    }  
  }  
}
```

**<font color=red>不合规代码（指针超过柔性数组成员范围）</font>**

在这个不合规的代码示例中，函数`find()`试图遍历柔性元素`buf`的成员。但是由于函数`g()`没有为`buf`数组分配存储空间，函数`find()`中的表达式`first++`将尝试访问未分配成员的`buf`数组的末尾。这将导致未定义行为。

```cpp
#include <stdlib.h>  
struct S {  
  size_t len;  
  char buf[];  /* Flexible array member */  
};  
const char *find(const struct S *s, int c) {  
  const char *first = s->buf;  
  const char *last  = s->buf + s->len;  
  while (first++ != last) { /* Undefined behavior */  
    if (*first == (unsigned char)c) {  
      return first;  
    }  
  }  
  return NULL;  
}  
void g(void) {  
  struct S *s = (struct S *)malloc(sizeof(struct S));  
  if (s == NULL) {  
    /* Handle error */  
  }  
  s->len = 0;  
  find(s, 'a');  
} 
```

**合规代码**

一个合规解决方案是检测并拒绝无效值`index`，这些无效值会导致指针运算时产生无效指针：

```cpp
#include <stdlib.h>  
struct S {  
  size_t len;  
  char buf[];  /* Flexible array member */  
};  
const char *find(const struct S *s, int c) {  
  const char *first = s->buf;  
  const char *last  = s->buf + s->len;  
  while (first != last) { /* Avoid incrementing here */  
if (*++first == (unsigned char)c) {  
      return first;  
    }  
  }  
  return NULL;  
}  
void g(void) {  
  struct S *s = (struct S *)malloc(sizeof(struct S));  
  if (s == NULL) {  
    /* Handle error */  
  }  
  s->len = 0;  
  find(s, 'a');  
}
```

### ARR36-C 不要将两个不同数组的指针做减法或者进行比较

若要两个指针相减，两者必须都指向同一个数组对象的元素或者只是这个数组对象最后一个元素的位置。相减的结果是两个数组元素的下标差。否则，得到的结果是不确定行为。

同样，使用关系运算符指针`<`，`<=`，`>=`，和`>`对指针的相对位置进行比较得出各指针指向元素的相互位置关系，未指向同一个数组的不同指针进行相减或比较将引发未定义的行为。

使用`==`和`!=`运算符进行指针的比较具有明确的语义，不论指针是否为空，是否指向相同类型的对象，或者指向数组对象尾部+1的位置，或者是指向一个函数等。

**<font color=red>不合规代码</font>**

在这个不合规代码示例中，指针减操作用于确定数组`nums`中有多少个可用成员：

```cpp
#include <stddef.h>  
enum { SIZE = 32 };  
void func(void) {  
  int nums[SIZE];  
  int end;  
  int *next_num_ptr = nums;  
  size_t free_elements;  
  /* Increment next_num_ptr as array fills */  
  free_elements = &end - next_num_ptr;  
}     
```

这个程序错误地假定`nums`数组和`end`变量比邻而居在存储器空间中，但实际上编译器允许在两个变量之间插入填充字节，甚至在内存中对它们重新排序。

**合规代码**

在这个合规的解决方案，`nums`数组中可用数组成员通过中减去指针`next_num_ptr`的方式获取，同时这个指针可以不被解除引用，它可以用于指针运算。

```cpp
#include <stddef.h>  
enum { SIZE = 32 };  
void func(void) {  
  int nums[SIZE];  
  int *next_num_ptr = nums;  
  size_t free_elements;  
  /* Increment next_num_ptr as array fills */  
  free_elements = &(nums[SIZE]) - next_num_ptr;  
} 
```

**例外**

**ARR36-­C­-EX1**：比较同一个结构体对象不同成员的指针是允许的，指向结构体后定义的成员的指针比指向结构体中先定义的成员指针大。

### ARR39-C 不要向指针中添加或减去缩放的整数

指针运算只有当指针指向一个数组的时候才是合理的（参见**ARR37-­C，不要给一个非数组对象指针加上或减去一个整数**）。当执行指针运算时，对指针进行加减操作时，其大小将自动缩放为该数组对象类型的大小。

向指针中添加或减去缩放的整数值是无效的，因为它可能产生不指向数组或者超过数组末尾的指针（参见**不要使用超出边界的指针或超出边界的数组下标**）。

同时，向指针增加一个非相同成员类型的大小时也是违反规则的，然而，假如`arr`是一个数组名，但不是一个指针的话，`arr[sizeof(arr)/sizeof(arr[0])])`这样的语句是允许的。

**<font color=red>不合规代码</font>**

在这个不合规的代码示例中，`sizeof(buf)`的结果和地址`buf`相加。这个例子之所以是不合规的，`sizeof(buf)`的实际大小将由**int**的大小进行伸缩，这个结果会导致然`buf`被伸缩。

```cpp
enum { INTBUFSIZE = 80 };  
extern int getdata(void);  
int buf[INTBUFSIZE];  
void func(void)   
{  
  int *buf_ptr = buf;  
  while (buf_ptr < (buf + sizeof(buf)))   
  {  
    *buf_ptr++ = getdata();  
  }  
}  
```

**合规代码**

此合规解决方案使用非伸缩整数来获取指向数组末尾的指针：

```cpp
enum { INTBUFSIZE = 80 };  
extern int getdata(void);  
int buf[INTBUFSIZE];  
void func(void)   
{  
  int *buf_ptr = buf;  
  while (buf_ptr < (buf + INTBUFSIZE))   
  {  
    *buf_ptr++ = getdata();  
  }  
}    
```

**<font color=red>不合规代码</font>**

在这个不符合要求的代码示例中，指针`s`加上了`skip`变量的值。然而，`skip`表示`ull_b`成员在`big`中的字节偏移量，当和指针`s`相加后，`skip`被加上了`skip`个`struct big`这样的大小。

```cpp
#include <string.h>  
#include <stdlib.h>  
#include <stddef.h>  
struct big   
{  
  unsigned long long ull_a;  
  unsigned long long ull_b;  
  unsigned long long ull_c;  
  int si_e;  
  int si_f;  
};  
void func(void)   
{  
  size_t skip = offsetof(struct big, ull_b);  
  struct big *s = (struct big *)malloc(sizeof(struct big));  
  if (s == NULL)   
  {  
    /* Handle malloc() error */  
  }  
  memset(s + skip, 0, sizeof(struct big) - skip);  
  /* ... */  
  free(s);  
  s = NULL;  
}
```

**合规代码**

这个合规的解决方案使用**unsigned char**来计算偏移而不使用`struct big`，后者会导致所加的大小被伸缩放大：

```cpp
#include <string.h>  
#include <stdlib.h>  
#include <stddef.h>  
struct big   
{  
  unsigned long long ull_a;  
  unsigned long long ull_b;  
  unsigned long long ull_c;  
  int si_d;  
  int si_e;  
};  
void func(void)   
{  
  size_t skip = offsetof(struct big, ull_b);  
  unsigned char *ptr = (unsigned char *)malloc(  
    sizeof(struct big)  
  );  
  if (ptr == NULL)   
  {  
     /* Handle malloc() error */  
  }  
  memset(ptr + skip, 0, sizeof(struct big) - skip);  
  /* ... */  
  free(ptr);  
  ptr = NULL;  
}  
```

## 字符和字符串（STR）

### <font style="background: yellow">✪ STR30-C 不要试图修改字符串常量</font>

字符串常量是双引号内的0个或多个字节字符的序列（如 **xyz** ），宽字符串常量基本相同，区别在于它有字母前缀L（例如 L**xyz** ）。

在编译时，字符串常量用于创建一个长度足以容纳字符序列和 `null` 终止符的具有静态持久期的数组。标准并没有指定这些数组是否不同。如果一个程序试图修改字符串常量，其行为是未定义的，但是常常会导致访问违规，因为字符串常量一般存储在只读内存中。

不要试图修改字符串常量，可以使用命名的字符数组实现可修改的字符串。不要将字符串常量（强制转换）赋值给**non-const** 指针。

**<font color=red>不合规代码</font>**

在这个不合规代码示例中， **char** 指针 `p` 初始化为指向一个字符串常量的地址。试图修改这个字符串常量会导致未定义的行为。

```cpp
char *p = "string literals";  
p[0] = 'S';
```

**合规代码**

当字符串常量做为数组初始化值时，它指定了数组中字符的初始值以及数组的长度。这段代码在字符数组 `a` 分配的空间中创建了这个字符串常量的一份拷贝。存储在 `a` 中的字符串可以安全地修改。

```cpp
char a[] = "string literals";  
a[0] = 'S';
```

**<font color=red>不合规代码</font>**

在这个不合规代码示例中， `mktemp` 函数入参是 **non-const** 指针， `mktemp` 函数修改了它的字符串参数。

```cpp
mktemp("/temp/edxxxxxxxx"); 
```

**合规代码**

不传递字符串常量，而是使用一个命名数组：

```cpp
static char fname[] = "/temp/edxxxxxxxx";  
mktemp(fname); 
```

**<font color=red>不合规代码</font>**

在这个不合规代码示例中，使用 `strrchr` 函数的 `char *` 类型返回结果，修改 `pathname` 。因为 `strrchr` 的入参是一个字符串常量，因此这种修改行为是未定义的。

```cpp
#include <stdio.h>  
#include <string.h>  
const char *get_dirname(const char *pathname) {  
    char *slash;  
    slash = strrchr(pathname, ‘/’);  
    if (slash) {  
        *slash = ‘\0’; /* Undefined behavior */  
    }  
    return pathname;  
} 
int main(void) {  
    puts(get_dirname(__FILE__));  
    return 0;  
} 
```

**合规代码**

避免修改 **const** 对象，即使 `strrchr` 函数返回的是 `non-const char *` 指针。仅仅将 `pathname` 入参的类型修改为`char *`是不够的，因为并没有强制要求编译器对将字符串常量赋值给`char *`进行检查。

```cpp
#include <stdio.h>  
#include <string.h>  
const char *get_dirname(const char *pathname, char *dirname, size_t size)   
{  
    const char *slash;  
    slash = strrchr(pathname, ‘/’);  
    if (slash) {  
        ptrdiff_t slash_idx = slash – pathname;  
        if ((size_t)slash_idx < size) {  
            memcpy(dirname, pathname, slash_idx);  
            dirname[slash_idx] = ‘\0’;  
            return dirname;  
        }  
    }  
    return 0;  
}  
int main(void)   
{  
    char dirname[260];  
    if (get_dirname(__FILE__, dirname, sizeof(dirname))) {  
        puts(dirname);  
    }  
    return 0;  
} 
```

### <font style="background: yellow">✪ STR31-C 保证字符串的存储具有足够的空间容纳字符数据和null结尾符</font>

把数据复制到一个不足以容纳这些数据的缓冲区会导致缓冲区溢出。缓冲区溢出并不限于`null` 结尾的字节字符串（**NTBS**），但是它常常是在操纵**NTBS**数据时发生。为了防止这类错误，需要对复制进行限制，可以通过截断或者保证目标缓冲区具有足够的空间容纳需要复制的字符数据和 `null` 结尾符。后者是更好的方法。

**<font color=red>不合规代码（fscanf()）</font>**

如下的不合规代码示例，调用 `fscanf()` 函数可能会导致缓冲区写溢出。

```cpp
#include <stdio.h>   
enum { BUF_LENGTH = 1024 };   
void get_data(void)   
{   
    char buf[BUF_LENGTH];   
    if (1 != fscanf(stdin, "%s", buf))   
    {   
        /* Handle error */   
    }  
    /* Rest of function */ 
} 
```

**合规代码（fscanf()）**

```cpp
#include <stdio.h>   
enum { BUF_LENGTH = 1024 };   
void get_data(void)   
{   
    char buf[BUF_LENGTH];   
    if (1 != fscanf(stdin, "%1023s", buf))   
    {  
        /* Handle error */   
    }  
    /* Rest of function */  
}    
```

**<font color=red>不合规代码（argv）</font>**

命令行参数会以字符串指针数组的形式传递给 `main()` 函数，从`argv[0]`到 `argv[argc–1]`。如果 `argc` 大于0，则 `argv[0]` 按惯例为程序的名字。如果 `argc` 大于1，则 `argv[1]` 到 `argv[argc-1]` 为程序的其他参数。因此，如果不适当的拷贝命令行参数，可能会导致安全隐患。正如下面的这段代码，攻击者可以通过操纵 `argv[0]` 的内容制造缓冲区溢出。

```cpp
#include <string.h>   
int main(int argc, char *argv[])   
{   
    /* Ensure argv[0] is not null */   
    const char *const name = (argc && argv[0]) ? argv[0] : "";   
    char prog_name[128];   
    strcpy(prog_name, name);   
    return 0;  
}
```

**合规代码（argv）**

使用 `strlen()` 函数来确定 `argv[0]` 字符串的长度，从而可以动态分配足够的内存。

```cpp
#include <stdlib.h>   
#include <string.h>   
int main(int argc, char *argv[])   
{   
    /* Ensure argv[0] is not null */   
    const char *const name = (argc && argv[0]) ? argv[0] : "";   
    char *prog_name = (char *)malloc(strlen(name) + 1);   
    if (prog_name != NULL)   
    {   
        strcpy(prog_name, name);   
    }   
    else   
    {  
        /* Handle error */  
    }  
    free(prog_name);   
    return 0;  
}  
```

**合规代码（argv）**

如果参数不需要被修改或被连接，则没有理由拷贝一份。不拷贝字符串是防止缓冲区写溢出的最好的手段，而且往往也最高效。不过不要做出 `argv[0]` 一定非空的错误假设。

```cpp
int main(int argc, char *argv[])     
{     
    /* Ensure argv[0] is not null */     
    const char * const prog_name = (argc && argv[0]) ? argv[0] : "";     
    /* ... */     
    return 0;    
}
```

**注**：`getenv`和`sprintf`有同样问题。

### STR32-C 不要将非null结尾的字符序列当做字符串传递给库函数

很多库函数接受一个字符串参数，且要求该字符串是以 `null` 字符结尾的。如果传递一个非 `null` 结尾的字符序列，则可能导致库函数访问边界外的非法内存。因此，不要传递一个非 `null` 结尾的字符序列给库函数。

**<font color=red>不合规代码</font>**

下面的代码示例中，字符序列 `c_str` 没有以 `null` 字符结尾，且当做入参传递给了`printf()` 函数。

```cpp
#include <stdio.h>   
void func(void)   
{   
    char c_str[3] = "abc";   
    printf("%s\n", c_str);  
}
```

**合规代码**

该解决方案在声明字符数组时未指定范围，此时，编译器会根据字符字面值的长度分配合适的存储空间，用于容纳该字符字面值以及 `null` 字符。

```cpp
#include <stdio.h>   
void func(void)   
{   
    char c_str[] = "abc";   
    printf("%s\n", c_str);  
} 
```

同样的，`realloc`和`strncpy`使用时也需要注意置`null`结尾。

### STR34-C 在转换为更大的整数长度时把字符转换为无符号类型

有符号字符数据在赋值或转换为更大的有符号类型之前必须转换为无符号类型。由于编译器可以选择把 **char** 定义为与 **signed char** 相同的范围、表示形式和行为，因此这个规则应该同时适用于 **signed char** 和普通的 **char** 字符类型。

这个规则只适用于字符数据可能包含被解释为负值的字符的情况下。例如，如果 **char** 类型用8位补码表示，大于 +127 的所有字符都解释为负值。

**<font color=red>不合规代码</font>**

这个不合规代码示例取自**bash 1.14.6**及更早版本中的一个潜在风险，它导致了**CERT AdvisoryCA­-1996­-22**的发布。这个潜在风险来自**bash**源代码**parse.y**模块中的`yy_string_get()` 函数中的**string**指针所引用的字符数据的符号扩展。

```cpp
static int yy_string_get(void)   
{   
    register char *c_str;   
    register int c;   
    c_str = bash_input.location.string;   
    c = EOF;   
    /* If the string doesn't exist or is empty, EOF found */   
    if (c_str && *c_str)   
    {   
        c = *c_str++;   
        bash_input.location.string = c_str;   
    }  
    return (c);  
}  
```

`c_str`变量用于遍历包含了需要解析的命令行的字符串。从这个指针提取字符时，它们存储在一个**int**类型的变量中。对于**char**类型默认为**signed char**的编译器，这个值赋值给 **int** 变量时会进行符号扩展。以字符255（­1的补码形式）为例，有符号扩展导致把­1这个值赋值给了这个整数`c`，这样就无法与 `EOF` 区分。

**<font color=red>不合规代码</font>**

这个问题可以通过显式地把 `c_str` 变量声明为 **unsigned char** 类型来修正。但是，这个解决方案违反了**使用普通 char 类型表示基本字符集中的字符**规范。

**合规代码**

在这个合规解决方案中，表达式 `*c_str++` 的结果在复制给 **int** 变量 `c` 之前转换为 **unsigned char** 类型。

```cpp
static int yy_string_get(void)   
{   
    register char *c_str;   
    register int c;   
    c_str = bash_input.location.string;   
    c = EOF;   
    /* If the string doesn't exist or is empty, EOF found */   
    if (c_str && *c_str)   
    {   
        c = (unsigned char)*c_str++;   
        bash_input.location.string = c_str;   
    }  
    return (c);  
}
```

## 内存管理（MEM）

### MEM31-C 释放不再需要的动态分配的内存

当通过调用标准内存分配函数分配的内存不再需要时，必须配对调用 `free()` 函数释放。

**<font color=red>不合规代码</font>**

在这个不合规代码示例中，通过 `malloc()` 分配的内存，在指向它的指针 `text_buffer` 生命周期结束前，没有释放该内存。

```cpp
#include <stdlib.h>   
enum { BUFFER_SIZE = 32 };   
int f(void)   
{   
    char *text_buffer = (char *)malloc(BUFFER_SIZE);   
    if (text_buffer == NULL)   
    {   
        return -1;   
    }  
    // free(text_buffer);  
    return 0;  
} 
```

**合规代码**

调用 `free()` 函数释放内存。

```cpp
#include <stdlib.h>   
enum { BUFFER_SIZE = 32 };   
int f(void)   
{   
    char *text_buffer = (char *)malloc(BUFFER_SIZE);   
    if (text_buffer == NULL)   
    {   
        return -1;   
    }  
    free(text_buffer);  
    return 0;  
} 
```

**例外**

当使用具有全程序生命周期的静态指针指向分配的内存时，可以不需要有配对的释放操作。下面这个例子中，通过 `malloc()` 分配的内存地址被赋予了 **static** 变量。

```cpp
#include <stdlib.h>   
enum { BUFFER_SIZE = 32 };   
int f(void) {   
    static char *text_buffer = NULL;   
    if (text_buffer == NULL)   
    {   
        text_buffer = (char *)malloc(BUFFER_SIZE);   
        if (text_buffer == NULL)   
        {   
            return -1;   
        }   
    }  
    return 0;  
}  
```

### MEM34-C 只释放动态分配的内存

释放并非动态分配的内存会导致严重的错误。这个错误造成的特定后果取决于编译器，有可能什么也不发生，也可能导致程序异常终止。不管是什么编译器，应该避免对不是由动态内存分配函数（例如 `malloc()` 、 `calloc()` 、 `realloc()` ）所返回的指针调用 `free()` 。

向 `realloc()` 提供一个指向并非动态分配的内存的指针也会产生类似的情况。 `realloc()` 函数用于改变一块动态内存的大小。如果向 `realloc()` 提供一个指向并非由 `malloc()` 这样的内存分配函数分配的内存的指针，程序可能会异常终止。

C语言标准指出，给 `free()` 或 `realloc()` 函数传递一个并非有内存管理函数返回的指针，或释放已经由 `free()` 或 `realloc()` 释放的内存，其行为是未定义的。传递空指针是安全的，因为C语言规范规定给 `free()` 函数传递空指针，不会有任何动作发生。

**<font color=red>不合规代码</font>**

这个不合规代码示例根据 `argc` 的值，把 `c_str` 设置为一块动态分配的内存的引用或者一个静态分配的字符串常量。不论那种情况， `c_str` 做为参数传递给 `free()` 。如果`c_str` 所引用的并不是动态分配的内存，对 `free(c_str)` 的调用就会出现错误。

```cpp
#include <stdlib.h>   
#include <string.h>   
#include <stdio.h>   
enum { MAX_ALLOCATION = 1000 };   
int main(int argc, const char *argv[]) {   
    char *c_str = NULL;   
    size_t len;   
    if (argc == 2) {   
        len = strlen(argv[1]) + 1;   
        if (len > MAX_ALLOCATION) {   
            /* Handle error */   
        }  
        c_str = (char *)malloc(len);   
        if (c_str == NULL) {   
            /* Handle error */  
        }  
        strcpy(c_str, argv[1]);   
    } else {   
        c_str = "usage: $>a.exe [string]";   
        printf("%s\n", c_str);   
    }  
    free(c_str);   
    return 0;   
}
```

**合规代码**

在这个合规解决方案中，消除了 `c_str` 执行非动态分配内存的可能。

```cpp
#include <stdlib.h>   
#include <string.h>   
#include <stdio.h>   
enum { MAX_ALLOCATION = 1000 };   
int main(int argc, const char *argv[]) {   
    char *c_str = NULL;   
    size_t len;   
    if (argc == 2) {   
        len = strlen(argv[1]) + 1;   
        if (len > MAX_ALLOCATION) {   
            /* Handle error */   
        }  
        c_str = (char *)malloc(len);   
        if (c_str == NULL) {   
            /* Handle error */  
        }  
        strcpy(c_str, argv[1]);   
    } else {   
        printf("usage: $>a.exe [string]" );    
        return EXIT_FAILURE; 
    }  
    free(c_str);   
    return 0;   
} 
```

### <font style="background: yellow">✪ MEM35-C 为对象分配足够的内存</font>

作为长度参数传递给 `malloc()` 、 `calloc()` 或 `realloc()` 的整数值必须是合法的，足以容纳被存储的对象。如果长度参数不正确或者可能被攻击者所操纵，就有可能发生缓冲区溢出。不正确的长度参数、不充分的范围检查、整数溢出或截断会导致分配长度不足的缓冲区。程序员必须保证内存分配函数的长度参数能够分配足够数量的内存。

**<font color=red>不合规代码（长度计算）</font>**

在这个不合规代码示例中，分配了一个**long**类型的数组并赋值给`p`。但是，它使用了`sizeof(int)`来确定分配内存的长度。如果`sizeof(long)`大于`sizeof(int)` ，会导致实际分配的内存不足。

```cpp
#include <stdint.h>   
#include <stdlib.h>   
void function(size_t len)   
{   
    long *p;   
    if (len == 0 || len > SIZE_MAX / sizeof(long))   
    {   
        /* Handle overflow */   
    }  
    p = (long *)malloc(len * sizeof(int));   
    if (p == NULL)   
    {   
        /* Handle error */   
    }  
    free(p);  
}
```

**合规代码（长度计算）**

为了修正这个不合规代码示例，使用 `sizeof(long)` 确定内存分配的长度。

```cpp
#include <stdint.h>   
#include <stdlib.h>   
void function(size_t len)   
{   
    long *p;   
    if (len == 0 || len > SIZE_MAX / sizeof(long))   
    {   
        /* Handle overflow */   
    }  
    p = (long *)malloc(len * sizeof(long));   
    if (p == NULL)   
    {   
        /* Handle error */   
    }  
    free(p);  
} 
```

另外，还可以使用 `sizeof(*p)` 正确地设置分配的长度。

# C++安全编码规范

## 声明及初始化

### DCL54-CPP 成对重载allocation与deallocation函数并置于相同作用域中

分配内存函数和释放内存函数，均可以在全局或类作用域内重载。要求分配内存和释放内存函数成对重载，并且作用域相同。

**<font color=red>不合规代码</font>**

如下代码中，`operator new ()` 在类范围内重载，但`operator delete()` 在类范围内没有相应重载。尽管重载的分配函数实际调用默认全局分配函数，但由于未能相应地更新分配地址，删除对象时将导致不可预知结果。

```cpp
#include <new>  
extern "C++" void update_bookkeeping(void *allocated_ptr, std::size_t size, bool alloc);  
struct S {  
    void *operator new(std::size_t size) noexcept(false)   
    {  
        void *ptr = ::operator new(size);  
        update_bookkeeping(ptr, size, true);  
        return ptr;  
    }  
};
```

**合规代码:**

如下代码中， `operator delete()` 应地在类范围内被定义。

```cpp
#include <new>  
extern "C++" void update_bookkeeping(void *allocated_ptr, std::size_t size, bool alloc); 
struct S  
{  
    void *operator new(std::size_t size) noexcept(false)  
    {  
        void *ptr = ::operator new(size);  
        update_bookkeeping(ptr, size, true);  
        return ptr;  
    }  
    void operator delete(void *ptr, std::size_t size) noexcept  
    {  
        ::operator delete(ptr);  
        update_bookkeeping(ptr, size, false);  
    }  
}; 
```

### <font style="background: yellow">✪ DCL55-CPP 避免跨信任边界传递类对象时发生信息泄露</font>

​    C++结构体经常包含填充位，当数据在不同信任域的结构体之间拷贝时，如果源结构体的填充位包含敏感信息，则可能导致信息泄露。本条规则要求，程序员必须确保，在进行结构体拷贝时，不拷贝填充信息。

**<font color=red>不合规代码</font>**

下面代码，结构体使用填充位确保成员对齐。当结构体数据复制到用户空间时，这些填充位包含的敏感信息可能泄露。

```cpp
#include <cstddef>  
struct test  
{  
    int a;  
    char b;  
    int c;  
};  
// 安全复制字节到用户空间  
extern int copy_to_user(void *dest, void *src, std::size_t size);  
void do_stuff(void *usr_buf)  
{  
    test arg{ 1, 2, 3 };  
    copy_to_user(usr_buf, &arg, sizeof(arg)); 
}
```

**<font color=red>不合规代码</font>**

看起来，下面代码中，初始化列表会将对象中所有比特初始化为0。但是，编译器可能将32位寄存器的低字节设置为2，高字节不变，再存储整个32位数据，仍然存在信息泄露风险。

```cpp
#include <cstddef>  
struct test  
{  
    int a;  
    char b;  
    int c;  
};  
//安全复制字节到用户空间  
extern int copy_to_user(void *dest, void *src, std::size_t size);  
void do_stuff(void *usr_buf)  
{  
    test arg{ };  
    arg.a = 1;  
    arg.b = 2;  
    arg.c = 3;  
    copy_to_user(usr_buf, &arg, sizeof(arg));  
} 
```

**合规代码**

以下代码，先将结构数据序列化，再复制到不受信任的上下文。

```cpp
#include <cstddef>  
#include <cstring>  
struct test  
{  
    int a;  
    char b;  
    int c;  
};  
// 安全复制字节到用户空间  
extern int copy_to_user(void *dest, void *src, std::size_t size);  
void do_stuff(void *usr_buf)  
{  
    test arg  
    { 1, 2, 3 };  
// 可能大于严格需要的内存大小  
    unsigned char buf[sizeof(arg)];  
    std::size_t offset = 0;  
    std::memcpy(buf + offset, &arg.a, sizeof(arg.a));  
    offset += sizeof(arg.a);   
    std::memcpy(buf + offset, &arg.b, sizeof(arg.b));  
    offset += sizeof(arg.b);  
    std::memcpy(buf + offset, &arg.c, sizeof(arg.c));  
    offset += sizeof(arg.c);  
    copy_to_user(usr_buf, buf, offset /* size of info copied */);  
}
```

这段代码保证了复制到非特权用户的填充位都是被初始化过的。复制到用户空间的结构现在是打包的，需要用`copy_to_user()`函数解包以重建原始的填充结构。

**合规代码（填充字节）**

以下代码，把填充位显式声明为结构中的字段。但是，这个解决方案不可移植，它特定用于**x86-­32**体系结构。

```cpp
#include <cstddef>  
struct test  
{  
    int a;  
    char b;  
    char padding_1, padding_2, padding_3;  
    int c;  
    test(int a, char b, int c) :  
            a(a), b(b), padding_1(0), padding_2(0), padding_3(0), c(c)  
    {  
    }  
};  
//确保c是最后一个填充字节之后的下一个字节。  
static_assert(offsetof(test, c) == offsetof(test, padding_3) + 1,  
        "Object contains intermediate padding");  
//确保没有尾填充。  
static_assert(sizeof(test) == offsetof(test, c) + sizeof(int),  
        "Object contains trailing padding");  
// 安全复制字节到用户空间  
extern int copy_to_user(void *dest, void *src, std::size_t size);  
void do_stuff(void *usr_buf)  
{  
    test arg  
    { 1, 2, 3 };  
    copy_to_user(usr_buf, &arg, sizeof(arg));  
}    
```

### DCL59-CPP 不要在头文件中定义匿名的命名空间

如果在某个头文件中定义匿名的命名空间，假设此匿名命名空间中定义了变量或函数，则所有包含这个头文件的编译单元中，将各自生成这些变量或函数的唯一实例，引起意外错误。

**<font color=red>不合规代码</font>**

以下代码，变量 `v` 定义在头文件的匿名空间中，导致**a.cpp**和**b.cpp**各自生成一个不同的`v` 实例，引起意外结果。

```cpp
// a.h  
#ifndef A_HEADER_FILE  
#define A_HEADER_FILE  
namespace  
{  
int v;  
}  
#endif // A_HEADER_FILE  
// a.cpp  
#include "a.h"  
#include <iostream>  
void f()  
{  
    std::cout << "f(): " << v << std::endl;  
    v = 42;  
// ...  
}  
// b.cpp  
#include "a.h"  
#include <iostream>  
void g()  
{  
    std::cout << "g(): " << v << std::endl;  
    v = 100;  
}  
 int main()  
{  
    extern void f();  
    f(); // Prints v, sets it to 42  
    g(); // Prints v, sets it to 100  
    f();  
    g();  
} 
```

当程序执行时，打印如下：

```shell
f(): 0
g(): 0
f(): 42
g(): 100
```

**合规代码**

以下代码， `v` 仅在一个编译单元中定义，但对于所有编译单元可见，其行为符合预期。

```cpp
// a.h  
#ifndef A_HEADER_FILE  
#define A_HEADER_FILE  
extern int v;  
#endif // A_HEADER_FILE  
// a.cpp  
#include "a.h"  
#include <iostream>  
int v; // Definition of global variable v  
void f()  
{  
    std::cout << "f(): " << v << std::endl;  
    v = 42;  
// ...  
}  
// b.cpp  
#include "a.h"  
#include <iostream>  
void g()  
{  
    std::cout << "g(): " << v << std::endl;  
    v = 100;  
}  
int main()  
{  
    extern void f();  
    f(); // Prints v, sets it to 42  
    g(); // Prints v, sets it to 100  
    f(); // Prints v, sets it back to 42  
    g(); // Prints v, sets it back to 100  
} 
```

程序执行结果如下：

```shell
f(): 0
g(): 42
f(): 100
g(): 42
```

**<font color=red>不合规代码</font>**

如下代码，在头文件的匿名空间中定义一个`f()`函数，导致最终生成多个不同的 `f()` 定义，链接时间增加，执行文件变大，性能降低。

```cpp
// a.h  
#ifndef A_HEADER_FILE  
#define A_HEADER_FILE  
namespace  
{  
    void f()  
    { /* ... */  
    }  
}  
#endif // A_HEADER_FILE  
// a.cpp  
#include "a.h"  
// ...  
// b.cpp  
#include "a.h"  
// ...
```

**合规代码**

如下代码， `f()` 没有使用匿名的命名空间，而是定义为内联函数。内联函数在包含它们的所有编译单元中定义相同，编译器仅生成函数的单个实例。

```cpp
// a.h  
#ifndef A_HEADER_FILE  
#define A_HEADER_FILE  
inline void f()  
{ /* ... */  
}  
#endif // A_HEADER_FILE  
// a.cpp  
#include "a.h"  
// ...  
// b.cpp  
#include "a.h"  
// ...    
```

## 表达式

### EXP50-CPP 不要依赖求值顺序

C++表达式或对象初始化，不依赖于求值顺序，以免带来不确定性，这个规则意味着，下面的声明具有确定的行为。

```cpp
i = i + 1;  
a[i] = i;
```

而如下的声明则没有

```cpp
// i is modified twice in the same full expression  
i = ++i + 1;  
// i is read ot  
```

常见的一些可能相互依赖影响的场景：

- 在逻辑 `&&` 或者 `||` 表达式中，如果对第二个表达式求值，则第一个表达式可能会对第二个表达式有影响

- 在条件表达式 `?:` 中，第一个表达式可能对第二个、第三个表达式的影响

- 当对初始化列表求值时，与每个初始化子句相关联的值计算可能会对排在其后面初始化子句有影响

- 不确定的函数执行顺序，函数执行的顺序不同，运行结果不同，尤其是在全局初始化阶段尤为明显

**<font color=red>不合规代码</font>**

在这个不合规的代码示例中， `i` 以不确定的顺序被求值不止一次，因此表达式的行为是未定义的。

```cpp
void f(int i, const int *b)  
{  
    int a = i + b[++i];  
// ...  
}
```

**合规代码**

这些示例独立于操作数的求值顺序，并且每个只有一种解释方式。

```cpp
void f(int i, const int *b)  
{  
    ++i;  
    int a = i + b[i];  
// ...  
}  
void f(int i, const int *b)  
{  
    int a = i + b[i + 1];  
    ++i;  
// ...  
} 
```

**<font color=red>不合规代码</font>**

此不合规代码示例，展示了函数参数的求值顺序未确定所带来的不确定行为。

```cpp
extern void c(int i, int j);  
int glob;  
int a()  
{  
    return glob + 10;  
}  
int b()  
{  
    glob = 42;  
    return glob;  
}  
void f()  
{  
    c(a(), b());  
} 
```

未指定 `a()` 和`b()` 的调用顺序，唯一可以确认的是在调用 `c()` 之前调用 `a()` 和`b()` 。 如果 `a()` 或 `b()` 在计算它们的返回值时依赖于执行顺序，就像在这个例子中一样，传递给 `c()` 的参数可能在不同的编译器计算结果不同。

**合规代码**

合规代码中， `a()` 和 `b()` 的求值顺序是固定的，所以不会产生不确定行为。

```cpp
extern void c(int i, int j);  
int glob;  
int a()  
{  
    return glob + 10;  
}  
int b()  
{  
    glob = 42;  
    return glob;  
}  
void f()  
{  
    int a_val, b_val;  
    a_val = a();  
    b_val = b();  
    c(a_val, b_val);  
} 
```

### EXP51-CPP 不要通过不正确类型指针删除一个数组

如果通过基类指针删除含有虚函数的子类数组，会导致无法预测的结果。

**<font color=red>不合规代码</font>**

本示例中创建了一个`Derived`类型的数组对象，保存为`Base *`。尽管`Base::~Base()`被声明为虚的，仍然会导致无法预测的结果。

```cpp
struct Base  
{  
    virtual ~Base() = default;  
};  
struct Derived final : Base  
{  
};  
void f()  
{  
    Base *b = new Derived[10];  
// ...  
    delete[] b;  
} 
```

**合规代码**

在下面这个合规解决方案中，`b`的静态类型是`Derived *`，这样当引用到这个数组对象和删除这个指针的时候就不会产生未定义的行为。

```cpp
struct Base  
{  
    virtual ~Base() = default;  
};  
struct Derived final : Base  
{  
};  
void f()  
{  
    Derived *b = new Derived[10];  
// ...  
    delete[] b;  
} 
```

### EXP52-CPP 不要依赖不求值的操作

C++中，如下表达式不对操作数求值，包括：`sizeof()`、`typeid()`、`noexcept()`、`decltype()`、`declval()`。不要在该类表达式中改变操作数的值。

**<font color=red>不合规代码（sizeof）</font>**

如下代码， `a++`这个表达式不会生效

```cpp
#include <iostream>  
void f()  
{  
    int a = 14;  
    int b = sizeof(a++);  
    std::cout << a << ", " << b << std::endl;  
} 
```

因此， `a` 的值在 `b` 初始化之后还是14.

**合规代码（sizeof）**

如下代码，变量`a`的值在`sizeof()` 操作符外面`++`

```cpp
#include <iostream>  
void f()  
{  
    int a = 14;  
    int b = sizeof(a);  
    ++a;  
    std::cout << a << ", " << b << std::endl;  
} 
```

**<font color=red>不合规代码（decltype）</font>**

如下代码，`i++`这个表达式在`decltype()`说明符中不被求值。

```cpp
#include <iostream>  
void f()  
{  
    int i = 0;  
    decltype(i++) h = 12;  
    std::cout << i;  
}
```

因此，`i`的值仍然是0。

**合规代码（decltype）**

如下代码，`i`在`decltype`说明符外面`++`，与预期结果相同

```cpp
#include <iostream>  
void f()  
{  
    int i = 0;  
    decltype(i) h = 12;  
    ++i;  
    std::cout << i;  
}  
```

### EXP53-CPP 不要读取未初始化的内存

在对象初始化之前读取对象的值，得到的是随机值。

**常见场景**：

- 函数内局部变量未初始化

- 类的成员变量未初始化

**<font color=red>不合规代码</font>**

在这个不合规代码中，未初始化的局部变量将作为表达式的一部分进行计算，打印出来的值为随机值。

```cpp
#include <iostream>  
void f()  
{  
    int i;  
    std::cout << i;  
}  
```

**合规代码**

在这个合规解决方案中，对象在打印其值之前进行初始化。

```cpp
#include <iostream>  
void f()  
{  
    int i=0;  
    std::cout << i;  
}  
```

**<font color=red>不合规代码</font>**

在这个不合规代码示例中，`int *`对象由一个**new-­expression**分配，但它指向的内存不会被初始化。打印指针值是明确定义的，但它指向的值是随机的。

```cpp
#include <iostream>  
void f()  
{  
    int *i = new int;  
    std::cout << i << ", " << *i;  
} 
```

**合规代码**

在这个合规解决方案中，在打印其值之前，将其值初始化为12。

```cpp
#include <iostream>  
void f()  
{  
    int *i = new int(12);  
    std::cout << i << ", " << *i;  
} 
```

可以在分配的类型之后加上括号或花括号，来完成由**new-­expression**生成的对象初始化，如果初始化不提供默认值，则会用零来初始化对象，如下面的代码所示：

```cpp
int *i = new int(); // zero-initializes *i  
int *j = new int{}; // zero-initializes *j  
int *k = new int(12); // initializes *k to 12  
int *l = new int{12}; // initializes *l to 12  
```

**<font color=red>不合规代码</font>**

在这个不合规代码示例中，类成员变量 `c` 没有被默认构造函数中的显式初始化，虽然局部变量 `s` 已经被默认初始化，但在调用 `S::f()` 中使用的 `c` 是未初始化的。

```cpp
class S  
{  
    int c;  
public:  
    int f(int i) const  
    {  
        return i + c;  
    }  
};  
void f()  
{  
    S s;  
    int i = s.f(10);  
}  
```

**合规代码**

在合规代码中，类`S`给出了一个默认构造函数初始化了类成员变量`c`。

```cpp
class S  
{  
    int c;  
public:  
    S() : c(0)  
    {  
    }  
    int f(int i) const  
    {  
        return i + c;  
    }  
};  
void f()  
{  
    S s;  
    int i = s.f(10);  
}  
```

### EXP54-CPP 不要访问在其生命周期之外的对象

每个对象都有其生命周期，在对象初始化之后、且在对象析构之前可以正常使用。

**<font color=red>不合规代码</font>**

在这个不合规代码示例中，对象的指针在对象的生命周期开始之前，被用来调用指向其对象的非静态成员函数，会导致未定义的行为。

```cpp
struct S  
{  
    void mem_fn();  
};  
void f()  
{  
    S *s;  
    s->mem_fn();  
}  
```

**合规代码**

在这个合规解决方案中，在调用`S::mem_fn()` 函数之前，确保对象的指针内存已分配。

```cpp
struct S  
{  
    void mem_fn();  
};  
void f()  
{  
    S *s = new S;  
    s->mem_fn();  
    delete s;  
}  
```

**<font color=red>不合规代码</font>**

在这个不合规代码示例中，对象指针在其生命周期结束后被隐式转换为一个虚拟基类，会导致未定义的行为。

```cpp
struct B  
{  
};  
struct D1: virtual B  
{  
};  
struct D2: virtual B  
{  
};  
struct S: D1, D2  
{  
};  
void f(const B *b)  
{  
}  
void g()  
{  
    S *s = new S;  
// Use s  
    delete s;  
    f(s);  
} 
```

**NOTES**： 尽管实际上 `f()` 并没有使用这个对象，但它作为参数传递给 `f()` 足以触发未定义的行为。

**<font color=red>不合规代码</font>**

在这个不合规代码示例中， `f()` 返回局部变量的地址。当将生成的指针传递给 `h()` 时，对 `i` 的l**value­-to-­rvalue**的转换会导致未定义的行为。

```cpp
int *g()  
{  
    int i = 12;  
    return &i;  
}
void h(int *i);  
void f()  
{  
    int *i = g();  
    h(i);  
}     
```

**NOTES**： 从函数返回局部对象的指针，一些编译器会生成诊断信息。

**合规代码**

在这个合规解决方案中，从 `g()` 返回的局部变量具有静态存储属性，在 `f()` 内其生命周期都是有效的。

```cpp
int *g()  
{  
    static int i = 12;  
    return &i;  
}  
void h(int *i);  
void f()  
{  
    int *i = g();  
    h(i);  
} 
```

**<font color=red>不合规代码</font>**

`std::initializer_list<>`对象是从初始化列表构造的，就类似于实现分配了一个临时数组并将其传递给`std::initializer_list < >` 构造函数，这个临时数组与其他临时对象具有相同的生命周期。这个不合规代码示例中， `std::initializer_list <int >` 类型的成员变量在构造函数的**ctor­-initializer**中被初始化。在这些情况下，这个所谓的临时数组的生命周期在构造函数执行完结束，因此访问`std::initializer_list<int >`成员变量的任何元素都会导致未定义的行为。

```cpp
#include <initializer_list>  
#include <iostream>  
class C  
{  
    std::initializer_list<int> l;  
public:  
    C() :l{ 1, 2, 3 }  
    {  
    }  
    int first() const  
    {  
        return *l.begin();  
    }  
};  
void f()  
{  
    C c;  
    std::cout << c.first();  
}  
```

**合规代码**

在这个合规解决方案中，`std::initializer<int>`的成员变量被`std::vector<int>`代替，它将初始化列表中的元素复制到容器，而不是依赖于对临时数组的悬挂引用。

```cpp
#include <iostream>  
#include <vector>  
class C  
{  
    std::vector<int> l;  
public:  
    C() :   l{ 1, 2, 3 }  
    {  
    }  
    int first() const  
    {  
        return *l.begin();  
    }  
};  
void f()  
{  
    C c;  
    std::cout << c.first();  
}  
```

**<font color=red>不合规代码</font>**

在这个不合规代码示例中，**lambda**对象存储在函数对象中，在后面调用（执行**lambda**）以获取对值的常量引用。**lambda**对象返回一个**int**值，然后存储在一个临时的**int**对象中，该对象被绑定到函数对象`const int&` 的返回值类型。但是，临时对象的生命周期，不会超过函数对象被调用的返回值，当访问结果值时会导致未定义的行为。

```cpp
#include <functional>  
void f()  
{  
    auto l = [](const int &j)  
    {   return j;};  
    std::function<const int&(const int &)> fn(l);  
    int i = 42;  
    int j = fn(i);  
}
```

**合规代码**

这个合规解决方案中，`std::function`对象返回一个**int**而不是`const int&`，确保该值被赋值，而不是绑定到一个临时引用。另一种解决方案是直接调用**lambda**，而不是通过`std::function <>` 对象。

```cpp
#include <functional>  
void f()  
{  
    auto l = [](const int &j)  
    {   return j;};  
    std::function<int(const int &)> fn(l);  
    int i = 42;  
    int j = fn(i);  
}  
```

### EXP57-CPP不要强制转换或删除指向不完整类的指针

引用不完全类类型的对象，也称为前向声明，是一种常见的做法。

但是以下两种情况，不能使用不完全类类型：

- 尝试删除指向不完整类类型的对象的指针

- 不要尝试转换指向不完整类类型的对象的指针

**<font color=red>不合规代码</font>**

在这个不合规代码示例中，这个类试图实现**pimpl**的常规语法，但是删除了一个指向不

完整的类类型的指针。如果 `Body` 具有一个**non-trivial**析构函数，则会导致未定义的行为。

```cpp
class Handle  
{  
    class Body *impl; // Declaration of a pointer to an incomplete class  
public:  
    ~Handle()  
    {  
        delete impl;  
    } // Deletion of pointer to an incomplete class  
// ...  
};  
```

**合规代码（delete）**

在这个合规解放方案中，将`impl`的删除移动到定义`Body`代码之后，使其删除时知道该指针的完整类型。

```cpp
class Handle  
{  
    class Body *impl; // Declaration of a pointer to an incomplete class  
public:  
    ~Handle();  
// ...  
};  
// Elsewhere  
class Body  
{ /* ... */  
};  
Handle::~Handle()  
{  
    delete impl;  
}     
```

### EXP62-CPP不要访问对象中非对象值部分的bits

C++中窄字符类型（**char**, **signed char**, **unsigned char**)及特定平台的整数类型，访问对象值表示的任何**bits**都是明确定义的，即可以通过它的**bits**来访问或者修改对象。其他类型（比如类），其对象可能由构成对象值的**bits**及其他**bits**构成（例如：虚表指针，填充字节，不具有访问权限的字段等），对该类对象，访问非对象值外的**bits**，在不同编译器或平台下，可能导致不确定行为。

**<font color=red>不合规代码</font>**

如下代码中，通过`std::memcmp`比较两个`S`对象，C++标准规定，类可以通过填充数据保证在存储器中正确对齐，填充内容及填充大小与编译器相关。当比较内容为非`S`对象值**bits**时，可能导致不确定行为。

```cpp
#include <cstring>  
struct S  
{  
    unsigned char buffType;  
    int size;  
};  
void f(const S &s1, const S &s2)  
{  
    if (!std::memcmp(&s1, &s2, sizeof(S)))  
    {  
        // ...  
    }
}
```

**合规代码**

在如下代码中，通过重载操作符 `==()` 来进行对象值的比较。

```cpp
struct S  
{  
    unsigned char buffType;  
    int size;  
    friend bool operator==(const S &lhs, const S &rhs)  
    {  
        return lhs.buffType == rhs.buffType && lhs.size == rhs.size;  
    }  
};  
void f(const S &s1, const S &s2)  
{  
    if (s1 == s2)  
    {  
        // ...  
    }  
} 
```

**<font color=red>不合规代码</font>**

如下代码中， `std::memset()`用于初始化对象`s`。由于类中存在虚函数，编译器会在对象s中增加虚表指针， `std::memset`会把虚表指针也同时初始化，调用对象的虚方法时，可能导致不确定行为。

```cpp
#include <cstring>  
struct S  
{  
    int i, j, k;  
// ...  
    virtual void f();  
};  
void f()  
{  
    S *s = new S;  
// ...  
    std::memset(s, 0, sizeof(S));  
// ...  
    s->f(); // undefined behavior  
}  
```

**合规代码**

如下代码中，`S`的数据成员被通过`clear()`显式初始化，而不是调用`std::memset()` 初始化。

```cpp
struct S  
{  
    int i, j, k;  
// ...  
    virtual void f();  
    void clear()  
    {  
        i = j = k = 0;  
    }  
};  
void f()  
{  
    S *s = new S;  
// ...  
    s->clear();  
// ...  
    s->f(); // ok  
}  
```

## 整型

### INT50-CPP 不要做超过枚举值范围的枚举类型转换

C+ + 中枚举有两种形式：基础类型固定的领域枚举，基础类型可能被修改的非领域枚举。可以通过枚举类型表示值的范围，也可以包括未指定枚举值的范围。为了避免对未确定的值进行操作，被转换的算术值必须在枚举可以表示的值得范围内。当动态检查超出范围值时，必须在转换表达式之前进行检查。

**<font color=red>不合规代码（边界检查）</font>**

本例中尝试检查给定值是否在枚举值可接受的范围内。但是它是在转换为枚举类型后执行的，可能无法表示给定的整数值。在二进制补码系统上，由枚举类型表示值的有效范围是`[0..3]`，因此如果该范围外的值传递给`f()`，则向枚举类型转换将导致未指定的值，并且在if语句中使用该值会导致未定义行为。

```cpp
enum EnumType  
{  
    First, Second, Third  
};  
void f(int intVar)  
{  
    EnumType enumVar = static_cast<EnumType>(intVar);  
    if (enumVar < First || enumVar > Third)  
    {  
// 捕获错误  
    }  
}  
```

**合规的代码示例（边界检查）**

此解决方案的检查在执行转换之前通过枚举类型表示该值，以确保转换不会导致未指定的值。它通过将转换的值限制为具有特性枚举值的值来实现。

```cpp
enum EnumType  
{  
    First, Second, Third  
};  
void f(int intVar)  
{  
    if (intVar < First || intVar > Third)  
    {  
        // 捕获错误  
    }  
    EnumType enumVar = static_cast<EnumType>(intVar);  
} 
```

**合规的代码示例（领域枚举）（C++11支持）**

此解决方案使用领域枚举，默认情况下是具有固定的底层使用**int**类型，允许将参数中的任何值转换为有效的枚举值。它不会将转换的值限制为具有特定枚举器值的转换值，但可以按照之前的合规解决方案所示进行操作。

```cpp
enum class EnumType  
{  
    First, Second, Third  
};  
void f(int intVar)  
{  
    EnumType enumVar = static_cast<EnumType>(intVar);  
}  
```

**合规的代码示例（固定的非领域枚举）（C++11支持）**

与前一个合规的代码示例类似，此解决方案使用未限定的枚举，但提供了一个固定的底层**int**类型，允许将参数中的任何值转换为有效的枚举值。

```cpp
enum EnumType : int  
{  
        First, Second, Third  
};  
void f(int intVar)  
{  
    EnumType enumVar = static_cast<EnumType>(intVar);  
}  
```

虽然类似于之前的合规解决方案，但是该解决方案与不合规的代码示例之间的不同之处在于枚举器值以代码表示，允许隐式转换。 先前的合规解决方案需要嵌套的名称说明符来标识枚举器（例如，`EnumType::First`），并且不会将枚举器值隐式转换为**int**。与不合规的代码示例一样，此解决方案不允许嵌套的名称说明符，并将枚举器值隐式转换为**int**。

## 内存管理

### MEM50-CPP 禁止访问已释放的内存

指向已经释放的内存的指针称为悬挂指针。访问悬挂指针，其程序行为是未定义的。

**<font color=red>不合规代码new和delete</font>**

在该不规范的代码示例中，`s`在它的内存被释放后再解引用。

```cpp
#include <new>  
struct S  
{  
    void f();  
};  
void g() noexcept(false)  
{  
    S *s = new S;  
    // ...  
    delete s;  
    // ...  
    s->f();  
} 
```

**合规代码(new和delete)**

在合规代码示例中，动态分配的内存直到不再使用时才被释放。

```cpp
#include <new>  
struct S  
{  
    void f();  
};  
void g() noexcept(false)  
{  
    S *s = new S;  
    // ...  
    s->f();  
    delete s;  
}  
```

**规范代码（自动存储期）**

尽最大可能，用自动存储期代替动态存储器。因为变量 `s` 在函数 `g()` 的作用域外不需要存活，在此合规代码示例中，采用自动存储器限制函数 `g()` 作用域内变量 `s` 的生存期。

```cpp
struct S  
{  
    void f();  
};  
void g()  
{  
    S s;  
    // ...  
    s.f();  
} 
```

**<font color=red>不合规代码(std::unique_ptr)</font>**

在此不合规代码示例中，由 `buff` 动态分配的内存，当对象在析构函数中隐式释放之后又被再次访问。

```cpp
#include <iostream>  
#include <memory>  
#include <cstring>  
int main(int argc, const char *argv[])  
{  
    const char *s = "";  
    if (argc > 1)  
    {  
        enum  
        {  
            BufferSize = 32  
        };  
        try  
        {  
            std::unique_ptr<char[]> buff(new char[BufferSize]);  
            std::memset(buff.get(), 0, BufferSize);  
// ...  
            s = std::strncpy(buff.get(), argv[1], BufferSize - 1);  
        } catch (std::bad_alloc &)  
        {  
// Handle error  
        }  
    }  
    std::cout << s << std::endl;  
}  
```

**合规代码(std::unique_ptr)**

在合规代码中， `buff`对象的生命周期延长，使得内存可用。

```cpp
#include <iostream>  
#include <memory>  
#include <cstring>  
int main(int argc, const char *argv[])  
{  
    std::unique_ptr<char[]> buff;  
    const char *s = "";  
    if (argc > 1)  
    {  
        enum  
        {  
            BufferSize = 32  
        };  
        try  
        {  
            buff.reset(new char[BufferSize]);  
            std::memset(buff.get(), 0, BufferSize);  
            // ...  
            s = std::strncpy(buff.get(), argv[1], BufferSize - 1);  
        } catch (std::bad_alloc &)  
        {  
            // Handle error  
        }  
    }  
    std::cout << s << std::endl;  
} 
```

**合规代码**

在该合规代码示例中，使用`std::string`类型的自动存储期变量来代替`std::unique_ptr<char[]>`，既降低了复杂性，又提高了安全性。

```cpp
#include <iostream>  
#include <string>  
int main(int argc, const char *argv[])  
{  
    std::string str;  
    if (argc > 1)  
    {  
        str = argv[1];  
    }  
    std::cout << str << std::endl;  
}   
```

**<font color=red>不合规代码(std::string::c_str())</font>**

在该不合规代码示例中，`std::string::c_str()`的调用发生在一个临时的`std::string`对象上。一旦该临时的`std::string`对象在赋值表达式的末尾被销毁，将会使指针指向已释放的内存，从而导致访问该指针的元素时出现未定义的行为。

```cpp
#include <string>  
std::string str_func();  
void display_string(const char *);  
void f()  
{  
    const char *str = str_func().c_str();  
    display_string(str); /* Undefined behavior */  
}  
```

**合规代码(std::string::c_str())**

在该合规代码中，函数`str_func`返回的字符串的本地副本，可以确保在调用`display_string()` 时字符串str仍然有效。

```cpp
#include <string>  
std::string str_func();  
void display_string(const char *s);  
void f()  
{  
    std::string str = str_func();  
    const char *cstr = str.c_str();  
    display_string(cstr); /* ok */  
}
```

**<font color=red>不合规代码</font>**

在该不合规代码示例中，尝试通过对 `operator new()` 的调用来分配零字节的内存。如果此请求成功，则需要`operator new()`返回非空指针，但是根据C++规范，尝试通过该指针操作内存是未定义行为。

```cpp
#include <new>  
void f() noexcept(false)  
{  
    unsigned char *ptr = static_cast<unsigned char *>(::operator new(0));  
    *ptr = 0;  
// ...  
    ::operator delete(ptr);  
} 
```

**合规代码**

在该合规代码中，程序员打算分配一个**unsigned char**对象，则使用new而不是直接调用`operator new()` 。

```cpp
void f() noexcept(false)  
{  
    unsigned char *ptr = new unsigned char;  
    *ptr = 0;  
// ...  
    delete ptr;  
}  
```

**合规代码**

如果程序员打算分配0字节的内存（可能获得一个唯一的指针值，它不能被程序中的任何其他指针重复使用，直到它被正确释放），那么推荐的解决方案是将`ptr`声明为**void***，而不是通过一致的实现来解引用。

```cpp
void f() noexcept(false)  
{  
    void *ptr = ::operator new(0);  
	// ...  
    ::operator delete(ptr);  
}  
```

### MEM52-CPP 检测并捕捉内存分配错误

默认的内存分配操作`::operator new(std::size_t)`分配失败后，会抛出一个`std::bad_alloc`异常。因此，你不需要去校验调用`::operator new(std::size_t)`的结果是否为`nullptr`。还有一种没有异常抛出的形式，例如`::operatornew(std::size_t, const std::nothrow_t &)`分配失败后，不会抛出异常，但是会把返回值置为`nullptr`。同样的行为也会发生在`operator new[]`上。此外，默认的分配器对象(`std::allocator`)使用`::operator new(std::size_t)`去分配，显得更加简单。

```cpp
T *p1 = new T; // Throws std::bad_alloc if allocation fails
T *p2 = new (std::nothrow) T; // Returns nullptr if allocation fails
T *p3 = new T[1]; // Throws std::bad_alloc if the allocation fails
T *p4 = new (std::nothrow) T[1]; // Returns nullptr if the allocation fails
```

与此同时，当传给`new`的`size`参数为负数或者过大时，`operator new []` 抛出类型为 `std::bad_array_new_length`的错误，该异常是`std::bad_alloc`的子类。当使用不抛异常的形式，那么在使用指针时检查返回值是否为`nullptr` 将是非常必要的。

**<font color=red>不合规代码</font>**

在该不合规代码中，使用`::operator new[](std::size_t)`创建一个**int**数组，分配的结果并没有校验。函数被标记为**nothrow**，需要调用者确保该函数不会抛出任何异常。因为`::operator new[](std::size_t)` 在分配失败时会抛出异常，它可能会导致程序的异常退出。

```cpp
#include <cstring>  
void f(const int *array, std::size_t size) noexcept  
{  
    int *copy = new int[size];  
    std::memcpy(copy, array, size * sizeof(*copy));  
	// ...  
    delete[] copy;  
}  
```

**合规代码（std::nothrow)**

当使用`std::nothrow`时，`new`操作符返回一个空指针或指向已分配空间的指针。始终测试返回的指针，以确保在引用该指针之前它不为`nullptr`。

```cpp
#include <cstring>  
#include <new>  
void f(const int *array, std::size_t size) noexcept  
{  
    int *copy = new (std::nothrow) int[size];  
    if (!copy)  
    {  
	// Handle error  
        return;  
    }  
    std::memcpy(copy, array, size * sizeof(*copy));  
	// ...  
    delete[] copy;  
}    
```

**合规代码（std::bad_alloc)**

当没有充足的内存分配时，还有一种选择，可以使用不带`std::nothrow`的`::operator new[]`，替代捕获`std::bad_alloc`异常。

```cpp
#include <cstring>  
#include <new>  
void f(const int *array, std::size_t size) noexcept  
{  
    int *copy;  
    try  
    {  
        copy = new int[size];  
    } catch (std::bad_alloc)  
    {  
	// Handle error  
        return;  
    }  
	// At this point, copy has been initialized to allocated memory  
    std::memcpy(copy, array, size * sizeof(*copy));  
	// ...  
    delete[] copy;  
}
```

**合规代码（noexcept(false)）**

如果一个函数像这样设计：希望函数调用者来捕获异常，此时正确的做法是，可以显式的标记该函数可能会返回异常。但是这种做法没有强制要求，因为没有**noexcept**标识符的函数都默认可以抛出异常。

```cpp
#include <cstring>  
void f(const int *array, std::size_t size) noexcept(false)  
{  
    int *copy = new int[size];  
	// If the allocation fails, it will throw an exception which the caller  
	// will have to handle.  
    std::memcpy(copy, array, size * sizeof(*copy));  
	// ...  
    delete[] copy;  
}  
```

### MEM53-CPP 手动管理对象的生命周期时，显式的构造和析构对象

在C++中，对象的动态创建包括两个阶段：第一个阶段负责分配足够的内存来存储对象，第二个阶段负责对象的类型初始化新分配的内存块。相似的，在C++中，动态创建的对象，其析构同样包括两个阶段：第一个阶段是负责根据对象类型销毁对象，第二个阶段是负责回收对象使用的内存。

当手工管理一个对象的生命周期，需要调用构造函数去初始化一个对象的生命周期；相似的，调用析构函数去终止一个对象的生命周期。使用一个在生命周期之外的对象是未定义行为。一个对象的创建可以显式的使用**placement new**来调用，对于对象分配器可以调用`construct()`函数进行创建。一个对象可以使用显式的析构函数调用来销毁，对于对象分配器可以调用`destory()` 函数来销毁。

**<font color=red>不合规代码</font>**

在该不合规代码例子中，一个具有非默认构造的类（因为存在一个用户自定义的构造函数）使用`std::malloc()` 创建对象，但是这个对象的构造函数未被调用，随后当通过`s­>f()`调用访问时将导致未定义的行为。

```cpp
#include <cstdlib>  
struct S  
{  
    S();  
    void f();  
};  
void g()  
{  
    S *s = static_cast<S *>(std::malloc(sizeof(S)));  
    s->f();  
    std::free(s);  
}  
```

**合规代码**

在该合规代码例子中，构造函数和析构函数都是显式调用。

```cpp
#include <cstdlib>  
#include <new>  
struct S  
{  
    S();  
    void f();  
};  
void g()  
{  
    void *ptr = std::malloc(sizeof(S));  
    S *s = new (ptr) S;  
    s->f();  
    s->~S();  
    std::free(ptr);  
}  
```

**<font color=red>不合规代码</font>**

在该不合规代码示例中，一个自定义容器类使用一个对象分配器获取任意元素的存储。当使用`copy_elements()` 函数时，假定使用拷贝构造的元素移动到新分配的存储空间，这个例子的错误在于没有显式的调用默认构造函数。如果这样的一个元素调用了它的`operator[]()`方法，它会在类型**T**上发生未定义行为。

```cpp
#include <memory>  
template<typename T, typename Alloc = std::allocator<T>>  
class Container  
{  
    T *underlyingStorage;  
    size_t numElements;  
    void copy_elements(T *from, T *to, size_t count);  
public:  
    void reserve(size_t count)  
    {  
        if (count > numElements)  
        {  
            Alloc alloc;  
            T *p = alloc.allocate(count); // Throws on failure  
            try  
            {  
                copy_elements(underlyingStorage, p, numElements);  
            } catch (...)  
            {  
                alloc.deallocate(p, count);  
                throw;  
            }  
            underlyingStorage = p;  
        }  
        numElements = count;  
    }  
    T &operator[](size_t idx)  
    {  
        return underlyingStorage[idx];  
    }  
    const T &operator[](size_t idx) const  
    {  
        return underlyingStorage[idx];  
    }  
};   
```

**合规代码**

在该合规代码示例中，所有的元素通过显式的调用拷贝构造或者默认构造函数进行了初始化.

```cpp
#include <memory>  
template<typename T, typename Alloc = std::allocator<T>>  
class Container  
{  
    T *underlyingStorage;  
    size_t numElements;  
    void copy_elements(T *from, T *to, size_t count);  
public:  
    void reserve(size_t count)  
    {  
        if (count > numElements)  
        {  
            Alloc alloc;  
            T *p = alloc.allocate(count); // Throws on failure  
            try  
            {  
                copy_elements(underlyingStorage, p, numElements);  
                for (size_t i = numElements; i < count; ++i)  
                {  
                    alloc.construct(&p[i]);  
                }  
            } catch (...)  
            {  
                alloc.deallocate(p, count);  
                throw;  
            }  
            underlyingStorage = p;  
        }  
        numElements = count;  
    }  
    T &operator[](size_t idx)  
    {  
        return underlyingStorage[idx];  
    }  
    const T &operator[](size_t idx) const  
    {  
        return underlyingStorage[idx];  
    }  
};      
```

## 面向对象编程

### OOP50-CPP 禁止在构造函数或析构函数中调用虚函数

当在对象构造或者析构期间，不要在构造函数或者析构函数中直接或间接调用虚函数。因为对象是按基类到子类的顺序构造的，在构造期间尝试从基类中调用子类的函数是相当危险的。此时，子类还没有机会去完成资源的初始化；如果在构造函数中调用虚函数，那么调用将不会发生在子类上。

同样地，对象析构的顺序与构造的顺序相反。当在子类的析构函数中调用虚函数，则有可能非法获取已经释放了的资源。

**<font color=red>不合规代码</font>**

在此处的不合规代码中，基类尝试在构造函数和析构函数中分别调用`seize`与`release`的虚函数。但是，`B::B()`构造函数实际上调用了`B::seize()`，而不是`D::seize()`。同样地，`B::~B()`析构函数调用了`B::release()`，而不是`D::release()`。

```cpp
struct B  
{  
    B()  
    {  
        seize();  
    }  
    virtual ~B()  
    {  
        release();  
    }  
protected:  
    virtual void seize();  
    virtual void release();  
};  
struct D: B  
{  
    virtual ~D() = default;  
protected:  
    void seize() override  
    {  
        B::seize();  
// Get derived resources...  
    }  
    void release() override  
    {  
// Release derived resources...  
        B::release();  
    }  
};
```

**合规代码**

在此处的合规代码中，构造函数和析构函数调用了非虚的、私有的成员函数(以**mine**为后缀)，替代原来的虚函数调用，结果每个类各自承担所持有的资源的分配和释放的职责。

```cpp
class B  
{  
    void seize_mine();  
    void release_mine();  
public:  
    B()  
    {  
        seize_mine();  
    }  
    virtual ~B()  
    {  
        release_mine();  
    }  
protected:  
    virtual void seize()  
    {  
        seize_mine();  
    }  
    virtual void release()  
    {  
        release_mine();  
    }  
};  
class D: public B  
{  
    void seize_mine();  
    void release_mine();  
public:  
    D()  
    {  
        seize_mine();  
    }  
    virtual ~D()  
    {  
        release_mine();  
    }  
protected:  
    void seize() override  
    {  
        B::seize();  
        seize_mine();  
    }  
    void release() override  
    {  
        release_mine();  
        B::release();  
    }  
};     
```

**例外**

存在一些合理的场景，允许在构造函数中通过显式地指定类的方式来调用虚函数(不是纯虚的)。

- **情况1:** 通过显式的类标识符明确地告诉代码维护者，此处期待完成在构造函数或析构函数中函数的静态调用。

  ```cpp
  struct A  
  {  
      A()  
      {  
  		// f();   // WRONG!  
          A::f();   // Okay  
      }  
      virtual void f();  
  };
  ```

- **情况2**:可以在构造函数或析构函数中调用一个**final**修饰的虚函数。

  ```cpp
  struct A  
  {  
      A();  
      virtual void f();  
  };  
  struct B: A  
  {  
      B() : A()  
      {  
          f();  // Okay  
      }  
      void f() override final;  
  };
  ```

- **情况3**: 同样地，当一个类被修饰为**final**时，可以在其构造函数或析构函数中调用虚函数。

  ```cpp
  struct A  
  {  
      A();  
      virtual void f();  
  };  
  struct B final : A  
  {  
      B() : A()  
      {  
          f();  // Okay  
      }  
      void f() override;  
  };  
  ```

在其他场景，`f ()`必须使用**final override**修饰，保证函数调用行为的一致性。

### OOP51-CPP 禁止切割子类对象

当子类继承父类，子类对象一般会附加其他成员变量。当以值的方式赋值或拷贝子类对象到父类对象时，这些附加的成员变量将不会被拷贝，这个行为通常称为对象切割。

禁止使用子类对象初始化一个父类对象，除非通过引用，指针，或者智能指针的抽象(例如`std::unique_ptr`，或者`std::shared_ptr`)。

**<font color=red>不合规代码</font>**

在此不合规代码中，子类`Manager`对象通过值的方式传递给一个接受父类`Employee`的函数中。最终，`Manager` 对象被切割，当调用`print()`函数时，导致信息丢失。

```cpp
#include <iostream>  
#include <string>  
class Employee  
{  
    std::string name;  
protected:  
    virtual void print(std::ostream &os) const  
    {  
        os << "Employee: " << get_name() << std::endl;  
    }  
public:  
    Employee(const std::string &name) :  
            name(name)  
    {  
    }  
    const std::string &get_name() const  
    {  
        return name;  
    }  
    friend std::ostream &operator<<(std::ostream &os, const Employee &e)  
    {  
        e.print(os);  
        return os;  
    }  
};  
class Manager: public Employee  
{  
    Employee assistant;  
protected:  
    void print(std::ostream &os) const override  
    {  
        os << "Manager: " << get_name() << std::endl;  
        os << "Assistant: " << std::endl << "\t" << get_assistant()  
                << std::endl;  
    }  
public:  
    Manager(const std::string &name, const Employee &assistant) :  
            Employee(name), assistant(assistant)  
{}  
    const Employee &get_assistant() const  
    {  
        return assistant;  
    }  
};  
  
void f(Employee e)  
{  
    std::cout << e;  
}  
int main()  
{  
    Employee coder("Joe Smith");  
    Employee typist("Bill Jones");  
    Manager designer("Jane Doe", typist);  
    f(coder);  
    f(typist);  
    f(designer);  
}
```

当f()传递参数`designer`时，`f()`的参数将被切割，并导致信息丢失。当打印对象`e`时，`Employee::print()`被调用，而不是`Manager::print()`，其运行结果如下：

```shell
Employee: Jane Doe
```

**合规代码(引用)**

存在一个改进的方案，使用引用替代指针，在`f()`实现里可以消除空指针的保护。

```cpp
// ... Remainder of code unchanged ...  
void f(const Employee &e)  
{  
    std::cout << e;  
}  
int main()  
{  
    Employee coder("Joe Smith");  
    Employee typist("Bill Jones");  
    Manager designer("Jane Doe", typist);  
    f(coder);  
    f(typist);  
    f(designer);  
}  
```

**合规代码(Noncopyable)**

在本合规代码中，通过继承**Noncopyable**抑制对象拷贝构造的能力，避免不经意地发生对象切割的问题。但是，这个解决方案也限制了`Manager`对象拷贝构造 `Employee` 对象的能力，其微妙地改变了类层次的语义关系。

```cpp
#include <iostream>  
#include <string>  
class Noncopyable  
{  
    Noncopyable(const Noncopyable &) = delete;  
    void operator=(const Noncopyable &) = delete;  
protected:  
    Noncopyable() = default;  
};  
class Employee: Noncopyable  
{  
// Remainder of the definition is unchanged.  
    std::string name;  
protected:  
    virtual void print(std::ostream &os) const  
    {  
        os << "Employee: " << get_name() << std::endl;  
    }  
public:  
    Employee(const std::string &name) :  
            name(name)  
    {  
    }  
    const std::string &get_name() const  
    {  
        return name;  
    }  
    friend std::ostream &operator<<(std::ostream &os, const Employee &e)  
    {  
        e.print(os);  
        return os;  
    }  
};  
class Manager: public Employee  
{  
    const Employee &assistant; // Note: The definition of Employee has been modified.  
// Remainder of the definition is unchanged.  
protected:  
    void print(std::ostream &os) const override  
    {  
        os << "Manager: " << get_name() << std::endl;  
        os << "Assistant: " << std::endl << "\t" << get_assistant()  
                << std::endl;  
    }  
public:  
    Manager(const std::string &name, const Employee &assistant) : Employee(name), assi  
    stant(assistant)  
    {}  
    const Employee &get_assistant() const  
    {  
        return assistant;  
    }  
};  
// If f() were declared as accepting an Employee, the program would be  
// ill-formed because Employee cannot be copy-initialized.  
void f(const Employee &e)  
{  
    std::cout << e;  
}  
int main()  
{  
    Employee coder("Joe Smith");  
    Employee typist("Bill Jones");  
    Manager designer("Jane Doe", typist);  
    f(coder);  
    f(typist);  
    f(designer);  
}  
```

**<font color=red>不合规代码</font>**

在此不合规代码中，使用了上述合规代码中`Employee`和`Manager`的类定义，并尝试缓存`Employee`对象到 `std::vector`容器中去。但是，`std::vector`要求列表元素类型是同质的，其结果将导致对象切割的问题。

```cpp
#include <iostream>  
#include <string>  
#include <vector>  
void f(const std::vector<Employee> &v)  
{  
    for (const auto &e : v)  
    {  
        std::cout << e;  
    }  
}  
int main()  
{  
    Employee typist("Joe Smith");  
    std::vector<Employee> v  
    { typist, Employee("Bill Jones"), Manager("Jane Doe", typist) };  
    f(v);  
}  
```

**合规代码**

在此合规代码中，使用了持有`std::unique_ptr`元素类型的**vector**类型，避免了对象切割问题。

```cpp
#include <iostream>  
#include <memory>  
#include <string>  
#include <vector>  
void f(const std::vector<std::unique_ptr<Employee>> &v)  
{  
    for (const auto &e : v)  
    {  
        std::cout << *e;  
    }  
}  
int main()  
{  
    std::vector < std::unique_ptr < Employee >> v;  
    v.emplace_back(new Employee("Joe Smith"));  
    v.emplace_back(new Employee("Bill Jones"));  
    v.emplace_back(new Manager("Jane Doe", *v.front()));  
    f (v); 
}  
```

### OOP52-CPP 禁止删除没有虚拟析构函数的多态对象

当父类没有定义虚拟析构函数时，尝试使用指向父类的指针删除子类对象将导致未定义的行为。

**<font color=red>不合规代码</font>**

在此不合规代码中，`b`是一个多态指针，其静态类型为`Base*` ，而其动态类型为`Derived*` 。因为`Base`未定义虚拟的析构函数，因此当`b`被删除时，其行为是未定义。

```cpp
struct Base  
{
    virtual void f();  
};  
struct Derived: Base  
{  
};  
void f()  
{  
    Base *b = new Derived();  
	// ...  
    delete b;  
}  
```

**<font color=red>不合规代码</font>**

在此不合规代码中，使用智能指针代替原生的指针类型。因为`std::unique_ptr`默认的析构函数将会`delete`内部持有的原生指针对象，其程序行为与上例类同。

```cpp
#include <memory>  
struct Base  
{  
    virtual void f();  
};  
struct Derived: Base  
{  
};  
void f()  
{  
    std::unique_ptr<Base> b = std::make_unique<Derived()>();  
}  
```

**合规代码**

在此合规代码中，父类显式地声明了虚拟析构函数，保证了`delete`多态操作的行为是良好定义的。

```cpp
struct Base  
{  
    virtual ~Base() = default;  
    virtual void f();  
};  
struct Derived: Base  
{  
};  
void f()  
{  
    Base *b = new Derived();  
	// ...  
    delete b;  
}  
```

### OOP53-CPP 规范化成员初始化列表的顺序

成员初始化的顺序与成员初始化列表指定的顺序无关。如果成员初始化未规范化，将导致未定义的行为，例如读取未初始化的内存。因此，务必需要规范化成员初始化列表的顺序：

- 首先，直接父类按照父类定义列表的顺序进行初始化；

- 然后，非静态成员变量按照类定义的顺序进行初始化。

**<font color=red>不合规代码</font>**

在此不合规代码中，`C::C()` 的初始化列表先尝试初始化`someVal`，然后初始化`dependsOnSomeVal`。其中`dependsOnSomeVal`的初始化依赖于`someVal`。因为成员变量声明的顺序与初始化列表成员的顺序不匹配，尝试读取`someVal`的值，并对`dependsOnSomeVal`进行初始化，将得到不确定的值。

```cpp
class C  
{  
    int dependsOnSomeVal;  
    int someVal;  
public:  
    C(int val) :  
            someVal(val), dependsOnSomeVal(someVal + 1)  
    {  
    }  
}; 
```

**合规代码**

在本合规代码中，改变了成员变量的声明顺序，以便保证其顺序与构造函数的初始化列表的顺序保持一致。

```cpp
class C  
{  
    int someVal;  
    int dependsOnSomeVal;  
public:  
    C(int val) :  
            someVal(val), dependsOnSomeVal(someVal + 1)  
    {  
    }  
};  
```

**<font color=red>不合规代码</font>**

在该不合规代码中，子类`D`尝试初始化基类`B1`时，其初始化值取自另外一个基类`B2`。但是，根据子类`D` 的基类定义列表，`B1`在`B2`之前初始化，这将导致程序行为是未定义的。

```cpp
class B1  
{  
    int val;  
public:  
    B1(int val) :  
            val(val)  
    {  
    }  
};  
class B2  
{  
    int otherVal;  
public:  
    B2(int otherVal) :  
            otherVal(otherVal)  
    {  
    }  
    int get_other_val() const  
    {  
        return otherVal;  
    }  
};  
class D: B1, B2  
{  
public:  
    D(int a) :  
            B2(a), B1(get_other_val())  
    {  
    }  
};
```

**合规代码**

在此合规代码中，两个基类使用来自子类构造函数的参数，并取得相同的值。其初始化列表不依赖与基类的初始化顺序。

```cpp
class B1  
{  
    int val;  
public:  
    B1(int val) : val(val)  
    {  
    }  
};  
class B2  
{  
    int otherVal;  
public:  
    B2(int otherVal) : otherVal(otherVal)  
    {  
    }  
};  
class D: B1, B2  
{  
public:  
    D(int a) :  
            B1(a), B2(a)  
    {  
    }  
};  
```

### OOP58-CPP 拷贝操作不允许修改原对象

拷贝操作(拷贝构造函数和拷贝赋值运算符重载)用于从原对象拷贝特征属性到目标对象，其目标对象成为原对象的一个副本。在理想的情况下，拷贝操作应该有一个惯用的签名。拷贝构造函数，即`T(const T&)`；及其拷贝赋值运算符重载，即`T& operator=(const T&)`；如果拷贝构造函数和拷贝赋值重载运算符不使用惯用的签名，则不符合的**CopyAssignable**概念的要求，如此将导致类型与标准库通用函数功能的不兼容。

当实现一个拷贝操作时，对于任何源对象的操作数或全局信息，不要改变任何外部可观察的成员。外部可观察成员包括但不限于参与比较或相等操作的成员，通过公共**API**公开其值的成员，及其全局变量。

在**C++11**中，引入了新的智能指针类型`std::unique_ptr`。 没有通过拷贝操作修改原对象，而是通过显式地删除了拷贝构造函数及其拷贝赋值运算符重载，并使用移动构造函数及其移动赋值运算符重载代替。

**<font color=red>不合规代码</font>**

在此不合规代码中， `A`的拷贝操作通过将原对象的成员变量置位为0，以此修改了原对象的状态。当调用 `std::fill()` 时，第一个元素拷贝了`obj` 值，此时`obj.m`值为12，然后被置位为0。随后的9份拷贝中，其值都为0。

```cpp
#include <algorithm>  
#include <vector>  
class A  
{  
    mutable int m;  
public:  
    A() :  
            m(0)  
    {  
    }  
    explicit A(int m) :  
            m(m)  
    {  
    }  
    A(const A &other) :  
            m(other.m)  
    {  
        other.m = 0;  
    }  
    A& operator=(const A &other)  
    {  
        if (&other != this)  
        {  
            m = other.m;  
            other.m = 0;  
        }  
        return *this;  
    }  
    int get_m() const  
    {  
        return m;  
    }  
};  
void f()  
{  
    std::vector<A> v{10};  
    A obj(12);  
    std::fill(v.begin(), v.end(), obj);  
}
```

**合规代码**

在此合规代码中，对`A`的拷贝操作并未修改原对象，因此保证了**vector**包含了`obj`价的多份拷贝。与此相反， `A` 也提供了移动操作，以便安全地修改原对象。

```cpp
#include <algorithm>  
#include <vector>  
class A  
{  
    int m;  
public:  
    A() :  
            m(0)  
    {  
    }  
    explicit A(int m) :  
            m(m)  
    {  
    }  
    A(const A &other) :  
            m(other.m)  
    {  
    }  
    A(A &&other) :  
            m(other.m)  
    {  
        other.m = 0;  
    }  
    A& operator=(const A &other)  
    {  
        if (&other != this)  
        {  
            m = other.m;  
        }  
        return *this;  
    }  
    A& operator=(A &&other)  
    {  
        m = other.m;  
        other.m = 0;  
        return *this;  
    }  
    int get_m() const  
    {  
        return m;  
    }  
};  
void f()  
{  
    std::vector<A> v{10};  
    A obj(12);  
    std::fill(v.begin(), v.end(), obj);  
}
```

## 杂项

### MSC52-CPP 带返回值的函数必须在每个路径中返回返回值

一个带返回值的函数必须在所有代码路径上返回返回值；否则，其行为未定义。C++标准**ISO/IEC 14882­-2014**第二章[**stmt.return**]明确提出：

控制越过函数语句末端，其等价于返回空值；当该函数需要返回值时，其行为未定义。

**<font color=red>不合规代码</font>**

在该代码中，遗漏了另外一种可能的场景：当输入为正数时返回该输入的值，所以不是所有的代码路径都返回了值。

```cpp
int absolute_value(int a)  
{  
    if (a < 0)  
    {  
        return -a;  
    }  
}
```

**合规代码**

在该代码中，所有代码路径都返回了值。

```cpp
int absolute_value(int a)  
{  
    if (a < 0)  
    {  
        return -a;  
    }  
    return a;  
} 
```

**<font color=red>不合规代码</font>**

在该代码中，**function­-try­-block**处理程序并没有返回值，当异常抛出时，其行为未定义。

```cpp
#include <vector>  
std::size_t f(std::vector<int> &v, std::size_t s)  
{  
    try  
    {  
        v.resize(s);  
        return s;  
    }  
    catch (...)  
    {  
    }  
}
```

**合规代码**

在这个正例中，**function­-try­-block**异常处理程序返回了值。

```cpp
#include <vector>  
std::size_t f(std::vector<int> &v, std::size_t s)  
{  
    try  
    {  
        v.resize(s);  
        return s;  
    } catch (...)  
    {  
        return 0;  
    }  
}  
```

# 本文件评审、修正记录

| 文件名称 | C++安全编码规范                              |               |               |        |
| -------- | ------------------------------------------------------------ | ------------- | ------------- | ------ |
| 序号     | 流程                                                         | 拟制人/审核人 | 拟制/审核时间 | 版本号 |
| 1        | 规范发布                                    | 于光杰        | 2019/5/15   | V1.0   |
| 2        | INT30-C、INT31-C和INT32-C等规则中-和*符号修复，ARR39-C删除有关int大小的无效说明 | 于光杰        | 2022/5/9   | V1.0.1   |
| 3        | 发布 | C/C++规范组        | 2022/5/12   | V1.1   |
| 4        | INT30-C和INT31-C规则中管道符号 \| 修复  | 于光杰        | 2026/4/30   | V1.1.1   |
| 5        | 发布  | C/C++规范组        | 2026/5/25   | V1.2  |
