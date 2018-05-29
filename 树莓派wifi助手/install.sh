# https://github.com/emptyhua/raspberry_pi_helper
# 手机端蓝牙连接树莓派设置wifi用
# 蓝牙连接教程：https://blog.csdn.net/guzhong10/article/details/78574577

sudo apt-get install nodejs bluetooth bluez libbluetooth-dev libudev-dev
sudo ln -s /usr/bin/nodejs /usr/bin/node
git clone https://github.com/emptyhua/raspberry_pi_helper.git
cd ./raspberry_pi_helper
npm install
sudo ./start_pihelper.py