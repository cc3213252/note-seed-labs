# 绕过防火墙

最有效的绕过防火墙的方法是隧道技术，它能够隐藏数据的真实意图。搭建隧道的方式有很多种，
其中虚拟专用网络（virtual private network, VPN）在IP层搭建隧道，被广泛用来绕过防火墙。

## 使用SSH隧道绕过防火墙

实验场景：  
公司防火墙会拦截所有进入公司的telnet数据，但允许用SSH登陆到内部一台叫apollo的机器  
home是自己机器名称，work是公司内部的一台机器，平时上班和家里都有需要通过telnet到
work机器来工作。

!!! ssh本地端口通过跳板映射到其他机器

    HostA$ ssh -L 0.0.0.0:PortA:HostC:PortC  user@HostB  
    HostA 上启动一个 PortA 端口，通过 HostB 转发到 HostC:PortC上，在 HostA 上运行

故要实现以上需求，只需两条命令：
```bash
ssh -L 8000:work:23 apollo
```
通过apollo，把本机8000端口映射到work的23端口  

```bash
telnet localhost 8000
```
相当于telnet到了work的23端口


另一个实验场景：  
正在使用公司内的work计算机，想访问facebook，但公司防火墙阻止访问。

```bash
ssh -L 8000:www.facebook.com:80 home
```
通过home机器，把本机8000映射到facebook的80端口，只需访问localhost:8000即可绕过防火墙

## 动态端口转发

上面为一个专门的网站建立了一个SSH隧道，那总不可能为每个网站都建一个隧道，就需要使用动态端口转发 

!!! 本地socks5代理

    HostA$ ssh -D localhost:1080  HostB  
    在 HostA 的本地 1080 端口启动一个 socks5 服务，
    通过本地 socks5 代理的数据会通过 ssh 链接先发送给 HostB，再从 HostB 转发送给远程主机  
    那么在 HostA 上面，浏览器配置 socks5 代理为 127.0.0.1:1080，
    看网页时就能把数据通过 HostB 代理出去，类似 ss/ssr 版本，只不过用 ssh 来实现

动态端口转发工作在TCP/IP模型的应用层和传输层之间（即OSI模型的会话层），因此它独立于应用逻辑，比
Web代理更加通用。

## 使用VPN绕过防火墙

最初开发VPN是出于安全考虑，希望提供从外部专用网络到内网的安全访问。然而，如今VPN通常被用来绕过防火墙，
尤其是绕过出口过滤。