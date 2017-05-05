# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from datetime import datetime
from django import forms
from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib import admin
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.conf.urls import patterns, include, url
#from django.contrib.admin import RelatedFieldListFilter
from django.contrib.admin.filters import RelatedOnlyFieldListFilter
from django.contrib.admin import helpers
from django.contrib.auth.models import User, Group
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.html import format_html

from employee.models import Employee, Role
from project import csvimporter, models
from .models import Industry, ServiceType, BillingType, ProjectType, Project, ProjectService, ProjectPlanResource, ProjectTask, \
					Sla, ServiceSla
from .models import WorkItemStatus, WorkItem, EmployeeAssignment, QcStatus, WorkItemAssignment, QcAttribute
from .models import NormalWorkItemAssignment, QcWorkItemAssignment
from .models import ProjectTaskTemplate,ProjectWorkItemTemplate,QcAttributeTemplate

from .forms import ImportWorkItemForm, ImportProjectTaskForm, ImportDailyTasksForm
from .forms import  ProjectAdminForm, WorkItemAssignmentForm,  ProjectTaskInlineForm
from .forms import  ProjectTaskForm, ProjectServiceAdminForm, WorkItemAdminForm, QcAssignmentForm, QcAttributeForm
from .forms import ImportWorkItemForm, ImportProjectTaskForm, ImportDailyTasksForm, WorkItemAssignmentInlineForm
from .forms import ProjectWorkItemTemplateForm, ProjectTaskTemplateForm, QcAttributeTemplateForm


"""
class RelatedOnlyFieldListFilter(RelatedFieldListFilter):
	def __init__(self, field, request, params, model, model_admin, field_path):
		super(RelatedOnlyFieldListFilter, self).__init__(
			field, request, params, model, model_admin, field_path)
		qs = field.related_field.model.objects.filter(
			id__in=model_admin.get_queryset(request).values_list(
				field.name, flat=True).distinct())
		self.lookup_choices = [(each.id, unicode(each)) for each in qs]
"""

class ServiceTypeAdmin(admin.ModelAdmin):
	list_display = (
		#u'id',
		#'created',
		#'modified',
		'title',
		'description',
   
	)
	list_filter = ('created', 'modified')
	search_fields = ('slug',)
admin.site.register(ServiceType, ServiceTypeAdmin)


class IndustryAdmin(admin.ModelAdmin):
	list_display = (
		#u'id',
		#'created',
		#'modified',
		'title',
		'description',
   
	)
	list_filter = ('created', 'modified')
	search_fields = ('slug',)
admin.site.register(Industry, IndustryAdmin)


class ServiceSlaInline(admin.TabularInline):
	
	model = models.ServiceSla
	list_display = (
		#u'id',
		#'created',
		#'service',
		'sla_type',
		'sla_value',
   
	)

class ServiceDocumentInline(admin.TabularInline):
	
	model = models.ServiceDocument
	list_display = (
		#u'id',
		#'created',
		#'modified',
		'document',
   
	)

class ServiceResourcePlanInline(admin.TabularInline):

	model = models.ServiceResourcePlan
	extra = 1
	list_display = (
		u'id',
		'experience_slab',
		'number_of_resources',
		'output_count_per_resource',
   
	)

class AssignServiceLeadInline(admin.TabularInline):

	model = models.AssignServiceLead
	extra = 1
	list_display = (
		u'id',
		'lead',

 
	)

class ServiceAdmin(admin.ModelAdmin):
	inlines = [ServiceSlaInline, ServiceDocumentInline,ServiceResourcePlanInline, AssignServiceLeadInline ]
	list_display = (
		u'id',
		'title',
		'customer',
		'shift_timings',
		'project_type',
		'service_type',
		#'scope_of_work',
		#'statement_of_procedure',
		# 'turn_around_time_in_hours',
		# 'quality',
		'number_of_resources',
		#'amount_per_billing_type',
		#'billing_type',
		'billing_interval_in_days',
		'operations_manager',
		#'created',
		#'modified',
	)	
	list_filter = ('service_type', 'project_type', 'operations_manager')
   
admin.site.register(models.Service, ServiceAdmin)


class BillingTypeAdmin(admin.ModelAdmin):
	list_display = (u'id', 'title', 'description')
admin.site.register(BillingType, BillingTypeAdmin)


class ProjectTypeAdmin(admin.ModelAdmin):
	list_display = (u'id', 'title', 'description', 'slug')
	search_fields = ('slug',)
admin.site.register(ProjectType, ProjectTypeAdmin)


class SlaAdmin(admin.ModelAdmin):
	list_display = (u'id', 'title')
admin.site.register(Sla, SlaAdmin)

class ServiceSlaAdmin(admin.ModelAdmin):
	list_display = (u'id', 'service', 'sla_type', 'sla_value')
admin.site.register(ServiceSla, ServiceSlaAdmin)



class TaskResourcePlanInline(admin.TabularInline):
	'''
		Tabular Inline View for 
	'''
	model = models.TaskResourcePlan
	min_num = 2
	max_num = 20
	extra = 1


class LeadTaskInline(admin.TabularInline):
	'''
		Tabular Inline View for 
	'''
	model = models.LeadTask
	min_num = 3
	max_num = 20
	extra = 1




class TaskAdmin(admin.ModelAdmin):
	inlines = [TaskResourcePlanInline, LeadTaskInline]
	list_display = (
		u'id', 
		'title', 
		'service',
		# 'folderpath',
		'no_of_txs',
		'no_of_txs_completed',
		'total_time_hours'
	)
admin.site.register(models.Task, TaskAdmin)


class LeadTaskResourcePlanInline(admin.TabularInline):
	'''
		Tabular Inline View for 
	'''
	model = models.LeadTaskResourcePlan
	min_num = 3
	max_num = 20
	extra = 1

class StaffTaskInline(admin.TabularInline):
	'''
		Tabular Inline View for 
	'''
	model = models.StaffTask
	min_num = 3
	max_num = 20
	extra = 1

class LeadTaskAdmin(admin.ModelAdmin):
	inlines = [LeadTaskResourcePlanInline, StaffTaskInline]
	list_display = (
		u'id', 
		'task', 
		'lead',
		# 'filename',
		'no_of_txs',
		'no_of_txs_completed',
		'total_time_hours'
	)
admin.site.register(models.LeadTask, LeadTaskAdmin)

class StaffTaskAdmin(admin.ModelAdmin):

	list_display = (
		u'id', 
		'lead_task', 
		'staff',
		'filename',
		'no_of_txs',
		'no_of_txs_completed',
		'total_time_hours',
		'created',
		'modified'
	)
admin.site.register(models.StaffTask, StaffTaskAdmin)

class ProjectPlanResourceInline(admin.TabularInline):
	'''
	Tabular Inline View for ProjectPlanResource
	'''
	model = ProjectPlanResource

	#suit_classes = 'suit-tab suit-tab-resourceplan'
	# min_num = 3
	# max_num = 20
	extra = 1
	# raw_id_fields = (,)

	list_display = (
	   # u'id',
		'experience_slab',
		'number_of_resources',
		'output_count_per_resource',
	)
	list_filter = ('experience_slab',)


