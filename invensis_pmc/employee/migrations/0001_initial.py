# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import mptt.fields
import django_extensions.db.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=255, verbose_name='title')),
                ('description', models.TextField(null=True, verbose_name='description', blank=True)),
                ('slug', django_extensions.db.fields.AutoSlugField(populate_from=b'title', verbose_name='slug', editable=False, blank=True)),
            ],
            options={
                'verbose_name': 'Department',
                'verbose_name_plural': 'Departments',
            },
        ),
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('lft', models.PositiveIntegerField(editable=False, db_index=True)),
                ('rght', models.PositiveIntegerField(editable=False, db_index=True)),
                ('tree_id', models.PositiveIntegerField(editable=False, db_index=True)),
                ('level', models.PositiveIntegerField(editable=False, db_index=True)),
                ('department', models.ForeignKey(to='employee.Department')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='EmployeeGrade',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=255, verbose_name='title')),
                ('description', models.TextField(null=True, verbose_name='description', blank=True)),
            ],
            options={
                'verbose_name': 'EmployeeGrade',
                'verbose_name_plural': 'EmployeeGrades',
            },
        ),
        migrations.CreateModel(
            name='EmployeeType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=255, verbose_name='title')),
                ('description', models.TextField(null=True, verbose_name='description', blank=True)),
            ],
            options={
                'verbose_name': 'EmployeeType',
                'verbose_name_plural': 'EmployeeTypes',
            },
        ),
        migrations.CreateModel(
            name='Organization',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=255, verbose_name='title')),
                ('description', models.TextField(null=True, verbose_name='description', blank=True)),
                ('slug', django_extensions.db.fields.AutoSlugField(populate_from=b'title', verbose_name='slug', editable=False, blank=True)),
            ],
            options={
                'verbose_name': 'Organization',
                'verbose_name_plural': 'Organizations',
            },
        ),
        migrations.CreateModel(
            name='RoleDescription',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=255, verbose_name='title')),
                ('description', models.TextField(null=True, verbose_name='description', blank=True)),
            ],
            options={
                'verbose_name': 'RoleDescription',
                'verbose_name_plural': 'RoleDescriptions',
            },
        ),
        migrations.AddField(
            model_name='employeegrade',
            name='role',
            field=models.ForeignKey(to='employee.RoleDescription'),
        ),
        migrations.AddField(
            model_name='employee',
            name='employee_grade',
            field=models.ForeignKey(to='employee.EmployeeGrade'),
        ),
        migrations.AddField(
            model_name='employee',
            name='employoee_type',
            field=models.ForeignKey(to='employee.EmployeeType'),
        ),
        migrations.AddField(
            model_name='employee',
            name='organization',
            field=models.ForeignKey(to='employee.Organization'),
        ),
        migrations.AddField(
            model_name='employee',
            name='parent',
            field=mptt.fields.TreeForeignKey(related_name='children', blank=True, to='employee.Employee', null=True),
        ),
        migrations.AddField(
            model_name='department',
            name='organization',
            field=models.ForeignKey(to='employee.Organization'),
        ),
    ]
