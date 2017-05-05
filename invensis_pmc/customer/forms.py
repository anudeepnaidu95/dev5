# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import csv, re
from django import forms
from django.forms import DateInput
from django.forms.models import BaseInlineFormSet,inlineformset_factory, formset_factory
from django.forms.formsets import BaseFormSet
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from django_select2.forms import ModelSelect2Widget, ModelSelect2MultipleWidget
from django.forms import TextInput, ModelForm, Textarea, Select
from suit.widgets import SuitDateWidget, SuitSplitDateTimeWidget, \
	EnclosedInput, LinkedSelect, AutosizedTextarea

from employee.models import Employee, EmployeeRole

from project import models
from .models import Customer,Followup , Lead, Country, CurrencyType

from crispy_forms.helper import FormHelper


RE_WHITESPACE = re.compile(u"\s+")

class TitleWidget(ModelSelect2Widget):
	search_fields = [ 'title__icontains', ]

class NameWidget(ModelSelect2Widget):
	search_fields = ['name__icontains']

class UserNameWidget(ModelSelect2Widget):
	search_fields = ['username__icontains']


class NameSelect2MultipleWidget(ModelSelect2MultipleWidget):
	search_fields = [
		'title__icontains',
	]

# Followup1Formset = forms.inlineformset_factory(Lead,
# 						    Followup,
# 						    can_delete=False,
# 						    fields = '__all__',
# 						    #fields=('next_followup', 'lead_status', 'percentage', 'is_converted_to_customer', 'remarks'),
# 						    extra = 1
# 						)



class ExampleFormSetHelper(FormHelper):
	def __init__(self, *args, **kwargs):
		super(ExampleFormSetHelper, self).__init__(*args, **kwargs)
		# self.form_method = 'post'
		# self.layout = Layout(
		#     'favorite_color',
		#     'favorite_food',
		# )
		# self.render_required_fields = True
		self.template = 'bootstrap3/table_inline_formset.html'
		
class FollowupForm1(forms.ModelForm):
	
	class Meta:
		model = Followup
		fields = ('next_followup' ,'lead_status' ,'is_converted_to_customer',  'percentage' , 'remarks', )
		exclude = ('lead',)


	def __init__(self, *args, **kwargs):

		super(FollowupForm1, self).__init__(*args, **kwargs)
		self.fields['next_followup'].widget.attrs['class'] = 'datefield'

		for form in self.fields:
			self.fields[form].empty_permitted = False

	def clean(self):
		super(FollowupForm1, self).clean()

		for field in ['next_followup','lead_status','percentage',]:
			if not self.cleaned_data.get(field, ''):
				msg = forms.ValidationError("This field is required.")
				self.add_error(field, msg)


class LeadForm(forms.ModelForm):
	#lead_date = forms.DateField(label = 'Lead Date' , input_formats=['%Y-%m-%d'])
	lead_date = forms.DateField(label = 'Lead Date' , input_formats=['%d-%m-%Y', '%Y-%m-%d'])


	#email = forms.EmailField(required=False)
	is_converted_to_customer = forms.BooleanField(required=False,initial=False)
	class Meta:
		model = Lead
		
		#fields = '__all__'
		fields = ['title', 'description', 'contact_name', 'designation', 'email', 'phone', 'addressline1',
					'addressline2', 'city', 'state', 'country', 'zip_code', 'industry', 'services', 'requirement',
					'lead_source', 'sales_rep', 'other_lead_source', 'is_converted_to_customer',
					'lead_date', 'owner'

			]

	def __init__(self, *args, **kwargs):

		request = kwargs.pop('request', None)
		print "self.request", request
		super(LeadForm, self).__init__(*args, **kwargs)
		
		
		self.fields['other_lead_source'].label = "If other source please specify"
		self.fields['sales_rep'].label = "Sales Respresentative"

		for form in self.fields:
			self.fields[form].required = True

		self.fields['other_lead_source'].required = False
		#self.fields['description'].required = False

		self.fields['description'] = forms.CharField(label='Company Description', widget=forms.widgets.Textarea(), required = False)
		#Textarea(attrs={'rows': 1,'cols': 40,'style': 'height: 1em;'})

		self.fields['requirement'].required = False
		self.fields['sales_rep'].required = False
		self.fields['is_converted_to_customer'].required = False
		self.fields['addressline1'].required = False
		self.fields['addressline2'].required = False
		self.fields['city'].required = False
		self.fields['state'].required = False

		self.fields['zip_code'].required = False
		self.fields['country'].required = False
		self.fields['lead_date'].required = False

		empl_role = EmployeeRole.objects.filter(role='sales_rep').values_list('employee_id', flat=True)
		self.fields['sales_rep'].queryset = Employee.objects.filter(id__in=empl_role)
		#self.fields['sales_rep'].widget.attrs['disabled'] = 'disabled'
		self.fields['sales_rep'].widget.attrs['readonly'] = True

		empl_role = EmployeeRole.objects.filter(role='sales_manager').values_list('employee_id', flat=True)
		self.fields['owner'].queryset = Employee.objects.filter(id__in=empl_role)
		self.fields['owner'].label = 'Sales Manager'

		if request.user.groups.filter(name='sales manager').exists():
			self.fields['owner'].required= False 


	def clean(self):
		cleaned_data = super(LeadForm, self).clean()
		converted_to_customer = cleaned_data.get("is_converted_to_customer")
		addressline1 = cleaned_data.get('addressline1')
		print "converted_to_customer", converted_to_customer

		if converted_to_customer:
			for field in ['addressline1','country','city', 'state', 'zip_code']:
				if not self.cleaned_data.get(field, ''):
					msg = forms.ValidationError("This field is required.")
					self.add_error(field, msg)



