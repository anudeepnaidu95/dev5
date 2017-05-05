# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.template.defaultfilters import slugify
from django_extensions.db.models import TitleSlugDescriptionModel, \
	TitleDescriptionModel, TimeStampedModel
from inhouseapp.utils.helpers import unique_slugify
from model_utils.models import TimeFramedModel
from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save

from customer.models import Customer
from employee.models import Employee, ExperienceSlab 
from django.contrib.auth.models import User



CUSTOM_FIELD_DATATYPES = (
	('INTEGER','INTEGER'),
	('STRING','STRING'),
	('DATE','DATE'),
	('DATETME','DATETIME'),
	('DECIMAL','DECIMAL'),
	# ('',''),
	)

class Sla(TitleSlugDescriptionModel):


	class Meta:
		unique_together = ("title",)
		verbose_name = "SLA Parameters"
		verbose_name_plural = "SLA Parameters"

	def __str__(self):
		return self.title
   

class ServiceType(TitleSlugDescriptionModel,TimeStampedModel):

	class Meta:
		unique_together = ("title",)
		verbose_name = "ServiceType"
		verbose_name_plural = "ServiceTypes"

	def __str__(self):
		return self.title

class Industry(TitleSlugDescriptionModel, TimeStampedModel):

	services = models.ManyToManyField(ServiceType)
	
	class Meta:
		unique_together = ("title",)
		verbose_name = "Industry"
		verbose_name_plural = "Industrys"

	def __str__(self):
		return self.title
	


# class Service(TitleSlugDescriptionModel,TimeStampedModel):

# 	class Meta:
# 		verbose_name = "Service"
# 		verbose_name_plural = "Services"

# 	def __str__(self):
# 		return self.title

	

#shd this be an enum ?
# per transaction
# per hour
# per person
class BillingType(TitleDescriptionModel):

	class Meta:
		unique_together = ("title",)
		verbose_name = "BillingType"
		verbose_name_plural = "BillingTypes"

	def __str__(self):
		return self.title
	
# enum ?
# one-time
# on-going

class ProjectType(TitleSlugDescriptionModel):

	class Meta:
		unique_together = ("title",)
		verbose_name = "ProjectType"
		verbose_name_plural = "ProjectTypes"

	def __str__(self):
		return self.title

SHIFT_OPTIONS = (

	('day','Day'),
	('afternoon','Afternoon'),
	('night','Night'),
	

	)


DOCUMENT_TYPES = (
	('nda','NDA'),
	('sla','SLA'),
	('agreement','Agreement'),
	('other','Other'),
	# ('',''),
	# ('',''),
	)	

BILLING_TYPES= (
	('per_fte','Per FTE'),
	('per_hour','Per Hour'),
	('per_tx','Per Transaction'),
	# ('',''),
	# ('',''),
	# ('',''),
	)

DAYS_OF_WEEK = (
	('monday','Monday'),
	('tuesday','Tuesday'),
	('wednesday','Wednesday'),
	('thursday','Thursday'),
	('friday','Friday'),
	('saturday','Saturday'),
	('sunday','Sunday'),
	# ('',''),
	# ('',''),
	)

VOLUME_DURATION_TYPES = (
	('per_day','per Day'),
	('per_week','per Week'),
	('per_month','per Month'),
	# ('',''),
	# ('',''),
	)

# class WorkWeekType(models.Model):
# 	title = models.CharField( max_length=50)
# 	no_of_days = models.PositiveSmallIntegerField(default=0)

# 	class Meta:
# 	    verbose_name = "WorkWeek Type"
# 	    verbose_name_plural = "WorkWeek Types"

# 	def __str__(self):
# 	    return self.title
	

class Service(TitleDescriptionModel, TimeFramedModel, TimeStampedModel):

	# organization = models.ForeignKey(Organization)
	customer =  models.ForeignKey(Customer)
	slug = models.CharField(max_length=255, blank=True , null=True)
	shift_timings = models.CharField(choices=SHIFT_OPTIONS, blank=True, null=True, max_length=20)
	scope_of_work = models.TextField(blank=True,null=True)
	statement_of_procedure = models.TextField(blank=True, null=True)

	project_type = models.ForeignKey(ProjectType, blank=True,null=True)

	# sla related info **********
	# turn_around_time_in_hours = models.SmallIntegerField(default=0)

	# percentage field
	# quality = models.SmallIntegerField(default=0)
	# ***************

	number_of_resources = models.SmallIntegerField(default=0)

	billing_interval_in_days = models.SmallIntegerField(default=0)
	
	# billing_type = models.ForeignKey(BillingType)
	billing_type = models.CharField(choices=BILLING_TYPES, max_length=20, blank=True, null=True)

	amount_per_billing_type = models.DecimalField(verbose_name='Pricing', max_digits=9, decimal_places=2,default=0)




	# project is created by a sales manager role
	# sales_manager = models.ForeignKey(Employee, blank=True,null=True)

	service_type = models.ForeignKey(ServiceType, verbose_name='Service')

	# filter employees of role -ops manager
	operations_manager = models.ForeignKey(Employee)
	created_by = models.ForeignKey(User)
	
	# capture workweek ***
	# workweek_type = models.ForeignKey(WorkWeekType, verbose_name='Work Week Type', blank=True, null=True)
	workweek_days = models.PositiveSmallIntegerField(verbose_name='Operational Days', default=0)
	workweek_start = models.CharField(verbose_name='Work Week Start', choices=DAYS_OF_WEEK, max_length=20, blank=True,null=True)
	workweek_end = models.CharField( verbose_name='Work Week End', choices=DAYS_OF_WEEK, max_length=20, blank=True,null=True)

	# capture daily work hours ***
	daily_work_hours = models.DecimalField(verbose_name='Operational Hours', max_digits=5, decimal_places=2, default=0.0)
	workhours_start = models.TimeField(verbose_name='Work Hours Start' , blank=True, null=True)
	workhours_end = models.TimeField(verbose_name='Work Hours End' , blank=True, null=True)

	# calculated fields ******
	projected_prj_value_per_month = models.DecimalField(verbose_name='Projected Project Value per month', max_digits=9, decimal_places=2, default=0)
	projected_prj_value_per_annum = models.DecimalField(verbose_name='Projected Project Value per annum', max_digits=9, decimal_places=2, default=0)

	# per hour related *******
	no_of_man_hours_per_month = models.IntegerField(verbose_name='Number of man hours per month', default=0)

	# per tx related *****
	tx_volume_duration_type = models.CharField( choices=VOLUME_DURATION_TYPES, verbose_name='Transaction Volume duration type', max_length=20 , blank=True, null=True)
	projected_tx_volume_per_day = models.IntegerField(verbose_name='Projected Transaction Volume per day', default=0)
	projected_tx_volume_per_week = models.IntegerField(verbose_name='Projected Transaction Volume per week', default=0)
	projected_tx_volume_per_month = models.IntegerField(verbose_name='Projected Transaction Volume per month', default=0)

	# calculated field ***
	fte_cost_per_month = models.DecimalField(verbose_name='FTE cost per month', max_digits=9, decimal_places=2, default=0)

	key_notes = models.TextField(verbose_name='Key Notes', blank=True,  null=True)


	encrypt_pricing =models.CharField(blank=True, null=True, max_length=4096)
	encrypt_fte_cost_per_month =models.CharField(blank=True, null=True, max_length=4096)
	encrypt_projected_prj_value_per_month =models.CharField(blank=True, null=True, max_length=4096)
	encrypt_projected_prj_value_per_annum =models.CharField(blank=True, null=True, max_length=4096)

	# conv rate of customer's currency with respect to USD***
	# in UI, we need to show prjected prj value ( both month and annum), ftecost per month in
	# customer's currency as well as usd (these values in readonly fields ).
	# conversion rate shd be retrieved from xe.com using their api
	# and stored here during save
	conversion_rate = models.DecimalField(max_digits=9, decimal_places=2, default=0)


	def save(self, *args, **kwargs):
		if not self.id:
			self.slug = slugify(self.title)
		super(Service, self).save(*args, **kwargs)  

	class Meta:
		unique_together = ("title",)
		verbose_name = "Project Detail"
		verbose_name_plural = "Project Details"

	def __str__(self):
		return self.title
	
