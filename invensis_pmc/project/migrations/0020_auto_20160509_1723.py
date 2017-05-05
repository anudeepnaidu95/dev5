# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0019_auto_20160506_1453'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='workitem',
            unique_together=set([('project_task', 'folder_name', 'file_name')]),
        ),
    ]
