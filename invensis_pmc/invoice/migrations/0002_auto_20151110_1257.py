# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('invoice', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='invoice',
            old_name='amount',
            new_name='total_amount',
        ),
        migrations.RenameField(
            model_name='invoicelineitem',
            old_name='amount',
            new_name='billing_amount_per_unit',
        ),
        migrations.AddField(
            model_name='invoicelineitem',
            name='billing_units',
            field=models.DecimalField(default=0, max_digits=9, decimal_places=2),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='invoicelineitem',
            name='line_amount',
            field=models.DecimalField(default=0, max_digits=9, decimal_places=2),
            preserve_default=True,
        ),
    ]