class ProjectServiceInline(admin.TabularInline):
	'''
	Tabular Inline View for ProjectService
	'''
	model = ProjectService
	#suit_classes = 'suit-tab suit-tab-projectservice'
	#form = ProjectServiceInlineForm
	# min_num = 3
	#max_num = 20
	extra = 1
	# raw_id_fields = (,)

	list_display = (
	   # u'id',
		'project',
		'industry',
		# 'service',
		'operations_manager',
	)
	list_filter = ('project', 'industry', 'operations_manager')
	#form=ProjectServiceInlineForm
	form=ProjectServiceAdminForm

	opsmagr_readonly_fields = ['industry', 'operations_manager',]

	def formfield_for_foreignkey(self, db_field, request=None,  **kwargs):
		if db_field.name =='operations_manager':
			kwargs['queryset'] = Employee.objects.filter(roles__title__exact='operations manager')
		return super(ProjectServiceInline, self).formfield_for_foreignkey(db_field, request=request,  **kwargs)


	def get_readonly_fields(self, request, obj=None):
		actions = super(ProjectServiceInline, self).get_readonly_fields(request, obj=obj)
		if request.user.groups.filter(name='operations manager').exists():
			return self.opsmagr_readonly_fields
		else:
			return actions

class ProjectAdmin(admin.ModelAdmin):
	inlines=(ProjectPlanResourceInline, ProjectServiceInline,)


	form = ProjectAdminForm
	list_display = (
		u'id',
		'title',
		'slug',
		'start',
		'end',
		'customer',
		#'scope_of_work',
		#'statement_of_procedure',
		'project_type',
		'quality',
		'number_of_resources',
		'turn_around_time_in_hours',
		#'amount_per_billing_type',
		#'billing_type',
		'billing_interval_in_days',
		'sales_manager',
		#'created',
		#'modified',
	)
	list_filter = (
		'created',
		'modified',
		'start',
		'end',
		('customer',RelatedOnlyFieldListFilter),
		('project_type',RelatedOnlyFieldListFilter),
		('billing_type',RelatedOnlyFieldListFilter),
		('sales_manager', RelatedOnlyFieldListFilter),
	)
	search_fields = ('slug',)
	prepopulated_fields = {'slug':('title',),}
	list_display_links = (u'id', 'title')

	Project.objects.order_by('sales_manager', 'customer')

	customer_readonly_fields = ('customer','project_type','number_of_resources','billing_interval_in_days',
			'turn_around_time_in_hours','amount_per_billing_type','billing_type','sales_manager',)


	ops_magr_readonly_fields = ('customer','sales_manager',)


  
   #suit_form_tabs = (('project', 'Project'), ('projectplanresource', 'ProjectPlanResource'),('projectservice', 'ProjectService'))

	def formfield_for_foreignkey(self, db_field, request=None,  **kwargs):
		if db_field.name =='sales_manager':
			kwargs['queryset'] = Employee.objects.filter(roles__title__exact= 'sales manager')
		return super(ProjectAdmin, self).formfield_for_foreignkey(db_field, request=request,  **kwargs)

	def get_readonly_fields(self, request, obj=None):
		actions = super(ProjectAdmin, self).get_readonly_fields(request, obj=obj)
		if request.user.groups.filter(name='customer').exists():
			return self.customer_readonly_fields

		elif request.user.groups.filter(name='operations manager').exists():
			return self.ops_magr_readonly_fields
		else:
			return actions

	
	def get_form(self, request, obj=None, **kwargs):
		self._request = request
	  
		if request.user.groups.filter(name='operations manager').exists():
			self.fieldsets = [
					('Project Info', {
						#'classes': ('suit-tab', 'suit-tab-project',),
						'fields': ['title','slug','shift_timings','start','end','description',]
					}),
					('Customer', { 
						#'classes': ('suit-tab', 'suit-tab-project',),
						'fields': ['customer',]
					}),
				
					('Requirements', {
						#'classes': ('suit-tab', 'suit-tab-project',),
						'fields': ['project_type','number_of_resources','scope_of_work', 'statement_of_procedure','quality',]
					}),
					('Sales Manager', {
						#'classes': ('suit-tab', 'suit-tab-project',),
						'fields': ['sales_manager',]
					}),
				]
		else:
			  self.fieldsets = [
				('Project Info', {
					#'classes': ('suit-tab', 'suit-tab-project',),
					'fields': ['title','slug','shift_timings','start','end','description',]
				}),
				('Customer', { 
					#'classes': ('suit-tab', 'suit-tab-project',),
					'fields': ['customer',]
				}),
		
				('Requirements', {
					#'classes': ('suit-tab', 'suit-tab-project',),
					'fields': ['project_type','number_of_resources','scope_of_work', 'statement_of_procedure','quality',]
				}),
				('Project Budget', {
					#'classes': ('suit-tab', 'suit-tab-project',),
					'fields': ['billing_interval_in_days','turn_around_time_in_hours','amount_per_billing_type','billing_type',]
				}),
				('Sales Manager', {
					#'classes': ('suit-tab', 'suit-tab-project',),
					'fields': ['sales_manager',]
				}),
			]
		return super(ProjectAdmin, self).get_form(request, obj=None, **kwargs)
	"""
	@property
	def suit_form_tabs(self):
		if self._request.user.groups.filter(name='sales manager').exists():
			tabs = (('project', 'Project'),('projectservice', 'ProjectService'))

		elif self._request.user.groups.filter(name='operations manager').exists():
			tabs = (('project', 'Project'),('resourceplan', 'ResourcePlan'),)
		else:
			tabs = (('project', 'Project'),('projectservice', 'ProjectService'),('resourceplan', 'ResourcePlan'),)
		return tabs
	"""
	def queryset(self, request):

		qs = super(ProjectAdmin, self).queryset(request)
		if request.user.is_superuser:
			# It is mine, all mine. Just return everything.
			return qs

		groups=request.user.groups.all()

		group_dict = dict([ (grp.name, grp)  for  grp in groups])

		# print  group_dict

		if 'sales manager' in group_dict:
			return qs.filter(sales_manager__user=request.user)

		elif 'customer' in group_dict:
			return qs.filter(customer__user = request.user)

		elif 'management' in group_dict:
			return qs

		elif 'operations manager' in group_dict:
			project_services=ProjectService.objects.filter(operations_manager__user = request.user)
			project_ids=[proj_svc.project_id for proj_svc in project_services]
			print "ops manager projects", project_ids
			return qs.filter(pk__in = project_ids)
			
		# import pdb; pdb.set_trace()
		# if "operations_manager" in request.user.groups

		# vendor_admin_user = VendorAdminUser.objects.get(user=request.user)
		# return qs.filter(vendor=vendor_admin_user.vendor)

		return qs
   

admin.site.register(Project, ProjectAdmin)


# class ProjectPlanAdmin(admin.ModelAdmin):
#     list_display = (u'id', 'project')
#     list_filter = ('project',)
# admin.site.register(ProjectPlan, ProjectPlanAdmin)


