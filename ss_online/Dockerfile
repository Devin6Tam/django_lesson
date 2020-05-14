FROM python_uwsgi:3.6.8

# 拷贝项目
RUN mkdir -p /var/www/
ADD . /var/www/

# 工作目录
WORKDIR /var/www/

# 其他非公共库的依赖包
COPY DjangoUeditor.tar /root/.pyenv/versions/3.6.8/lib/python3.6/site-packages

# 执行文件
RUN sed -i 's/\r//' start.sh

EXPOSE 8000

CMD ["/bin/bash"]