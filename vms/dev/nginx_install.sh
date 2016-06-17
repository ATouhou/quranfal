#!/usr/bin/env bash

VM_NAME=$1

sudo apt-get update -y
sudo apt-get -y install nginx upstart # upstart for uwsgi
sudo /home/virtualenv/edgleweb/bin/pip install uwsgi
sudo cp /home/edgleweb/vms/$VM_NAME/nginx_edgleweb_config /etc/nginx/sites-available/edgleweb
sudo cp /home/edgleweb/vms/$VM_NAME/uwsgi.conf /etc/init/
sudo ln -s /etc/nginx/sites-available/edgleweb /etc/nginx/sites-enabled
sudo nginx -t #testing
#init-checkconf /etc/init/uwsgi.conf #testing
#does not work, see: http://serverfault.com/questions/740034/what-is-meant-by-sbin-init-too-old
sudo service nginx restart
#sudo start uwsgi #upstart does not work anymore! :(
