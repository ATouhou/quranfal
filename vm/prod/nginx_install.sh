#!/usr/bin/env bash

VM_DIR=$1
VENV_DIR=$2
PROJECT_NAME=$3

sudo apt-get update -y
sudo apt-get -y install nginx upstart # upstart for uwsgi

sudo rm /etc/nginx/sites-enabled/default
sudo cp $VM_DIR/nginx_config /etc/nginx/sites-available/$PROJECT_NAME
sudo ln -s /etc/nginx/sites-available/$PROJECT_NAME /etc/nginx/sites-enabled/$PROJECT_NAME
sudo nginx -t #testing

sudo $VENV_DIR/bin/pip install uwsgi
sudo chmod a+wr -R /home/ubuntu/.cache
sudo cp $VM_DIR/uwsgi.conf /etc/init/
init-checkconf /etc/init/uwsgi.conf #testing

sudo start uwsgi

sudo service nginx restart
