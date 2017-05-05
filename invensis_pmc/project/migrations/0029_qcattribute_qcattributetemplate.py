# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0028_auto_20160523_1428'),
    ]

    operations = [
        migrations.CreateModel(
            name='QcAttribute',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('qc_attribute1', models.CharField(max_length=255, null=True, blank=True)),
                ('qc_attribute2', models.CharField(max_length=255, null=True, blank=True)),
                ('qc_attribute3', models.CharField(max_length=255, null=True, blank=True)),
                ('qc_attribute4', models.CharField(max_length=255, null=True, blank=True)),
                ('qc_attribute5', models.CharField(max_length=255, null=True, blank=True)),
                ('qc_attribute6', models.CharField(max_length=255, null=True, blank=True)),
                ('qc_attribute7', models.CharField(max_length=255, null=True, blank=True)),
                ('qc_attribute8', models.CharField(max_length=255, null=True, blank=True)),
                ('qc_attribute9', models.CharField(max_length=255, null=True, blank=True)),
                ('qc_attribute10', models.CharField(max_length=255, null=True, blank=True)),
                ('qc_attribute11', models.CharField(max_length=255, null=True, blank=True)),
                ('qc_attribute12', models.CharField(max_length=255, null=True, blank=True)),
                ('qc_attribute13', models.CharField(max_length=255, null=True, blank=True)),
                ('qc_attribute14', models.CharField(max_length=255, null=True, blank=True)),
                ('qc_attribute15', models.CharField(max_length=255, null=True, blank=True)),
                ('qc_attribute16', models.CharField(max_length=255, null=True, blank=True)),
                ('qc_attribute17', models.CharField(max_length=255, null=True, blank=True)),
                ('qc_attribute18', models.CharField(max_length=255, null=True, blank=True)),
                ('qc_attribute19', models.CharField(max_length=255, null=True, blank=True)),
                ('qc_attribute20', models.CharField(max_length=255, null=True, blank=True)),
                ('qc_attribute21', models.CharField(max_length=255, null=True, blank=True)),
                ('qc_attribute22', models.CharField(max_length=255, null=True, blank=True)),
                ('qc_attribute23', models.CharField(max_length=255, null=True, blank=True)),
                ('qc_attribute24', models.CharField(max_length=255, null=True, blank=True)),
                ('qc_attribute25', models.CharField(max_length=255, null=True, blank=True)),
                ('qc_attribute26', models.CharField(max_length=255, null=True, blank=True)),
                ('qc_attribute27', models.CharField(max_length=255, null=True, blank=True)),
                ('qc_attribute28', models.CharField(max_length=255, null=True, blank=True)),
                ('qc_attribute29', models.CharField(max_length=255, null=True, blank=True)),
                ('qc_attribute30', models.CharField(max_length=255, null=True, blank=True)),
                ('workitem', models.ForeignKey(to='project.WorkItemAssignment')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='QcAttributeTemplate',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('qc_attribute_field1', models.CharField(max_length=255, null=True, blank=True)),
                ('qc_attribute_field2', models.CharField(max_length=255, null=True, blank=True)),
                ('qc_attribute_field3', models.CharField(max_length=255, null=True, blank=True)),
                ('qc_attribute_field4', models.CharField(max_length=255, null=True, blank=True)),
                ('qc_attribute_field5', models.CharField(max_length=255, null=True, blank=True)),
                ('qc_attribute_field6', models.CharField(max_length=255, null=True, blank=True)),
                ('qc_attribute_field7', models.CharField(max_length=255, null=True, blank=True)),
                ('qc_attribute_field8', models.CharField(max_length=255, null=True, blank=True)),
                ('qc_attribute_field9', models.CharField(max_length=255, null=True, blank=True)),
                ('qc_attribute_field10', models.CharField(max_length=255, null=True, blank=True)),
                ('qc_attribute_field11', models.CharField(max_length=255, null=True, blank=True)),
                ('qc_attribute_field12', models.CharField(max_length=255, null=True, blank=True)),
                ('qc_attribute_field13', models.CharField(max_length=255, null=True, blank=True)),
                ('qc_attribute_field14', models.CharField(max_length=255, null=True, blank=True)),
                ('qc_attribute_field15', models.CharField(max_length=255, null=True, blank=True)),
                ('qc_attribute_field16', models.CharField(max_length=255, null=True, blank=True)),
                ('qc_attribute_field17', models.CharField(max_length=255, null=True, blank=True)),
                ('qc_attribute_field18', models.CharField(max_length=255, null=True, blank=True)),
                ('qc_attribute_field19', models.CharField(max_length=255, null=True, blank=True)),
                ('qc_attribute_field20', models.CharField(max_length=255, null=True, blank=True)),
                ('qc_attribute_field21', models.CharField(max_length=255, null=True, blank=True)),
                ('qc_attribute_field22', models.CharField(max_length=255, null=True, blank=True)),
                ('qc_attribute_field23', models.CharField(max_length=255, null=True, blank=True)),
                ('qc_attribute_field24', models.CharField(max_length=255, null=True, blank=True)),
                ('qc_attribute_field25', models.CharField(max_length=255, null=True, blank=True)),
                ('qc_attribute_field26', models.CharField(max_length=255, null=True, blank=True)),
                ('qc_attribute_field27', models.CharField(max_length=255, null=True, blank=True)),
                ('qc_attribute_field28', models.CharField(max_length=255, null=True, blank=True)),
                ('qc_attribute_field29', models.CharField(max_length=255, null=True, blank=True)),
                ('qc_attribute_field30', models.CharField(max_length=255, null=True, blank=True)),
                ('project', models.ForeignKey(to='project.Project')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
