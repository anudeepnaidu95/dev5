# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0005_auto_20160330_1154'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='customer',
            options={'verbose_name': 'Enquiry', 'verbose_name_plural': 'Customers'},
        ),
        migrations.AddField(
            model_name='customer',
            name='is_converted_to_customer',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='customer',
            name='lead_source',
            field=models.CharField(blank=True, max_length=20, null=True, choices=[('web', 'Web'), ('sales-team', 'Sales Team'), ('reference', 'Reference'), ('other', 'Other')]),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='customer',
            name='other_lead_source',
            field=models.CharField(max_length=100, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='followup',
            name='remarks',
            field=models.TextField(null=True, verbose_name='Notes', blank=True),
        ),
    ]
