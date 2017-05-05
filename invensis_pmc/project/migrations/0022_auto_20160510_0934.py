# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0021_auto_20160509_1727'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='workitemassignment',
            unique_together=set([('id', 'workitem')]),
        ),
    ]
