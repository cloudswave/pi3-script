apt-get install php7.0 php7.0-fpm php7.0-common php-mbstring
apt-get remove --purge apache* -y
apt-get autoremove --purge -y
apt-get install nginx
cp ./default /etc/nginx/sites-available/
/etc/init.d/php7-fpm restart
/etc/init.d/nginx restart
wget http://static.kodcloud.com/update/download/kodexplorer4.25.zip
unzip kodexplorer4.25.zip /home/pi/www/
