# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hr', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='employeeleave',
            name='end',
            field=models.DateTimeField(null=True, verbose_name='end', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='employeeleave',
            name='start',
            field=models.DateTimeField(null=True, verbose_name='start', blank=True),
            preserve_default=True,
        ),
    ]
