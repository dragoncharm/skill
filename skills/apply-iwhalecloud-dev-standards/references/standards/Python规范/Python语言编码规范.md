![image](uploads/20132/6e0b352a-6d68-4472-93e1-71c62674ca65/image.png)

# 概述

本文规定了浩鲸科技Python开发的编码规范，并明确各角色的工作职责。随着本规范的发布，以本文为准。

## 编写目的

i.       本规范以 PEP8 为基础

ii.       让不同编码习惯的开发者更好的协作配合

iii.       形成良好的基础编码规范与风格，提高代码安全性、健壮性、可读性

## 适用范围

规范适用于指导对 Python 项目开发编码过程进行规范化约束的软件研发工作。

## 角色和职责

   开发：负责按照规范进行Python编码

   运维：负责根据规范编写运维需要的Python编码

# Python 开发规范

## 命名规范

### 概述

1)  【推荐】名字应该能够标识事物的特性，并且与业务挂钩。

2)  【推荐】名字应该使用英文单词，而不能为拼音。

3)  【推荐】名字可以有两个或三个单词组成，但不应多于 4 个，控制在 3 至 30个字母以内。

4)  【强制】命名不能和关键字冲突。

### 包和模块命名

1)  【强制】包命名采用全小写命名。

2)  【推荐】通过功能命名。

3)  【推荐】模块命名应短小，并且全为小写，如果需要多单词增加可读性，使用下划线进行拼接。

### 类命名

1)  【强制】类命名采用驼峰命名约定，大写字母开头，各个单词首字母大写。

2)  【强制】Activity、Fragment、Service 等命名必须以 Activity、Fragment、Service相应后缀结束。

3)  【推荐】当接口已有文档说明且主要是被用作调用时，也可以使用函数的命名约定。

### 函数命名

1)  【推荐】函数命名都是小写，必要时使用下划线连接各单词提高可读性。

2)  【推荐】只有当已有代码风格已经是混合大小写时，为了保留向后兼容性才使用混合大小写。

3)  【强制】用单下划线(_)开头表示模块函数是 protected 的。

4)  【强制】用双下划线(__)开头的实例方法表示类内私有。

### 变量命名

1)  【强制】变量命都是小写，多单词使用下划线连接。

2)  【推荐】类型变量名称通常应使用简短的驼峰命名，建议将后缀_co 或_contra 添加到用于声明相应的协变和逆变的行为。

**正例**

```python
from typing import TypeVar
VT_co = TypeVar('VT_co'，covariant=True)
KT_contra = TypeVar('KT_contra'，contravariant=True)
```

3)  【强制】类型变量的定义统一放在 import 之后。

4)  【强制】类变量统一放在类注释的之后，所有类函数的之前。

5)  【推荐】全局变量：适用于函数的命名规范。

6)  【强制】用单下划线(_)开头表示模块变量是 protected 的。

7)  【强制】用双下划线(__)开头的实例变量表示类内私有。

### 常量命名

1)  【推荐】全部使用大写并且下划线将单词分开。

### 异常命名

1)  【推荐】由于异常实际上也是类，因此类命名的约定也适用与异常。不同的是，如果异常实际上是抛出错误的话，异常名后应该加上“Error”的后缀。

## 注释规范

### 概述

1)  【推荐】一般情况下源程序的有效注释量必须在 30%以上。

2)  【强制】避免使用装饰性内容，保持注释的简洁。

3)  【强制】注释信息不仅要包括代码的功能，还应给出原因，不要为注释而注释。

4)  【强制】注释不能嵌套。

5)  【强制】避免使用行尾注释。

6)  【推荐】生成开发文档的需要用中文编写。

7)  【推荐】如果需要注释的内容太多，需附加文档进行说明，注释时加上"参见《****》"。

8)  【强制】复杂的分支流程必须注释。

9)  【推荐】代码质量不高但能正常运行，或者还没有实现的代码用# TODO:声明。

10)  【推荐】可以根据[PEP-484]对Python3代码进行类型注释,并且在build时用类型检查工具例如[pytype]进行类型检查。

