#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import paho.mqtt.client as mqtt
import time
import sys
import bbc
import json
import conf
import threading

clientid = "18q29ne5h1c1p3v4s119qv74mhzdj5rcmzrgf1x1acsrf8wn017cdxxyj"
pri_key = "55a3faef666e9ba7b648e815c490b844ff458abc56d7537a5477d79cd718dae0"
forkid = "0000000006854ebdc236f48dbbe5c87312ea0abd7398888374b5ee9a5eb1d291"
amount = 0
index = 0
utxo = []

print("zj addr is %s" % clientid)


def begin_test(client):
    time.sleep(3)
    print("begin test ...")
    json_data = {
        "type":"zj -> yxm and bbc",
        "data":"abcdefg"
    }
    lws_req(json.dumps(json_data))
    yxm_req(json.dumps(json_data))
    print("zj -> (bbc and yxm)",json_data)

def on_connect(client, userdata, flags, rc):
    global forkid
    global clientid
    client.subscribe("zj-sub", qos=2)
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
    threading.Thread(target=begin_test, args=(client,)).start()

def lws_req(json_data):
    global client
    global clientid
    global amount
    global pri_key
    global index
    global forkid
    global utxo
    ts = int(time.time())
    vchdata = bbc.GetVchJson(json_data,ts)
    
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

def yxm_req(josn_data):
    client.publish("yxm-sub",payload=json.dumps(josn_data), qos=2)
    
def yxm_resp(yxm_cmd_resp):
    print("yxm -> zj",yxm_cmd_resp)
    sys.exit()


def on_message(client, userdata, msg): 
    global clientid
    if msg.topic == clientid:
        bbc_cmd_resp = json.loads(msg.payload.decode())
        lws_resp(bbc_cmd_resp)
    
    if msg.topic == "zj-sub":
        yxm_cmd_resp = json.loads(msg.payload.decode())
        yxm_resp(yxm_cmd_resp)

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.tls_set(ca_certs='./certs/ca.pem', certfile='./certs/client.pem', keyfile='./certs/client.key')
client.tls_insecure_set(True)
client.connect('mqtt.bigbangcamera.com', 8883, 60)
client.loop_forever()