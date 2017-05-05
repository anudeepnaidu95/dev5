# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
import django_extensions.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0002_employee_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='ExperienceSlab',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', django_extensions.db.fields.CreationDateTimeField(default=django.utils.timezone.now, verbose_name='created', editable=False, blank=True)),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(default=django.utils.timezone.now, verbose_name='modified', editable=False, blank=True)),
                ('title', models.CharField(max_length=255, verbose_name='title')),
                ('description', models.TextField(null=True, verbose_name='description', blank=True)),
                ('slug', django_extensions.db.fields.AutoSlugField(populate_from=b'title', verbose_name='slug', editable=False, blank=True)),
            ],
            options={
                'verbose_name': 'ExperienceSlab',
                'verbose_name_plural': 'ExperienceSlabs',
            },
            bases=(models.Model,),
        ),
        migrations.RenameModel(
            old_name='RoleDescription',
            new_name='Role',
        ),
        migrations.RemoveField(
            model_name='employeegrade',
            name='role',
        ),
        migrations.AlterModelOptions(
            name='role',
            options={'verbose_name': 'Role', 'verbose_name_plural': 'Roles'},
        ),
        migrations.RemoveField(
            model_name='employee',
            name='employee_grade',
        ),
        migrations.DeleteModel(
            name='EmployeeGrade',
        ),
        migrations.RemoveField(
            model_name='employee',
            name='employoee_type',
        ),
        migrations.DeleteModel(
            name='EmployeeType',
        ),
        migrations.AddField(
            model_name='employee',
            name='role',
            field=models.ForeignKey(blank=True, to='employee.Role', null=True),
            preserve_default=True,
        ),
    ]