# only show for ops mgr
class AssignServiceLead(models.Model):
	service = models.ForeignKey(Service, related_name='+')

	# only lead roles here***
	lead = models.ForeignKey(Employee, related_name='+')

	class Meta:
		verbose_name = "Assign Lead To Service"
		verbose_name_plural = "Assign Lead To Service"

	def __str__(self):
		return str(self.id)

class ServiceDocument(models.Model):
	service = models.ForeignKey(Service, related_name='+')

	document_type = models.CharField(choices=DOCUMENT_TYPES, verbose_name='Document Type', max_length=20, blank=True, null=True)
	document = models.FileField(upload_to='service_documents/', verbose_name='Upload Document')
	
	share_with_others = models.NullBooleanField(verbose_name='Share with others', default=False, blank=True, null=True)
	other_document_type = models.CharField( max_length=255, blank=True, null=True)
	
	class Meta:
		verbose_name = "Upload Document"
		verbose_name_plural = "Upload Documents"

	def __str__(self):
		return str(self.id)
	

class ServiceResourcePlan(models.Model):
	service = models.ForeignKey(Service, related_name='+')
	experience_slab = models.ForeignKey(ExperienceSlab, related_name='+')

	number_of_resources = models.SmallIntegerField(verbose_name='Number of Resources', default=0)

	output_count_per_resource = models.SmallIntegerField(verbose_name='Output Count', default=0)

	class Meta:
		verbose_name = "Resource Plan"
		verbose_name_plural = "Resource Plan"

	def __str__(self):
		return str(self.id)

class ServiceSla(models.Model):
	service = models.ForeignKey(Service, related_name='+')
	sla_type = models.ForeignKey(Sla, verbose_name='Parameters', related_name='+')
	sla_value = models.CharField(verbose_name='Metrics', max_length=255)

	class Meta:
		verbose_name = "ServiceSla"
		verbose_name_plural = "ServiceSlas"

	def __str__(self):
		return str(self.id)

TASK_STATUS = (
	('new','New'),
	# ('in_progress','In Progress'),
	('completed','Completed'),
	# ('on_hold','On Hold'),
	('cancelled','Cancelled'),
	('rejected','Rejected'),
	('pending','Pending'),
	('qc','Quality Check'),

	# ('',''),

	)
class Task(TimeFramedModel, TimeStampedModel):

	title = models.CharField( max_length=255 )
	service = models.ForeignKey(Service, related_name='+', verbose_name='Project Detail')

	# created from title 
	# slug = models.CharField(max_length=255, blank=True , null=True)

	# folderpath = models.FilePathField(max_length=1024, allow_files=False, allow_folders = True, blank=True, null=True)
	# folderpath = models.FileField(max_length=1024,  blank=True, null=True)
	# folderpath = models.FileField(max_length=1024,  blank=True, null=True)
	folderpath = models.CharField(max_length=1024,  blank=True, null=True)

	
	no_of_txs = models.PositiveIntegerField(verbose_name='Number of Transactions', blank=True, null=True, default=0)

	no_of_txs_completed = models.PositiveIntegerField(verbose_name='Number of Transactions completed', blank=True, default=0, null=True)

	# is this required ???
	total_time_hours = models.PositiveIntegerField(blank=True, null=True, default=0)

	scope_of_work = models.TextField(blank=True,null=True)
	
	status = models.CharField(choices=TASK_STATUS, max_length=20, blank=True, null=True, default='new')

	# custom_field1 =models.CharField(max_length=255, blank=True, null=True)
	# custom_field2 =models.CharField(max_length=255, blank=True, null=True)
	# custom_field3 =models.CharField(max_length=255, blank=True, null=True)
	# custom_field4 =models.CharField(max_length=255, blank=True, null=True)
	# custom_field5 =models.CharField(max_length=255, blank=True, null=True)
	# custom_field6 =models.CharField(max_length=255, blank=True, null=True)
	# custom_field7 =models.CharField(max_length=255, blank=True, null=True)
	# custom_field8 =models.CharField(max_length=255, blank=True, null=True)
	# custom_field9 =models.CharField(max_length=255, blank=True, null=True)
	# custom_field10 =models.CharField(max_length=255, blank=True, null=True)

	created_by = models.ForeignKey(User, blank=True, null=True)
	def __str__(self):
		return '%s---%s' %(self.service.title, self.title)

	# def save(self, *args, **kwargs):
	# 	if not self.id:
	# 		self.slug = slugify("%s" %self.title)
	# 	super(Task, self).save(*args, **kwargs)  
		
	class Meta:
		verbose_name = "Task"
		verbose_name_plural = "Tasks"

					
