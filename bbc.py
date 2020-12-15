#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import hashlib
import ed25519
import time
import uuid
import requests
import json
import sys
from binascii import hexlify, unhexlify
import struct
import base64
import conf

from ctypes import *

bbc = cdll.LoadLibrary('./libbbc.so')

def Addr2Hex(addr):
	hex_str = "-" * 66
	addr = c_char_p(str(addr).encode())
	hex_str = c_char_p(str(hex_str).encode())
	bbc.Addr2Hex(addr, hex_str)
	return hex_str.value


def TxFee(nVchData):
	nMinFee = 10000
	if 0 == nVchData:
		return nMinFee
	multiplier = int(nVchData / 200)
	if (nVchData % 200) > 0:
		multiplier = multiplier + 1
	if multiplier > 5:
		return nMinFee + nMinFee * 10 + (multiplier - 5) * nMinFee * 4
	else:
		return nMinFee + multiplier * nMinFee * 2

def GetTx(ts,forkid,utxo,addr,vchdata,pri_key):

	nVersion = hexlify(struct.pack("<H", 1))
	data = nVersion

	nType = hexlify(struct.pack("<H", 0))
	data = data + nType

	time = hexlify(struct.pack("<I", ts))
	data = data + time

	lockuntil = hexlify(struct.pack("<I", 0))
	data = data + lockuntil

	forkid = hexlify(unhexlify(forkid)[::-1])
	data = data + forkid

	input_size = hexlify(struct.pack("<B", len(utxo)))
	data = data + input_size
	amount = 0
	for obj in utxo:
		txid = obj["txid"] 
		txid = hexlify(unhexlify(txid)[::-1])
		out_n = hexlify(struct.pack("<B", obj["out"]))
		amount += obj["amount"]
		data = data + txid + out_n

	data = data + Addr2Hex(addr)
	fee =  TxFee(len(vchdata))

	nAmount = hexlify(struct.pack("<Q", int(amount - fee)))
	data = data + nAmount

	txfee = hexlify(struct.pack("<Q", fee))
	data = data + txfee
	vchdata_n = hexlify(struct.pack("<B", int(len(vchdata) / 2)))
	data = data + vchdata_n + vchdata
	blake2b = hashlib.blake2b(digest_size=32)
	blake2b.update(unhexlify(data))
	sign_hash = blake2b.hexdigest()

	sk = ed25519.SigningKey(unhexlify(pri_key)[::-1])
	sign_data = sk.sign(unhexlify(sign_hash))

	sign_size = hexlify(struct.pack("<B", len(sign_data)))
	data = data + sign_size + hexlify(sign_data)

	blake2b = hashlib.blake2b(digest_size=32)
	blake2b.update(unhexlify(data))
	txid_new = blake2b.hexdigest()
	txid_new = hexlify(struct.pack(">I", ts)) + hexlify(unhexlify(txid_new)[::-1])[8:]
	return {"txid":txid_new,"n":0,"amount":amount - fee,"tx":data}

def GetVchJson(data,ts):
	json_data = {
		"data":data
	}
	str_time = hexlify(struct.pack("<I", ts))
	b64_json = hexlify(base64.b64encode(b"json"))
	b64_json_n = hexlify(struct.pack("<B", int(len(b64_json) / 2)))
	return uuid.uuid1().hex.encode() + str_time + b64_json_n + b64_json + hexlify(json.dumps(json_data).encode())

def GetUtxo(address):
	forkid = "0000000006854ebdc236f48dbbe5c87312ea0abd7398888374b5ee9a5eb1d291"
	data_json = {
		"id":1,
		"method":"listunspent",
		"jsonrpc":"2.0",
		"params":
		{
			"address":address,
			"fork":forkid
		}
	}
	response = requests.post(conf.bbc_url, json=data_json)
	res = json.loads(response.text)
	for obj in res["result"]["addresses"][0]["unspents"]:
		obj["amount"] = int(obj["amount"] * 1000000)
	return res["result"]["addresses"][0]["unspents"]
	
if __name__ == '__main__':
	url = conf.bbc_url
	forkid = "0000000006854ebdc236f48dbbe5c87312ea0abd7398888374b5ee9a5eb1d291"
	address = "1965p604xzdrffvg90ax9bk0q3xyqn5zz2vc9zpbe3wdswzazj7d144mm"
	data_json = {
		"id":1,
		"method":"listunspent",
		"jsonrpc":"2.0",
		"params":
		{
			"address":address,
			"fork":forkid
		}
	}
	response = requests.post(url, json=data_json)
	res = json.loads(response.text)
	utxo = res["result"]["addresses"][0]["unspents"]
	
	ts = int(time.time())
	vchdata = GetVchJson("hello bbc by shang",ts)
	pri_key = "9df809804369829983150491d1086b99f6493356f91ccc080e661a76a976a4ee"
	data = GetTx(ts,forkid,utxo,address,vchdata,pri_key)

	data_json = {
		"id":2,
		"method":"sendrawtransaction",
		"jsonrpc":"2.0",
		"params":
		{
			"txdata":data["tx"]
		}
	}
	response = requests.post(url, json=data_json)
	res = json.loads(response.text)
	if res["result"] == data["txid"].decode():
		data_json = {
			"id":2,
			"method":"gettransaction",
			"jsonrpc":"2.0",
			"params":
			{
				"txid":data["txid"]
			}
		}
		response = requests.post(url, json=data_json)
		res = json.loads(response.text)
		data_str = res["result"]["transaction"]["data"]
		print("uuid1", data_str[0:8] + "-" + data_str[8:12] + "-" + data_str[12:16] + "-" + data_str[16:20] + "-" + data_str[20:32])
		v = struct.unpack("<I", unhexlify(data_str[32:40]))
		timeArray = time.localtime(v[0])
		otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
		print( "时间:", otherStyleTime)
		b64_json_n = struct.unpack("<B", unhexlify(data_str[40:42]))[0]
		if base64.b64decode(unhexlify(data_str[42:42+b64_json_n*2].encode())) == b"json":
			print("json:",json.loads(unhexlify(data_str[42+b64_json_n*2:]).decode()))
		else:
			print("不可解析")
	else:
		print("err")