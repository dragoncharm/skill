![image](uploads/110959/0b5b95a4-7c50-44c5-9b0b-46965729e76d/image.png)

### 适用对象

Objective-C 开发人员

### 目的

为了持续、稳定地开发出高质量，健壮的软件系统，为了保证团队中成员的编码质量，特制定本文档。用于规范团队内部开发过程，增加程序的健壮性，便于后续测试及代码维护，最终提高公司软件产品的生产力。

### 编程规范

#### 基本原则

##### 代码结构

代码结构需要保持以下两种特性:

- 可读性可维护性
- 一致性

##### 代码语言

应该使用美式英语(US-EN)，不是用英式英语或者拼音。

正例

```c
UIColor *myColor = [UIColor whiteColor];
```

`反例`

```c
UIColor *myColour = [UIColor whiteColor];
UIColor *yanse = [UIColor whiteColor];
```

##### 代码文件

单个.m文件内部方法数不允许超过25个。
单个.m文件内部行数不允许超过800行。

##### 代码布局风格

1. 【建议】关于View的布局，纯代码推荐Masonry，代码的可读性好，使用可视化编辑建议使用Xib，不推荐使用storyBoard。
2. 【建议】默认采⽤ `@property` 来定义属性
3. 【建议】所有的属性都使用getter和setter

正例

```c
#pragma mark----------------------------------getter and setter

- (UIButton *)configBtn {
    return nil;
}
- (UITableView *)tableView {
    return nil;
}
```

4. 【建议】关于继承，建议能不用尽量不⽤，建议使用别的⽅案代替，比如：组合
5. 【建议】每⼀个delegate都把对应的protocol名字带上，delegate⽅法不要到处乱写，写到⼀块区域里面去，⽐如UITableViewDelegate的⽅法集就写上#pragma mark - UITableViewDelegate，看的⾮常清晰

正例

```c
#pragma mark----------------------------------UITableViewDelegate

- (NSInteger)tableView:(UITableView *)tableView indentationLevelForRowAtIndexPath:(NSIndexPath *)indexPath {
    return 0;
}
-(UITableViewCell *)objectInConfigBtnAtIndex:(NSUInteger)index {
    return nil;
}

#pragma mark----------------------------------CustomDelegate
/*
⾃⼰的代理
*/
```

#### 变量、表达式、函数

##### 【强制】使用装箱表达，可以用字面量语法，迁移到object-c的新的表达方式

