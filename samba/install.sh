# 参考：https://www.cnblogs.com/mnstar/p/8144943.html
sudo cp -rf ./smb.conf /etc/samba/
# 设置pi密码
echo "please set smbpasswd for pi"
sudo smbpasswd -a pi

sudo /etc/init.d/samba restart
