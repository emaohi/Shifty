# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-12-25 14:28
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0018_auto_20171225_1528'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employeerequest',
            name='sent_time',
            field=models.DateTimeField(),
        ),
    ]
