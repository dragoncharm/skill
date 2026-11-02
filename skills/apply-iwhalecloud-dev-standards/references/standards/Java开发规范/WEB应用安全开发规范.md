![image](uploads/50608/c9902e96-6080-4d43-8283-acfbb760aa4f/image.png)

# 前 言

本规范定义了Web应用系统安全开发和Web编码安全相关的技术要求，旨在保障Web应用平台的安全性、完整性和可用性。从安全角度规范Web应用系统开发人员，培养开发人员在日常的设计与编码工作中的安全意识，实现安全编码，保障系统安全。

## 适用说明

本规范定义了Web应用系统安全开发和Web编码安全相关的技术要求。
<mark><font color="red">备注</font>：当前规范考试命题范围是规范标题中带有✪符号的</mark>

## 安全实战原则

- 默认安全原则。
- 纵深防御原则，包含两层含义：首先，在各层面、各方面实施安全方案，各方案之间相互配合，避免出现漏洞；找到安全问题产生的本质原因，实施针对性的安全方案。
- 数据与代码分离原则，如缓冲区溢出以及各类“注入”问题。
- 不可预测性原则，如CSRF防御中生成随机token以及加密、随机数、哈希等。

# 客户端脚本安全

## <font style="background: yellow">✪XSS</font>

Cross Site Script（XSS），跨站点脚本攻击。当应用程序的新网页中包含不受信任的、未经恰当验证或转义的数据时，或者使用可以创建HTML或JavaScript 的浏览器API 更新现有的网页时，就会出现XSS 缺陷。XSS 让攻击者能够在受害者的浏览器中执行脚本，并劫持用户会话、破坏网站或将用户重定向到恶意站点。

XSS根据效果的不同分为以下三类：反射型XSS、存储型XSS和DOM Based XSS。

恶意攻击者可以利用XSS做到：

- 盗取用户cookie，伪造用户身份登录。
- 控制用户浏览器。
- 结合浏览器及其插件漏洞，下载病毒木马到浏览者的计算机上执行。
- 衍生URL跳转漏洞。
- 让官方网站出现钓鱼页面。
- 蠕虫攻击。

XSS防御方案：输出编码、输入转义。

###  <font style="background: yellow">✪输出编码</font>

原则，在正确的地方使用正确的编码方式，目前Web网站大多都是用MVC架构，那么XSS发生在View层，即应用拼接变量到HTML页面时产生。

#### 在HTML标签中显示“用户可控数据”，使用HtmlEncode进行转义。

<font color="red">反例</font>

```html
<div>$var</div>
$var的值为<script>alert(/xss/)</script>
<a href=#>$var</a>
$var的值为<img src=# onerror=alert(1)/>
```

#### 在HTML内容语境中显示“用户可控数据”，使用HtmlContent进行转义。

<font color="red">反例</font>

```html
<textarea name="text">$var</textarea>
```

输入同1

#### 在HTML元素属性中显示“用户可控数据”，使用HtmlAttribute进行转义。

<font color="red">反例</font>

```html
<input type="text" name="a" value="$var"/>
$var的值为"><script>alert(/xss/)</script>
```

#### 在<script\>中使用“用户可控数据”，必须确保输出的变量在引号中，使用JavaScriptEncode进行转义。

```html
<script>
var data = "$var";
</script>
$var的值为";alert(/xss/);//
```

#### 在事件中使用“用户可控数据”，使用JavaScriptEncode进行转义。

```html
<button onclick="funcA('$var ')">
$var的值为');alert(/xss/);//
```

#### 在CSS中输出的“用户可控数据”，需要做CSS escape转义。

在CSS、style、style属性中形成XSS方式多样化，可参考下图XSS攻击的例子：

![image](uploads/50608/311ecae6-1f2d-4062-9d32-c5357d5b5eac/image.png)

尽可能禁止在用户输入变量在style标签、html标签的style属性以及CSS文件中输出。

#### URL的输出是“用户可控数据”时，需要进行URL转义。

HTML中一些元素属性的值是URL，这些URL如果是“用户可控数据”，针对完整的URL需先验证URL的有效性，避免URL中存在非法协议（如javascript等伪协议）；之后再根据URL所在的HTML语境选择合适的函数进行转义。

一般先验证URL的有效性，再根据输出语境选择适当的转义函数：

```javascript         
String userURL = request.getParameter( "userURL" )
boolean isValidURL = Validator.IsValidURL(userURL, 255);
if (isValidURL) { 
    <a href="<%= Encode.forHtmlAttribute(userURL)%>">
<%= Encode.forHtmlContent(untrustedLinkName) %>
</a>
}
````

如果是对URL中的参数进行编码则可以使用下面的方式进行转义。

```html
<a href="http://www.owasp.org/<%=Encode.forUriComponent(UNTRUSTED)%>?qry#fragment">
<a href="/search?value=<%=Encode.forUriComponent(UNTRUSTED)%>&order=1#top">
```

Encode.forUriComponent函数除字母、数字以及“-”、“_”、“.”、“~”外，其余字符转义后的格式为“%HH”。

上述方法均是针对从服务器应用直接输出到HTM页面的XSS漏洞，转义发生在模板引擎或者明确知道该参数的输出语境的情况下（view层），在服务端使用OWASP提供的API对输出进行转义；如果没有使用模板引擎，若使用前端框架的视图渲染机制，则需要前端框架根据输出语境对服务器返回的数据选择合适的函数进行转义；可使用设计上就会自动编码来解决XSS问题的框架，如：Ruby 3.0 或 React JS，需要了解每个框架的XSS保护的局限性，并适当地处理未覆盖的用例。

备注：上面示例中的转义API以及转义字符规则实现，参考OWASP Java Encoder Project或者ESAPI

#### DOM-based XSS解决方案

此类XSS是从JavaScript中输出数据到HTML页面中，如下代码中，通过Ajax请求从服务端获取数据portalList，之后动态追加到DOM节点中，此时需要开发人员根据上面所列的数据输出语境选择适当的函数进行转义：

 ```javascript
