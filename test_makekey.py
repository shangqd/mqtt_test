#!/usr/bin/python
# -*- coding: UTF-8 -*-

import time
import uuid
import requests
import json
import sys
from binascii import hexlify, unhexlify
import struct


json_addr = []
for num in range(1000):
    url = 'http://127.0.0.1:9902'
    data =  {
        "id":42,
        "method":"makekeypair",
        "jsonrpc":"2.0","params":{}
    }

    response = requests.post(url, json=data)
    res = json.loads(response.text)
    privkey = res["result"]["privkey"]
    pubkey = res["result"]["pubkey"]

    data = {
        "id":44,
        "method":"getpubkeyaddress",
        "jsonrpc":"2.0",
        "params":{"pubkey":pubkey}
    }

    response = requests.post(url, json=data)
    res = json.loads(response.text)

    obj = { "privkey" :privkey,
        "pubkey":pubkey,
        "address":res["result"]
    }
    json_addr.append(obj)

filename = 'addr.json'
with open(filename,'w') as file_obj:
    json.dump(json_addr,file_obj)