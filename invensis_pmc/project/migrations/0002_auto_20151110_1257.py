# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
import django_extensions.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0003_auto_20151110_1257'),
        ('project', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='EmployeeAssignment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', django_extensions.db.fields.CreationDateTimeField(default=django.utils.timezone.now, verbose_name='created', editable=False, blank=True)),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(default=django.utils.timezone.now, verbose_name='modified', editable=False, blank=True)),
                ('start', models.DateTimeField(null=True, verbose_name='start', blank=True)),
                ('end', models.DateTimeField(null=True, verbose_name='end', blank=True)),
                ('comments', models.TextField()),
                ('employee', models.ForeignKey(to='employee.Employee')),
                ('experience_slab', models.ForeignKey(to='employee.ExperienceSlab')),
                ('project', models.ForeignKey(to='project.Project')),
            ],
            options={
                'verbose_name': 'EmployeeAssignment',
                'verbose_name_plural': 'EmployeeAssignments',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ProjectPlan',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('project', models.ForeignKey(to='project.Project')),
            ],
            options={
                'verbose_name': 'ProjectPlan',
                'verbose_name_plural': 'ProjectPlans',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ProjectPlanResource',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('number_of_resources', models.SmallIntegerField()),
                ('output_count_per_resource', models.SmallIntegerField()),
                ('experience_slab', models.ForeignKey(to='employee.ExperienceSlab')),
            ],
            options={
                'verbose_name': 'ProjectPlanResource',
                'verbose_name_plural': 'ProjectPlanResources',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ProjectType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=255, verbose_name='title')),
                ('description', models.TextField(null=True, verbose_name='description', blank=True)),
                ('slug', django_extensions.db.fields.AutoSlugField(populate_from=b'title', verbose_name='slug', editable=False, blank=True)),
            ],
            options={
                'verbose_name': 'ProjectType',
                'verbose_name_plural': 'ProjectTypes',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='QcStatus',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=255, verbose_name='title')),
                ('description', models.TextField(null=True, verbose_name='description', blank=True)),
                ('slug', django_extensions.db.fields.AutoSlugField(populate_from=b'title', verbose_name='slug', editable=False, blank=True)),
            ],
            options={
                'verbose_name': 'QcStatus',
                'verbose_name_plural': 'QcStatuss',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='WorkItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', django_extensions.db.fields.CreationDateTimeField(default=django.utils.timezone.now, verbose_name='created', editable=False, blank=True)),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(default=django.utils.timezone.now, verbose_name='modified', editable=False, blank=True)),
                ('file_name', models.CharField(max_length=1024, null=True, blank=True)),
                ('file_path', models.CharField(max_length=1024, null=True, blank=True)),
                ('project_task', models.ForeignKey(to='project.ProjectTask')),
            ],
            options={
                'verbose_name': 'WorkItem',
                'verbose_name_plural': 'WorkItems',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='WorkItemAssignment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', django_extensions.db.fields.CreationDateTimeField(default=django.utils.timezone.now, verbose_name='created', editable=False, blank=True)),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(default=django.utils.timezone.now, verbose_name='modified', editable=False, blank=True)),
                ('start', models.DateTimeField(null=True, verbose_name='start', blank=True)),
                ('end', models.DateTimeField(null=True, verbose_name='end', blank=True)),
                ('is_qc_required', models.NullBooleanField(default=False)),
                ('error_percent', models.SmallIntegerField(null=True, blank=True)),
                ('agent', models.ForeignKey(related_name=b'+', to='employee.Employee')),
                ('lead', models.ForeignKey(related_name=b'+', to='employee.Employee')),
                ('qc_status', models.ForeignKey(blank=True, to='project.QcStatus', null=True)),
                ('workitem', models.ForeignKey(to='project.WorkItem')),
            ],
            options={
                'verbose_name': 'WorkItemAssignment',
                'verbose_name_plural': 'WorkItemAssignments',
            },
            bases=(models.Model,),
        ),
        migrations.RenameModel(
            old_name='FileStatus',
            new_name='WorkItemStatus',
        ),
        migrations.RemoveField(
            model_name='employeeprojecthistory',
            name='employee',
        ),
        migrations.RemoveField(
            model_name='employeeprojecthistory',
            name='project',
        ),
        migrations.DeleteModel(
            name='EmployeeProjectHistory',
        ),
        migrations.RemoveField(
            model_name='projectfile',
            name='project',
        ),
        migrations.DeleteModel(
            name='ProjectFile',
        ),
        migrations.RemoveField(
            model_name='projecttaskfile',
            name='project_task',
        ),
        migrations.RemoveField(
            model_name='projecttaskfile',
            name='status',
        ),
        migrations.DeleteModel(
            name='ProjectTaskFile',
        ),
        migrations.AddField(
            model_name='workitemassignment',
            name='workitem_status',
            field=models.ForeignKey(to='project.WorkItemStatus'),
            preserve_default=True,
        ),
        migrations.AlterModelOptions(
            name='workitemstatus',
            options={'verbose_name': 'WorkItemStatus', 'verbose_name_plural': 'WorkItemStatuss'},
        ),
        migrations.RenameField(
            model_name='project',
            old_name='amount',
            new_name='amount_per_billing_type',
        ),
        migrations.RemoveField(
            model_name='project',
            name='billing_interval',
        ),
        migrations.RemoveField(
            model_name='project',
            name='file_path',
        ),
        migrations.RemoveField(
            model_name='projecttask',
            name='date',
        ),
        migrations.RemoveField(
            model_name='projecttask',
            name='employee',
        ),
        migrations.AddField(
            model_name='project',
            name='billing_interval_in_days',
            field=models.SmallIntegerField(default=0),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='project',
            name='created',
            field=django_extensions.db.fields.CreationDateTimeField(default=django.utils.timezone.now, verbose_name='created', editable=False, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='project',
            name='modified',
            field=django_extensions.db.fields.ModificationDateTimeField(default=django.utils.timezone.now, verbose_name='modified', editable=False, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='project',
            name='number_of_resources',
            field=models.SmallIntegerField(default=0),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='project',
            name='project_type',
            field=models.ForeignKey(blank=True, to='project.ProjectType', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='project',
            name='quality',
            field=models.SmallIntegerField(default=0),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='project',
            name='scope_of_work',
            field=models.TextField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='project',
            name='state_of_procedure',
            field=models.TextField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='project',
            name='turn_around_time_in_hours',
            field=models.SmallIntegerField(default=0),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='projecttask',
            name='customer_ftp_path',
            field=models.CharField(max_length=1024, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='projecttask',
            name='description',
            field=models.TextField(null=True, verbose_name='description', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='projecttask',
            name='end',
            field=models.DateTimeField(null=True, verbose_name='end', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='projecttask',
            name='internal_server_path',
            field=models.CharField(max_length=1024, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='projecttask',
            name='scope_of_work',
            field=models.TextField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='projecttask',
            name='slug',
            field=django_extensions.db.fields.AutoSlugField(default=None, populate_from=b'title', editable=False, blank=True, verbose_name='slug'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='projecttask',
            name='start',
            field=models.DateTimeField(null=True, verbose_name='start', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='projecttask',
            name='title',
            field=models.CharField(default=None, max_length=255, verbose_name='title'),
            preserve_default=False,
        ),
    ]
