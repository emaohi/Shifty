# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2018-03-18 22:46
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0033_auto_20180319_0034'),
    ]

    operations = [
        migrations.RenameField(
            model_name='shiftswap',
            old_name='requested_shift_id',
            new_name='requested_shift',
        ),
        migrations.RenameField(
            model_name='shiftswap',
            old_name='requester_shift_id',
            new_name='requester_shift',
        ),
    ]