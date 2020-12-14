#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import time
import uuid
import requests
import json
import sys
from binascii import hexlify, unhexlify
import struct
from multiprocessing import Process
#import subprocess
import os

filename = 'test_addr510.json'

with open(filename)as fp:
    json_data = json.load(fp)
    index = 1
    for obj in json_data:
        lwc_id = 'lwc%s' % index
        index = index + 1
        print(obj["privkey"],obj["pubkey"],lwc_id)
        os.system('./lwc.py %s %s >./log/%s &' % (obj["address"],obj["privkey"], lwc_id))
        time.sleep(1)
        if index > 500:
            exit()
