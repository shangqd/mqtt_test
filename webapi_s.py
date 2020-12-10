#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import pymysql
import sys
import json
import requests
from binascii import hexlify, unhexlify
from flask import Flask,jsonify,render_template,request,make_response, send_from_directory, abort
import os
import hashlib
import uuid
from werkzeug.utils import secure_filename
import hashlib
from pathlib import Path

app = Flask(__name__)


@app.route('/')
def help():
    return  '''
            <a href='/getutxo/1965p604xzdrffvg90ax9bk0q3xyqn5zz2vc9zpbe3wdswzazj7d144mm/0000000006854ebdc236f48dbbe5c87312ea0abd7398888374b5ee9a5eb1d291'>查看utxo</a>
            '''

@app.route('/getutxo/<address>/<fork>')
def getutxo(address,fork):
    json_data = {
        "id":1,
        "method":"listunspent",
        "jsonrpc":"2.0",
        "params":
        {
            "address":address,
            "fork":fork
        }
    }
    response = requests.post("http://127.0.0.1:9902", json=json_data)
    res = json.loads(response.text)
    return jsonify(res["result"]["addresses"][0]["unspents"])

#sudo pip install uWSGI==2.0.15
#uwsgi --http :5000 --wsgi-file api.py --callable app
if __name__ == '__main__':
    print("app run ...")
    app.run(host = '0.0.0.0',port=19902, debug=True)