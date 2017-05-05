# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0037_auto_20160701_1419'),
    ]

    operations = [
        migrations.AlterField(
            model_name='workitemassignment',
            name='time_in_min',
            field=models.CharField(max_length=20, null=True, blank=True),
        ),
    ]
