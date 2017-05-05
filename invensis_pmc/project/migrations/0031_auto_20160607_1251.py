# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0030_auto_20160528_1407'),
    ]

    operations = [
        migrations.DeleteModel(
            name='NormalWorkItemAssignment',
        ),
        migrations.DeleteModel(
            name='QcWorkItemAssignment',
        ),
        migrations.AlterModelOptions(
            name='qcattribute',
            options={'verbose_name': 'QcAttribute', 'verbose_name_plural': 'QcAttributes'},
        ),
    ]
