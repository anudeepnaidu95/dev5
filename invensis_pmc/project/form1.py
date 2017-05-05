# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django import forms

from django.contrib.admin import widgets
	

from employee.models import Employee, EmployeeRole
from customer.models import Customer

from  project import models


class ServiceTypeForm(forms.ModelForm):

	class Meta:
		model = models.ServiceType
		fields = '__all__'


class IndustryForm(forms.ModelForm):
	#services = forms.MultipleChoiceField(queryset=models.ServiceType.objects.all())
	class Meta:
		model = models.Industry
		fields = '__all__'


class ProjectTypeForm(forms.ModelForm):

	class Meta:
		model = models.ProjectType
		fields = '__all__'


class BillingTypeForm(forms.ModelForm):

	class Meta:
		model = models.BillingType
		fields = '__all__'


class ProjectTaskForm(forms.ModelForm):
	
	class Meta:
		model = models.ProjectTask
		fields = '__all__'


class WorkItemForm(forms.ModelForm):
	
	class Meta:
		model = models.WorkItem
		fields = '__all__'

		
class WorkItemAssignmentForm(forms.ModelForm):
	
	class Meta:
		model = models.WorkItemAssignment
		fields = '__all__'


class QcAssignmentForm(forms.ModelForm):
	
	class Meta:
		model = models.WorkItemAssignment
		fields = '__all__'


class ServiceSlaForm(forms.ModelForm):
	
	class Meta:
		model = models.ServiceSla
		fields = ('service','sla_type', 'sla_value',)
		#exclude = ('service',)

class SlaForm(forms.ModelForm):
	
	class Meta:
		model = models.Sla
		fields = '__all__'



class ServiceDocumentForm(forms.ModelForm):
	
	class Meta:
		model = models.ServiceDocument
		fields = ('service','document_type','document',)
		#exclude = ('service',)

class AssignServiceLeadForm(forms.ModelForm):

	class Meta:
		model = models.AssignServiceLead 
		fields = ('lead', )
		exclude = ('service', )

	def __init__(self, *args, **kwargs):
		request = kwargs.pop('request', None)
		print "request", request
		super(AssignServiceLeadForm, self).__init__(*args, **kwargs)

		empl_role = EmployeeRole.objects.filter(role='lead').values_list('employee_id', flat=False)
		
		if request.user.groups.filter(name="operations manager"):
			ops_empl = Employee.objects.get(user__username=request.user)
			self.fields['lead'].queryset = ops_empl.get_children()


class ServiceSlaInlineForm(forms.ModelForm):
	
	class Meta:
		model = models.ServiceSla
		fields = ('sla_type', 'sla_value',)
		exclude = ('service',)




class ServiceDocumentInlineForm(forms.ModelForm):
	share_with_others = forms.BooleanField(required=False,initial=False)
	class Meta:
		model = models.ServiceDocument
		fields = ('document_type','document','share_with_others', 'other_document_type')
		exclude = ('service',)

	#def __init__(self, *args, **kwargs):

		#super(ServiceDocumentInlineForm, self).__init__(*args, **kwargs)

		#if document_type == 'other':
		    #self.fields['other_document_type'] = forms.CharField(required=False))

	def clean(self):
		super(ServiceDocumentInlineForm, self).clean()

		for field in ['document_type']:
			if not self.cleaned_data.get(field, ''):
				msg = forms.ValidationError("This field is required.")
				self.add_error(field, msg)



class ServiceResourcePlanInlineForm(forms.ModelForm):

	class Meta:
		model = models.ServiceResourcePlan
		fields = ('experience_slab', 'number_of_resources', 'output_count_per_resource')
		exclude = ('service',)

	def clean(self):
		super(ServiceResourcePlanInlineForm, self).clean()

		for field in ['number_of_resources', 'output_count_per_resource']:
			if not self.cleaned_data.get(field, ''):
				msg = forms.ValidationError("This field is required.")
				self.add_error(field, msg)


time_widget = forms.widgets.TimeInput(attrs={'class': 'timepicker',})
time_widget.format = '%I:%M %p'
	

