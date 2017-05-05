# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0005_employee_roles'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='roles',
            field=models.ManyToManyField(related_name=b'roles', to=b'employee.Role'),
        ),
    ]
