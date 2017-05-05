# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0007_auto_20160309_1106'),
    ]

    operations = [
        migrations.CreateModel(
            name='NormalWorkItemAssignment',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=('project.workitemassignment',),
        ),
        migrations.CreateModel(
            name='QcWorkItemAssignment',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=('project.workitemassignment',),
        ),
    ]
