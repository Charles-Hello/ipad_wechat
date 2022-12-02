
import os
# ----------非大佬一般不用动！👇🏻--------------#
# 获取ToKen的密码
ToKen_Password = "aa123456"

# 获取ToKen的api诺兰的密码
ToKen_Nolan_Password = "NolanWeChatApi"

# 获取ToKen的有效期默认为60分钟一次(改了不知道有没有效果，自己尝试哈哈哈哈)
ToKen_Expired = "60"

# Token刷新时间周期为(默认3600s一次)
Token_cycle = 3600

# 心跳检测时间周期(默认为20s一次)
Heartbeat_cycle = 20


# -----------非大佬一般不用动！👆🏻--------------#


# 选择是否开启网页扫码端口(默认选择端口为：30920，如需更换请自行修改端口)
'''
当QRCODE_PORT= None时，开启本地扫码，适合于Windows，MacOS系统操作系统
'''
QRCODE_PORT = int(os.getenv("QRCODE_PORT"))

# 选择是否开启邮箱接收(输入你的邮箱地址，邮箱默认为None(代表不发送，反之则一定执行邮箱发送图片)，例如1140***@qq.com, "防伪字符串")
'''
关于防伪字符串: 为了方便大家使用, 采用自带公开邮箱, 省去邮箱配置的麻烦.
                        所以收到登录邮件后, 一定要对比确认防伪字符串和你设置一致才可扫码登录, 否则将导致: 包括但不限于微信数据泄露.
'''

if bool(os.getenv("QRCODE_EMAIL")):
    QRCODE_EMAIL=os.getenv("QRCODE_EMAIL").split(',')
else:
    QRCODE_EMAIL = None

# 输入你微信代理地区地址和端口(决定你的微信登录的城市)[ps:关于内网的话，需要找个公网穿透出来除非本身就是公网。]
PROXY_IP_ADDRESS=str(os.getenv("PROXY_IP_ADDRESS"))
PROXY_IP_PORT = int(os.getenv("PROXY_IP_PORT"))



# 诺兰的swagger接口地址
NOLAN_URL = str(os.getenv("NOLAN_URL"))

# 输入你的回调（接管信息）地址
CALL_BACK_IP = str(os.getenv("CALL_BACK_IP"))

# 保存你的cookie的文件
Filename = "token.txt"

# # 是否开启报错debug分享（默认为ture）
# Debug_feedback = True
