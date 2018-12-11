#!/bin/sh
mkdir /home/pi/bin/
cp -r * /home/pi/bin/
cd /home/pi/bin/
killall frpc
nohup ./frpc &
