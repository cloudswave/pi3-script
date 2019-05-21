#!/bin/sh
# 参考https://www.jianshu.com/p/9e6289478bc8
mkdir /home/pi/bin/
cd /home/pi/bin/
wget https://github.com/syncthing/syncthing/releases/download/v1.1.4-rc.1/syncthing-linux-arm-v1.1.4-rc.1.tar.gz
tar zxvf syncthing-linux-arm-v1.1.4-rc.1.tar.gz
rm -rf syncthing-linux-arm-v1.1.4-rc.1.tar.gz
mv syncthing-linux-arm-v1.1.4-rc.1 syncthing
chmod +x ./syncthing/syncthing
./syncthing/syncthing