class TaskResourcePlan(models.Model):
	task = models.ForeignKey(Task, related_name='+')
	experience_slab = models.ForeignKey(ExperienceSlab, related_name='+')

	number_of_resources = models.SmallIntegerField(verbose_name='Number of Resources', default=0)

	output_count_per_resource = models.SmallIntegerField(verbose_name='Output Count', default=0)

	class Meta:
		verbose_name = "Resource Plan"
		verbose_name_plural = "Resource Plan"

	def __str__(self):
		return str(self.id)

class TaskTemplate(models.Model):
	service = models.ForeignKey(Service, related_name='+')

	custom_field1_title  = models.CharField(max_length=255, blank=True, null=True)
	custom_field2_title  = models.CharField(max_length=255, blank=True, null=True)
	custom_field3_title  = models.CharField(max_length=255, blank=True, null=True)
	custom_field4_title  = models.CharField(max_length=255, blank=True, null=True)
	custom_field5_title  = models.CharField(max_length=255, blank=True, null=True)
	custom_field6_title  = models.CharField(max_length=255, blank=True, null=True)
	custom_field7_title  = models.CharField(max_length=255, blank=True, null=True)
	custom_field8_title  = models.CharField(max_length=255, blank=True, null=True)
	custom_field9_title  = models.CharField(max_length=255, blank=True, null=True)
	custom_field10_title = models.CharField(max_length=255, blank=True, null=True)

	custom_field1_slug =models.CharField(max_length=255, blank=True, null=True)
	custom_field2_slug =models.CharField(max_length=255, blank=True, null=True)
	custom_field3_slug =models.CharField(max_length=255, blank=True, null=True)
	custom_field4_slug =models.CharField(max_length=255, blank=True, null=True)
	custom_field5_slug =models.CharField(max_length=255, blank=True, null=True)
	custom_field6_slug =models.CharField(max_length=255, blank=True, null=True)
	custom_field7_slug =models.CharField(max_length=255, blank=True, null=True)
	custom_field8_slug =models.CharField(max_length=255, blank=True, null=True)
	custom_field9_slug =models.CharField(max_length=255, blank=True, null=True)
	custom_field10_slug =models.CharField(max_length=255, blank=True, null=True)

	custom_field1_datatype =models.CharField(choices=CUSTOM_FIELD_DATATYPES,max_length=30, blank=True, null=True)
	custom_field2_datatype =models.CharField(choices=CUSTOM_FIELD_DATATYPES,max_length=30, blank=True, null=True)
	custom_field3_datatype =models.CharField(choices=CUSTOM_FIELD_DATATYPES,max_length=30, blank=True, null=True)
	custom_field4_datatype =models.CharField(choices=CUSTOM_FIELD_DATATYPES,max_length=30, blank=True, null=True)
	custom_field5_datatype =models.CharField(choices=CUSTOM_FIELD_DATATYPES,max_length=30, blank=True, null=True)
	custom_field6_datatype =models.CharField(choices=CUSTOM_FIELD_DATATYPES,max_length=30, blank=True, null=True)
	custom_field7_datatype =models.CharField(choices=CUSTOM_FIELD_DATATYPES,max_length=30, blank=True, null=True)
	custom_field8_datatype =models.CharField(choices=CUSTOM_FIELD_DATATYPES,max_length=30, blank=True, null=True)
	custom_field9_datatype =models.CharField(choices=CUSTOM_FIELD_DATATYPES,max_length=30, blank=True, null=True)
	custom_field10_datatype =models.CharField(choices=CUSTOM_FIELD_DATATYPES,max_length=30, blank=True, null=True)

	# @receiver(post_save, sender=Service)
	# def ensure_project_exists(sender, **kwargs):
	# 	if kwargs.get('created', True):
	# 		TaskTemplate.objects.get_or_create(service=kwargs.get('instance'))

class LeadTask( TimeStampedModel):

	# title = models.CharField( max_length=255 )
	task = models.ForeignKey(Task, related_name='+')

	# filter only leads under ops mgr*******
	lead = models.ForeignKey(Employee, related_name='+')

	# created from title 
	# slug = models.CharField(max_length=255, blank=True , null=True)

	# filename = models.FilePathField(max_length=1024, allow_files=True, allow_folders = False, blank=True, null=True)
	# filename = models.FileField(max_length=1024,  blank=True, null=True)
	filename = models.CharField(max_length=1024,  blank=True, null=True)

	no_of_txs = models.PositiveIntegerField(verbose_name='Number of Transactions', blank=True, null=True, default=0)

	no_of_txs_completed = models.PositiveIntegerField(verbose_name='Number of Transactions completed', blank=True, default=0, null=True)

	# is this required ???
	total_time_hours = models.PositiveIntegerField(blank=True, null=True, default=0)
	status = models.CharField(choices=TASK_STATUS, max_length=20, blank=True, null=True, default='new')
	# scope_of_work = models.TextField(blank=True,null=True)

	# custom_field1 =models.CharField(max_length=255, blank=True, null=True)
	# custom_field2 =models.CharField(max_length=255, blank=True, null=True)
	# custom_field3 =models.CharField(max_length=255, blank=True, null=True)
	# custom_field4 =models.CharField(max_length=255, blank=True, null=True)
	# custom_field5 =models.CharField(max_length=255, blank=True, null=True)
	# custom_field6 =models.CharField(max_length=255, blank=True, null=True)
	# custom_field7 =models.CharField(max_length=255, blank=True, null=True)
	# custom_field8 =models.CharField(max_length=255, blank=True, null=True)
	# custom_field9 =models.CharField(max_length=255, blank=True, null=True)
	# custom_field10 =models.CharField(max_length=255, blank=True, null=True)
	created_by = models.ForeignKey(User, blank=True, null=True)
	def __str__(self):
		return '%s---%s' % (self.task, self.filename)

	class Meta:
		verbose_name = "Lead Task"
		verbose_name_plural = "Lead Tasks"


class LeadTaskResourcePlan(models.Model):
	lead_task = models.ForeignKey(LeadTask, related_name='+')
	experience_slab = models.ForeignKey(ExperienceSlab, related_name='+')

	number_of_resources = models.SmallIntegerField(verbose_name='Number of Resources', default=0)

	output_count_per_resource = models.SmallIntegerField(verbose_name='Output Count', default=0)

	class Meta:
		verbose_name = "Lead Task Resource Plan"
		verbose_name_plural = "Lead Task Resource Plan"

	def __str__(self):
		return str(self.id)




