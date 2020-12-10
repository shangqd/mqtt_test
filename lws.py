#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import paho.mqtt.client as mqtt

def lws_on_connect(client, userdata, flags, rc):
    client.subscribe('lws',qos=2)
    print("Connected with result code: " + str(rc))

def lws_on_message(client, userdata, msg):
    a = bytes.decode(msg.payload)
    if msg.topic == "lws":
        print('subscribe: %s' % a)
        client.subscribe(a,qos=2)
        client.publish(a, payload="lwc start",qos=2)
    else:
        client.publish(msg.topic + "-", payload=msg.payload,qos=2)
        print(msg.topic+","+str(msg.payload))

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