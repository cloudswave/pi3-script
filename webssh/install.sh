# https://github.com/huashengdun/webssh
# https://webssh.huashengdun.org/

sudo apt-get install libffi-dev
pip install webssh

mkdir /home/pi/bin/
basepath=$(cd `dirname $0`; pwd)
ln -s $basepath/wssh ~/bin/wssh

screen -dmS wssh ~/bin/wssh #run background 
# Open your browser, navigate to 127.0.0.1:8888 
# http://10.10.10.224:8888/?hostname=ssh.zhuxiaobo.ml&port=56675&username=pi&password=***
