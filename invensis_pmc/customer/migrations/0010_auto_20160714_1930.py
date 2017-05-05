# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-14 14:00
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_extensions.db.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('project', '0039_auto_20160714_1930'),
        ('employee', '0009_auto_20160714_1930'),
        ('customer', '0009_auto_20160625_1147'),
    ]

    operations = [
        migrations.CreateModel(
            name='Lead',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('title', models.CharField(max_length=255, verbose_name='Company Name')),
                ('description', models.CharField(blank=True, max_length=255, null=True)),
                ('contact_name', models.CharField(blank=True, max_length=100, null=True)),
                ('designation', models.CharField(blank=True, max_length=100, null=True)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('phone', models.CharField(blank=True, max_length=50, null=True)),
                ('addressline1', models.CharField(blank=True, max_length=255, null=True)),
                ('addressline2', models.CharField(blank=True, max_length=255, null=True)),
                ('city', models.CharField(blank=True, max_length=255, null=True)),
                ('zip_code', models.CharField(blank=True, max_length=20, null=True)),
                ('state', models.CharField(blank=True, max_length=255, null=True)),
                ('requirement', models.TextField(blank=True, null=True)),
                ('lead_source', models.CharField(blank=True, choices=[('web', 'Web'), ('sales-team', 'Sales Team'), ('reference', 'Reference'), ('other', 'Other')], max_length=20, null=True)),
                ('other_lead_source', models.CharField(blank=True, max_length=100, null=True)),
                ('is_converted_to_customer', models.BooleanField(default=False)),
                ('country', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='customer.Country')),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('industry', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='project.Industry')),
                ('owner', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='employee.Employee')),
                ('sales_rep', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to='employee.Employee')),
            ],
            options={
                'verbose_name': 'Enquiry',
                'verbose_name_plural': 'Enquiries',
            },
        ),
        migrations.AlterModelOptions(
            name='customer',
            options={'verbose_name': 'Customer', 'verbose_name_plural': 'Customers'},
        ),
        migrations.RemoveField(
            model_name='customer',
            name='is_converted_to_customer',
        ),
        migrations.RemoveField(
            model_name='customer',
            name='user',
        ),
        migrations.RemoveField(
            model_name='followup',
            name='customer',
        ),
        migrations.RemoveField(
            model_name='followup',
            name='status',
        ),
        migrations.AddField(
            model_name='customer',
            name='created_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='followup',
            name='is_converted_to_customer',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='customer',
            name='created',
            field=django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created'),
        ),
        migrations.AlterField(
            model_name='customer',
            name='description',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='customer',
            name='email',
            field=models.EmailField(blank=True, max_length=254, null=True),
        ),
        migrations.AlterField(
            model_name='customer',
            name='modified',
            field=django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified'),
        ),
        migrations.AlterField(
            model_name='customer',
            name='title',
            field=models.CharField(max_length=255, verbose_name='Company Name'),
        ),
        migrations.AlterField(
            model_name='followup',
            name='created',
            field=django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created'),
        ),
        migrations.AlterField(
            model_name='followup',
            name='modified',
            field=django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified'),
        ),
        migrations.AddField(
            model_name='followup',
            name='lead',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='customer.Lead'),
        ),
    ]