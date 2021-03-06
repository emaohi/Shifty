# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2018-03-18 22:34
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0032_shiftswap'),
    ]

    operations = [
        migrations.AddField(
            model_name='shiftswap',
            name='requested_shift_id',
            field=models.ForeignKey(default=12, on_delete=django.db.models.deletion.CASCADE, related_name='SwapRequested', to='core.Shift'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='shiftswap',
            name='requester_shift_id',
            field=models.ForeignKey(default='12', on_delete=django.db.models.deletion.CASCADE, related_name='SwapRequesting', to='core.Shift'),
            preserve_default=False,
        ),
    ]
