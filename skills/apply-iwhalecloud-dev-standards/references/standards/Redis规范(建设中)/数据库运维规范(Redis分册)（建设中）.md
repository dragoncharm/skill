![image](uploads/4076/52a66472-0d83-4943-9e8f-421935d752aa/PG_operation_Redis.png)

# 运维规范

| 重要程度 | 规范                                                         | 说明                                                         |
| -------- | ------------------------------------------------------------ | ------------------------------------------------------------ |
| ★★★★★    | <span style='color:red'>避免高耗时或高风险的命令： KEYS、FLUSHALL、FLUSHDB</span> | 生产环境中，无限制地使用高风险命令可能带来诸多问题：<br />1. 执行**FLUSHALL**、**FLUSHDB**命令会直接清空全部数据，并阻塞Redis服务：如果一定要清空数据时，需要使用**FLUSHDB ASYNC**来进行异步删除<br />2. 执行**KEYS**同样会阻塞Redis服务：应该使用多次精确查询或**SCAN**命令来代替 |
| ★★★★★    | <span style='color:red'>为核心指标配置监控报警</span>        | 为ZCache主机的**CPU**使用率、**内存**使用率、**带宽**使用率、**磁盘**使用率等核心指标配置监控报警，实时掌握实例运行状态 |
| ★★★★☆    | <span style='color:red'>定期检缓存服务状态</span>            | 通过Manager管理平台可快速查看缓存服务运维状态：节点状态、键值数、访问量、内存使用量等信息 |

# 日常运维

> **备注**：以下运维操作使用的工具（例如redis-cli、rc-start.sh等）可直接在缓存用户（即ZCache安装部署时指定的系统用户，例如：zcache、zcache_spc、zcache_aof、zcache_cdr、zcache_irc等用户）下执行，而无需指定路径信息（因为命令所在路径已经添加至`PATH`环境变量中）。

## 停止缓存服务

### 方式一：通过ZCM停止服务

登陆**ZCM管理门户**(也即**云雀研发云**)，打开菜单：**中间件中心** -> **中间件管理**，找到要操作的ZCache服务，操作菜单中点击`停止服务`：

![image](uploads/4076/3bf3163f-8d63-46e0-8ac0-f8152bec4c3a/zcm_stop_zcache.png)

### 方式二：通过rc-stop.sh工具停止服务

使用`rc-stop.sh`工具能够一键停止对应的缓存服务。

1. 使用ssh登陆到缓存服务所在的任一主机上

   > 只要在其中一台主机上执行停止集群工具即可

2. 切换到缓存服务所在的系统用户下（如果已经是使用缓存用户ssh到主机，那省略该步骤）：`su - 缓存用户名`

   > **缓存服务所在的系统用户**：即安装部署时指定的系统用户，例如：zcache、zcache_spc、zcache_aof、zcache_cdr、zcache_irc等。
   >
   > **备注**：在缓存服务主机上可通过`ps -ef|grep redis-server`命令来查看当前主机上运行的redis进程，其中第一列即为进程所属的系统用户
   >
   > ![image](uploads/4076/b9157c14-f07b-4459-b54e-a396636ae454/ps_redis_server.png)

3. 直接执行工具停止服务：`rc-stop.sh`

   ![image](uploads/4076/545d7f42-e5d3-4612-bd64-e9f1442efded/rc-stop.png)

   > **备注**：停止完成后，可通过`ps -ef|grep redis-server`命令验证对应的redis进程已不在。

## 启动缓存服务

### 方式一：通过ZCM启动服务

登陆**ZCM管理门户**(也即**云雀研发云**)，打开菜单：**中间件中心** -> **中间件管理**，找到要操作的ZCache服务，操作菜单中点击`启动服务`：

![image](uploads/4076/11f2eb63-1973-483f-8277-f45c9e57d812/zcm_start_zcache.png)

### 方式二：通过rc-start.sh工具启动服务

使用`rc-start.sh`工具能够一键停止对应的缓存服务。

1. 使用ssh登陆到缓存服务所在的任一主机上

   > 只要在其中一台主机上执行启动集群工具即可，工具会自动使用ssh登陆到其他主机来启动各个服务节点

2. 切换到缓存服务所在的系统用户下（如果已经是使用缓存用户ssh到主机，那省略该步骤）：`su - 缓存用户名`

   > **缓存服务所在的系统用户**：即安装部署时指定的系统用户，例如：zcache、zcache_spc、zcache_aof、zcache_cdr、zcache_irc等。

3. 直接执行工具启动服务：`rc-start.sh`

   ![image](uploads/4076/d257d88b-d549-4356-92b9-89f19ec7e83f/rc-start.png)

   > **备注**：
   >
   > - 启动过程中有进度提示，当启动完成后，进度展示为`100%`，启动工具随后执行结束。
   > - 启动完成后，可通过`ps -ef|grep redis-server`命令验证对应的redis进程已存在。

## 缓存服务状态查看

### 方式一：通过Manager检查

1. 登陆**中间件管理门户**，打开菜单：**分布式缓存管理** -> **缓存库管理**，找到要检查的ZCache服务

   ![image](uploads/4076/3c5946ca-6502-4553-b8a6-f1fd71c59c4c/manager_zcache.png)

2. 点击该缓存服务实例(**zcache_yu**)可进入查看服务运行状态详情：

   ![image](uploads/4076/d2831890-ff20-4322-9832-d714ea945399/manager_cluster_status.png)

### 方式二：通过rc-tool.sh工具检查

使用`rc-tool.sh`工具能够检查缓存集群的运行情况。

1. 使用ssh登陆到缓存服务所在的任一主机上

   > 只要在其中一台主机上执行检查缓存状态的工具即可