**正例**

```python
def func(a: int) -> List[int]:
```

11)  【参考】存在错误隐患的代码用# FIXME:声明。

### 程序文件注释

1)  【强制】采用文档字符串的形式进行注释（三个双引号的形式）。

2)  【参考】应该包含如下：

**正例**

```python
#  文件描述  （Description）：描述此类的作用；

#  作者  （Author）：创建者或者修改者名；

#  版本  （Version）：创建或者修复时的编号，需要自行在 bug 管理系统中创建 bug 号，使用 bug 号进行命名（若无 bug 管理工具的临时办法：如无 bug 号，从 1 开始，修改时依次增加）；

#  日期（Date）：创建或者修改时的日期，使用“-”进行年月日分割；

#  记录（Record）：创建或者修改的工作内容描述；
```

###  类注释

1)  【强制】类应该在其定义下有一个用于描述该类的文档字符串。

2)  【推荐】如果你的类有公共属性(Attributes)，那么文档中应该有一个属性(Attributes)段。并且应该遵守和函数参数相同的格式。

###  函数和方法注释

下文所指的函数,包括函数，方法，以及生成器。

1)  【强制】一个函数必须要有文档字符串，除非它满足以下条件之一。

i.       外部不可见

ii.       非常短小

iii.       简单明了

2)  【强制】文档字符串应该包含函数做什么，以及输入和输出的详细描述。通常不应该描述"怎么做"，除非是一些复杂的算法。当开发人员调用该函数时， 文档字符串应该提供足够的信息，而无需看代码。对于复杂的代码，在代码旁边加注释会比使用文档字符串更有意义。

3)  【参考】关于函数的几个方面应该在特定的小节中进行描述记录，这几个方面如下文所述。每节应该以一个标题行开始，标题行以冒号结尾。除标题行外，节的其他内容应被缩进 2 个空格。

4)  【参考】Args:

列出每个参数的名字,并在名字后使用一个冒号和一个空格，分隔对该参数的描述。如果描述太长超过了单行 80 字符,使用 2 或者 4 个空格的悬挂缩进(与文件其他部分保持一致)。描述应该包括所需的类型和含义。如果一个函数接受\*foo(可变长度参数列表)或者**bar(任意关键字参数)，应该详细列出\*foo 和\**bar。

5)  【参考】Returns: (或者 Yields: 用于生成器)

描述返回值的类型和语义。如果函数返回 None，这一部分可以省略。

6)  【参考】Raises:

列出与接口有关的所有异常。

### 块注释和行注释

1)  【强制】块注释一般写在对应的代码之前，并且和对应的代码有同样的缩进级别。

2)  【强制】块注释的每一行都应该以#和一个空格开头（除非该文本是在注释内缩进对齐的）。

3)  【强制】块注释中的段落应该用只含单个#的一行隔开。

### 行内注释

1)  【参考】尽量少用行内注释。

2)  【参考】行内注释是和代码语名写在一行内的注释。行内注释应该至少和代码语句之间有两个空格间隔，并且以#和一个空格开始。

## 格式规范

### 概述

1)  【强制】代码未写，文档先行。注释必须按照统一的范式编写。

2)  【强制】不许使用复杂的运算表达式，必要时添加括号而不依赖于优先级。

### 缩进

1)  【强制】缩进使用 4 个空格，空格是首选的缩进方式。

2)  【强制】禁止混用空格和 Tab。

### 换行

1)  【推荐】每行代码的最大长度不该超过 80 个字符，以下情况除外：

i.       长的导入模块语句

ii.       注释里的 URL

###  空白行

1)  【强制】使用 2 个空行来分隔最外层的函数(function)和类(class)定义。

2)  【强制】使用 1 个空行来分隔类中的方法(method)定义。

3)  【推荐】在函数内使用空行（尽量少）使代码逻辑更清晰。

### 对齐

1)  【强制】不要用空格来垂直对齐多行间的标记，因为这会成为维护的负担(适用于:，#，=等)。

2)  【推荐】续行应该与包裹元素对齐，要么使用圆括号，方括号，花括号内的隐式行连接来垂直对齐，要么使用挂行缩进对齐。

