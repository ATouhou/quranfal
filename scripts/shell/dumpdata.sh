#!/usr/bin/env bash

sudo -u postgres pg_dump quranfalweb --schema=public > /home/quran/quranfalweb/data/quranfalweb.sql

#/home/edgleweb/manage.py dumpdata dashboard -o /home/edgleweb/dashboard/fixtures/data.json # exclude=dashboard.Data not in orm
#sudo -u postgres pg_dump edgleweb --table=public.dashboard_data > /home/edgleweb/data/data.sql
