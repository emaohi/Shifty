# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2018-04-01 09:55
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0038_auto_20180328_1701'),
    ]

    operations = [
        migrations.AddField(
            model_name='shiftswap',
            name='employee_request',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='swap_request', to='core.EmployeeRequest'),
        ),
    ]
