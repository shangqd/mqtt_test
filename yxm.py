#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import paho.mqtt.client as mqtt
import time
import sys
import bbc
import json
import conf

clientid = "1965p604xzdrffvg90ax9bk0q3xyqn5zz2vc9zpbe3wdswzazj7d144mm"
pri_key = "9df809804369829983150491d1086b99f6493356f91ccc080e661a76a976a4ee"
forkid = "0000000006854ebdc236f48dbbe5c87312ea0abd7398888374b5ee9a5eb1d291"
amount = 0
index = 0
utxo = []

print("yxm addr is %s" % clientid)

def on_connect(client, userdata, flags, rc):
    global forkid
    global clientid
    client.subscribe("yxm-sub", qos=2)
    client.subscribe(clientid, qos=2)
    bbc_cmd = {
        "id":0,
        "method":"listunspent",
        "address":clientid,
        "jsonrpc":"2.0",
        "params":{
            "address":clientid,
            "fork": forkid
        }
    }
    client.publish("lws-" + conf.lws_id, payload=json.dumps(bbc_cmd), qos=2)
    print("Connected with result code: " + str(rc))

def lws_resp(bbc_cmd_resp):
    global clientid
    global amount
    global pri_key
    global index
    global forkid
    global utxo
    utxo = []
    if "result" in bbc_cmd_resp:
        if "addresses" in bbc_cmd_resp["result"]:
            for obj in bbc_cmd_resp["result"]["addresses"][0]["unspents"]:
                utxo.append({
                    "txid": obj["txid"],
                    "out": obj["out"], 
                    "amount": obj["amount"] * 1000000,  
                    "lockuntil": obj["lockuntil"]})
        else:
            utxo.append({
                "txid": bbc_cmd_resp["result"],
                "out": 0, 
                "amount": amount, 
                "lockuntil": 0})
    print("bbc ok",len(utxo))

def lws_req(josn_data):
    global clientid
    global amount
    global pri_key
    global index
    global forkid
    global utxo
    global client
    ts = int(time.time())
    vchdata = bbc.GetVchJson(josn_data,ts)
    
    data = bbc.GetTx(ts,forkid,utxo,clientid,vchdata,pri_key)
    amount = data["amount"]
    #print(index,ts,time.strftime("%H:%M:%S", time.localtime()),"addr:%s, amount:%s" % (clientid, amount / 1000000))
    data_json = {
		"id":2,
		"method":"sendrawtransaction",
        "address":clientid,
		"jsonrpc":"2.0",
		"params":
		{
			"txdata":data["tx"].decode()
		}
	}
    client.publish("lws-" + conf.lws_id,payload=json.dumps(data_json), qos=2)

def zj_resp(zj_cmd_resp):
    print("zj -> yxm",zj_cmd_resp)
    josn_data = {
        "type":"yxm --> zj",
        "data":"123456"
    }
    josn_data = json.dumps(josn_data)
    print("yxm -> (bbc and zj)",josn_data)
    lws_req(josn_data)
    zj_req(josn_data)

def zj_req(josn_data):
    global client
    client.publish("zj-sub",payload=josn_data, qos=2)

def on_message(client, userdata, msg):
    global clientid
    if msg.topic == clientid:
        bbc_cmd_resp = json.loads(msg.payload.decode())
        lws_resp(bbc_cmd_resp)
    
    if msg.topic == "yxm-sub":
        zj_cmd_resp = json.loads(msg.payload.decode())
        zj_resp(zj_cmd_resp)

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.tls_set(ca_certs='./certs/ca.pem', certfile='./certs/client.pem', keyfile='./certs/client.key')
client.tls_insecure_set(True)
client.connect('mqtt.bigbangcamera.com', 8883, 60)
client.loop_forever()