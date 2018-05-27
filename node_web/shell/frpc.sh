killall frpc
nohup /home/pi/bin/frpc -c /home/pi/frpc.ini &
echo `date`:frpc >> /home/pi/pi3-script/node_web/shell/shell.log