# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0009_auto_20160310_1214'),
    ]

    operations = [
        migrations.CreateModel(
            name='ImportWorkItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=255, verbose_name='title')),
                ('description', models.TextField(null=True, verbose_name='description', blank=True)),
                ('csv_file', models.FileField(upload_to=b'')),
                ('project_task', models.ForeignKey(to='project.ProjectTask')),
            ],
            options={
                'verbose_name': 'ImportWorkItem',
                'verbose_name_plural': 'ImportWorkItems',
            },
            bases=(models.Model,),
        ),
        migrations.AlterField(
            model_name='workitemassignment',
            name='agents',
            field=models.ManyToManyField(related_name=b'+', to=b'employee.Employee'),
        ),
    ]
