### 环境ubuntu20,python3.8.5
```
pip install requests
pip install ed25519
pip install paho.mqtt
```

### mqtt 服务部署(可选项)
```
https://www.emqx.io/cn/downloads#broker   
wget https://www.emqx.io/cn/downloads/broker/v4.2.3/emqx-ubuntu16.04-4.2.3-x86_64.zip  
unzip emqx-ubuntu16.04-4.2.3-x86_64.zip   
./bin/emqx start   
```

### 启动bbc
```
bigbang -daemon
```
### 启动lws
```
./lws.py
```
### 启动lwc
```
./lwc.py
```
### 压力测试
```
./test.py
```
### 压测统计
```
cd test
./stat.py
```
### 渝信码测试，运行完成一个业务退出
```
./lws.py
./yxm.py
./zj.py
```
