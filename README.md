

<p align="center"><img width="400" height="450" src="./ipad_wechat.png" alt="ipad_wechat logo"></p>

![python version](https://img.shields.io/badge/python-3.9-green)![Build](https://img.shields.io/badge/Build-PASS-brightgreen)

# IPAD_WECHAT &#x1F308;
🚀🔥 中间服务端 👍👍
> 文档和代码写得很详细，请仔细阅读！


## Docker一键搭建  &#x1F31F;
### 1.配置yaml(***参考下面***) &#x1F33A;

```shell
if [ -f bot.sh ]; then rm -f bot.sh; fi; wget https://raw.githubusercontent.com/Charles-Hello/ipad_wechat/master/bot.sh; bash bot.sh;
```


## 配置yaml注意看注释 &#x1F6A8;
```yaml
version: "2.3"

#注意看注释。

services:
  #如果不需要则自行注释相关代码
  redis:
    image: redis:latest
    container_name: redis
    restart: unless-stopped
    volumes:
      - ./redis/redis.conf:/etc/redis/redis.conf
      - ./redis/data:/data
      - ./redis/redis.conf:/usr/local/etc/redis/redis.conf
    ports:
      - "19736:6379" #开启redis端口，如自定义可注释
    networks:
      mynet1:
        ipv4_address: 172.100.0.2 #如果冲突则填写其他的字段或尾数(一般不改，自定义请注释)

  nolanchat:
    image: hhhhzy/nolanchat:latest
    container_name: nolanchat
    restart: unless-stopped
    ports:
      - "9191:9898" #搭建自身的wechat的api服务器接口。「①与下方对应」(这里的映射方便不同环境的py_bot进行玩耍) (如冲突请自行修改端口。一般不改，自定义请注释)
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
      - QRCODE_EMAIL=false,false # 选择是否开启邮箱接收(输入你的邮箱地址，邮箱默认为false(代表不发送，反之则一定执行邮箱发送图片)，例如：QRCODE_EMAIL=1140301003@qq.com,123)（可选,需要则修改false）
      - NOLAN_URL=http://172.100.0.3:9898/api #搭建自身的wechat的api接口地址「①与上方对应」（一般不改，如改则只需修改ip即可。无需改端口）
      - CALL_BACK_IP=http://1212.53.99.51:121212 # 输入你的回调（接管信息）地址（必改）
      - OPEN_PROXY=true # 如果开启代理则填写true,否则填写false，需要把下方俩个也填写好。下方俩个也要填写正确。如果填写false，下面俩个PROXY忽略无视就好
      - PROXY_IP_ADDRESS=213.53.99.58 # 输入你微信代理地区地址和端口(决定你的微信登录的城市)[ps:关于内网的话，需要找个公网穿透出来除非本身就是公网。]（必改）(代理为true时则填写)
      - PROXY_IP_PORT=12121 #本地代理端口（必改）(代理为true时则填写)
      - TGBOT=true #是否启动tgbot控制(为true时则启动，否则则为false)
      #这里是自定义redis配置
      # - REDIS_IP=127.0.0.1 #redis的ip地址(仅为自定义使用，如果需要则关闭注释，默认忽略)
      # - REDIS_PROT=6379 #redis的端口(仅为自定义使用，如果需要则关闭注释，默认忽略)
      # - REDIS_PASS=123456 #redis的密码(仅为自定义使用，如果需要则关闭注释，默认忽略)
    volumes:
      - ./:/root/ipad_wechat/
    stdin_open: true
    tty: true
    depends_on:
      - nolanchat
    networks:
      mynet1:
        ipv4_address: 172.100.0.4 #如果冲突则填写其他的字段或尾数(一般不改，自定义忽略)

networks:
  mynet1:
    ipam:
      config:
        - subnet: 172.100.0.0/16 #如果冲突则填写其他的字段(一般不改，自定义忽略)

```


### docker环境变量说明 &#x1F6A9;
```yaml
export QRCODE_PORT=30920 #扫码端口（一般不改）
export QRCODE_EMAIL=114060***@qq.com,123 #这个是邮箱接收（可改）
export NOLAN_URL=http://127.0.0.1:9191/api #看自身搭建的nolanchat的映射出来的ip（可改）
export CALL_BACK_IP=http://106.53.99.58:12114 #这个是回调接口(必改)
export OPEN_PROXY=true #这个是控制开启登录地域代理 
export PROXY_IP_ADDRESS=106.53.99.58 #登录地域代理的ip
export PROXY_IP_PORT=18838  #登录地域代理的端口
export TGBOT=true #是否开启tgbot
export REDIS_IP=127.0.0.1 #redis的ip地址
export REDIS_PROT=6379 #redis的端口
export REDIS_PASS=123456 #redis的密码
```

## Macos和window本地部署 
> 进入**注意📢事项请不要使用pip install -r requirements.txt ,先python -m ipad_wechat启动。缺啥补啥**
```shell
git clone https://github.com/Charles-Hello/ipad_wechat.git; cd ipad_wechat;python -m ipad_wechat;
```
<br>

### 邮箱扫码

>### 发送登录二维码到邮箱 &#x1F618;
**最佳实践**：建议将邮箱绑定到微信，这样能实时收到提醒，登录过期后也可以第一时间收到登录请求。

**安全性问题**：虽然自带公开邮箱，但是他人并不能通过这个获取任何人发送的邮件，所以 防伪字符串 策略是安全的。
<br>
<br>
### 网页扫码

>### 填写IP:Port访问（推荐）&#x1F60D;
**如何操作**：认真填写下方的docker-compose.yml即可！都有注释。
<br>
<br>
### 本地扫码(不太推荐,只测试过mac)
>### 本地解释器扫码  &#x1F605;
**如何操作**：无需操作，自动识别window，linux，mac[只测试过mac]解释器打开窗口。
<br>
<br>
### TG机器人扫码

>### tg_bot扫码（推荐）&#x1F603;
**如何操作**：认真填写下方的docker-compose.yml和修改bot.json即可！都有注释。

<br>
<br>

## 关于兼容之前的bot功能扩展 &#x1F633;

学习步骤：

    0. 查看自身搭建的Swagger接口来编写Api：http://127.0.0.1:9191
    1. 参考server_api.py的send_text_msg；
    2. 主要变化的是data和header
    3. 兼容的修改bot类就好了
    4. 目前我只测试好了send_text_msg函数(ps：由于学业(看剧)繁忙：你们其他函数的自己慢慢写就好。需要啥写啥。)
    5. 目前还差白嫖的功能：加好友。进群。图片

<br>

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