QC_STATUS = (
	('new','New'),
	# ('in_progress','In Progress'),
	('completed','Completed'),
	# ('on_hold','On Hold'),
	('cancelled','Cancelled'),
	('rejected','Rejected'),

	# ('',''),
	)

TASK_PRIORITY = (
	(1,'Low',),
	(2,'Medium',),
	(3,'High',),
	# ('','',),
	# ('','',),

	)


class StaffTask( TimeStampedModel):

	# title = models.CharField( max_length=255 )
	lead_task = models.ForeignKey(LeadTask, related_name='+')

	# filter only agents under ops mgr*******
	staff = models.ForeignKey(Employee, verbose_name='Agent / Artist', related_name='+')

	# filename = models.FilePathField(max_length=1024, allow_files=True, allow_folders = False, blank=True, null=True)
	# filename = models.FileField(max_length=1024, blank=True, null=True)
	filename = models.CharField(max_length=1024, blank=True, null=True)

	no_of_txs = models.PositiveIntegerField(verbose_name='Number of Transactions', blank=True, null=True, default=0)

	no_of_txs_completed = models.PositiveIntegerField(verbose_name='Number of Transactions completed', blank=True, default=0, null=True)

	# is this required ???
	total_time_hours = models.PositiveIntegerField(blank=True, null=True, default=0)

	# scope_of_work = models.TextField(blank=True,null=True)

	# custom_field1 =models.CharField(max_length=255, blank=True, null=True)
	# custom_field2 =models.CharField(max_length=255, blank=True, null=True)
	# custom_field3 =models.CharField(max_length=255, blank=True, null=True)
	# custom_field4 =models.CharField(max_length=255, blank=True, null=True)
	# custom_field5 =models.CharField(max_length=255, blank=True, null=True)
	# custom_field6 =models.CharField(max_length=255, blank=True, null=True)
	# custom_field7 =models.CharField(max_length=255, blank=True, null=True)
	# custom_field8 =models.CharField(max_length=255, blank=True, null=True)
	# custom_field9 =models.CharField(max_length=255, blank=True, null=True)
	# custom_field10 =models.CharField(max_length=255, blank=True, null=True)


	# workitem_status = models.ForeignKey(WorkItemStatus, default=workitem_status_default)
	status = models.CharField(choices=TASK_STATUS, max_length=20, blank=True, null=True, default='new')

	time_in_min = models.CharField(blank=True, null=True, max_length=20)

	is_qc_required = models.NullBooleanField(default=False, blank=True,null=True)

	qc_time_in_min = models.CharField(blank=True, null=True, max_length=20)

	is_workedon = models.NullBooleanField(default=False, blank=True,null=True)

	# this field will contain time history for this task
	# s:2016-08-14{{time}};p:timestamp;s:timestamp;c:timestamp;
	time_history = models.TextField(blank=True, null=True)	
	qc_time_history = models.TextField(blank=True, null=True)	

	# add a "quality control" role
	qc_lead = models.ForeignKey(Employee, verbose_name='QC Lead', related_name='+', blank=True, null=True)
	qc_status = models.CharField(choices=QC_STATUS, verbose_name='QC Status', max_length=20, blank=True, null=True)

	# percentage field
	error_percent = models.SmallIntegerField(blank=True,null=True)
	no_of_errors = models.IntegerField(default=0)	
	error_description = models.TextField(blank=True,null=True)

	priority = models.PositiveSmallIntegerField(choices=TASK_PRIORITY)
	created_by = models.ForeignKey(User, blank=True, null=True)
	def __str__(self):
		return '%s' % ( self.filename)

	class Meta:
		verbose_name = "Agent / Artist Task"
		verbose_name_plural = "Agent / Artist Tasks"


class StaffTaskQc(models.Model):
	staff_task = models.ForeignKey(StaffTask, related_name='+')
	qc_attribute1  =  models.BooleanField(default=False)
	qc_attribute2  =  models.BooleanField(default=False)
	qc_attribute3  =  models.BooleanField(default=False)
	qc_attribute4  =  models.BooleanField(default=False)
	qc_attribute5  =  models.BooleanField(default=False)
	qc_attribute6  =  models.BooleanField(default=False)
	qc_attribute7  =  models.BooleanField(default=False)
	qc_attribute8  =  models.BooleanField(default=False)
	qc_attribute9  =  models.BooleanField(default=False)
	qc_attribute10 =  models.BooleanField(default=False)
	qc_attribute11 =  models.BooleanField(default=False)
	qc_attribute12 =  models.BooleanField(default=False)
	qc_attribute13 =  models.BooleanField(default=False)
	qc_attribute14 =  models.BooleanField(default=False)
	qc_attribute15 =  models.BooleanField(default=False)
	qc_attribute16 =  models.BooleanField(default=False)
	qc_attribute17 =  models.BooleanField(default=False)
	qc_attribute18 =  models.BooleanField(default=False)
	qc_attribute19 =  models.BooleanField(default=False)
	qc_attribute20 =  models.BooleanField(default=False)
	qc_attribute21 =  models.BooleanField(default=False)
	qc_attribute22 =  models.BooleanField(default=False)
	qc_attribute23 =  models.BooleanField(default=False)
	qc_attribute24 =  models.BooleanField(default=False)
	qc_attribute25 =  models.BooleanField(default=False)
	qc_attribute26 =  models.BooleanField(default=False)
	qc_attribute27 =  models.BooleanField(default=False)
	qc_attribute28 =  models.BooleanField(default=False)
	qc_attribute29 =  models.BooleanField(default=False)
	qc_attribute30 =  models.BooleanField(default=False)

	class Meta:
		verbose_name = "Agent / Artist Task Qc"
		verbose_name_plural = "Agent / Artist Task Qc"


	@receiver(post_save, sender=StaffTask)
	def ensure_stafftask_exists(sender, **kwargs):
		if kwargs.get('created', True):
			StaffTaskQc.objects.get_or_create(staff_task=kwargs.get('instance'))


				
