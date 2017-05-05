# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
import django_extensions.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0001_initial'),
        ('customer', '0001_initial'),
        ('employee', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Conversation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', django_extensions.db.fields.CreationDateTimeField(default=django.utils.timezone.now, verbose_name='created', editable=False, blank=True)),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(default=django.utils.timezone.now, verbose_name='modified', editable=False, blank=True)),
                ('body', models.TextField(null=True, blank=True)),
                ('customer', models.ForeignKey(blank=True, to='customer.Customer', null=True)),
                ('employee', models.ForeignKey(blank=True, to='employee.Employee', null=True)),
            ],
            options={
                'verbose_name': 'Conversation',
                'verbose_name_plural': 'Conversations',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Query',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', django_extensions.db.fields.CreationDateTimeField(default=django.utils.timezone.now, verbose_name='created', editable=False, blank=True)),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(default=django.utils.timezone.now, verbose_name='modified', editable=False, blank=True)),
                ('subject', models.CharField(max_length=255, null=True, blank=True)),
                ('customer', models.ForeignKey(to='customer.Customer')),
                ('project', models.ForeignKey(to='project.Project')),
            ],
            options={
                'verbose_name': 'Query',
                'verbose_name_plural': 'Querys',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='QueryStatus',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=255, verbose_name='title')),
                ('description', models.TextField(null=True, verbose_name='description', blank=True)),
            ],
            options={
                'verbose_name': 'QueryStatus',
                'verbose_name_plural': 'QueryStatuss',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='query',
            name='query_status',
            field=models.ForeignKey(to='support.QueryStatus'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='query',
            name='task',
            field=models.ForeignKey(to='project.ProjectTask'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='conversation',
            name='query',
            field=models.ForeignKey(to='support.Query'),
            preserve_default=True,
        ),
    ]
