# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-12-29 09:33
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0022_auto_20161216_1711'),
    ]

    operations = [
        migrations.AlterField(
            model_name='followup',
            name='lead_status',
            field=models.CharField(blank=True, choices=[('PROSPECTING', 'Prospecting'), ('TRIAL', 'Trial'), ('NEGOTIATING', 'Negotiating'), ('WON', 'Won'), ('LOST', 'Lost')], max_length=20),
        ),
        migrations.AlterField(
            model_name='lead',
            name='latest_lead_status',
            field=models.CharField(blank=True, choices=[('PROSPECTING', 'Prospecting'), ('TRIAL', 'Trial'), ('NEGOTIATING', 'Negotiating'), ('WON', 'Won'), ('LOST', 'Lost')], max_length=20, null=True),
        ),
    ]
