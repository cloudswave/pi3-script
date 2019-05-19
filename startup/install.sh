basepath=$(cd `dirname $0`; pwd)
ln -s $basepath/startup.sh ~/startup.sh
#cp ./startup.sh /home/pi
echo "please add startup to /etc/rc.local demo:"
cat ./rc.local
sudo vi /etc/rc.local
