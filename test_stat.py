#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import os
res = []
for file in os.listdir("./log"):
    f = open("./log/" + file,"r")
    ts = 0
    while True:
        text = f.readline()
        new_ts = text.split(" ")
        if len(new_ts) > 1:
            new_ts  = new_ts[1]
        else:
            break
        if not text:
            break

        if (new_ts.isdigit()):
            if ts == 0:
                ts = int(new_ts)
            else:
                res.append(int(new_ts) - ts)
                ts = int(new_ts)
print("avg:",sum(res)/len(res),",max:",max(res),",min:",min(res),",len:",len(res))