#!/bin/sh
LOG_FILE="/home/pi/boot.log"
logit(){
    echo $(date "+%Y-%m-%d %H:%M:%S"): ${*} >> ${LOG_FILE}
}
cd /home/pi
# koe
logit "samba aria2c kode start"
/etc/init.d/samba restart &
aria2c --conf-path="/home/pi/pi3-script/aria2/aria2.conf" -D &
/etc/init.d/php7.0-fpm restart &
/etc/init.d/nginx restart &
logit "homeassistan start"
nohup /home/pi/homeassistant/bin/hass -c "/home/pi/.homeassistant" >> /dev/null &

# 监控frpc进程
logit "frpc start"
nohup ./bin/monitor.sh >> /dev/null &