from employee.models import EmployeeRole
class ServiceForm(forms.ModelForm):
	customer_currency_type =  forms.CharField(widget=forms.TextInput(attrs={'readonly':'readonly'}),required=False)
	workhours_start =  forms.TimeField(widget=forms.TimeInput(format='%I:%M %p'),required=False)
	workhours_end =  forms.TimeField(widget=forms.TimeInput(format='%I:%M %p'),required=False)
	class Meta:
		model = models.Service

		fields = ('title','customer', 'shift_timings', 'scope_of_work', 'statement_of_procedure', 'project_type',
					'number_of_resources', 'billing_interval_in_days', 'billing_type', 'amount_per_billing_type',
					'service_type', 'operations_manager', 'workweek_days', 'workweek_start', 'workweek_end', 
					'daily_work_hours', 'workhours_start', 'workhours_end', 'projected_prj_value_per_month', 'projected_prj_value_per_annum',
					'no_of_man_hours_per_month', 'tx_volume_duration_type', 'projected_tx_volume_per_day', 'projected_tx_volume_per_week', 
					'projected_tx_volume_per_month', 'fte_cost_per_month', 'key_notes',  'conversion_rate', 'customer_currency_type'
			)

	def __init__(self, *args, **kwargs):
		print kwargs
		customer = kwargs.pop('customer', None)
		print "customer", customer
		billing_choice = kwargs.pop('billing_choice', None)
		print "billing_choice", billing_choice
		super(ServiceForm, self).__init__(*args, **kwargs)
		self.fields['title'].label = "Project Name"
		self.fields['workweek_days'].widget = forms.TextInput(attrs={'readonly':'readonly'})
		self.fields['daily_work_hours'].widget = forms.TextInput(attrs={'readonly':'readonly'})
		self.fields['tx_volume_duration_type'].label = 'Estimated transactions'
		#self.fields['projected_prj_value_per_month']   = forms.IntegerField(label='Projected Project Value Per Month', required=False, initial=0)
		#self.fields['projected_prj_value_per_annum']  = forms.IntegerField(label='Projected Project Value Per Annum', required=False, initial=0)
		#self.fields['fte_cost_per_month'] = forms.IntegerField(label='Projected Transactions Per Month', required=False, initial=0)

		empl_role = EmployeeRole.objects.filter(role='ops_manager').values_list('employee_id', flat=False)
		self.fields['operations_manager'].queryset = Employee.objects.filter(id__in=empl_role)
		self.fields['billing_interval_in_days'].required = False
		#self.fields['amount_per_billing_type'] = forms.IntegerField(label='Pricing', required=False)
		self.fields['projected_tx_volume_per_day']   = forms.IntegerField(label='Projected Transactions Per Day', required=False)
		self.fields['projected_tx_volume_per_week']  = forms.IntegerField(label='Projected Transactions Per Week', required=False)
		self.fields['projected_tx_volume_per_month'] = forms.IntegerField(label='Projected Transactions Per Month', required=False)

		try:
			customer_name = Customer.objects.get(title=customer)
			self.fields['customer_currency_type'].initial = customer_name.currency
		except Customer.DoesNotExist:
			pass
		"""
		if billing_choice == 'per_fte':
			self.fields['no_of_man_hours_per_month'].widget = forms.HiddenInput()
			self.fields['tx_volume_duration_type'].widget = forms.HiddenInput()
			self.fields['projected_tx_volume_per_day'].widget = forms.HiddenInput()
			self.fields['projected_tx_volume_per_week'].widget = forms.HiddenInput()
			self.fields['projected_tx_volume_per_month'].widget = forms.HiddenInput()

		elif billing_choice == 'per_hour':
			self.fields['no_of_man_hours_per_month'] = forms.IntegerField(required=True)
			self.fields['tx_volume_duration_type'].widget = forms.HiddenInput()
			self.fields['projected_tx_volume_per_day'].widget = forms.IntegerField(label='Projected Transactions Per Day', required=False)
			self.fields['projected_tx_volume_per_week'].widget = forms.IntegerField(label='Projected Transactions Per Week', required=False)
			self.fields['projected_tx_volume_per_month'].widget = forms.IntegerField(label='Projected Transactions Per Month', required=False)
		
		elif billing_choice == 'per_tx':
			self.fields['tx_volume_duration_type']       = forms.IntegerField(label='Estimated transactions', required=True)
			self.fields['projected_tx_volume_per_day']   = forms.IntegerField(label='Projected Transactions Per Day', required=True)
			self.fields['projected_tx_volume_per_week']  = forms.IntegerField(label='Projected Transactions Per Week', required=True)
			self.fields['projected_tx_volume_per_month'] = forms.IntegerField(label='Projected Transactions Per Month', required=True)
		else:
			pass
		"""


	def clean(self):
		cleaned_data = super(ServiceForm, self).clean()
		customer_currency = cleaned_data.get('customer_currency_type')
		billing_choice = cleaned_data.get('billing_type')

		if customer_currency not in['USD', '']:
			for field in ['conversion_rate']:
				if not self.cleaned_data.get(field, ''):
					msg = forms.ValidationError("This field is required.")
					self.add_error(field, msg)
		"""
		if billing_choice == 'per_hour':
			for field in ['no_of_man_hours_per_month',]:
				msg = forms.ValidationError("This field is required")
				self.add_error(field, msg)
		elif billing_choice == 'per_tx':
			for field in ['tx_volume_duration_type','projected_tx_volume_per_day','projected_tx_volume_per_week', 'projected_tx_volume_per_month']:
				msg = forms.ValidationError("This field is required")
				self.add_error(field, msg)
		else:
			pass
		"""
