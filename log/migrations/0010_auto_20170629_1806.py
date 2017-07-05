# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-29 15:06
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('log', '0009_employeeprofile_enable_mailing'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employeeprofile',
            name='phone_num',
            field=models.CharField(blank=True, max_length=16, validators=[django.core.validators.RegexValidator(message='Wrong phone number format.', regex='^\\+?1?\\d{9,15}$')]),
        ),
    ]
