#安装所需软件包
sudo apt-get install ntfs-3g
#加载内核模块
sudo modprobe fuse
mkdir /home/pi/share/my_usb
sudo mount /dev/sda1 /home/pi/share/my_usb -w
#sudo umount /home/pi/share/my_usb
sudo echo /dev/sda1 /home/pi/share/my_usb auto defaults,noexec,umask=0000 0 0 >> /etc/fstab
