# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-14 14:00
from __future__ import unicode_literals

from django.db import migrations
import django_extensions.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('hr', '0002_auto_20151111_0417'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='created',
            field=django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created'),
        ),
        migrations.AlterField(
            model_name='notification',
            name='modified',
            field=django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified'),
        ),
    ]
