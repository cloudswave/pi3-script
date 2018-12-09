#!/bin/bash
LOG_FILE="/home/pi/boot.log"
function logit()
{
    echo "[${USER}][`date`] - ${*}" >> ${LOG_FILE}
}
cd /home/pi

# koe
logit "kode start"
/etc/init.d/php7.0-fpm restart &
/etc/init.d/nginx restart &

# node 
logit "node start"
forever start -w ./pi3-script/node_web/app.js

# nas 
logit "samba restart"
/etc/init.d/samba restart &

# web shell
shellinaboxd -b -t -p 4200


#wifi助手
logit "raspberry_pi_helper start"
sudo nohup ./raspberry_pi_helper/start_pihelper.py >> /dev/null &

# 智能家居助手
nohup ./homeassistant/bin/hass -c "/home/pi/.homeassistant" >> /dev/null &

# 监控frpc进程
#nohup ./monitor.sh >> /dev/null &

# 叮当语音
#echo ...启动叮当语音.. >> ./startup.log
#sh /home/pi/dingdang/launcher/dingdang-launcher-user.sh
# shairplay
#nohup shairplay -a pi >> /dev/null &
#logit "shairport start"
#./shairport/shairport -a pi -d

# frpc
#logit "frpc start"
#nohup ./bin/frpc >> /dev/null &

# usb mount
./my_usb.sh

#设置硬盘自动休眠，数值/12 = 分钟，设置为120就是无操作10分钟后休眠
sudo hdparm -S 120 /dev/sda1

# aria2c
logit "aria2c start"
aria2c --conf-path="/home/pi/aria2/aria2.conf" -D

