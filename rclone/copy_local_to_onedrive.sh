#！/bin/sh
ERROR_LOG_FILE=~/onedrive_backup.log
echo $(date "+%Y-%m-%d %H:%M:%S"): "onedrive backup data start" >> ${ERROR_LOG_FILE}
rclone copy /media/pi/DA18-EBFA/pi-backup/ remote:pi
rclone copy /media/pi/DA18-EBFA/apk/ remote:apk
rclone copy /media/pi/DA18-EBFA/ip-webcam/ remote:ip-webcam
rclone copy /media/pi/DA18-EBFA/pc-software/ remote:ip-software
rclone copy /media/pi/DA18-EBFA/document/ remote:document
rclone copy /media/pi/DA18-EBFA/fuli/short-video/ remote:fuli/short-video
echo $(date "+%Y-%m-%d %H:%M:%S"): "onedrive backup data end" >> ${ERROR_LOG_FILE}
