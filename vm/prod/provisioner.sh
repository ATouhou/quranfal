#!/bin/bash

PROJECT_NAME=$1
PGSQL_VERSION=9.3
PYTHON_VERSION=3.4
PROJECT_DIR=/home/quran/$PROJECT_NAME
HOME_DIR=/home/ubuntu
VENV_DIR=/home/virtualenv
VM_DIR=$PROJECT_DIR/vm/prod
SETTINGS=quranfalweb.settings_production

printf "================================================ updating system"
sudo apt-get update -y

printf "================================================ install postgresql"
if ! command -v psql; then
    # the latter 2 packages needed for django, and possibly pgAdmin
    sudo apt-get install -y postgresql-$PGSQL_VERSION libpq-dev postgresql-contrib
else
    printf "================================================ database seems to exist. skipping..."
fi

printf "================================================ copying postgresql conf files"
sudo cp "$VM_DIR/pg_hba.conf" "/etc/postgresql/$PGSQL_VERSION/main/pg_hba.conf"
sudo cp "$VM_DIR/postgresql-$PGSQL_VERSION.conf" "/etc/postgresql/$PGSQL_VERSION/main/postgresql.conf"

printf "================================================ create project user and database"
sudo -u postgres psql -c "create database $PROJECT_NAME;"
sudo -u postgres psql -c "create user $PROJECT_NAME with password '$PROJECT_NAME' superuser;"

printf "================================================ adding localhost to /etc/hosts; lacks at aws"
sudo chown ubuntu:ubuntu /etc/hosts
sudo echo "127.0.0.1 localhost" >> /etc/hosts

printf "================================================ restart service after config change"
sudo service postgresql restart

printf "================================================ install git and python"
sudo apt-get install -y git
sudo apt-get install -y python3-setuptools libpq-dev python3-dev build-essential python-virtualenv

printf "================================================ installing and activating virtualenv"
if [[ ! -d $VENV_DIR ]]; then
    cd /usr/local/bin
    virtualenv -p python3.4 $VENV_DIR
    cd $VENV_DIR/bin/
    sudo chmod -R a+rwx $VENV_DIR
    ./activate
    sudo ./pip3 install --upgrade pip # for a bug in django
    sudo $VENV_DIR/bin/pip3 install -r $VM_DIR/requirements.txt
    echo "export DJANGO_SETTINGS_MODULE=$PROJECT_NAME.settings_production" >> $HOME_DIR/.bashrc
    echo "source $VENV_DIR/bin/activate" >> $HOME_DIR/.bashrc
    echo "cd $PROJECT_DIR" >> $HOME_DIR/.bashrc
else
    source $VENV_DIR/bin/activate
fi

printf "================================================ installing django-quran"
cd $PROJECT_DIR/../django-quran
sudo find . -name '*.pyc' -delete
sudo $VENV_DIR/bin/pip3 install -e .
cd $PROJECT_DIR

printf "================================================ collecting static"
$VENV_DIR/bin/python3 manage.py collectstatic --noinput --settings=$SETTINGS

printf "================================================ loading data"
$PROJECT_DIR/scripts/shell/loaddata.sh

printf "================================================ migrating apps"
#$VENV_DIR/bin/python3 manage.py migrate --settings=$SETTINGS

printf "================================================ installing nginx and uwsgi"
source $VM_DIR/nginx_install.sh $VM_DIR $VENV_DIR $PROJECT_NAME
