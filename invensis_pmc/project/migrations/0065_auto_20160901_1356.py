# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-09-01 08:26
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0064_auto_20160830_1609'),
    ]

    operations = [
        migrations.AddField(
            model_name='stafftask',
            name='qc_time_history',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='stafftask',
            name='qc_time_in_min',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