垂直对齐：

**正例**

```python
def long_function_name(var_one，var_two,                                            

                       var_three，var_four):                      

 print(var_one)   
```

### 库的导入

1)  【强制】每个导入应该独占一行。

2)  【强制】使用 import 开头的导入，一行只能导入一个库，禁止使用逗号分开， 导入多个库。

3)  【推荐】使用 from import 形式的导入，一行只能导入一个库，特殊情况下可以使用逗号分开导入多个库。

4)  【强制】导入总应该放在文件顶部，位于模块注释和文档字符串之后，模块全局变量和常量之前。导入应该按照从最通用到最不通用的顺序分组：

i.       标准库的导入

ii.       第三方库的导入

iii.       应用程序指定导入

5)  【推荐】使用绝对(absolute)import，因为这样通常更易读，在 import 系统没有正确配置（比如中的路径以 sys.path 结束）的情况下，也会有更好的表现

（或者至少会给出错误信息）：

**正例**

```python
import mypkg.sibling                                               

from mypkg import sibling                                               

from mypkg.sibling import example  
```

                                             

6)  【强制】隐式相对 import 是禁止使用的。

显示导入和隐式导入说明假设有如下包结构：

**正例**

```python
thing

├── books

│      ├── adventure.py

│      ├── history.py

│      ├── horror.py

│      ├── init.py

│      └── lovestory.py

├── furniture

│      ├── armchair.py

│      ├── bench.py

│      ├── init.py

│      ├── screen.py

│      └── stool.py

└──    init.py
```

7)  【推荐】显式的相对 import 也是一种可以接受的方式，标准库代码应当一直使用绝对 import，避免复杂的包布局。

**正例**

```python
from . import sibling                                                

from .sibling import example       
```

                                         

### 字符串

1)  【强制】避免在循环中用+和+=操作符来累加字符串。主要原因：

i.       字符串是不可变的，每一次的赋值，原来引用的对象没有及时被删除（系统有机制回收内存，但是不及时），增加内存负担。
ii.       随着字符串的累加，长度越来越长写入的时间也逐渐增加所以如果循环规模比较大，效率就明显下降。
iii.       推荐将每个字符串都记入一个列表并使用''.join来将列表在循环结束后连接(或将每个子字符串写入io.BytesIO缓存)。

**<font color="red">反例</font>**

```python
employee_table = '<table>'
for last_name, first_name in employee_list:
    employee_table += '<tr><td>%s, %s</td></tr>' % (last_name, first_name)
employee_table += '</table>'
```

**正例**

```python
items = ['<table>']
for last_name, first_name in employee_list:
    items.append('<tr><td>%s, %s</td></tr>' % (last_name, first_name))
items.append('</table>')
employee_table = ''.join(items)
```

2)  【推荐】在同一个文件中，保持使用字符串引号的一致性。使用单引号'或者双引号"之一用以引用字符串，并在同一文件中沿用。
3)  【推荐】优先使用f-string,%,或者str.format格式化字符串而非做字符串拼接，代码可读性更好。

### 空值比较

1)  【推荐】通用使用 if foo is None: 形式来比较空值。

### 日志输出

1)  【推荐】 推荐使用logging而非print打印日志，logging的优点是：
i.       可以控制消息的级别，过滤掉那些并不重要的消息。
ii.       可决定输出到什么地方，以及怎么输出。有许多的重要性别级可供选择，debug、info、warning、error以及critical。通过赋予logger或者handler不同的级别，就可以只输出错误消息到特定的记录文件中，或者在调试时只记录调试信息。

**正例**

```python
import logging
# level=logging.DEBUG 、INFO 、WARNING、ERROR、CRITICAL
def log_testing():
    logging.basicConfig(level=logging.ERROR)
    logging.debug('debug，用来打印一些调试信息，级别最低')
    logging.info('info，用来打印一些正常的操作信息')
    logging.warning('waring，用来用来打印警告信息')
    logging.error('error，一般用来打印一些错误信息')
    logging.critical('critical，用来打印一些致命的错误信息，等级最高')

log_testing()
```

