# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-10-19 16:32
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0013_shiftslot_is_mandatory'),
    ]

    operations = [
        migrations.AddField(
            model_name='shiftslot',
            name='name',
            field=models.CharField(blank=True, default='Custom', max_length=30, null=True),
        ),
    ]
