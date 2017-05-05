# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0022_auto_20160510_0934'),
    ]

    operations = [
        migrations.AddField(
            model_name='workitem',
            name='slug',
            field=models.CharField(max_length=1024, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='projecttask',
            name='slug',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AlterUniqueTogether(
            name='projecttask',
            unique_together=set([('project_service', 'slug')]),
        ),
        migrations.AlterUniqueTogether(
            name='workitem',
            unique_together=set([('project_task', 'folder_name', 'file_name')]),
        ),
        migrations.AlterUniqueTogether(
            name='workitemassignment',
            unique_together=None,
        ),
    ]
