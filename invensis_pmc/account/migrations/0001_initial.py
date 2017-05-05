# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import account.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('added_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('modified_at', models.DateTimeField(auto_now=True, null=True)),
                ('avatar', models.ImageField(max_length=1024, null=True, upload_to=account.models.get_account_file_name, blank=True)),
                ('is_verified', models.BooleanField(default=False)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Request',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('added_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('modified_at', models.DateTimeField(auto_now=True, null=True)),
                ('type', models.SmallIntegerField(choices=[(1, b'Account Verify'), (2, b'Email Change'), (3, b'Password Reset')])),
                ('is_approved', models.BooleanField(default=False)),
                ('activation_key', models.CharField(max_length=64, blank=True)),
                ('key_expires_at', models.DateTimeField(auto_now_add=True)),
                ('str_field_1', models.CharField(max_length=64, null=True, blank=True)),
                ('str_field_2', models.CharField(max_length=64, null=True, blank=True)),
                ('dec_field_1', models.DecimalField(null=True, max_digits=9, decimal_places=2, blank=True)),
                ('dec_field_2', models.DecimalField(null=True, max_digits=9, decimal_places=2, blank=True)),
                ('bool_field_1', models.BooleanField(default=False)),
                ('bool_field_2', models.BooleanField(default=False)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
    ]