class OpsMgrServiceForm(forms.ModelForm):
	workhours_start =  forms.TimeField(widget=forms.TimeInput(format='%I:%M %p'),required=False)
	workhours_end =  forms.TimeField(widget=forms.TimeInput(format='%I:%M %p'),required=False)
	class Meta:
		model = models.Service
		fields = ('title','customer', 'shift_timings', 'scope_of_work', 'statement_of_procedure', 'project_type',
					'number_of_resources', 'billing_interval_in_days', 'billing_type', 'amount_per_billing_type',
					'service_type', 'operations_manager', 'workweek_days', 'workweek_start', 'workweek_end', 
					'daily_work_hours', 'workhours_start', 'workhours_end', 'projected_prj_value_per_month', 'projected_prj_value_per_annum',
					'no_of_man_hours_per_month', 'tx_volume_duration_type', 'projected_tx_volume_per_day', 'projected_tx_volume_per_week', 
					'projected_tx_volume_per_month', 'fte_cost_per_month', 'key_notes',
			)
		exclude = ('operations_manager', 'billing_interval_in_days', 'projected_prj_value_per_month','projected_prj_value_per_annum','fte_cost_per_month',
					'amount_per_billing_type',
				)

	def __init__(self, *args, **kwargs):

		super(OpsMgrServiceForm, self).__init__(*args, **kwargs)
		
		self.fields['workweek_days'].widget = forms.TextInput(attrs={'readonly':'readonly'})
		self.fields['daily_work_hours'].widget = forms.TextInput(attrs={'readonly':'readonly'})
		

		self.fields['tx_volume_duration_type'].label = 'Estimated transactions'
		self.fields['projected_tx_volume_per_day'].label='Projected Transactions Per Day'
		self.fields['projected_tx_volume_per_week'].label= 'Projected Transactions Per Week'
		self.fields['projected_tx_volume_per_month'].label= 'Projected Transactions Per Month'



		
class ServiceResourcePlanForm(forms.ModelForm):
	class Meta:
		model = models.ServiceResourcePlan
		fields = ('service','experience_slab', 'number_of_resources', 'output_count_per_resource')
		#exclude = ('service',)

	def __init__(self, *args, **kwargs):
		super(ServiceResourcePlanForm, self).__init__(*args, **kwargs)

		self.fields['output_count_per_resource'].label = 'Target'

	def clean(self):
		super(ServiceResourcePlanForm, self).clean()

		for field in ['experience_slab', 'number_of_resources', 'output_count_per_resource']:
			if not self.cleaned_data.get(field, ''):
				msg = forms.ValidationError("This field is required.")
				self.add_error(field, msg)


class TaskForm(forms.ModelForm):

	start = forms.DateTimeField(label = 'Start Date' , input_formats=['%Y-%m-%d %H:%M:%S', '%d/%m/%Y'])
	end = forms.DateTimeField(label = 'End Date' ,input_formats=['%Y-%m-%d %H:%M:%S', '%d/%m/%Y'])

	class Meta:
		model = models.Task

		fields = ('title', 'folderpath', 'no_of_txs', 'scope_of_work', 'start', 'end')
	
	   
	def __init__(self, *args, **kwargs):
		super(TaskForm, self).__init__(*args, **kwargs)

		self.fields['title'].widget = forms.TextInput(attrs={'readonly':'readonly'})
		self.fields['folderpath'].required = True
		self.fields['no_of_txs'].required = True

		
	def clean(self):
		super(TaskForm, self).clean()

		for field in ['no_of_txs',]:
			if not self.cleaned_data.get(field, ''):
				msg = forms.ValidationError("This field is required.")
				self.add_error(field, msg)
	
class TaskResourcePlanForm(forms.ModelForm):
	
	class Meta:
		model = models.TaskResourcePlan
		fields = ('experience_slab', 'number_of_resources', 'output_count_per_resource',)
		exclude = ('task',)
	def __init__(self,*args,**kwargs):
		super(TaskResourcePlanForm,self).__init__(*args,**kwargs)
		self.fields['output_count_per_resource'].label='Target'