if (portal.appGlobal.get('portalId') === portalList[i].portalId) {
        that.$('.portalMenu') .append( "<li class='portal-menu__item active'>" +
                                "<a href='javascript:void 0'> " +
                                fish.escape(portalList[i].portalName) +
                                '</a>' +
                                '</li>'
                               );
    }
```

以下几个地方为JavaScript输出到HTML页面的必经之路，会触发此类XSS问题，需重点关注：

document.write();
document.writeIn();
xxx.innerHTML=
xxx.outerHTML=
innerHtml.replace
document.attachEvent()
document.location.replace()
…………

**OWASP解决此类XSS问题的思路可参考如下链接：**

[https://github.com/OWASP/CheatSheetSeries/blob/master/cheatsheets/DOM_based_XSS_Prevention_Cheat_Sheet.md](https://github.com/OWASP/CheatSheetSeries/blob/master/cheatsheets/DOM_based_XSS_Prevention_Cheat_Sheet.md)

#### Cookie设置HttpOnly属性

对作为用户身份认证的Cookie设置HttpOnly属性，有助于缓解XSS攻击中的Cookie劫持问题。

#### 响应头部设置Content-Security-Policy以及X-XSS-Protection属性

#### AJAX输出转义

- 对于JSON格式的返回值，需要正确设置响应头部的Content-Type，避免浏览器将返回数据当作脚本来执行，如：

```javascript
HTTP/1.1 200
Date: Wed, 06 Feb 2013 10:28:54 GMT
Server: Microsoft-IIS/7.5....
Content-Type: application/json; charset=utf-8
......
```

服务端设置响应头部内容类型的代码示例：

```java
response.setContentType("application/json");
```

- 不要将返回的JSON字符串直接输出到JavaScript脚本中，先进行html转义，如：

```html
<div id="init_data" style="display: none">
    <%= html_escape(data.to_json) %>
</div>
```

```javascript
var dataElement = document.getElementById('init_data');
var initData = JSON.parse(dataElement.textContent);
```

#### 引用第三方脚本

通过script标签、requireJs加载第三方网站的脚本或者通过iframe的src属性嵌入第三方网站（非本应用内的脚本或者网站），如果第三方网站存在安全问题，并被攻击者注入恶意脚本，则加载该第三方网站的脚本或打开页面，则会执行恶意脚本造成XSS攻击。

**解决方案：**

1. 禁止加载第三方脚本，或配置白名单。
2. 在响应头部设置X-Frame-Options属性，限制iframe打开的源。

### <font style="background: yellow">✪输入校验</font>

- 如果用户的数据有明确的格式要求，如用户名只能为数字与字母组合、电话、邮箱、生日等信息，都有一定的格式规范，输入参数有长度、范围限制、密码规则等，检查的逻辑必须放在服务端的代码中实现。Web开发的普遍的做法，在客户端的JavaScript中和服务端代码中实现相同的输入检查。在客户端JavaScript中进行输入校验，可以阻挡大部分误操作的用户，从而节约服务器资源。

如用户密码中某一个字符连续出现3次：

前端校验：

```javascript
if (/(.)\1{2}/.test(password)) {
    return i18n.PWD_CONTINUOUS_CHAR_NUM.replace("{0}", 2);
}
```

服务端校验：

```java
public static boolean checkPwdContinuousChar(String pwd) {
        Pattern p = Pattern.compile("(.)\\1{2}");
        Matcher matcher = p.matcher(pwd);
        return matcher.find();
    }
