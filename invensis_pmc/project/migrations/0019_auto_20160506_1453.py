# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0018_auto_20160506_1130'),
    ]

    operations = [
        migrations.DeleteModel(
            name='ImportWorkItem',
        ),
        migrations.AlterUniqueTogether(
            name='workitem',
            unique_together=None,
        ),
    ]
