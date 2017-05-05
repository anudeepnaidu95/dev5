# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0025_auto_20160514_1511'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='slug',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
    ]
