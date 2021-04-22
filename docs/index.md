# 网络安全Seed Labs实验笔记

 [项目源代码](https://github.com/cc3213252/note-seed-labs)

## Set-UID攻击

* [Set-UID背景](./setuid/background.md)
* [Set-UID的主要攻击面](./setuid/attack-setuid.md)
* [通过system函数攻击](./setuid/attack-system.md)
* [用execve代替system](./setuid/use-execve.md)
* [攻击php调外部命令](./setuid/attack-php.md)

## 环境变量攻击

* [环境变量背景](./env/background.md)
* [攻击动态链接库](./env/attack-lib.md)
* [攻击外部程序](env/attack-outprogram.md)
* [攻击程序本身](env/attack-program.md)

## Shellshock攻击

* [Shellshock背景](./shellshock/background.md)
* [攻击Set-UID](./shellshock/attack-setuid.md)
* [攻击CGI程序](./shellshock/attack-cgi.md)
* [攻击PHP程序](./shellshock/attack-php.md)

## 缓冲区溢出攻击

* [程序运行原理](./overflow/program.md)
* [准备攻击环境](./overflow/env-perpare.md)
* [构造shellcode](./overflow/shellcode.md)
* [防御措施](./overflow/defense.md)
* [攻破bash保护](./overflow/attack-bashguard.md)

## return-to-libc攻击

* [return-to-libc背景](./returntolibc/background.md)
* [发起return-to-libc攻击](./returntolibc/attack.md)

## 格式化字符串漏洞

* [格式化字符串漏洞背景](./formatvul/background.md)
* [攻击格式化字符串漏洞](./formatvul/attack.md)
* [注入恶意代码](./formatvul/malware.md)
* [防御措施](./formatvul/defense.md)

## 竟态条件漏洞

* [竟态条件漏洞攻击](racecondition/attack.md)
* [防御措施](./racecondition/defense.md)

## 脏牛竟态条件攻击

* [脏牛攻击背景](dirtycow/background.md)
* [脏牛漏洞攻击](dirtycow/attack.md)

## 跨站请求伪造

* [CSRF背景](csrf/background.md)
* [CSRF攻击GET](csrf/attack-get.md)
* [CSRF攻击POST](csrf/attack-post.md)
* [防御措施](csrf/defense.md)

## 跨站脚本攻击

* [XSS背景](xss/background.md)
* [XSS攻击](xss/attack.md)
* [实现自我传播](xss/self-spread.md)