2. 切换到缓存服务所在的系统用户下（如果已经是使用缓存用户ssh到主机，那省略该步骤）：`su - 缓存用户名`

   > **缓存服务所在的系统用户**：即安装部署时指定的系统用户，例如：zcache、zcache_spc、zcache_aof、zcache_cdr、zcache_irc等。
   >
   > **备注**：在缓存服务主机上可通过`ps -ef|grep redis-server`命令来查看当前主机上运行的redis进程，其中第一列即为进程所属的系统用户。

3. 直接执行工具检查缓存集群运行状态：`rc-tool.sh nodes` （如果缓存服务设置了访问密码，那么需要增加`-a '密码'`参数：`rc-tool.sh -a '密码' nodes`）

   ![image](uploads/4076/509eaed1-497f-43d9-ac59-0761d4060eac/rctool_nodes.png)

   **集群运行状态信息说明**：

   工具展示的内容包含上下两部分：集群节点信息和集群汇总信息

   - **集群节点信息**
     - **SERVER**：Redis服务节点的`IP:端口`
     - **STATUS**：节点状态，`OK`-正常；`FAIL`-异常
     - **ROLE**：角色，`master`-主节点;`slave`-从节点
     - **VERSION**：版本号
     - **UPTIME**：已持续运行时长，单位：秒
     - **KEYS**：节点存储的缓存键值数
     - **USEMEM**：节点使用的内存大小
     - **CLIENTS**：节点当前连接的客户端数
     - **OPS**：节点当前每秒执行的命令请求数
     - **ELAPSED**：节点访问时延，单位：微秒
     - **SLOTS**：主节点拥有的分片槽位数（从节点为空）
   - **集群汇总信息**：其中每项都有两个值，以/间隔；分别代表**主节点统计信息**和**集群所有节点统计信息**
     - **NODES**：节点数
     - **KEYS**：键值数
     - **USEMEM**：使用内存大小
     - **CLIENTS**：客户端连接数
     - **OPS**：每秒执行命令数

## 参数查询修改

<span style='color:red'>**注意**：通常情况下我们只需要查看参数取值，不需要进行参数调整</span>

### 方式一：通过Manager处理

1. 登陆**中间件管理门户**，打开菜单：**分布式缓存管理** -> **缓存库管理**，找到要检查的ZCache服务

   ![image](uploads/4076/d06d5f8d-4ece-4aac-b111-1acaff8f644e/manager_zcache.png)

2. 点击该缓存服务实例(**zcache_yu**)可进入缓存库服务详情页面，选择要查看参数的`节点详情`按钮：

   ![image](uploads/4076/c7694806-640c-44f9-b349-28dcb3561b9a/manager_nodeinfo.png)

3. 进入服务节点详情页面后，切换到`节点配置`Tab页，可以查找相关参数取值，其中存在编辑按钮的参数，表示允许进行在线修改

   ![image](uploads/4076/426063da-1629-4bf0-b2e1-e3ad90257ce7/manager_node_config.png)

> **说明**：通过Manager查看修改，相对操作简单。但是如果要全量查询/修改所有节点的某个参数，需要逐个节点处理，操作繁琐，这种场景下可采用方式二进行处理

### 方式二：通过rc-setconfig.sh工具处理

使用`rc-setconfig.sh`工具可以方便的对所有节点进行指定参数查询和在线修改处理：

> **注意**：并不是所有参数都支持在线修改，例如`dir`、`port`、`bind`等参数就不允许在线修改，具体可以通过Manager中`节点配置`页面查看哪些参数允许在线修改。

1. 使用ssh登陆到缓存服务所在的任一主机上

   > 只要在其中一台主机上执行参数访问工具即可

2. 切换到缓存服务所在的系统用户下（如果已经是使用缓存用户ssh到主机，那省略该步骤）：`su - 缓存用户名`

   > **缓存服务所在的系统用户**：即安装部署时指定的系统用户，例如：zcache、zcache_spc、zcache_aof、zcache_cdr、zcache_irc等。
   >
   > **备注**：在缓存服务主机上可通过`ps -ef|grep redis-server`命令来查看当前主机上运行的redis进程，其中第一列即为进程所属的系统用户。

3. **查询集群服务参数**：`rc-setconfig.sh -a '密码' 参数名`

   ```shell
   # 命令格式：rc-setconfig.sh -a '密码' 参数名
   # 备注：其中如果缓存服务没有设置访问密码，那么不需要设置-a参数
   # 示例：查询loglevel参数取值，可以看到各个节点日志级别参数值都是notice
   $ rc-setconfig.sh loglevel
   2021-07-05 16:36:54  *  Process config on all nodes ...
   2021-07-05 16:36:54  *  Get the value of <loglevel> :
   ================================================================================
    SERVER                | loglevel
   --------------------------------------------------------------------------------
    172.16.17.3:7620      | "notice"
    172.16.17.3:7621      | "notice"
    172.16.17.4:7620      | "notice"
    172.16.17.4:7621      | "notice"
   ================================================================================
   $ 
   ```

