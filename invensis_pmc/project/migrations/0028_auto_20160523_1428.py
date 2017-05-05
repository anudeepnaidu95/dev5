# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0027_auto_20160518_1412'),
    ]

    operations = [
        migrations.AlterField(
            model_name='workitemassignment',
            name='workitem_status',
            field=models.ForeignKey(default=7, to='project.WorkItemStatus'),
        ),
    ]
