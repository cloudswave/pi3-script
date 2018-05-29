#!/bin/sh
cd /home/pi
# koe
echo "kode start" >> ./startup.log
/etc/init.d/php7-fpm restart &
/etc/init.d/nginx restart &

# node 
echo "node start" >> ./startup.log
forever start -w ./pi3-script/node_web/app.js

# nas 
echo samba restart >> ./startup.log
/etc/init.d/samba restart &

# frpc 
echo "frpc start" >> ./startup.log
nohup ./bin/frpc &

#挂载U
./mount-usb.sh

#wifi助手
echo "raspberry_pi_helper start" >> ./startup.log
sudo nohup ./raspberry_pi_helper/start_pihelper.py &