

import re
import urllib.request
import logging
import os

os.chdir(os.getcwd()+"/"+__file__.split('/')[-2])
def Ping_Add_server(Call_Back_IP:str):
    opener = urllib.request.build_opener()
    opener.addheaders = [('User-agent', 'Mozilla/49.0.2')]
    print('开始检查回调地址：')
    try:
        opener.open(Call_Back_IP)
        logging.info(Call_Back_IP + '托管没问题')
    except :
        logging.error(Call_Back_IP + '托管地址访问出错，请检查状态，请及时更正！')

def getsize(filename:str)->int:
    with open(filename, 'r') as f1:
        i = f1.read()
        BE_guid = re.findall("你的guid=\"(.*)\"", i)[0]
    if BE_guid == "":
        logging.info('无登陆状态')
        return 0
    else:
        logging.error('guid不是空的，则用该设备作为以后登录凭证')
        return 1

def get_guid_id(filename:str)->str:
    with open(filename,'r') as f1:
        i = f1.read()
        BE_guid = re.findall("你的guid=\"(.*)\"", i)[0]
        return BE_guid

def get_authorization_id(filename:str)->str:
    with open(filename,'r') as f1:
        i = f1.read()
        BE_Authorization = re.findall("你的Authorization=\"(.*)\"", i)[0]
        return BE_Authorization


def sub_file_value(filename:str,method:str,value:str):
    with open(filename, 'r') as f1:
        a = f1.read()
    BE_guid = re.findall("你的guid=\"(.*)\"", a)[0]
    # print("BE_guid：" )
    BE_Authorization = re.findall("你的Authorization=\"(.*)\"", a)[0]
    # print("BE_Authorization：" + BE_Authorization)
    if method == "guid" and BE_guid !="":
        a = a.replace(BE_guid, value)
    elif method == "guid" and BE_guid =="":
        a = a.replace("你的guid=\"\"", "你的guid=\""+value+"\"")
    elif method != "guid" and BE_Authorization != "":
        a = a.replace(BE_Authorization, value)
    elif method != "guid" and BE_Authorization == "":
        a = a.replace("你的Authorization=\"\"", "你的Authorization=\""+value+"\"")

    with open(filename, 'w') as f1:
        f1.write(a)



