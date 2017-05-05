# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0008_auto_20160310_1512'),
        ('customer', '0008_auto_20160621_1223'),
    ]

    operations = [
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('code', models.CharField(max_length=3)),
            ],
            options={
                'verbose_name': 'Country',
                'verbose_name_plural': 'Countrys',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='customer',
            name='addressline1',
            field=models.CharField(max_length=255, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='customer',
            name='addressline2',
            field=models.CharField(max_length=255, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='customer',
            name='city',
            field=models.CharField(max_length=255, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='customer',
            name='country',
            field=models.ForeignKey(blank=True, to='customer.Country', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='customer',
            name='sales_rep',
            field=models.ForeignKey(related_name='+', blank=True, to='employee.Employee', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='customer',
            name='state',
            field=models.CharField(max_length=255, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='customer',
            name='zip_code',
            field=models.CharField(max_length=20, null=True, blank=True),
            preserve_default=True,
        ),
    ]
