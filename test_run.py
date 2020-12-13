#!/usr/bin/python
# -*- coding: UTF-8 -*-

import time
import uuid
import requests
import json
import sys
from binascii import hexlify, unhexlify
import struct
from multiprocessing import Process
import subprocess

filename = 'test_addr490.json'

with open(filename)as fp:
    json_data = json.load(fp)
    index = 1
    for obj in json_data:
        lwc_id = 'lwc%s' % index
        index = index + 1
        print(obj["privkey"],obj["pubkey"],lwc_id)
        subprocess.Popen(['./client',obj["privkey"],obj["pubkey"],lwc_id])
        time.sleep(index)
        if index == 2:
            exit()

'''
filename = 'test_addr510.json'
with open(filename)as fp:
    json_data = json.load(fp)
    index = 1
    for obj in json_data:
        lwc_id = 'lwc%s' % index
        index = index + 1
        print(obj["privkey"],obj["pubkey"],lwc_id)
        subprocess.Popen(['./client',obj["privkey"],obj["pubkey"],lwc_id])
        time.sleep(index)
        if index == 2:
            exit()
'''