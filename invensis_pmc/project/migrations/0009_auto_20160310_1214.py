# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0008_normalworkitemassignment_qcworkitemassignment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='workitemassignment',
            name='agents',
            field=models.ManyToManyField(related_name=b'employee_agents', to=b'employee.Employee'),
        ),
    ]