### 表达式和语句中的空格

1)  【推荐】以下情况避免无关的空格：

i.       在括号或大括号内

**<font color="red">反例</font>**

```python
spam( ham[ 1 ], { eggs: 2 } )
```

**正例**

```python
spam(ham[1], {eggs: 2})
```

ii.       在尾随逗号和后面的右括号之间

**<font color="red">反例</font>**

```python
bar = (0, )
```

**正例**

```python
bar = (0,)
```

iii.       在逗号，分号或冒号前面

**<font color="red">反例</font>**

```python
if x == 4 : print x , y ; x , y = y , x  
```

**正例**

```python
if x == 4: print x, y; x, y = y, x  
```

iv.       紧接在开始函数调用的参数列表的开括号之前

**<font color="red">反例</font>**

```python
spam (1)
```

**正例**

```python
spam(1)
```

v.       紧接在开始括号之前，开始索引或切片

**<font color="red">反例</font>**

```python
dct ['key'] = lst [index]
```

**正例**

```python
dct['key'] = lst[index]
```

vi.       在一个赋值（或其他）运算符周围有多于一个的空间来对齐它

**<font color="red">反例</font>**

```python
x             = 1
y             = 2
long_variable = 3
```

**正例**

```python
x = 1
y = 2
long_variable = 3
```

2)  【参考】其他建议

i.       总是围绕这些二元运算符在两侧使用一个空格

**<font color="red">反例</font>**

```python
x=3
i+=1
```

**正例**

```python
x = 3
i += 1
```

ii.       用于指示关键字参数或默认参数值时，不要在=符号周围使用空格

**<font color="red">反例</font>**

```python
return magic(r = real, i = imag)
```

**正例**

```python
return magic(r=real, i=imag)
```

# Linux系统下安装miniconda以及pylint

## 概述

Miniconda是一个轻量级、免费且开源的跨平台软件包管理系统，它提供了conda这个全能的包管理器。
Pylint 是一个 Python 代码分析工具，它分析 Python 代码中的错误，查找不符合代码风格标准和有潜在问题的代码，除了平常代码分析工具的作用之外，它提供了更多的功能：如检查一行代码的长度，变量名是否符合命名标准，一个声明过的接口是否被真正实现等等。

## miniconda安装及基本用法

### 安装

1)推荐到[清华大学开源软件镜像网站](https://mirrors.tuna.tsinghua.edu.cn/)，在输入框检索anaconda后点击，如下图所示。
![image](uploads/80429/636fc676-70cf-43b3-845b-285df1b59642/image.png)
2)点击miniconda,如下图所示。
![image](uploads/80429/04c6ceb8-2da5-4921-a4b8-6c609e9c509f/image.png)
3)找到适合你的Linux系统版本的Miniconda安装程序，这里以Linux-x86_64为例，右键复制链接地址。
![image](uploads/80429/1caa62f0-ce8c-4ca3-833a-a6a4f5d45afd/image.png)
4)打开终端，利用wget命令下载并运行对应的sh文件安装程序。

```bash
wget https://mirrors.tuna.tsinghua.edu.cn/anaconda/miniconda/Miniconda3-py39_24.4.0-0-Linux-x86_64.sh
bash Miniconda3-py39_24.4.0-0-Linux-x86_64.sh
```

5)验证是否安装成功。
在终端输入以下命令，如果可以看到conda的版本信息，那么恭喜你！安装成功啦！

```bash
conda --version
```

### 基本用法

1)配置镜像源
为了加速conda包的下载速度，你可以配置conda使用国内的镜像源。这可以通过修改~/.condarc文件来实现。例如，你可以将channels和show_channel_urls配置项设置为使用清华大学的conda镜像。

