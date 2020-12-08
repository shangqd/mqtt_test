#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import paho.mqtt.client as mqtt

client = mqtt.Client()

def on_connect(client, userdata, flags, rc):
    print("Connected with result code: " + str(rc))

def on_message(client, userdata, msg):
    a = bytes.decode(msg.payload)
    if msg.topic == "lws":
        client.subscribe(a, qos=2)
    else:
        client.publish(msg.topic + "-", payload=msg.payload, qos=2)
    print(msg.topic + " " + str(msg.payload))

client.on_connect = on_connect
client.on_message = on_message
client.connect('127.0.0.1', 1883, 600)
client.subscribe('lws', qos=2)
client.loop_forever()