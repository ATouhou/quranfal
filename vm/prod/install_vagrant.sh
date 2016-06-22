#!/usr/bin/env bash

wget https://releases.hashicorp.com/vagrant/1.6.5/vagrant_1.6.5_x86_64.deb
sudo dpkg -i vagrant_1.6.5_x86_64.deb

cd /home/quran/quranfalweb/vm/prod/
vagrant plugin install vagrant-aws
vagrant box add dummy https://github.com/mitchellh/vagrant-aws/raw/master/dummy.box

cp awskey.pem /home/vagrant
chmod 600 /home/vagrant/awskey.pem

