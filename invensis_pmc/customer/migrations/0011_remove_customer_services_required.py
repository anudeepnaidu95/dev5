# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-14 14:19
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0010_auto_20160714_1930'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customer',
            name='services_required',
        ),
    ]
