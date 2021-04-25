# 防御措施

防御SQL注入攻击的方法有三种：  
1、过滤掉代码  
2、通过编译把代码变成数据  
3、把代码和数据分开  

## 过滤掉代码和把代码变成数据

比如把撇号进行编码  
编码前：aaa' OR 1=1 #  
编码后：aaa\' OR 1=1 #

PHP的mysqli有一个内置方法，称为mysqli::real_escape_string()，可以编码sql中的特殊字符。
但是这种方法有办法可以绕过。

## 预处理语句


在sql数据库中，预处理语句是用于优化的，当需要多次执行同一条或相似的sql语句时，可以用预处理语句来加快速度。  
使用预处理语句可以向数据库发送一个sql语句模板，模板中保留有些未确定的值（参数），尽管预处理语句不是为安全
而设计的，但是却是一个防御sql注入攻击的理想方法。

比如如下代码：
```php
$conn = new mysqli("localhost", "root", "seedubuntu", "dbtest")
$sql = "select Name, Salary, SSN from employee where eid='$eid' and password='$pwd'";
$result = $conn->query($sql);
```
用php的mysqli扩展提供的预处理语句来改写如下：
```php
$conn = new mysqli("localhost", "root", "seedubuntu", "dbtest")
$sql = "select Name, Salary, SSN from employee where eid= ? and password=?";

if ($stmt = $conn->prepare($sql))
{
    $stmt->bind_param("ss", $eid, $pwd);
    $stmt->execute();
    $stmt->bind_result($name, $salary, $ssn);
    while($stmt->fetch()){
        printf("%s %s %s\n", $name, $salary, $ssn);
    }
}
```