```bash
channels:
  - defaults
  - https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/main/
  - https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/r/
  - https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud/conda-forge/
show_channel_urls: true
default_channels:
  - https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/main/
  - https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/r/
  - https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud/conda-forge/
custom_channels:
  conda-forge: https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud
  msys2: https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud
  bioconda: https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud
  menpo: https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud
  pytorch: https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud
```

2)常用命令

```bash
conda create -n py38 python=3.8 #创建一个名为py38的新环境，并安装Python 3.8。
conda activate py38 #激活名为py38的环境。
conda deactivate #退出当前激活的环境。
conda install package_name #在当前环境中安装包名为package_name的包。
conda remove package_name #在当前环境中卸载包名为package_name的包。
conda env list #列出所有已创建的环境。
conda env export > environment.yml #导出当前环境的配置信息到environment.yml文件中。
conda env create -f environment.yml #根据environment.yml文件中的配置信息创建一个新的环境。
```

## Pylint安装及基本用法

### 安装

在安装好miniconda后，我们可以使用以下命名安装代码分析工具Pylint

```bash
conda install pylint
pylint --version # 查看是否安装成功
```

![image](uploads/80429/f0ab971f-b28b-4fe3-8680-58d79b914820/image.png)

### 基本用法

1)查看帮助信息

```bash
pylint -h
或
pylint --help
 
--generate-rcfile
生成一个配置文件示例；
可以使用重定向把这个配置文件保存下来用做以后使用；
也可以在前面加上其它选项，使这些选项的值被包含在这个产生的配置文件里；
如：“pylint --persistent=n --generate-rcfile > pylint.conf”，查看 pylint.conf，可以看到 persistent=no，而不再是其默认值 yes；
 
 
--rcfile=<file>
指定一个配置文件；
把使用的配置放在配置文件中，这样不仅规范了自己代码，也可以方便地和别人共享这些规范；
如：pylint --rcfile=pylint.conf s1.py
使用pylint.conf这个配置文件来对s1.py进行检查
 
-i <y_or_n>, --include-ids=<y_or_n>
在输出中包含 message 的 id, 然后通过“pylint --help-msg=<msg-id>”来查看这个错误的详细信息，这样可以具体地定位错误。
 
 
-r <y_or_n>, --reports=<y_or_n>
表示 Pylint 的输出中是否包含报告部分；
 
 
--files-output=<y_or_n>
将每个 module /package 的 message 输出到一个以 pylint_module/package. [txt|html] 命名的文件中；
如果有 report 的话，输出到名为 pylint_global.[txt|html] 的文件中。默认是输出到屏幕上不输出到文件里；
 
 
-f <format>, --output-format=<format>
设置输出格式；
可以选择的格式有 text, parseable, colorized, msvs (visual studio) 和 html, 默认的输出格式是 text；
 
 
--disable-msg=<msg ids>
禁止指定 id 的 message；
例如：输出中包含了 W0402 这个 warning 的 message, 如果不希望它在输出中出现，可以使用“--disable-msg= W0402”；
```

2)导出配置

```bash
# 生成默认配置文件
pylint --persistent=n --generate-rcfile > pylintrc
# 路径下会生成一个pylint.conf文件，都是pylint的默认配置,这个可以自行修改，为了跟团队项目统一
```

3)检查单个Python文件

```bash
# 检查单个py文件，指定使用刚刚生成的默认配置文件，不指定，也是使用默认
pylint --rcfile=pylintrc s1.py
```

![image](uploads/80429/cb07c8a8-fa09-4ea6-9bdc-1bfd98d6e998/image.png)
4)检查整个项目

```bash
### 注意：检查整个项目，一定要在项目路径下新建__init__.py,否则会报错
# 切换到上一层
cd .. 
# 执行
pylint pylint_demo
# 修改过后再执行，下图是对比
```

![image](uploads/80429/b68aa0c9-61a8-4294-8e96-08c07bbb2b61/image.png)
5)生成报告

```bash
# 执行
pylint -ry pylint_demo
#### 说明######
1 Pylint结果的级别：error，warning，refactor，convention；
2 可以根据首字母确定相应的级别，例如，C表示convention（规范）、W表示warning（告警）、E表示error（错误）；
3 级别之后的数字表示告警所在文件中的行号和列号；
4 参数 “-ry”开启报告，“-rn”关闭报告（只显示警告和错误），默认为关闭报告；

```

