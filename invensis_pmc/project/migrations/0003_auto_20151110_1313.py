# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0002_auto_20151110_1257'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='projectplan',
            name='project',
        ),
        migrations.DeleteModel(
            name='ProjectPlan',
        ),
        migrations.AddField(
            model_name='projectplanresource',
            name='project',
            field=models.ForeignKey(default=None, to='project.Project'),
            preserve_default=False,
        ),
    ]
