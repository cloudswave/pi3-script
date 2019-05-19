#!/bin/bash
#readme http://www.senra.me/solutions-to-aria2-bt-metalink-download-slowly
killall aria2c
path=/home/pi/pi3-script/aria2/aria2.conf
list=`wget -qO- https://raw.githubusercontent.com/ngosang/trackerslist/master/trackers_all.txt|awk NF|sed ":a;N;s/\n/,/g;ta"`
if [ -z "`grep "bt-tracker" ${path}`" ]; then
    sed -i '$a bt-tracker='${list} ${path}
    echo add......
else
    sed -i "s@bt-tracker.*@bt-tracker=$list@g" ${path}
    echo update......
fi
aria2c --conf-path=/home/pi/pi3-script/aria2/aria2.conf -D