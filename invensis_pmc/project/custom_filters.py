# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django import forms

from employee.models import Employee,EmployeeRole,ROLES

from django.contrib.admin import widgets
	

from employee.models import Employee, EmployeeRole
from customer.models import Customer

from  project import models
import django_filters

# QC_STATUS = (



# 	('new','New'),
# 	# ('in_progress','In Progress'),
# 	('completed','Completed'),
# 	# ('on_hold','On Hold'),
# 	# ('cancelled','Cancelled'),
# 	('rejected','Rejected'),


# 	# ('',''),
# 	)
	

class StaffTaskFilter(django_filters.FilterSet):
	staff=django_filters.ModelChoiceFilter(queryset=models.Employee.objects.all())	
	filename = django_filters.CharFilter()
	modified = django_filters.DateTimeFromToRangeFilter('modified', label=('modified date'),lookup_type='contains' )
	class Meta:
		model = models.StaffTask
		fields = ['staff','filename','created','modified']
	
	
class LeadTaskFilter(django_filters.FilterSet):
	lead=django_filters.ModelChoiceFilter(queryset=models.Employee.objects.all())
	filename = django_filters.CharFilter()
	created = django_filters.DateTimeFromToRangeFilter('created', label=('modified date'),lookup_type='contains' )
	class Meta:
		model = models.StaffTask
		#fields = ('no_of_txs_completed',)
		fields = ['lead','filename']


class QcTaskFilter(django_filters.FilterSet):
	qc_lead=django_filters.ModelChoiceFilter(queryset=models.Employee.objects.all())
	filename = django_filters.CharFilter()
	modified = django_filters.DateTimeFromToRangeFilter('modified', label=('modified date'),lookup_type='contains' )
	class Meta:
		model = models.StaffTask
		#fields = ('no_of_txs_completed',)
		fields = ['qc_lead','filename']