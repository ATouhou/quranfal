# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-06-09 17:50
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quranfal', '0005_auto_20160609_1748'),
    ]

    operations = [
        migrations.AlterField(
            model_name='useraya',
            name='date',
            field=models.DateField(auto_now_add=True, null=True),
        ),
        migrations.AlterField(
            model_name='userword',
            name='date',
            field=models.DateField(auto_now_add=True, null=True),
        ),
    ]
