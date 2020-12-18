#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import time
import requests
import json
import sys
import bbc
import paho.mqtt.client as mqtt
import conf

def lws_on_connect(client, userdata, flags, rc):
    client.subscribe(conf.lws_id,qos=2)
    print("Connected with result code: " + str(rc))

def lws_on_message(client, userdata, msg):
    a = bytes.decode(msg.payload)
    if msg.topic == conf.lws_id:
        client.subscribe(a,qos=2)
        print('subscribe: %s' % a)
        utxos = json.dumps(bbc.GetUtxo(a))
        client.publish(a + "-", payload=utxos,qos=2)
        
    else:
        print(time.strftime("%H:%M:%S", time.localtime()),"client is",msg.topic)
        response = requests.post(conf.bbc_url, json=json.loads(msg.payload))
        client.publish(msg.topic + "-", payload=response.text,qos=2)



def lws_run():
    client = mqtt.Client()
    client.on_connect = lws_on_connect
    client.on_message = lws_on_message
    client.tls_set(ca_certs='ca.pem', certfile='client.pem', keyfile='client.key')
    client.tls_insecure_set(True)
    client.connect('mqtt.bigbangcamera.com', 8883, 60)
    client.loop_forever()

if __name__ == '__main__':
    lws_run()