# 试飞构建

1. 进入云雀研发云（https://dev.iwhalecloud.com）并登陆，点击有上角菜单——>开发中心——>持续构建，如下图：

![image](uploads/80429/99d37bc4-a776-4b44-a28d-79ae19994a3b/image.png)

2. 进入持续构建页面后点击新建构建，进入新建页面如下图，配置应用模块，在语言模板处选择Python，最后选择要构建的的镜像（建议选择3.8版本），点击【下一步】。

![image](uploads/80429/bae7275e-e255-46b9-9ec9-0511c1c6609b/image.png)

3. Maven私服页面，选择不使用Maven私服，直接点击【下一步】。

![image](uploads/80429/985fa427-c402-47d4-9bb7-f0039480da9f/image.png)

4. 代码检查页面，不打开代码检查，不需要单元测试，直接点击【下一步】。

![image](uploads/80429/2d6ca4f3-06b7-4232-841d-a3a216ff08d4/image.png)

5. 制作镜像页面，不制作镜像，直接点击【下一步】。

![image](uploads/80429/45978823-8dd5-43ee-81a1-65f640580993/image.png)

6. 推送更新页面，不开启推送，直接点击【下一步】。
   ![image](uploads/80429/11d21fd9-f9d2-47da-bef3-d46aadc418e4/image.png)

7. 自动化回归页面，不开启自动化回归，直接点击【新建构建】按钮。
   ![image](uploads/80429/5b30ce79-3547-468b-8c66-af1af1f0b054/image.png)

8. 进入流程构建页面。点击【高级配置】按钮，展开高级配置。打开Maven本地缓存，打开NPM本地缓存，构建方式选择【平台构建】。
   ![image](uploads/80429/2a4cadf8-a352-4b6f-a1db-4e83d71c33af/image.png)

9. 点击【代码下载】，展开代码下载信息页面。【类型】选择“GIT”，关闭“浅克隆”和关闭“使用令牌”；用户名和密码填写zmp的账号及密码；填写git上的代码路径和下载分支。
   ![image](uploads/80429/baa3ed65-d78c-4615-ac63-f935c23fda9b/image.png)

10. 点击【代码编译】右上角的【x】。将改流程删除。
    ![image](uploads/80429/5bebc4ac-0147-4d32-a3b2-79cd3a74845a/image.png)

11. 点击【代码下载】和【end】之间的【+】，添加【代码分析】流程。
    ![image](uploads/80429/ea9262ce-647f-4630-9b0e-6a77de28aad7/image.png)
    ![image](uploads/80429/a5e27280-f827-4f9e-8434-83e98b88a9bd/image.png)

12. 代码分析页面，不填写任何信息，直接点击【保存】即可创建代码构建流程。
    ![image](uploads/80429/5b1db43c-2396-431a-95e0-d2e57ba486b1/image.png)

# 本文件评审、修正记录

| 文件名称 | Python语言编码规范                                            |               |               |        |
| -------- | ------------------------------------------------------------ | ------------- | ------------- | ------ |
| 序号     | 流程                                                         | 拟制人/审核人 | 拟制/审核时间 | 版本号 |
| 1        | 编写                                                         | 张翊/沈广盼/马驰 | 2023/03/06    | V0.1   |
| 2        | 根据公开评审意见进行规范修订                                    | 张翊/沈广盼/马驰/罗辉 | 2023/03/17    | V0.2   |
| 3        | 发布                                    | Python规范组 | 2023/03/22    | V1.0   |
| 4        | 增加第三章节Linux系统下安装miniconda以及pylint安装用法；增加第四章节Python试飞构建配置方法；                                   | 张翊/杨纪中/胡东浩/陈思焱 | 2024/06/20    | V1.0.1   |
| 5        | 发布                                    | Python规范组 | 2024/06/20    | V1.1   |
