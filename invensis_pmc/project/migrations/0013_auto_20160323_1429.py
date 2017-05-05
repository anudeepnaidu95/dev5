# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0012_auto_20160323_1401'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='projectplanresource',
            options={'verbose_name': 'ResourcePlan', 'verbose_name_plural': 'ResourcePlans'},
        ),
    ]
