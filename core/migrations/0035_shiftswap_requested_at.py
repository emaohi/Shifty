# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2018-03-26 19:47
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0034_auto_20180319_0046'),
    ]

    operations = [
        migrations.AddField(
            model_name='shiftswap',
            name='requested_at',
            field=models.DateTimeField(auto_now_add=True),
            preserve_default=False,
        ),
    ]
