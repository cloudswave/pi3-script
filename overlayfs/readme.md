## 使用overlayfs影子系统打造一个只读的不怕意外关机的树莓派
关闭交换分区
```
sudo swapoff -a
sudo rm -rf /swapfile
free # 查看是否生效

pi@raspbian:~/pi3-script/overlayfs$ free
              total        used        free      shared  buff/cache   available
Mem:         977980      491368       27672       13900      458940      430668
Swap:             0           0           0

```
永久关闭swap,将/boot分区也修改为只读，修改 fstab 文件，把/boot 对应的行改为ro
```
sudo vi /etc/fstab
# 修改后
pi@raspbian:~/pi3-script/overlayfs$ cat /etc/fstab
proc /proc proc defaults 0 0
PARTUUID=daf1c5e3-01 /boot vfat ro 0 2
PARTUUID=daf1c5e3-02 / ext4 defaults,noatime,nodiratime 0 1
# 注释掉下面这行
# /swapfile swap swap defaults 0 0



```
add script to /sbin
```
cp ./overlayRoot.sh /sbin/
```
add command to ~/.bashrc
```
function reboot_rw(){
  sudo mount -o remount,rw /boot
  sudo sed -i 's/ init=\/sbin\/overlayRoot.sh//g' /boot/cmdline.txt
  sudo reboot
}
function reboot_ro() {
  sudo mount -o remount,rw /boot
  sudo sed -i 's/\($\)/ init=\/sbin\/overlayRoot.sh/g' /boot/cmdline.txt
  sudo reboot
}
function rw() {
    sudo mount -o remount,rw /ro
    sudo mount -o remount,rw /boot
}
```
切换overlayfs指令
```
reboot_ro # enter overlayfs
mount # 查看是否生效  /dev/mmcblk0p2 改为挂载在 /ro ，并且是只读；/boot 也挂载为只读；而 / 的 type 变成了overlay
# /dev/mmcblk0p2 on /ro type ext4 (ro,noatime,data=ordered) 

reboot_rw # exit overlayfs
rw # 不切换系统的时候挂载读写
```
临时想读写
```
sudo mount -o remount,rw /ro
sudo mount -o remount,rw /boot
```

参考：
http://www.glgxt.cn/file/25.html
https://blog.csdn.net/bona020/article/details/79039410
https://blog.csdn.net/zhufu86/article/details/78906046