4. **修改集群服务参数**：`rc-setconfig.sh -a '密码' -w 参数名 参数值`

   ```shell
   # 命令格式：rc-setconfig.sh -a '密码' -w 参数名 参数值
   # 备注：其中如果缓存服务没有设置访问密码，那么不需要设置-a参数；
   #      -w参数表示参数值会被同时写入配置文件中($HOME/conf/redis-端口号.conf),这样节点重启后修改的参数值仍有效
   # 示例：在线修改集群中各节点的日志级别(loglevel)参数未warning。
   # （未使用-w参数，所以参数不会被修改至配置文件中，节点重启后仍使用配置文件中原有日志级别的配置）
   $ rc-setconfig.sh loglevel warning
   2021-07-05 16:46:30  *  Process config on all nodes ...
   2021-07-05 16:46:30  *  [172.16.17.3:7620]: CONFIG SET loglevel warning : [OK]
   2021-07-05 16:46:30  *  [172.16.17.3:7621]: CONFIG SET loglevel warning : [OK]
   2021-07-05 16:46:30  *  [172.16.17.4:7620]: CONFIG SET loglevel warning : [OK]
   2021-07-05 16:46:30  *  [172.16.17.4:7621]: CONFIG SET loglevel warning : [OK]
   2021-07-05 16:46:30  *  Get the value of <loglevel> :
   ================================================================================
    SERVER                | loglevel
   --------------------------------------------------------------------------------
    172.16.17.3:7620      | "warning"
    172.16.17.3:7621      | "warning"
    172.16.17.4:7620      | "warning"
    172.16.17.4:7621      | "warning"
   ================================================================================
   ```

## 服务日志查询

### 服务日志路径

缓存服务日志存在于数据目录中（即安装部署时配置的数据目录），可通过如下几种方式获取数据目录路径

