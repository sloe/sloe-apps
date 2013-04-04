#!/bin/bash

yum_cache="-C"
installpath=`dirname "$0"`
wssloepath=`dirname "$installpath"`
sitepath=`dirname "$wssloepath"`
echo "Sitepath=$sitepath"

fusionfile=rpmfusion-free-release-6-1.noarch.rpm
if [ ! -f "/tmp/$fusionfile" ] ; then
  wget "http://download1.rpmfusion.org/free/el/updates/6/x86_64/$fusionfile" --output-document="/tmp/$fusionfile"
  yum_cache=
fi

rpm -ivh "/tmp/$fusionfile"

epelfile=epel-release-6-8.noarch.rpm
if [ ! -f "/tmp/$epelfile" ] ; then
  wget "http://mirror01.th.ifl.net/epel/6/x86_64/$epelfile" --output-document="/tmp/$epelfile"
  yum_cache=
fi

rpm -ivh "/tmp/$epelfile"

nginxfile=nginx-release-centos-6-0.el6.ngx.noarch.rpm
if [ ! -f "/tmp/$nginxfile" ] ; then
  wget "http://nginx.org/packages/centos/6/noarch/RPMS/$nginxfile" --output-document="/tmp/$nginxfile"
  yum_cache=
fi

rpm -ivh "/tmp/$nginxfile"

yum install -y $yum_cache php php-mbstring php-mysql php-fpm nginx phpMyAdmin GraphicsMagick ffmpeg
chkconfig php-fpm on
chkconfig nginx on

file="/etc/php-fpm.d/www.conf"
fileorig="$file.orig"
if [ ! -f "$fileorig" ] ; then
  echo Taking pristine backup of $file to $fileorig
  cp "$file" "$fileorig"
fi
cp "$fileorig" "$file"
cat "$installpath/php-fpm/www.conf.append" >> "$file"

file=/etc/nginx/nginx.conf
fileorig=/etc/nginx/nginx.conf.orig
if [ ! -f "$fileorig" ] ; then
  echo Taking pristine backup of $file to $fileorig
  cp "$file" "$fileorig"
fi
cp "$fileorig" "$file"
cat "$installpath/nginx/nginx.conf.append" >> "$file"

cp "$installpath/nginx/sloe.conf" /etc/nginx/sloe.conf
cp "$installpath/nginx/sloe-http.conf" /etc/nginx/conf.d/sloe-http.conf
default="/etc/nginx/conf.d/default.conf"

if [ -f "$default" ] ; then
  disabled="/etc/nginx/conf.d.disabled"
  echo Moving nginx default.conf to $disabled
  mkdir "$disabled"
  mv "$default" "$disabled"
fi

if [ ! -L "$sitepath/sql_admin" ] ; then
  echo "Symlinking $sitepath/sql_admin to /usr/share/phpMyAdmin"
  ln -s /usr/share/phpMyAdmin "$sitepath/sql_admin"
fi

service php-fpm restart
service nginx restart


