# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0026_auto_20160514_1631'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='projecttask',
            unique_together=set([('project_service', 'slug'), ('project_service', 'title')]),
        ),
    ]
