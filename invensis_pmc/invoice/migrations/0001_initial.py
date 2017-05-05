# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0001_initial'),
        ('employee', '0001_initial'),
        ('customer', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Invoice',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('start', models.DateTimeField(null=True, verbose_name='start', blank=True)),
                ('end', models.DateTimeField(null=True, verbose_name='end', blank=True)),
                ('date', models.DateField()),
                ('amount', models.DecimalField(default=0, max_digits=9, decimal_places=2)),
                ('customer', models.ForeignKey(to='customer.Customer')),
                ('project', models.ForeignKey(to='project.Project')),
            ],
            options={
                'verbose_name': 'Invoice',
                'verbose_name_plural': 'Invoices',
            },
        ),
        migrations.CreateModel(
            name='InvoiceLineItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('amount', models.DecimalField(default=0, max_digits=9, decimal_places=2)),
                ('billing_type', models.ForeignKey(to='project.BillingType')),
                ('employee', models.ForeignKey(blank=True, to='employee.Employee', null=True)),
                ('invoice', models.ForeignKey(to='invoice.Invoice')),
            ],
            options={
                'verbose_name': 'InvoiceLineItem',
                'verbose_name_plural': 'InvoiceLineItems',
            },
        ),
    ]