class LeadTaskForm(forms.ModelForm):
	
	class Meta:
		model = models.LeadTask
		fields = ('lead', 'filename', 'no_of_txs',)
		#exclude = ('task',)
	def __init__(self, *args, **kwargs):
		request = kwargs.pop('request', None)
		print "request user", request.user
		super(LeadTaskForm, self).__init__(*args, **kwargs)
		empl_role = EmployeeRole.objects.filter(role='lead').values_list('employee_id',flat=True)
		#self.fields['lead'].queryset = Employee.objects.filter(id__in=empl_role)

		self.fields['filename'].label='File Path'
		self.fields['lead'].required = True
		#self.fields['filename'].required = True
		#self.fields['no_of_txs'].required = True
		current_employ = Employee.objects.get(user__username=request.user)
		if request.user.groups.filter(name="lead").exists():
			reporting_manager = current_employ.parent
			self.fields['lead'].queryset = reporting_manager.get_children()

		if request.user.groups.filter(name="operations manager").exists():
			self.fields['lead'].queryset = current_employ.get_children()


	def clean(self):
		super(LeadTaskForm, self).clean()

		for field in ['filename','no_of_txs',]:
			if not self.cleaned_data.get(field, ''):
				msg = forms.ValidationError("This field is required.")
				self.add_error(field, msg)



class LeadTaskResourceInlineForm(forms.ModelForm):
	
	class Meta:
		model = models.LeadTaskResourcePlan
		fields = ('experience_slab', 'number_of_resources', 'output_count_per_resource',)
		exclude = ('lead_task',)

	def clean(self):
		super(LeadTaskResourceInlineForm, self).clean()

		for field in ['number_of_resources', 'output_count_per_resource',]:
			if not self.cleaned_data.get(field, ''):
				msg = forms.ValidationError("This field is required.")
				self.add_error(field, msg)


class StaffTaskInlineForm(forms.ModelForm):
	is_qc_required = forms.BooleanField(required=False,initial=False)
	class Meta:
		model = models.StaffTask
		fields = ('staff', 'filename', 'no_of_txs','is_qc_required','qc_lead','priority', 'status')
		exclude = ('lead_task',)

	def __init__(self, *args, **kwargs):

		request = kwargs.pop('request', None)
		#print 'my user', self.user

		super(StaffTaskInlineForm, self).__init__(*args, **kwargs)

		# try:
		# 	emp_lead = Employee.objects.get(user__username=self.user)
		# 	agent_emps = emp_lead.get_children()

		# 	empl_role = EmployeeRole.objects.filter(role='staff').values_list('employee_id', flat=True)
		# 	#self.fields['staff'].queryset = Employee.objects.filter(id__in=empl_role)
		# 	self.fields['staff'].queryset = agent_emps
		# except KeyError:
		# 	pass

		empl_role = EmployeeRole.objects.filter(role='qc').values_list('employee_id', flat=True)
		self.fields['qc_lead'].queryset = Employee.objects.filter(id__in=empl_role)
		#self.fields['lead'].required = False
		self.fields['filename'].required = False
		self.fields['no_of_txs'].required = False

		current_emp = Employee.objects.get(user__username=request.user)
		if request.user.groups.filter(name='operations manager'):
			self.fields['staff'].queryset = current_emp.get_descendants()
		if request.user.groups.filter(name='lead'):
			current_emp_manager = current_emp.parent
			self.fields['staff'].queryset = current_emp_manager.get_descendants()


	def clean(self):
		cleaned_data = super(StaffTaskInlineForm, self).clean()
		is_qc_required = cleaned_data.get('is_qc_required')
		qc_lead = cleaned_data.get('qc_lead')
		print "is_qc_required", is_qc_required

		for field in ['filename', 'no_of_txs']:
			if not self.cleaned_data.get(field, ''):
				msg = forms.ValidationError("This field is required.")
				self.add_error(field, msg)
		if is_qc_required:
			for field in ['qc_lead']:
				if not self.cleaned_data.get(field, ''):
					msg = forms.ValidationError("This field is required.")
					self.add_error(field, msg)

		if qc_lead:
			for field in ['is_qc_required']:
				if not self.cleaned_data.get(field, ''):
					msg = forms.ValidationError("This field is required.")
					self.add_error(field, msg)




class StaffTaskForm(forms.ModelForm):
	
	class Meta:
		model = models.StaffTask
		fields = ('status', 'no_of_txs_completed',)


class QcTaskForm(forms.ModelForm):
	
	class Meta:
		model = models.StaffTask
		fields = ('error_percent','no_of_errors','error_description',)


class QcTemplateForm(forms.ModelForm):
	
	class Meta:
		model = models.QcTemplate
		fields = '__all__'



