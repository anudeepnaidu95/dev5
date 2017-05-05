# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0003_auto_20160312_1213'),
    ]

    operations = [
        migrations.AlterField(
            model_name='followup',
            name='lead_status',
            field=models.CharField(blank=True, max_length=20, choices=[(b'COLD', b'Cold'), (b'WARM', b'Warm'), (b'HOT', b'Hot')]),
        ),
    ]
