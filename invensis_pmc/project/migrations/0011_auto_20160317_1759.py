# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0010_auto_20160312_1213'),
    ]

    operations = [
        migrations.AlterField(
            model_name='workitemassignment',
            name='workitem_status',
            field=models.ForeignKey(default=1, to='project.WorkItemStatus'),
        ),
        migrations.AlterUniqueTogether(
            name='workitem',
            unique_together=set([('project_task', 'file_name')]),
        ),
    ]
