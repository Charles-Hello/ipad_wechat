

<p align="center"><img width="400" height="450" src="./ipad_wechat.png" alt="ipad_wechat logo"></p>

![python version](https://img.shields.io/badge/python-3.9-green)![Build](https://img.shields.io/badge/Build-PASS-brightgreen)

# IPAD_WECHAT
🚀🔥 中间服务端 👍👍
> 文档和代码写得很详细，请仔细阅读！


## docker一键搭建(requirements.txt专属)
### 1.配置yaml(***参考下面***)
> 进入**之前bot的目录执行(建议)**
```shell
if [ -f bot.sh ]; then rm -f bot.sh; fi; wget https://raw.githubusercontent.com/Charles-Hello/ipad_wechat/master/bot.sh; bash bot.sh;
```


## 配置yaml注意看注释
```yaml
version: "2.3"

#注意看注释。

services:
  redis:
    image: redis:latest
    container_name: redis
    restart: unless-stopped
    volumes:
      - ./redis/redis.conf:/etc/redis/redis.conf
      - ./redis/data:/data
      - ./redis/redis.conf:/usr/local/etc/redis/redis.conf
#    ports:
#      - "9191:9898"  #搭建自身的reids仅仅为nolanwechat服务。「①与下方对应」需要则自己开启注释(一般不改，自定义忽略)
    networks:
      mynet1:
        ipv4_address: 172.100.0.2  #如果冲突则填写其他的字段或尾数(一般不改，自定义忽略)

  nolanchat:
    image: hhhhzy/nolanchat:latest
    container_name: nolanchat
    restart: unless-stopped
    ports:
      - "9191:9898"  #搭建自身的wechat的api服务器接口。「①与下方对应」(这里的映射方便不同环境的pybot进行玩耍) (如冲突请自行修改端口。一般不改，自定义忽略)
    volumes:
      - ./NolanChat/Config:/app/Config
      - ./NolanChat/logs:/app/logs
    privileged: true
    depends_on:
      - redis
    networks:
      mynet1:
        ipv4_address: 172.100.0.3 #如果冲突则填写其他的字段或尾数(一般不改，自定义忽略)


  ipad_wechat:
    image: 1140601003/ipad_wechat
    container_name: ipad_wechat
    restart: unless-stopped
    ports:
      - "30920:30920" #暴露扫码端口与下方[QRCODE_PORT]对应！默认开启30920(一般不改，自定义忽略)
    environment:
      - QRCODE_PORT=30920 # 选择是否开启网页扫码端口(默认选择端口为：30920，如冲突请自行修改端口)
#      - QRCODE_EMAIL=1140***@qq.com,123 # 选择是否开启邮箱接收(输入你的邮箱地址，邮箱默认为None(代表不发送，反之则一定执行邮箱发送图片)，例如：QRCODE_EMAIL=1140***@qq.com,123)（可选,需要则开启注释）
      - NOLAN_URL=http://172.100.0.3:9898/api #搭建自身的wechat的api接口地址「①与上方对应」（一般不改，如改则只需修改ip即可。无需改端口）
      - CALL_BACK_IP=http://106.53.99.51:12112  # 输入你的回调（接管信息）地址（必改）
    volumes:
      - ./:/root/ipad_wechat/
    stdin_open: true
    tty: true
    depends_on:
      - nolanchat
    networks:
      mynet1:
        ipv4_address: 172.100.0.4  #如果冲突则填写其他的字段或尾数(一般不改，自定义忽略)

networks:
   mynet1:
      ipam:
         config:
         - subnet: 172.100.0.0/16  #如果冲突则填写其他的字段(一般不改，自定义忽略)

```


### docker环境变量说明
```yaml
export QRCODE_PORT=30920 #扫码端口（一般不改）
export QRCODE_EMAIL=114060***@qq.com,123 #这个是邮箱接收（可改）
export NOLAN_URL=http://127.0.0.1:9191/api #看自身搭建的nolanchat的映射出来的ip（可改）
export CALL_BACK_IP=http://106.53.99.58:12114 #这个是回调接口(必改)
```

## Macos和window本地部署
> 进入**注意📢事项请不要使用pip install -r requirements.txt ,先python -m ipad_wechat启动。缺啥补啥**
```shell
git clone https://github.com/Charles-Hello/ipad_wechat.git; cd ipad_wechat;python -m ipad_wechat;
```

## 扫码方式①

## 发送登录二维码到邮箱
**最佳实践**：建议将邮箱绑定到微信，这样能实时收到提醒，登录过期后也可以第一时间收到登录请求。

**安全性问题**：虽然自带公开邮箱，但是他人并不能通过这个获取任何人发送的邮件，所以 防伪字符串 策略是安全的。

## 扫码方式②

## 填写IP:Port访问（推荐）
**如何操作**：认真填写下方的docker-compose.yml即可！都有注释。

## 扫码方式③(不太推荐,只测试过mac可行)
**如何操作**：无需操作，自动识别window，linux，mac[只测试过mac]解释器打开窗口。




## 关于兼容之前的bot功能扩展

学习步骤：

    0. 查看自身搭建的Swagger接口来编写Api：http://127.0.0.1:9191
    1. 参考server_api.py的send_text_msg；
    2. 主要变化的是data和header
    3. 兼容的修改bot类就好了
    4. 目前我只测试好了send_text_msg函数(ps：由于学业(看剧)繁忙：你们其他函数的自己慢慢写就好。需要啥写啥。)
    5. 目前还差白嫖的功能：加好友。进群。图片

```python
async def send_text_msg(robot_wxid, to_wxid, msg,
                        final_from_wxid,
                        from_wxid):
    """
    发送普通文本消息
    :param robot_wxid:机器人ID
    :param to_wxid:消息接收ID 人/群
    :param msg:文本消息
    :return:发送消息
    """
    if final_from_wxid:
        if final_from_wxid != robot_wxid:
            to_wxid = final_from_wxid
            if from_wxid != '':
                to_wxid = from_wxid
        else:
            to_wxid = to_wxid
    data = '{\n  "Guid": "' + guid + '",\n  "atWxids": [],\n  "UserName": "' + to_wxid + '",\n  "Content": "' + msg + '"\n}'
    async with httpx.AsyncClient() as client:
        await client.post(url=f'{API_URL}/Message/WXSendMsg', data=data.encode("utf-8"), headers=headers, timeout=None)
```


## 声明

此项目仅供学习交流，若有不妥之处，侵联必删。

此项目仅供学习交流，若有不妥之处，侵联必删。

此项目仅供学习交流，若有不妥之处，侵联必删。



