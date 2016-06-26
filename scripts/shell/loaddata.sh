#!/usr/bin/env bash


cat "/home/quran/quranfalweb/data/quranfalweb.sql" | sudo -i -u postgres psql quranfalweb

#/home/edgleweb/manage.py loaddata /home/edgleweb/dashboard/fixtures/data.json
#cat "/home/edgleweb/data/data.sql" | sudo -i -u postgres psql edgleweb


