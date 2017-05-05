# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0024_auto_20160514_1448'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='workitem',
            unique_together=set([('project_task', 'folder_name', 'file_name')]),
        ),
    ]
