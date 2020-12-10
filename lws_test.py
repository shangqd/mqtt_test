#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import time, threading
from multiprocessing.dummy import Pool
import paho.mqtt.client as mqtt

concurrency = 100

def lws_on_connect(client, userdata, flags, rc):
    client.subscribe('lws')
    print("Connected with result code: " + str(rc))

def lws_on_message(client, userdata, msg):
    a = bytes.decode(msg.payload)
    if msg.topic == "lws":
        print('subscribe: %s' % a)
        client.subscribe(a)
        client.publish(a, payload="lwc start")
    else:
        client.publish(msg.topic + "-", payload=msg.payload)
    # print(msg.topic + " " + str(msg.payload))

def lws_run():
    client = mqtt.Client()
    client.on_connect = lws_on_connect
    client.on_message = lws_on_message
    client.tls_set(ca_certs='ca.pem', certfile='client.pem', keyfile='client.key')
    client.tls_insecure_set(True)
    client.connect('mqtt.bigbangcamera.com', 8883, 60)
    client.loop_forever()


def client_on_connect_warp(clientid):
    def client_on_connect(client, userdata, flags, rc):
        print("Connected with client: " + str(clientid))
        client.subscribe(str(clientid) + "-")
        client.publish('lws', payload=str(clientid))
        print("client notified: %s" % clientid)
        # time.sleep(10)
        # client.publish(str(clientid), payload="lwc start")
        # print("client published: %s" % clientid)
    return client_on_connect

index = 0
# clientid = 0

def client_on_message_warp(clientid):
    def client_on_message(client, userdata, msg):
        global index
        print('----' + msg.topic + " " + str(msg.payload))
        time.sleep(0.1)
        index += 1
        client.publish(str(clientid), payload=("test-%d" % index), qos=2)
        # print('--> %s' % index)
    return client_on_message

def client_run(clientid):
    client = mqtt.Client()
    client.on_connect = client_on_connect_warp(clientid)
    client.on_message = client_on_message_warp(clientid)
    client.tls_set(ca_certs='ca.pem', certfile='client.pem', keyfile='client.key')
    client.tls_insecure_set(True)
    client.connect('mqtt.bigbangcamera.com', 8883, 60)
    client.loop_forever()

if __name__ == '__main__':
    threading.Thread(target=lws_run, daemon=True).start()
    time.sleep(2)
    client_pool = Pool(concurrency)
    client_pool.map(client_run, range(concurrency))

