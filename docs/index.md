# 网络安全攻防实验

 [项目源代码](https://github.com/cc3213252/note-seed-labs)

## 软件安全

<table border="0">
    <tr>
        <td><strong>Set-UID攻击</strong></td>
        <td><a href="setuid/background">背景</a></td>
        <td><a href="setuid/attack-setuid">Set-UID的主要攻击面</a></td>
        <td><a href="setuid/attack-system">通过system函数攻击</a></td>
        <td><a href="setuid/use-execve">用execve代替system</a></td>
        <td><a href="setuid/attack-php">攻击php调外部命令</a></td>
    </tr>
    <tr>
        <td><strong>环境变量攻击</strong></td>
        <td><a href="env/background">背景</a></td>
        <td><a href="env/attack-lib">攻击动态链接库</a></td>
        <td><a href="env/attack-outprogram">攻击外部程序</a></td>
        <td><a href="env/attack-program">攻击程序本身</a></td>
    </tr>
    <tr>
        <td><strong>Shellshock攻击</strong></td>
        <td><a href="shellshock/background">背景</a></td>
        <td><a href="shellshock/attack-setuid">攻击Set-UID</a></td>
        <td><a href="shellshock/attack-cgi">攻击CGI程序</a></td>
        <td><a href="shellshock/attack-php">攻击PHP程序</a></td>
    </tr>
    <tr>
        <td><strong>缓冲区溢出攻击</strong></td>
        <td><a href="overflow/program">程序运行原理</a></td>
        <td><a href="overflow/env-perpare">准备攻击环境</a></td>
        <td><a href="overflow/shellcode">构造shellcode</a></td>
        <td><a href="overflow/defense">防御措施</a></td>
        <td><a href="overflow/attack-bashguard">攻破bash保护</a></td>
    </tr>
    <tr>
        <td><strong>return-to-libc攻击</strong></td>
        <td><a href="returntolibc/background">背景</a></td>
        <td><a href="returntolibc/attack">发起攻击</a></td>
    </tr>
    <tr>
        <td><strong>格式化字符串漏洞</strong></td>
        <td><a href="formatvul/background">背景</a></td>
        <td><a href="formatvul/attack">攻击格式化字符串漏洞</a></td>
        <td><a href="formatvul/malware">注入恶意代码</a></td>
        <td><a href="formatvul/defense">防御措施</a></td>
    </tr>
    <tr>
        <td><strong>竟态条件漏洞</strong></td>
        <td><a href="racecondition/attack">竟态条件漏洞攻击</a></td>
        <td><a href="racecondition/defense">防御措施</a></td>
    </tr>
    <tr>
        <td><strong>脏牛竟态条件攻击</strong></td>
        <td><a href="dirtycow/background">背景</a></td>
        <td><a href="dirtycow/attack">脏牛漏洞攻击</a></td>
    </tr>
</table>

</br>

## Web安全

<table border="0">
    <tr>
        <td><strong>跨站请求伪造</strong></td>
        <td><a href="csrf/background">背景</a></td>
        <td><a href="csrf/attack-get">CSRF攻击GET</a></td>
        <td><a href="csrf/attack-post">CSRF攻击POST</a></td>
        <td><a href="csrf/defense">防御措施</a></td>
    </tr>
    <tr>
        <td><strong>跨站脚本攻击</strong></td>
        <td><a href="xss/background">背景</a></td>
        <td><a href="xss/attack">XSS攻击</a></td>
        <td><a href="xss/self-spread">实现自我传播</a></td>
        <td><a href="xss/defense">防御措施</a></td>
    </tr>
    <tr>
        <td><strong>SQL注入攻击</strong></td>
        <td><a href="sqlinjection/background">背景</a></td>
        <td><a href="sqlinjection/attack">SQL注入攻击</a></td>
        <td><a href="sqlinjection/defense">防御措施</a></td>
    </tr>
</table>

</br>

## 网络安全

<table border="0">
    <tr>
        <td><strong>数据包嗅探和伪造</strong></td>
        <td><a href="packetsniff/background">背景</a></td>
        <td><a href="packetsniff/packet-sniffing">嗅探</a></td>
        <td><a href="packetsniff/tools">工具</a></td>
        <td><a href="packetsniff/packet-spoofing">伪造</a></td>
        <td><a href="packetsniff/sniff-spoof">嗅探与伪造</a></td>
    </tr>
    <tr>
        <td><strong>对TCP的攻击</strong></td>
        <td><a href="tcp/background">TCP攻击背景</a></td>
        <td><a href="tcp/syn-attack">SYN泛洪攻击</a></td>
        <td><a href="tcp/rst-attack">TCP复位攻击</a></td>
        <td><a href="tcp/session-attack">TCP会话劫持</a></td>
    </tr>
    <tr>
        <td><strong>防火墙</strong></td>
        <td><a href="firewall/background">防火墙基本概念</a></td>
        <td><a href="firewall/netfilter">用Netfilter实现一个防火墙</a></td>
        <td><a href="firewall/iptables">用iptables实现一个防火墙</a></td>
        <td><a href="firewall/stateful">状态防火墙和应用防火墙</a></td>
        <td><a href="firewall/evading">绕过防火墙</a></td>
    </tr>
    <tr>
        <td><strong>对DNS的攻击</strong></td>
        <td><a href="dns/background">DNS基本概念</a></td>
        <td><a href="dns/conf-env">配置DNS实验环境</a></td>
        <td><a href="dns/attack-local">本地DNS缓存中毒攻击</a></td>
        <td><a href="dns/attack-remote">远程DNS缓存中毒攻击</a></td>
        <td><a href="dns/evil-reply">恶意DNS服务器伪造攻击</a></td>
        <td><a href="dns/defense">预防DNS缓存中毒攻击</a></td>
    </tr>
    <tr>
        <td><strong>虚拟专用网络</strong></td>
        <td><a href="vpn/background">VPN基本概念</a></td>
        <td><a href="vpn/vpn-detail">基于TLS/SSL的VPN原理细节</a></td>
        <td><a href="vpn/develop-vpn">开发VPN程序</a></td>
        <td><a href="vpn/network-setting">VPN的网络配置</a></td>
    </tr>
    <tr>
        <td><strong>心脏滴血漏洞</strong></td>
        <td><a href="heartbleed/attack">攻击</a></td>
    </tr>
    <tr>
        <td><strong>公钥基础设施</strong></td>
        <td><a href="pki/public-key">公钥证书</a></td>
        <td><a href="pki/ca">认证机构</a></td>
        <td><a href="pki/root-middle-ca">根与中间CA</a></td>
        <td><a href="pki/defense-mid-attack">防御中间人攻击</a></td>
    </tr>
    <tr>
        <td><strong>传输层安全</strong></td>
        <td><a href="transport/background">TLS概述</a></td>
        <td><a href="transport/client">TLS客户端编程</a></td>
        <td><a href="transport/mid-attack">中间人攻击没主机校验的服务</a></td>
        <td><a href="transport/server">TLS服务器编程</a></td>
    </tr>
</table>

</br>

## 硬件和系统安全

<table border="0">
    <tr>
        <td><strong>Meltdown攻击</strong></td>
        <td><a href="system/background">概述</a></td>
        <td><a href="system/flushreload-attack">刷新与重载攻击</a></td>
        <td><a href="system/kernel-perpare">内核空间写值</a></td>
        <td><a href="system/outoforder-attack">CPU乱序执行攻击</a></td>
    </tr>
</table>

