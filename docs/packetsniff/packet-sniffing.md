# 数据包嗅探

## socket接收数据包

以下为一个UDP服务器程序，INADDR_ANY表示socket绑定到本机所有ip地址  
```c
// udp_server.c
#include <unistd.h>
#include <stdio.h>
#include <string.h>
#include <sys/socket.h>
#include <netinet/ip.h>

void main()
{
    struct sockaddr_in server;
    struce sockaddr_in client;
    int clientlen;
    char buf[1500];
    
    int sock = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP); 
    memset((char *) &server, 0, sizeof(server));
    server.sin_family = AF_INET;
    server.sin_addr.s_addr = htonl(INADDR_ANY);
    server.sin_port = htons(9090);
    
    if(bind(sock, (struct sockaddr *)&server, sizeof(server)) < 0)
        perror("ERROR on binding");
    
    while(1){
        bzero(buf, 1500);
        recvfrom(sock, buf, 1500-1, 0, (struce sockaddr *)&client, &clientlen);
        printf("%s\n", buf);
    }
    close(sock);
}
```

## 原始套接字数据包嗅探

以上程序只能接收发送给它的数据包，如果目的ip地址是其他设备或者目的端口号不是由该程序注册的端口的话，就无法接收数据包。  
而嗅探器程序需要能够捕捉网络中传输的所有数据包，无论其ip地址和端口号是什么，可以由一种称为原始套接字(raw socket)的
特殊socket实现，如下：  
```c
// sniff_raw.c
#include <unistd.h>
#include <stdio.h>
#include <sys/socket.h>
#include <linux/if_packet.h>
#include <net/ethernet.h>
#include <arpa/inet.h>

int main()
{
    int PACKET_LEN = 512;
    char buffer[PACKET_LEN];
    struct sockaddr saddr;
    struct packet_mreq mr;
    
    int sock = socket(AF_PACKET, SOCK_RAW, htons(ETH_P_ALL)); // 创建raw socket
    mr.mr_type = PACKET_MR_PROMISC;  // 设置为混杂模式
    setsockopt(sock, SOL_PACKET, PACKET_ADD_MEMBERSHIP, &mr, sizeof(mr));
    
    while(1)
    {
        int data_size = recvfrom(sock, buffer, PACKET_LEN, 0, &saddr, (socklen_t*)sizeof(saddr));
        if(data_size)printf("Got one packet\n");
    }
    close(sock);
    return 0;
}
```

!!! 原始套接字和普通套接字的区别

    普通套接字当内核接收到数据包时，它会通过网络协议栈传递数据包，并最终将数据包的载荷（payload）通过socket传递
    给应用程序。  
    对于原始套接字，内核首先会向socket（和它的应用）传递数据包的一份拷贝，包括链路层头部等信息，然后再进一步将数据
    包传递给协议栈。raw socket不会拦截数据包，只是得到了数据包的一份拷贝。

```c
int sock = socket(AF_PACKET, SOCK_RAW, htons(ETH_P_ALL));
```
ETH_P_ALL表示所有协议类型的数据包都应该被传递给raw socket。ETH_P_IP表示只有ip数据包传递给raw socket。
这个程序没有设置数据包过滤，如果过滤可以使用SO_ATTACH_FILTER选项来调用setsockopt  

pcap（packet capture，数据包捕捉）API提供了一种跨平台、高效的数据包捕获机制。特点之一是提供了一个编译器，
使程序员可以用可读性较强的布尔表达式来指定过滤规则。编译器将表达式翻译成为内核可以利用的BPF伪代码。  
libpcap和Winpcap分别是unix和windows中的pcap API。在Linux中，pcap是用raw socket实现的。

## pcap API实现数据包嗅探

