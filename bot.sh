#!/bin/sh

dir=$(pwd)
door=$dir
file=docker-compose.yml
project=ipad_wechat
docker_yml=$door/$project/$file


_echo(){
    case $1 in
    -u|upon)
        echo
        echo -e "${2}"
        ;;
    -d|down)
        echo -e "${2}"
        echo
        ;;
    -r|red)
        echo
        echo -e "${Red}${2}${suffix}"
        echo
        ;;
    -g|green)
        echo
        echo -e "${Green}${2}${suffix}"
        echo
        ;;
    -i|info)
        echo -e "${Info} ${2}"
        ;;
    -e|error)
        echo -e "${Error} ${2}"
        ;;
    -t|tip)
        echo
        echo -e "${Tip} ${2}"
        echo
        ;;
    -w|warning)
        echo -e "${Warning} ${2}"
        ;;
    *)
        echo
        echo -e "${1}"
        echo
        ;;
    esac
}

check_port_occupy(){
    local port=$1

    if [ ! "$(command -v lsof)" ]; then
        package_install "lsof" > /dev/null 2>&1
    fi
    if [ `lsof -i:"${port}" | grep -v google_ | grep -v COMMAND | wc -l` -ne 0 ];then
        # Occupied
        return 0
    else
        # Unoccupied
        return 1
    fi
}

_read(){
    case $1 in
    -u|upon)
        echo
        read -e -p "${2}" inputInfo
        ;;
    -d|down)
        read -e -p "${2}" inputInfo
        echo
        ;;
    *)
        echo
        read -e -p "${1}" inputInfo
        echo
        ;;
    esac
}



check_git_file(){
  if [ ! -d "$project" ]; then
  _read "检测到ipad_wechat文件不存在，是否需要拉取！(默认: y) [y/n]:"
  local k="${inputInfo}"
  [ -z "${k}" ] && k="N"
  case "${k:0:1}" in
      y|Y)
          _echo -g "正在为你拉取!"
          git clone https://github.com/Charles-Hello/ipad_wechat.git
          ;;
      n|N)
          _echo -e "取消拉取最新库!"
          ;;
      *)
          _echo -e "输入有误，请重新输入!"
          ;;
  esac
else
  _read "检测到ipad_wechat文件已存在，是否还需要拉取更新最新版本(默认: n) [y/n]: "
  local get_input="${inputInfo}"
  [ -z "${get_input}" ] && get_input="N"
  case "${get_input:0:1}" in
      y|Y)
          _echo -g "正在为你拉取最新最新库"
          rm -rf ipad_wechat
          git clone https://github.com/Charles-Hello/ipad_wechat.git
          ;;
      n|N)
          _echo -e "取消拉取最新库"
          ;;
      *)
          _echo -e "输入有误，请重新输入!"
          ;;
  esac
fi
}

dispose(){
  # check_git_file
#   _echo  "正在检查${install_service}状态!"
#   init_check 6379
  content=$(sed -n "47p" "$docker_yml")
  result=$(echo $content | grep "121212")
  if [[ $result != "" ]]; then
    _echo -g  "$file没有改动,请你改动一下。"
    sleep 1
    _echo -g  "$file修改完了之后，直接再次运行一键命令即可"
    sleep 3
    vi "$docker_yml"
  fi
  content=$(sed -n "4p" "$door/$project/tg_bot/bot.json")
  result=$(echo "$content" | grep "1123121218")
  if [[ $result != "" ]]; then
      _read "是否需要安装tgbot控制(默认: n) [y/n]: "
  local get_input="${inputInfo}"
  [ -z "${get_input}" ] && get_input="N"
  case "${get_input:0:1}" in
      y|Y)
          _echo -g "请填写bot.json对应的内容"
          sleep 3
          vi "$door/$project/tg_bot/bot.json"
          ;;
      n|N)
          _echo -e "取消"
          ;;
      *)
          _echo -e "输入有误，请重新输入!"
          ;;
  esac
    vi "$door/$project/tg_bot/bot.json"
  else
    _echo -g  "检测到已经改动$door/$project/tg_bot/bot.json内容"
  fi

  cd "$door"/$project || exit
  _echo -g  "开始搭建$project"
  # # chmod +x docker-entrypoint.sh
  docker-compose up -d
  docker-compose logs #以后写check
  echo ""
  _echo -g  "$project已搭建完成！"
  echo ""
  # # docker exec -it $project bash tail -f wechat.log
  _echo -g "如需卸载请前往ipad_wechat文件夹使用docker-compose down即可"
  _echo -g "如需查看log请前往ipad_wechat文件夹使用docker-compose logs"
  # _echo -g  "docker exec -it $project bash "
  # _echo -g "如果需要开启tg_bot请自行修改$door/$project/tg_bot/bot.json文件(否则忽略这句话，直接执行以下代码即可)"
  # _echo -g  "nohup  python3 -m $project  > wechat.log  2>&1 &"
  # _echo -g "tail -f wechat.log"

}




init_check(){
  local time=3
  local port=6379
if ! check_port_occupy "${port}"; then
  _echo -g "${port}$install_service默认端口没有被占用"
  echo "速度决定！！！你还有${time}秒钟考虑，如果决定放弃，按CTRL+C。继续则帮你安装$install_service"
  sleep ${time}
  _read "请输入你想要安装$install_service的端口: "
  local _port_="${inputInfo}"
  redis 6379
else
  _read "检测到$install_service默认${port}端口被占用，是否还需要安装$install_service(默认: n) [y/n]: "
  local yn="${inputInfo}"
  _echo -g "占用${port}端口的进程信息如下: "
  lsof -i:"${port}"
  [ -z "${yn}" ] && yn="N"
  case "${yn:0:1}" in
      y|Y)
          _read "请输入你想要安装$install_service的端口: "
          local _port="${inputInfo}"
          sleep 1
          _echo -g "正在为你安装$install_service!"
          redis _port
          ;;
      n|N)
          _echo -e "端口${port}被占用，可能存在$install_service服务"
          _echo -e "如已安装，请自行修改$door/$project/NolanChat/Config/Redis.json中的内容"
          ;;
      *)
          _echo -e "输入有误，请重新输入!"
          ;;
  esac
fi

}




main() {
  local name="bot"
    cat << EOF
██╗██████╗  █████╗ ██████╗       ██╗    ██╗███████╗ ██████╗██╗  ██╗ █████╗ ████████╗
██║██╔══██╗██╔══██╗██╔══██╗      ██║    ██║██╔════╝██╔════╝██║  ██║██╔══██╗╚══██╔══╝
██║██████╔╝███████║██║  ██║█████╗██║ █╗ ██║█████╗  ██║     ███████║███████║   ██║
██║██╔═══╝ ██╔══██║██║  ██║╚════╝██║███╗██║██╔══╝  ██║     ██╔══██║██╔══██║   ██║
██║██║     ██║  ██║██████╔╝      ╚███╔███╔╝███████╗╚██████╗██║  ██║██║  ██║   ██║
╚═╝╚═╝     ╚═╝  ╚═╝╚═════╝        ╚══╝╚══╝ ╚══════╝ ╚═════╝╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝
EOF
    echo "请选择您需要进行的操作:"
    echo "  1) 安装ipad_wechat(中间件)"
    echo "  2) 退出脚本"
    echo ""
    echo -n "请输入编号: "
    read N
    case $N in
      1) dispose ;;
      2) exit ;;
      *) echo "输入错误！请重新 bash ${name}.sh 启动脚本" ;;
    esac
}
main