class ProjectPlanResourceAdmin(admin.ModelAdmin):
	list_display = (
	   # u'id',
		'experience_slab',
		'number_of_resources',
		'output_count_per_resource',
	)
	list_filter = ('experience_slab',)

	def formfield_for_foreignkey(self, db_field, request, **kwargs):
		
		if db_field.name == "project":
			if not request.user.is_superuser:
				pro_service = [s.id for s in ProjectService.objects.filter(operations_manager__user=request.user)]
				print "printing ops mgr pro services", pro_service
				kwargs["queryset"] = Project.objects.filter(projectservice__id__in=pro_service)
		
		return super(ProjectPlanResourceAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)
	

	def queryset(self, request):

		qs = super(ProjectPlanResourceAdmin, self).queryset(request)
		if request.user.is_superuser:
			# It is mine, all mine. Just return everything.
			return qs

		groups=request.user.groups.all()

		group_dict = dict([ (grp.name, grp)  for  grp in groups])

		# print  group_dict

		if 'operations manager' in group_dict:
			project_services=ProjectService.objects.filter(operations_manager__user = request.user)
			service_ids=[ps.service_id for ps in project_services]
			print "ops manager services", service_ids
			return qs.filter(project__projectservice__operations_manager__user=request.user)
			
		return qs
admin.site.register(ProjectPlanResource, ProjectPlanResourceAdmin)



class WorkItemInline(admin.StackedInline):
	'''
	Tabular Inline View for WorkItem
	'''
	model = WorkItem
	# min_num = 3
	# max_num = 20
	#suit_classes = 'suit-tab suit-tab-workitem'
	#extra = 1
	# raw_id_fields = (,)
	form = WorkItemAdminForm
	list_display = (
		u'id',
		'created',
		'modified',
		'project_task',
		'file_name',
		#'file_path',
	)
	list_filter = ('created', 'modified', 'project_task')
	agent_readonly_fields=('file_name',)
	def get_readonly_fields(self, request, obj=None):
		actions = super(WorkItemInline, self).get_readonly_fields(request, obj=obj)
		if request.user.groups.filter(name='agent').exists():
			return self.agent_readonly_fields
		else:
			return actions
		   
	def queryset(self, request):

		qs = super(WorkItemInline, self).queryset(request)
		if request.user.is_superuser:
			# It is mine, all mine. Just return everything.
			return qs

		groups=request.user.groups.all()
		group_dict = dict([ (grp.name, grp)  for  grp in groups])

	
		if  'management' in  group_dict :
			return qs

		elif 'lead' in group_dict:
			return qs.filter(workitemassignment__lead__user = request.user)

		elif 'agent' in group_dict:
			return qs.filter(workitemassignment__agents__user = request.user)

		elif 'operations manager' in group_dict:
			opmgr_project_tasks = ProjectTask.objects.filter(project_service__operations_manager__user=request.user)
			opmgr_projectTask_ids = [task.id for task in opmgr_project_tasks]
			return qs.filter(project_task__id__in = opmgr_projectTask_ids)

		return qs



from django.http import JsonResponse
import json
from django.core import serializers

class ProjectTaskAdmin(admin.ModelAdmin):
	#inlines = (WorkItemInline,)
	form = ProjectTaskForm

	list_display = (
		u'id',
		#'created',
		#'modified',
		'project',
		'TaskName',
		'slug',
		#'description',
		#'start',
		#'end',
		#'scope_of_work',
		'project_service',
		
	)
	list_filter = (
		'created', 
		'modified', 
		'start', 
		'end', 
		('project_service', RelatedOnlyFieldListFilter),
	)
	search_fields = ('slug',)
	list_display_links = ['id','TaskName']
   # prepopulated_fields = {'slug':('project','project_service','title',),}

	agent_readonly_fields = ('title','start','end','project','description','scope_of_work','project_service','total_workitems', )
	customer_readonly_fields = ('scope_of_work','project_service',)

	#fields = ['title','description','project_service','scope_of_work','total_workitems','total_workitems_completed','total_time_hours',\
				#'custom_field1','custom_field2','custom_field3','custom_field4','custom_field5','custom_field6','custom_field7',\
			   # 'custom_field8','custom_field9','custom_field10',
		#]

	def formfield_for_foreignkey(self, db_field, request, **kwargs):
		if request.user.groups.filter(name='operations manager').exists():
			if db_field.name == "project":	
				pro_service = [s.id for s in ProjectService.objects.filter(operations_manager__user=request.user)]
				print "printing ops mgr pro services", pro_service
				kwargs["queryset"] = Project.objects.filter(projectservice__id__in=pro_service)
			
			if db_field.name == "project_service":
				kwargs["queryset"] = ProjectService.objects.filter(operations_manager__user=request.user)

		
		return super(ProjectTaskAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)
	


	def get_form(self, request, obj=None, **kwargs):
		if request.user.groups.filter(name__in=['agent',]).exists():
			self.fieldsets = [
				('Project Task', {
					'fields': ['project','title','project_service','total_workitems','total_workitems_completed', 'total_time_hours',
							'scope_of_work', 'custom_field1','custom_field2','custom_field3','custom_field4','custom_field5','custom_field6','custom_field7',\
							'custom_field8','custom_field9','custom_field10']
				}),
			]

		else:
			self.fieldsets = [
				('Project Task', {
					'fields': ['project','title','project_service','total_workitems','total_workitems_completed', 'total_time_hours',
							'scope_of_work', 'custom_field1','custom_field2','custom_field3','custom_field4','custom_field5','custom_field6','custom_field7',\
							'custom_field8','custom_field9','custom_field10']
				}),
			]

		return super(ProjectTaskAdmin, self).get_form(request, obj=None, **kwargs)


	def get_readonly_fields(self, request, obj=None):
		actions = super(ProjectTaskAdmin, self).get_readonly_fields(request, obj=obj)
		if request.user.groups.filter(name='customer').exists():
			return self.customer_readonly_fields
		elif request.user.groups.filter(name='agent').exists():
			return self.agent_readonly_fields
		else:
			return actions


	def queryset(self, request):

		qs = super(ProjectTaskAdmin, self).queryset(request)
		if request.user.is_superuser:
			# It is mine, all mine. Just return everything.
			return qs

		groups=request.user.groups.all()
		group_dict = dict([ (grp.name, grp)  for  grp in groups])

		project_ids=[]
		if  'management' in  group_dict :
			return qs

		elif 'lead' in group_dict:
			work_items = WorkItem.objects.filter(workitemassignment__lead__user = request.user)
			lead_work_items_ids = [work.project_task_id for work in work_items]
			print "lead work items", work_items
			return qs.filter(pk__in=lead_work_items_ids)

		elif 'agent' in group_dict:
			work_items = WorkItem.objects.filter(workitemassignment__agents__user = request.user)
			agents_work_items_ids = [work.project_task_id for work in work_items]
			print "agents work items", work_items
			return qs.filter(pk__in=agents_work_items_ids)

		elif 'operations manager' in group_dict:
			return qs.filter(project_service__operations_manager__user = request.user)

		return qs

	def get_urls(self):
		urls = super(ProjectTaskAdmin,self).get_urls()
		add_urls = [
				url(r'upload/$', self.admin_site.admin_view(self.upload), name='project_projecttask_upload'),
				url(r'process_import/$', self.admin_site.admin_view(self.upload), name='project_projecttask_process_import'),
		]
		return add_urls + urls

	def upload(self,request):

		context = {
			'title': 'Upload Project Tasks',
			'app_label': self.model._meta.app_label,
			'opts': self.model._meta,
			'has_change_permission': self.has_change_permission(request)
		}
		# Handle form request
		if request.method == 'POST':
			
			form = ImportProjectTaskForm(request.POST or None, request.FILES)
			if form.is_valid():
				# Do CSV processing and create records

				file = form.cleaned_data['file']
				
				#cleaned_rows = form.cleaned_data["rows"]
				#invalid_rows = form.cleaned_data["invalid_rows"]

				fields, data_lines = csvimporter.handle_uploaded_file(file)
				csv_result, rows_error, rows_updated = csvimporter.create_projecttask_in_db(data_lines)
				
				if csv_result:
					message = 'Successfully imported %d Project Tasks from the csv file to the database.\n' %len(rows_updated)
					messages.add_message(request, messages.INFO, message)
					context['result'] = csv_result
					context['rows_updated'] = rows_updated
					context['fields'] = fields
					return HttpResponseRedirect("../")

				else:
					#message = 'There are some errors occured.'
					#messages.add_message(request, messages.ERROR, rows_error)
					context['rows_error'] = rows_error
		else:
			form = ImportProjectTaskForm()
		context['form'] = form
		return render(request, 'admin/project/projecttask/upload.html', context)



