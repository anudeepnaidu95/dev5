# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0003_auto_20151110_1313'),
    ]

    operations = [
        migrations.RenameField(
            model_name='project',
            old_name='state_of_procedure',
            new_name='statement_of_procedure',
        ),
    ]
