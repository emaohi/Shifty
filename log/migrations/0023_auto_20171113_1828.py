# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-11-13 16:28
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('log', '0022_auto_20171030_1717'),
    ]

    operations = [
        migrations.RenameField(
            model_name='business',
            old_name='start_slot_countdown',
            new_name='slot_request_enabled',
        ),
    ]