class QcTemplate(models.Model):
	service   		     =  models.ForeignKey(Service, related_name='+')
	qc_attribute_field1  =  models.CharField(max_length=255, blank=True, null=True)
	qc_attribute_field2  =  models.CharField(max_length=255, blank=True, null=True)
	qc_attribute_field3  =  models.CharField(max_length=255, blank=True, null=True)
	qc_attribute_field4  =  models.CharField(max_length=255, blank=True, null=True)
	qc_attribute_field5  =  models.CharField(max_length=255, blank=True, null=True)
	qc_attribute_field6  =  models.CharField(max_length=255, blank=True, null=True)
	qc_attribute_field7  =  models.CharField(max_length=255, blank=True, null=True)
	qc_attribute_field8  =  models.CharField(max_length=255, blank=True, null=True)
	qc_attribute_field9  =  models.CharField(max_length=255, blank=True, null=True)
	qc_attribute_field10 =  models.CharField(max_length=255, blank=True, null=True)
	qc_attribute_field11 =  models.CharField(max_length=255, blank=True, null=True)
	qc_attribute_field12 =  models.CharField(max_length=255, blank=True, null=True)
	qc_attribute_field13 =  models.CharField(max_length=255, blank=True, null=True)
	qc_attribute_field14 =  models.CharField(max_length=255, blank=True, null=True)
	qc_attribute_field15 =  models.CharField(max_length=255, blank=True, null=True)
	qc_attribute_field16 =  models.CharField(max_length=255, blank=True, null=True)
	qc_attribute_field17 =  models.CharField(max_length=255, blank=True, null=True)
	qc_attribute_field18 =  models.CharField(max_length=255, blank=True, null=True)
	qc_attribute_field19 =  models.CharField(max_length=255, blank=True, null=True)
	qc_attribute_field20 =  models.CharField(max_length=255, blank=True, null=True)
	qc_attribute_field21 =  models.CharField(max_length=255, blank=True, null=True)
	qc_attribute_field22 =  models.CharField(max_length=255, blank=True, null=True)
	qc_attribute_field23 =  models.CharField(max_length=255, blank=True, null=True)
	qc_attribute_field24 =  models.CharField(max_length=255, blank=True, null=True)
	qc_attribute_field25 =  models.CharField(max_length=255, blank=True, null=True)
	qc_attribute_field26 =  models.CharField(max_length=255, blank=True, null=True)
	qc_attribute_field27 =  models.CharField(max_length=255, blank=True, null=True)
	qc_attribute_field28 =  models.CharField(max_length=255, blank=True, null=True)
	qc_attribute_field29 =  models.CharField(max_length=255, blank=True, null=True)
	qc_attribute_field30 =  models.CharField(max_length=255, blank=True, null=True)

	class Meta:
		unique_together = ("service",)



class Project(TitleDescriptionModel, TimeFramedModel, TimeStampedModel):



	# organization = models.ForeignKey(Organization)
	customer =  models.ForeignKey(Customer)
	slug = models.CharField(max_length=255, blank=True , null=True)
	shift_timings = models.CharField(choices=SHIFT_OPTIONS, blank=True, null=True, max_length=20)
	scope_of_work = models.TextField(blank=True,null=True)
	statement_of_procedure = models.TextField(blank=True, null=True)

	project_type = models.ForeignKey(ProjectType, blank=True,null=True)

	turn_around_time_in_hours = models.SmallIntegerField(default=0)

	# percentage field
	quality = models.SmallIntegerField(default=0)

	number_of_resources = models.SmallIntegerField(default=0)

	billing_interval_in_days = models.SmallIntegerField(default=0)
	amount_per_billing_type = models.DecimalField( max_digits=9, decimal_places=2,default=0)
	billing_type = models.ForeignKey(BillingType)

	# file_path = models.CharField( max_length=1024, blank=True, null=True)

	# project is created by a sales manager role
	sales_manager = models.ForeignKey(Employee, blank=True,null=True)



	class Meta:
		verbose_name = "Project"
		verbose_name_plural = "Projects"

	def __str__(self):
		return self.title
	
	def save(self, *args, **kwargs):
		if not self.id:
			self.slug = slugify(self.title)
		super(Project, self).save(*args, **kwargs)  



class ProjectService(models.Model):
	"""servcies required by a project

	"""

	project = models.ForeignKey(Project)

	industry = models.ForeignKey(Industry)
	# service = models.ForeignKey(Service)

	# filter employees of role -ops manager
	operations_manager = models.ForeignKey(Employee)

	class Meta:
		verbose_name = "ProjectService"
		verbose_name_plural = "ProjectServices"

	def __str__(self):
		return '%s' %(self.project.title)
	
# class ProjectPlan(models.Model):
# 	project = models.ForeignKey(Project)


# 	class Meta:
# 	    verbose_name = "ProjectPlan"
# 	    verbose_name_plural = "ProjectPlans"

# 	def __str__(self):
# 	    pass
	
class ProjectPlanResource(models.Model):
	project = models.ForeignKey(Project)
	experience_slab = models.ForeignKey(ExperienceSlab)

	number_of_resources = models.SmallIntegerField()

	output_count_per_resource = models.SmallIntegerField()

	class Meta:
		verbose_name = "ResourcePlan"
		verbose_name_plural = "ResourcePlans"

	def __str__(self):
		return str(self.id)



class ProjectTask(TitleDescriptionModel, TimeFramedModel, TimeStampedModel):

	project = models.ForeignKey(Project, null=True)

	# created from title 
	# unique within a prj service

	slug = models.CharField(max_length=255, blank=True , null=True)
	# project tasks  are for  a particular service
	project_service = models.ForeignKey(ProjectService, blank=True, null=True)

	total_workitems = models.PositiveIntegerField(blank=True, null=True, default=0)

	total_workitems_completed = models.PositiveIntegerField(blank=True, default=0, null=True)

	total_time_hours = models.PositiveIntegerField(blank=True, null=True, default=0)

	# employee =  models.ForeignKey(Employee)
	# date = models.DateField()

	scope_of_work = models.TextField(blank=True,null=True)


	custom_field1 =models.CharField(max_length=255, blank=True, null=True)
	custom_field2 =models.CharField(max_length=255, blank=True, null=True)
	custom_field3 =models.CharField(max_length=255, blank=True, null=True)
	custom_field4 =models.CharField(max_length=255, blank=True, null=True)
	custom_field5 =models.CharField(max_length=255, blank=True, null=True)
	custom_field6 =models.CharField(max_length=255, blank=True, null=True)
	custom_field7 =models.CharField(max_length=255, blank=True, null=True)
	custom_field8 =models.CharField(max_length=255, blank=True, null=True)
	custom_field9 =models.CharField(max_length=255, blank=True, null=True)
	custom_field10 =models.CharField(max_length=255, blank=True, null=True)

	class Meta:
		unique_together = (('project_service', 'slug'),('project_service', 'title'),)
		verbose_name = "ProjectTask"
		verbose_name_plural = "ProjectTasks"

	def __str__(self):
		#return self.title or u''
		return '%s---%s' %(self.project.title, self.title)

	def save(self, *args, **kwargs):
		if not self.id:
			self.slug = slugify("%s" %self.title)
		super(ProjectTask, self).save(*args, **kwargs)  

	def TaskName(self, *args, **kwargs):
		return self.title


	
