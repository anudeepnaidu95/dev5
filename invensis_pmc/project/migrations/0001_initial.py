# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
import django_extensions.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0001_initial'),
        ('customer', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='BillingType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=255, verbose_name='title')),
                ('description', models.TextField(null=True, verbose_name='description', blank=True)),
            ],
            options={
                'verbose_name': 'BillingType',
                'verbose_name_plural': 'BillingTypes',
            },
        ),
        migrations.CreateModel(
            name='EmployeeProjectHistory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('start', models.DateTimeField(null=True, verbose_name='start', blank=True)),
                ('end', models.DateTimeField(null=True, verbose_name='end', blank=True)),
                ('employee', models.ForeignKey(to='employee.Employee')),
            ],
            options={
                'verbose_name': 'EmployeeProjectHistory',
                'verbose_name_plural': 'EmployeeProjectHistorys',
            },
        ),
        migrations.CreateModel(
            name='FileStatus',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=255, verbose_name='title')),
                ('description', models.TextField(null=True, verbose_name='description', blank=True)),
            ],
            options={
                'verbose_name': 'FileStatus',
                'verbose_name_plural': 'FileStatuss',
            },
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=255, verbose_name='title')),
                ('description', models.TextField(null=True, verbose_name='description', blank=True)),
                ('slug', django_extensions.db.fields.AutoSlugField(populate_from=b'title', verbose_name='slug', editable=False, blank=True)),
                ('start', models.DateTimeField(null=True, verbose_name='start', blank=True)),
                ('end', models.DateTimeField(null=True, verbose_name='end', blank=True)),
                ('billing_interval', models.SmallIntegerField()),
                ('amount', models.DecimalField(default=0, max_digits=9, decimal_places=2)),
                ('file_path', models.CharField(max_length=1024, null=True, blank=True)),
                ('billing_type', models.ForeignKey(to='project.BillingType')),
                ('customer', models.ForeignKey(to='customer.Customer')),
                ('organization', models.ForeignKey(to='employee.Organization')),
            ],
            options={
                'verbose_name': 'Project',
                'verbose_name_plural': 'Projects',
            },
        ),
        migrations.CreateModel(
            name='ProjectFile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', django_extensions.db.fields.CreationDateTimeField(default=django.utils.timezone.now, verbose_name='created', editable=False, blank=True)),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(default=django.utils.timezone.now, verbose_name='modified', editable=False, blank=True)),
                ('file_name', models.CharField(max_length=1024)),
                ('date', models.DateField()),
                ('project', models.ForeignKey(to='project.Project')),
            ],
            options={
                'verbose_name': 'ProjectFile',
                'verbose_name_plural': 'ProjectFiles',
            },
        ),
        migrations.CreateModel(
            name='ProjectTask',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', django_extensions.db.fields.CreationDateTimeField(default=django.utils.timezone.now, verbose_name='created', editable=False, blank=True)),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(default=django.utils.timezone.now, verbose_name='modified', editable=False, blank=True)),
                ('date', models.DateField()),
                ('employee', models.ForeignKey(to='employee.Employee')),
                ('project', models.ForeignKey(to='project.Project')),
            ],
            options={
                'verbose_name': 'ProjectTask',
                'verbose_name_plural': 'ProjectTasks',
            },
        ),
        migrations.CreateModel(
            name='ProjectTaskFile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('file_name', models.CharField(max_length=1024)),
                ('project_task', models.ForeignKey(to='project.ProjectTask')),
                ('status', models.ForeignKey(to='project.FileStatus')),
            ],
            options={
                'verbose_name': 'ProjectTaskFile',
                'verbose_name_plural': 'ProjectTaskFiles',
            },
        ),
        migrations.AddField(
            model_name='employeeprojecthistory',
            name='project',
            field=models.ForeignKey(to='project.Project'),
        ),
    ]
