# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-10-12 13:43
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0012_delete_tmpholiday'),
    ]

    operations = [
        migrations.AddField(
            model_name='shiftslot',
            name='is_mandatory',
            field=models.BooleanField(default=False),
        ),
    ]
