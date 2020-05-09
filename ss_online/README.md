# 环境准备：

```
使用pip导出第三方依赖
pip freeze > requirements.txt
使用pip基于requirements.txt中依赖版本安装
pip install -r requirements.txt
```
```
生成数据库迁移文件
python manage.py makemigrations
运行migrate命令，创建数据库和数据表
python manage.py migrate

注：数据库相关操作，可以使用navicat传输生产环境或手动导出基础数据库并执行到生成环境；
后期的数据表结构变更，可以进行增量执行
```
```
准备linux、ubuntu服务器,安装依赖库
yum install openssl-devel bzip2-devel expat-devel gdbm-devel readline-devel sqlite-devel gcc gcc-c++  openssl-devel libffi-devel python-devel mariadb-devel
sudo apt-get install zlib1g-dev libbz2-dev libssl-dev libncurses5-dev libmysqlclient-dev libsqlite3-dev libreadline-dev tk-dev libgdbm-dev libdb-dev libpcap-dev xz-utils libexpat1-dev liblzma-dev libffi-dev libc6-dev
```

# 环境部署

## 单体服务部署

```
安装python 3.6.8
wget http://mirrors.sohu.com/python/3.6.8/Python-3.6.8.tgz
tar -xzvf Python-3.6.8.tgz -C  /tmp
cd /tmp/Python-3.6.8/

./configure --prefix=/usr/local
make
make altinstall

```
```
安装虚拟环境

yum install python-setuptools python-devel
pip install virtualenvwrapper
编辑.bashrc文件
export WORKON_HOME=$HOME/.virtualenvs
source /usr/local/bin/virtualenvwrapper.sh
重新加载.bashrc文件
source  ~/.bashrc

新建虚拟环境
mkvirtualenv ssonline

进入虚拟环境 
workon ssonline

安装依赖包
pip install -r requirements.txt
```
```
安装uwsgi

pip install uwsgi
```
```
安装nginx
sudo yum install epel-release
sudo yum install nginx
sudo systemctl start nginx
```
```
测试
uwsgi --http :8000 --module ssonline.wsgi
运行项目
uwsgi uwsgi.ini
停止项目
uwsgi --stop uwsgi.pid
杀掉进程
pkill -f uwsgi -9 
```

## 分布式服务部署（镜像版）

```
构建镜像
docker build -t ss_online:v1 .

docker run -itd -p 3031:3031 -p 80:80 ss_online:v1
```