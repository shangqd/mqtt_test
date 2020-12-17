#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import time
import uuid
import requests
import json
import sys
from binascii import hexlify, unhexlify
import struct
import hashlib

url = 'http://127.0.0.1:9902'

str_ = '币的社区治理功能将会从800高度开始，1000高度结束，开始进行该功能的治理．'.encode('utf-8')

s = hashlib.sha256()
s.update(str_)
b = s.hexdigest()

data_json = {
    "id":1,
    "method":"getpubkeyaddress",
    "jsonrpc":"2.0",
    "params": {
        "pubkey":s.hexdigest()
    }
}

response = requests.post(url, json=data_json)
res = json.loads(response.text)

data_json = {
    "id":1,
    "method":"addnewtemplate",
    "jsonrpc":"2.0",
    "params":{
        "type":"dexbbcmap",
        "dexbbcmap":{
            "owner":res["result"]
            }
        }
    }
response = requests.post(url, json=data_json)
res = json.loads(response.text)
print("投票地址",res["result"])

str_16 = hexlify(str_)
str_time = hexlify(struct.pack("<I", int(time.time())))
data = uuid.uuid1().hex.encode() + str_time + b"00" + str_16

data_json = {
    "id":1,
    "method":"sendfrom",
    "jsonrpc":"2.0",
    "params":{
        "from":"1965p604xzdrffvg90ax9bk0q3xyqn5zz2vc9zpbe3wdswzazj7d144mm",
        "to":res["result"],
        "amount":100.00000000,
        "data":data.decode('utf-8')
        }
    }
response = requests.post(url, json=data_json)
res = json.loads(response.text)
data_json = {
    "id":1,
    "method":"gettransaction",
    "jsonrpc":"2.0",
    "params":{
        "txid":res["result"]
        }
    }
response = requests.post(url, json=data_json)
res = json.loads(response.text)
data_str = res["result"]["transaction"]["data"]

print("uuid", data_str[0:8] + "-" + data_str[8:12] + "-" + data_str[12:16] + "-" + data_str[16:20] + "-" + data_str[20:32])
v = struct.unpack("<I", unhexlify(data_str[32:40]))
timeArray = time.localtime(v[0])
otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
print("时间:", otherStyleTime)
print("立项内容:", unhexlify(data_str[42:]).decode('utf-8'))