#!/bin/sh
echo "===init==="
function update()
{
  	sudo cp /etc/apt/sources.list /etc/apt/sources.list.bak
	sudo cp sources.list /etc/apt/sources.list
	sudo apt-get -y update
	sudo apt-get -y upgrade
	sudo apt-get -y dist-upgrade
	sudo rpi-update
	
	#配置wifi: 
    sudo raspi-config 
    #修改root密码： 
    chpasswd root
}

function startup(){
    #设置开机启动
    echo "add startup to /etc/rc.local demo:"
    cp ./startup/startup.sh /home/pi/
    sudo cp /etc/rc.local /etc/rc.local.bak
    sudo cp ./startup/rc.local /etc/rc.local
    #cat ./rc.local
    #sudo vi /etc/rc.local
}

function base()
{
	# vi
	sudo apt-get -y remove vim-common
	sudo apt-get -y install vim
	cp vimrc ~/.vimrc
	# IP
	#sudo cp interfaces /etc/network/interfaces
	#sudo systemctl daemon-reload
	#sudo service networking restart
	# Chinese
	#sudo apt-get -y install ttf-wqy-zenhei ttf-wqy-microhei
	#sudo apt-get -y install fcitx fcitx-googlepinyin fcitx-module-cloudpinyin fcitx-sunpinyin
	
	#echo LC_ALL="en_US.UTF-8" | sudo tee -a  /etc/environment
	#echo LANG="en_US.UTF-8" | sudo tee -a /etc/environment
	# USB
	#echo "# USB Voltage" | sudo tee -a /boot/config.txt
	#echo "max_usb_current=1" | sudo tee -a /boot/config.txt
	# SSH
    #设置 SSH，打开密钥登录功能
    ssh-keygen -t rsa
    cat ~/.ssh/id_rsa.pub >> ~/.ssh/authorized_keys
    echo "RSAAuthentication yes" | sudo tee -a /etc/ssh/sshd_config
    echo "PubkeyAuthentication yes" | sudo tee -a /etc/ssh/sshd_config
    echo "PermitRootLogin yes" | sudo tee -a /etc/ssh/sshd_config
    sudo /etc/init.d/ssh restart
    # 以后新电脑上先ssh-keygen 然后 将id_rsa.pub内容追加到服务器~/.ssh/authorized_keys中
    #echo "公钥内容" >>  ~/.ssh/authorized_keys
    
	# zip
	sudo apt-get -y install zip
	# ssh key
	ssh-keygen -t rsa -C "764724624@qq.com" -b 4096
	


}


function dev()
{
  	#zsh
	#安装zsh: `sudo apt-get install zsh`
    sudo apt-get install zsh
    #安装oh-my-zsh: `sh -c "$(curl -fsSL https://raw.github.com/robbyrussell/oh-my-zsh/master/tools/install.sh)"`
    sh -c "$(curl -fsSL https://raw.github.com/robbyrussell/oh-my-zsh/master/tools/install.sh)"
    cp ./zsh/.zshrc ~ #配置
    source ~/.zshrc
    #安装autojump:
    sudo apt-get install autojump
    
    sudo apt-get install git
    sudo apt-get install nodejs
    sudo apt-get install npm
    sudo apt-get install forever
    sudo ln -s /usr/bin/nodejs /usr/bin/node
}

function php_nginx_kode(){
    echo "安装php nginx kode"
    return
    sudo -s
    apt-get install php7.0 php7.0-fpm php7.0-common php-mbstring
    apt-get remove --purge apache* -y
    apt-get autoremove --purge -y
    apt-get install nginx
    cp ./php_nginx_kode/default /etc/nginx/sites-available/
    /etc/init.d/php7-fpm restart
    /etc/init.d/nginx restart
    wget http://static.kodcloud.com/update/download/kodexplorer4.25.zip
    unzip kodexplorer4.25.zip -d /home/pi/www/
	 su -c 'setenforce 0'
	 chmod -R 777 /home/pi/www/
    exit
    
}

function frpc(){
    cp -r ./frpc/frpc /home/pi/bin/
    cp ./frpc/frpc.ini /home/pi/
    killall frpc
    nohup /home/pi/bin/frpc -c /home/pi/frpc.ini &
}

function tools(){
    
    php_nginx_kode
    
    frpc
    return
    
    #安装aria2
    sudo apt-get install aria2
    cp -r ./aria2 /home/pi/
    aria2c --conf-path="/home/pi/aria2/aria2.conf" -D
    
    # Samba
    cp ./samba/smb.conf /etc/samba/
    cat ./samba/smb.conf
    sudo /etc/init.d/samba restart
}
#------------main
update
startup
base
dev
tools

# Done
echo "===============end=================!"
