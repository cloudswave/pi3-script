#!/bin/sh
LOG_FILE="/home/pi/boot.log"
logit(){
    echo $(date "+%Y-%m-%d %H:%M:%S"): ${*} >> ${LOG_FILE}
}
cd /home/pi
# koe
logit "samba aria2c start"
/etc/init.d/samba restart &
#aria2c --conf-path="/home/pi/pi3-script/aria2/aria2.conf" -D &
qbittorrent-nox --webui-port=8081 -d

logit "homeassistan start"
nohup /home/pi/homeassistant/bin/hass -c "/home/pi/.homeassistant" >> /dev/null &

logit "webssh start"
screen -dmS wssh ./bin/wssh

# 监控frpc进程
logit "frpc start"
nohup ./bin/monitor.sh >> /dev/null &

#syncthing
logit "syncthing start"
nohup ./bin/syncthing/syncthing >> /dev/null &

logit "php nginx start"
/etc/init.d/php7.0-fpm restart &
/etc/init.d/nginx restart &
sleep 5
logit "chown -R pi:pi /run/php/"
sudo chown -R pi:pi /run/php/ &
