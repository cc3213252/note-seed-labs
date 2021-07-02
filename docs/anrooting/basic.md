# 安卓rooting

## rooting背景

安卓设备默认用户没有root权限，这对于想深入定制不太方便，安卓设备获取root权限这个过程有个专有名词叫rooting。
为何要获取root权限？比如安卓系统有很多预装软件，用不到又占用资源，需要卸载，往往需要root用户才能卸载。

**从安卓内部获取root**，这种手段会借助一些已经存在的系统漏洞。如果这些漏洞在内核中或者运行在有root权限的
守护进程中，就可以利用这些漏洞获取root权限

rooting概览：
![rooting概览](../img/anrooting-overview.png)

**从安卓外部获取root**，假设我们安装了双系统，只要我们挂载了有安卓系统的分区，就可以修改安卓的系统文件。
安卓设备已经预置了另一个系统在里面，叫recovery模式，为了恢复系统用的，但经常被用来更新操作系统。  
为了防止用户执行任意命令，recovery模式没有提供一个shell提示，取而代之的是用了OTA技术（Over-The-Air）,
就是用一个外部的包，这个包包含了命令和文件用来更新安卓。这个包叫OTA包  

多数OTA包需要有供应商的签名，故需要绕过这个保护机制。

**重新安装recovery系统**，比绕过更简单的方法是重新安装recovery系统。但是有另一个机制阻止我们重装recovery系统，
那就是Bootloader。bootloader用更底层的代码在设备上电后加载系统，当bootloader被锁住时，只能加载已经预装
在设备上的系统。只有把它解锁才能安装定制化的系统。  
制造商往往会出于控制设备上运行软件的目的，把bootloader锁放在安装包的外面，同时也提供让用户可以解锁bootloader
的方法，但是用户这样做会丢失所有数据并无法保修。

## OTA背景

!!! Edify语言

    edify是用来解析zip文件，从而进一步安装安卓系统的脚本语言。edify脚本并不一定是用于固件更新，
    它还可以用来替换、增加、删除特定的文件，甚至是格式化分区。通常情况下，edify脚本在recovery模式下
    flash zip包的时候运行。
    
OTA的结构如下：  
![OTA结构](../img/anrooting-ota-struct.png)

下面两个是edify的两个重要文件：  
update-binary，当用户选择刷入zip时执行的二进制解释器，用来执行OTA更新，他来加载updater-script  
updater-script，edify语言描述的安卓系统安装脚本，是文本文件  
这两文件包含了签名和证书  

当对OTA包签名后，recovery系统用update-binary把OTA包解压到/tmp目录  
update-binary命令格式：  
```bash
update-binary 3 stdout /sdcard/ota.zip
```
3是版本号，stdout是和recovery通信管道  
成功执行updater-script后，recovery系统会把执行日志拷贝到/cache/recovery目录，然后重启进入系统，
这就是OTA包更新安卓系统的过程。

## 实验环境

这个实验我们假设bootloader可以被解锁，预置的recovery系统可以被替换。由于替换系统非常复杂，目前我们
用的系统已经是一个定制化的recovery系统。实际上，我们用ubuntu 16.04当作是recovery系统，这个系统可以
执行任意命令。  
我们的这个步骤，除了替换recovery系统外，其他步骤都一样。  
这个安卓虚拟机基于userdebug源码编译的，并且很多后门已经被设置成用来获取root权限，这个实验不是用这些后门
来获取权限，而是用OTA机制来获取。

!!! 安卓编译选项

    安卓有三种编译选项，分别是eng、user、userdebug。eng是用于工程版本，user用于发行版本，userdebug
    是部分调试版本
    
## task1: 编译一个简单的OTA包

准备一个攻击脚本dummy.sh，让recovery系统启动时运行该脚本  
```bash
echo hello > /system/dummy
```

**1、写更新脚本**，update-binary这个文件可以是二进制可执行文件，也可以是脚本文件（由于安装了bash），
dummy.sh这个文件应放在/android目录下，因为安卓分区已经挂载到这个目录下了，安卓是建立在linux系统上的，
启动时，linux是先启动，启动过程用/system/etc/init.sh这个脚本，我们通过在init.sh中插入命令来启动dummy.sh，
由于我们是通过OTA方式修改文件，通过以下命令可实现这个目的：  
update-binary.sh文件内容：  
```bash
sed -i "/return 0/i /system/xbin/dummy.sh" /android/system/etc/init.sh
```
-i表示编译文件  
/return 0/ 表示找到return 0这行代码  
i 表示在找到的代码前插入  
/system/xbin/dummy.sh是插入的内容  
最后是编辑的文件  

**2、编译OTA包**，