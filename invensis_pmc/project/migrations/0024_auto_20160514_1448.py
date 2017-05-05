# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0023_auto_20160514_1429'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='workitem',
            unique_together=None,
        ),
    ]
