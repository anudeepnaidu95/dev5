# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-08-09 09:07
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0052_auto_20160808_1918'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='leadtask',
            name='filename',
        ),
        migrations.RemoveField(
            model_name='stafftask',
            name='filename',
        ),
        migrations.RemoveField(
            model_name='task',
            name='folderpath',
        ),
    ]