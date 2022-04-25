# How to start NFTVerse
NFTVerse is a a platform useing NFT technology to protect intellectual property rights of digital works, do as givien follewed to start this project.

- [Web2](#Web2)
  - [Environment](#Environment)
  - [MySQL](#MySQL)
  - [Python Requirements](#Python Requirements)
- Web3
  - Ethereum
  - IPFS

## Web2

Follow these steps to prepare your local environment for NFTVerse development.

Run this command to get your project:

~~~
git clone https://github.com/roomdestroyer/NFTVerse
~~~



### Environment

Linux environment

- gcc version 9.3.0 (Ubuntu 9.3.0-17ubuntu1~20.04)
- Python 3.8.10
- pip 22.0.4
- mysql  Ver 8.0.28-0ubuntu0.20.04.3 for Linux on x86_64 ((Ubuntu))

This environment has been verified, it might need some extra efforts to run this project under other environment. 



### MySQL

#### Download and Config root account

We'll demonstrate the download and config steps from scratch to make you run this successfully as soon as possible.

First, uninstall mysql in your environment, to make sure that we'll get a pure environment, only if you're not using MySQL. 

```bash
sudo apt-get remove mysql-common
sudo apt-get autoremove --purge mysql-*
dpkg -l|grep ^rc|awk '{print$2}'|sudo xargs dpkg -P
sudo rm -rf /etc/mysql/ /var/lib/mysql
sudo apt autoclean
```

Then, run this command to check if there exists some dependencies in your Linux:

~~~
dpkg --list|grep mysql
~~~

There shouldn't be any dependencies now, if acctually exists, remove them one-by-one. Now, install MySQL:

~~~
sudo apt-get install mysql-server
~~~

Change your root account and password:

~~~
sudo cat /etc/mysql/debian.cnf
~~~

It will looks like this:

![image-20220426000550286](https://s2.loli.net/2022/04/26/rVJanHcxizuQZP3.png)

Copy the `user` line and `password` line, and run this command:

~~~
mysql -udebian-sys-maint -pzaHnqj98xThqT3SI
~~~

This allows you to login in MySQL from system account.

Run commands as following, you'll actually change your root account password finally:

~~~
mysql> use mysql;         
mysql> ALTER USER 'root'@'%' IDENTIFIED WITH mysql_native_password BY '***';   
mysql> flush privileges;
~~~

And now see your account:

~~~
mysql> select host, user, authentication_string, plugin from mysql.user;
~~~

You can login MySQL with root account if it looks like this:

![image-20220426000955763](https://s2.loli.net/2022/04/26/D4Hh78wiYmFruoc.png)



#### Setting up remote Connections

Now you can login with root account, run commands as following:

~~~
mysql> use mysql;
mysql> grant all privileges on *.* to 'root'@'%';
mysql> flush privileges;
mysql> quit;
~~~

Then, remove local connection restrictions:

~~~
sudo vim /etc/mysql/mysql.conf.d/mysqld.cnf
~~~

Find the `bind-address = 127.0.0.1` line, and comment out it:

~~~
# bind-address          = 127.0.0.1
~~~

Save your changes, exit and restart mysql:

~~~
sudo service mysql restart
~~~

Now, your MySQL environment has been configged.



## Python Requirements

