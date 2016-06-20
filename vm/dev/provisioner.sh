#!/bin/bash

# basic settings
PGSQL_VERSION=9.4
PYTHON_VERSION=3.4
PROJECT_NAME=quranfalweb
PROJECT_DIR=/home/quran/$PROJECT_NAME
HOME_DIR=/home/vagrant
VENV_DIR=$HOME_DIR/$PROJECT_NAME
VM_NAME=dev
VM_DIR=$PROJECT_DIR/vm/$VM_NAME

#sudo adduser edgleweb www-data

sudo apt-get update -y

# install postgresql and update config files from the project folder
if ! command -v psql; then
	# the latter 2 packages needed for django, and possibly pgAdmin
    sudo apt-get install -y postgresql-$PGSQL_VERSION libpq-dev postgresql-contrib
    
	# conf files
	sudo cp "$VM_DIR/pg_hba.conf" "/etc/postgresql/$PGSQL_VERSION/main/pg_hba.conf"
    sudo cp "$VM_DIR/postgresql-$PGSQL_VERSION.conf" "/etc/postgresql/$PGSQL_VERSION/main/postgresql.conf"

	# create project user and database
	sudo -u postgres psql -c "create database $PROJECT_NAME;" #db needs to be created before debugger installation so to create extension
	sudo -u postgres psql -c "create user $PROJECT_NAME with password '$PROJECT_NAME' superuser;"

    sudo chown ubuntu:ubuntu /etc/hosts
    sudo echo "127.0.0.1 localhost" >> /etc/hosts

	# restart service after config change
	sudo service postgresql restart
else
    printf "\n Database seems to exist. skipping...\n\n"
fi

sudo apt-get install -y git
sudo apt-get install -y python3-setuptools libpq-dev python3-dev build-essential python-virtualenv

if [[ ! -d $VENV_DIR ]]; then
    cd /usr/local/bin
    virtualenv -p python3.4 $VENV_DIR
    cd $VENV_DIR/bin/
    sudo chmod 777 activate
    ./activate
    sudo ./pip3 install --upgrade pip # for a bug in django
    sudo $VENV_DIR/bin/pip3 install -r $VM_DIR/requirements.txt
    echo "export DJANGO_SETTINGS_MODULE=$PROJECT_NAME.settings_production" >> $HOME_DIR/.bashrc
    echo "source $VENV_DIR/bin/activate" >> $HOME_DIR/.bashrc
    echo "cd $PROJECT_DIR" >> $HOME_DIR/.bashrc
else
    source $VENV_DIR/bin/activate
fi

cd $PROJECT_DIR/../django-quran
sudo find . -name '*.pyc' -delete
sudo $VENV_DIR/bin/python3 setup.py install
cd $PROJECT_DIR

# export django settings
export DJANGO_SETTINGS_MODULE=$PROJECT_NAME.settings_production

# migrate
$VENV_DIR/bin/python3 manage.py migrate --settings=quranfalweb.settings_production

# load data
$VENV_DIR/bin/python3 manage.py load_all --settings=quranfalweb.settings_production

# run server
sudo $VENV_DIR/bin/python3 manage.py runserver 0.0.0.0:80 --settings=quranfalweb.settings_production # without sudo cant access port 80
