#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import paho.mqtt.client as mqtt
import time
import sys
import bbc
import json


clientid = "1965p604xzdrffvg90ax9bk0q3xyqn5zz2vc9zpbe3wdswzazj7d144mm"
amount = 0
if len(sys.argv) == 2:
    clientid = sys.argv[1]

print("clientid is %s" % clientid)

def on_connect(client, userdata, flags, rc):
    client.subscribe(clientid + "-", qos=2)
    client.publish('lws', payload=clientid, qos=2)
    print("Connected with result code: " + str(rc))

def on_message(client, userdata, msg):
    global clientid
    global amount
    utxo = json.loads(msg.payload.decode())
    if "result" in utxo:
        utxo = [{
            "txid": utxo["result"],
            "out": 0, 
            "amount": amount,  
            "lockuntil": 0}]
    forkid = "0000000006854ebdc236f48dbbe5c87312ea0abd7398888374b5ee9a5eb1d291"
    ts = int(time.time())
    vchdata = bbc.GetVchJson("hello bbc by shang",ts)
    pri_key = "9df809804369829983150491d1086b99f6493356f91ccc080e661a76a976a4ee"
    data = bbc.GetTx(ts,forkid,utxo,clientid,vchdata,pri_key)
    amount = data["amount"]
    print(time.strftime("%H:%M:%S", time.localtime()),"addr:%s, amount:%s" % (clientid, amount / 1000000))
    data_json = {
		"id":2,
		"method":"sendrawtransaction",
		"jsonrpc":"2.0",
		"params":
		{
			"txdata":data["tx"].decode()
		}
	}
    time.sleep(3)
    client.publish(clientid,payload=json.dumps(data_json), qos=2)


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
#client.connect('127.0.0.1', 1883, 600)
client.tls_set(ca_certs='ca.pem', certfile='client.pem', keyfile='client.key')
client.tls_insecure_set(True)
client.connect('mqtt.bigbangcamera.com', 8883, 60)
#client.publish(clientid,payload=clientid,qos=2)
client.loop_forever()