# 抵御XSS攻击

XSS漏洞的根本原因是HTML允许JavaScript中的代码和数据混编。  
有两种方法可以防御XSS攻击：  
1、过滤数据中的代码，或把代码转成数据  
2、强制开发者把代码和数据分开，然后对代码部分添加约束条件  

## 去除代码

有两种方法：  
1、过滤掉数据中的代码  
2、通过编码把代码转换成数据  

### 过滤方法

由于JavaScript代码混在数据中的方法很多，使用script标签不是唯一注入方法，有开源库可以使用jsoup，不建议自己开发。

### 编码方法

攻击的代码被服务器编码，浏览器看到后，再还原显示

### Elgg的防范策略

elgg综合使用了上面两种，用HTMLawed的PHP模块过滤，用htmlspecialchars的PHP函数来编码，只是实验中关闭了。

## 用内容安全策略来抵御XSS攻击

!!! 网页中放入js代码两种方式

    嵌入式：代码直接在网页中。  
    引入式：把代码放在另外一个文件或url中，包含进网页  
    
**嵌入式代码是导致XSS漏洞的罪魁祸首。**xss攻击者虽然也可以用引入式方法在数据中加入代码，但无法将代码
放在被网站信任的地方。  
告诉浏览器哪些来源是可以信任的是通过一个叫做内容安全策略的机制实现的（CSP content security policy）。  
通过CSP，网站可以通过在回复的头部加入一些CSP规则，告诉浏览器不要运行页面中嵌入的任何JavaScript代码，
所有代码都必须从网站单独下载。  

比如如下CSP规则： 
```text
Content-Security-Policy: script-src 'self'
```
不仅禁止了所有嵌入式代码，还规定只有来自和该网页同一网站的代码才可以被执行（这是self的意义）。在这个规则下，
引入js必须这样写：  
```html
<script src="myscript.js"></script>
```

但有时需要运行从其他可以信任的网站下载的代码，CSP允许提供一个白名单，如：  
```text
Content-Security-Policy: script-src 'self' example.com 
                         https://apis.google.com
```

***安全地使用嵌入式代码***
如果开发者确想用嵌入式的方法把代码放到网页中，CSP也提供了一种安全的做法，就是要求在CSP规则中指明哪些嵌入代码是
可信的。有两种：  
1、把可信代码的单项哈希值放在CSP规则中  
2、用nonce，在CSP规则中设置一些可信任的nonce  
```text
Content-Security-Policy: script-src 'nonce-34fo3er92d'
```
```html
<script nonce="34fo3er92d">...</script>
```