class CustomerForm(forms.ModelForm):
	#industry = forms.ModelChoiceField(label='Industry', queryset=models.Industry.objects.all())
	#services = forms.MultipleChoiceField(label='Services', queryset=models.ServiceType.objects.all())

	class Meta:
		model = Customer
		
		fields = ['title', 'description', 'contact_name', 'designation', 'email', 'phone', 'addressline1',
					'addressline2', 'city', 'state', 'country', 'zip_code', 'industry', 'services', 'requirement',
					'lead_source', 'sales_rep', 'other_lead_source', 'currency', 'last_invoice_no', 'invoice_format',
					'company_name_invoice'

			]
	def __init__(self, *args, **kwargs):
		super(CustomerForm, self).__init__(*args, **kwargs)

		
		for form in self.fields:
			self.fields[form].required = True
		self.fields['other_lead_source'].required = False
		self.fields['description'].required = False
		self.fields['requirement'].required = False
		self.fields['sales_rep'].required = False
		self.fields['lead_source'].required = False
		self.fields['addressline2'].required = False
		
class FollowupAdminForm(forms.ModelForm):
	class Meta:
		model=Followup
		fields='__all__'
		widgets = {
			'customer':TitleWidget,
		}


class FollowupForm(forms.ModelForm):
	
	class Meta:
		model = Followup
		fields = '__all__'
	
class CountryForm(forms.ModelForm):

	class Meta:

		model = Country
		fields = "__all__"

class CurrencyTypeForm(forms.ModelForm):

	class Meta:

		model = CurrencyType
		fields = "__all__"

class ImportLeadForm(forms.Form):
	
	file = forms.FileField(label='CSV')

	class Meta:
		model = Lead
		fields = ('file',)

	def __init__(self, *args, **kwargs):
			super(ImportLeadForm, self).__init__(*args, **kwargs)
			self.max_upload_size = 1024*1024 #1 MB
			self.fileformat = None
			self.filename = None


	def clean_file(self):
		"""Parses the CSV file."""
		file = self.cleaned_data.get("file")
		
		if file:
			try:
				dialect = csv.Sniffer().sniff(file.read(10000), delimiters='\t,;')
				file.seek(0)
				reader = csv.reader(file, dialect)
			  
				try:
					header_row = reader.next()
				except StopIteration:
					raise forms.ValidationError("That CSV file is empty.")
				headers = [RE_WHITESPACE.sub("_", cell.decode("utf-8", "ignore").lower().strip()) for cell in header_row ]
				# Check the required fields.
				if len(headers) == 0:
					raise forms.ValidationError("That CSV file did not contain a valid header line.")

				clean_rows = []
				invalid_rows = []
				invalid_cells = []

			except csv.Error:
				raise forms.ValidationError("Please upload a valid CSV file.")
			# Check that some rows were parsed.
		    
			if not clean_rows and invalid_rows:
				raise forms.ValidationError("No ProjectTasks could be imported, due to errors in that CSV file.")
			# Store the parsed data.
			self.cleaned_data["rows"] = clean_rows
			self.cleaned_data["invalid_rows"] = invalid_rows
		return file