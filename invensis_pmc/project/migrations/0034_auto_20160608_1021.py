# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0033_auto_20160608_1009'),
    ]

    operations = [
        migrations.AlterField(
            model_name='qcattribute',
            name='dailytask',
            field=models.ForeignKey(to='project.WorkItemAssignment'  , blank=True, null=True,),
        ),
    ]
