#!/usr/bin/python
# -*- coding: UTF-8 -*-

import time
import uuid
import requests
import json
import sys
from binascii import hexlify, unhexlify
import struct

str_ = b'hello abc'
str_16 = hexlify(str_)
str_time = hexlify(struct.pack("<I", int(time.time())))
str_uuid = str(uuid.uuid1()).replace('-','')
data = str_uuid + str_time + "00" + str_16

url = 'http://127.0.0.1:9902'
data = '{"id":1,"method":"sendfrom","jsonrpc":"2.0","params":{"from":"1965p604xzdrffvg90ax9bk0q3xyqn5zz2vc9zpbe3wdswzazj7d144mm","to":"1965p604xzdrffvg90ax9bk0q3xyqn5zz2vc9zpbe3wdswzazj7d144mm","amount":100.00000000,"data":"%s"}}' % data
response = requests.post(url, data=data)
res = json.loads(response.text)
txid = res["result"]
data = '{"id":1,"method":"gettransaction","jsonrpc":"2.0","params":{"txid":"%s"}}' % txid
response = requests.post(url, data=data)
res = json.loads(response.text)
data_str = res["result"]["transaction"]["data"]

print("uuid1", data_str[0:8] + "-" + data_str[8:12] + "-" + data_str[12:16] + "-" + data_str[16:20] + "-" + data_str[20:32])
v = struct.unpack("<I", unhexlify(data_str[32:40]))
timeArray = time.localtime(v[0])
otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
print("时间:", otherStyleTime)
print("内容:", unhexlify(data_str[42:]))