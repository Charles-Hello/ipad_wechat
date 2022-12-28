#!/bin/bash
dir_root=/root
project=ipad_wechat
cd $dir_root || exit
nohup  python3 -m $project  > wechat.log  2>&1 &
tail -f $dir_root/wechat.log
exec "$@"
