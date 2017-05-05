# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0003_auto_20151110_1257'),
        ('project', '0006_auto_20160309_1049'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='workitem',
            name='assignments',
        ),
        migrations.RemoveField(
            model_name='workitemassignment',
            name='agent',
        ),
        migrations.AddField(
            model_name='workitemassignment',
            name='agents',
            field=models.ManyToManyField(related_name=b'+', to='employee.Employee'),
            preserve_default=True,
        ),
    ]
