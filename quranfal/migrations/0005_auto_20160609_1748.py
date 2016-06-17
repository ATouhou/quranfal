# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-06-09 17:48
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('quran', '0009_word_utextmin'),
        ('quranfal', '0004_auto_20160608_2136'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userword',
            name='word',
        ),
        migrations.AddField(
            model_name='userword',
            name='distinct_word',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='userwords', to='quran.DistinctWord'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='useraya',
            name='aya',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='userayas', to='quran.Aya'),
        ),
    ]