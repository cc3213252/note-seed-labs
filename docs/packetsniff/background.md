# 数据包嗅探和伪造背景

## 网络接口卡

设备通过网络接口卡（network interface card, NIC，简称网卡）接入网络。每个网卡都有一个硬件地址，叫MAC地址。  

!!! 广播型介质

    网络中的设备均连接到一个共享的介质上。常用的本地通信网络、以太网和WIFI都是广播型介质。

!!! 内核处理普通数据包原理

    当数据包在传播介质中流动时，网络中的每个网卡都能听到所有广播的数据帧（frame），这些数据帧会被复制到
    网卡的内存中，网卡会检查数据帧头部的目的地址。如果目的地址和该网卡的MAC地址相匹配，那么该数据帧就会
    通过直接存储器访问（direct memory access, DMA）的方式被复制到操作系统内核的缓存中，接着网卡会
    以中断的方式告诉CPU它接收到了新的数据，然后CPU会将它们全部从缓存中复制到一个队列中，以便为新数据包
    的到来腾出空间。根据协议规定，内核在处理队列中的数据包时会调用不同的回调函数。

!!! 混杂模式

    promiscuous mode，嗅探程序要处理目标地址和自身MAC地址不匹配的数据帧，要把网卡设置成混杂模式。
    一般是网络管理员诊断网络问题或者是黑客监听使用。有线网络使用。

!!! 监听模式

    monitor mode，无线网卡是通过监听模式进行嗅探的。由于无线网络存在相邻设备干扰的问题，会严重影响网络的
    性能，为了解决这个问题，wifi设备通过不同的信道传递数据，接入点将相邻设备用不同的信道连接起来，从而减少了
    冲突带来的影响。wifi网卡的设计也做了相应的调整，可以在整个可用带宽和信道的分片上进行通信，由于这样的设计，
    当网卡处于监听模式时，它只能捕捉所监听信道中的802.11数据帧。  
    这意味着，与以太网能监听所有数据帧不同，由于存在不同的信道，可能会错过一个网络中其他信道传输的信息。大多数
    无线网卡都不支持监听模式，即使支持，默认也是禁用。

## BSD数据包过滤器

当进行网络嗅探时，嗅探器经常只会对某些特定类型的数据包感兴趣，如TCP数据包或者DNS数据包。  
系统可以将所有捕获到的数据包交给嗅探程序，嗅探程序会丢弃它不需要的数据包，但是这种处理方式效率低下，因为
把这些没用的数据包从内核传到嗅探程序是需要花费CPU时间的。  

UNIX操作系统定义了BSD数据包过滤器(BSD packet filter, BPF)，用于在底层实现数据包的过滤。BPF允许用户
空间的程序将一个过滤器和一个套接字进行绑定，其本质上是为了告知内核尽早丢弃不需要的数据包。  
过滤器一般是首先使用布尔操作符编写的可读性较强的代码，随后该代码被编译成伪代码传递给BPF驱动。

经过编译的bsd代码如下：
![编译过的bsd代码](../img/packet-bsd.png)
这段BPF代码只过滤了22号端口，但可读性很差，再绑定socket：
```c
struct sock_fprog bpf = {
    .len = ARRAY_SIZE(code);
    .filter = code,
};

setsockopt(sock, SOL_SOCKET, SO_ATTACH_FILTER, &bpf, sizeof(bpf));
```
与bpf一旦与socket绑定，当数据包到达内核时，回调函数就会被调用，用于判断该数据包是否应该过滤。通过过滤的数据
包被压入协议栈。