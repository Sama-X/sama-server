FROM python:3.11

LABEL tag="sama"
LABEL version="0.0.1"
# 设置python 环境变量
ENV PYTHONUNBUFFERED 1

# 设置容器时间，有的容器时区与我们的时区不同，可能会带来麻烦
RUN cp /usr/share/zoneinfo/Asia/Shanghai /etc/localtime && echo 'Asia/Shanghai' >/etc/timezone 

# 设置语言为utf-8
ENV LANG C.UTF-8

ARG work=/app/data
WORKDIR ${work}
# 拷贝当前文件代码到工作目录
COPY . ${work}
# 设置工作目录，也就是下面执行 ENTRYPOINT 后面命令的路径
RUN chmod +x ${work}/docker/deploy/*
# 根据requirement.txt下载好依赖包
RUN /usr/local/bin/pip3 install -i http://mirrors.aliyun.com/pypi/simple/ --trusted mirrors.aliyun.com -r requirements.txt

EXPOSE 8003
