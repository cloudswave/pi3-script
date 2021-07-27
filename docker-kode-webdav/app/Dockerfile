# https://www.evling.me/
FROM php:7.4-fpm-alpine3.12

LABEL maintainer="evling2020@gmail.com"
ENV KODBOX_VERSION=1.14

# entrypoint.sh and cron.sh dependencies
RUN echo @testing http://mirrors.ustc.edu.cn/alpine/edge/testing >> /etc/apk/repositories && \
    sed -i 's/dl-cdn.alpinelinux.org/mirrors.ustc.edu.cn/g' /etc/apk/repositories && \
    echo /etc/apk/respositories && \
    apk update && apk upgrade &&\
    apk add --no-cache \
            imagemagick \
                ffmpeg \
            unzip \
        rsync \
        unrar \
        tzdata && \
        cp /usr/share/zoneinfo/Asia/Shanghai /etc/localtime && \
        echo "Asia/Shanghai" > /etc/timezone

# install the PHP extensions we need
# see https://docs.nextcloud.com/server/stable/admin_manual/installation/source_installation.html
RUN set -ex; \
    \
    apk add --no-cache --virtual .build-deps \
        $PHPIZE_DEPS \
        autoconf \
        freetype-dev \
        icu-dev \
        libevent-dev \
        libjpeg-turbo-dev \
        libmcrypt-dev \
        libpng-dev \
        libmemcached-dev \
        libxml2-dev \
        libzip-dev \
        openldap-dev \
        pcre-dev \
        postgresql-dev \
        imagemagick-dev \
        libwebp-dev \
        gmp-dev \
    ; \
    \
    docker-php-ext-configure gd --with-freetype --with-jpeg --with-webp; \
    docker-php-ext-configure ldap; \
    docker-php-ext-install -j "$(nproc)" \
            mysqli \
        bcmath \
        exif \
        gd \
        intl \
        ldap \
        opcache \
        pcntl \
        pdo_mysql \
        pdo_pgsql \
        zip \
        gmp \
    ; \
    \
# pecl will claim success even if one install fails, so we need to perform each install separately
    pecl install APCu-5.1.18; \
    pecl install memcached-3.1.5; \
    pecl install redis-5.3.1; \
    pecl install imagick-3.4.4; \
    \
    docker-php-ext-enable \
        apcu \
        memcached \
        redis \
        imagick \
    ; \
    \
    runDeps="$( \
        scanelf --needed --nobanner --format '%n#p' --recursive /usr/local/lib/php/extensions \
            | tr ',' '\n' \
            | sort -u \
            | awk 'system("[ -e /usr/local/lib/" $1 " ]") == 0 { next } { print "so:" $1 }' \
    )"; \
    apk del tzdata .build-deps

# set recommended PHP.ini settings
# see https://docs.nextcloud.com/server/12/admin_manual/configuration_server/server_tuning.html#enable-php-opcache
RUN { \
        echo 'opcache.enable=1'; \
        echo 'opcache.interned_strings_buffer=8'; \
        echo 'opcache.max_accelerated_files=10000'; \
        echo 'opcache.memory_consumption=128'; \
        echo 'opcache.save_comments=1'; \
        echo 'opcache.revalidate_freq=1'; \
                echo 'post_max_size=10G'; \
                echo 'upload_max_filesize=10G'; \
                echo 'max_execution_time=3600'; \
    } > /usr/local/etc/php/conf.d/opcache-recommended.ini; \
    \
    echo 'apc.enable_cli=1' >> /usr/local/etc/php/conf.d/docker-php-ext-apcu.ini; \
    \
    echo 'memory_limit=512M' > /usr/local/etc/php/conf.d/memory-limit.ini; \
    \
    mkdir /var/www/data; \
    chown -R www-data:root /var/www; \
    chmod -R g=u /var/www

VOLUME /var/www/html

ADD setting_user.example /usr/src/kodbox/config/setting_user.example
RUN set -ex; \
    apk add --no-cache --virtual .fetch-deps \
        bzip2 \
        gnupg \
    ; \
    \
    curl -fsSL -o kodbox.zip \
        "http://static.kodcloud.com/update/download/kodbox.${KODBOX_VERSION}.zip"; \
    export GNUPGHOME="$(mktemp -d)"; \
    unzip -d /usr/src/kodbox kodbox.zip; \
    cp /usr/bin/unrar /usr/src/kodbox/app/sdks/archiveLib/bin/rar; \
    sed -i "s/'chunkSize'                       => 0.5,/'chunkSize'                     => 5,/g" /usr/src/kodbox/config/setting.php;\
    gpgconf --kill all; \
    apk del .fetch-deps

COPY entrypoint.sh /
RUN chmod +x /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]
CMD ["php-fpm"]
