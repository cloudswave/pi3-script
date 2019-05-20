#!/bin/sh
mkdir /home/pi/bin/
#cp -r * /home/pi/bin/
basepath=$(cd `dirname $0`; pwd)
ln -s $basepath/frpc ~/bin/frpc
ln -s $basepath/monitor.sh ~/bin/monitor.sh
ln -s $basepath/frpc.ini ~/bin/frpc.ini

nohup ~/bin/monitor.sh >> /dev/null &