#shd this be an enum?
#new, assigned, wip, completed, rejected ???
class WorkItemStatus(TitleDescriptionModel):

	class Meta:
		verbose_name = "WorkItemStatus"
		verbose_name_plural = "WorkItemStatuss"

	def __str__(self):
		return self.title


from django.core.exceptions import MultipleObjectsReturned
class WorkItem(TimeStampedModel):
	project_task = models.ForeignKey(ProjectTask)

	# create slug from foldername and filename
	# shd be unique within the prj task
	slug = models.CharField(max_length=1024, blank=True, null=True)

	folder_name = models.CharField(max_length=255, blank=True, null=True)
	file_name = models.CharField(max_length=255, blank=True, null=True)

	number_of_items = models.PositiveIntegerField(blank=True, null=True, default=0)

	number_of_workitems_completed = models.PositiveIntegerField(blank=True, default=0, null=True)
	# date = models.DateField()

	# assignments = models.ManyToManyField(Employee, through='WorkItemAssignment', through_fields=('workitem', 'agent', ))


	custom_field1 =models.CharField(max_length=255, blank=True, null=True)
	custom_field2 =models.CharField(max_length=255, blank=True, null=True)
	custom_field3 =models.CharField(max_length=255, blank=True, null=True)
	custom_field4 =models.CharField(max_length=255, blank=True, null=True)
	custom_field5 =models.CharField(max_length=255, blank=True, null=True)
	custom_field6 =models.CharField(max_length=255, blank=True, null=True)
	custom_field7 =models.CharField(max_length=255, blank=True, null=True)
	custom_field8 =models.CharField(max_length=255, blank=True, null=True)
	custom_field9 =models.CharField(max_length=255, blank=True, null=True)
	custom_field10 =models.CharField(max_length=255, blank=True, null=True)

	class Meta:
		unique_together = (('project_task','folder_name','file_name'),)
		verbose_name = "WorkItem"
		verbose_name_plural = "WorkItems"

	def __str__(self):
		return self.file_name
	

	def save(self, *args, **kwargs):
		if not self.id:
			slug_str = "%s %s " % (self.folder_name, self.file_name) 
			#unique_slugify(self, slug_str) 
			self.slug = slugify("%s" %slug_str)
		super(WorkItem, self).save(*args, **kwargs)  

	def project(self):
		return self.project_task.project


	def projectService(self):
		return self.project_task.project_service


# class ProjectTaskFile(models.Model):

# 	project_task = models.ForeignKey(ProjectTask)
# 	file_name =  models.CharField( max_length=1024)
# 	status =  models.ForeignKey(FileStatus)
# 	class Meta:
# 	    verbose_name = "ProjectTaskFile"
# 	    verbose_name_plural = "ProjectTaskFiles"

# 	def __str__(self):
# 	    return str(self.id)

	
# thru model ?
class EmployeeAssignment(TimeFramedModel, TimeStampedModel):

	employee =  models.ForeignKey(Employee)
	# project = models.ForeignKey(Project)

	experience_slab = models.ForeignKey(ExperienceSlab)
	# oa_experiance_slab = models.TextField(default=True)
	comments = models.TextField()


	class Meta:
		verbose_name = "EmployeeAssignment"
		verbose_name_plural = "EmployeeAssignments"

	def __str__(self):
		return  str(self.id)
# enum
# pass ?
# fail ?
# ...???
# quality check status
class QcStatus(TitleSlugDescriptionModel):


	class Meta:
		verbose_name = "QcStatus"
		verbose_name_plural = "QcStatuss"

	def __str__(self):
		return self.title


class WorkItemAssignment(TimeFramedModel, TimeStampedModel):
	workitem_status_default = 1
	
	workitem = models.ForeignKey(WorkItem)

	lead =  models.ForeignKey(Employee, related_name='+')

	agents = models.ManyToManyField(Employee, related_name='+')
	# agent =  models.ForeignKey(Employee, related_name='+')

	workitem_status = models.ForeignKey(WorkItemStatus, default=workitem_status_default)

	time_in_min = models.CharField(blank=True, null=True, max_length=20)

	is_qc_required = models.NullBooleanField(default=False, blank=True,null=True)

	qc_status = models.ForeignKey(QcStatus, blank=True,null=True)

	# add a "quality control" role
	qc_agent = models.ForeignKey(Employee, related_name='+', blank=True, null=True)

	# percentage field
	error_percent = models.SmallIntegerField(blank=True,null=True)

	class Meta:
		#unique_together = (('id','workitem',),)
		verbose_name = "WorkItemAssignment"
		verbose_name_plural = "WorkItemAssignments"

	def __str__(self):
		return self.workitem.file_name


	def associates(self):
		return " / ".join([a.name for a in self.agents.all()])

	def no_of_items(self):
		return self.workitem.number_of_items

	def no_of_items_completed(self):
		return self.workitem.number_of_workitems_completed


class NormalWorkItemAssignment(WorkItemAssignment):
   
	class Meta:
		proxy = True
		verbose_name = "DailyTask"
		verbose_name_plural = "DailyTasks"
	    # form = WorkItemAssignmentForm

class QcWorkItemAssignment(WorkItemAssignment):
	
	class Meta:
		proxy = True
		verbose_name = "QcAssignment"
		verbose_name_plural = "QcAssignments"

 
