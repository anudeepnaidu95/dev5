# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0015_merge'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProjectTaskTemplate',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('custom_field1_title', models.CharField(max_length=255, null=True, blank=True)),
                ('custom_field2_title', models.CharField(max_length=255, null=True, blank=True)),
                ('custom_field3_title', models.CharField(max_length=255, null=True, blank=True)),
                ('custom_field4_title', models.CharField(max_length=255, null=True, blank=True)),
                ('custom_field5_title', models.CharField(max_length=255, null=True, blank=True)),
                ('custom_field6_title', models.CharField(max_length=255, null=True, blank=True)),
                ('custom_field7_title', models.CharField(max_length=255, null=True, blank=True)),
                ('custom_field8_title', models.CharField(max_length=255, null=True, blank=True)),
                ('custom_field9_title', models.CharField(max_length=255, null=True, blank=True)),
                ('custom_field10_title', models.CharField(max_length=255, null=True, blank=True)),
                ('custom_field1_datatype', models.CharField(blank=True, max_length=30, null=True, choices=[('INTEGER', 'INTEGER'), ('STRING', 'STRING'), ('DATE', 'DATE'), ('DATETME', 'DATETIME'), ('DECIMAL', 'DECIMAL')])),
                ('custom_field2_datatype', models.CharField(blank=True, max_length=30, null=True, choices=[('INTEGER', 'INTEGER'), ('STRING', 'STRING'), ('DATE', 'DATE'), ('DATETME', 'DATETIME'), ('DECIMAL', 'DECIMAL')])),
                ('custom_field3_datatype', models.CharField(blank=True, max_length=30, null=True, choices=[('INTEGER', 'INTEGER'), ('STRING', 'STRING'), ('DATE', 'DATE'), ('DATETME', 'DATETIME'), ('DECIMAL', 'DECIMAL')])),
                ('custom_field4_datatype', models.CharField(blank=True, max_length=30, null=True, choices=[('INTEGER', 'INTEGER'), ('STRING', 'STRING'), ('DATE', 'DATE'), ('DATETME', 'DATETIME'), ('DECIMAL', 'DECIMAL')])),
                ('custom_field5_datatype', models.CharField(blank=True, max_length=30, null=True, choices=[('INTEGER', 'INTEGER'), ('STRING', 'STRING'), ('DATE', 'DATE'), ('DATETME', 'DATETIME'), ('DECIMAL', 'DECIMAL')])),
                ('custom_field6_datatype', models.CharField(blank=True, max_length=30, null=True, choices=[('INTEGER', 'INTEGER'), ('STRING', 'STRING'), ('DATE', 'DATE'), ('DATETME', 'DATETIME'), ('DECIMAL', 'DECIMAL')])),
                ('custom_field7_datatype', models.CharField(blank=True, max_length=30, null=True, choices=[('INTEGER', 'INTEGER'), ('STRING', 'STRING'), ('DATE', 'DATE'), ('DATETME', 'DATETIME'), ('DECIMAL', 'DECIMAL')])),
                ('custom_field8_datatype', models.CharField(blank=True, max_length=30, null=True, choices=[('INTEGER', 'INTEGER'), ('STRING', 'STRING'), ('DATE', 'DATE'), ('DATETME', 'DATETIME'), ('DECIMAL', 'DECIMAL')])),
                ('custom_field9_datatype', models.CharField(blank=True, max_length=30, null=True, choices=[('INTEGER', 'INTEGER'), ('STRING', 'STRING'), ('DATE', 'DATE'), ('DATETME', 'DATETIME'), ('DECIMAL', 'DECIMAL')])),
                ('custom_field10_datatype', models.CharField(blank=True, max_length=30, null=True, choices=[('INTEGER', 'INTEGER'), ('STRING', 'STRING'), ('DATE', 'DATE'), ('DATETME', 'DATETIME'), ('DECIMAL', 'DECIMAL')])),
                ('project', models.ForeignKey(related_name='+', to='project.Project')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ProjectWorkItemTemplate',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('custom_field1_title', models.CharField(max_length=255, null=True, blank=True)),
                ('custom_field2_title', models.CharField(max_length=255, null=True, blank=True)),
                ('custom_field3_title', models.CharField(max_length=255, null=True, blank=True)),
                ('custom_field4_title', models.CharField(max_length=255, null=True, blank=True)),
                ('custom_field5_title', models.CharField(max_length=255, null=True, blank=True)),
                ('custom_field6_title', models.CharField(max_length=255, null=True, blank=True)),
                ('custom_field7_title', models.CharField(max_length=255, null=True, blank=True)),
                ('custom_field8_title', models.CharField(max_length=255, null=True, blank=True)),
                ('custom_field9_title', models.CharField(max_length=255, null=True, blank=True)),
                ('custom_field10_title', models.CharField(max_length=255, null=True, blank=True)),
                ('custom_field1_datatype', models.CharField(blank=True, max_length=30, null=True, choices=[('INTEGER', 'INTEGER'), ('STRING', 'STRING'), ('DATE', 'DATE'), ('DATETME', 'DATETIME'), ('DECIMAL', 'DECIMAL')])),
                ('custom_field2_datatype', models.CharField(blank=True, max_length=30, null=True, choices=[('INTEGER', 'INTEGER'), ('STRING', 'STRING'), ('DATE', 'DATE'), ('DATETME', 'DATETIME'), ('DECIMAL', 'DECIMAL')])),
                ('custom_field3_datatype', models.CharField(blank=True, max_length=30, null=True, choices=[('INTEGER', 'INTEGER'), ('STRING', 'STRING'), ('DATE', 'DATE'), ('DATETME', 'DATETIME'), ('DECIMAL', 'DECIMAL')])),
                ('custom_field4_datatype', models.CharField(blank=True, max_length=30, null=True, choices=[('INTEGER', 'INTEGER'), ('STRING', 'STRING'), ('DATE', 'DATE'), ('DATETME', 'DATETIME'), ('DECIMAL', 'DECIMAL')])),
                ('custom_field5_datatype', models.CharField(blank=True, max_length=30, null=True, choices=[('INTEGER', 'INTEGER'), ('STRING', 'STRING'), ('DATE', 'DATE'), ('DATETME', 'DATETIME'), ('DECIMAL', 'DECIMAL')])),
                ('custom_field6_datatype', models.CharField(blank=True, max_length=30, null=True, choices=[('INTEGER', 'INTEGER'), ('STRING', 'STRING'), ('DATE', 'DATE'), ('DATETME', 'DATETIME'), ('DECIMAL', 'DECIMAL')])),
                ('custom_field7_datatype', models.CharField(blank=True, max_length=30, null=True, choices=[('INTEGER', 'INTEGER'), ('STRING', 'STRING'), ('DATE', 'DATE'), ('DATETME', 'DATETIME'), ('DECIMAL', 'DECIMAL')])),
                ('custom_field8_datatype', models.CharField(blank=True, max_length=30, null=True, choices=[('INTEGER', 'INTEGER'), ('STRING', 'STRING'), ('DATE', 'DATE'), ('DATETME', 'DATETIME'), ('DECIMAL', 'DECIMAL')])),
                ('custom_field9_datatype', models.CharField(blank=True, max_length=30, null=True, choices=[('INTEGER', 'INTEGER'), ('STRING', 'STRING'), ('DATE', 'DATE'), ('DATETME', 'DATETIME'), ('DECIMAL', 'DECIMAL')])),
                ('custom_field10_datatype', models.CharField(blank=True, max_length=30, null=True, choices=[('INTEGER', 'INTEGER'), ('STRING', 'STRING'), ('DATE', 'DATE'), ('DATETME', 'DATETIME'), ('DECIMAL', 'DECIMAL')])),
                ('project', models.ForeignKey(related_name='+', to='project.Project')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='projecttask',
            name='customer_ftp_path',
        ),
        migrations.RemoveField(
            model_name='projecttask',
            name='internal_server_path',
        ),
        migrations.RemoveField(
            model_name='workitem',
            name='file_path',
        ),
        migrations.AddField(
            model_name='projecttask',
            name='custom_field1',
            field=models.CharField(max_length=255, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='projecttask',
            name='custom_field10',
            field=models.CharField(max_length=255, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='projecttask',
            name='custom_field2',
            field=models.CharField(max_length=255, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='projecttask',
            name='custom_field3',
            field=models.CharField(max_length=255, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='projecttask',
            name='custom_field4',
            field=models.CharField(max_length=255, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='projecttask',
            name='custom_field5',
            field=models.CharField(max_length=255, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='projecttask',
            name='custom_field6',
            field=models.CharField(max_length=255, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='projecttask',
            name='custom_field7',
            field=models.CharField(max_length=255, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='projecttask',
            name='custom_field8',
            field=models.CharField(max_length=255, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='projecttask',
            name='custom_field9',
            field=models.CharField(max_length=255, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='projecttask',
            name='project',
            field=models.ForeignKey(to='project.Project', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='projecttask',
            name='total_time_hours',
            field=models.PositiveIntegerField(default=0, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='projecttask',
            name='total_workitems',
            field=models.PositiveIntegerField(default=0, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='projecttask',
            name='total_workitems_completed',
            field=models.PositiveIntegerField(default=0, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='workitem',
            name='custom_field1',
            field=models.CharField(max_length=255, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='workitem',
            name='custom_field10',
            field=models.CharField(max_length=255, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='workitem',
            name='custom_field2',
            field=models.CharField(max_length=255, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='workitem',
            name='custom_field3',
            field=models.CharField(max_length=255, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='workitem',
            name='custom_field4',
            field=models.CharField(max_length=255, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='workitem',
            name='custom_field5',
            field=models.CharField(max_length=255, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='workitem',
            name='custom_field6',
            field=models.CharField(max_length=255, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='workitem',
            name='custom_field7',
            field=models.CharField(max_length=255, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='workitem',
            name='custom_field8',
            field=models.CharField(max_length=255, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='workitem',
            name='custom_field9',
            field=models.CharField(max_length=255, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='workitem',
            name='folder_name',
            field=models.CharField(max_length=255, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='workitem',
            name='number_of_items',
            field=models.PositiveIntegerField(default=0, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='workitem',
            name='number_of_workitems_completed',
            field=models.PositiveIntegerField(default=0, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='workitem',
            name='file_name',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
    ]
