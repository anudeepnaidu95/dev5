# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0020_auto_20160509_1723'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='workitem',
            unique_together=set([('id', 'project_task', 'folder_name', 'file_name')]),
        ),
    ]
