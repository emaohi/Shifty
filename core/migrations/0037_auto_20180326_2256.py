# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2018-03-26 19:56
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('log', '0033_employeeprofile_new_messages'),
        ('core', '0036_auto_20180326_2252'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='shiftswap',
            unique_together=set([('requester', 'requester_shift'), ('requester', 'requested_shift')]),
        ),
    ]