# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-05-01 12:22
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('log', '0005_employeeprofile_avg_rate'),
    ]

    operations = [
        migrations.AddField(
            model_name='business',
            name='tip_methos',
            field=models.CharField(choices=[('P', 'Personal'), ('G', 'Group')], default='G', max_length=1),
        ),
    ]
