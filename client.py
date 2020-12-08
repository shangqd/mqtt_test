#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import paho.mqtt.client as mqtt
import time
import sys

if len(sys.argv) == 1:
    print("./client clientid")
    sys.exit()

client = mqtt.Client()
def on_connect(client, userdata, flags, rc):
    print("Connected with result code: " + str(rc))

index = 0
clientid = sys.argv[1] 
#"lws-lwc01"
def on_message(client, userdata, msg):
    global index
    global clientid
    print(msg.topic + " " + str(msg.payload))
    time.sleep(3)
    index += 1
    client.publish(clientid, payload=("test-%d" % index), qos=2)

client.on_connect = on_connect
client.on_message = on_message
client.connect('127.0.0.1', 1883, 600)
client.subscribe(clientid + "-", qos=2)
client.publish('lws', payload=clientid, qos=2)
time.sleep(2)
client.publish(clientid, payload="lwc start", qos=2)
client.loop_forever()