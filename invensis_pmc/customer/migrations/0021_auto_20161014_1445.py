# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-10-14 09:15
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0020_auto_20161010_1504'),
    ]

    operations = [
        migrations.AddField(
            model_name='lead',
            name='lead_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='followup',
            name='lead_status',
            field=models.CharField(blank=True, choices=[('COLD', 'Cold'), ('WARM', 'Warm'), ('HOT', 'Hot'), ('WON', 'Won'), ('LOST', 'Lost')], max_length=20),
        ),
        migrations.AlterField(
            model_name='lead',
            name='latest_lead_status',
            field=models.CharField(blank=True, choices=[('COLD', 'Cold'), ('WARM', 'Warm'), ('HOT', 'Hot'), ('WON', 'Won'), ('LOST', 'Lost')], max_length=20, null=True),
        ),
    ]
