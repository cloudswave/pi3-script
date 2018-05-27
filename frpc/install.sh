#!/bin/sh
cp -r * /home/pi/bin/
cd /home/pi/bin/
killall frpc
nohup ./frpc &
