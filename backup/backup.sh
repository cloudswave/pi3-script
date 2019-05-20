#！/bin/sh
#备份存放路径
TARGET_DIR=/media/pi/DA18-EBFA/pi-backup
#要备份的文件列表
BACKUP_FOLDERS=(
    '/home/pi/pi3-script/frpc'
    '/home/pi/pi3-script/startup'
    '/home/pi/.homeassistant/'
    '/home/pi/www/'
)
#排除的文件列表
EXCLUDES=(
    '*/.cloud'
    '*/.storage'
    '*/deps'
    '*/.uuid'
    '*/home-assistant_v2.db'
    '*/tts'
    '*/tts'
    '*/__pycache__'
    '*/*.log'
    '*/backup'
    '*/temp'
    '*/session'
    '*/recycle_kod'
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
