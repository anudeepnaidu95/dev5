# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-09-14 12:52
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0065_auto_20160901_1356'),
    ]

    operations = [
        migrations.AddField(
            model_name='servicedocument',
            name='other_document_type',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
