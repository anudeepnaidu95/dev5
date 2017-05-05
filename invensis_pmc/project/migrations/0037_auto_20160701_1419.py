# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0036_remove_project_organization'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='shift_timings',
            field=models.CharField(blank=True, max_length=20, null=True, choices=[('day', 'Day'), ('afternoon', 'Afternoon'), ('night', 'Night')]),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='workitemassignment',
            name='time_in_min',
            field=models.PositiveIntegerField(default=0, null=True, blank=True),
            preserve_default=True,
        ),
    ]
