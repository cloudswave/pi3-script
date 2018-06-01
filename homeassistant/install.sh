#https://github.com/home-assistant/home-assistant
#https://home-assistant.cc/installation/general/

#Home Assistant 官方推荐使用 Python 虚拟环境安装 Home Assistant 以避免影响生产环境。
sudo apt-get install python3 python3-venv python3-pip
python3 -m venv homeassistant
cd homeassistant
source bin/activate
python3 -m pip install --upgrade homeassistant
hass --open-ui

sudo apt-get install vlc-nox
sudo usermod -a -G audio pi

cp ./*.yaml /home/pi/.homeassistant/
cp -r ./custom_components /home/pi/.homeassistant/

# 以下代码可以放到开机自启动shell脚本中
#killall hass
nohup /home/pi/homeassistant/bin/hass -c "/home/pi/.homeassistant" >> /dev/null &
