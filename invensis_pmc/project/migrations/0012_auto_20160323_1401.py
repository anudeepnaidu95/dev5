# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0011_auto_20160317_1759'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='normalworkitemassignment',
            options={'verbose_name': 'Daily Assignment', 'verbose_name_plural': 'Daily Assignments'},
        ),
        migrations.AlterModelOptions(
            name='qcworkitemassignment',
            options={'verbose_name': 'QcAssignment', 'verbose_name_plural': 'QcAssignments'},
        ),
    ]
