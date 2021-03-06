# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-11-16 09:00
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('invoice', '0004_auto_20161010_1504'),
    ]

    operations = [
        migrations.CreateModel(
            name='InvoiceSetup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company_name', models.CharField(blank=True, max_length=255, null=True)),
                ('addressline1', models.CharField(blank=True, max_length=255, null=True)),
                ('addressline2', models.CharField(blank=True, max_length=255, null=True)),
                ('city', models.CharField(blank=True, max_length=50, null=True)),
                ('state', models.CharField(blank=True, max_length=50, null=True)),
                ('country', models.CharField(blank=True, max_length=50, null=True)),
                ('pincode', models.CharField(blank=True, max_length=50, null=True)),
                ('phone', models.CharField(blank=True, max_length=50, null=True)),
                ('email', models.CharField(blank=True, max_length=255, null=True)),
            ],
            options={
                'verbose_name': 'InvoiceSetup',
                'verbose_name_plural': 'InvoiceSetups',
            },
        ),
        migrations.CreateModel(
            name='PaymentTerms',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('terms', models.CharField(max_length=1024)),
                ('invoice_setup', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='invoice.InvoiceSetup')),
            ],
            options={
                'verbose_name': 'PaymentTerms',
                'verbose_name_plural': 'PaymentTermss',
            },
        ),
        migrations.CreateModel(
            name='WireTransferInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('beneficiary_name', models.CharField(blank=True, max_length=255, null=True)),
                ('bank_name', models.CharField(blank=True, max_length=255, null=True)),
                ('routing_number', models.CharField(blank=True, max_length=255, null=True)),
                ('account_number', models.CharField(blank=True, max_length=255, null=True)),
                ('swift_id', models.CharField(blank=True, max_length=50, null=True)),
                ('invoice_setup', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='invoice.InvoiceSetup')),
            ],
            options={
                'verbose_name': 'WireTransferInfo',
                'verbose_name_plural': 'WireTransferInfos',
            },
        ),
    ]
