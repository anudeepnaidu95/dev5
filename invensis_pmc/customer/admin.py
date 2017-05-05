# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import admin
from django.contrib.auth.models import User
from employee.models import Employee
from .models import Customer, Followup, Country, Lead
from .forms import CustomerForm,FollowupForm, FollowupAdminForm, LeadForm

from import_export import fields,resources, formats
from import_export.widgets import ForeignKeyWidget,ManyToManyWidget, DateWidget
from import_export.admin import ImportExportModelAdmin, ImportMixin, ImportExportMixin
from import_export.admin import DEFAULT_FORMATS
from project.models import Industry, ServiceType
from employee.models import Employee



class CountryWidget(ForeignKeyWidget):
	def clean(self, value, row=None):
		return self.model.objects.get(name__icontains = value)

class IndustryWidget(ForeignKeyWidget):
	def clean(self, value, row=None):
		return self.model.objects.get(title__icontains = value)

class ServicesWidget(ManyToManyWidget):
	def clean(self, value, row=None):
		return self.model.objects.filter(title__icontains = value)

class CustomerResource(resources.ModelResource):

	country = fields.Field(column_name='country', attribute='country',
						widget=CountryWidget(Country, field='name'))

	industry = fields.Field(column_name='industry', attribute='industry',
						widget=ForeignKeyWidget(Industry, field='title'))

	services = fields.Field(column_name='services', attribute='services',
						widget=ServicesWidget(ServiceType,field='title', separator="/"))

	owner = fields.Field(column_name='owner', attribute='owner',
					   widget=ForeignKeyWidget(Employee, 'name'))

	sales_rep = fields.Field(column_name='sales_rep', attribute='sales_rep',
					   widget=ForeignKeyWidget(Employee, 'name'))

	lead_date = fields.Field(column_name='lead_date', attribute='lead_date',
						widget=DateWidget(format="%d-%m-%Y"))

	class Meta:
		model = Lead
		skip_unchanged = True
		report_skipped = True

		import_id_fields = ('title',)
		fields = ('title','contact_name','email', 'phone','city', 'state', 'country', 'requirement', 'industry','services', 'lead_date','lead_source','latest_lead_status','sales_rep','owner')
		export_order = ('title','contact_name','email', 'phone', 'city', 'state', 'country', 'requirement', 'industry','services','lead_date','lead_source','latest_lead_status','sales_rep','owner')


class FollowupInline(admin.TabularInline):

	model = Followup
	extra = 1
	form = FollowupForm
	#suit_classes = 'suit-tab suit-tab-followup'

	list_display = (
	
		'next_followup',
		'lead_status',
		'percentage',
		# 'status' ,
		'remarks',

	)
	list_filter = (
		'lead_status',
		)


class LeadAdmin(ImportExportMixin, admin.ModelAdmin):
	inlines = (FollowupInline,)
	resource_class = CustomerResource
	form = LeadForm

	fieldsets = [
		('Enquiry', {
			#'classes': ('suit-tab', 'suit-tab-customer',),
			'fields': ['title','description']
		}),
		('Contact Person', {
			#'classes': ('suit-tab', 'suit-tab-customer',),
			'fields': ['contact_name','designation','email','phone',]}),

		('Address', {
			#'classes': ('suit-tab', 'suit-tab-customer',),
			'fields': ['country','state','city','addressline1','addressline2','zip_code']}),

		('Lead Source', {
			#'classes': ('suit-tab', 'suit-tab-customer',),
			'fields': ['lead_source', 'sales_rep','other_lead_source',]}),

		('Requirements', {
			#'classes': ('suit-tab', 'suit-tab-customer',),
			'fields': ['industry','requirement',]}),

		('Sales Manager', {
			#'classes': ('suit-tab', 'suit-tab-customer',),
			'fields': ['owner',]}),

	]

	#suit_form_tabs = (('customer', 'Customer'), ('followup', 'Followup'))
	#exclude_fields = ['user']


	list_display = (
		 'title',
		#'description',
		#'id' ,
		'contact_name',
		'designation',
		'email',
		'phone',
		'country',
		'state',
		'industry',
		# 'service',
		'owner',
		'created',

	)
	list_filter = ('contact_name',)

	"""
	def formfield_for_foreignkey(self, db_field, request=None,  **kwargs):
		# if db_field.name =='user':
		#     emp_customer = Employee.objects.filter(roles__title__exact='customer')
		#     emp_customer_ids = [emp.id for emp in emp_customer]
		#     kwargs['queryset'] = User.objects.filter(employee__id__in = emp_customer_ids)
		#     print "emp_customer_ids", emp_customer_ids

		if db_field.name =='owner':
			kwargs['queryset'] = Employee.objects.filter(roles__title__exact='sales manager')

		elif db_field.name == 'sales_rep':
			kwargs['queryset'] = Employee.objects.filter(roles__title__exact='sales rep')

		return super(LeadAdmin, self).formfield_for_foreignkey(db_field, request=request,  **kwargs)
	"""
