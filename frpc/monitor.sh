#!/bin/bash
LOG_FILE="/home/pi/boot.log"
logit(){
    echo $(date "+%Y-%m-%d %H:%M:%S"): ${*} >> ${LOG_FILE}
}
while true;do
    count=`ps -ef|grep frpc|grep -v grep`
        if [ "$?" != "0" ];then
		logit "no frpc, run frpc"
		/home/pi/bin/frpc -c /home/pi/bin/frpc.ini
	#else
		#logit "frpc is runing..."
	fi
	sleep 5
done
