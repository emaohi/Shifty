# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2018-04-20 16:06
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('log', '0033_employeeprofile_new_messages'),
    ]

    operations = [
        migrations.AddField(
            model_name='employeeprofile',
            name='preferred_shit_time_frames',
            field=models.TextField(blank=True, max_length=200, null=True),
        ),
    ]
