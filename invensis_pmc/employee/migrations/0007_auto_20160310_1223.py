# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0006_auto_20160310_1214'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='roles',
            field=models.ManyToManyField(related_name=b'emp_role', to=b'employee.Role'),
        ),
    ]