```

- 采用XSS Filter防御，检查用户输入的数据中是否包含一些特殊字符，如<、>、’、”等，如果发现有这些特殊字符，则进行过滤或者编码。但是XSS Filter对于用户输入数据的语境理解不完整，有时候会误杀一些数据，改变用户原本的意思。如用户原意是输入1+1<3，转义后变为1+1&lt;3。

此时可以使用一些敏感词黑名单，匹配到再转义，缓解语境问题。

```java
public static String stripXSS(String value) {
        if (value != null) {
            String oriValue = value;
            // Avoid null characters
            value = value.replaceAll("", "");
Pattern scriptPattern = Pattern.compile(
            "<[\r\n| | ]*script[\r\n| | ]*>(.*?)</[\r\n| | ]*script[\r\n| | ]*>", Pattern.CASE_INSENSITIVE);
            value = scriptPattern.matcher(value).replaceAll("");
            ………
            // Avoid expression(...) expressions
            scriptPattern = Pattern.compile("expression\\((.*?)\\)",
                Pattern.CASE_INSENSITIVE | Pattern.MULTILINE | Pattern.DOTALL);
            value = scriptPattern.matcher(value).replaceAll("");
            // Avoid javascript:... expressions
            // old : javascript:
            scriptPattern = Pattern.compile("
javascript[\r\n| | ]*:[\r\n| | ]*", Pattern.CASE_INSENSITIVE);
            value = scriptPattern.matcher(value).replaceAll("");
            // Avoid SQL injection //add by shi.pengyan 2013-6-25
            scriptPattern = Pattern.compile(SQL_REG, Pattern.CASE_INSENSITIVE);
            value = scriptPattern.matcher(value).replaceAll("");
            // value = StringEscapeUtils.escapeHtml(value);
            value = htmlEncode(value);
}
private static String htmlEncode(String value) {
        if (value == null) {
            return value;
       }
        // value = value.replaceAll("\\(", "(").replaceAll("\\)", ")");
        value = value.replaceAll("&", "&");
        value = value.replaceAll("'", "'").replaceAll("\"", """);
        value = value.replaceAll("<", "<").replaceAll(">", ">");
        return value;
    }
```

## <font style="background: yellow">✪CSRF</font>

Cross-Site Request Forgery（CSRF），跨站点请求伪造攻击。

当Web服务器从客户端接收请求而没有任何机制来验证该请求是否被故意发送时，攻击者可能会欺骗客户端向Web服务器发出任意的请求，Web服务器却将其视为真实的请求。可通过URL，图像加载，XMLHttpRequest，form表单等来完成，并且可能导致数据暴露或意外的代码执行。

防御方案如下：

1. 在用户成功登录应用后，设置一个随机的CSRF TOKEN存储至当前用户的Session中，同时返回到前端并保存在应用的全局变量中缓存起来。
2. 设置请求中的CSRF TOKEN

AJAX请求时，将CSRF TOKEN设置到请求头部，代码示例如下：

```javascript
$(function () {
var token = $("meta[name='_csrf']").attr("content");
var header = $("meta[name='_csrf_header']").attr("content");
$(document).ajaxSend(function(e, xhr, options) {
        xhr.setRequestHeader(header, token);
});
});
```

表单提交的方式需要生成一个隐藏域，禁止在表单的GET请求中。

```html
<form action="${logoutUrl}"  method="post">
<input type="submit"   value="Log out" />
<input type="hidden"   name="${_csrf.parameterName}"  value="${_csrf.token}"/>
</form>
```

3. AJAX或者表单方式提交请求后，应用服务器需要判断请求头部或者表单中的CSRF TOKEN值是否与用户Session中的TOKEN值一致，如果不一致或没有这个值，则判定为CSRF攻击，同时记录攻击日志并返回提示信息到前端，示例代码如下（spring security）：

```java
String actualToken = request.getHeader(csrfToken.getHeaderName());
if (actualToken == null) {
actualToken = request.getParameter(csrfToken.getParameterName());
}
if (!csrfToken.getToken().equals(actualToken)) {
if (this.logger.isDebugEnabled()) {
this.logger.debug("Invalid CSRF token found for "
+ UrlUtils.buildFullRequestUrl(request));
}
if (missingToken) {
this.accessDeniedHandler.handle(request, response,
new MissingCsrfTokenException(actualToken));
}
else {
this.accessDeniedHandler.handle(request, response,
new InvalidCsrfTokenException(csrfToken, actualToken));
}
return;
}
```

如果没有使用安全框架，开发人员可以写一个filter，实现token的校验功能。

由于攻击者无法预测每一个用户登录时随机生成的CSRF TOKEN值，因此无法伪造该参数或者请求头部。敏感操作的请求方法使用POST，而不要使用GET，以form表单或者Ajax的形式提交；URL中不要出现token，否则会通过Referer泄露；如果存在跨域漏洞，token也会泄露；如果系统中存在XSS漏洞，则CSRF的防御方案将会失效。

## 点击劫持

Clickjacking，点击劫持。

用户界面（UI）允许加载一些不可信的信息或者第三方网站，并向用户展示伪造的信息，这容易造成钓鱼网站攻击。

可通过设置请求响应头X-Frame-Options的方式来防御点击劫持，该头部支持三个可选的值：

- DENY：浏览器拒绝当前页面加载任何frame页面
- SAMEORIGIN：frame页面的地址只能为同源域名下的页面
- ALLOW-FROM：自定义允许frame加载的页面地址

代码示例如下：

```java
public void init(FilterConfig filterConfig) throws ServletException {
        XFrameOptions = filterConfig.getInitParameter("XFrameOptions");
}
public void doFilter(ServletRequest servletRequest, ServletResponse servletResponse,
        FilterChain filterChain) throws IOException, ServletException {
        HttpServletResponse response = (HttpServletResponse) servletResponse;    
        if (!StringUtil.isEmpty(XFrameOptions)) {
            response.addHeader("X-Frame-Options", XFrameOptions);
        }
        filterChain.doFilter(servletRequest, response);
    }
```

“Content Security Policy”（指令较多且比较严格，使用时需要花时间了解下各个指令的含义）以及NO Script扩展也能有效防御点击劫持。此外，该响应头部也可以在Web服务器上进行配置。

“Content Security Policy”参考链接：[https://www.w3.org/TR/CSP3/](https://www.w3.org/TR/CSP3/)

## CORS

Cross Origin Resource Sharing，跨域资源共享，解决浏览器同源策略限制，允许脚本的跨域请求，同时也会带来安全问题，需要限制跨域请求应用的源，可通过HTTP Header进行精确的控制：

![image](uploads/50608/ec8cdf64-f3a2-484a-920d-88c15550a699/image.png)

实现方式：

1. 简单的自定义CORSFilter / Interceptor，对跨域请求的源进行校验。
2. Nginx 配置支持Ajax跨域，配置上图中列出的各项。
3. 使用安全框架的CORS防御机制。

# 服务器端应用安全

## <font style="background: yellow">✪注入</font>

将不受信任的数据作为命令或查询的一部分发送到解析器时，会产生诸如SQL注入、NoSQL注入、OS注入和LDAP注入的注入缺陷。攻击者的恶意数据可以诱使解析器在没有适当授权的情况下执行非预期命令或访问数据。

### <font style="background: yellow">✪SQL注入攻击</font>

当应用程序将用户输入的内容，拼接到SQL语句中，一起提交给数据库执行时，就会产生SQL注入威胁。可能造成SQL注入的示例代码如下：

Java(jdbc)示例：

```java
HttpServletRequest request, HttpServletResponse response) {
JdbcConnection conn = new JdbcConnection();
final String sql = "select * from product where pname like '%"
   + request.getParameter("pname") + "%'";
conn.execqueryResultSet(sql);
```

Java(ibatis)示例：

```sql
<select id=" unsafe " resultType="com.ztesoft.zsmart.pot.dto.RoleDto">
        SELECT
        ROLE_ID,ROLE_NAME,COMMENTS,ROLE_CODE,IS_LOCKED FROM BFM_ROLE WHERE ROLE_CODE = '$roleCode $'
    </select>
```

**解决方案：**

书写SQL语句时，应使用预编译语句，对所有传入SQL语句中的变量做绑定。用户拼接进来的变量，无论内容是什么，都会被当作替代符号“?”所替代的值，数据库也不会把恶意用户拼接进来的数据，当作SQL语句的一部分去解析。

Java（jdbc）示例：

```java
final String sql = "select * from product where pname like ?"; 
java.sql.PreparedStatement ps = (java.sql.PreparedStatement)
conn.prepareStatement(sql);
ps.setObject(1, "%"+request.getParameter("pname")+"%");
ResultSet rs = ps.executeQuery();
```

Java(ibatis)示例：

```sql
 <select id=" unsafe " resultType="com.ztesoft.zsmart.pot.dto.RoleDto">
        SELECT
        ROLE_ID,ROLE_NAME,COMMENTS,ROLE_CODE,IS_LOCKED FROM BFM_ROLE
WHERE     ROLE_CODE = #roleCode#
    </select>
```

另外，检查数据类型、使用安全的存储过程、使用安全编码函数等。SQL注入问题可参考《Java语言安全编码规范》规则1.2，或者参考后端框架的SQL防御实施方案。

### <font style="background: yellow">✪代码与命令注入</font>

对这种注入攻击，所有需要执行的系统命令，必须是开发人员定义好的，不允许接收用户传来的参数，加入到系统命令中去。禁用eval()、system()等可以执行命令的函数。如果一定要用，则必须对用户输入数据进行处理。

## <font style="background: yellow">✪文件上传/下载</font>

### <font style="background: yellow">✪文件上传</font>

Web应用程序在处理用户上传的文件时，没有判断文件的扩展名是否在允许的范围内，就把文件保存在服务器上，导致恶意用户将可执行的脚本文件到Web服务器上，通过该脚本文件获得执行服务器命令的能力。

**防御方案：**

1. 文件上传的目录设置为不可执行
2. 判断文件类型
3. 使用随机数改写文件名和文件路径
4. 单独设置文件服务器的域名

参考代码如下：

- 设置上传文件扩展名白名单，不属于白名单内的文件扩展名，则不允许上传。

```properties
#最大上传文件大小，单位字节，默认10MB
#file.upload.maxFileSize=10485760
#上传文件类型
#file.upload.type=
checkFileType(originalFileNameSuffix,uploadProperties.getType());
checkFileSize(file.getSize(),uploadProperties.getMaxFileSize());
```

- 校验文件头部的类型与文件扩展名以及各种类型文件的大小，与配置不同则拒绝上传。

```java
 // 获取文件头
        String currentFileHeader = getFileHeader(file);
        String[] expectFileHeaderArr = initFileTypes.get(expectFileType);
        Boolean retFlag = false;
        // 期望的文件头
        for (String expectFileHeader : expectFileHeaderArr) {
            if(expectFileHeader.equals(currentFileHeader)){
                retFlag = true;
                break;
            }
        }
```

- 上传文件的目录通过配置文件进行配置，并在服务端校验文件路径

```properties
#上传文件在服务器上的物理路径,只能配置一个。
#file.upload.directory= /home/upload
checkDirectory(uploadDirectory, finalUploadDirectory);
```

- 上传文件要保存的文件名，由系统生成随机文件名或者用户自定义的文件名，以满足不同的需求。

```java
// 得到随机文件名
String fileName = UUID.randomUUID() + "." + originalFileNameSuffix;
```

- 对./以及../等进行屏蔽，防止用户恶意猜解后台服务器目录结构。

```java
if (isStrictValidation && (fileDirectory.contains("./") || fileDirectory.contains(".\\"))) {
logger.error("filePath contains ./ or ../");
throw new Exception("S-UPLOAD-009");
}
```

### <font style="background: yellow">✪文件下载</font>

任意文件下载攻击和目录遍历攻击，处理用户下载文件请求时，允许用户提交任意文件路径且未做任何校验，便将服务器上对应的文件直接发送给用户，将造成任意文件下载威胁。如果让用户提交文件目录地址，就把目录下的文件列表发给用户，会造成目录遍历安全威胁。

恶意用户会变换目录或文件地址，下载服务器上的敏感文件、数据库链接配置文件、网站源代码等。

**防御方案：**

1. 要下载的文件地址保存至数据库中。
2. 文件路径保存至数据库，让用户提交文件对应 ID 下载文件。
3. 下载文件之前做权限判断。
4. 文件放在 web 无法直接访问的目录下。
5. 记录文件下载日志。
6. 不允许提供目录遍历服务。

记录不符合规范的上传文件日志

参考实现如下：

- 通过用户与菜单，菜单与下载目录的映射关系进行配置，阻止越权访问文件。

```java
if(!DownloadPrivUtil.getInstance().validatePathPriv(session, realFilePath)){
   response.getWriter().print("You have no permission to download this file.");
   return;
 }
```

- 对./以及../等进行屏蔽，防止用户恶意猜解后台服务器目录结构。

```java
 //严格模式下，包含./或者.\直接报错
if (isStrictValidation && (realFilePath.contains("./") || realFilePath.contains(".\\"))) {
      response.getWriter().print("Can not download this file.");
       return;
    }
```

- 下载文件的目录通过配置文件进行配置，且web无法直接访问该目录，下载文件时校验目录的合法性。

```java
 #允许下载的文件路径，多个目录用逗号隔开,下载路径不配置默认使用文件上传目录
#file.download.directory=
//判断filePath是否在配置的白名单路径下
    directory = directory.replace('\\','/');
    if (realFilePath.startsWith(directory)){
           canDownload = true;
            break;
    }
```

- 通过配置控制文件下载后是否在服务器端进行删除，有些业务可能同时存在文件下载后删除与不删除两种场景，需要分别开发两个不同的接口以满足该需求，禁止通过请求中传入的参数决定文件是否删除的逻辑。另外，两个接口中对应的下载目录要设置为不同的路径。

```java
 if (needDelete) {
     f.delete();
    }
```

## <font style="background: yellow">✪访问控制</font>

未对通过身份验证的用户实施恰当的访问控制。攻击者可以利用这些缺陷访问未经授权的功能或数据，例如：访问其他用户的帐户、查看敏感文件、修改其他用户的数据、更改访问权限等。

### <font style="background: yellow">✪垂直权限</font>

Vertical Access Control，垂直权限安全攻击，即权限提升攻击。

如果web应用程序没有做权限控制，恶意用户可以猜测其他管理页面的URL，从而访问或控制其他权限级别较高的用户拥有的数据或页面，达到权限提升目的。 该安全威胁会导致普通用户变成管理员权限。

可采用Spring Security提供的权限管理机制是基于RBAC模型的一个实现，一种是“基于URL的访问控制”，另一种是“基于method的访问控制”。

基于URL的访问控制的配置如下：

```html
<http pattern="/restful/**" create-session="stateless">
<intercept-url pattern='/**' access="hasRole('REMOTE')" />
<http-basic />
</http>
```

基于表达式的访问控制的配置如下：

```java
protected void configure(HttpSecurity http) throws Exception {
    http
        .authorizeRequests()                                  
            .antMatchers("/resources/**", "/signup", "/about").permitAll()                  2
            .antMatchers("/admin/**").hasRole("ADMIN")        
            .antMatchers("/db/**").access("hasRole('ADMIN') and hasRole('DBA')")            
            .anyRequest().authenticated()         
            .and()
        // ...
        .formLogin();
}
```

基于method的访问控制配置如下：

```java
@PreAuthorize("hasRole('USER')")
@PostFilter("hasPermission(filterObject, 'read') or hasPermission(filterObject, 'admin')")
public List<Contact> getAll();
```

权限管理是业务需求的一个问题，系统定制自己的权限管理系统时，可选择基于RBAC模型作为依据。不同角色的权限有高低之分，高权限角色访问低权限角色的资源往往是被允许的，而低权限角色访问高权限角色的资源则被禁止，即越权访问。

在配置权限时，应当使用“最小权限原则”，并使用“默认拒绝”的策略，只对有需要的主体单独配置“允许”的策略。

### <font style="background: yellow">✪水平权限</font>

Horizontal Access Control，访问控制攻击，即水平权限安全攻击。

相对于垂直权限，水平权限问题是同一个角色上，Web应用程序接收到用户修改信息的请求，未对该信息的所属人进行校验，直接从用户提交的request参数（用户可控数据）中获取数据所属人id，进而导致恶意攻击者通过篡改数据ID，达到修改其他用户数据的目的。即缺少一个用户与数据的对应关系。

![image](uploads/50608/2ad45f6c-3e48-46e2-9237-5c83bc83e531/image.png)

基本防御原则是如果修改的是当前登录用户的信息，则从Session中获取当前用户的id，不要使用前端传递过来的id，各开发人员在编码时要注意此类场景，非此类场景的请求，需要确保应用中具有垂直权限访问控制。另外，也可对一些参数进行加密处理，在服务端进行校验。

## <font style="background: yellow">✪认证与会话管理</font>

通常，通过错误使用应用程序的身份认证和会话管理功能，攻击者或者利用其它开发缺陷来暂时性或永久性冒充其他用户的身份。

### <font style="background: yellow">✪认证管理</font>

可参考《浩鲸科技产品安全研发规范V1.0》中口令与认证管理章节的内容。

### <font style="background: yellow">✪会话管理</font>

解决方法：

**Cookie设置http only与secure属性**

尽量不要在Cookie中设置一些不必要的信息。如果是业务需要，则对于不在前端使用的Cookie设置http only属性，而在前端使用且是敏感信息的Cookie，则需要进行加密处理，并配合https协议来部署应用。所有设置http only属性的cookie要调用统一的接口。

Java中设置Cookie http only属性的代码如下：

```java
response.setHeader("SET-COOKIE", "user=" + request.getParameter("cookie") + "; HttpOnly");
```

浏览器默认在http协议下请求一个站点时，会发送明文Cookie，如果网络中有监控，则可能被截获。如果Web应用网站全站是https的，则可以设置Cookie的Secure属性，这样浏览器只会在https协议下发送Cookie。攻击者即使窃听网络，也无法获取用户明文Cookie。

Cookie 设置Secure属性后，只有在https协议下访问应用时，浏览器才会发送COOKIE，开发人员需要了解该特性。

设置Cookie Secure属性的代码如下：

```java
response.setHeader("SET-COOKIE", "user=" + request.getParameter("cookie") + "; HttpOnly ; Secure ");
```

**Session Fixation 与Expires攻击**

**Session Fixation，session固定攻击。**

如果请求URL中携带有jsessionid，则攻击者可以事先获取一个未认证的SessionID，然后发送给用户去认证，此时由于登录后应用未更新SessionID的值，则攻击者可利用该SessionID直接登录受害者的账户。因此，在用户成功登录应用后，要注销原来的session并为用户重新生成一个新的session，以防御session固定攻击。

Spring Security参考实现如下:

```java
private void sessionManagement(HttpSecurity http) throws Exception {
    http.sessionManagement()
        ……
    }
```

或参考如下实现，若session中已经设置属性，则需将原来的属性存储到新的session中：

```java
public static void reGenerateSessionId() {
        HttpSession session = currentSession.get();
        HttpServletRequest req = RequestUtil.getRequest();
        if (session != null && req != null) {
            // 将原session中的属性移到一个临时Map中
            Map<String, Object> tempMap = new HashMap<String, Object>();
            Enumeration<String> sessionNames = session.getAttributeNames();
            while (sessionNames.hasMoreElements()) {
                String sessionName = sessionNames.nextElement();
                tempMap.put(sessionName, session.getAttribute(sessionName));
            }
            // 注销登录之前的session,产生一个新的sessionId
            session.invalidate();
            session = req.getSession(true);
            //copy原session中的属性到新的session中
            for (Map.Entry<String, Object> entry : tempMap.entrySet()) {
                session.setAttribute(entry.getKey(), entry.getValue());
            }
            //将新的session设置成线程的本地变量值
            currentSession.set(session);
        }
    }
```

Session Expires，Session有效期安全攻击或Session保持攻击。

如果攻击者通过某种方式获取到用户的SessionID，且应用未对Session设置强制超时时间，攻击者一旦曾经获取过用户的Session，就可以一直使用。需要对session设置超时时间、同一账号的在线人数以及超过在线人数后登录策略，踢出或者禁止登录，最好支持可配，提高应用的可用性。

基于Spring Security开发的产品参考如下：

```java
private void sessionManagement(HttpSecurity http) throws Exception {
 http.sessionManagement()
    .maximumSessions(securityProperties.getMaxSessions())
    .maxSessionsPreventsLogin(securityProperties.isMaxSessionsPreventsLogin())
        ……
    }
```

或参考如下实现：

```java
// 用户在线扫描，将超时未操作的用户在在线用表中的状态置为失效
Long maxIdleMinutes = defaultTimeoutMinute
// 当前时间的30min之前的，即用户没操作时间
Date date = new Date(DateUtil.getNowDate().getTime() - 1000 * 60 * maxIdleMinutes);
// 同时将在线用户标记为X
List<SsoUserOnlineDto> list =
new UserOnlineManager().queryAndDeleteTimeOutUser(date);
// 记录日志
if (list != null && !list.isEmpty()) {
    ……
}
//将失效状态的用户session注销
if (!isUserOnline) {
  session.invalidate();
  logger.info("user has offline. sessionId = [{}], userId=[{}]", session.getId(), userId);
  return true;
}
```

## <font style="background: yellow">✪不安全的重定向</font>

URL Redirect，URL跳转攻击。Web应用程序接受用户输入的URL，或者http请求参数包含URL值，且Web应用程序未做任何校验就将请求重定向到该URL，攻击者如果修改URL的值为恶意站点的地址，将会造成网络钓鱼诈骗并窃取用户凭据。

通常使用URL白名单机制来解决重定向问题，限制应用跳转的地址，最好提供一个公共接口，涉及到地址跳转的地方统一由该接口进行白名单校验，可参考如下实现方式：

- 信任URL白名单机制

如果URL跳转仅限于公司内部的应用，则可以使用信任跳转URL白名单机制，在白名单中则跳转，否则，将当前会话置为失效，记录日志并跳转到错误页面，代码示例如下：

```java
String trustedList = ConfigurationMgr.instance().getString("urlRedirect.trustedList", "");
 if (StringUtil.isNotEmpty(trustedList) && trustedList.indexOf(paramValue) < 0) {
    String rootStr = UrlUtil.getWebRoot(request);
    request.getSession().invalidate();
    response.sendRedirect(rootStr + "/Error.do?SSO_ERROR_CODE=P_ILLEGAL_URL");
}
```

- 关于重定向中的参数需要进行URL编码，具体参见XSS部分，避免带来XSS攻击。

## SSRF

SSRF(Server-Side Request Forgery)，服务器端请求伪造。

Web服务器从上游组件接收URL，但它不能有效地确保将请求发送到预期的目标地址。通过向不可信的主机或端口提供URL，攻击者可以看到服务器正在发送的请求，并绕过阻止攻击者直接访问URL的防火墙等访问控制。 服务器被用作代理来对内部网络中的主机进行端口扫描，使用其他URL，例如可以访问系统上的文档（使用file：//），或使用其他协议，如gopher://或tftp ://，可以提供对请求内容的更大控制。

恶意攻击者通过SSRF可以做到：

1. 对外网、服务器所在内网、本地进行端口扫描，获取一些服务器的banner信息；
2. 攻击运行在内网或本地的应用程序（比如溢出）；
3. 对内网web应用进行指纹识别，通过访问默认文件实现；
4. 攻击内外网的web应用，主要是使用get参数就可以实现的攻击；
5. 利用file协议读取本地文件等。

业务产品如果存在从服务端发起http请求的场景，且请求URL是用户可控数据，可对用户输入的URL参数使用正则表达式进行过滤或者使用白名单机制，可参考如下实现：

```java
^(https?):\/\/(([a-zA-Z0-9\._-~]+\.[a-zA-Z_-~]+)|(localhost)|(([0-9]{1,3}\.){3}[0-9]{1,3}))(:[0-9]+)?\/[^\s:\|]*$
private void validateWsUrl(String wsUrl) throws BaseAppException {
        String appWsUrlRegExp =
 Config.getInstance().getParam("APP_WEBSERVICE_URL_REGEXP", "false").trim();
        if (StringUtil.isNotEmpty(appWsUrlRegExp)
 && !"false".equalsIgnoreCase(appWsUrlRegExp) && StringUtil.isNotEmpty(wsUrl)) {
            String[] params = wsUrl.split(";");
            Pattern pattern = Pattern.compile(appWsUrlRegExp);
            if (!pattern.matcher(params[0]).matches()) {
                ExceptionHandler.publish("S-APP-10007", ExceptionHandler.BUSS_ERROR);
            }
        }
    }
```

## <font style="background: yellow">✪加密算法与随机数</font>

### <font style="background: yellow">✪密钥管理</font>

禁止将密钥硬编码到代码里，如下反例代码：

<font color="red">反例</font>

```java
public boolean verifyAdmin(String pwd) {
  if (pwd.equals( "34783fdfsd9sfds")) {
    ……
}
}
```

禁止将加密密钥、签名的salt等“key”硬编码到代码中，如下反例代码：

<font color="red">反例</font>

```java
byte[] key =  "My Encryption Key".getBytes();
DESKeySpec desKeySpec = new DESKeySpec(key);
```

应将密钥（包括密码）保存在配置文件中或者数据库中，在使用时由程序读出密钥并加载到内存中。另外，密钥所在的配置文件与数据库需要严格的控制访问权限，同时配置文件中的密钥要使用强加密算法进行加密。

### <font style="background: yellow">✪伪随机数</font>

使用足够强壮的随机数生成算法，Java中使用java.security.SecurtiyRandom。

在加密算法的选择和使用上，有以下最佳实践：

1. 不要使用ECB模式；
2. 不要使用流密码（如RC4）；
3. 使用HMAC-SHA1代替MD5，或SHA1；
4. 不要使用相同的key做相同的事情；
5. salts与IV需要随机产生；
6. 不要自己实现加密算法，使用安全专家已经实现好的库；
7. 不要依赖系统的保密性

建议：

1. 使用CBC模式的AES256用于加密；
2. 使用HMAC-SHA512用于完整性检查；
3. 使用带salt的SHA-256或SHA-512用于hashing。

## 数据安全

参考《浩鲸科技产品安全研发规范V1.0》中数据安全的要求。

# Web框架安全

一般来说，当我们深入理解问题的本质后，在正确的地方实施针对性的安全方案。对于一些主要的安全威胁，如XSS、CSRF、SQL注入、访问控制、认证、URL跳转等不涉及业务逻辑的安全问题，可以统一在框架中得到解决，并能够大大减轻程序员的工作量，节约人力成本，也能够降低程序员一个个修补造成的遗漏风险。另外，如果在每个业务里修补安全漏洞，补丁的标准难以统一，而在框架中集中实施的安全方案，可以使所有基于框架开发的业务受益，也更容易评估安全方案的有效性。

在此背景下，前端框架的Portal产品以及基于Spring Security开发的鉴权客户端，针对适合在框架层面控制的安全问题进行实现，并根据应用部署场景提供有对应的API，如Cookie设置HttpOnly属性、密码校验、记录服务日志等。

以下内容是Portal已经实现的安全功能，涉及到的一些配置在portalConfig.properties文件中。以下内容是Portal已经实现的安全功能，涉及到的一些配置在portalConfig.properties文件中。由于考虑到兼容性，一些安全配置默认是关闭的，基于Portal开发的产品开发人员需注意。而不是基于Portal开发的产品请参考第2、3章节中的解决方案。

## 账号管理

锁定、启用、停用以及设置账号的生效、失效日期。

![image](uploads/50608/2e2165dc-6802-4007-acec-ea5201d308ad/image.png)

## 会话管理

以Portal作为登录入口的应用需注意以下配置项，同时代码中已经实现session固定攻击与超期攻击，并对sessionID设置http only属性，业务侧可不必额外实现。

提供设置Cookie httponly属性的API接口：

com.ztesoft.zsmart.pot.utils.CookieUtils.addCookie(HttpServletResponse, Cookie, boolean)。

```properties
#同一个用户的最大session在线数量
app.security.max-sessions=-1
#同一个用户达到最大在线数之后再次登录是否进行阻止,还是将前一个用户踢出去
app.security.max-sessions-prevents-login=true
#session Cookie相关的配置
#cookie里面存储sessionid的名称,默认是SESSION
server.session.cookie.name=SESSION
#path在多中心集成环境,默认为/,在单体环境默认是应用名
server.session.cookie.path=/
server.session.cookie.domain=localhost
server.session.cookie.max-age=3600
```

## 口令管理

以Portal作为登录入口并进行密码校验的产品，可通过配置满足对应的安全需求，不必额外实现。

同时Portal提供密码规则校验API：

前端：portal.utils.isMatchPwdRule(password, that.pwdComposition)

服务端工具类：com.ztesoft.zsmart.pot.utils.PasswordRuleUtil

RestAPI：请求URL：pwd/validity，传递密码参数pwd：xxx

- 根据产品需求设置安全级别

![image](uploads/50608/6bda1c7a-93fd-46d9-b1b2-df6973ec5a36/image.png)

- 口令管理配置界面，可配置不同级别的口令复杂度、长度、密码有效期等。

![image](uploads/50608/fa0bc46f-4da9-4e98-b0c6-8bccf3f45071/image.png)

```properties
密码重试次数、自动解锁时间配置。
#密码允许的错误次数，默认为3
app.security.exceed-retry-limit=3
#密码有效期到达之前几天提醒
app.security.password-expired-remind=10
#锁定多长时间自动解锁(单位：分钟)
app.security.autoUnlockTime=30
#自动解锁定时器多久执行(单位：分钟)
app.security.autoUnlockTaskInterval=30
```

## XSS

Portal 目前在服务端，采用XSS filter黑名单的方式，对输入数据进行敏感词匹配并转义，该功能默认是关闭的，开启后将会根据黑名单规则转义请求参数。前端则主要是fish框架从控件层面对输出进行转义。

上述措施只是从一定程度上防御XSS，不能从整体上杜绝XSS攻击，各产品都应该按照2.1中的解决方案排查代码，根据输出语境选择合适的转义函数对输入数据进行转义。

```properties
#是否开启XSS过滤功能，默认关闭
app.security.enableXss=false
```

## CSRF

Portal CSRF防御方案是基于Spring Security实现的，从应用整体对除(GET|HEAD|TRACE|OPTIONS)方法外的请求进行CSRF token校验。该校验默认是开启的，如果关闭该校验，则配置csrf-url-skip为/*或者设置为开发者模式。

如果业务侧ajax请求使用的是Portal前端RestAPIHelper.js中提供的接口，则不用再在头部添加token，否则，请参看2.2根据对应场景添加token。服务端则由框架来校验token，业务无需额外实现。

```properties
#跳过CSRF校验的url
app.security.csrf-url-skip=
#排除某个请求不需要经过session验证
app.security.excludeUrl=
```

## 防盗链

防盗链Referer判断，作为CSRF防御的补充，配置如下：

```properties
#跳过referrer校验的url，以'/'开头,多个url以'|'分隔。如果url带有参数，在url后面加上'[?].*'
app.security.referrerUrlSkip=
#防盗链referrer域名白名单,默认为空表示不校验,多个以逗号分隔
app.security.referrerWhiteList=
```

## 上传/下载

Portal针对上传文件功能，根据配置文件做如下校验：

1. 检验文件上传路径是否在配置的白名单中
2. 生成随机文件名
3. 检查文件类型（包括文件头部类型是否被篡改）与大小（支持根据文件类型配置文件大小）
4. 防止文件路径猜解

```properties
#文件上传下载配置
#windows系统目录分隔符用\\,如 D:\\home
#linux系统目录分隔符用/,如 /home
#上传文件在服务器上的物理路径,只能配置一个。
file.upload.directory= /home/upload
#最大上传文件大小，单位字节，默认10MB
file.upload.maxFileSize=10485760
#上传文件类型
file.upload.type=
#默认为false,true表示严格模式，禁止上传路径中包含./或者.\的文件
file.upload.strictValidation=false
#文件类型与文件头部编码映射关系（文本类型不受限制）, 如jpg:FFD8FFE000104A|******
#默认不配置，采用框架默认值，如果有额外类型定义，需要同时定义以下两个参数
file.upload.extendsMimeTypes=
file.upload.checkHeaderLength=-1
#文件类型:文件大小,文件类型与文件大小之间以冒号(:)分隔,多个配置以逗号(,)分隔,
#其中文件大小单位为字节(b).如jpg:12345,bmp:12,xls:124,xlsx:123456
file.upload.fileSize4Type=
```

Portal针对下载文件功能，根据配置文件做如下校验：

1. 校验文件路径是否在白名单
2. 防止文件路径猜解
3. 文件下载权限校验（通过加密路径并与用户信息绑定）

```properties
#允许下载的文件路径，多个目录用逗号隔开,下载路径不配置默认使用文件上传目录
file.download.directory=
#默认为false,true表示严格模式，禁止下载路径中包含./或者.\的文件
file.download.strictValidation=false
#文件下载是否启用文件相对路径加密模式，同时实现权限控制
file.download.encryptFilePath=false
```

如果业务产品与Portal不是分离部署，业务产品可直接使用Portal提供的上传与下载接口/file/upload、/file/uploads/file/download来上传/下载文件。

如果业务产品与Portal是分离部署，则需要业务产品自己写controller实现文件上传到业务侧的应用服务器上，如/billing/file/upload，可参考portal-web包中的上传/下载接口，当然业务侧也可自行实现。

com.ztesoft.zsmart.pot.controller.UploadDownloadController。

## 服务权限

框架默认关闭菜单、界面元素与角色服务权限的校验，且是基于Spring Security来实现的，业务产品根据具体的服务校验需求开启对应的配置，并在界面上配置角色、组件、菜单对应的服务请求权限，根据业务实际场景分配权限给用户即可。代码层面无需做额外实现。

```properties
#是否启用基于菜单的访问控制列表的校验
app.security.enable-acl=false
#是否启用基于界面元素的访问控制列表的校验
app.security.enable-cacl=false
#是否启用基于角色的访问控制的校验
app.security.enable-rbac=false
```

角色服务权限配置界面：

![image](uploads/50608/f3f01141-e0b6-49e8-a356-019f0f4aec01/image.png)

组件服务权限配置界面，通过右键点击界面元素，其中界面元素需以下规则才能触发右键事件：

```javascript
// 指定触发右键菜单的元素选择器
selector: "button,div>.ui-nav-button,input[type='button'],
div.ui-jqgrid-pager li,.ui-tabs[priv]>.ui-tabs-nav>li>a,div.grid th"
```

![image](uploads/50608/39bbe376-96ff-412f-a9ef-cd176b886d7b/image.png)

菜单服务权限配置：

![image](uploads/50608/c26347f1-534d-4864-9cba-3875c4494a1d/image.png)

## 日志管理

包含登录日志、系统日志、审计日志。

记录日志服务为：com.ztesoft.zsmart.pot.service.AuthLogService

前端在CommonAction.js文件中提供有调用记录服务日志的接口如下：

```javascript
addServiceLog: function(logDto) {
   return fish.post('servicelog', logDto); // 该方法用于记录业务log
 },
```

其中，Portal对登录、注销、配置参数的修改以及Portal菜单中的添加、删除、修改、授权、取消权限、鉴权、修改用户口令等事件已经在应用中记录了日志；同时，业务产品也需要对重要业务数据的创建、删除、修改、查询等事件记录日志，以便回溯。

对于上述事件的结果，不管是成功还是失败，都需要记录日志。

![image](uploads/50608/64b59939-6ada-4bac-bbb5-39ed3a050260/image.png)

## CORS

跨域资源共享时， Portal默认配为*，即允许跨域，以满足开发环境中前后端分离的场景。生成环境禁止置为*。如果没有跨域需求，请置为空，表示不允许跨域，以防御跨域请求漏洞。如果业务侧存在跨域访问Portal服务的需求，请根据实际情况配置允许跨域访问的应用的域名,多个域名以逗号分隔。

```properties
#跨域资源访问源域名配置,多个域名请以逗号分隔,默认为*,即应用允许跨域进行访问
app.security.allowOrigin=*
```

## 点击劫持

X-Frame-Options选项支持可配置，其中xFrameAllowFrom只支持配置一个源，如果逗号分隔配置多个源，浏览器默认匹配第一个。

备注：谷歌浏览器不支持ALLOW-FROM选项，页面会正常加载。

```properties
#HTTP响应头配置
#默认为SAMEORIGIN,可配置为DENY,ALLOW-FROM,如果配置为空,则不添加该头部
app.security.xFrameOptions=SAMEORIGIN
#如果xFrameOptions配置为ALLOW-FROM,则需要配置该属性，共三种策略,格式为policy;源
#static;源
#regexp;支持配置源正则表达式
#whitelist;支持配置多个源,逗号分隔
app.security.xFrameAllowFrom=
```

Content-Security-Policy响应头部指令支持可配置，该头部会限制加载的静态资源，而且指令很多且比较严格，框架默认不进行配置，产品根据安全需求酌情配置。

```properties
#HTTP响应头配置,用以限制页面加载的资源，默认为空，即不添加该头部
app.security.contentSecurityPolicyDirectives=
#加载的资源不符合CSP头部指令时，只报告错误,资源正常加载，默认false，调试用,策略使用配置的CSP指令
app.security.contentSecurityPolicyReportOnly=false
```

## 工具类

提供CookieUtil工具类，实现配置cookie的HttpOnly、Secure属性。

工具类：com.ztesoft.zsmart.pot.util.CookieUtil

# 参考说明

1. 《阿里巴巴集团web安全标准Ver1.4》

2. V8、V9等产品内部测试时发现的安全问题

3. 《白帽子讲Web安全》

4. [https://www.owasp.org/index.php/XSS_Filter_Evasion_Cheat_Sheet](https://www.owasp.org/index.php/XSS_Filter_Evasion_Cheat_Sheet)

5. [https://github.com/OWASP/CheatSheetSeries/blob/master/cheatsheets/Cross_Site_Scripting_Prevention_Cheat_Sheet.md](https://github.com/OWASP/CheatSheetSeries/blob/master/cheatsheets/Cross_Site_Scripting_Prevention_Cheat_Sheet.md)

6. [https://www.owasp.org/index.php/OWASP_Java_Encoder_Project#tab=Use_the_Java_Encoder_Project](https://www.owasp.org/index.php/OWASP_Java_Encoder_Project#tab=Use_the_Java_Encoder_Project)

# 本文件评审、修正记录

| 文件名称 | WEB应用安全开发规范                                    |               |               |        |
| -------- | ------------------------------------------------------------ | ------------- | ------------- | ------ |
| 序号     | 流程                                                         | 拟制人/审核人 | 拟制/审核时间 | 版本号 |
| 1        | 编写                                                       | 赵灵歌               |               | V0.1   |
| 2        | 首次发布                                                   | 产品安全能力中心       | 2019/5/15    | V1.0   |