```c
#include <pcap.h>
#include <stdio.h>

void got_packet(u_char *args, const struct pcap_pkthdr *header, const u_char *packet)
{
    printf("Got a packet\n");
}

int main()
{
    pcap_t *handle;
    char errbuf[PCAP_ERRBUF_SIZE];
    struct bpf_program fp;
    char filter_exp[] = "ip proto icmp";
    bpf_u_int32 net;
    
    handle = pcap_open_live("enp0s3", BUFSIZ, 1, 100, errbuf); 
    pcap_compile(handle, &fp, filter_exp, 0, net);  //编译过滤表达式
    pcap_setfilter(handle, &fp);  // 把编译好的BPF过滤器交给内核
    pcap_loop(handle, -1, got_packet, NULL); 
    pcap_close(handle);
    return 0;
}
```

```c
pcap_open_live("enp0s3", BUFSIZ, 1, 100, errbuf);
```
这行是开启有效pcap会话，enp0s3是网络设备名，实际ifconfig替换成自己的，1表示开启混杂模式
```c
pcap_compile(handle, &fp, filter_exp, 0, net);  //编译过滤表达式
pcap_setfilter(handle, &fp);  // 把编译好的BPF过滤器交给内核
```
这两行是设置过滤器，BPF过滤器是底层语言写的，开发人员很难阅读，pcap API提供的编译器可以将布尔表达式
转换成底层BPF程序。
```c
pcap_loop(handle, -1, got_packet, NULL); 
```
捕获数据包，第二个参数是希望捕获多少个数据包，-1表示永远不停止，第三个是回调函数
编译sniff.c的命令如下：
```bash
gcc -o sniff sniff.c -lpcap
```

## 处理捕获的数据包

```c
void got_packet(u_char *args, const struct pcap_pkthdr *header, const u_char *packet)
{
    printf("Got a packet\n");
}
```
接收数据包的回调函数中，第三个参数packet是一个指针，指向存储在缓冲区中的数据包。指针类型是unsigned char，说明
缓冲区内存会被当做字符序列进行处理，是有结构的。c语言一个高效处理方法是使用结构体和类型转换的概念。

!!! pcap过滤器实例

    dst host 10.0.2.5 只捕获目的ip地址为10.0.2.5的数据包  
    src host 10.0.2.6 只捕获源ip地址为10.0.2.6的数据包  
    host 10.0.2.6 and src host port 9090 只捕获源或目的ip地址为10.0.2.6，并且源端口号为9090的数据包  
    proto tcp 只捕获TCP数据包  
    
!!! Note

    数据包实际上是一个以太网帧

```c
#include <pcap.h>
#include <stdio.h>
#include <arpa/inet.h>

struct ipheader {
    unsigned char iph_ihl:4,  // ip头长度
                  iph_ver:4;  // ip版本
    unsigned char iph_tos;    // 服务版本
    unsigned short int iph_len;  // ip包长度
    unsigned short int iph_ident;
    unsigned short int iph_flag:3,
                       iph_offset:13;
    unsigned char  iph_ttl;
    unsigned char  iph_protocol;
    unsigned short int iph_chksum;
    struct in_addr iph_sourceip;
    struct in_addr iph_destip;
};

void got_packet(u_char *args, const struct pcap_pkthdr *header, const u_char *packet)
{
    struct ethheader *eth = (struct ethheader *)packet;
    if (ntohs(eth->ether_type) == 0x0800){
        struct ipheader *ip = (struct ipheader *)(packet + sizeof(struct ethheader));
        printf("    From: %s\n", inet_ntoa(ip->iph_sourceip));
        printf("      To: %s\n", inet_ntoa(ip->iph_destip));
        
        switch(ip->iph_protocol){
            case IPPROTO_TCP:
                printf("    Protocol: TCP\n");
                return;
            case IPPROTO_UDP:
                printf("    Protocol: UDP\n");
                return;
            case IPPROTO_ICMP:
                printf("    Protocol: ICMP\n");
                return;
            default:
                printf("    Protocol: others\n");
                return;
}
```