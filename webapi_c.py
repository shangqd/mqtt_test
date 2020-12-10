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
import bbc
import os
#1965p604xzdrffvg90ax9bk0q3xyqn5zz2vc9zpbe3wdswzazj7d144mm

#url = "http://127.0.0.1:19902/getutxo/1965p604xzdrffvg90ax9bk0q3xyqn5zz2vc9zpbe3wdswzazj7d144mm/0000000006854ebdc236f48dbbe5c87312ea0abd7398888374b5ee9a5eb1d291"
#response = requests.get(url)
#res = json.loads(response.text)
#utxo = res[0]
#'out': 0, 'amount': 300000000.0, 'txid'
#print(utxo["out"],utxo["amount"],utxo["txid"])
nVersion = hexlify(struct.pack("<H", 1))
data = nVersion

nType = hexlify(struct.pack("<H", 0))
data = data + nType

ts = 1607503628
time = hexlify(struct.pack("<I", ts))
data = data + time

lockuntil = hexlify(struct.pack("<I", 0))
data = data + lockuntil

forkid = "0000000006854ebdc236f48dbbe5c87312ea0abd7398888374b5ee9a5eb1d291"
forkid = hexlify(unhexlify(forkid)[::-1])
data = data + forkid

input_size = hexlify(struct.pack("<B", 1))
data = data + input_size

txid = "5de140807b1160347b1a303ec004625116901df66d2220fb3ff6a1ea0019836b"
txid = hexlify(unhexlify(txid)[::-1])
out_n = hexlify(struct.pack("<B", 0))
data = data + txid + out_n

data = data + bbc.Addr2Hex("1965p604xzdrffvg90ax9bk0q3xyqn5zz2vc9zpbe3wdswzazj7d144mm")

nAmount = hexlify(struct.pack("<Q", 299999999000000))
data = data + nAmount

txfee = hexlify(struct.pack("<Q", 1000000))
data = data + txfee

vchdata = b""
vchdata_n = hexlify(struct.pack("<B", len(vchdata)))
data = data + vchdata_n + vchdata

blake2b = hashlib.blake2b(digest_size=32)
blake2b.update(unhexlify(data))
sign_hash = blake2b.hexdigest()

pri_key = "9df809804369829983150491d1086b99f6493356f91ccc080e661a76a976a4ee"
sk = ed25519.SigningKey(unhexlify(pri_key)[::-1])
sign_data = sk.sign(unhexlify(sign_hash))

sign_size = hexlify(struct.pack("<B", len(sign_data)))
data = data + sign_size + hexlify(sign_data)

#print(data)

blake2b = hashlib.blake2b(digest_size=32)
blake2b.update(unhexlify(data))
txid_new = blake2b.hexdigest()
txid_new = hexlify(struct.pack(">I", ts)) + hexlify(unhexlify(txid_new)[::-1])[8:]
if txid_new == b"5fd08f0c2b3abdc6cda584def9425b615566742a61d58fd692d5b58b7db8b979":
    print("OK")

#5fd08f0c2b3abdc6cda584def9425b615566742a61d58fd692d5b58b7db8b979
#5fd08f0c2b3abdc6cda584def9425b615566742a61d58fd692d5b58b7db8b979
#010000000c8fd05f0000000091d2b15e9aeeb57483889873bd0aea1273c8e5bb8df436c2bd4e850600000000016b831900eaa1f63ffb20226df61d9016516204c03e301a7b3460117b8040e15d0001498b63009dfb70f7ee0902ba95cc171f7d7a97ff16d89fd96e1f1b9e7d5f91dac07d5f31d910010040420f0000000000004091a1f21c411ee54776f503b0a96ad8578cdd70ee1d18b7895435e78ea83d007e3ac0a6f2fec278a43b9b9852828815bb97ade2c67dca2c0fb6c132fdc739f008
#010000000c8fd05f0000000091d2b15e9aeeb57483889873bd0aea1273c8e5bb8df436c2bd4e850600000000016b831900eaa1f63ffb20226df61d9016516204c03e301a7b3460117b8040e15d0001498b63009dfb70f7ee0902ba95cc171f7d7a97ff16d89fd96e1f1b9e7d5f91dac07d5f31d910010040420f0000000000004091a1f21c411ee54776f503b0a96ad8578cdd70ee1d18b7895435e78ea83d007e3ac0a6f2fec278a43b9b9852828815bb97ade2c67dca2c0fb6c132fdc739f008
