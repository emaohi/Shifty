# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2018-03-11 15:32
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('log', '0031_auto_20180301_1932'),
    ]

    operations = [
        migrations.AddField(
            model_name='business',
            name='logo',
            field=models.ImageField(blank=True, null=True, upload_to='logos/'),
        ),
    ]
