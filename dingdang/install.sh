
#安装dingdang参考：https://github.com/dingdang-robot/dingdang-robot/wiki/install

cp ./dingdnag /home/pi/.dingdang/

# 以下代码可以放到开机自启动shell脚本中
# 叮当语音
#echo ...启动叮当语音.. >> ./startup.log
sh /home/pi/dingdang/launcher/dingdang-launcher-user.sh
