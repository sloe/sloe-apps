#!/bin/bash

cd /tmp
installpath=`dirname "$0"`

yum install -y ImageMagick php-mbstring php-mysql php-fpm
chkconfig php-fpm on

#wget http://nginx.org/packages/centos/6/noarch/RPMS/nginx-release-centos-6-0.el6.ngx.noarch.rpm
#rpm -ivh nginx-release-centos-6-0.el6.ngx.noarch.rpm
#yum install -y nginx
#chkconfig nginx on

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
service php-fpm restart
service nginx restart


