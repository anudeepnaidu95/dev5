# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0004_remove_employee_role'),
    ]

    operations = [
        migrations.AddField(
            model_name='employee',
            name='roles',
            field=models.ManyToManyField(related_name=b'+', to='employee.Role'),
            preserve_default=True,
        ),
    ]
