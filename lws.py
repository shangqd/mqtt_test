#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import time
import requests
import json
import sys
import bbc
import paho.mqtt.client as mqtt
import conf

def lws_on_connect(client, userdata, flags, rc):
    client.subscribe("lws-" + conf.lws_id,qos=2)
    print("Connected with result code: " + str(rc))

def lws_on_message(client, userdata, msg):
    try:
        bbc_cmd = json.loads(msg.payload)
        response = requests.post(conf.bbc_url, json=bbc_cmd)
        client.publish(bbc_cmd["address"], payload=response.text,qos=2)
    except:
        print("err:",time.strftime("%H:%M:%S", time.localtime()),bbc_cmd,response.text)


def lws_run():
    client = mqtt.Client()
    client.on_connect = lws_on_connect
    client.on_message = lws_on_message
    client.tls_set(ca_certs='./certs/ca.pem', certfile='./certs/client.pem', keyfile='./certs/client.key')
    client.tls_insecure_set(True)
    client.connect('mqtt.bigbangcamera.com', 8883, 60)
    client.loop_forever()

if __name__ == '__main__':
    lws_run()