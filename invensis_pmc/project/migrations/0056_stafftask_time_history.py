# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-08-11 10:56
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0055_auto_20160811_1332'),
    ]

    operations = [
        migrations.AddField(
            model_name='stafftask',
            name='time_history',
            field=models.TextField(blank=True, null=True),
        ),
    ]
