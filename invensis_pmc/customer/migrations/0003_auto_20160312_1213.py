# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
import django_extensions.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0008_auto_20160310_1512'),
        ('project', '0010_auto_20160312_1213'),
        ('customer', '0002_customer_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='Followup',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', django_extensions.db.fields.CreationDateTimeField(default=django.utils.timezone.now, verbose_name='created', editable=False, blank=True)),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(default=django.utils.timezone.now, verbose_name='modified', editable=False, blank=True)),
                ('remarks', models.TextField(null=True, blank=True)),
                ('next_followup', models.DateField(blank=True)),
                ('status', models.CharField(blank=True, max_length=20, choices=[(b'WON', b'Won'), (b'LOST', b'Lost')])),
                ('lead_status', models.CharField(blank=True, max_length=20, choices=[(b'WARM', b'Warm'), (b'HOT', b'Hot'), (b'COLD', b'Cold')])),
                ('percentage', models.PositiveSmallIntegerField(default=0)),
                ('customer', models.ForeignKey(to='customer.Customer')),
            ],
            options={
                'ordering': ('-modified', '-created'),
                'abstract': False,
                'get_latest_by': 'modified',
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='customer',
            name='organization',
        ),
        migrations.AddField(
            model_name='customer',
            name='contact_name',
            field=models.CharField(max_length=100, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='customer',
            name='created',
            field=django_extensions.db.fields.CreationDateTimeField(default=django.utils.timezone.now, verbose_name='created', editable=False, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='customer',
            name='designation',
            field=models.CharField(max_length=100, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='customer',
            name='email',
            field=models.EmailField(max_length=75, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='customer',
            name='industry',
            field=models.ForeignKey(blank=True, to='project.Industry', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='customer',
            name='modified',
            field=django_extensions.db.fields.ModificationDateTimeField(default=django.utils.timezone.now, verbose_name='modified', editable=False, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='customer',
            name='owner',
            field=models.ForeignKey(blank=True, to='employee.Employee', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='customer',
            name='phone',
            field=models.CharField(max_length=50, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='customer',
            name='requirement',
            field=models.TextField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='customer',
            name='services_required',
            field=models.ManyToManyField(to='project.Service'),
            preserve_default=True,
        ),
    ]
