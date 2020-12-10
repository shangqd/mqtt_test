#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import paho.mqtt.client as mqtt
import time
import sys
if len(sys.argv) == 1:
    print("./client clientid")
    sys.exit()

def on_connect(client, userdata, flags, rc):
    client.subscribe(clientid + "-", qos=2)
    client.publish('lws', payload=clientid, qos=2)
    print("Connected with result code: " + str(rc))

index = 0
clientid = sys.argv[1] 
#"lws-lwc01"
def on_message(client, userdata, msg):
    global index
    global clientid
    print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),msg.topic + " " + str(msg.payload))
    time.sleep(1)
    index += 1
    client.publish(clientid, payload=("test-%d" % index), qos=2)
    if index >= 500:
        sys.exit()

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
#client.connect('127.0.0.1', 1883, 600)
client.tls_set(ca_certs='ca.pem', certfile='client.pem', keyfile='client.key')
client.tls_insecure_set(True)
client.connect('mqtt.bigbangcamera.com', 8883, 60)
#time.sleep(2)
client.loop_forever()