#!/bin/sh
LOG_FILE="/home/pi/boot.log"
function logit()
{
    echo "[${USER}][`date`] - ${*}" >> ${LOG_FILE}
}
cd /home/pi
# koe
logit "kode start"
/etc/init.d/samba restart &
aria2c --conf-path="/home/pi/pi3-script/aria2/aria2.conf" -D &
/etc/init.d/php7.0-fpm restart &
/etc/init.d/nginx restart &
logit "智能家居助手 start"
nohup /home/pi/homeassistant/bin/hass -c "/home/pi/.homeassistant" >> /dev/null &

# 监控frpc进程
nohup ./bin/monitor.sh >> /dev/null &
