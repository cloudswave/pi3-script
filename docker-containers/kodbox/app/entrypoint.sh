#!/bin/sh
set -eu

# version_greater A B returns whether A > B
version_greater() {
    [ "$(printf '%s\n' "$@" | sort -t '.' -n -k1,1 -k2,2 -k3,3 -k4,4 | head -n 1)" != "$1" ]
}

# return true if specified directory is empty
directory_empty() {
    [ -z "$(ls -A "$1/")" ]
}

run_as() {
    if [ "$(id -u)" = 0 ]; then
        su -p www-data -s /bin/sh -c "$1"
    else
        sh -c "$1"
    fi
}

# usage: file_env VAR [DEFAULT]
#    ie: file_env 'XYZ_DB_PASSWORD' 'example'
# (will allow for "$XYZ_DB_PASSWORD_FILE" to fill in the value of
#  "$XYZ_DB_PASSWORD" from a file, especially for Docker's secrets feature)
file_env() {
    local var="$1"
    local fileVar="${var}_FILE"
    local def="${2:-}"
    local varValue=$(env | grep -E "^${var}=" | sed -E -e "s/^${var}=//")
    local fileVarValue=$(env | grep -E "^${fileVar}=" | sed -E -e "s/^${fileVar}=//")
    if [ -n "${varValue}" ] && [ -n "${fileVarValue}" ]; then
        echo >&2 "error: both $var and $fileVar are set (but are exclusive)"
        exit 1
    fi
    if [ -n "${varValue}" ]; then
        export "$var"="${varValue}"
    elif [ -n "${fileVarValue}" ]; then
        export "$var"="$(cat "${fileVarValue}")"
    elif [ -n "${def}" ]; then
        export "$var"="$def"
    fi
    unset "$fileVar"
}

if expr "$1" : "apache2-foreground" 1>/dev/null; then
    if [ -n "${APACHE_DISABLE_REWRITE_IP+x}" ]; then
        a2disconf remoteip
    fi
fi

if expr "$1" : "apache2-foreground" 1>/dev/null || [ "$1" = "php-fpm" ] || [ "${NEXTCLOUD_UPDATE:-0}" -eq 1 ]; then
    if [ -n "${REDIS_HOST+x}" ]; then

        echo "Configuring Redis as session handler"
        {
            echo 'session.save_handler = redis'
            # check if redis host is an unix socket path
            if [ "$(echo "$REDIS_HOST" | cut -c1-1)" = "/" ]; then
              if [ -n "${REDIS_HOST_PASSWORD+x}" ]; then
                echo "session.save_path = \"unix://${REDIS_HOST}?auth=${REDIS_HOST_PASSWORD}\""
              else
                echo "session.save_path = \"unix://${REDIS_HOST}\""
              fi
            # check if redis password has been set
            elif [ -n "${REDIS_HOST_PASSWORD+x}" ]; then
                echo "session.save_path = \"tcp://${REDIS_HOST}:${REDIS_HOST_PORT:=6379}?auth=${REDIS_HOST_PASSWORD}\""
            else
                echo "session.save_path = \"tcp://${REDIS_HOST}:${REDIS_HOST_PORT:=6379}\""
            fi
        } > /usr/local/etc/php/conf.d/redis-session.ini
    fi

    file_env MYSQL_SERVER
    file_env MYSQL_DATABASE
    file_env MYSQL_USER
    file_env MYSQL_PASSWORD
    file_env MYSQL_PORT
    file_env SESSION_TYPE
    file_env SESSION_HOST
    file_env SESSION_PORT
    file_env KODBOX_ADMIN_USER
    file_env KODBOX_ADMIN_PASSWORD

    MYSQL_PORT=${MYSQL_PORT:-3306}
    SESSION_TYPE=${SESSION_PORT:-redis}
    SESSION_PORT=${SESSION_PORT:-6379}


    if [ -n "${MYSQL_DATABASE+x}" ] && [ -n "${MYSQL_USER+x}" ] && [ -n "${MYSQL_PASSWORD+x}" ] && [ ! -f "/usr/src/kodbox/config/setting_user.php" ]; then
            cp /usr/src/kodbox/config/setting_user.example /usr/src/kodbox/config/setting_user.php
            sed -i "s/MYSQL_SERVER/${MYSQL_SERVER}/g" /usr/src/kodbox/config/setting_user.php
            sed -i "s/MYSQL_DATABASE/${MYSQL_DATABASE}/g" /usr/src/kodbox/config/setting_user.php
            sed -i "s/MYSQL_USER/${MYSQL_USER}/g" /usr/src/kodbox/config/setting_user.php
            sed -i "s/MYSQL_PASSWORD/${MYSQL_PASSWORD}/g" /usr/src/kodbox/config/setting_user.php
	    sed -i "s/MYSQL_PORT/${MYSQL_PORT}/g" /usr/src/kodbox/config/setting_user.php
            touch /usr/src/kodbox/data/system/fastinstall.lock

	    if [ -n "${KODBOX_ADMIN_USER+x}" ] && [ -n "${KODBOX_ADMIN_PASSWORD+x}" ]; then
                echo -e "ADM_NAME=${KODBOX_ADMIN_USER}\nADM_PWD=${KODBOX_ADMIN_PASSWORD}" >> /usr/src/kodbox/data/system/fastinstall.lock
            fi
	    if [ -n "${SESSION_HOST+x}" ]; then
                sed -i "s/SESSION_TYPE/${SESSION_TYPE}/g" /usr/src/kodbox/config/setting_user.php
                sed -i "s/SESSION_HOST/${SESSION_HOST}/g" /usr/src/kodbox/config/setting_user.php
                sed -i "s/SESSION_PORT/${SESSION_PORT}/g" /usr/src/kodbox/config/setting_user.php
            else
                sed -i "s/SESSION_TYPE/file/g" /usr/src/kodbox/config/setting_user.php
                sed -i "s/SESSION_HOST/file/g" /usr/src/kodbox/config/setting_user.php
            fi

    fi

#    if version_greater "$image_version" "$installed_version"; then
    if directory_empty "/var/www/html"; then
        if [ "$(id -u)" = 0 ]; then
            rsync_options="-rlDog --chown www-data:root"
        else
            rsync_options="-rlD"
        fi
#        rsync $rsync_options --delete --exclude-from=/upgrade.exclude /usr/src/kodbox/ /var/www/html/
        rsync $rsync_options --delete /usr/src/kodbox/ /var/www/html/
	if [ -n "${KODBOX_ADMIN_USER+x}" ] && [ -n "${KODBOX_ADMIN_PASSWORD+x}" ]; then
            waiting_for_db
            php /var/www/html/index.php "install/index/auto"
            chown -R www-data:root /var/www
        fi
    else
        echo "KODBOX has been configured!"
    fi
fi

exec "$@"