class StaffTaskQcForm(forms.ModelForm):

	"""docstring for StaffTaskQc"""

	class Meta:
		model = models.StaffTaskQc
		fields = '__all__'
		exclude = ('staff_task',)

	
	def __init__(self, *arg, **kwargs):
		service = kwargs.pop('service_name', None)
		print "service", service
		super(StaffTaskQcForm, self).__init__(*arg, **kwargs)
		
		try:
			get_task_project = models.Service.objects.filter(title=service)
			print "get_task_project", get_task_project

			qcattribute_template = models.QcTemplate.objects.get(service=get_task_project)
			print "qcattribute_template", qcattribute_template

			qc_attribute1  =  self.get_field_mapping('qc_attribute1',qcattribute_template.qc_attribute_field1)
			qc_attribute2  =  self.get_field_mapping('qc_attribute2',qcattribute_template.qc_attribute_field2)
			qc_attribute3  =  self.get_field_mapping('qc_attribute3',qcattribute_template.qc_attribute_field3)
			qc_attribute4  =  self.get_field_mapping('qc_attribute4',qcattribute_template.qc_attribute_field4)
			qc_attribute5  =  self.get_field_mapping('qc_attribute5',qcattribute_template.qc_attribute_field5)
			qc_attribute6  =  self.get_field_mapping('qc_attribute6',qcattribute_template.qc_attribute_field6)
			qc_attribute7  =  self.get_field_mapping('qc_attribute7',qcattribute_template.qc_attribute_field7)
			qc_attribute8  =  self.get_field_mapping('qc_attribute8',qcattribute_template.qc_attribute_field8)
			qc_attribute9  =  self.get_field_mapping('qc_attribute9',qcattribute_template.qc_attribute_field9)
			qc_attribute10 =  self.get_field_mapping('qc_attribute10',qcattribute_template.qc_attribute_field10)

			qc_attribute11 =  self.get_field_mapping('qc_attribute11',qcattribute_template.qc_attribute_field11)
			qc_attribute12 =  self.get_field_mapping('qc_attribute12',qcattribute_template.qc_attribute_field12)
			qc_attribute13 =  self.get_field_mapping('qc_attribute13',qcattribute_template.qc_attribute_field13)
			qc_attribute14 =  self.get_field_mapping('qc_attribute14',qcattribute_template.qc_attribute_field14)
			qc_attribute15 =  self.get_field_mapping('qc_attribute15',qcattribute_template.qc_attribute_field15)
			qc_attribute16 =  self.get_field_mapping('qc_attribute16',qcattribute_template.qc_attribute_field16)
			qc_attribute17 =  self.get_field_mapping('qc_attribute17',qcattribute_template.qc_attribute_field17)
			qc_attribute18 =  self.get_field_mapping('qc_attribute18',qcattribute_template.qc_attribute_field18)
			qc_attribute19 =  self.get_field_mapping('qc_attribute19',qcattribute_template.qc_attribute_field19)
			qc_attribute20 =  self.get_field_mapping('qc_attribute20',qcattribute_template.qc_attribute_field20)

			qc_attribute21 =  self.get_field_mapping('qc_attribute21',qcattribute_template.qc_attribute_field21)
			qc_attribute22 =  self.get_field_mapping('qc_attribute22',qcattribute_template.qc_attribute_field22)
			qc_attribute23 =  self.get_field_mapping('qc_attribute23',qcattribute_template.qc_attribute_field23)
			qc_attribute24 =  self.get_field_mapping('qc_attribute24',qcattribute_template.qc_attribute_field24)
			qc_attribute25 =  self.get_field_mapping('qc_attribute25',qcattribute_template.qc_attribute_field25)
			qc_attribute26 =  self.get_field_mapping('qc_attribute26',qcattribute_template.qc_attribute_field26)
			qc_attribute27 =  self.get_field_mapping('qc_attribute27',qcattribute_template.qc_attribute_field27)
			qc_attribute28 =  self.get_field_mapping('qc_attribute28',qcattribute_template.qc_attribute_field28)
			qc_attribute29 =  self.get_field_mapping('qc_attribute29',qcattribute_template.qc_attribute_field29)
			qc_attribute30 =  self.get_field_mapping('qc_attribute30',qcattribute_template.qc_attribute_field30)

		except models.Service.DoesNotExist:
			pass

		except models.QcTemplate.DoesNotExist:
			pass

	def get_field_mapping(self, field, mapping_field):

		if not mapping_field in (None, ''):
			self.fields[field].label = mapping_field
			self.fields[field].required = False 
		else:
			self.fields[field].widget = forms.HiddenInput()


