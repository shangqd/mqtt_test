#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import time
import uuid
import requests
import json
import sys
from binascii import hexlify, unhexlify
import struct

url = 'http://127.0.0.1:9902'
filename = 'test_addr510.json'
with open(filename)as fp:
    json_data = json.load(fp)
    for obj in json_data:
        data = {
            "id":4,
            "method":"sendfrom",
            "jsonrpc":"2.0",
            "params":{
                "from":"1965p604xzdrffvg90ax9bk0q3xyqn5zz2vc9zpbe3wdswzazj7d144mm",
                "to":obj["address"],
                "amount":100000.00
            }
        }
        response = requests.post(url, json=data)
        res = json.loads(response.text)
        txid = res["result"]
        print(txid)