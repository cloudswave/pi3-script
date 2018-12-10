APP下载地址：https://itunes.apple.com/cn/app/shu-mei-pai-zhu-shou/id1110826090?l=zh&ls=1&mt=8

树莓派助手可以帮助树莓派3通过手机APP设置WiFi连接，下面是树莓派接收端的安装过程
```bash
sudo apt-get install nodejs bluetooth bluez libbluetooth-dev libudev-dev
sudo ln -s /usr/bin/nodejs /usr/bin/node
git clone https://github.com/emptyhua/raspberry_pi_helper.git
cd ./raspberry_pi_helper
npm install
sudo ./start_pihelper.py
```
安装成功后，下载树莓派助手APP，便可以搜索到树莓派。调试成功后便可以将start_pihelper.py设置开机自启。
