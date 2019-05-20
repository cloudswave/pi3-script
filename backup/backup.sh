#！/bin/sh
TARGET_DIR=/media/pi/DA18-EBFA/pi-backup
BACKUP_FOLDERS=(
'/home/pi/bin/'
'/home/pi/.homeassistant/'
'/home/pi/www/'
'/home/pi/startup.sh'
)
EXCLUDES=(
'*/.uuid'
'*/home-assistant_v2.db'
'*/tts'
'*/tts'
'*/__pycache__'
'*/*.log'
'*/backup'
'*/temp'
'*/session'
)


ERROR_LOG_FILE=./backup.log
mkdir -p ${TARGET_DIR}
DIRS=''
for i in "${BACKUP_FOLDERS[@]}"; do
    DIRS="${DIRS} ${i}"
done
excludelist=''
#excludelist="--exclude */.uuid --exclude */home-assistant_v2.db --exclude */tts --exclude */__pycache__ --exclude */*.log"
for j in "${EXCLUDES[@]}"; do
    excludelist="${excludelist} --exclude ${j}"
done
echo $(date "+%Y-%m-%d %H:%M:%S"): backup data to ${TARGET_DIR}/backup-$(date +%Y%m%d).tar.gz start >> ${ERROR_LOG_FILE}
tar czPvf ${TARGET_DIR}/backup-$(date +%Y%m%d).tar.gz ${excludelist} ${DIRS}  
echo $(date "+%Y-%m-%d %H:%M:%S"): "backup data end" >> ${ERROR_LOG_FILE}

#删除改文件夹下超过30天的文件
find ${TARGET_DIR} -mtime +30 -name "*.tar.gz" -exec rm -rf {} \;
