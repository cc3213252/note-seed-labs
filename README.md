# 网络安全Seed-labs实验

http://note.blueegg.net.cn/seed-labs  

[B站专栏视频](https://space.bilibili.com/622705305/channel/detail?cid=174341)

## 打包发布

```bash
mkdocs build
fab dev_upload
```

## 安装32位ubuntu系统

```bash
wget https://cloud-images.ubuntu.com/vagrant/trusty/20191107/trusty-server-cloudimg-i386-vagrant-disk1.box
vagrant box add ubuntu14.04-i386 trusty-server-cloudimg-i386-vagrant-disk1.box
```

## 脏牛漏洞用ubuntu 12.04系统

```bash
wget https://cloud-images.ubuntu.com/vagrant/precise/20170502/precise-server-cloudimg-i386-vagrant-disk1.box --no-check-certificate
vagrant box add ubuntu12.04-i386 precise-server-cloudimg-i386-vagrant-disk1.box
```