- 方式一：通过[<u>参数查询修改</u>](#参数查询修改)来查看数据目录参数`dir`的取值

- 方式二：使用缓存用户ssh登陆至缓存主机上，直接查询配置文件，检查本机redis服务节点的数据目录：

  ```shell
  # 示例：节点配置文件在$HOME/conf/目录下，配置文件命名格式：redis-端口号.conf
  # 7620节点的数据目录：/home/yugj/data/7620/
  # 7621节点的数据目录：/home/yugj/data/7621/
  $ grep dir $HOME/conf/redis-*.conf
  /home/yugj/conf/redis-7620.conf:dir /home/yugj/data/7620/
  /home/yugj/conf/redis-7621.conf:dir /home/yugj/data/7621/
  ```

### 服务日志获取

进入节点的数据目录中，可以查看到服务日志，其命名格式：`redis-端口号.log`

> **备注**：ZCache V9.0.18版本开始，`rc-tool.sh`工具增加了**logs**子命令来把集群下的所有节点的日志归集到一起打包，方便日志下载
>
> ![image](uploads/4076/88fb69d5-039c-4a02-ac69-b499747d39a2/V9.0.18-logs.png)

## 缓存数据查询

### 方式一：通过Manager查看

1. 登陆**中间件管理门户**，打开菜单：**分布式缓存管理** -> **缓存库管理**，找到要检查的ZCache服务

   ![image](uploads/4076/46fb48a2-f8c8-4990-8a03-d013c5e923e2/manager_zcache.png)

2. 点击该缓存服务实例(**zcache_yu**)可进入缓存库服务详情页面，点击`缓存查询`按钮可进入查询页面：

   ![image](uploads/4076/b9e33ff6-22dd-495a-9988-8aaf65985546/manager_query.png)

3. 进入**缓存查询**页面后，在输入**缓存键名**后，点击`缓存查询`按钮（或直接键盘`回车`），即可查询指定key，如果无法精确匹配到键值，则会自动进行模糊查询（模糊查询会比较耗时，用户可以点击弹出的取消按钮，来终止模糊查询）：<span style='color:red'>生产环境下，请尽可能使用精确键查询</span>

   ![image](uploads/4076/81e0a372-88c2-4747-b460-792281d7a8f8/manager_getkey.png)

   **查询结果说明**：查询结果在下方展示，分为左右两块区域：**缓存键**、**缓存键信息**

   - **缓存键**：位于左侧区域；鼠标点击某个键，将会在右侧展示**缓存键信息**

   - **缓存键信息**：主要包含5项信息

     - **对象类型**：string、list、hash、set、zset等类型
     - **元素个数**：string类型对应的是值的长度；而对于其他类型，即为其中包含的元素数
     - **生命周期**：展示键值剩余的生存时长（单位：秒），其中**-1**表示键值不会自动过期失效
     - **归属节点**：即该键值所存储的服务节点地址信息
     - **缓存键值列表**：里面为缓存键值的详细数据内容

### 方式二：通过redis-cli工具查看

以缓存系统用户登陆ZCache主机后，可以使用redis-cli工具来进行缓存数据查询访问操作，相关使用详情请查看对应链接：

- redis-cli工具使用介绍：[<u>redis-cli说明</u>](#redis-cli)
- 字符串(String)查询命令：[<u>GET</u>](#get：获取字符串缓存key的值)
- 哈希(Hash)查询命令：[<u>HMGET</u>](#hmget：获取哈希缓存key的多个域值)
- 列表(List)查询命令：[<u>LRANGE</u>](#lrange：获取列表指定区间内的元素)
- 集合(Set)查询命令：[<u>SMEMBERS</u>](#smembers：获取集合缓存key中的所有元素)
- 有序集合(ZSet)查询命令：[<u>ZRANGE</u>](#zrange：获取有序集合缓存key指定区间内元素列表)

**使用示例**：

```shell
# 使用人机交互方式来执行redis-cli工具，进入交互指令界面进行缓存数据查询
$ redis-cli -h 127.0.0.1 -p 6379 -c
127.0.0.1:6379> get strkey   		# 查询String类型缓存key：strkey
"value"
127.0.0.1:6379> hmget hashkey field1 field2 nofield 	# 查询Hash类型缓存key中的指定元素：hashkey
1) "foo"   	# field1域的值
2) "bar"	# field2域的值
3) (nil)	# nofield域的值(nil表示哈希key中无该域)
127.0.0.1:6379> lrange listkey 0 1  # 查询List类型缓存key中的前两个元素：listkey
1) "one"
2) "two"
127.0.0.1:6379> smembers setkey		# 查询Set类型缓存key中的所有元素：setkey
1) "hello"
2) "world"
127.0.0.1:6379> zrange zsetkey 0 1	# 查询ZSet类型缓存key中的前两个元素：zsetkey
1) "a"
2) "b"
127.0.0.1:6379> 
```

# 常用工具

## redis-cli

**redis-cli**是一个ZCache的命令行终端工具，可用于连接ZCache服务并执行相关Redis命令，这里主要介绍工具的常用方式（更多详细参数介绍，可执行`redis-cli -h`进行查看学习）。

- Redis命令介绍请查看文档：[<u>Redis常用命令</u>](#redis常用命令)
- 所内同事可点击[[<u>redis-cli工具演练入口</u>](http://172.16.17.3:7682/)]进行工具使用练习

### 工具执行格式

```shell
# redis-cli 工具执行基本格式：
redis-cli [OPTIONS] [cmd [arg [arg ...]]]
```

**工具主要参数（OPTIONS）说明**：

- `-h <host>`：指定访问的缓存服务IP，默认取值为`127.0.0.1`。【`-h`与`-p`参数配合，即通过工具访问指定缓存节点服务】

- `-p <port>`：指定访问的缓存服务端口，默认取值为`6379`。【`-h`与`-p`参数配合，即通过工具访问指定缓存节点服务】

- `-a <password>`：指定缓存服务的访问密码，如果密码中包含特殊字符，请将密码包含于引号('')中；如果缓存服务未设置密码访问，则不需要指定该参数

  > **例如**：缓存服务密码为`abc$123A`，那么密码参数应设置为：`-a 'abc$123A'`

- `-c`：该参数请固定使用，用于在访问缓存集群时，能够根据键值所在节点，自动跳转到正确的节点来执行键值访问命令

  ```shell
  # 如果工具执行参数中未使用-c参数，而访问的键值不在当前节点(127.0.0.1:7360)时，则会报MOVED错误：
  127.0.0.1:7360> get key
  (error) MOVED 12539 127.0.0.1:7363
  127.0.0.1:7360> 
  
  # 如果工具执行参数中使用了-c参数，那么工具能够正确访问到缓存键值
  127.0.0.1:7360> get key
  -> Redirected to slot [12539] located at 127.0.0.1:7363
  "value"
  127.0.0.1:7363> 
  ```

### 工具执行方式

* **人机交互方式**：工具执行的命令行参数中不包含Redis命令，进入人机交互界面后，可输入Redis命令进行缓存服务访问操作：

  ```shell
  # 执行格式：redis-cli -h <host> -p <port> -a <password> -c 
  # 备注：工具传入的参数没有顺序要求；如果缓存服务未设置密码访问，则不需要指定-a参数
  # 示例：
  $ redis-cli -h 127.0.0.1 -p 7360 -a '密码' -c
  127.0.0.1:7360> set key value
  -> Redirected to slot [12539] located at 127.0.0.1:7363
  OK
  127.0.0.1:7363> get key
  "value"
  127.0.0.1:7363> quit      # 通过quit命令来退出工具执行（也可以使用ctrl+c退出）
  $ 
  # -> Redirected ... 信息说明：因为访问的key在其他节点，而redis-cli工具执行时设置了-c参数，
  # 所以工具能够自动跳转到key所在的节点来执行键值访问处理
  ```

* **命令行方式**：工具执行参数中包含要操作的Redis命令，工具执行得到命令的返回结果后随之退出

  ```shell
  # 执行格式：redis-cli -h <host> -p <port> -c -a <password> [command]
  # 注意：工具传入的参数没有顺序要求，但是执行的Redis命令（command）必须在最后（即所有参数之后）
  # 示例：
  $ redis-cli -h 127.0.0.1 -p 7360 -a '密码' -c get key
  "value"
  $ 
  ```

# Redis常用命令

这里主要介绍日常运维过程中可能使用到的常用命令，更多命令信息请查看[<u>参考文档</u>](#参考文档)：

- 如下命令中示例都是使用`redis-cli`工具演示
- Redis命令名不区分大小写：例如`GET`和`get`表示的命令一样
- 所内同事可点击[[<u>Redis命令演练入口</u>](http://172.16.17.3:7681/)]进行命令使用练习

## 管理命令

### EXISTS：检查key是否存在

* **功能** : 检查指定的缓存key是否存在

* **格式**：`EXISTS key`

* **参数** : 待检查缓存key的名称

* **返回值** : 若key存在返回1，否则返回0。

* **示例**：

  ```shell
  127.0.0.1:6379> set testkey testvalue
  OK
  127.0.0.1:6379> exists testkey   	  # 检查存在的key，返回：1
  (integer) 1
  127.0.0.1:6379> exists notexistskey   # 检查不存在的key，返回：0
  (integer) 0
  127.0.0.1:6379> 
  ```

### TYPE：获取key的类型

* **功能** : 获取指定缓存key的数据类型

* **格式**：`TYPE key`

* **参数** : 待检查缓存key的名称

* **返回值** :

  * `none`：表示key不存在
  * `string`：字符串
  * `list`：列表
  * `set`：集合
  * `zset`：有序集合（也即SortedSet）
  * `hash`：哈希表
* **示例** :

  ```shell
  127.0.0.1:6379> set weather "sunny"
  OK
  127.0.0.1:6379> type weather        # 测试检查字符串类型
  string
  127.0.0.1:6379> type testkey        # 测试检查不存在的key 
  none
  127.0.0.1:6379> 
  ```

### TTL：获取key的过期时间

* **功能**：获取指定缓存 key 的剩余生存时间，单位：秒

* **格式**：`TTL key`

* **参数**：待检查缓存key的名称

* **返回值** :

  * `-2`：表示key不存在
  * `-1`：表示key存在，但没有设置过期时间（即key不会自动过期）
  * `正整数`：表示key的剩余生存时间，单位为秒
* **示例** ：

  ```shell
  127.0.0.1:6379> ttl key     
  (integer) -2			# key不存在时，返回-2
  127.0.0.1:6379> set key value  
  OK
  127.0.0.1:6379> ttl key  
  (integer) -1			# key存在，但是没有设置超时时间， 返回-1
  127.0.0.1:6379> expire key 100  # 设置key过期时间为100秒（即100秒后key会被自动删除）
  (integer) 1
  127.0.0.1:6379> ttl key  
  (integer) 98			# key剩余生存时间为98秒（执行命令时已过去2秒）
  127.0.0.1:6379> 
  ```

### DEL：删除key

* **功能** : 删除指定的缓存key

* **格式**：`DEL key`

* **参数** : 待删除缓存key的名称

* **返回值** ：实际被删除的key数量

* **备注**：使用该命令时，请一次只删除一个key；因为对于分布式缓存，多个key的分片大概率不一样，同时删除多个key会操作失败

* **示例** :

  ```shell
  127.0.0.1:6379> set testkey testvalue
  OK
  127.0.0.1:6379> del testkey    # 删除1个key,删除成功返回1
  (integer) 1
  127.0.0.1:6379> del testkey    # 删除不存在的 直接返回0 
  (integer) 0
  127.0.0.1:6379>
  ```

### QUIT：客户端退出

* **功能**：当前客户端退出。redis-cli工具人机交互执行时，可使用该命令来退出工具执行

* **格式**：`QUIT`

* **参数**：无

* **返回值**：OK。【redis-cli工具会直接退出，而未展示返回值】

* **示例** :

  ```shell
  127.0.0.1:6379> quit
  $ 
  ```

### CLUSTER NODES：获取集群节点信息

* **功能**：获取缓存集群中所有服务节点的相关信息

* **格式**：`CLUSTER NODES`

* **参数** : 无

* **返回值** : 集群中的所有节点信息，每行展示一个节点信息，各信息间以空格间隔：`<id> <ip:port> <flags> <masterid> <ping-sent> <pong-recv> <config-epoch> <link-state> <slot> <slot> ... <slot>`

  * `id`：节点唯一标识ID，固定为40个字节的字符串
  * `ip:port`：节点的服务地址
  * `flags`：逗号分割的标记位，可能包含的标记如下
    * **myself**: 当前执行的`cluster nodes`命令所在的节点
    * **master**: 该节点为主节点
    * **slave** : 该节点为从节点
    * **handshake**: 还未取得信任的节点，当前正在与其进行握手
  * `masterid`：如果节点是slave，则该字段为其所属的主节点的ID；否则该字段固定展示为`-`
  * `ping-sent`：**myself**节点最近一次向该节点发送ping的时间（Unix毫秒时间戳），`0`表示最近发送的ping已经收到pong响应
  * `pong-recv`：**myself**节点最近一次收到该节点返回pong的时间（unix毫秒时间戳）
  * `config-epoch`：节点的epoch版本号
  * `link-state`：**myself**节点链接该节点的状态
    * **connected**：链接已建立
    * **disconnected**：链接断开
  * `slot`：哈希槽值或者一个哈希槽范围。如果只是一个值，那就是只有一个槽会被使用； 如果是一个范围，节点将会处理包括起始槽和结束槽在内的所有哈希槽（中间以`-`连接）
* **示例** :

  ```shell
  192.168.151.129:7904> cluster nodes
  8d410dfc2091da7507d300936a10c8dba7bab954 192.168.151.129:7905 master - 0 1578637586000 10 connected 10923-16383
  d0e5ae0b1e6fe93877794e504f899fff31c67687 192.168.151.129:7900 master - 0 1578637587407 15 connected 0-5460
  5a2b8cb75407e6ae89e6f9d966ee869124a74956 192.168.151.129:7903 slave d0e5ae0b1e6fe93877794e504f899fff31c67687 0 1578637588413 15 connected
  102b30303065b89ee22ce3c71f89168e09eb380a 192.168.151.129:7901 slave 521b51462ccb8837f2c6b60712eddfe0f52b1dc7 0 1578637586000 14 connected
  edbc31415c7635af9ba78cedc3d0e85bfe42e603 192.168.151.129:7902 slave 8d410dfc2091da7507d300936a10c8dba7bab954 0 1578637587000 10 connected 
  521b51462ccb8837f2c6b60712eddfe0f52b1dc7 192.168.151.129:7904 myself,master - 0 1578637587000 14 connected 5461-10922
  192.168.151.129:7904> 
  ```

## 字符串(String)操作命令

### SET：设置字符串缓存key的值

* **功能**：设置字符串缓存key为指定值

* **格式**：`SET key value [EX seconds] [PX milliseconds] [NX|XX|EQ oldvalue]`

* **参数**：其中前两个参数key和value为必选参数

  * `key`：要操作的字符串缓存键名称

  * `value`：该缓存键要设置的键值

  * `EX seconds`：设置键的过期时间为`second`秒

  * `PX milliseconds`：设置键的过期时间为`millisecond`毫秒

  * `NX`：只在键不存在时，才对键进行设置`value`操作

  * `XX`：只在键已经存在时，才将键值修改为`value`

  * `EQ oldvalue`：只有当原来的键值等于`oldvalue`时，才将键值修改为`value`

    > EQ参数为ZCache扩展功能，可用于实现分布式锁

* **返回值**：命令执行成功返回OK。如果设置了`NX`、`XX`或者`EQ`，但因为条件没达到而造成设置操作未执行，那么命令返回nil

* **示例**：

  ```shell
  127.0.0.1:6379> set testkey value
  OK
  127.0.0.1:6379> set testkey value2 EQ value   # 当testkey的值未value时，将其设置为新值value2：成功
  OK
  127.0.0.1:6379> get testkey
  "value2"
  127.0.0.1:6379> set testkey value3 EQ value   # 当testkey的值未value时，将其设置为新值value3：失败
  (nil)
  127.0.0.1:6379> get testkey
  "value2"
  127.0.0.1:6379>
  ```

### GET：获取字符串缓存key的值

* **功能**：获取指定字符串缓存key的值

* **格式**：`GET key`

* **参数**：待查询缓存key的名称

* **返回值**：该缓存key的值，key不存在时返回空(nil)。

* **示例**：

  ```shell
  127.0.0.1:6379> get testkey
  "value"
  127.0.0.1:6379> get notexistskey # 获取不存在的key返回nil
  (nil)
  127.0.0.1:6379> 
  ```

### STRLEN：获取字符串缓存key的值长度

* **功能**：获取指定字符串缓存key中的符串值长度

* **格式**：`STRLEN key`

* **参数**：待查询缓存key的名称

* **返回值**：返回字符串值的长度；当key不存在时，则返回0

* **示例**：

  ```shell
  127.0.0.1:6379> set key1 "hello world"
  OK
  127.0.0.1:6379> strlen key1
  (integer) 11
  127.0.0.1:6379>
  ```

## 哈希(Hash)操作命令

### HMSET：设置哈希缓存key的多个域值

* **功能**：同时将多个field-value (域-值)对设置到哈希缓存key中

* **格式**：`HMSET key field1 value1 [field2 value2 ]`

* **参数**：需要指定至少一对field-value。

  - **key**：待操作的哈希缓存key名称
  - **field1**：待操作哈希key中的域名称
  - **value1**：待写入的哈希key的域值
* **返回值**：如果命令执行成功，返回 OK 。

* **示例**：

  ```shell
  127.0.0.1:6379> hmset myhash field1 "hello" field2 "world"
  OK
  127.0.0.1:6379> hget myhash field1
  "hello"
  127.0.0.1:6379> hget myhash field2
  "world"
  127.0.0.1:6379>
  ```

### HMGET：获取哈希缓存key的多个域值

* **功能**：获取哈希缓存key的指定域字段的值。

* **格式**：`HMGET key field1 [field2]`

* **参数**：需要至少指定一个域名

  * **key**：待操作的哈希缓存key名称
  * **field1**：待操作哈希key中的域名称
* **返回值**：返回一个包含多个给定域字段的列表值，列表值的排列顺序和指定域字段的请求顺序一样。

* **示例**：

  ```shell
  127.0.0.1:6379> hset myhash field2 "bar"
  (integer) 1
  127.0.0.1:6379> hset myhash field1 "foo"
  (integer) 1
  127.0.0.1:6379> hmget myhash field1 field2 nofield
  1) "foo"   	# field1域的值
  2) "bar"	# field2域的值
  3) (nil)	# nofield域的值 （nil表示哈希key中无该域）
  127.0.0.1:6379>
  ```

### HDEL：删除哈希缓存key中的域

* **功能**：删除哈希缓存key中的域

* **格式**：`HDEL key field1 [field2]`

* **参数**：需要至少指定一个待删除域字段

  * **key**：待操作的哈希缓存key名称
  * **field1**：待删除的域名称
* **返回值**：返回被实际删除域的数量，不包括被忽略的域

* **示例**：

  ```shell
  127.0.0.1:6379> hset myhash field1 "foo"
  (integer) 1
  127.0.0.1:6379> hdel myhash field1
  (integer) 1
  127.0.0.1:6379> hdel myhash field2
  (integer) 0
  127.0.0.1:6379>
  ```

### HGETALL：获取哈希缓存key中的所有域值

* **功能**：获取哈希缓存key中的所有域字段和值。

* **格式**：`HGETALL key`

* **参数**：待查询的哈希缓存key名称

* **返回值**：以列表形式返回哈希缓存key的所有字段及字段值，列表中元素信息按field-value成对出现； 若 key不存在，返回空列表。

* **示例**：

  ```shell
  127.0.0.1:6379> hmset myhash field1 "hello" field2 "world"
  OK
  127.0.0.1:6379> hgetall myhash
  1) "field1"		# 域名field1
  2) "hello"		# field1域的值
  3) "field2"		# 域名field2
  4) "world"		# field2域的值
  127.0.0.1:6379>
  ```

### HLEN：获取哈希缓存key的域个数

* **功能**：获取哈希key中的域字段数量

* **格式**：`HLEN key`

* **参数**：待操作的哈希缓存key名称

* **返回值**：返回哈希表中域字段的数量。当key不存在时，返回0。

* **示例**：

  ```shell
  127.0.0.1:6379> hmset myhash field1 "foo" field2 "bar"
  OK
  127.0.0.1:6379> hlen myhash
  (integer) 2
  127.0.0.1:6379> 
  ```

## 列表(List)操作命令

### RPUSH：写入元素到列表key中

* **功能**：从列表缓存key右侧添加一个或多个元素

* **格式**：`RPUSH key value1 [value2]`

* **参数**：需要至少设置一个value

  * **key**：待操作的列表缓存key名称
  * **value1**：待增加到列表中的value元素
* **返回值**：返回执行完RPUSH命令后列表的长度

* **示例**：

  ```shell
  127.0.0.1:6379> llen mylist
  (integer) 0
  127.0.0.1:6379> rpush mylist "one"  # 插入一个元素。
  (integer) 1
  127.0.0.1:6379> rpush mylist "two"
  (integer) 2
  127.0.0.1:6379> llen mylist
  (integer) 2
  127.0.0.1:6379> 
  ```

### LPOP：从列表key中弹出元素

* **功能**：从列表缓存key左侧获取到第一个元素，同时将该元素从列表中删除

* **格式**：`LPOP key`

* **参数**：待操作的列表缓存key名称

* **返回值**：返回列表的第一个元素。 当列表key不存在时，返回 nil。

* **示例**：

  ```shell
  127.0.0.1:6379> rpush list1 "foo" 	# 从右侧写入元素foo 
  (integer) 1
  127.0.0.1:6379> rpush list1 "bar" 	# 从右侧写入元素bar 
  (integer) 2
  127.0.0.1:6379> lpop list1   		# 从左侧返回列表的第一个元素。 
  "foo"
  127.0.0.1:6379> llen mylist
  (integer) 1
  127.0.0.1:6379> 
  ```

### LRANGE：获取列表指定区间内的元素

* **功能**：获取列表缓存key指定区间范围[start,stop]内的元素

* **格式**：`LRANGE key start stop`

* **参数**：

  * `key`：待操作的列表缓存key名称
  * `start`：区间起始位置
  * `stop`：区间结束位置

  > **备注**：区间参数 `start` 和 `stop` 都以`0`为底。即以 `0` 表示第一个元素，以 `1` 表示第二个元素，以此类推。也可以使用负数下标，以 `-1` 表示最后一个元素， `-2` 表示倒数第二个元素，以此类推

* **返回值**：一个列表，包含指定区间内的元素。

* **示例**：

  ```shell
  127.0.0.1:6379> rpush mylist "one" "two" "three"
  (integer) 3
  127.0.0.1:6379> lrange mylist 0 0   # 0代表第一个元素。
  1) "one"
  127.0.0.1:6379> lrange mylist 5 10
  (empty list or set)
  127.0.0.1:6379> lrange mylist 1 10  # 1代表是第二个元素。
  1) "two"
  2) "three"
  127.0.0.1:6379> lrange mylist 0 -1  # -1代表是列表的最后一个元素，所以该命令会返回list中全部元素
  1) "one"
  2) "two"
  3) "three"
  127.0.0.1:6379> 
  ```

### LLEN：获取列表key的长度

* **功能**：获取列表缓存key的长度，即列表中包含的元素个数

* **格式**：`LLEN key`

* **参数**：待操作的列表缓存key名称

* **返回值**：返回列表的长度

* **示例**：

  ```shell
  127.0.0.1:6379> llen mylist  			# 查询列表长度为0 
  (integer) 0
  127.0.0.1:6379> rpush mylist "hello"  	# 写入第一个元素
  (integer) 1
  127.0.0.1:6379> llen mylist  			# 查询列表的长度为1 
  (integer) 1
  127.0.0.1:6379> rpush mylist "world"  	# 写入第二个元素
  (integer) 2
  127.0.0.1:6379> llen mylist  			# 查询列表的长度为2 
  (integer) 2
  127.0.0.1:6379> 
  ```

## 集合(Set)操作命令

### SADD：向集合缓存key中写入多个元素值

* **功能**：向集合缓存key中添加一个或多个元素值。（集合中的元素具有唯一性）

* **格式**：`SADD key member1 [member2]`

* **参数**：至少需要指定一个元素值

  * **key**：待操作的集合缓存key名称
  * **member1**：待增加到集合中的元素值
* **返回值** ：返回实际被新添加到集合中的新元素数量，不包括被已存在的元素。

* **示例**：

  ```shell
  127.0.0.1:6379> sadd myset "world"
  (integer) 1		# 新增元素world，返回1
  127.0.0.1:6379> sadd myset "world" "hello" "foo"
  (integer) 2		# 新增元素hello和foo，返回2 （world元素已存在）
  127.0.0.1:6379> smembers myset
  1) "hello"
  2) "foo"
  3) "world"
  127.0.0.1:6379>
  ```

### SISMEMBER：检查集合缓存key中是否包含指定元素

* **功能**：检查集合缓存key中是否包含指定元素，即元素是否存在于集合中

* **格式**：`SISMEMBER key member`

* **参数**：

  * **key**：待检查的集合缓存key名称
  * **member1**：待检查的元素值
* **返回值**：如果元素存在于集合缓存key中，则返回 1；如果集合中不包含该元素，或集合缓存key不存在，则返回0。

* **示例**：

  ```shell
  127.0.0.1:6379> sadd myset1 "hello"
  (integer) 1
  127.0.0.1:6379> sismember myset1 "hello"
  (integer) 1
  127.0.0.1:6379> sismember myset1 "world"
  (integer) 0
  127.0.0.1:6379>
  ```

### SREM：删除集合缓存key中的元素

* **功能**：删除集合缓存key中的元素

* **格式** ：`SREM key member1 [member2]`

* **参数** ：需要至少指定一个待删除元素

  * **key**：待操作的集合缓存key名称
  * **member1**：待删除的元素名
* **返回值**：返回被实际删除的元素数量，不包括被忽略的元素

* **示例**：

  ```shell
  127.0.0.1:6379> sadd myset1 "hello" "world" "bar"
  (integer) 3
  127.0.0.1:6379> srem myset1 "hello" "bar" "notexitsmember"
  (integer) 2		# 实际被删除元素hello和bar，返回2
  127.0.0.1:6379> smembers myset1
  1) "world"
  127.0.0.1:6379>
  ```

### SMEMBERS：获取集合缓存key中的所有元素

* **功能** ：返回集合缓存key中的所有元素值

* **格式** ：`SMEMBERS key`

* **参数**：待操作的集合缓存key名称

* **返回值**：返回集合中的所有元素列表

* **示例**：

  ```shell
  127.0.0.1:6379> sadd myset1 "hello" "world"
  (integer) 2
  127.0.0.1:6379> smembers myset1
  1) "hello"
  2) "world"
  127.0.0.1:6379>
  ```

### SCARD：获取集合缓存key中的元素数

* **功能**：获取集合缓存key中的元素个数。

* **格式**：`SCARD key`

* **参数**：待操作的集合缓存key名称

* **返回值** ：返回集合中元素的数量。当集合key不存在时，返回0。

* **示例**：

  ```shell
  127.0.0.1:6379> scard myset
  (integer) 0
  127.0.0.1:6379> sadd myset "foo"
  (integer) 1
  127.0.0.1:6379> sadd myset "hello" "world"
  (integer) 2
  127.0.0.1:6379> scard myset
  (integer) 3
  127.0.0.1:6379>
  ```

## 有序集合(ZSet)操作命令

### ZADD：向有序集合缓存key中写入多个元素

* **功能**：向有序集合缓存key中写入多个成员，或者更新已存在元素的分数

* **格式**：`ZADD key score1 member1 [score2 member2]`

* **参数**：至少需要指定一对`score-member`元素分值对

  * `key`：待操作的有序集合缓存key的名称
  * `score1`：待写入的元素名
  * `member1`：待写入的元素`score1`的分值
* **返回值**：返回实际添加的新元素的数量，不包括那些被更新的、已经存在的元素

* **示例**：

  ```shell
  127.0.0.1:6379> zadd myzset 1 "one"
  (integer) 1		# 新增元素one，分值为1
  127.0.0.1:6379> zadd myzset 1 "one" 2 "two" 3 "three"
  (integer) 2		# 新增元素two和three。（元素one已存在）
  127.0.0.1:6379> zrange myzset 0 -1 WITHSCORES
  1) "one"
  2) "1"
  3) "two"
  4) "2"
  5) "three"
  6) "3"
  127.0.0.1:6379>
  ```

### ZREM：删除有序集合缓存key中的元素

* **功能**：删除有序集合缓存key中的元素

* **格式**：`ZREM key member [member ...]`

* **参数**：至少需要指定一个待删除的元素

  - `key`：待操作的有序集合缓存key名称
  - `member`：待删除的元素名
* **返回值**：返回实际被删除的元素数量，不包含被忽略的元素。

* **示例**：

  ```shell
  127.0.0.1:6379> zadd page_rank 8 bing.com
  (integer) 1			# 新增元素bing.com，返回1
  127.0.0.1:6379> zadd page_rank 8 bing.com 9 baidu.com 10 google.com
  (integer) 2			# 新增元素baidu.com和google.com，返回2.(bing.com已存在)
  127.0.0.1:6379> zrem page_rank  google.com
  (integer) 1
  127.0.0.1:6379> zrange page_rank 0 -1 withscores
  1) "bing.com"
  2) "8"
  3) "baidu.com"
  4) "9"
  127.0.0.1:6379>
  ```

### ZCARD：获取有序集合缓存key中的元素数

* **功能**： 获取有序集合缓存key中的元素个数

* **格式**：`ZCARD key`

* **参数**： 待操作的有序集合缓存key名称

* **返回值**：成功返回有序集的元素个数； 当key不存在时返回0。

* **示例**：

  ```shell
  127.0.0.1:6379> zadd myzset 1 "one" 2 "two"
  (integer) 2
  127.0.0.1:6379> zcard myzset
  (integer) 2
  127.0.0.1:6379>
  ```

### ZRANGE：获取有序集合缓存key指定区间内元素列表

* **功能**： 获取有序集合缓存key指定区间内元素列表，返回值中可选择带有分值

* **格式**：`ZRANGE key start stop [WITHSCORES]`

* **参数**：

  * `key`：待操作的有序集合缓存key名称
  * `start`：待查询区间的起始位置，取值0表示从有序集合中第一个元素开始查询
  * `stop`：待查询区间的结束位置，取值-1时表示查询到有序集合中最后一个元素
  * `WITHSCORES`：返回结果列表中包含元素的分值

  > **备注**：区间参数 `start` 和 `stop` 都以`0`为底。即以 `0` 表示第一个元素，以 `1` 表示第二个元素，以此类推。也可以使用负数下标，以 `-1` 表示最后一个元素， `-2` 表示倒数第二个元素，以此类推

* **返回值**：返回有序集合在指定范围内的元素列表，如果设置了`WITHSCORES`参数，则列表中包含元素分值。

* **示例**：

  ```shell
  127.0.0.1:6379> ZADD myzset 0 a 0 b 1 c 1 d 2 e
  (integer) 5
  127.0.0.1:6379> ZRANGE myzset 0 -1 # 只获取有序集合中的所有成员
  1) "a"
  2) "b"
  3) "c"
  4) "d"
  5) "e"
  127.0.0.1:6379> ZRANGE myzset 0 -1 withscores  # 获取有序集合中的所有成员，包含分值
   1) "a"
   2) "0"		# 元素a的分值
   3) "b"
   4) "0"		# 元素b的分值
   5) "c"
   6) "1"		# 元素c的分值
   7) "d"
   8) "1"		# 元素d的分值
   9) "e"
  10) "2"		# 元素e的分值
  127.0.0.1:6379>
  ```

# 沙盒演练

- [<u>redis-cli工具演练入口</u>](http://172.16.17.3:7682/)
- [<u>Redis命令演练入口</u>](http://172.16.17.3:7681/)

# 参考文档

- [<u>分布式缓存ZCache在线文档</u>](https://edu.iwhalecloud.com/zcache/)

