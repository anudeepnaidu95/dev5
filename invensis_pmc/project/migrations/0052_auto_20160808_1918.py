# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-08-08 13:48
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0051_auto_20160808_1811'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='sla',
            options={'verbose_name': 'SLA Parameters', 'verbose_name_plural': 'SLA Parameters'},
        ),
        migrations.AddField(
            model_name='servicedocument',
            name='share_with_others',
            field=models.BooleanField(default=False, verbose_name='Share with others'),
        ),
        migrations.AlterField(
            model_name='service',
            name='billing_type',
            field=models.CharField(blank=True, choices=[('per_fte', 'Per FTE'), ('per_hour', 'Per Hour'), ('per_tx', 'Per Transaction')], max_length=20, null=True),
        ),
    ]
