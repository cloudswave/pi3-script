basepath=$(cd `dirname $0`; pwd)
ln -s $basepath/backup.sh ~/backup.sh
~/backup.sh
