https://www.emqx.io/cn/downloads#broker   
wget https://www.emqx.io/cn/downloads/broker/v4.2.3/emqx-ubuntu16.04-4.2.3-x86_64.zip  
unzip emqx-ubuntu16.04-4.2.3-x86_64.zip   
./bin/emqx start   

``` 部署容器
https://www.runoob.com/docker/docker-install-python.html
sudo docker pull python:3.9
sudo docker images python:3.9
sudo docker run -it -v /home/shang/shangqd/mqtt_test:/var/tmp python:3.9 /bin/bash
### 容器内执行
git clone https://github.com/shangqd/mqtt_test
# 修改配置项目的配置文件能让他正常访问bbc
cd mqtt_test
pip install requests
pip install ed25519
pip install paho.mqtt
python3 lws.py
```

# 管理容器
sudo docker ps -a
sudo docker rm -f e3d72a15ac9e
docker attach 1e560fca3906 
