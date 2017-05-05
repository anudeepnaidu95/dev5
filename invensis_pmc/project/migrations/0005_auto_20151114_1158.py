# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
import django_extensions.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0003_auto_20151110_1257'),
        ('project', '0004_auto_20151110_1321'),
    ]

    operations = [
        migrations.CreateModel(
            name='Industry',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', django_extensions.db.fields.CreationDateTimeField(default=django.utils.timezone.now, verbose_name='created', editable=False, blank=True)),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(default=django.utils.timezone.now, verbose_name='modified', editable=False, blank=True)),
                ('title', models.CharField(max_length=255, verbose_name='title')),
                ('description', models.TextField(null=True, verbose_name='description', blank=True)),
                ('slug', django_extensions.db.fields.AutoSlugField(populate_from=b'title', verbose_name='slug', editable=False, blank=True)),
            ],
            options={
                'verbose_name': 'Industry',
                'verbose_name_plural': 'Industrys',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ProjectService',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('industry', models.ForeignKey(to='project.Industry')),
                ('operations_manager', models.ForeignKey(to='employee.Employee')),
                ('project', models.ForeignKey(to='project.Project')),
            ],
            options={
                'verbose_name': 'ProjectService',
                'verbose_name_plural': 'ProjectServices',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', django_extensions.db.fields.CreationDateTimeField(default=django.utils.timezone.now, verbose_name='created', editable=False, blank=True)),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(default=django.utils.timezone.now, verbose_name='modified', editable=False, blank=True)),
                ('title', models.CharField(max_length=255, verbose_name='title')),
                ('description', models.TextField(null=True, verbose_name='description', blank=True)),
                ('slug', django_extensions.db.fields.AutoSlugField(populate_from=b'title', verbose_name='slug', editable=False, blank=True)),
            ],
            options={
                'verbose_name': 'Service',
                'verbose_name_plural': 'Services',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='projectservice',
            name='service',
            field=models.ForeignKey(to='project.Service'),
            preserve_default=True,
        ),
        migrations.RemoveField(
            model_name='projecttask',
            name='project',
        ),
        migrations.AddField(
            model_name='project',
            name='sales_manager',
            field=models.ForeignKey(blank=True, to='employee.Employee', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='projecttask',
            name='project_service',
            field=models.ForeignKey(blank=True, to='project.ProjectService', null=True),
            preserve_default=True,
        ),
    ]
