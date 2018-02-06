# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2018-02-06 10:19
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('log', '0024_employeeprofile_menu_score'),
        ('core', '0021_auto_20180129_1002'),
    ]

    operations = [
        migrations.CreateModel(
            name='Shift',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_tips', models.IntegerField(blank=True, null=True)),
                ('remarks', models.TextField(blank=True, max_length=200, null=True)),
                ('employees', models.ManyToManyField(related_name='shifts', to='log.EmployeeProfile')),
                ('slot', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.ShiftSlot')),
            ],
        ),
        migrations.AlterField(
            model_name='employeerequest',
            name='sent_time',
            field=models.DateTimeField(default=datetime.datetime(2018, 2, 6, 12, 19, 27, 691971)),
        ),
    ]
