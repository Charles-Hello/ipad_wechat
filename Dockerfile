FROM python:3.9-alpine
MAINTAINER Miao
ADD ./ /root/ipad_wechat
WORKDIR /root
EXPOSE 22 30920
ENV DEBIAN_FRONTEND teletype
ARG DEBIAN_FRONTEND=noninteractive
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US.UTF-8
ENV LC_ALL en_US.UTF-8
ENV BOTTLE_VER 0.12.18
RUN set -x \
    && sed -i 's/dl-cdn.alpinelinux.org/mirrors.aliyun.com/g' /etc/apk/repositories \
    && apk update -f \
    && apk upgrade \
    && apk --no-cache add -f bash \
                             coreutils \
                             moreutils \
                             git \
                             curl \
                             wget \
                             tzdata \
                             perl \
                             openssl \
                             nginx \
                             nodejs \
                             jq \
                             openssh \
                             npm \apt-utils\
                            libgl1-mesa-glx \
                            libglib2.0-dev\
    && rm -rf /var/cache/apk/* \
    && apk update \
    && ln -sf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime \
    && echo "Asia/Shanghai" > /etc/timezone \
    && pip3 config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple\
    && cd ipad_wechat && pip install -r requirements.txt && cd ..\