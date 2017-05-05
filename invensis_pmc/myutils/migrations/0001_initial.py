# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-12-16 11:41
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UserAudit',
            fields=[
                ('username', models.CharField(max_length=30, primary_key=True, serialize=False)),
                ('event', models.CharField(choices=[('LOGIN', 'Login'), ('LOGOUT', 'Logout'), ('PWD_CHANGE', 'Password Change')], max_length=20)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('ip_address', models.CharField(max_length=20)),
            ],
        ),
    ]