admin.site.register(Lead, LeadAdmin)

class CustomerAdmin(admin.ModelAdmin):
	# inlines = (FollowupInline,)

	form = CustomerForm

	fieldsets = [
		('Customer', {
			#'classes': ('suit-tab', 'suit-tab-customer',),
			'fields': ['title','description']
		}),
		('Contact Person', {
			#'classes': ('suit-tab', 'suit-tab-customer',),
			'fields': ['contact_name','designation','email','phone',]}),

		('Customer Address', {
			#'classes': ('suit-tab', 'suit-tab-customer',),
			'fields': ['country','state','city','addressline1','addressline2','zip_code']}),

		('Lead Source', {
			#'classes': ('suit-tab', 'suit-tab-customer',),
			'fields': ['lead_source', 'sales_rep','other_lead_source',]}),

		('Requirements', {
			#'classes': ('suit-tab', 'suit-tab-customer',),
			'fields': ['industry','requirement',]}),

		('Sales Manager', {
			#'classes': ('suit-tab', 'suit-tab-customer',),
			'fields': ['owner',]}),

	]

	#suit_form_tabs = (('customer', 'Customer'), ('followup', 'Followup'))
	#exclude_fields = ['user']


	list_display = (
		# 'Company',
		#'description',
		'title' ,
		'contact_name',
		'designation',
		'email',
		'phone',
		'country',
		'state',
		'industry',
		# 'service',
		'owner',
		'created',

	)
	list_filter = ('contact_name',)


	# def formfield_for_foreignkey(self, db_field, request=None,  **kwargs):
	#     # if db_field.name =='user':
	#     #     emp_customer = Employee.objects.filter(roles__title__exact='customer')
	#     #     emp_customer_ids = [emp.id for emp in emp_customer]
	#     #     kwargs['queryset'] = User.objects.filter(employee__id__in = emp_customer_ids)
	#     #     print "emp_customer_ids", emp_customer_ids

	#     if db_field.name =='owner':
	#     	kwargs['queryset'] = Employee.objects.filter(roles__title__exact='sales manager')

	#     elif db_field.name == 'sales_rep':
	# 		kwargs['queryset'] = Employee.objects.filter(roles__title__exact='sales rep')

	#     return super(CustomerAdmin, self).formfield_for_foreignkey(db_field, request=request,  **kwargs)

admin.site.register(Customer, CustomerAdmin)




class FollowupAdmin(admin.ModelAdmin):
	list_display = (
	# 'customer',
	'next_followup',
	'lead_status',
	'percentage',
	# 'status' ,
	'created',
	'modified',

	)
	list_filter = ( 'lead_status',)
	form = FollowupAdminForm
admin.site.register(Followup, FollowupAdmin)
	
class CountryAdmin(admin.ModelAdmin):
	list_display = (
	'code',
	'name',
	)
	list_filter = ('code', 'name',)

admin.site.register(Country, CountryAdmin)








