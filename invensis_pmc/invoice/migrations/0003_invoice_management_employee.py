# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0003_auto_20151110_1257'),
        ('invoice', '0002_auto_20151110_1257'),
    ]

    operations = [
        migrations.AddField(
            model_name='invoice',
            name='management_employee',
            field=models.ForeignKey(default=None, to='employee.Employee'),
            preserve_default=False,
        ),
    ]
