apt-get install php7.0 php7.0-fpm php7.0-common php-mbstring
apt-get remove --purge apache* -y
apt-get autoremove --purge -y
apt-get install nginx
cp ./default /etc/nginx/sites-available/

wget http://static.kodcloud.com/update/download/kodexplorer4.25.zip
unzip kodexplorer4.25.zip /home/pi/www/

#为了使KodExplorer能读写树莓派pi用户下挂载的移动硬盘（/media/pi/）需要修改nginx，php运行用户为pi，下面为修改笔记
sudo vi /etc/nginx/nginx.conf
#user pi; #第一行
sudo vi /etc/php/7.0/fpm/php-fpm.conf
# 末尾增加
# user = pi
# group = pi

sudo chown -R pi:pi /run/php/
sudo chown -R pi:pi /var/log/nginx/
sudo chown -R pi:pi /var/log/nginx/
sudo chown -R pi:pi /home/pi/www/

/etc/init.d/php7.0-fpm restart
/etc/init.d/nginx restart
