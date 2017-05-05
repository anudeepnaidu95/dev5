# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0031_auto_20160607_1251'),
    ]

    operations = [
        migrations.CreateModel(
            name='NormalWorkItemAssignment',
            fields=[
            ],
            options={
                'verbose_name': 'DailyTask',
                'proxy': True,
                'verbose_name_plural': 'DailyTasks',
            },
            bases=('project.workitemassignment',),
        ),
        migrations.CreateModel(
            name='QcWorkItemAssignment',
            fields=[
            ],
            options={
                'verbose_name': 'QcAssignment',
                'proxy': True,
                'verbose_name_plural': 'QcAssignments',
            },
            bases=('project.workitemassignment',),
        ),
    ]
