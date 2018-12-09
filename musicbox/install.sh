#参考：http://jingyan.eeboard.com/article/75227
sudo apt-get install python-pip python-setuptools -y
sudo pip install requests
sudo pip2 install NetEase-MusicBox
sudo apt-get install mpg123
exit
# 个人版安装
#https://github.com/cloudswave/musicbox
git clone git@github.com:cloudswave/musicbox.git && cd musicbox
python setup.py install