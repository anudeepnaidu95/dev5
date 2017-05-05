# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0013_auto_20160323_1429'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='normalworkitemassignment',
            options={'verbose_name': 'DailyTask', 'verbose_name_plural': 'DailyTasks'},
        ),
    ]
