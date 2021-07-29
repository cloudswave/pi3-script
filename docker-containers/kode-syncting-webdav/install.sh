docker run -d \
  --name kodexplorer \
  --hostname=kodexplorer \
  -p 5210:5210 \
  -p 5218:5218 \
  -p 8384:8384 \
  -v /home/pi/koddata:/koddata \
  -v /media:/koddata/Group/public/home/media \
 -v /home/pi:/koddata/Group/public/home/pi\
  --restart unless-stopped \
  ethanzhu/kode-syncthing

docker run -d \
-v $HOME/Download:/data/download \
-v /media:/data/media \
-e USERNAME=webdav \
-e PASSWORD=webdav \
-p 1480:80 \
--restart=unless-stopped \
--name=webdav \
ugeek/webdav:arm-alpine