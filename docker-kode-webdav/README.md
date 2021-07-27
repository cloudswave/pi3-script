## 简介
网络上基于 docker 的 kodbox 镜像多为 x86 平台所构建的，本项目支持在 aarch64 的平台和 x86 平台构建，该项目的初衷是在树梅派上部署 kodbox 。但本文迟迟未发布，截至本文发布日， `KodCloud-dev` 已 于12 天前发布了一版具有 Dockerfile 构建的项目，见最后的参考，读者可自行测试吧。

## 文件结构简要说明

```bash
|-- kodbox
	|-- app  # kodbox镜像构建及初始化脚本
		|-- Dockerfile  # kodbox 镜像构建文件
		|-- entrypoint.sh
		|-- initdb.d  # 数据库初始化脚本
		|-- mysql_db.txt
		|-- mysql_password.txt  # 数据库密码，请修改
		|-- mysql_user.txt
		|-- setting_user.example
	|-- web
		|-- conf.d  # nginx 配置目录
		|-- nginx.conf  # nginx 主配置文件，定义了日志记录格式
		|-- sslcerts  # ssl 证书及密钥文件目录，替换为自己的
	|-- docker-compose.yml  # 编排文件
```

## 快速使用
```bash
git clone https://github.com/evling2020/kodbox.git
docker-compose build
docker-compose up -d
```



## 参考
- https://github.com/KodCloud-dev/docker
