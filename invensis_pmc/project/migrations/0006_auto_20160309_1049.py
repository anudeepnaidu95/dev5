# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0003_auto_20151110_1257'),
        ('project', '0005_auto_20151114_1158'),
    ]

    operations = [
        migrations.AddField(
            model_name='workitem',
            name='assignments',
            field=models.ManyToManyField(to='employee.Employee', through='project.WorkItemAssignment'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='workitemassignment',
            name='qc_agent',
            field=models.ForeignKey(related_name=b'+', blank=True, to='employee.Employee', null=True),
            preserve_default=True,
        ),
    ]
