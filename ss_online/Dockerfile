FROM centos:7
# 作者
MAINTAINER txtxw
# 设置编码
ENV LANG zh_CN.UTF-8
# 同步时区
ENV TZ=Asia/Shanghai
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# 同步时间
RUN yum -y install ntp ntpdate && \
    ntpdate cn.pool.ntp.org

# 1. 安装基本依赖
RUN yum install epel-release -y && yum makecache && yum install wget unzip epel-release nginx xz gcc gcc-devel mysql-devel python-devel automake zlib-devel openssl-devel supervisor groupinstall development libxslt-devel libxml2-devel libcurl-devel git -y
#WORKDIR /var/www/

# 2. 准备python
#RUN wget http://mirrors.sohu.com/python/3.6.8/Python-3.6.8.tar.xz
#RUN xz -d Python-3.6.8.tar.xz && tar xvf Python-3.6.8.tar && cd Python-3.6.8 && ./configure && make && make install
# pyenv环境配置
RUN git clone https://github.com/pyenv/pyenv.git ~/.pyenv && \
    echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bash_profile && \
    echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bash_profile && \
    echo 'eval "$(pyenv init -)"' >> ~/.bash_profile

# 环境变量生效
RUN source ~/.bash_profile

# 使用pyenv配置python环境
RUN v=3.6.8 && \
    wget http://mirrors.sohu.com/python/$v/Python-$v.tar.xz -P $(pyenv root)/cache/ && \
    pyenv install $v && \
    pyenv global $v

# 3. 安装websdk
RUN pip install --upgrade pip -i https://mirrors.aliyun.com/pypi/simple/
RUN pip install --upgrade setuptools -i https://mirrors.aliyun.com/pypi/simple/
#RUN pip install -U git+https://github.com/ss1917/ops_sdk.git


# 4. 复制代码
RUN mkdir -p /var/www/
ADD . /var/www/

# 5. 安装pip依赖(生成不全，待解决)
RUN pip install -r /var/www/requirements.txt -i https://mirrors.aliyun.com/pypi/simple/

RUN pip install uwsgi -i https://mirrors.aliyun.com/pypi/simple/

# 6. 日志
VOLUME /var/log/

# 7. 准备文件
COPY nginx-app.conf /etc/nginx/conf.d/default.conf


EXPOSE 80

CMD ["/bin/bash","start.sh"]