class QcAttribute(models.Model):
	dailytask      =  models.ForeignKey(WorkItemAssignment, blank=True,null=True)
	qc_attribute1  =  models.BooleanField(default=False)
	qc_attribute2  =  models.BooleanField(default=False)
	qc_attribute3  =  models.BooleanField(default=False)
	qc_attribute4  =  models.BooleanField(default=False)
	qc_attribute5  =  models.BooleanField(default=False)
	qc_attribute6  =  models.BooleanField(default=False)
	qc_attribute7  =  models.BooleanField(default=False)
	qc_attribute8  =  models.BooleanField(default=False)
	qc_attribute9  =  models.BooleanField(default=False)
	qc_attribute10 =  models.BooleanField(default=False)
	qc_attribute11 =  models.BooleanField(default=False)
	qc_attribute12 =  models.BooleanField(default=False)
	qc_attribute13 =  models.BooleanField(default=False)
	qc_attribute14 =  models.BooleanField(default=False)
	qc_attribute15 =  models.BooleanField(default=False)
	qc_attribute16 =  models.BooleanField(default=False)
	qc_attribute17 =  models.BooleanField(default=False)
	qc_attribute18 =  models.BooleanField(default=False)
	qc_attribute19 =  models.BooleanField(default=False)
	qc_attribute20 =  models.BooleanField(default=False)
	qc_attribute21 =  models.BooleanField(default=False)
	qc_attribute22 =  models.BooleanField(default=False)
	qc_attribute23 =  models.BooleanField(default=False)
	qc_attribute24 =  models.BooleanField(default=False)
	qc_attribute25 =  models.BooleanField(default=False)
	qc_attribute26 =  models.BooleanField(default=False)
	qc_attribute27 =  models.BooleanField(default=False)
	qc_attribute28 =  models.BooleanField(default=False)
	qc_attribute29 =  models.BooleanField(default=False)
	qc_attribute30 =  models.BooleanField(default=False)

	class Meta:
		verbose_name = "QcAttribute"
		verbose_name_plural = "QcAttributes"


	@receiver(post_save, sender=NormalWorkItemAssignment)
	def ensure_workitem_exists(sender, **kwargs):
		#print kwargs
		if kwargs.get('created', True):
			QcAttribute.objects.get_or_create(dailytask=kwargs.get('instance'))


				
class QcAttributeTemplate(models.Model):
	project   		     =  models.ForeignKey(Project)
	qc_attribute_field1  =  models.CharField(max_length=255, blank=True, null=True)
	qc_attribute_field2  =  models.CharField(max_length=255, blank=True, null=True)
	qc_attribute_field3  =  models.CharField(max_length=255, blank=True, null=True)
	qc_attribute_field4  =  models.CharField(max_length=255, blank=True, null=True)
	qc_attribute_field5  =  models.CharField(max_length=255, blank=True, null=True)
	qc_attribute_field6  =  models.CharField(max_length=255, blank=True, null=True)
	qc_attribute_field7  =  models.CharField(max_length=255, blank=True, null=True)
	qc_attribute_field8  =  models.CharField(max_length=255, blank=True, null=True)
	qc_attribute_field9  =  models.CharField(max_length=255, blank=True, null=True)
	qc_attribute_field10 =  models.CharField(max_length=255, blank=True, null=True)
	qc_attribute_field11 =  models.CharField(max_length=255, blank=True, null=True)
	qc_attribute_field12 =  models.CharField(max_length=255, blank=True, null=True)
	qc_attribute_field13 =  models.CharField(max_length=255, blank=True, null=True)
	qc_attribute_field14 =  models.CharField(max_length=255, blank=True, null=True)
	qc_attribute_field15 =  models.CharField(max_length=255, blank=True, null=True)
	qc_attribute_field16 =  models.CharField(max_length=255, blank=True, null=True)
	qc_attribute_field17 =  models.CharField(max_length=255, blank=True, null=True)
	qc_attribute_field18 =  models.CharField(max_length=255, blank=True, null=True)
	qc_attribute_field19 =  models.CharField(max_length=255, blank=True, null=True)
	qc_attribute_field20 =  models.CharField(max_length=255, blank=True, null=True)
	qc_attribute_field21 =  models.CharField(max_length=255, blank=True, null=True)
	qc_attribute_field22 =  models.CharField(max_length=255, blank=True, null=True)
	qc_attribute_field23 =  models.CharField(max_length=255, blank=True, null=True)
	qc_attribute_field24 =  models.CharField(max_length=255, blank=True, null=True)
	qc_attribute_field25 =  models.CharField(max_length=255, blank=True, null=True)
	qc_attribute_field26 =  models.CharField(max_length=255, blank=True, null=True)
	qc_attribute_field27 =  models.CharField(max_length=255, blank=True, null=True)
	qc_attribute_field28 =  models.CharField(max_length=255, blank=True, null=True)
	qc_attribute_field29 =  models.CharField(max_length=255, blank=True, null=True)
	qc_attribute_field30 =  models.CharField(max_length=255, blank=True, null=True)



		
