# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-06-10 15:03
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quranfal', '0006_auto_20160609_1750'),
    ]

    operations = [
        migrations.RenameField(
            model_name='list',
            old_name='words',
            new_name='distinct_words',
        ),
    ]