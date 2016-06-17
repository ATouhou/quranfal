#!/usr/bin/env bash

VM_DIR=$1
VENV_DIR=$2
PROJECT_NAME=$3

sudo apt-get update -y
sudo apt-get -y install nginx upstart # upstart for uwsgi

sudo cp $VM_DIR/nginx_config /etc/nginx/sites-available/$PROJECT_NAME
sudo ln -s /etc/nginx/sites-available/$PROJECT_NAME /etc/nginx/sites-enabled
sudo nginx -t #testing

sudo $VENV_DIR/bin/pip install uwsgi
#init-checkconf /etc/init/uwsgi.conf #testing
#does not work, see: http://serverfault.com/questions/740034/what-is-meant-by-sbin-init-too-old
sudo service nginx restart
#sudo start uwsgi #upstart does not work anymore! :(
