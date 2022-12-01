FROM fnndsc/ubuntu-python3
MAINTAINER Miao
ADD ./ /root/ipad_wechat
WORKDIR /root
EXPOSE 22 30920
ENV DEBIAN_FRONTEND teletype
ARG DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y --no-install-recommends apt-utils && apt-get -y install libgl1-mesa-glx
RUN apt-get install -y libglib2.0-dev
RUN pip3 config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
RUN cd ipad_wechat && pip install -r requirements.txt && cd ..
#RUN python3 -m ipad_wechat