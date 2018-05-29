#参考：http://ju.outofmemory.cn/entry/325107  https://zhuanlan.zhihu.com/p/21492887?refer=tuijiankan

sudo apt-get install  libao-dev libssl-dev git avahi-utils libwww-perl
sudo apt-get install libcrypt-openssl-rsa-perl libio-socket-inet6-perl  libmodule-build-perl

git clone https://github.com/njh/perl-net-sdp.git
cd perl-net-sdp
perl Build.PL
./Build
./Build test
sudo ./Build install
cd ..

git clone https://github.com/abrasive/shairport.git
cd shairport
make