> [UseBoxedExpression](http://docs.oclint.org/en/stable/rules/migration.html#useboxedexpression)

正例

```c
// good
void aMethod()
{
    NSNumber *fortyTwo = @(43 - 1);

    NSString *env = @(getenv("PATH"));
}
```

`反例`

```c
// bad
void aMethod()
{
    NSNumber *fortyTwo = [NSNumber numberWithInt:(43 - 1)];

    NSString *env = [NSString stringWithUTF8String:getenv("PATH")];
}
```

##### 【强制】使用容器的literal语法，可以迁移到object-c的新的表达方式

> [UseContainerLiteral](http://docs.oclint.org/en/stable/rules/migration.html#usecontainerliteral)

正例

```c
// good
void aMethod()
{
    NSArray *a = @[ @1, @2, @3 ];

    NSDictionary *d = @{ @1 : @2, @3 : @4 };
}
```

`反例`

```c
// bad
void aMethod()
{
    NSArray *a = [NSArray arrayWithObjects:@1, @2, @3, nil];

    NSDictionary *d = [NSDictionary dictionaryWithObjects:@[@2,@4] forKeys:@[@1,@3]];
}
```

##### 【强制】使用number的literal语法，可以迁移到object-c的新的表达方式

> [UseNumberLiteral](http://docs.oclint.org/en/stable/rules/migration.html#usenumberliteral)

正例

```c
// good
void aMethod()
{
    NSNumber *fortyTwo = @42;

    NSNumber *yesBool = @YES;
}
```

`反例`

```c
// bad
void aMethod()
{
    NSNumber *fortyTwo = [NSNumber numberWithInt:42];

    NSNumber *yesBool = [NSNumber numberWithBool:YES];
}
```

##### 【强制】使用下标访问对象，可以迁移到object-c的新的表达方式

> [UseObjectSubscripting](http://docs.oclint.org/en/stable/rules/migration.html#useobjectsubscripting)

正例

```c
// good
void aMethod(NSArray *a, NSDictionary *d)
{
    id item = a[0];

    id item = d[@1];
}
```

`反例`

```c
// bad
void aMethod(NSArray *a, NSDictionary *d)
{
    id item = [a objectAtIndex:0];

    id item = [d objectForKey:@1];
}
```

##### 【强制】禁止变量名过长（oclint 阈值：20）

> [LongVariableName](http://docs.oclint.org/en/stable/rules/naming.html#longvariablename)

`反例`

```c
// bad
void aMethod()
{
    int reallyReallyLongIntegerName;
}
```

##### 【强制】禁止变量名过短（oclint 阈值：3）

> [ShortVariableName](http://docs.oclint.org/en/stable/rules/naming.html#shortvariablename)

`反例`

```c
//bad
void aMethod(int i)  // i is short
{
    int ii;          // ii is short
}
```

##### 【建议】使用描述性的方法名和变量名（不要毫无意义的名字）

正例

```c
// good
UIButton *settingsButton;
```

`反例`

```c
// bad
UIButton *setBut;
```

##### 【建议】常量应该以小驼峰法命名，并以相关类名作为前缀

正例

```c
// good
static const NSTimeInterval ZOCSignInViewControllerFadeOutAnimationDuration = 0.4;
```

`反例`

```c
// bad
static const NSTimeInterval fadeOutTime = 0.4;
```

##### 【建议】使⽤常量来代替字符串字⾯值和数字，这样能够⽅便复用，⽽且可以快速修改⽽不需要查找和替换。常量应该⽤ static 声明为静态常量，⽽不要⽤ #define ，除非它明确的作为⼀个宏来使⽤。

正例

```c
// good
static NSString * const ZOCCacheControllerDidClearCacheNotification = @"ZOCCacheControllerDidClearCacheNotification";
static const CGFloat ZOCImageThumbnailHeight = 50.0f;
```

`反例`

```c
// bad
#define CompanyName @"Apple Inc."
#define magicNumber 42
```

##### 【建议】⽅法名与方法类型 ( - / + 符号)之间应该以空格间隔。⽅法段之间也应该以空格间隔(以符合 Apple 风格)。参数前应该总是有⼀个描述性的关键词。

尽可能少用 "and" 这个词。它不应该用来阐明有多个参数，⽐如下⾯的 initWithWidth:height:

正例

```c
// good
- (void)setExampleText:(NSString *)text image:(UIImage *)image;
- (void)sendAction:(SEL)aSelector to:(id)anObject forAllCells: (BOOL)flag;
- (id)viewWithTag:(NSInteger)tag;
- (instancetype)initWithWidth:(CGFloat)width height:(CGFloat)height;
```

`反例`

```c
// bad
- (void)setT:(NSString *)text i:(UIImage *)image;
- (void)sendAction:(SEL)aSelector :(id)anObject :(BOOL)flag;
- (id)taggedView:(NSInteger)tag;
- (instancetype)initWithWidth:(CGFloat)width andHeight: (CGFloat)height;
- (instancetype)initWith:(int)width and:(int)height;  // Never do this.
```

##### 【建议】常量应该在头文件中以这样的形式暴露给外部，并在实现⽂件中为它赋值

正例

```c
extern NSString *const ZOCCacheControllerDidClearCacheNotification
```

##### 【建议】使⽤字⾯值来创建不可变的 NSString , NSDictionary , NSArray , 和 NSNumber 对象。注意不要将 nil 传进 NSArray 和 NSDictionary 里，因为这样会导致崩溃。（对第1、2条的补充）

正例

```c
// good
NSArray *names = @[@"Brian", @"Matt", @"Chris", @"Alex", @"Steve", @"Paul"];
NSDictionary *productManagers = @{@"iPhone" : @"Kate", @"iPad" : @"Kamal", @"Mobile Web" : @"Bill"};
NSNumber *shouldUseLiterals = @YES;
NSNumber *buildingZIPCode = @10018;
```

`反例`

```c
// bad
NSArray *names = [NSArray arrayWithObjects:@"Brian", @"Matt", @"Chris", @"Alex", @"Steve", @"Paul", nil];
NSDictionary *productManagers = [NSDictionary dictionaryWithObjectsAndKeys: @"Kate", @"iPhone", @"Kamal", @"iPad", @"Bill", @"Mobile Web", nil];
NSNumber *shouldUseLiterals = [NSNumber numberWithBool:YES];
NSNumber *buildingZIPCode = [NSNumber numberWithInteger:10018];
```

如果要⽤到这些类的可变副本，我们推荐使用 NSMutableArray , NSMutableString 这样的类，避免如下使用的方式：

`反例`

```c
NSMutableArray *aMutableArray = [@[] mutableCopy];
```

##### 【建议】图⽚名称必须要全部为小写，并且名称要是能表示图片使⽤含义的

正例

```c
// good
home_title_btn_search
```

`反例`

```c
// bad
Search_Icon
icon1
```

#### if条件语句

##### 【强制】条件语句体必须被⼤括号包围。

正例

```c
// good
if (!error) {
    return success;
}
```

`反例`

```c
// bad
if (!error)
    return success;
//或者
 if (!error) return success;
```

##### 【强制】不要使⽤尤达表达式。尤达表达式是指，拿⼀个常量去和变量比较，而不是拿变量去 和常量比较。

正例

```c
// good
if ([myValue isEqual:@42]) { ... }
```

`反例`

```c
// bad
if ([@42 isEqual:myValue]) { ... }
```

##### 【强制】禁用条件语句中的位操作符

> [BitwiseOperatorInConditional](http://docs.oclint.org/en/stable/rules/basic.html#bitwiseoperatorinconditional)

`反例`

```c
// bad
void example(int a, int b)
{
    if (a | b)
    {
    }
    if (a & b)
    {
    }
}
```

##### 【强制】错误的空检查会让程序崩溃

> [BrokenNullCheck](http://docs.oclint.org/en/stable/rules/basic.html#brokennullcheck)

`反例`

```c
// bad
void m(A *a, B *b)
{
    if (a != NULL || a->bar(b))
    {
    }

    if (a == NULL && a->bar(b))
    {
    }
}
```

##### 【强制】nil检查条件，某些情况会返回相反的结果

> [BrokenNilCheck](http://docs.oclint.org/en/stable/rules/basic.html#brokennilcheck)

`反例`

```c
// bad
+ (void)compare:(A *)obj1 withOther:(A *)obj2
{
    if (obj1 || [obj1 isEqualTo:obj2])
    {
    }

    if (!obj1 && ![obj1 isEqualTo:obj2])
    {
    }
}
```

##### 【强制】奇偶数检查（x % 2 == 1检查奇数，对负数无效，需要使用 x & 1 == 1或者 x % 2 != 0来代替）

> [BrokenOddnessCheck](http://docs.oclint.org/en/stable/rules/basic.html#brokenoddnesscheck)

正例

```c
// good
void example()
{
    if (x & 1 == 1)
    {
    }

    if (x % 2 != 0)
    {
    }
}
```

`反例`

```c
// bad
void example()
{
    if (x % 2 == 1)
    {
    }

    if (foo() % 2 == 1)
    {
    }
}
```

##### 【强制】可以合并的连续两个if,应该合并，提高代码的可读性

> [CollapsibleIfStatements](http://docs.oclint.org/en/stable/rules/basic.html#collapsibleifstatements)

正例

```c
// good
void example(bool x, bool y)
{
    if (x && y)
    {
        foo();
    }
}
```

`反例`

```c
// bad
void example(bool x, bool y)
{
    if (x)              // these two if statements can be
    {
        if (y)          // combined to if (x && y)
        {
            foo();
        }
    }
}
```

##### 【强制】禁止 if 表达式的条件是已经确定的 true 或者 false

> [ConstantIfExpression](http://docs.oclint.org/en/stable/rules/basic.html#constantifexpression)

`反例`

```c
// bad
void example()
{
    if (true)       // always true
    {
        foo();
    }
    if (1 == 0)     // always false
    {
        bar();
    }
}
```

##### 【强制】Null检查位置错误，空检查应该在其他运算之前（在OC中向一个空指针发送消息并不会发生什么，但是在C或者C++中可能会引起crash，同时可能会造成代码阅读的困惑）

> [MisplacedNullCheck](http://docs.oclint.org/en/stable/rules/basic.html#misplacednullcheck)

正例

```c
// good
void m(A *a, B *b)
{
    if (a != NULL && a->bar(b))
    {
    }

    if (!a || a->bar(b))
    {
    }
}
```

`反例`

```c
// bad
void m(A *a, B *b)
{
    if (a->bar(b) && a != NULL) // bad
    {
    }

    if (a->bar(b) || !a)        // bad
    {
    }
}
```

##### 【强制】nil检查放错地方了（在Objective-C中，发送消息给nil指针什么都不做。但是代码读者可能会对放错位置的nil检查感到困惑）

> [MisplacedNilCheck](http://docs.oclint.org/en/stable/rules/basic.html#misplacednilcheck)

`正例`

```c
// good
+ (void)compare:(A *)obj1 withOther:(A *)obj2
{
    if (obj1 && [obj1 isEqualTo:obj2])
    {
    }

    if (obj1 == nil || ![obj1 isEqualTo:obj2])
    {
    }
}
```

`反例`

```c
// bad
+ (void)compare:(A *)obj1 withOther:(A *)obj2
{
    if ([obj1 isEqualTo:obj2] && obj1)
    {
    }

    if (![obj1 isEqualTo:obj2] || obj1 == nil)
    {
    }
}
```

##### 【强制】禁止使用反向逻辑，这让程序不容易理解，一般是指用（！a）而不是（a）

> [InvertedLogic](http://docs.oclint.org/en/stable/rules/convention.html#invertedlogic)

正例

```c
// good
int example(int a)
{
    int i;
    f (a == 0)
    {
        i = 0;
    }
    else
    {
        i = 1;
    }

    return i ? 1 : -1;
}
```

`反例`

```c
// bad
int example(int a)
{
    int i;
    if (a != 0)
    {
        i = 1;
    }
    else
    {
        i = 0;
    }

    return !i ? -1 : 1;
}
```

##### 【强制】更早return比较好（意思是，有其他出口，可以先return掉时，先执行其他出口，再继续代码）

> [PreferEarlyExit](http://docs.oclint.org/en/stable/rules/convention.html#preferearlyexit)

正例

```c
// good
int *doSomething(int a) {
  if (foo(a)) {
    return 0;
  }

  if (!bar(a)) {
    return 0;
  }

  if (!doOtherThing(a)) {
    return 0;
  }

  // ... some long code ....
}
```

`反例`

```c
// bad
int *doSomething(int a) {
  if (!foo(a) && bar(a) && doOtherThing(a)) {
    // ... some really long code ....
  }

  return 0;
}
```

##### 【强制】禁止空的else，在if中有操作，else中却是空的，此时else可以被安全移除

> [EmptyElseBlock](http://docs.oclint.org/en/stable/rules/empty.html#emptyelseblock)

`反例`

```c
// bad
int example(int a)
{
    if (1)
    {
        return a + 1;
    }
    else                // empty else statement, can be safely removed
    {
    }
}
```

##### 【强制】禁止空的if，if中代码为空

> [EmptyIfStatement](http://docs.oclint.org/en/stable/rules/empty.html#emptyifstatement)

`反例`

```c
// bad
void example(int a)
{
    if (a == 1)                  // empty if statement
    {
    }
}
```

##### 【强制】禁止多余的运算条件

> [RedundantConditionalOperator](http://docs.oclint.org/en/stable/rules/redundant.html#redundantconditionaloperator)

- true表达式得到结果为true，false对应的表达式结果为false;
- true 对应 false，false 对应 true;
- true，false 对应的结果是一样的.

正例

```c
// good
void example(int a, int b, int c)
{
    bool b1 = a > b;
    bool b2 = !(a > b);
    int i1 = 1;
    float f1 = 1.0;
    int i2 = c;
}
```

`反例`

```c
// bad
void example(int a, int b, int c)
{
    bool b1 = a > b ? true : false;     // true/false: bool b1 = a > b;
    bool b2 = a > b ? false : true;     // false/true: bool b2 = !(a > b);
    int i1 = a > b ? 1 : 1;             // same constant: int i1 = 1;
    float f1 = a > b ? 1.0 : 1.00;      // equally constant: float f1 = 1.0;
    int i2 = a > b ? c : c;             // same variable: int i2 = c;
}
```

##### 【强制】禁止多余的if语句

[RedundantIfStatement](http://docs.oclint.org/en/stable/rules/redundant.html#redundantifstatement)

正例

```c
// good
bool example(int a, int b)
{
    return a == b;
}
```

`反例`

```c
// bad
bool example(int a, int b)
{
    if (a == b)             // this if statement is redundant
    {
        return true;
    }
    else
    {
        return false;
    }                       // the entire method can be simplified to return a == b;
}
```

##### 【强制】对于复杂的 if 子句，把它们提取出来赋给⼀个 BOOL 变量

正例

```c
// good
BOOL nameContainsSwift = [sessionName containsString:@"Swift"];
BOOL isCurrentYear = [sessionDateCompontents year] == 2014;
BOOL isSwiftSession = nameContainsSwift && isCurrentYear;
if (isSwiftSession) {
    // Do something very cool
}
```

#### switch...case

##### 【强制】一个全覆盖的switch语句，不应该有默认值设置default语句

> [UnnecessaryDefaultStatement](http://docs.oclint.org/en/stable/rules/convention.html#unnecessarydefaultstatement)

正例

```c
typedef enum {
    value1 = 0,
    value2 = 1
} eValues;

// good
void aMethod(eValues a)
{
    switch(a)
    {
        case value1:
            break;
        case value2:
            break;
    }
}
```

`反例`

```c
typedef enum {
    value1 = 0,
    value2 = 1
} eValues;

// bad
void aMethod(eValues a)
{
    switch(a)
    {
        case value1:
            break;
        case value2:
            break;
        default:          // this break is obsolete because all
            break;        // values of variable a are already covered.
    }
}
```

##### 【强制】switch中default放在Switch的最后一行

> [MisplacedDefaultLabel](http://docs.oclint.org/en/stable/rules/convention.html#misplaceddefaultlabel)

正例

```c
// good
void example(int a)
{
    switch (a) {
        case 1:
            break;
        case 2:
            break;
        default:
            break;
    }
}
```

`反例`

```c
// bad
void example(int a)
{
    switch (a) {
        case 1:
            break;
        default:  // the default case should be last
            break;
        case 2:
            break;
    }
}
```

##### 【强制】禁止switch语句没有break（在switch中如果缺少break很容易引入bug）

> [MissingBreakInSwitchStatement](http://docs.oclint.org/en/stable/rules/convention.html#missingbreakinswitchstatement)

正例

```c
// good
void example(int a)
{
    switch (a) {
        case 1:
            break;
        case 2:
            // do something
            break;
        default:
            break;
    }
}
```

`反例`

```c
// bad
void example(int a)
{
    switch (a) {
        case 1:
            break;
        case 2:
            // do something
        default:
            break;
    }
}
```

##### 【强制】禁止switch中条件有非case条件

> [NonCaseLabelInSwitchStatement](http://docs.oclint.org/en/stable/rules/convention.html#noncaselabelinswitchstatement)

正例

```c
// good
void example(int a)
{
    switch (a) {
        case 1:
            break;
        case 2:
            break;
        default:
            break;
    }
}
```

`反例`

```c
// bad
void example(int a)
{
    switch (a) {
        case 1:
            break;
        label1:     // label in a switch statement in really confusing
            break;
        default:
            break;
    }
}
```

##### 【强制】switch（指非全覆盖）应该有default

> [MissingDefaultStatement](http://docs.oclint.org/en/stable/rules/convention.html#missingdefaultstatement)

正例

```c
// good
void example(int a)
{
    switch (a) {
        case 1:
            break;
        case 2:
            break;
        default:
            break;
    }
}
```

`反例`

```c
// bad
void example(int a)
{
    switch (a) {
        case 1:
            break;
        case 2:
            break;
        // should have a default
    }
}
```

##### 【强制】switch分支较少时，应该用if代替

> [TooFewBranchesInSwitchStatement](http://docs.oclint.org/en/stable/rules/convention.html#toofewbranchesinswitchstatement)

正例

```c
// good
void example(int a)
{
    if(a) {
        // doSomething
    } else {
        // doSomething
    }
}
```

`反例`

```c
// bad
void example(int a)
{
    switch (a) {
        case 1:
            break;
        default:
            break;
    } // Better to use an if statement and check if variable a equals 1.
}
```

##### 【强制】禁止空的switch，switch中代码为空

> [EmptySwitchStatement](http://docs.oclint.org/en/stable/rules/empty.html#emptyswitchstatement)

`反例`

```c
// bad
void example(int i)
{
    switch (i)              // empty switch statement
    {
    }
}
```

##### 【强制】case语句如果是单行，⼤括号不必要，多行则必须添加大括号

正例

```c
// good
switch (condition) {
    case 1:
        // ...
        break;
    case 2: {
        // ...
        // Multi-line example using braces
        break;
    }
    case 3:
        // ...
        break;
    default:
        // ...
        break;
}
```

`反例`

```c
// bad
switch (condition) {
    case 1:
        // ...
        break;
    case 2:
        // ...
        // Multi-line example should using braces
        break;
    case 3:
        // ...
        break;
    default:
        // ...
        break;
}
```

#### for、do...while循环

##### 【强制】一些情况下for循环应该转换为while，使代码更简洁

> [ForLoopShouldBeWhileLoop](http://docs.oclint.org/en/stable/rules/basic.html#forloopshouldbewhileloop)

正例

```c
// good
void example(int a)
{
    do
    {
        foo(a);
    } while (a<100);
}
```

`反例`

```c
// bad
void example(int a)
{
    for (; a < 100;)
    {
        foo(a);
    }
}
```

##### 【强制】禁止增量词混乱（如果不是因为笔误写错了，那么这种混乱的写法容易造成代码阅读的问题）

> [JumbledIncrementer](http://docs.oclint.org/en/stable/rules/basic.html#jumbledincrementer)

正例

```c
// good
void aMethod(int a) {
    for (int i = 0; i < a; i++) {
        for (int j = 0; j < a; j++) {
        }
    }
}
```

`反例`

```c
// bad
void aMethod(int a) {
    for (int i = 0; i < a; i++) {
        for (int j = 0; j < a; i++) { // references both 'i' and 'j'
        }
    }
}
```

##### 【强制】不要在for循环或者其他循环语句的末尾使用break

> [AvoidBranchingStatementAsLastInLoop](http://docs.oclint.org/en/stable/rules/convention.html#avoidbranchingstatementaslastinloop)

正例

```c
// good
void example()
{
    for (int i = 0; i < 10; i++)
    {
        if (foo(i))
        {
            continue;
        }
    }
}
```

`反例`

```c
// bad
void example()
{
    for (int i = 0; i < 10; i++)
    {
        if (foo(i))
        {
            continue;
        }
        break;      // this break is confusing
    }
}
```

##### 【强制】禁止空的Do while，在do-while循环中没有做任何事情

> [EmptyDoWhileStatement](http://docs.oclint.org/en/stable/rules/empty.html#emptydowhilestatement)

`反例`

```c
// bad
void example()
{
    do
    {                           // empty do-while statement
    } while(1);
}
```

##### 【强制】禁止空的for，for循环为空

> [EmptyForStatement](http://docs.oclint.org/en/stable/rules/empty.html#emptyforstatement)

`反例`

```c
// bad
void example(NSArray *array)
{
    for (;;)                // empty for statement
    {
    }

    for (id it in array)    // empty for-each statement
    {
    }
}
```

##### 【强制】禁止空的while，While循环中没有代码

> [EmptyWhileStatement](http://docs.oclint.org/en/stable/rules/empty.html#emptywhilestatement)

`反例`

```c
// bad
void example(int a)
{
    while(a--)              // empty while statement
    {
    }
}
```

#### 三元运算

##### 【强制】三元运算符要简洁的使用，不要嵌套使用

正例

```c
// good
result = a > b ? x : y;
```

`反例`

```c
// bad
result = a > b ? x = c > d ? c : d : y;
```

##### 【建议】当三元运算符的第二个参数(if 分支)返回与条件语句中已经检查的对象相同对象的时候，第二个参数可以省略

正例

```c
// good
result = object ? : [self createObject];
```

`反例`

```c
// bad
result = object ? object : [self createObject];
```

#### finally代码块

##### 【强制】禁止finally块中包含return

> [ReturnFromFinallyBlock](http://docs.oclint.org/en/stable/rules/basic.html#returnfromfinallyblock)

正例

```c
// good
void example()
{
    @try
    {
        foo();
    }
    @catch(id ex)
    {
        bar();
    }
    @finally
    {
        // doSomething
    }
}
```

`反例`

```c
// bad
void example()
{
    @try
    {
        foo();
    }
    @catch(id ex)
    {
        bar();
    }
    @finally
    {
        return;         // this can discard exceptions.
    }
}
```

##### 【强制】禁止从Finally块抛出异常，可能掩盖其他的错误

[ThrowExceptionFromFinallyBlock](http://docs.oclint.org/en/stable/rules/basic.html#throwexceptionfromfinallyblock)

`反例`

```c
// bad
void example()
{
    @try {;}
    @catch(id ex) {;}
    @finally {
        id ex1;
        @throw ex1;                              // this throws an exception
        NSException *ex2 = [NSException new];
        [ex2 raise];                             // this throws an exception, too
    }
}
```

##### 【强制】禁止空的finally，在@finally中没有进行任何操作

> [EmptyFinallyStatement](http://docs.oclint.org/en/stable/rules/empty.html#emptyfinallystatement)

`反例`

```c
// bad
void example()
{
    Foo *foo;
    @try
    {
        [foo bar];
    }
    @catch(NSException *e)
    {
        NSLog(@"Exception occurred: %@", [e description]);
    }
    @finally            // empty finally statement, probably forget to clean up?
    {
    }
}
```

#### try...catch 代码块

##### 【强制】禁止空的catch，一个异常exception被catch到了，但是却没有对此做任何操作

> [EmptyCatchStatement](http://docs.oclint.org/en/stable/rules/empty.html#emptycatchstatement)

正例

```c
// good
void example()
{
    try
    {
        int* m= new int[1000];
    }
    catch(...)
    {
        // need do something
    }
}
```

`反例`

```c
// bad
void example()
{
    try
    {
        int* m= new int[1000];
    }
    catch(...)                  // empty catch statement, this swallows an exception
    {
    }
}
```

##### 【强制】禁止空的try，try中代码为空

> [EmptyTryStatement](http://docs.oclint.org/en/stable/rules/empty.html#emptytrystatement)

`反例`

```c
// bad
void example()
{
    try                     // but this try statement is empty
    {
    }
    catch(...)
    {
        cout << "Exception is caught!";
    }
}
```

#### 枚举、闭包

##### 【强制】当使⽤ enum 的时候，使用固定类型定义 NS_ENUM()

正例

```c
// good
typedef NS_ENUM(NSUInteger, ZOCMachineState) {
    ZOCMachineStateNone,
    ZOCMachineStateIdle,
    ZOCMachineStateRunning,
    ZOCMachineStatePaused
};
```

##### 【建议】返回类型与  (^ 之间保留一个空格

##### 【建议】在参数列表中，每个参数之间保留一个空格

正例

```c
double (^multiplyTwoValues)(double, double);

^(double firstValue, double secondValue) {
    return firstValue * secondValue;
};
```

`反例`

```c
double(^multiplyTwoValues)(double,double);

^(double firstValue,double secondValue) {
    return firstValue * secondValue;
};
```

#### 类申明

- 在 `@interface`/`@implementation` 与类名之间保留一个空格
- 在类名与 `:` 之间，以及 `:` 与父类之间保留一个空格
- 在父类名于协议 `<` 之间保留一个空格
- 遵循多个协议以一个空格分隔
- 属性申明内部每个定义之前预留一个空格
- 属性申明结束与类型定义之间预留一个空格
- 属性类型定义与属性命名预留一个空格
- **属性申明 `@property` 与 `(`之间不保留空格**

正例

```c
@interface SDImageAWebPCoder : SDImageIOAnimatedCoder <SDProgressiveImageCoder, SDAnimatedImageCoder>

@property(nonatomic, class, readonly, nonnull) SDImageAWebPCoder *sharedCoder;

@end

@implementation SDImageAWebPCoder

@end
```

`反例`

```c
@interface   SDImageAWebPCoder:SDImageIOAnimatedCoder<SDProgressiveImageCoder,SDAnimatedImageCoder>

@property(nonatomic,class,readonly,nonnull)SDImageAWebPCoder*sharedCoder;

@end

@implementation    SDImageAWebPCoder

@end
```

#### 无效、无意义代码，或者未使用的代码

##### 【强制】禁止在 return, break, continue, and throw 之后写代码

> [DeadCode](http://docs.oclint.org/en/stable/rules/basic.html#deadcode)

正例

```c
// good
void example(id collection)
{
    for (id it in collection)
    {
        continue;
    }
    return;
}
```

`反例`

```c
// bad
void example(id collection)
{
    for (id it in collection)
    {
        continue;
        int i1;                 // dead code
    }
    return;
    int i2;                     // dead code
}
```

##### 【强制】禁止使用双重否定等没有意义的代码

> [DoubleNegative](http://docs.oclint.org/en/stable/rules/basic.html#doublenegative)

正例

```c
// good
void example()
{
    int b1 = 1;
}
```

`反例`

```c
// bad
void example()
{
    int b1 = !!1;
    int b2 = ~~1;
}
```

##### 【强制】禁止多余运算符，多余的运算符应该简化，便于阅读

> [MultipleUnaryOperator](http://docs.oclint.org/en/stable/rules/basic.html#multipleunaryoperator)

`反例`

```c
// bad
void example()
{
    int b = -(+(!(~1)));
}
```

##### 【强制】禁止定义多余的变量

> [RedundantLocalVariable](http://docs.oclint.org/en/stable/rules/redundant.html#redundantlocalvariable)

正例

```c
// good
int example(int a)
{
    return a * 2;
}
```

`反例`

```c
// bad
int example(int a)
{
    int b = a * 2;
    return b;   // variable b is returned immediately after its declaration,
}               // can be simplified to return a * 2;
```

##### 【强制】禁止多余的判空nil检查

> [RedundantNilCheck](http://docs.oclint.org/en/stable/rules/redundant.html#redundantnilcheck)

正例

```c
// good
+ (void)compare:(A *)obj1 withOther:(A *)obj2
{
    if ([obj1 isEqualTo:obj2])
    {
    }
}
```

`反例`

```c
// bad
+ (void)compare:(A *)obj1 withOther:(A *)obj2
{
    if (obj1 && [obj1 isEqualTo:obj2]) // if ([obj1 isEqualTo:obj2]) is okay
    {
    }
}
```

##### 【强制】禁止多余的else条件，当一个if语句有返回语句，那么else 语句就不是必要的。剩下的语句可以不再代码块中运行

> [UnnecessaryElseStatement](http://docs.oclint.org/en/stable/rules/redundant.html#unnecessaryelsestatement)

正例

```c
// good
bool example(int a)
{
    if (a == 1)
    {
        cout << "a is 1.";
        return true;
    }
    cout << "a is not 1."
}
```

`反例`

```c
// bad
bool example(int a)
{
    if (a == 1)
    {
        cout << "a is 1.";
        return true;
    }
    else
    {
        cout << "a is not 1."
    }
}
```

##### 【强制】禁止多余的dealloc，nil 检查，在Dealloc中(释放内存)不需要判空，就能Delete元素

> [UnnecessaryNullCheckForDealloc](http://docs.oclint.org/en/stable/rules/redundant.html#unnecessarynullcheckfordealloc)

正例

```c
// good
void m(char* c) {
    delete c;
}
```

`反例`

```c
// bad
void m(char* c) {
    if (c != nullptr) { // and be simplified to delete c;
        delete c;
    }
}
```

##### 【强制】禁止多余的括号

> [UselessParentheses](http://docs.oclint.org/en/stable/rules/redundant.html#uselessparentheses)

正例

```c
// good
int example(int a)
{
    int y = a + 1;
    if (y > 0)
    {
        return a;
    }
    return 0;
}
```

`反例`

```c
// bad
int example(int a)
{
    int y = (a + 1);
    if ((y > 0))
    {
        return a;
    }
    return (0);
}
```

##### 【强制】禁止没有使用的本地变量，声明了，却没有使用的本地变量

> [UnusedLocalVariable](http://docs.oclint.org/en/stable/rules/unused.html#unusedlocalvariable)

正例

```c
// good
int example(int a)
{
    int i;
    return i;
}
```

`反例`

```c
// bad
int example(int a)
{
    int i;          // variable i is declared, but not used
    return 0;
}
```

##### 【强制】禁止没有使用的方法参数

> [UnusedMethodParameter](http://docs.oclint.org/en/stable/rules/unused.html#unusedmethodparameter)

正例

```c
// good
int example(int a)
{
    return a+2;
}
```

`反例`

```c
// bad
int example(int a)  // parameter a is not used
{
    return 0;
}
```

#### 类

##### 【强制】如果重写 isEqual 方法，必须要实现 hash 方法

> [MissingHashMethod](http://docs.oclint.org/en/stable/rules/cocoa.html#missinghashmethod)

正例

```c
// good
@implementation BaseObject

- (BOOL)isEqual:(id)obj {
    return YES;
}

- (int)hash is missing {
    // do something
}

@end
```

`反例`

```c
// bad
@implementation BaseObject

- (BOOL)isEqual:(id)obj {
    return YES;
}

@end
```

##### 【强制】当一个类使用注解__attribute__((annotate("oclint:enforce[must call super]")))的时候, 他的所有实现（包括他自己和子类）都必须调用超类的实现

> [MissingCallToBaseMethod](http://docs.oclint.org/en/stable/rules/cocoa.html#missingcalltobasemethod)

正例

```c
@interface UIView (OCLintStaticChecks)
- (void)layoutSubviews __attribute__((annotate("oclint:enforce[must call super]")));
@end

@interface CustomView : UIView
@end

@implementation CustomView

// good
- (void)layoutSubviews {
    [super layoutSubviews];
}
@end
```

`反例`

```c
@interface UIView (OCLintStaticChecks)
- (void)layoutSubviews __attribute__((annotate("oclint:enforce[must call super]")));
@end

@interface CustomView : UIView
@end

@implementation CustomView

// bad
- (void)layoutSubviews {
    // do do do somthing
}
@end
```

##### 【强制】当一个方法标记__attribute__((annotate("oclint:enforce[prohibited call]")))注解,所有的引用都将被禁止。

> [CallingProhibitedMethod](http://docs.oclint.org/en/stable/rules/cocoa.html#callingprohibitedmethod)

`反例`

```c
//.h
@interface A : NSObject
- (void)foo __attribute__((annotate("oclint:enforce[prohibited call]")));
@end

//.m
@implementation A
- (void)foo {
}
- (void)bar {
    // bad 此处不可调用foo方法
    [self foo];
}
@end
```

##### 【强制】当一个方法声明含有attribute((annotate("oclint:enforce[protected method]")))时，只有它和它的子类可以调用，因为OC中没有Protected，可以用这种方式达到Protected效果

> [CallingProtectedMethod](http://docs.oclint.org/en/stable/rules/cocoa.html#callingprotectedmethod)

正例

```c
// good
@interface A : NSObject
- (void)foo __attribute__((annotate("oclint:enforce[protected method]")));
@end

@implementation A
- (void)bar {
    [self.a foo];
}
@end
```

`反例`

```c
// bad
@interface A : NSObject
- (void)foo __attribute__((annotate("oclint:enforce[protected method]")));
@end

@interface B : NSObject
@property (strong, nonatomic) A* a;
@end

@implementation B
- (void)bar {
    [self.a foo]; // calling protected method foo from outside A and its subclasses
}
@end
```

##### 【强制】子类必须实现父类的抽象方法

正例

```c
// good
// Parent.h
@interface Parent

- (void)anAbstractMethod __attribute__((annotate("oclint:enforce[subclass must implement]")));

@end

// Child.h
@interface Child : Parent
@end

// Child.m
@implementation Child

// Child, as a subclass of Parent, must implement anAbstractMethod
- (void)anAbstractMethod {}

@end
```

`反例`

```c
// bad
@interface Parent

- (void)anAbstractMethod __attribute__((annotate("oclint:enforce[subclass must implement]")));

@end

@interface Child : Parent
@end

@implementation Child
......
......
@end
```

##### 【强制】禁止类的行数过多（oclint 阈值：800）

> [LongClass](http://docs.oclint.org/en/stable/rules/size.html#longclass)

`反例`

```c
// bad
class Foo
{
    void bar()
    {
        // 1001 lines of code
    }
}
```

##### 【强制】禁止一个类定义太多的字段，表明它做了太多的事儿，应该去做抽象，重新设计（oclint 阈值：20）

> [TooManyFields](http://docs.oclint.org/en/stable/rules/size.html#toomanyfields)

`反例`

```c
// bad
class c
{
    int a, b;
    int c;
    // ...
    int l;
    int m, n;
    // ...
    int x, y, z;

    void m() {}
};
```

##### 【强制】禁止一个类有太多的方法，证明他做了太多的事儿，不利于理解。应该考虑重构（oclint 阈值：25）

> [TooManyMethods](http://docs.oclint.org/en/stable/rules/size.html#toomanymethods)

`反例`

```c
// bad
class c
{
    int a();
    int b();
    int c();
    // ...
    int l();
    int m();
    int n();
    // ...
    int x();
    int y();
    int z();
    int aa();
    int ab();
    int ac();
    int ad();
    int ae();
};
```

##### 【建议】类名应该以三个大写字⺟作为前缀(双字母前缀为 Apple 的类预留)，如ZOC，把说明性的部分放在前缀和⽗类名的在中间。

如果你有⼀个 `ZOCNetworkClient` 类，⼦类的名字会是 `ZOCTwitterNetworkClient` (注意 "Twitter" 在 "ZOC" 和 "NetworkClient" 之间)； 按照这个约定， 一个 `UIViewController` 的⼦类会是 `ZOCTimelineViewController`

#### Initializer 和 dealloc

将 dealloc ⽅法放在实现⽂件的最前面(直接在 `@synthesize` 以及 `@dynamic` 之后)， init 跟在 dealloc ⽅法后面。
如果有多个初始化⽅法， 指定初始化方法 (designated initializer) 应该放在最前面，间接初始化⽅法 (secondary initializer) 跟在后面，这样更有逻辑性。如今有了 ARC，dealloc ⽅法⼏乎不需要实现，不过把 init 和 dealloc 放在⼀起可以从视觉上强调它们是⼀对的。通常，在 init ⽅法中做的事情需要在 dealloc ⽅法中撤销。

##### 【建议】指定Designated 和 Secondary 初始化⽅法

Objective-C 有指定初始化方法(designated initializer)和间接(secondary initializer) 初始化方法的观念。 designated 初始化方法是提供所有的参数，secondary 初始化⽅法是一个或多个，并且提供⼀个或者更多的默认参数来调用 designated 初始化的初始化⽅法。

```c
@implementation ZOCEvent
- (instancetype)initWithTitle:(NSString *)title
                         date:(NSDate *)date
                     location:(CLLocation *)location
{
    self = [super init];
    if (self) {
        _title = title;
        _date = date;
        _location = location;
    }
    return self;
}

- (instancetype)initWithTitle:(NSString *)title
                         date:(NSDate *)date
{
    return [self initWithTitle:title date:date location:nil];
}

- (instancetype)initWithTitle:(NSString *)title
{
    return [self initWithTitle:title date:[NSDate date] location:nil];
}

@end
```

```c
- (instancetype)initWithTitle:(NSString *)title date:(NSDate *)date location:(CLLocation *)location
```

就是 designated 初始化方法，另外的两个是 secondary 初始化⽅法。因为它们仅仅是调用类实现的 designated 初始化⽅法

##### 【建议】使⽤ instancetype 来返回类实例

正例

```c
@interface ZOCPerson
+ (instancetype)personWithName:(NSString *)name;
@end
```

##### 【建议】如果可能，请尽量避免使用单例，⽽是依赖注⼊。 然⽽，如果⼀定要用，请使⽤⼀个线程安全的模式来创建共享的实例。对于 GCD，用 dispatch_once() 函数就可以咯。

```c
+ (instancetype)sharedInstance
{
    static id sharedInstance = nil;
    static dispatch_once_t onceToken = 0;
    dispatch_once(&onceToken, ^{
    sharedInstance = [[self alloc] init];
    });
    return sharedInstance;
}
```

使⽤ dispatch_once()，来控制代码同步，取代了原来的约定俗成的用法。

```c
+ (instancetype)sharedInstance
{
    static id sharedInstance;
    @synchronized(self) {
        if (sharedInstance == nil) {
            sharedInstance = [[MyClass alloc] init];
        }
    }
    return sharedInstance;
}
```

#### 属性

##### 【强制】属性应该尽可能描述性地命名，避免缩写，并且是⼩写字母开头的驼峰命名

##### 【建议】点符号，当使⽤ setter getter ⽅法的时候使用点符号。

正例

```c
// good
view.backgroundColor = [UIColor orangeColor];
[UIApplication sharedApplication].delegate;
```

`反例`

```c
// bad
[view setBackgroundColor:[UIColor orangeColor]];
UIApplication.sharedApplication.delegate;
```

##### 【建议】属性定义，按照下⾯的格式来定义属性

正例

```c
@property (nonatomic, readwrite, copy) NSString *name;
```

属性的参数应该按照下面的顺序排列: 原⼦性，读写 和 内存管理。

你必须使⽤ nonatomic ，除⾮特别需要的情况。在iOS中， atomic 带来的锁特别影响性能。

属性可以存储⼀个代码块。为了让它存活到定义的块的结束，必须使⽤ copy (block 最早在栈⾥面创建，使用 copy 让 block 拷贝到堆⾥面去)
为了完成一个共有的 getter 和⼀个私有的 setter，你应该声明公开的属性为 readonly 并且在类扩展中重新定义通用的属性为 readwrite 的

```c
//.h⽂件中
@interface MyClass : NSObject
@property (nonatomic, readonly, strong) NSObject *object; @end

//.m⽂件中
@interface MyClass ()
@property (nonatomic, readwrite, strong) NSObject *object; @end
@implementation MyClass
//Do Something cool
@end
```

描述 BOOL 属性的词如果是形容词，那么setter不应该带 is 前缀，但它对应的 getter 访问器应该带上这个前缀，如:

正例

```c
@property (assign, getter=isEditable) BOOL editable;
```

##### 【建议】私有属性应该定义在类的实现文件的类的扩展 (匿名的 category) 中。不允许在有名字的 category(如 ZOCPrivate )中定义私有属性，除⾮你扩展其他类。

正例

```c
@interface ZOCViewController ()
@property (nonatomic, strong) UIView *bannerView;
@end
```

##### 【强制】任何可以用⼀个可变的对象设置的((⽐如 NSString , NSArray , NSURLRequest )) 属性的内存管理类型必须是 copy 的。

避免暴露在公开的接口中可变的对象，提供可以只读的属性来返回你对象的不可变的副本。

```c
/* .h */
@property (nonatomic, readonly) NSArray *elements

/* .m */
- (NSArray *)elements {
    return [self.mutableElements copy];
}
```

##### 【建议】懒加载(Lazy Loading)使⽤以下模板:

```c
- (NSDateFormatter *)dateFormatter {
    if (!_dateFormatter) {
        _dateFormatter = [[NSDateFormatter alloc] init];
        NSLocale *enUSPOSIXLocale = [[NSLocale alloc] initWithLocaleIdentifier:@"en_US_POSIX"];
        [_dateFormatter setLocale:enUSPOSIXLocale];
        [_dateFormatter setDateFormat:@"yyyy-MM-dd'T'HH:mm:ss.SSS"];//毫秒是SSS，⽽而⾮非SSSSS
    }
    return _dateFormatter;
}
```

#### 函数方法

##### 【强制】禁止多个分支嵌套，比如一个函数有多少个分支(if, while,for,等等)

> [HighCyclomaticComplexity](http://docs.oclint.org/en/stable/rules/size.html#highcyclomaticcomplexity)

正例

```c
// good
void example1(int a, int b, int c)
{
    if (a == b)
    {
        if (b == c)
        {
        }
        else if (a == c)
        {
        }
        else
        {
        }
    }
}

void example2(int c)
{
    for (int i = 0; i < c; i++)
    {
    }
}

void example3(int c)
{
    switch(c)
    {
        case 1:
            break;
        case 2:
            break;
        default:
            break;
    }
}
```

`反例`

```c
// bad
void example(int a, int b, int c) // 1
{
    if (a == b)                   // 2
    {
        if (b == c)               // 3
        {
        }
        else if (a == c)          // 4
        {
        }
        else
        {
        }
    }
    for (int i = 0; i < c; i++)   // 5
    {
    }
    switch(c)
    {
        case 1:                   // 6
            break;
        case 2:                   // 7
            break;
        default:                  // 8
            break;
    }
}
```

##### 【强制】禁止过长的函数方法，一个方法不应该太长，太长的方法影响后续的阅读，应该将每个方法都去做一个简单的事（oclint 阈值：50）

> [LongMethod](http://docs.oclint.org/en/stable/rules/size.html#longmethod)

`反例`

```c
// bad
void example()
{
    cout << "hello world";
    cout << "hello world";
    // repeat 100 times
}
```

##### 【建议】禁止方法中某个代码块中代码行数过多（只统计有效的语句），查看代码块中代码是否能拆分，公共功能能否提供一个公共接口。空语句，空块，右括号或分号后的右括号会被忽略（oclint 阈值：30）

> [HighNcssMethod](http://docs.oclint.org/en/stable/rules/size.html#highncssmethod)

`反例`

```c
// bad
void example()          // 1
{
    if (1)              // 2
    {
    }
    else                // 3
    {
    }
    // do something  有效代码100 行
}
```

##### 【强制】禁止代码块嵌套过多（oclint 阈值：5）

> [DeepNestedBlock](http://docs.oclint.org/en/stable/rules/size.html#deepnestedblock)

正例

```c
// good
if (1)
{

}
```

`反例`

```c
// bad
if (1)
{               // 1
    {           // 2
        {       // 3
        }
    }
}
```

##### 【强制】禁止高复杂的方法，指一个方法中各种可能的执行路径总和（oclint 阈值：200）

> [HighNPathComplexity](http://docs.oclint.org/en/stable/rules/size.html#highnpathcomplexity)

`反例`

```c
// bad
void example()
{
    // 难以理解的复杂代码，各种判断等
}
```

##### 【强制】禁止一个方法中有过多参数，方法中有太多的参数是难以理解和后期维护的（oclint 阈值：10）

> [TooManyParameters](http://docs.oclint.org/en/stable/rules/size.html#toomanyparameters)

正例

```c
// good
void example(int a, int b)
{
}
```

`反例`

```c
// bad
void example(int a, int b, int c, int d, int e, int f,
    int g, int h, int i, int j, int k, int l)
{
}
```

##### 【建议】参数断⾔使⽤ NSParameterAssert() 来断⾔条件是否成立，或是抛出⼀个异常。

##### 【强制】永远不要在你的私有方法前加上 _  前缀。这个前缀是 Apple 保留的。不要冒重载苹果的私有⽅法的风险。

##### 【强制】使用 #pragma mark - 对.m文件内部函数进行归类。

正例

```c
#pragma mark - Lifecycle

- (instancetype)init {}
- (void)dealloc {}
- (void)viewDidLoad {}
- (void)viewWillAppear:(BOOL)animated {}
- (void)didReceiveMemoryWarning {}

#pragma mark - Custom Accessors

- (void)setCustomProperty:(id)value {}
- (id)customProperty {}

#pragma mark - IBActions

- (IBAction)submitData:(id)sender {}

#pragma mark - Public

- (void)publicMethod {}

#pragma mark - Private

- (void)privateMethod {}

#pragma mark - Protocol conformance
#pragma mark - UITextFieldDelegate
#pragma mark - UITableViewDataSource
#pragma mark - UITableViewDelegate

#pragma mark - NSCopying

- (id)copyWithZone:(NSZone *)zone {}

#pragma mark - NSObject

- (NSString *)description {}
```

##### 【强制】禁止使用goto语句（goto被认为是有风险的）

> [GotoStatement](http://docs.oclint.org/en/stable/rules/basic.html#gotostatement)

`反例`

```c
// bad
void example()
{
    A:
        a();
    goto A;     // Considered Harmful
}
```

##### 【强制】禁止在getter、setter和init方法之外分配synthesize ivar（意思是某些成员的初始化不在getter/setter或者init中，而在其他位置）

> [AssignIvarOutsideAccessors](http://docs.oclint.org/en/stable/rules/convention.html#assignivaroutsideaccessors)

`反例`

```c
@interface Foo : NSObject
{
    int _bar;
}
@property (assign, nonatomic) int bar;
@end
@implementation Foo
@synthesize bar = _bar;
- (void)doSomething {
    _bar = 3; // access _bar outside its getter, setter or init
}
@end
```

##### 【强制】禁止将值重新分配给参数，容易出问题

> [ParameterReassignment](http://docs.oclint.org/en/stable/rules/convention.html#parameterreassignment)

正例

```c
// good
void example(int a)
{
    if (a < 0)
    {
        int b = 0;
    }
}
```

`反例`

```c
// bad
void example(int a)
{
    if (a < 0)
    {
        a = 0; // reassign parameter a to 0
    }
}
```

##### 【强制】禁止一行代码过长，一行代码太长，非常不利于阅读和维护，应该将代码转换为多行（oclint 阈值：300）

> [LongLine](http://docs.oclint.org/en/stable/rules/size.html#longline)

`反例`

```c
// bad
void example()
{
    int a012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789;
}
```

##### 【强制】避免私有静态成员，破坏封装性

> [AvoidPrivateStaticMembers](http://docs.oclint.org/en/stable/rules/design.html#avoidprivatestaticmembers)

正例

```c
// good
class Foo
{
    int a;
}; 
class Bar
{
    int b();
}
```

`反例`

```c
// bad
class Foo
{
    static int a;       // static field
};
class Bar
{
    static int b();     // static method
}
```

#### Categories分类

##### 【强制】要在 category ⽅法前加上⾃己的⼩写前缀以及下划线

正例

```c
// good
@interface NSDate (ZOCTimeExtensions)
- (NSString *)zoc_timeAgoShort;
@end
```

`反例`

```c
// bad
@interface NSDate (ZOCTimeExtensions)
- (NSString *)timeAgoShort;
@end
```

##### 【强制】分类可以用来在头文件中定义⼀组功能相似的方法，参⻅NSDate，NSURLSession等

正例

```c
@interface NSDate : NSObject <NSCopying, NSSecureCoding>

@property (readonly) NSTimeInterval timeIntervalSinceReferenceDate;

@end

@interface NSDate (NSDateCreation)
+ (instancetype)date;
+ (instancetype)dateWithTimeIntervalSinceNow:(NSTimeInterval)secs;
+ (instancetype)dateWithTimeIntervalSinceReferenceDate: (NSTimeInterval)ti;
+ (instancetype)dateWithTimeIntervalSince1970:(NSTimeInterval)secs;
+ (instancetype)dateWithTimeInterval:(NSTimeInterval)secsToBeAdded sinceDate:(NSDate *)date;
// ...
@end
```

##### 【强制】禁止两个不同的category下有一个同名的方法

假设 CategoryA 的 funcA，CategoryB 的 funcA 都是很重要的业务代码必须要执行到，不然就会出bug，CategoryA 和 CategoryB 是两个业务团队写的，彼此不知道对方怎么命名，此时就会出bug了，还非常难调试

```c
// 主类
@interface OCCategoryMethodTest : NSObject
@end
@implementation OCCategoryMethodTest
@end

// CategoryA
@interface OCCategoryMethodTest (CategoryA)
- (void)funcA;
@end
@implementation OCCategoryMethodTest (CategoryA)
- (void)funcA {
    NSLog(@"Category A");
}
@end

// CategoryB
@interface OCCategoryMethodTest (CategoryB)
- (void)funcA;
@end
@implementation OCCategoryMethodTest (CategoryB)

// bad 与CategoryA中的方法同名了
- (void)funcA {
    NSLog(@"Category B");
}
@end


// 在另一个类中测试调用代码
OCCategoryMethodTest *test = [[OCCategoryMethodTest alloc] init];
[test funcA];    // 此处代码会打印什么结果呢？我这是 “Category B”
```

#### NSNotification

##### 【强制】定义 NSNotification 名称时，在公开的接口⽂件中将其声明为 extern 的， 并且在对应的实现⽂件⾥面定义。

正例

```c
// Foo.h
extern NSString * const ZOCFooDidBecomeBarNotification

// Foo.m
NSString * const ZOCFooDidBecomeBarNotification = @"ZOCFooDidBecomeBarNotification";
```

#### 美化代码

##### 【建议】缩进使⽤ 4 个空格，不要使用 tab 键

##### 【建议】⽅法的⼤括号和其他的⼤括号( if / else / switch / while 等) 总是在同⼀行开始，在新起⼀⾏结束。

正例

```c
// good
if (user.isHappy) {
    //Do something
}
else {
    //Do something else
}
```

`反例`

```c
// bad
if (user.isHappy)
{
    //Do something
} else {
    //Do something else
}
```

##### 【建议】⽅法之间应该要有⼀个空⾏来帮助代码看起来清晰且有组织。⽅法内的空格应该⽤来分离功能，但是通常不同的功能应该⽤新的⽅法来定义。

##### 【建议】优先使⽤ auto-synthesize。但是如果必要的话， @synthesize and @dynamic

##### 【建议】在实现⽂件中的声明应该新起一⾏

##### 【建议】应该总是让冒号对⻬。有⼀些⽅法签名可能超过三个冒号，⽤冒号对⻬可以让代码更具有可读性。即使有代码块存在，也应该⽤冒号对⻬⽅法

正例

```c
// good
[UIView animateWithDuration:1.0
                 animations:^{
                     // something
                 }
                completion:^(BOOL finished) {
                     // something
                }];
```

`反例`

```c
// bad
[UIView animateWithDuration:1.0 animations:^{
    // something
} completion:^(BOOL finished) {
    // something
}];
```

##### 【建议】换行，⻓行的代码在第⼆行以⼀个间隔(2个空格)延续

正例

```c
//good
self.productsRequest = [[SKProductsRequest alloc]
  initWithProductIdentifiers:productIdentifiers];
```

`反例`

```c
//bad
self.productsRequest = [[SKProductsRequest alloc]
initWithProductIdentifiers:productIdentifiers];
```

##### 【建议】括号

- 控制语句使用括号包裹 (if-else, for, switch)

#### Pragma

##### Pragma Mark

- #pragma mark - 是⼀个在类内部组织代码并且帮助你分组⽅法实现的好办法。
- 不同功能组的⽅法
- protocols 的实现
- 对⽗类⽅法的重写

正例

```c
- (void)dealloc { /* ... */ }
- (instancetype)init { /* ... */ }

#pragma mark - View Lifecycle (View 的⽣生命周期)
- (void)viewDidLoad { /* ... */ }
- (void)viewWillAppear:(BOOL)animated { /* ... */ }
- (void)didReceiveMemoryWarning { /* ... */ }

#pragma mark - Custom Accessors (⾃自定义访问器器)
- (void)setCustomProperty:(id)value { /* ... */ }
- (id)customProperty { /* ... */ }

#pragma mark - IBActions
- (IBAction)submitData:(id)sender { /* ... */ }

#pragma mark - Public
- (void)publicMethod { /* ... */ }

#pragma mark - Private
- (void)zoc_privateMethod { /* ... */ }

#pragma mark - UITableViewDataSource
- (UITableViewCell *)tableView:(UITableView *)tableView cellForRowAtIndexPath:(NSIndexPath *)indexPath { /* ... */ }

#pragma mark - ZOCSuperclass
// ... 重载来⾃自 ZOCSuperclass 的⽅方法 #pragma mark - NSObject
- (NSString *)description { /* ... */ }
```

##### 忽略没有使⽤变量的编译警告（如果你非要保留一个没有用到的变量），使⽤ #pragma unused()

正例

```c
- (NSInteger)giveMeFive
{
    NSString *foo;
    #pragma unused (foo)
    return 5;
}
```

#### 注释

##### 【强制】单行注释，使用双斜杠 //

适⽤于单行的代码，包括注释斜杠。它适合简短的函数，特别是(但不仅仅是)⾮ public 的 API:

⽂本应该⽤⼀个动词 ("return") 而不是 "returns" 这样的描述。

正例

```c
// Return a user-readable form of a Frobnozz, html-escaped.
```

##### 【强制】多行注释，如果描述超过⼀行，应改用⻓字符串文档

以 /** 开始，换⾏写一句总结的话，以 ?或者!或者. 结尾，空⼀行，在与第⼀行对⻬的位置开始写剩下的注释，最后⽤ */ 结束。

正例

```c
/**
This comment serves to demonstrate the format of a docstring.

Note that the summary line is always at most one line long, and after the opening block comment, and each line of text is preceded by a single space.
*/
```

⼀个函数必须有⼀个字符串文档，除⾮它符合下面的所有条件:

- ⾮公开
- 很短
- 显而易见

##### 【强制】注释（字符串文档）应该描述函数的调⽤符号和语义，⽽不是它如何实现

#### 对象间的通讯

##### 【建议】使⽤ block 定义异步接⼝，当你定义⼀个类似下面的接⼝的时候，使⽤一个单独的 block 作为接口的最后一个参数。把需要提供的数据和错误信息整合到⼀个单独 block 中，比分别提供成功和失败的 block 要好

正例

```c
- (void)downloadObjectsAtPath:(NSString *)path
                   completion:(void(^)(NSArray *objects, NSError *error))completion;
```

调⽤者更关心的是实际的数据，就像这样:

```c
- (void)downloadObjectsAtPath:(NSString *)path
                   completion:(void(^)(NSArray *objects, NSError *error))completion {
    if (objects) {
        // do something with the data
    }
    else {
        // some error occurred, 'error' variable should not be nil by contract
    }
}
```

##### 【强制】self 的循环引⽤，当使⽤代码块和异步分发的时候，要注意避免引⽤循环。 使用 weak 来引⽤对象，避免引⽤循环

正例

```c
// good
__weak __typeof(self) weakSelf = self;
[self executeBlock:^(NSData *data, NSError *error) {
    [weakSelf doSomethingWithData:data];
}];
```

`反例`

```c
// bad
[self executeBlock:^(NSData *data, NSError *error) {
    [self doSomethingWithData:data];
}];
```

多个语句的例⼦:

正例

```c
// good
__weak __typeof(self)weakSelf = self;
[self executeBlock:^(NSData *data, NSError *error) {
    __strong __typeof(weakSelf) strongSelf = weakSelf;
    if (strongSelf) {
        [strongSelf doSomethingWithData:data];
        [strongSelf doSomethingWithData:data];
    }
}];
```

`反例`

```c
// bad
__weak __typeof(self)weakSelf = self;
[self executeBlock:^(NSData *data, NSError *error) {
    [weakSelf doSomethingWithData:data];
    [weakSelf doSomethingWithData:data];
}];
```

#### 委托和数据源

##### 【建议】委托可以分为如下两种类型

- 委托模式(delegate pattern):事件发⽣的时候，委托者需要通知代理者。
- 数据源模式(datasource pattern): 委托者需要从数据源对象拉取数据。

正例

```c
@class ZOCSignUpViewController;

@protocol ZOCSignUpViewControllerDelegate <NSObject>
- (void)signUpViewControllerDidPressSignUpButton: (ZOCSignUpViewController *)controller;
@end

@protocol ZOCSignUpViewControllerDataSource <NSObject>
- (ZOCUserCredentials *)credentialsForSignUpViewController: (ZOCSignUpViewController *)controller;
@end

@interface ZOCSignUpViewController : UIViewController
@property (nonatomic, weak) id<ZOCSignUpViewControllerDelegate> delegate;
@property (nonatomic, weak) id<ZOCSignUpViewControllerDataSource> dataSource;

@end
```

##### 【强制】代理方法必须以调⽤者(即委托者)作为第⼀个参数

正例

```c
- (void)calculatorDidCalculateValue:(CGFloat)value;
```

##### 【强制】默认情况下，代理者需要实现 protocol 的⽅法。可以⽤ @required 和 @optional 关键字来标记⽅法是否是必要的还是可选的(默认是 @required )

```c
@protocol ZOCSignUpViewControllerDelegate <NSObject>
@required
- (void)signUpViewController:(ZOCSignUpViewController *)controller didProvideSignUpInfo:(NSDictionary *)dict;
@optional
- (void)signUpViewControllerDidPressSignUpButton: (ZOCSignUpViewController *)controller;
@end
```

##### 【强制】对于可选的方法，委托者必须在发送消息前检查代理是否确实现了特定的⽅法(否则会 crash)

```c
if ([self.delegate respondsToSelector:@selector(signUpViewControllerDidPressSignUpButton:)]) {
    [self.delegate signUpViewControllerDidPressSignUpButton:self];
}
```

#### 废弃的 API

##### 【强制】禁止使用废弃的 API

> **禁止** 在项目中使用 Apple 官方标记为 `Deprecated` 的 API（如 `UIWebView`、`NSURLConnection` 等）
> **审核风险**：使用废弃 API 可能导致 App Store 审核被拒
> **性能与安全**：废弃 API 存在内存泄漏、性能低下、安全漏洞等问题（如 `UIWebView` 不支持 JavaScript 现代沙盒机制）。
> **技术债务**：废弃 API 未来可能被系统移除，导致应用崩溃或功能异常。
> **必须** 使用 Apple 推荐的替代方案（如 `WKWebView`、`URLSession`）。

常见废弃 API 替换

| 废弃 API | 替代方案 | 关键差异 |
| ---- | ---- | ---- |
| `NSURLConnection` | `URLSession` | 支持后台传输、更简洁的异步 API |
| `UIActionSheet` | `UIAlertController` | 统一弹窗样式、支持 Block 回调 |
| `NSStringDrawing` | `NSAttributedString` | 支持复杂文本样式、高性能渲染 |

### 安全

#### 敏感数据

##### 【强制】在设备本地保存数据时，不使用明文存储敏感数据，如果确实需要，应对敏感数据进行加密处理后再保存

【自动/工具检查手段】梆梆

> 如果将敏感数据存储在iOS设备中，由于环境是不安全的，这将可能导致存储的敏感数据泄露。

> 在 iOS 中最普遍的本地存储方式就是将数据存到 plist 文件，但是由于它没有加密，因此这种方式保存敏感信息是不安全的。即使在没有越狱的设备上，plist 文件也可以通过工具获取。因此在 plist 中明文存储的敏感信息很容易被泄露。另外，iOS 中也经常使用 NSUserDefaults 来保存数据到 plist 文件，这也是不安全的。在 iOS 中 SQLite 是很常用的数据库，但由于 SQLite 数据库没有内置的加密支持，因此在 SQLite 中明文存储的敏感信息也是不安全的，容易导致敏感信息泄露。

> 可以使用 Keychain 加密保存敏感信息，Keychain 是 iOS 所提供的一种安全存储数据的方式，它会将数据以加密的方式存储在设备中，因此用 Keychain 来保存敏感信息是比较安全的，使用 Apple 提供的 KeychainItemWrapper 类可以方便的使用 KeyChain 来保存数据。

正例

```c
// plist
// 获取沙盒路径
NSArray *path = NSSearchPathForDirectoriesInDomains(NSDocumentDirectory, NSUserDomainMask, YES);
NSString *documentsPath = [path objectAtIndex:0];
NSString *plistPath = [documentsPath stringByAppendingPathComponent:@"userInfo.plist"];
NSLog(@"plist path: %@", plistPath);
NSMutableDictionary *newsDict = [NSMutableDictionary dictionary];
// 加密数据
NSString *value = aesEncryptString(@"the data need be encrypted.");
[newsDict setObject:value forKey:@"key"];
// 存储文件
[newsDict writeToFile:plistPath atomically:YES];

//SQLite 
NSString *databasePath = [[NSSearchPathForDirectoriesInDomains (NSDocumentDirectory, NSUserDomainMask, YES) objectAtIndex:0] stringByAppendingPathComponent: @"sqlcipher.db"];
sqlite3 *db;
bool sqlcipher_valid = NO;
if ( sqlite3_open( [databasePath UTF8String], &db ) == SQLITE_OK ) {
  const char* key = [@"BIGSecret" UTF8String];
  sqlite3_key( db, key, strlen( key ) );
  if ( sqlite3_exec( db, (const char *) "SELECT count(*) FROM sqlite_master;", NULL, NULL, NULL ) == SQLITE_OK ) {
    if ( sqlite3_prepare_v2( database, "PRAGMA cipher_version;", -1, &stmt, NULL ) == SQLITE_OK ) {
      if ( sqlite3_step( stmt ) == SQLITE_ROW ) {
        const unsigned char *ver = sqlite3_column_text( stmt, 0 );
        if ( ver != NULL ) {
          sqlcipher_valid = YES;
          // password is correct (or database initialize), and verified to be using sqlcipher
        }
      }  
      sqlite3_finalize( stmt );
    }
  }
  sqlite3_close( db );
}

// Keychain 
KeychainItemWrapper *wrapper = [[KeychainItemWrapper alloc] initWithIdentifier:@"Account Number" accessGroup:@"YOUR_APP_ID_HERE.com.yourcompany.AppIdentifier"];
[wrapper setObject:@"" forKey:(id)kSecAttrAccount];
[wrapper setObject:@"" forKey:(id)kSecValueData];
```

`反例`

```c
NSArray *paths = NSSearchPathForDirectoriesInDomains(NSDocumentDirectory,NSUserDomainMask,YES);
NSString *documentsDirectory = [paths objectAtIndex:0];
NSString *filePath = [documentsDirectory stringByAppendingString:@"/userInfo.plist"]; NSMutableDictionary* plist = [[NSMutableDictionary alloc] init];
[plist setValue:self.usernameTextField.text forKey:@"username"];
[plist setValue:self.passwordTextField.text forKey:@"passwprd"];
[plist writeToFile:filePath atomically:YES];

// NSUserDefaults
+ (void)setUserDefaultsValue:(id)value key:(NSString *)key {
NSUserDefaults *userDefaults = [NSUserDefaults standardUserDefaults];
[userDefaults setObject:value forKey:key];
[[NSUserDefaults standardUserDefaults] synchronize];
}

//SQLite
sqlite3 *db;
int result = sqlite3_open([path UTF8String], &db);
char *sql = "insert into t_person(name, age) values(?, ?);";
sqlite3_stmt *stmt;
if (sqlite3_prepare_v2(db, sql, -1, &stmt, NULL) == SQLITE_OK) {
  sqlite3_bind_text(stmt, 1, "Tom", -1, NULL);
  sqlite3_bind_int(stmt, 2, 27);
}

if (sqlite3_step(stmt) != SQLITE_DONE) {
  NSLog(@"insert error!");
}
sqlite3_finalize(stmt);
```

##### 【强制】禁止将密钥进行硬编码存储

【自动/工具检查手段】Fortify

> 如果密钥以明文字符串形式存储在代码中。攻击者可以通过反编译的方式获取应用代码和加密密钥，这将导致加密数据被解密还原的风险。可以使用 Keychain 来保存密钥

正例

```c
//Create a Query Dictionary
SecKeyRef key = <#### a key #>;
NSData* tag = [@"com.example.keys.mykey" dataUsingEncoding:NSUTF8StringEncoding];
NSDictionary* addquery = @{ (id)kSecValueRef: (__bridge id)key, (id)kSecClass: (id)kSecClassKey, (id)kSecAttrApplicationTag: tag, };
//Store the Item
OSStatus status = SecItemAdd((__bridge CFDictionaryRef)addquery, NULL);
if (status != errSecSuccess) {
  <# Handle the error #>
} else {
  <# Use the key #>
}
//Retrieve the Item
NSDictionary *getquery = @{ (id)kSecClass: (id)kSecClassKey, (id)kSecAttrApplicationTag: tag, (id)kSecAttrKeyType: (id)kSecAttrKeyTypeRSA, (id)kSecReturnRef: @YES,
};
```

`反例`

```c
static NSString *const PSW_AES_KEY = @"TESTPASSWORD";
static NSString *const AES_IV_PARAMETER = @"AES00IVPARAMETER";
@implementation NSString (AES)
- (NSString*)encryptWithAES {
  NSData *data = [self dataUsingEncoding:NSUTF8StringEncoding];
  NSData *AESData = [self AES128operation:kCCEncrypt data:data key:PSW_AES_KEY iv:AES_IV_PARAMETER];  
  NSString *baseStr_GTM = [self encodeBase64Data:AESData];
  NSString *baseStr = [AESData base64EncodedStringWithOptions:NSDataBase64Encoding64CharacterLineLength];
  return baseStr_GTM;
}

- (NSString*)decryptWithAES {
  NSData *data = [self dataUsingEncoding:NSUTF8StringEncoding];
  NSData *baseData_GTM = [self decodeBase64Data:data];
  NSData *baseData = [[NSData alloc]initWithBase64EncodedString:self options:0];
  NSData *AESData_GTM = [self AES128operation:kCCDecrypt data:baseData_GTM key:PSW_AES_KEY iv:AES_IV_PARAMETER];
  NSData *AESData = [self AES128operation:kCCDecrypt data:baseData key:PSW_AES_KEY iv:AES_IV_PARAMETER];
  NSString *decStr_GTM = [[NSString alloc] initWithData:AESData_GTM encoding:NSUTF8StringEncoding];
  NSString *decStr = [[NSString alloc] initWithData:AESData encoding:NSUTF8StringEncoding];
  return decStr;
}
```

##### 【强制】应用记录日志信息时，不应记录任何敏感信息

【自动/工具检查手段】梆梆可检查是否禁止调试日志输出

> 通常应用在运行时会将一些运行过程的信息写到日志记录中。如果日志中记录了敏感信息，而这样的日志信息在客户端是不安全，容易导致这些敏感信息泄露。攻击者在用 Xcode 调试应用时可以查看应用运行时输出的日志信息，如果其中包含敏感信息，就会导致敏感信息泄露。所以，在日志中记录相关信息时，不保存敏感信息。

> 在日志中记录相关信息时，不保存敏感信息，或在发布版本时禁止调试日志输出。使用 define 来启用 NSLog 语句进行开发和调试，并在发布软件之前禁用这些语句。这可以将以下代码放入相应的 PREFIX_HEADER（* .pch）文件中。

```c
#ifdef DEBUG
# define NSLog (...) NSLog(__VA_ARGS__)
#else
# define NSLog (...)
#endif
```

`反例`

```c
if ( [self.nameTF.text isEqualToString:@""] ) {
  [SVProgressHUD showErrorWithStatus:@"请输入用户名"];
  return;
}
if ( [self.passwordTF.text isEqualToString:@""] ) {
  [SVProgressHUD showErrorWithStatus:@"请输入密码"];
  return;
}

NSString *interface = @"/web/app/login.form";
NSDictionary *param = @ { @"loginName" : self.nameTF.text, @"password" :[common md5:[NSString stringWithFormat:@"{%@}", self.passwordTF.text]] };
NSLog( @"loginName : %s , password : %s", self.nameTF.text, self.passwordTF.text )
```

##### 【建议】在涉及敏感数据输入文本框中，禁用键盘缓存

【自动/工具检查手段】暂无

##### 【建议】在涉及敏感数据的文本框中，停用剪切板功能

【自动/工具检查手段】暂无

##### 【强制】当敏感数据需要显示在前端页面时，对敏感信息进行脱敏处理

【自动/工具检查手段】暂无

##### 【强制】在进行业务查询时，应仅返回满足业务需要的数据，不应返回多余的敏感信息

【自动/工具检查手段】暂无

#### 加密强度不足

##### 【强制】不使用弱随机数，使用安全的随机数生成方式

【自动/工具检查手段】梆梆

> 通常，使用随机数的场景包括但不限于如下场景：
> • 生成密钥：对称密码，消息认证
> • 生成密钥对：公钥密码，数字签名
> • 生成 IV： 用于分组密码的 CBC，CFB 和 OFB 模式
> • 生成 nonce: 用于防御重放攻击; 分组密码的 CTR 模式
> • 生成盐：用于基于口令的密码 PBE 等

> 由于使用弱随机函数生成随机数时，在相同初始向量的情况下会生存相同的随机数，因此通过这样方式生成的随机数没有足够的随机性，存在被破解的风险。使用相同的种子就可以生成相同的随机数，攻击者如果获得了应用随机数生成的种子，那么攻击者就可以破解应用中使用随机数场景的安全控制。

正例

```c
NSInteger randomNumber = arc4random() % 16;
Or
int randomNumber = SecRandomCopyBytes(kSecRandomDefault, 16, randomBytes);
```

`反例`

```c
rand();
random();
```

##### 【强制】引入加密算法时使用安全的加密算法

【自动/工具检查手段】梆梆可检查AES,DES，哈希算法

> 禁止使用自行开发的加密算法，必须使用公开、安全的标准加密算法，不安全的加密算法都是已经被破解的算法，使用它们加密的数据已不再安全，对于不安全的加密算法可以使用暴力破解或者破解工具来对密文数据进行破解。

> 使用以下加密算法时，密钥的长度应满足：AES 256 及以上长度；RSA 2048 及以上长度；ECC 256 及以上长度；SM2 256 及以上长度；SHA256 256；SM3 256。

> 使用 AES/DES/DESede 等加密算法时，不要使用默认的加密模式 ECB，应显示指定使用 CBC 或 CFB 加密模式。

正例

```c
// AES
-(NSData *)AES256EncryptWithKey:(NSData *)key {
  const void * keyPtr2 = [key bytes];
  char (*keyPtr)[32] = keyPtr2;
  NSUInteger dataLength = [self length];
  size_t bufferSize = dataLength + kCCBlockSizeAES256;
  void *buffer = malloc( bufferSize );
  size_t numBytesEncrypted = 0;
  CCCryptorStatus cryptStatus = CCCrypt( kCCEncrypt, kCCAlgorithmAES256, kCCOptionPKCS7Padding [key bytes], kCCKeySizeAES256, NULL, [self bytes], dataLength, buffer, bufferSize, &numBytesEncrypted );
  if ( cryptStatus == kCCSuccess ) {
    return([NSData dataWithBytesNoCopy:buffer length:numBytesEncrypted]);
  }
  free( buffer );
  return(nil);
}

// HASH 算法，SHA256 
- (NSString *)SHA256 {
  const char *s = [self cStringUsingEncoding:NSASCIIStringEncoding];
  NSData *keyData = [NSData dataWithBytes:s length:strlen(s)];
  uint8_t digest[CC_SHA256_DIGEST_LENGTH] = {0};
  CC_SHA256(keyData.bytes, (CC_LONG)keyData.length, digest);
  NSData *out = [NSData dataWithBytes:digest length:CC_SHA256_DIGEST_LENGTH];
  NSString *hash = [out description];
  hash = [hash stringByReplacingOccurrencesOfString:@" " withString:@""];
  hash = [hash stringByReplacingOccurrencesOfString:@"<" withString:@""];
  hash = [hash stringByReplacingOccurrencesOfString:@">" withString:@""];
  return hash;
}
```

`反例`

```c
// DES
- (NSData *)encryptDESByKey:(NSData *)key data:(NSData *)data {
  size_t numBytesEncrypted = 0;
  size_t bufferSize = data.length + kCCBlockSizeDES;
  void *buffer = malloc(bufferSize);
   CCCryptorStatus result = CCCrypt( kCCEncrypt, kCCAlgorithmDES, kCCOptionPKCS7Padding, key.bytes, kCCKeySizeDES, NULL, data.bytes, data.length, buffer, bufferSize, &numBytesEncrypted);
  NSData *output = [NSData dataWithBytes:buffer length:numBytesEncrypted];
  free(buffer);
  if( result == kCCSuccess ) {
    return output;
  } else {
    NSLog(@"Failed DES encrypt...");
    return nil;
  }
}

// RSA
#define kRSA_KEY_SIZE 512
@interface ViewController : UIViewController {
  SecKeyRef publicKeyRef;
  SecKeyRef privateKeyRef;
}

//生成 RSA 密钥对，公钥和私钥，支持的 SIZE 有 sizes for RSA keys are: 512, 768, 1024, 2048.
- (void)generateRSAKeyPair:(int)keySize {
  OSStatus ret = 0;
  publicKeyRef = NULL;
  privateKeyRef = NULL;
  ret = SecKeyGeneratePair( (CFDictionaryRef) @ { (id) kSecAttrKeyType: (id) kSecAttrKeyTypeRSA, (id) kSecAttrKeySizeInBits: @ (keySize) }, &publicKeyRef, &privateKeyRef );
  NSAssert( ret == errSecSuccess, @"密钥对生成失败：%d", ret );
  NSLog( @"%@", publicKeyRef );
  NSLog( @"%@", privateKeyRef );
  NSLog( @"max size:%lu", SecKeyGetBlockSize( privateKeyRef ) );
}

// 不安全的 HASH 算法，MD5 哈希算法。
+(NSString *)MD5ForLower32Bate:(NSString *)str{
  //要进行 UTF8 的转码
  const char* input = [str UTF8String];
  unsigned char result[CC_MD5_DIGEST_LENGTH];
  CC_MD5(input, (CC_LONG)strlen(input), result);
  NSMutableString *digest = [NSMutableString stringWithCapacity:CC_MD5_DIGEST_LENGTH * 2];
  for (NSInteger i = 0; i < CC_MD5_DIGEST_LENGTH; i++) {
    [digest appendFormat:@"%02x", result[i]];
  }
  return digest;
}
```

#### 通信安全

##### 【建议】通信过程需要使用HTTPS加密

【自动/工具检查手段】梆梆

> 由于 HTTP 是明文传输数据，在不可信的网络环境下，网络请求可能被中间人攻击（Man-in-the-MiddleAttack）， 导致传输的敏感信息被中间人获取或篡改。攻击者可以通过工具对网络中传输的数据进行嗅探，如果应用使用 HTTP 明文传输数据，那么传输的敏感数据将会被泄露。所以，应用在通过网络传输数据时，需要使用HTTPS加密。

> Apple 在 iOS9 中新增了 App Transport Security（ATS）特性，对所有的 HTTP 协议都强制使用了 HTTPS 协议进行传输。但如果开发者在 Info.plist 中将 NSAllowsArbitraryLoads 设置为 ture，这就会导致绕过 ATS 而使用 HTTP 来进行通信。

正例

```c
// NSURLSession
- (void)urlSession {
  NSURL *url = [NSURL URLWithString:@"https://example.com/"];
  NSURLSession *session = [NSURLSession sessionWithConfiguration:[NSURLSessionConfiguration defaultSessionConfiguration] 
  delegate:self delegateQueue:[NSOperationQueue mainQueue]];

  NSURLSessionDataTask *dataTask = [session dataTaskWithURL:url completionHandler:^(NSData * _Nullable data, NSURLResponse * _Nullable response, NSError * _Nullable error) {
  NSLog (@"%@", [[NSString alloc] initWithData:data encoding:NSUTF8StringEncoding]);
}];
[dataTask resume];
}

// AFN 框架
AFHTTPSessionManager * manager = [AFHTTPSessionManager manager];
NSString * cerPath = [[NSBundle mainBundle] pathForResource:@"server" ofType:@"cer"];
NSData * cerData = [NSData dataWithContentsOfFile:cerPath];
NSLog( @"%@", cerData );
manager.securityPolicy = [AFSecurityPolicy policyWithPinningMode:AFSSLPinningModeCertificate withPinnedCertificates:[[NSArray alloc] initWithObjects:cerData, nil]]
manager.securityPolicy.allowInvalidCertificates = NO;
manager.securityPolicy.validatesDomainName = YES;
manager.requestSerializer = [AFJSONRequestSerializer serializer];
manager.responseSerializer = [AFJSONResponseSerializer serializer];
NSDictionary * parameter = @ { @"username" : self.username, @"password" : self.password };
[manager POST:@"https://example.com" parameters:parameter success:^(NSURLSessionDataTask * task, id responseObject) {
  NSLog (@"success %@", responseObject);
}

failure:^(NSURLSessionDataTask * task, NSError * error) {
NSLog (@"failure %@", error);
}]
```

`反例`

```c
// NSURLConnectiong
NSURL *url = [NSURL URLWithString:@"http://example.com"];
NSMutableURLRequest *request = [NSMutableURLRequest requestWithURL:url];
request.HTTPMethod = @"POST"; request.timeoutInterval = 5;
NSString *param = [NSString stringWithFormat:@"name=%@&password=%@",name, password];
request.HTTPBody = [param dataUsingEncoding:NSUTF8StringEncoding];
[NSURLConnection sendSynchronousRequest:request returningResponse:nil error:nil];

// NSURLSession 
NSURLSession *session = [NSURLSession sharedSession];
NSURL *url = [NSURL URLWithString:@"http://example.com"];
NSURLSessionTask *task = [session dataTaskWithURL:url completionHandler:^(NSData *data, NSURLResponse *response, NSError *error) {
NSLog(@"%@", [NSJSONSerialization JSONObjectWithData:data options:kNilOptions error:nil]);
}];
[task resume];
```

##### 【建议】HTTPS通信过程中需要对服务器证书进行校验

【自动/工具检查手段】梆梆

> 应用在使用证书进行HTTPS通信时，如果没有对服务端提交的证书进行安全检查，就可能导致在不可信的网络环境中的数据请求被进行中间人攻击，导致传输的敏感信息被中间人获取或篡改。使用假的证书冒充服务端与客户端通信，由于客户端未对正式进行恰当的安全验证，就可以导致用假证书冒充与客户端通信成功。所以应用在使用证书进行HTTPS通信时，需要进行正确验证。

正例

```c
AFHTTPSessionManager * manager = [AFHTTPSessionManager manager];
NSString * cerPath = [[NSBundle mainBundle] pathForResource:@"server" ofType:@"cer"];
NSData * cerData = [NSData dataWithContentsOfFile:cerPath];
NSLog( @"%@", cerData );
manager.securityPolicy = [AFSecurityPolicy policyWithPinningMode:AFSSLPinningModeCertificate withPinnedCertificates:[[NSArray alloc] initWithObjects:cerData, nil]];
manager.securityPolicy.allowInvalidCertificates = YES;
manager.securityPolicy.validatesDomainName = YES;
manager.requestSerializer = [AFJSONRequestSerializer serializer];
manager.responseSerializer = [AFJSONResponseSerializer serializer];
NSDictionary * parameter = @ { @"username" : self.username, @"password" : self.password };
[manager POST:@"https://example.com" parameters:parameter success:^(NSURLSessionDataTask * task, id responseObject) {
NSLog (@"success %@", responseObject);
} failure:^(NSURLSessionDataTask * task, NSError * error) {
NSLog (@"failure %@", error);
}]
```

`反例`

```c
// 本地证书库没有添加 server 的 CA 证书
AFHTTPSessionManager *manager = [AFHTTPSessionManager manager];
manager.securityPolicy.allowInvalidCertificates = YES;
manager.securityPolicy.validatesDomainName = NO;
manager.requestSerializer.cachePolicy = NSURLRequestReloadIgnoringLocalCacheData;
[manager GET:@"https://example.com/" parameters:nil progress:nil success:^(NSURLSessionDataTask * _Nonnull task, id _Nullable responseObject) {
NSLog (@"%@", responseObject);
} failure:^(NSURLSessionDataTask * _Nullable task, NSError * _Nonnull error) {
NSLog (@"%@", error);
}];

// 使用 AFNetworking，如果其 securityPolicy 的 validatesDomainName 设置为 NO，则不会对证书域名进行检查。
securityPolicy.validatesDomainName = NO;
```

#### 数据溢出问题

##### 【建议】对缓冲区溢出问题进行防御

【自动/工具检查手段】梆梆可检查是否使用编译器堆栈保护技术、地址空间随机化技术

> 缓冲区是存储任何类型的数据的地方，当缓冲区中的数据超过缓冲区本身的大小时，会发生溢出。然后攻击者可以执行溢出攻击，来获得对程序的控制和执行恶意载荷。攻击者在溢出点输入精心构造的数据，让应用在溢出后将执行攻击者构造的代码，导致用户被攻击。

> 根据缓冲区大小检查数据长度，能够防御缓冲区溢出。由于 C 语言中很多字符串处理函数的固有缺陷，容易导致缓冲区溢出，因此要尽量避免使用这些函数，而使用更安全的函数代替。另外，可以启用编译器堆栈保护技术、地址空间随机化技术等来防御。

正例

```c
char buf[1024];
...
if (size < sizeof(buf)) {
  ...
}
```

`反例`

```c
char buf[1024];
...
if (size < 1024) {
  ...
}
```

##### 【建议】对整数溢出问题进行防御

【自动/工具检查手段】暂无

> 使用未验证的整形数据进行算术运算，可能会导致计算结果过大而无法在系统位宽度范围内存储，比较安全的方法是使用内建的 clang 算术检查。

正例

```c
size_t bytes;
if (__builtin_umull_overflow(m, n, &bytes)) {
  /* Overflow occured. Handle appropriately. */
} else {
  /* Allocate "bytes" space. */
}
```

`反例`

```c
size_t bytes = n * m;
if (bytes < n `````` bytes < m) {
  /* BAD BAD BAD */
  ...
  /* allocate “bytes” space */
}
```

#### 异常处理

##### 【强制】对异常进行恰当的处理，并不暴露敏感信息

【自动/工具检查手段】暂无

> 如果应用未对异常进行恰当的处理，不仅可能会影响应用的正常使用，而且其暴露的内部异常提示信息也可能被攻击者利用来攻击应用。攻击者可以触发应用异常来获取显示的异常信息，并可通过这些暴露的敏感异常信息来帮助分析应用漏洞，达到攻击应用的目的。

`反例`

```c
// 数组越界未处理
NSArray *array = [NSArray array];
[array objectAtIndex:1]; //数组越界

// 处理异常时暴露敏感信息，直接抛出栈异常信息
@try{
  //do work here
} @catch ( NSException *exception ) {
  NSLog( @"%@", [exception callStackSymbols] );
}
```

#### 本地注入防护

##### 【建议】防御本地 SQL 注入，使用参数化查询可以有效防御 SQL 注入

【自动/工具检查手段】暂无

> 在 iOS 本地使用数据库时，其所有操作都和传统服务端的数据库类似，因此存在于服务端的 SQL 注入问题也存在于本地的数据库中。但是攻击者却可能提交恶意的参数，导致SQL注入，执行危险操作。可以使用参数化查询，防御 SQL 注入。

正例

```c
NSString* safeSqlString = [NSString stringWithFormat:@"select * from country where engname = ?"];
NSString* engname = [NSString stringWithFormat:@"%@", self.mytitle.text];
sqlite3_stmt* statement;
if ( sqlite3_prepare_v2( db, [safeSqlString UTF8String], -1, &statement, nil ) == SQLITE_OK ) {
  if ( sqlite3_bind_text( statement, 1, [engname UTF8String], -1, NULL ) != SQLITE_OK ) {
    /* Error Handling Code */
    NSAssert1( 0, @"code1%s", sqlite3_errmsg( db ) );
    sqlite3_finalize( statement );
    return;
  }
sqlite3_reset( statement );
TabelDatas = [self statementtoMSarray:statement];
[self.mytable reloadData];
} else {
  NSLog( @"%s", sqlite3_errmsg( db ) );
}
sqlite3_finalize( statement );
```

`反例`

```c
NSString *sql2 = [NSString stringWithFormat:@"select * from country where engname = %@",self.mytitle.text];
```

#### 组件使用安全

##### 【强制】使用URL Schemes进行数据传递时，应指定可调用的应用，并对接收的数据进行检查，

【自动/工具检查手段】梆梆

> iOS系统中为了方便App之间的相互调用与通讯，可使用URL Schemes来实现应用的唤起和数据的传递，如果应用没有正确验证 URL 及其参数的情况下，处理对其 URL schemes 的调用，以及在触发重要操作之前未提示用户进行确认，当恶意应用在 URL schemes 中发送了恶意数据， 就可能会对正常应用产生安全影响。

正例

```c
// 限定能调用的应用
- (BOOL)application:(UIApplication *)application openURL:(NSURL *)url sourceApplication:(NSString *)sourceApplication annotation:(id)annotation {
  NSLog( @"sourceApplication: %@", sourceApplication );
  NSLog( @"URL scheme:%@", [url scheme] );
  NSLog( @"URL query: %@", [url query] );
  
  if ( [sourceApplication isEqualToString:@"com.3Sixty.CallCustomURL"] ) {
    UIAlertView *alertView = [[UIAlertView alloc] initWithTitle:@"OPEN" message:[url query] delegate:nil cancelButtonTitle:@"OK" otherButtonTitles:nil];
    [alertView show];
    return(YES);
  }else{
    return(NO);
  }
}

// 数据进行检查
NSString * regex = @"(/^[0-9]*$/)";
NSPredicate * pred = [NSPredicate predicateWithFormat:@"SELF MATCHES %@", regex];
BOOL isMatch = [pred evaluateWithObject:str];
```

`反例`

```c
-(BOOL)application:(UIApplication *)application openURL:(NSURL *)url sourceApplication:(NSString *)sourceApplication annotation:(id)annotation {
  NSLog( @"sourceApplication: %@", sourceApplication );
  NSLog( @"URL scheme:%@", [url scheme] ); 
  NSLog( @"URL query: %@", [url query] );
  UIAlertView *alertView = [[UIAlertView alloc] initWithTitle:@"OPEN" message:[url query] delegate:nil cancelButtonTitle:@"OK" otherButtonTitles:nil];
  [alertView show];
  return(YES);
}
```

#### WebView安全

> iOS 中的 WebView 和我们平常使用的浏览器类似，因此浏览器面临的一些 问题，在 WebView 中也可能出现。

##### 【建议】禁止WebView启用JavaScript，如果需要启用，需要进行相关的安全防护

【自动/工具检查手段】暂无

> 如果不是必须，不要在WebView中启用JavaScript。如果确实需要在 WebView 中使用 JavaScript，则建议输出数据时进行编码处理。对于 HTML 中的数据，除了字母、数字外的所有字符应编码成 HTML 实体格式 &#xHH。对于 JavaScript 中的数据，除了字母、数字外的所有字符应编 码成\uXXXX 格式

`反例`

```c
- (void)viewDidLoad {
  NSURL *url = [NSURL URLWithString:@"http://www.example.com/"];
  NSURLRequest *request = [NSURLRequest requestWithURL:url];
  WKPreferences *pref = [[WKPreferences alloc] init];
  [pref setJavaScriptEnabled:YES];
  [pref setJavaScriptCanOpenWindowsAutomatically:YES];
  WKWebViewConfiguration *conf = [[WKWebViewConfiguration alloc] init];
  [conf setPreferences:pref]; _webView = [[WKWebView alloc]initWithFrame:CGRectMake(self.view.frame.origin.x,85, self.view.frame.size.width, self.view.frame.size.height-85) configuration:conf] ;
  [_webView loadRequest:request];
  [self.view addSubview:_webView];
}
```

##### 【建议】关闭相关配置，防御跨域访问漏洞问题

【自动/工具检查手段】梆梆

> iOS WebView 的跨域访问漏洞是由于其 UIWebView 的 WebKitAllowUniversalAccessFromFileURLs 和 WebKitAllowFileAccessFromFileURLs 默认开启。 Apple 在 iOS 8.0 以后推出了 WKWebView 代替 UIWebView，并且 WKWebView 默认 allowFileAccessFromFileURLs 和 allowUniversalAccessFromFileURLs 选项为 false，但如果开发人员启用了这两个 API，则同样会存在跨域漏洞

> 如果要使用 WebView 时应尽量使用 WKWebView ，且不要启用 allowFileAccessFromFileURLs 和 allowUniversalAccessFromFileURLs。 另外，不要在 WebView 中加载来自外部传入的 file://域页面。对于加载的本地文件，用户应不能够更改加载文件的路径和文件名，以确保 WebView 载入的文件都是可信的。

`反例`

```c
WKWebViewConfiguration * configuration = [[WKWebViewConfiguration alloc] init];
[configuration.preferences setValue:@TRUE forKey:@"allowFileAccessFromFileURLs"];
[configuration setValue:@TRUE forKey:@"allowUniversalAccessFromFileURLs"];
WKWebView *wkweb = [[WKWebView alloc] initWithFrame:self.view.frame configuration:configuration];
wkweb.center = self.view.center;
wkweb.UIDelegate = self;
[self.view addSubview:wkweb];
NSString *resourcePath = [[NSBundle mainBundle] resourcePath];
NSString *filePath =[resourcePath stringByAppendingPathComponent:@"index.html"];
NSMutableString *htmlstring=[[NSMutableString alloc] initWithContentsOfFile:filePath encoding:NSUTF8StringEncoding error:nil];
NSURL *baseUrl=[NSURL fileURLWithPath:[[NSBundle mainBundle] bundlePath]];
[wkweb loadHTMLString:htmlstring baseURL:baseUrl];
```

##### 【强制】在JavaScript中禁止使用innerHTML属性

【自动/工具检查手段】梆梆

> 客户端上的JavaScript脚本可以访问浏览器的DOM并修改页面的内容，不依赖服务器的数据，直接从浏览器端获取数据并执行。在JavaScript中DOM的innerHTML属性可以赋值一个标签，容易受到XSS攻击。如果攻击者利用该漏洞进行攻击，可能会导致账号或Cookie信息被窃取，从而冒充管理者登录后台进行数据篡改等恶意操作。DOM型XSS漏洞是基于文档对象模型（Document Object Model）的一种漏洞。它的攻击代码不需要服务器解析响应，而是通过浏览器端的DOM解析触发XSS。

#### 其他安全要求

##### 【强制】禁止使用不安全的API函数

【自动/工具检查手段】梆梆

> iOS中提供的系统API函数中，包含一些存在安全隐患或者需配合指定方式使用的系统API，否则将会导致安全性问题。其中，比较明显的一种问题就是缓冲区溢出攻击。此类API中无法自动对栈中的数组进行边界检查，而且局部变量和状态信息，都存在栈中。这样，对越界的数组元素的写操可能会破坏存储在栈中的状态信息。当程序使用这个被破坏的状态，试图重新加载寄存器或执行ret指令时，就会出现很严重的错误，可能导致程序运行失败、系统关机、重新启动。更加致命的情况是让程序跳转去执行攻击者的恶意指令，比如非法提升权限，执行恶意代码等。
> 应用程序中禁止调用的系统风险函数和过期api,同时防止系统直接调用存在C缓冲区溢出的函数如 memcpy、scanf、sprintf、strcpy、vsprintf

##### 【强制】禁止使用URL Schemes唤醒应用

    > 源于 11546904 新电gomo app安全问题治理- Abuse of URL Schemes 

    说明：可以结合客户需求考虑是否支持URL Schemes唤醒

##### 【强制】应用在申请用户权限时只申请必要的权限，申请的权限需要用户授予后才能使用

    > 源于 | 11547236 新电gomo app安全问题治理- Excessive Application Permissions

##### 【强制】应用切换到后台时，应该对界面敏感数据进行模糊化处理

    > 源于 | 11537913 新电gomo app安全问题治理- Sensitive Information Included in Snapshots

    说明：可以结合客户需求考虑

##### 【强制】对于包含敏感数据页面应该禁止截图

    > 源于 | 11537913 新电gomo app安全问题治理- Sensitive Information Included in Snapshots

    说明：可以结合客户需求考虑

#### 发布安全

##### 【建议】在对应用进行签名时，应使用有效的证书进行签名

【自动/工具检查手段】梆梆

##### 【建议】应用发布前，调试符号应从原生二进制文件中删除，调试代码应进行删除

【自动/工具检查手段】暂无

##### 【强制】正式发布的包文件需执行安全加固流程对ipa文件执行安全加固

> 补充要求 ：执行安全加固后，研发所内的出厂测试、CD，以及现场的UAT、BRT，都必须测试安全加固后的版本，充分验证加固后APP的兼容性
> 规范来源：故障单号：3796792

【自动/工具检查手段】APP发布流程

### 持续构建步骤

#### 新建构建

按照下方图示，找到持续构建入口，并点击新建构建

![image](uploads/113737/9f225dc7-6f31-4058-b842-7725d4b4f688/image.png)

![image](uploads/113737/db785ff7-e477-42cd-9040-253eaed96685/image.png)

##### 新建构建 - 应用模块

![image](uploads/113737/5549aa26-c46e-44d5-84af-3d6fa039270f/image.png)

- 应用模块：按照后面提示自行选择合适的应用模块，或者新建
- 语言模版：选择iOS（iOS项目选择该选项）
- Agent：iOS项目构建运行的主机，在提供主机中，选择一个即可（注：给每个产品线分配的主机不同）
- 后面直接点击下一步，如果没有其他特殊要求，全部默认行为，最后点击新建构建
  ![image](uploads/113737/1b4bb7c0-9f42-4804-a5d3-d69f8ce246ff/image.png)

##### 编辑构建 - 代码下载

![image](uploads/113737/1699323b-431b-45e2-8c67-fa3cb8957245/image.png)

填写对应的信息，将代码下载到之前第二步的主机上（新建构建 - 应用模块 - agent）

##### 编辑构建 - 代码编译

这个步骤中，可以增加一些脚本，用于打包制品、上传制品等，需要用户自己写脚本，在下面“脚本模版”章节中，会给一些功能脚本模版，可以参照模版做修改

##### 构建编辑 - 代码分析

![image](uploads/113737/57a1abb1-470c-4bda-85ae-f74ce01883b6/image.png)

- 扫描路径：默认不填，表示检查当前目录下的所有代码
- 例外路径：例外文件配置，请填写例外文件的文件名，无需填写相对路径，多个例外文件时请用英文逗号(,)分隔，例外的文件不做检查

代码分析的原理，请参考[OCLint iOS代码检测](https://docs.iwhalecloud.com/doi/cjxWb4/OCLint%20iOS%E4%BB%A3%E7%A0%81%E6%A3%80%E6%B5%8B)

#### 脚本模本

脚本仅供参考，需要根据实际的工程进行修改

##### 下载脚本和配置文件

| 功能         | 文件名      | 文件地址                                                                                                                                |
| ------------ | ----------- | --------------------------------------------------------------------------------------------------------------------------------------- |
| 打包ipa脚本  | build.sh    | [https://docs.iwhalecloud.com/dmz-proxy/cos/download/853/build.sh](https://docs.iwhalecloud.com/dmz-proxy/cos/download/853/build.sh)       |
| fastlane配置 | fastlane.rb | [https://docs.iwhalecloud.com/dmz-proxy/cos/download/853/fastlane.rb](https://docs.iwhalecloud.com/dmz-proxy/cos/download/853/fastlane.rb) |

##### 关于build.sh的说明

###### 能力

1. 该文件用于fastlane打包出iOS工程的ipa包；

###### 准备工作

1. 规范的pch文件，用于切换工程内部环境数据；
2. 规范的podfile文件；

###### 详细说明

1. 该脚本接收3个外部参数，即使用时 `sh build.sh 1.0.0 100 Preprod`命令中的 `1.0.0`为工程版本号，会修改iOS工程Version，`100`为工程构建编号，修改iOS工程的Build，`Preprod`为iOS工程内部pch文件中华用于切换环境数据的参数（有的项目可能不需要切换环境，可不加该参数）；
2. envVariables方法中定义了一些环境变量，使用该脚本，需要根据实际的项目路径进行修改；
3. uploadCode方法，看各个项目的需求，如果在打包ipa之前，确认当前代码是需要打包的版本，则不需要该步骤；
4. envAction方法，用于切换pch文件中的iOS环境数据，按需调用；
5. podAction方法，主要为了安装pod依赖，同时如果项目没有适配xcode 15，则需要在 `OTHER_LDFLAGS`添加配制项 `-ld64`；
6. ipaBuild方法，主要用于修改iOS工程版本号，以及调用fastlane action，fastlane action中，配置了打包ipa(adhoc)并上传到pgyer的功能；

脚本通用性，目前需要考虑的问题（除了已定的通过脚本参数传入的），可以根据自己项目的具体要求自行优化：

1. scheme
2. bundle identifiler
3. workspace
4. pp文件名称
5. 如何先自动先手动（这样是为了修改bundle ID ，切换不同team 和pp文件的自动化）

##### 关于fastlane.rb的说明

###### 能力

根据配置信息，将项目打包并导出.ipa文件，上传到pgyer

###### 需要替换的参数

- api_key： 替换成用户自己的蒲公英api_key，获取方式查看下方截图，或者自行搜索；
  ![image](uploads/110959/de1944e2-dfc2-4841-aec7-290110311087/image.png)
- gym()：该方法中涉及到的项目信息相关的都需要替换，但大部分信息，在配置文件中我们都提供了自动获取的方式，只需要替换少部分字段，如 `provisioningProfiles` 里面的，其他如果因为工具版本升级或者api更新导致的脚本不可用，用户自行查阅资料解决
- 注释：配置文件中，注释的信息有时候也可能会对你有所帮助

#### 制品上传

##### ipa上传到pgyer

- [使用 Fastlane 上传 App 到蒲公英](https://www.pgyer.com/doc/view/fastlane)，在上面的fastlane配置文件也有对应的示例
- 使用shell脚本，参照[官方示例](https://github.com/PGYER/upload-app-api-example/blob/main/shell-demo/pgyer_upload.sh)

##### ipa上传到对象存储桶

研发云有“对象存储服务”，可以将ipa制品上传到存储桶

关于存储的说明，请查看[官网说明](https://dev.iwhalecloud.com/portal/zcm-doc/helper/cosdocs/zh/index.html#/didcjtgm3?id=%e5%85%b3%e4%ba%8e%e6%a1%b6%e7%9a%84%e8%af%b4%e6%98%8e)

下方步骤介绍一下，在流程中，如何将.ipa上传到对象存储桶，对照下方存储桶信息填写即可(代码中没有.ipa，用tt.sh文件作为示例代替)

![image](uploads/113737/5e7170ab-1877-4f86-8e71-9af73d5af16b/image.png)

![image](uploads/113737/21d7269d-a9b0-44a0-b530-6a6e073fa3bd/image.png)

- 模式：选择MinIO模式
- EndPoint：MinIO服务地址
- Bucket： MinIO存储桶名称
- Access Key：MinIO Access Key
- Secret Key：MinIO Secret Key
- 源路径：想要上传到存储桶的文件
- 目标路径：上传的文件，放在存储桶的位置

![image](uploads/113737/e4cf248e-d1fc-4dda-b293-cbe405474f72/image.png)

# 本文件评审、修正记录

| 文件名称 | IOS开发规范（Objective-C） |               |               |        |
| -------- | -------------------------- | ------------- | ------------- | ------ |
| 序号     | 流程                       | 拟制人/审核人 | 拟制/审核时间 | 版本号 |
| 1        | 编写                       | APP规范组(Objective-c)      | 2022/12/01    | V0.1   |
| 2        | 增加持续构建步骤，指导开发人员在研发云上进行ios持续构建的配置  | 王小虎      | 2025/2/12    | V0.2   |
| 3        |  1. 3.6.2章节由强制改为建议；2. 修正括号有歧义的条款   | APP规范组(Objective-c)      | 2025/3/18    | V0.3   |
| 4        |  增加3.23.1章节 【强制】禁止使用废弃的API（规范来源：利比亚项目测试环境）  | 王小虎      | 2025/3/24    | V0.4   |
| 5        | 正式发布                       | APP规范组(Objective-c)      | 2025/04/14    | V1.0   |
| 6        | 根据反馈意见调整oclint阈值：<br>“3.12.8. 【强制】禁止一个类有太多的方法，证明他做了太多的事儿，不利于理解。应该考虑重构”oclint阈值调整为25<br>“3.12.6. 【强制】禁止类的行数过多”oclint阈值调整为800        | 王小虎     | 2025/11/18    | V1.0.1   |
| 7        | 发布                       | APP规范组(Objective-c)      | 2025/11/24    | V1.1   |
| 8        | 新增章节“4.9.2. 【强制】禁止使用URL Schemes唤醒应用”(规范来源： 安全治理单11546904 ) <br>新增章节“4.9.3. 【强制】应用在申请用户权限时只申请必要的权限，申请的权限需要用户授予后才能使用”(规范来源： 安全治理单11547236 ) <br>新增章节“4.9.4. 【强制】应用切换到后台时，应该对界面敏感数据进行模糊化处理”(规范来源： 安全治理单11537913 )  <br>新增章节“4.9.5. 【强制】对于包含敏感数据页面应该禁止截图”(规范来源： 安全治理单11537913 )                      |  王小虎      | 2026/3/10    | V1.1.1   |
| 9        | 发布                       | APP规范组(Objective-c)      | 2026/03/23    | V1.2   |
| 10        | 补充规范章节“4.10.3. 【强制】正式发布的包文件需执行安全加固流程对ipa文件执行安全加固” 后的具体验证要求；<br>补充要求 ：执行安全加固后，研发所内的出厂测试、CD，以及现场的UAT、BRT，都必须测试安全加固后的版本，充分验证加固后APP的兼容性（规范来源：故障单号：3796792）|  王小虎    | 2026/05/20    | V1.2.1   |
| 11        | 发布                       | APP规范组(Objective-c)      | 2026/05/25    | V1.3   |