admin.site.register(ProjectTask, ProjectTaskAdmin)
#admin.site.disable_action('delete_selected')
#admin.site.add_action('delete_selected')


class WorkItemStatusAdmin(admin.ModelAdmin):
	list_display = (u'id', 'title', 'description')
admin.site.register(WorkItemStatus, WorkItemStatusAdmin)



#<<<<<<< HEAD
#=======
# class WorkItemAssignmentInline(admin.TabularInline):
#     '''
#     Tabular Inline View for WorkItemAssignment
#     '''
#     model = WorkItemAssignment
#     # min_num = 3
#     # max_num = 20
#     extra = 1
#     # raw_id_fields = (,)


#>>>>>>> 0af8b9a6ef33f963c3d29f69e531c43766895e02
class WorkItemAssignmentInline(admin.TabularInline):
	'''
	Tabular Inline View for WorkItem
	'''
	model = WorkItemAssignment
	min_num = 1
	#max_num = 5
	#suit_classes = 'suit-tab suit-tab-workitem'
	extra = 1
	# raw_id_fields = (,)
	form = WorkItemAssignmentInlineForm
	list_display = (
		u'id',
	#	'created',
	#	'modified',
		'project_task',
		'file_name',
		#'file_path',
	)
	agent_readonly_fields = ('lead','agents','time_in_min')

	def get_readonly_fields(self, request, obj=None):
		actions = super(WorkItemAssignmentInline, self).get_readonly_fields(request, obj=obj)
		if request.user.groups.filter(name='agent').exists():
			return self.agent_readonly_fields

		return actions

	def formfield_for_foreignkey(self, db_field, request, **kwargs):
		if db_field.name == "lead":
			kwargs['queryset'] =Employee.objects.filter(roles__title__in = ['project lead', 'team lead']).distinct()

		return super(WorkItemAssignmentInline, self).formfield_for_foreignkey(db_field, request, **kwargs)

	def formfield_for_manytomany(self, db_field, request, **kwargs):
		if db_field.name == "agents":
			kwargs["queryset"] = Employee.objects.filter(roles__title__exact='agent' )
		return super(WorkItemAssignmentInline, self).formfield_for_manytomany(db_field, request, **kwargs)



class WorkItemAdmin(admin.ModelAdmin):
	inlines = (WorkItemAssignmentInline, )
	
	#resource_class = WorkItemResource
	list_display = (
		u'id',
		'project',
		'projectService',
		'project_task',
		'folder_name',
		'file_name',
		'number_of_items',
		
	)
	list_filter = (
		#'created',
		#'modified',
		#'start',
		#'end',  
		('project_task', RelatedOnlyFieldListFilter),

	)
	list_display_links = [u'id', 'file_name',]
	search_fields = ['slug','file_name','folder_name' ,'project_task__title']
	#prepopulated_fields = {'slug':('folder_name', 'file_name'),}

	form = WorkItemAdminForm
	
	agent_readonly_fields = ('project_task','folder_name', 'file_name')


	def formfield_for_foreignkey(self,db_field, request, **kwargs):
		if db_field.name == 'project_task':
			if not request.user.is_superuser:
				project_ids = [p.id for p in Project.objects.filter(projectservice__operations_manager__user=request.user)]
				print "print project ids", project_ids
				kwargs['queryset'] = ProjectTask.objects.filter(project_id__in=project_ids).distinct()

		return super(WorkItemAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)


	def get_readonly_fields(self, request, obj=None):
		actions = super(WorkItemAdmin, self).get_readonly_fields(request, obj=obj)
		if request.user.groups.filter(name='agent').exists():
			readonly = ('project_task','file_name','folder_name','number_of_items' )
			return readonly

		elif request.user.groups.filter(name='customer').exists():
			return self.agent_readonly_fields

		else:
			return actions


	def get_list_display(self, request):
		actions = super(WorkItemAdmin, self).get_list_display(request)
		if request.user.groups.filter(name='agent').exists():
			display = ('id','project_task','file_name','folder_name','number_of_items' )
			return display

		else:
			return actions
	
	def queryset(self, request):

		qs = super(WorkItemAdmin, self).queryset(request)
		if request.user.is_superuser:
			# It is mine, all mine. Just return everything.
			return qs

		groups=request.user.groups.all()
		group_dict = dict([ (grp.name, grp)  for  grp in groups])

	
		if  'management' in  group_dict :
			return qs

		elif 'lead' in group_dict:
			return qs.filter(workitemassignment__lead__user = request.user).distinct()

		elif 'agent' in group_dict:
			return qs.filter(workitemassignment__agents__user = request.user).distinct()

		elif 'operations manager' in group_dict:
			opmgr_project_tasks = ProjectTask.objects.filter(project_service__operations_manager__user=request.user)
			opmgr_projectTask_ids = [task.id for task in opmgr_project_tasks]
			#print 'opmgr_projectTask_ids', opmgr_projectTask_ids
			return qs.filter(project_task__id__in = opmgr_projectTask_ids)

		elif 'customer' in group_dict:
			project_tasks = ProjectTask.objects.filter(project_service__project__customer__user=request.user)
			project_task_ids = [task.id for task in project_tasks]
			return qs.filter(project_task__id__in = project_task_ids)
		

		return qs

	def get_urls(self):
		urls = super(WorkItemAdmin,self).get_urls()
		add_urls = [
				url(r'upload/$', self.admin_site.admin_view(self.upload), name='project_workitem_upload'),
		]
		return add_urls + urls

	def upload(self,request):

		context = {
			'title': 'Upload WorkItems',
			'app_label': self.model._meta.app_label,
			'opts': self.model._meta,
			'has_change_permission': self.has_change_permission(request)
		}
 
		# Handle form request
		if request.method == 'POST':
			form = ImportLeadForm(request.POST, request.FILES)
			if form.is_valid():
				# Do CSV processing and create ProductKey records

				file = form.cleaned_data['file']
				fields, data_lines = csvimporter.handle_uploaded_file(file)
				csv_result, rows_error, rows_updated = csvimporter.create_workitems_in_db(data_lines)

				if csv_result:
					message = 'Successfully imported %d Work items from the csv file to the database.\n' %len(rows_updated)
					#message += 'The system is creating Active Directory Accounts using those information in the background.\n'
					message += 'Please wait...'
					messages.add_message(request, messages.INFO, message)
					context['result'] = csv_result
					context['rows_updated'] = rows_updated

					return HttpResponseRedirect("../")

				else:
					message = 'There are some %d errors occured. Please try again.' %len(rows_error)
					messages.add_message(request, messages.INFO, message)
					context['rows_error'] = rows_error

		else:
			form = ImportWorkItemForm()
		context['form'] = form
 
		context['adminform'] = helpers.AdminForm(form, list([(None, {'fields': form.base_fields})]),
												 self.get_prepopulated_fields(request))
 
		return render(request, 'admin/project/projecttask/upload.html', context)


	


	
