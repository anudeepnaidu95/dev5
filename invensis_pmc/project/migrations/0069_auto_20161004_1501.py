# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-10-04 09:31
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0068_auto_20160929_1245'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='qctemplate',
            unique_together=set([('service',)]),
        ),
    ]
