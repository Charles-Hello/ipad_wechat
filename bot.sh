#!/bin/
dir=`pwd`
door=$dir
file=docker-compose.yml
project=ipad_wechat
docker_yml=$door/$project/$file
if [ ! -d "/$project" ]; then
  git clone https://github.com/Charles-Hello/ipad_wechat.git
fi
content=`sed -n "25p" $docker_yml`
result=$(echo $content | grep "106.53.99.58")
if [[ $result != "" ]]; then
  echo -e  "$file没有改动"
  vi $docker_yml
else
  echo -e  "检测到已经改动$file内容"
  cd $door/$project
  docker-compose up -d
fi