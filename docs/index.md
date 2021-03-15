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