admin.site.register(WorkItem, WorkItemAdmin)




class EmployeeAssignmentAdmin(admin.ModelAdmin):
	list_display = (
		#u'id',
		#'created',
		#'modified',
		'employee',
		# 'project',
		'experience_slab',
		'start',
		'end',
		'comments',
	)
	list_filter = (
		'created',
		'modified',
		'start',
		'end',
		('employee', RelatedOnlyFieldListFilter),
		# ('project', RelatedOnlyFieldListFilter),
		'experience_slab',
	)
admin.site.register(EmployeeAssignment, EmployeeAssignmentAdmin)


class QcStatusAdmin(admin.ModelAdmin):
	list_display = (u'id', 'title', 'description', 'slug')
	search_fields = ('slug',)
admin.site.register(QcStatus, QcStatusAdmin)





class WorkItemAssignmentAdmin(admin.ModelAdmin):

	#resource_class = WorkItemAssignmentResource
	#list_display_links = [u'id','workitem',]

	list_display = (
		u'id',
		#'created',
		#'modified',
		'workitem',
		'lead',
		'associates',
		'workitem_status',
		'no_of_items',
		'no_of_items_completed',
		'is_qc_required',
		'start',
		'end',
		'button'
	   
		
	)
	list_filter = (
		#'created',
		#'modified',
		'start',
		'end',
		#('workitem',RelatedOnlyFieldListFilter),
		('lead', RelatedOnlyFieldListFilter),
		# ('agent', RelatedOnlyFieldListFilter),
		'workitem_status',
		
	)
	form = WorkItemAssignmentForm
	search_fields = ['workitem__file_name','lead__name', 'agents__name']

	agent_readonly_fields = ('lead','agents', 'workitem','time_in_min')
		

	def formfield_for_foreignkey(self, db_field, request, **kwargs):
		if request.user.groups.filter(name='operations manager').exists():
			if db_field.name=='workitem':			
				proj_tasks_ids = [pt.id for pt in ProjectTask.objects.filter(project__projectservice__operations_manager__user=request.user)]
				print "projecttask ids", proj_tasks_ids
				kwargs['queryset'] = WorkItem.objects.filter(project_task_id__in=proj_tasks_ids)

			if db_field.name == "lead":				
				rel_empl =Employee.objects.get(user=request.user)
				#rel_empl =Employee.objects.filter(roles__title__in = ['project lead', 'team lead'])
				kwargs['queryset'] = rel_empl.get_children().filter(roles__title__in = ['project lead', 'team lead'])

		elif request.user.groups.filter(name='lead').exists():
			if db_field.name=='workitem':			
				proj_tasks_ids = [pt.id for pt in ProjectTask.objects.filter(project__projectservice__operations_manager__user=request.user)]
				print "projecttask ids", proj_tasks_ids
				kwargs['queryset'] = WorkItem.objects.filter(project_task_id__in=proj_tasks_ids)

			if db_field.name == "lead":				
				rel_empl =Employee.objects.get(user=request.user)
				#rel_empl =Employee.objects.filter(roles__title__in = ['project lead', 'team lead'])
				kwargs['queryset'] = rel_empl.get_descendants(include_self=True).filter(roles__title__in = ['project lead', 'team lead'])

		return super(WorkItemAssignmentAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

	def formfield_for_manytomany(self, db_field, request, **kwargs):
		if request.user.groups.filter(name='operations manager').exists():
			if db_field.name == "agents":
				related_agents = Employee.objects.get(user=request.user)
				kwargs["queryset"] = related_agents.get_descendants().filter(roles__title__exact = 'agent')

		elif request.user.groups.filter(name='lead').exists():
			if db_field.name == "agents":
				related_agents = Employee.objects.get(user=request.user)
				kwargs["queryset"] = related_agents.get_descendants().filter(roles__title__exact = 'agent')

		return super(WorkItemAssignmentAdmin, self).formfield_for_manytomany(db_field, request, **kwargs)

	def get_form(self, request, obj=None, **kwargs):
		if request.user.groups.filter(name__in=['agent', 'lead','operations manager']).exists():
			self.exclude = ('error_percent','qc_status','qc_agent') 
		else:
			self.exclude = ()
		return super(WorkItemAssignmentAdmin, self).get_form(request, obj=None, **kwargs)


	def get_readonly_fields(self, request, obj=None):
		actions = super(WorkItemAssignmentAdmin, self).get_readonly_fields(request, obj=obj)
		
		if request.user.groups.filter(name='agent').exists():
			return self.agent_readonly_fields
		elif request.user.groups.filter(name='customer').exists():
			return self.agent_readonly_fields
		else:
			return actions

	def get_list_display(self, request):
		actions = super(WorkItemAssignmentAdmin, self).get_list_display(request)
		if request.user.groups.filter(name='agent').exists():
			display = ('id','workitem','lead','no_of_items','workitem_status','button' )
			return display

		elif request.user.groups.filter(name='operations manager').exists():
			display = ('id','workitem','lead','associates','workitem_status','no_of_items','no_of_items_completed','time_in_min','start','end' )
			return display

		elif request.user.groups.filter(name='lead').exists():
			display = ('id','workitem','associates','workitem_status','no_of_items','no_of_items_completed','time_in_min','start','end' )
			return display
		else:
			display = ('id','workitem','associates','workitem_status','no_of_items','no_of_items_completed','time_in_min','start','end' )
			return display
		return actions
	
	def get_list_display_links(self, request, list_display):
		actions = super(WorkItemAssignmentAdmin, self).get_list_display_links(request,list_display)
		if request.user.groups.filter(name='agent').exists():
			display = ('button', )
			return display

		else:
			return actions

	def get_queryset(self, request):

		qs = super(WorkItemAssignmentAdmin, self).queryset(request)
		if request.user.is_superuser:
			# It is mine, all mine. Just return everything.
			return qs

		groups=request.user.groups.all()
		group_dict = dict([ (grp.name, grp)  for  grp in groups])

		if 'management' in  group_dict :
			return qs
		
		elif 'lead' in group_dict:
			return qs.filter(lead__user = request.user)
		
		elif 'agent' in group_dict:
			"""
			emp_agent = Employee.objects.get(user=request.user)
			print "employee agents are", emp_agent

			qs = WorkItemAssignment.objects.filter(agents=emp_agent, workitem_status__title__in=['new', 'assigned', 'work in progress', 'on hold'])

			#get_agents = Employee.objects.filter(workitemassignment=)

			print "daily tasks", qs
			"""
			return qs.filter(agents__user = request.user, workitem_status__title__in=['new', 'assigned', 'work in progress', 'on hold'])

		elif 'operations manager' in group_dict:
			opmgr_work_items = WorkItem.objects.filter(project_task__project_service__operations_manager__user=request.user)
			opmgr_workitems_ids = [work.id for work in opmgr_work_items]
			print "opmgr_workitems_ids", opmgr_workitems_ids
			return qs.filter(workitem__id__in = opmgr_workitems_ids)

		elif 'customer' in group_dict:
			work_items = WorkItem.objects.filter(project_task__project_service__project__customer__user =request.user)
			workitems_ids= [ work.id for work in work_items]
			print " customer work items", workitems_ids
			return qs.filter(workitem__id__in = workitems_ids)
		return qs


	def get_urls(self):
		urls = super(WorkItemAssignmentAdmin,self).get_urls()
		add_urls = [
				url(r'upload/$', self.admin_site.admin_view(self.upload), name='project_normalworkitemassignment_upload')
		]
		return add_urls + urls


	def upload(self,request):

		context = {
			'title': 'Upload DailyTasks',
			'app_label': self.model._meta.app_label,
			'opts': self.model._meta,
			'has_change_permission': self.has_change_permission(request)
		}

		# Handle form request
		if request.method == "POST":
			form = ImportDailyTasksForm(request.POST, request.FILES)
			if form.is_valid():

				file = form.cleaned_data['file']
				fields, data_lines = csvimporter.handle_uploaded_file(file)
				csv_result, rows_error, rows_updated = csvimporter.create_dailytasks_in_db(data_lines)

				if csv_result:
					message = 'Successfully imported %d Work items from the csv file to the database.\n' %len(rows_updated)
					#message += 'The system is creating Active Directory Accounts using those information in the background.\n'
					message += 'Please wait...'
					messages.add_message(request, messages.INFO, message)
					context['result'] = csv_result
					context['rows_updated'] = rows_updated

					return HttpResponseRedirect("../")

				else:
					message = 'There are some %d errors occured. Please try again.' %len(rows_error)
					messages.add_message(request, messages.INFO, message)
					context['rows_error'] = rows_error
				
		else:
			form = ImportDailyTasksForm()
		# Render the template.

		context['form'] = form

		context['adminform'] = helpers.AdminForm(form, list([(None, {'fields': form.base_fields})]),
												 self.get_prepopulated_fields(request))

		return render(request, 'admin/project/projecttask/upload.html', context)
	


	def button(self, object):
		
		url = reverse('admin:%s_normalworkitemassignment_change' %(object._meta.app_label,),  args=[object.id] )

		return format_html("<a href='%s' class='btn btn-high' name='startwork' type='button' >Start</a>" %(url)
			#'<input class= "field-start",  type="submit" value="StartWorking" />'
			)
	button.short_description = ' '
	button.allow_tags = True


	change_form_template = 'admin/project/normalworkitemassignment/change_form.html'

	def response_change(self, request, obj):
		opts = self.model._meta
		pk_value = obj._get_pk_val()
		preserved_filters = self.get_preserved_filters(request)

		if request.POST.has_key("startwork"):
			msg = 'The %(name)s "%(obj)s" is Started working'  % {
				'name': obj._meta.verbose_name, 'obj': obj
			}
			startwork_id = request.POST['startwork']
			print "startwork id", startwork

			dailytask = WorkItemAssignment.objects.get(pk=obj.id)
			print "dailytask", dailytask
			
			dailytask.workitem_status = WorkItemStatus.objects.get(id__exact='3')
			dailytask.save()

			self.message_user(request, msg)

			return HttpResponseRedirect(".")

		if request.POST.has_key("start"):
			msg = 'The %(name)s "%(obj)s" is timer started'  % {
				'name': obj._meta.verbose_name, 'obj': obj
			}
			self.message_user(request, msg)

			return HttpResponseRedirect(".")


		if request.POST.has_key("stop"):
			msg = 'The %(name)s "%(obj)s" is paused.' % {
				'name': obj._meta.verbose_name, 'obj': obj
			}
			self.message_user(request, msg)
			return HttpResponseRedirect(".")


		if request.POST.has_key("sendtoqc"):
			msg = 'The %(name)s "%(obj)s" is Submitted to QC'  % {
				'name': obj._meta.verbose_name, 'obj': obj
			}

			try:
				dailytask = WorkItemAssignment.objects.get(pk=obj.id)
				print "dailytask", dailytask

				start_time = request.POST['start_1']
				print "start time", start_time
				end_time = request.POST['end_1']
				print "end time", end_time
				FMT = '%H:%M:%S'
				time_diff = datetime.strptime(end_time, FMT) - datetime.strptime(start_time, FMT)
				print "time diff", time_diff
				#timer_value = request.POST.get('timerValue')
				get_workitem_status = WorkItemStatus.objects.get(id__exact='5')
				print "get_workitem_status", get_workitem_status


				dailytask.workitem_status = get_workitem_status
				dailytask.time_in_min = time_diff
				
				items_completed = request.POST['number_of_workitems_completed']
				print "number_of_workitems_completed", items_completed
				workitem = WorkItem.objects.get(file_name=obj)
				print " printing workitem name", workitem
				workitem.number_of_workitems_completed = items_completed
				workitem.save()

				dailytask.save()
			except ValueError as e:

				messages.add_message(request, messages.INFO, e)
			except WorkItemAssignment.DoesNotExist:
				pass

			except WorkItem.MultipleObjectsReturned:
				pass


			response = HttpResponseRedirect("../")
			
			self.message_user(request, msg)
			return response

		if "send" in request.POST:
			# handle the action on your obj
			redirect_url = reverse('admin:%s_%s_change' %
							   (opts.app_label, opts.model_name),
							   args=(pk_value,),
							   current_app=self.admin_site.name)
			redirect_url = add_preserved_filters({'preserved_filters': preserved_filters, 'opts': opts}, redirect_url)
			return HttpResponseRedirect(redirect_url)
		else:
			return super(WorkItemAssignmentAdmin, self).response_change(request, obj)

admin.site.register(NormalWorkItemAssignment, WorkItemAssignmentAdmin)



class QcAttributeInline(admin.StackedInline):
	'''
	Tabular Inline View for ProjectService
	'''

	form = QcAttributeForm
	model = QcAttribute
	#suit_classes = 'suit-tab suit-tab-qcattribute'
	#form = ProjectServiceInlineForm
	# min_num = 3
	max_num = 1
	extra = 1
	# raw_id_fields = (,)

	list_display = (
		'workitem',
	)
	list_filter = ('workitem',)

	"""
	#fields = ['qc_attribute1', 'qc_attribute2',]
	def get_form(self, request, obj=None, **kwargs):
		form_fields = super(QcAttributeInline, self).get_form(request, obj=None, **kwargs)
		print kwargs
		
		try:
			workitem_obj_id = request.resolver_match.args[0]
			print "workitem_obj_id", workitem_obj_id
			get_workitem = WorkItemAssignment.objects.get(id=workitem_obj_id)

			get_project_task = ProjectTask.objects.get(workitem__file_name__exact=get_workitem)
			print "project task", get_project_task
			try:
				project = Project.objects.get(projecttask=get_project_task)
				print "printing project name", project
	
				qcattribute_template = QcAttributeTemplate.objects.get(project=project)
				print "qcattribute_template", qcattribute_template
				print "qcattribute_template.qc_attribute_field1", qcattribute_template.qc_attribute_field1

				if db_field.name == 'qc_attribute1':
					kwargs.update({
						'required': False,
						'label': 'asfisdnisd'
						})

					return db_field.form_fields(**kwargs)

			except QcAttributeTemplate.DoesNotExist:
				pass

				
				#self.fields['qc_attribute1'].label = qcattribute_template.qc_attribute_field1
			except Project.DoesNotExist:
				pass


		except IndexError:
			pass
		return form_fields
	"""




class QcWorkItemAssignmentAdmin(admin.ModelAdmin):

	inlines=(QcAttributeInline, )

	list_display_links = (u'id','workitem')
	list_display = (
		u'id',
		#'created',
		#'modified',
		'workitem',
		'lead',
		'associates',
		#'workitem_status',
		#'is_qc_required',
		'start',
		'end',
		'qc_agent',
		'qc_status',
		'error_percent',
	)
	list_filter = (
		#'created',
		#'modified',
		'start',
		'end',
		#('workitem',RelatedOnlyFieldListFilter),
		('lead', RelatedOnlyFieldListFilter),
		# ('agent', RelatedOnlyFieldListFilter),
		'workitem_status',
		'qc_status',
	)

	search_fields = ['workitem__file_name','lead__name', 'agents__name']

	form = QcAssignmentForm


	agent_readonly_fields = ('lead',  'agents', 'workitem', 'created', 'modified', )

	qc_readonly_fields = ( 'workitem', 'lead','agents','qc_agent', 'is_qc_required', )
	

	fieldsets = [
			 ('QcAssignment', {
			#'classes': ('suit-tab', 'suit-tab-qcassignment',),
			'fields': ['workitem', 'start', 'end','lead', 'qc_agent', 'qc_status', 'error_percent']
			}),

		]

	#suit_form_tabs = (('qcassignment', 'QcAssignment'), ('qcattribute', 'QcAttribute'),)

   
	def formfield_for_foreignkey(self, db_field, request, **kwargs):
		if db_field.name=='workitem':
			if not request.user.is_superuser:
				proj_tasks_ids = [pt.id for pt in ProjectTask.objects.filter(project__projectservice__operations_manager__user=request.user)]
				print "projecttask ids", proj_tasks_ids
				kwargs['queryset'] = WorkItem.objects.filter(project_task_id__in=proj_tasks_ids)
		
		if db_field.name == "qc_agent":
			kwargs["queryset"] = Employee.objects.filter(roles__title__exact='quality control')
		
		if db_field.name == "lead":
			kwargs['queryset'] =Employee.objects.filter(roles__title__in = ['project lead', 'team lead']).distinct()
		return super(QcWorkItemAssignmentAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

	def formfield_for_manytomany(self, db_field, request, **kwargs):
		if db_field.name == "agents":
			kwargs["queryset"] = Employee.objects.filter(roles__title__exact='agent' )
		return super(QcWorkItemAssignmentAdmin, self).formfield_for_manytomany(db_field, request, **kwargs)

	def get_readonly_fields(self, request, obj=None):
		actions = super(QcWorkItemAssignmentAdmin, self).get_readonly_fields(request, obj=obj)
		
		if request.user.groups.filter(name='agent').exists():
			return self.agent_readonly_fields

		elif request.user.groups.filter(name='customer').exists():
			return self.agent_readonly_fields

		elif request.user.groups.filter(name='qc').exists():
			return self.qc_readonly_fields

		else:
			return actions


	def queryset(self, request):

		qs = super(QcWorkItemAssignmentAdmin, self).queryset(request)
		if request.user.is_superuser:
			# It is mine, all mine. Just return everything.
			return qs

		groups=request.user.groups.all()
		group_dict = dict([ (grp.name, grp)  for  grp in groups])

		if 'management' in  group_dict :
			return qs

		elif 'lead' in group_dict:
			return qs.filter(lead__user = request.user)

		elif 'agent' in group_dict:
			return qs.filter(agent__user = request.user)

		elif 'operations manager' in group_dict:
			opmgr_work_items = WorkItem.objects.filter(project_task__project_service__operations_manager__user=request.user)
			opmgr_workitems_ids = [work.id for work in opmgr_work_items]
			print "opmgr_workitems_ids", opmgr_workitems_ids
			return qs.filter(workitem__id__in = opmgr_workitems_ids)

		elif 'customer' in group_dict:
			work_items = WorkItem.objects.filter(project_task__project_service__project__customer__user =request.user)
			workitems_ids= [ work.id for work in work_items]
			print " customer work items", workitems_ids
			return qs.filter(workitem__id__in = workitems_ids)
		return qs




admin.site.register(QcWorkItemAssignment, QcWorkItemAssignmentAdmin)


class ProjectTaskInline(admin.TabularInline):
	'''
	Tabular Inline View for ProjectTask
	'''
	model = ProjectTask
	form = ProjectTaskInlineForm
	# min_num = 3
	# max_num = 20
	extra = 1
	#suit_classes = 'suit-tab suit-tab-projecttask'
	# raw_id_fields = (,)
	list_display = (
		'title',
		'description',
		#'slug',
		'scope_of_work',
		'project_service',
		'customer_ftp_path',
		'internal_server_path',
		'start',
		'end',
	)
	list_filter = ('created', 'modified', 'start', 'end', 'project_service')
	search_fields = ('slug',)



class ProjectServiceAdmin(admin.ModelAdmin):
	inlines = (ProjectTaskInline,)
	
	list_display = (
	   # u'id',
		'project',
		'industry',
		# 'service',
		'operations_manager'
	)
	list_filter = (
		('project', RelatedOnlyFieldListFilter),
		'industry', 
		('operations_manager', RelatedOnlyFieldListFilter,)
	)
	list_select_related = ('operations_manager',)

	form = ProjectServiceAdminForm
	
	fieldsets = [
		('Project Service', {
			#'classes': ('suit-tab', 'suit-tab-project_service',),
			'fields': ['project','industry',]
		}),
		('Operations Manager', {
			#'classes': ('suit-tab', 'suit-tab-project_service',),
			'fields': ['operations_manager',]
		}),
	   
	]

	#suit_form_tabs = (('project_service', 'ProjectService'), ('projecttask', 'ProjectTask'))

	#form = ProjectServiceInlineForm
	def get_form(self, request, obj=None, **kwargs):
		self._request = request
		return super(ProjectServiceAdmin, self).get_form(request, obj=None, **kwargs)

	@property
	def suit_form_tabs(self):
		if self._request.user.groups.filter(name='sales manager').exists():
			tabs = (('project_service', 'ProjectService'), )
		else:
			tabs = (('project_service', 'ProjectService'),('projecttask', 'ProjectTask'),)
		return tabs


	def formfield_for_foreignkey(self, db_field, request=None,  **kwargs):
		if db_field.name =='project':
			if not request.user.is_superuser:
				kwargs['queryset'] = Project.objects.filter(projectservice__operations_manager__user=request.user)
		"""
		if db_field.name =='service':
			if not request.user.is_superuser:
				pro_service_ids = [s.id for s in ProjectService.objects.filter(operations_manager__user=request.user)]
				kwargs['queryset'] = Service.objects.filter(id__in = pro_service_ids)
		"""
		if db_field.name =='operations_manager':
			kwargs['queryset'] = Employee.objects.filter(roles__title__exact='operations manager')
		return super(ProjectServiceAdmin, self).formfield_for_foreignkey(db_field, request=request,  **kwargs)

	def queryset(self, request):

		qs = super(ProjectServiceAdmin, self).queryset(request)
		if request.user.is_superuser:
			# It is mine, all mine. Just return everything.
			return qs

		groups=request.user.groups.all()

		group_dict = dict([(grp.name, grp) for  grp in groups])

		# print  group_dict

		if 'management' in  group_dict:
			return qs

		elif 'sales manager' in group_dict:
			return qs.filter(project__sales_manager__user=request.user)

		elif 'operations manager' in group_dict:
			return qs.filter(operations_manager__user = request.user)

		return qs    

admin.site.register(ProjectService, ProjectServiceAdmin)



class ProjectTaskTemplateAdmin(admin.ModelAdmin):
	list_display = (u'project', )
	form = ProjectTaskTemplateForm
	prepopulated_fields = { 'custom_field1_slug': ('custom_field1_title',),
							'custom_field2_slug': ('custom_field2_title',),
							'custom_field3_slug': ('custom_field3_title',),
							'custom_field4_slug': ('custom_field4_title',),
							'custom_field5_slug': ('custom_field5_title',),
							'custom_field6_slug': ('custom_field6_title',),
							'custom_field7_slug': ('custom_field7_title',),
							'custom_field8_slug': ('custom_field8_title',),
							'custom_field9_slug': ('custom_field9_title',),
							'custom_field10_slug': ('custom_field10_title',)
						}
	def formfield_for_foreignkey(self,db_field, request, **kwargs):
		if db_field.name == 'project':
			if not request.user.is_superuser:
				kwargs['queryset'] = Project.objects.filter(projectservice__operations_manager__user=request.user)

		return super(ProjectTaskTemplateAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

	def queryset(self, request):

		qs = super(ProjectTaskTemplateAdmin, self).queryset(request)
		if request.user.is_superuser:
			# It is mine, all mine. Just return everything.
			return qs

		groups=request.user.groups.all()

		group_dict = dict([ (grp.name, grp)  for  grp in groups])

		# print  group_dict

		if 'operations manager' in group_dict:

			return qs.filter(project__projectservice__operations_manager__user=request.user)
			
		return qs
admin.site.register(ProjectTaskTemplate, ProjectTaskTemplateAdmin)


class ProjectWorkItemTemplateAdmin(admin.ModelAdmin):
	list_display = (u'project', )
	form = ProjectWorkItemTemplateForm
	prepopulated_fields = { 'custom_field1_slug': ('custom_field1_title',),
							'custom_field2_slug': ('custom_field2_title',),
							'custom_field3_slug': ('custom_field3_title',),
							'custom_field4_slug': ('custom_field4_title',),
							'custom_field5_slug': ('custom_field5_title',),
							'custom_field6_slug': ('custom_field6_title',),
							'custom_field7_slug': ('custom_field7_title',),
							'custom_field8_slug': ('custom_field8_title',),
							'custom_field9_slug': ('custom_field9_title',),
							'custom_field10_slug': ('custom_field10_title',)
					}

	def formfield_for_foreignkey(self,db_field, request, **kwargs):
		if db_field.name == 'project':
			if not request.user.is_superuser:
				kwargs['queryset'] = Project.objects.filter(projectservice__operations_manager__user=request.user)

		return super(ProjectWorkItemTemplateAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

	def queryset(self, request):

		qs = super(ProjectWorkItemTemplateAdmin, self).queryset(request)
		if request.user.is_superuser:
			# It is mine, all mine. Just return everything.
			return qs

		groups=request.user.groups.all()

		group_dict = dict([ (grp.name, grp)  for  grp in groups])

		# print  group_dict

		if 'operations manager' in group_dict:

			return qs.filter(project__projectservice__operations_manager__user=request.user)
			
		return qs
  
admin.site.register(ProjectWorkItemTemplate, ProjectWorkItemTemplateAdmin)


class QcAttributeAdmin(admin.ModelAdmin):

	form = QcAttributeForm
	list_display = (u'id','dailytask',)


	def formfield_for_foreignkey(self,db_field, request, **kwargs):
		if db_field.name == 'dailytask':
			if not request.user.is_superuser:
				workitem_ids = [w.id for w in WorkItem.objects.filter(project_task__project__projectservice__operations_manager__user=request.user)]
				print "printing workitem ids", workitem_ids
				kwargs['queryset'] = WorkItemAssignment.objects.filter(workitem_id__in=workitem_ids)

		return super(QcAttributeAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

	def queryset(self, request):

		qs = super(QcAttributeAdmin, self).queryset(request)
		if request.user.is_superuser:
			# It is mine, all mine. Just return everything.
			return qs

		groups=request.user.groups.all()

		group_dict = dict([ (grp.name, grp)  for  grp in groups])

		# print  group_dict

		if 'operations manager' in group_dict:
			#workitem_assignments = WorkItemAssignment.objects.filter()

			return qs.filter(dailytask__workitem__project_task__project__projectservice__operations_manager__user=request.user)
			
		return qs


admin.site.register(QcAttribute, QcAttributeAdmin)

class QcAttributeTemplateAdmin(admin.ModelAdmin):
	form = QcAttributeTemplateForm
	list_display = ('project',)

	def formfield_for_foreignkey(self,db_field, request, **kwargs):
		if db_field.name == 'project':
			if not request.user.is_superuser:
				kwargs['queryset'] = Project.objects.filter(projectservice__operations_manager__user=request.user)

		return super(QcAttributeTemplateAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)


	def queryset(self, request):

		qs = super(QcAttributeTemplateAdmin, self).queryset(request)
		if request.user.is_superuser:
			# It is mine, all mine. Just return everything.
			return qs

		groups=request.user.groups.all()

		group_dict = dict([ (grp.name, grp)  for  grp in groups])

		# print  group_dict

		if 'operations manager' in group_dict:

			return qs.filter(project__projectservice__operations_manager__user=request.user)
			
		return qs
admin.site.register(QcAttributeTemplate, QcAttributeTemplateAdmin)




