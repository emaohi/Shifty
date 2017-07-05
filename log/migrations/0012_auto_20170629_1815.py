# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-29 15:15
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('log', '0011_auto_20170629_1813'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employeeprofile',
            name='phone_num',
            field=models.CharField(blank=True, max_length=16, validators=[django.core.validators.RegexValidator(message='Wrong phone number format.', regex='^05d{1}\\-d{7}$')]),
        ),
    ]