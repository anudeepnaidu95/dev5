# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0004_auto_20160316_1206'),
    ]

    operations = [
        migrations.AlterField(
            model_name='followup',
            name='percentage',
            field=models.CharField(blank=True, max_length=10, choices=[(b'10', b'10'), (b'20', b'20'), (b'30', b'30'), (b'40', b'40'), (b'50', b'50'), (b'60', b'60'), (b'70', b'70'), (b'80', b'80'), (b'90', b'90'), (b'100', b'100')]),
        ),
    ]
