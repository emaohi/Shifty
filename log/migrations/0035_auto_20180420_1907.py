# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2018-04-20 16:07
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('log', '0034_employeeprofile_preferred_shit_time_frames'),
    ]

    operations = [
        migrations.RenameField(
            model_name='employeeprofile',
            old_name='preferred_shit_time_frames',
            new_name='preferred_shift_time_frames',
        ),
    ]