class ProjectTaskTemplate(models.Model):
	project = models.ForeignKey(Project, related_name='+')
	custom_field1_title  = models.CharField(max_length=255, blank=True, null=True)
	custom_field2_title  = models.CharField(max_length=255, blank=True, null=True)
	custom_field3_title  = models.CharField(max_length=255, blank=True, null=True)
	custom_field4_title  = models.CharField(max_length=255, blank=True, null=True)
	custom_field5_title  = models.CharField(max_length=255, blank=True, null=True)
	custom_field6_title  = models.CharField(max_length=255, blank=True, null=True)
	custom_field7_title  = models.CharField(max_length=255, blank=True, null=True)
	custom_field8_title  = models.CharField(max_length=255, blank=True, null=True)
	custom_field9_title  = models.CharField(max_length=255, blank=True, null=True)
	custom_field10_title = models.CharField(max_length=255, blank=True, null=True)

	custom_field1_slug =models.CharField(max_length=255, blank=True, null=True)
	custom_field2_slug =models.CharField(max_length=255, blank=True, null=True)
	custom_field3_slug =models.CharField(max_length=255, blank=True, null=True)
	custom_field4_slug =models.CharField(max_length=255, blank=True, null=True)
	custom_field5_slug =models.CharField(max_length=255, blank=True, null=True)
	custom_field6_slug =models.CharField(max_length=255, blank=True, null=True)
	custom_field7_slug =models.CharField(max_length=255, blank=True, null=True)
	custom_field8_slug =models.CharField(max_length=255, blank=True, null=True)
	custom_field9_slug =models.CharField(max_length=255, blank=True, null=True)
	custom_field10_slug =models.CharField(max_length=255, blank=True, null=True)

	custom_field1_datatype =models.CharField(choices=CUSTOM_FIELD_DATATYPES,max_length=30, blank=True, null=True)
	custom_field2_datatype =models.CharField(choices=CUSTOM_FIELD_DATATYPES,max_length=30, blank=True, null=True)
	custom_field3_datatype =models.CharField(choices=CUSTOM_FIELD_DATATYPES,max_length=30, blank=True, null=True)
	custom_field4_datatype =models.CharField(choices=CUSTOM_FIELD_DATATYPES,max_length=30, blank=True, null=True)
	custom_field5_datatype =models.CharField(choices=CUSTOM_FIELD_DATATYPES,max_length=30, blank=True, null=True)
	custom_field6_datatype =models.CharField(choices=CUSTOM_FIELD_DATATYPES,max_length=30, blank=True, null=True)
	custom_field7_datatype =models.CharField(choices=CUSTOM_FIELD_DATATYPES,max_length=30, blank=True, null=True)
	custom_field8_datatype =models.CharField(choices=CUSTOM_FIELD_DATATYPES,max_length=30, blank=True, null=True)
	custom_field9_datatype =models.CharField(choices=CUSTOM_FIELD_DATATYPES,max_length=30, blank=True, null=True)
	custom_field10_datatype =models.CharField(choices=CUSTOM_FIELD_DATATYPES,max_length=30, blank=True, null=True)

	"""
	def save(self, *args, **kwargs):
		if not self.id:
			# Newly created object, so set slug
			self.custom_field1_slug = slugify(self.custom_field1_title)
			self.custom_field2_slug = slugify(self.custom_field2_title)
			self.custom_field3_slug = slugify(self.custom_field3_title)
			self.custom_field4_slug = slugify(self.custom_field4_title)
			self.custom_field5_slug = slugify(self.custom_field5_title)
			self.custom_field6_slug = slugify(self.custom_field6_title)
			self.custom_field7_slug = slugify(self.custom_field7_title)
			self.custom_field8_slug = slugify(self.custom_field8_title)
			self.custom_field9_slug = slugify(self.custom_field9_title)
			self.custom_field10_slug = slugify(self.custom_field10_title)

		super(ProjectTaskTemplate, self).save(*args, **kwargs)
	"""
	@receiver(post_save, sender=Project)
	def ensure_project_exists(sender, **kwargs):
		#print kwargs
		if kwargs.get('created', True):
			ProjectTaskTemplate.objects.get_or_create(project=kwargs.get('instance'))


class ProjectWorkItemTemplate(models.Model):

	project = models.ForeignKey(Project, related_name='+')
	custom_field1_title =models.CharField(max_length=255, blank=True, null=True)
	custom_field2_title =models.CharField(max_length=255, blank=True, null=True)
	custom_field3_title =models.CharField(max_length=255, blank=True, null=True)
	custom_field4_title =models.CharField(max_length=255, blank=True, null=True)
	custom_field5_title =models.CharField(max_length=255, blank=True, null=True)
	custom_field6_title =models.CharField(max_length=255, blank=True, null=True)
	custom_field7_title =models.CharField(max_length=255, blank=True, null=True)
	custom_field8_title =models.CharField(max_length=255, blank=True, null=True)
	custom_field9_title =models.CharField(max_length=255, blank=True, null=True)
	custom_field10_title =models.CharField(max_length=255, blank=True, null=True)

	custom_field1_slug =models.CharField(max_length=255, blank=True, null=True)
	custom_field2_slug =models.CharField(max_length=255, blank=True, null=True)
	custom_field3_slug =models.CharField(max_length=255, blank=True, null=True)
	custom_field4_slug =models.CharField(max_length=255, blank=True, null=True)
	custom_field5_slug =models.CharField(max_length=255, blank=True, null=True)
	custom_field6_slug =models.CharField(max_length=255, blank=True, null=True)
	custom_field7_slug =models.CharField(max_length=255, blank=True, null=True)
	custom_field8_slug =models.CharField(max_length=255, blank=True, null=True)
	custom_field9_slug =models.CharField(max_length=255, blank=True, null=True)
	custom_field10_slug =models.CharField(max_length=255, blank=True, null=True)

	custom_field1_datatype =models.CharField(choices=CUSTOM_FIELD_DATATYPES,max_length=30, blank=True, null=True)
	custom_field2_datatype =models.CharField(choices=CUSTOM_FIELD_DATATYPES,max_length=30, blank=True, null=True)
	custom_field3_datatype =models.CharField(choices=CUSTOM_FIELD_DATATYPES,max_length=30, blank=True, null=True)
	custom_field4_datatype =models.CharField(choices=CUSTOM_FIELD_DATATYPES,max_length=30, blank=True, null=True)
	custom_field5_datatype =models.CharField(choices=CUSTOM_FIELD_DATATYPES,max_length=30, blank=True, null=True)
	custom_field6_datatype =models.CharField(choices=CUSTOM_FIELD_DATATYPES,max_length=30, blank=True, null=True)
	custom_field7_datatype =models.CharField(choices=CUSTOM_FIELD_DATATYPES,max_length=30, blank=True, null=True)
	custom_field8_datatype =models.CharField(choices=CUSTOM_FIELD_DATATYPES,max_length=30, blank=True, null=True)
	custom_field9_datatype =models.CharField(choices=CUSTOM_FIELD_DATATYPES,max_length=30, blank=True, null=True)
	custom_field10_datatype =models.CharField(choices=CUSTOM_FIELD_DATATYPES,max_length=30, blank=True, null=True)

	"""
	def save(self, *args, **kwargs):
		if not self.id:
			# Newly created object, so set slug
			self.custom_field1_slug = slugify(self.custom_field1_title)
			self.custom_field2_slug = slugify(self.custom_field2_title)
			self.custom_field3_slug = slugify(self.custom_field3_title)
			self.custom_field4_slug = slugify(self.custom_field4_title)
			self.custom_field5_slug = slugify(self.custom_field5_title)
			self.custom_field6_slug = slugify(self.custom_field6_title)
			self.custom_field7_slug = slugify(self.custom_field7_title)
			self.custom_field8_slug = slugify(self.custom_field8_title)
			self.custom_field9_slug = slugify(self.custom_field9_title)
			self.custom_field10_slug = slugify(self.custom_field10_title)

		super(ProjectWorkItemTemplate, self).save(*args, **kwargs)
	"""

	@receiver(post_save, sender=Project)
	def ensure_workitem_template_exists(sender, **kwargs):
		#print kwargs
		if kwargs.get('created', True):
			ProjectWorkItemTemplate.objects.get_or_create(project=kwargs.get('instance'))
