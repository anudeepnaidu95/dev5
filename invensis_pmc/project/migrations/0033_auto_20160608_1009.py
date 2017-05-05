# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0032_normalworkitemassignment_qcworkitemassignment'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='qcattribute',
            name='workitem',
        ),
        migrations.AddField(
            model_name='qcattribute',
            name='dailytask',
            field=models.ForeignKey(blank=True, to='project.WorkItemAssignment', null=True),
            preserve_default=True,
        ),
    ]
