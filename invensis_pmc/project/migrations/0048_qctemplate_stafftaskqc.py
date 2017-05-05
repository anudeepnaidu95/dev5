# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-29 18:20
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0047_auto_20160729_2336'),
    ]

    operations = [
        migrations.CreateModel(
            name='QcTemplate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('qc_attribute_field1', models.CharField(blank=True, max_length=255, null=True)),
                ('qc_attribute_field2', models.CharField(blank=True, max_length=255, null=True)),
                ('qc_attribute_field3', models.CharField(blank=True, max_length=255, null=True)),
                ('qc_attribute_field4', models.CharField(blank=True, max_length=255, null=True)),
                ('qc_attribute_field5', models.CharField(blank=True, max_length=255, null=True)),
                ('qc_attribute_field6', models.CharField(blank=True, max_length=255, null=True)),
                ('qc_attribute_field7', models.CharField(blank=True, max_length=255, null=True)),
                ('qc_attribute_field8', models.CharField(blank=True, max_length=255, null=True)),
                ('qc_attribute_field9', models.CharField(blank=True, max_length=255, null=True)),
                ('qc_attribute_field10', models.CharField(blank=True, max_length=255, null=True)),
                ('qc_attribute_field11', models.CharField(blank=True, max_length=255, null=True)),
                ('qc_attribute_field12', models.CharField(blank=True, max_length=255, null=True)),
                ('qc_attribute_field13', models.CharField(blank=True, max_length=255, null=True)),
                ('qc_attribute_field14', models.CharField(blank=True, max_length=255, null=True)),
                ('qc_attribute_field15', models.CharField(blank=True, max_length=255, null=True)),
                ('qc_attribute_field16', models.CharField(blank=True, max_length=255, null=True)),
                ('qc_attribute_field17', models.CharField(blank=True, max_length=255, null=True)),
                ('qc_attribute_field18', models.CharField(blank=True, max_length=255, null=True)),
                ('qc_attribute_field19', models.CharField(blank=True, max_length=255, null=True)),
                ('qc_attribute_field20', models.CharField(blank=True, max_length=255, null=True)),
                ('qc_attribute_field21', models.CharField(blank=True, max_length=255, null=True)),
                ('qc_attribute_field22', models.CharField(blank=True, max_length=255, null=True)),
                ('qc_attribute_field23', models.CharField(blank=True, max_length=255, null=True)),
                ('qc_attribute_field24', models.CharField(blank=True, max_length=255, null=True)),
                ('qc_attribute_field25', models.CharField(blank=True, max_length=255, null=True)),
                ('qc_attribute_field26', models.CharField(blank=True, max_length=255, null=True)),
                ('qc_attribute_field27', models.CharField(blank=True, max_length=255, null=True)),
                ('qc_attribute_field28', models.CharField(blank=True, max_length=255, null=True)),
                ('qc_attribute_field29', models.CharField(blank=True, max_length=255, null=True)),
                ('qc_attribute_field30', models.CharField(blank=True, max_length=255, null=True)),
                ('service', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='project.Service')),
            ],
        ),
        migrations.CreateModel(
            name='StaffTaskQc',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('qc_attribute1', models.BooleanField(default=False)),
                ('qc_attribute2', models.BooleanField(default=False)),
                ('qc_attribute3', models.BooleanField(default=False)),
                ('qc_attribute4', models.BooleanField(default=False)),
                ('qc_attribute5', models.BooleanField(default=False)),
                ('qc_attribute6', models.BooleanField(default=False)),
                ('qc_attribute7', models.BooleanField(default=False)),
                ('qc_attribute8', models.BooleanField(default=False)),
                ('qc_attribute9', models.BooleanField(default=False)),
                ('qc_attribute10', models.BooleanField(default=False)),
                ('qc_attribute11', models.BooleanField(default=False)),
                ('qc_attribute12', models.BooleanField(default=False)),
                ('qc_attribute13', models.BooleanField(default=False)),
                ('qc_attribute14', models.BooleanField(default=False)),
                ('qc_attribute15', models.BooleanField(default=False)),
                ('qc_attribute16', models.BooleanField(default=False)),
                ('qc_attribute17', models.BooleanField(default=False)),
                ('qc_attribute18', models.BooleanField(default=False)),
                ('qc_attribute19', models.BooleanField(default=False)),
                ('qc_attribute20', models.BooleanField(default=False)),
                ('qc_attribute21', models.BooleanField(default=False)),
                ('qc_attribute22', models.BooleanField(default=False)),
                ('qc_attribute23', models.BooleanField(default=False)),
                ('qc_attribute24', models.BooleanField(default=False)),
                ('qc_attribute25', models.BooleanField(default=False)),
                ('qc_attribute26', models.BooleanField(default=False)),
                ('qc_attribute27', models.BooleanField(default=False)),
                ('qc_attribute28', models.BooleanField(default=False)),
                ('qc_attribute29', models.BooleanField(default=False)),
                ('qc_attribute30', models.BooleanField(default=False)),
                ('staff_task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='project.StaffTask')),
            ],
            options={
                'verbose_name': 'Agent / Artist Task Qc',
                'verbose_name_plural': 'Agent / Artist Task Qc',
            },
        ),
    ]
