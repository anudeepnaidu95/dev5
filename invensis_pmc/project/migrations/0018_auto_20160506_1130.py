# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0017_auto_20160505_1222'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='importworkitem',
            name='description',
        ),
        migrations.RemoveField(
            model_name='importworkitem',
            name='project_task',
        ),
        migrations.RemoveField(
            model_name='importworkitem',
            name='title',
        ),
    ]
