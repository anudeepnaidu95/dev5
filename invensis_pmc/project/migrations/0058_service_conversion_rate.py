# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-08-18 10:13
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0057_auto_20160818_1532'),
    ]

    operations = [
        migrations.AddField(
            model_name='service',
            name='conversion_rate',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=9),
        ),
    ]