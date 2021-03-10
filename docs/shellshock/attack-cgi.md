# 攻击CGI程序

## apache环境搭建

```bash
sudo apt install apache2
sudo ln -s /etc/apache2/mods-available/cgid.conf /etc/apache2/mods-enabled/cgid.conf
sudo ln -s /etc/apache2/mods-available/cgid.load /etc/apache2/mods-enabled/cgid.load
sudo ln -s /etc/apache2/mods-available/cgi.load /etc/apache2/mods-enabled/cgi.load
sudo /etc/init.d/apache2 restart
```

```bash
sudo vi /var/www/html/test.cgi
```

```bash
#!/bin/bash

echo "Content-type: text/plain"
echo 
echo
echo "Hello World"
```

```bash
sudo chmod 755 test.cgi
```

http://192.168.0.11/cgi-bin/test.cgi