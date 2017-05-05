# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import csv, re
from django import forms
from django.forms import TextInput, ModelForm, Textarea, Select
from django.forms.widgets import HiddenInput
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from django.contrib.admin.widgets import RelatedFieldWidgetWrapper
from suit.widgets import LinkedSelect, AutosizedTextarea,SuitSplitDateTimeWidget,EnclosedInput
from django_select2.forms import ModelSelect2Widget
from django_select2.forms import ModelSelect2MultipleWidget

from employee.models import Employee, Role

from .models import ProjectService, Project, WorkItemAssignment, WorkItem, ProjectTask, QcAttribute
from .models import ProjectTaskTemplate, ProjectWorkItemTemplate, QcAttributeTemplate,ProjectPlanResource

RE_WHITESPACE = re.compile(u"\s+")
class ProjectTaskInlineForm(forms.ModelForm):

	class Meta:
		model = ProjectTask
		fields = ('title','description','project_service','start', 'end')
		
		widgets = {
			#'scope_of_work': AutosizedTextarea(attrs={'class': 'input-medium', 'rows': 2,'style': 'width:95%'}),
			'description': AutosizedTextarea(attrs={'class': 'input-medium', 'rows': 2,'style': 'width:95%'}),
			'title' : TextInput(attrs={'class': 'input-small'}),
		
	   
		}
		

class NameWidget(ModelSelect2Widget):
	search_fields = [
		'name__icontains',
	]

class TitleWidget(ModelSelect2Widget):
	search_fields = [
		'title__icontains',
	]

class ProjectTitleWidget(ModelSelect2Widget):
	search_fields = [
		'title__icontains',
		'project__title__icontains',
	]


class NameSelect2MultipleWidget(ModelSelect2MultipleWidget):
	search_fields = [
		'name__icontains',
	]


class ProjectServiceAdminForm(forms.ModelForm):
	class Meta:
		model = ProjectService
		fields = '__all__'
		widgets = {
			#'operations_manager': NameWidget,
		}

class ProjectPlanResourceAdminForm(forms.ModelForm):
	class Meta:
		model = ProjectPlanResource
		fields = '__all__'
		


class ProjectAdminForm(forms.ModelForm):
	
	class Meta:
		model = Project
		fields = '__all__'

	


class ServiceWidget(ModelSelect2Widget):
	search_fields = [
		'service__title__icontains',
		'project__title__icontains',
	]


class ProjectTaskForm(forms.ModelForm):
	

	class Meta:
		model = ProjectTask
		#fields = '__all__'
		fields = ['project','project_service','title','slug','total_workitems','total_workitems_completed', 'total_time_hours',
					'scope_of_work', 'custom_field1','custom_field2','custom_field3','custom_field4','custom_field5','custom_field6','custom_field7',\
					'custom_field8','custom_field9','custom_field10']
		widgets = {
			'project': TitleWidget,
			'project_service' : ServiceWidget,
		}

	def __init__(self, hide_condition=True, *args, **kwargs):
		
		self.request = kwargs.pop('request', None)
		super(ProjectTaskForm, self).__init__(*args, **kwargs)
	
		try:
			project_task = ProjectTask.objects.get(id=self.instance.pk)
			print project_task
			
			project_name = Project.objects.get(projecttask=project_task)
			print "print me project name", project_name

			project_task_template = ProjectTaskTemplate.objects.get(project=project_name)

			custom_field1 = self.get_field_mapping('custom_field1', project_task_template.custom_field1_title, project_task_template.custom_field1_datatype)
			custom_field2 = self.get_field_mapping('custom_field2', project_task_template.custom_field2_title, project_task_template.custom_field2_datatype)
			custom_field3 = self.get_field_mapping('custom_field3', project_task_template.custom_field3_title, project_task_template.custom_field3_datatype)
			custom_field4 = self.get_field_mapping('custom_field4', project_task_template.custom_field4_title, project_task_template.custom_field4_datatype)
			custom_field5 = self.get_field_mapping('custom_field5', project_task_template.custom_field5_title, project_task_template.custom_field5_datatype)
			custom_field6 = self.get_field_mapping('custom_field6', project_task_template.custom_field6_title, project_task_template.custom_field6_datatype)
			custom_field7 = self.get_field_mapping('custom_field7', project_task_template.custom_field7_title, project_task_template.custom_field7_datatype)
			custom_field8 = self.get_field_mapping('custom_field8', project_task_template.custom_field8_title, project_task_template.custom_field8_datatype)
			custom_field9 = self.get_field_mapping('custom_field9', project_task_template.custom_field9_title, project_task_template.custom_field9_datatype)
			custom_field10 = self.get_field_mapping('custom_field10', project_task_template.custom_field10_title, project_task_template.custom_field10_datatype)

		except ProjectTaskTemplate.DoesNotExist:
			pass
		except Project.DoesNotExist:
			pass
		except ProjectTask.DoesNotExist: 
			pass


	def get_field_mapping(self, field, mapping_field, field_type,):

		if not mapping_field in (None, ''):
			if field_type == 'INTEGER':
				self.fields[field] = forms.IntegerField(required=False, label=mapping_field)
				#self.fields[field].widget.attrs['readonly'] = "readonly"
			elif field_type == 'DECIMAL':
				self.fields[field] = forms.DecimalField(decimal_places=4, max_digits=8, required=False, label=mapping_field)
				#self.fields[field].widget.attrs['readonly'] = "readonly"
			elif field_type == 'DATE':
				self.fields[field] = forms.DateField(required=False, label=mapping_field,input_formats=['%d/%m/%Y','%d-%m-%Y', '%m/%d/%Y','%Y-%m-%d', '%Y%m%d'], widget=forms.DateInput(format = '%d/%m/%Y'))
				#self.fields[field].widget.attrs['readonly'] = "readonly"
			elif field_type == 'DATETIME':
				self.fields[field] = forms.DateTimeField(required=False, label=mapping_field)
				#self.fields[field].widget.attrs['readonly'] = "readonly"
			elif field_type == 'STRING':
				self.fields[field] = forms.CharField(required=False, label=mapping_field)
				#self.fields[field].widget.attrs['readonly'] = "readonly"
			else:
				self.fields[field] = forms.CharField(required=False, label=mapping_field)
				#self.fields[field].widget.attrs['readonly'] = "readonly"
		else:
			self.fields[field].widget = forms.HiddenInput()
			#self.fields[field] = forms.CharField(widget=forms.HiddenInput(attrs={'style': 'display:none;'}), required=False)


class ReadOnlyFieldsMixin(object):
    readonly_fields =()

    def __init__(self, *args, **kwargs):
        super(ReadOnlyFieldsMixin, self).__init__(*args, **kwargs)
        for field in (field for name, field in self.fields.iteritems() if name in self.readonly_fields):
            field.widget.attrs['disabled'] = 'true'
            field.required = False

    def clean(self):
        cleaned_data = super(ReadOnlyFieldsMixin,self).clean()
        for field in self.readonly_fields:
           cleaned_data[field] = getattr(self.instance, field)

        return cleaned_data



class WorkItemAdminForm(forms.ModelForm):
	#start = forms.DateField()
	#end = forms.DateField()
	"""
	project = forms.ModelChoiceField(label='Project', queryset=Project.objects.all(), 
									#widget=forms.TextInput(attrs={'readonly':'readonly'})
								)
	
	project_service = forms.ModelChoiceField(label='Project Service', 
											queryset=Service.objects.all().distinct(),
											#widget=forms.TextInput(attrs={'readonly':'readonly'})
											)
	#project_service = forms.ModelChoiceField(queryset=Service.objects.all(), widget=TitleWidget)
	"""
	#readonly_fields = ('project','project_service','project_task','folder_name', 'file_name')
	class Meta:
		model = WorkItem
		
		fields = ['project_task', 'folder_name', 'file_name', 'number_of_items', 'number_of_workitems_completed', 
				'custom_field1', 'custom_field2', 'custom_field3', 'custom_field4', 'custom_field5','custom_field6',
				'custom_field7', 'custom_field8','custom_field9', 'custom_field10'
			]
	
		widgets = {
			'project_task': ProjectTitleWidget,

		}


	def __init__(self, *args, **kwargs):

		form_fields = kwargs.pop("fields", {})
		self.request = kwargs.pop('request', None)
		super(WorkItemAdminForm, self).__init__(*args, **kwargs)

		try:
			workitem = WorkItem.objects.get(id=self.instance.pk)
			project_task = ProjectTask.objects.get(workitem=workitem)			
			project_name = Project.objects.get(projecttask__title=project_task)
			print "print me project name", project_name
			"""
			self.fields['project'].empty_label = None
			self.fields['project'].queryset = Project.objects.filter(projecttask__title=project_task)
			#self.fields['project'].widget = forms.TextInput(attrs={'readonly':'readonly'})

			self.fields['project_service'].queryset = ProjectService.objects.filter(project__projecttask__title=project_task)
			self.fields['project_service'].empty_label = None
			#self.fields['project_service'].widget = forms.TextInput(attrs={'readonly':'readonly'})
			
			self.fields['project_task'].queryset = ProjectTask.objects.filter(project=self.fields['project'].queryset)
			"""
			project_workitem_template = ProjectWorkItemTemplate.objects.get(project=project_name)
			print "project task project_workitem_template", project_workitem_template

			custom_field1 = self.get_field_mapping('custom_field1', project_workitem_template.custom_field1_title, project_workitem_template.custom_field1_datatype)
			custom_field2 = self.get_field_mapping('custom_field2', project_workitem_template.custom_field2_title, project_workitem_template.custom_field2_datatype)
			custom_field3 = self.get_field_mapping('custom_field3', project_workitem_template.custom_field3_title, project_workitem_template.custom_field3_datatype)
			custom_field4 = self.get_field_mapping('custom_field4', project_workitem_template.custom_field4_title, project_workitem_template.custom_field4_datatype)
			custom_field5 = self.get_field_mapping('custom_field5', project_workitem_template.custom_field5_title, project_workitem_template.custom_field5_datatype)
			custom_field6 = self.get_field_mapping('custom_field6', project_workitem_template.custom_field6_title, project_workitem_template.custom_field6_datatype)
			custom_field7 = self.get_field_mapping('custom_field7', project_workitem_template.custom_field7_title, project_workitem_template.custom_field7_datatype)
			custom_field8 = self.get_field_mapping('custom_field8', project_workitem_template.custom_field8_title, project_workitem_template.custom_field8_datatype)
			custom_field9 = self.get_field_mapping('custom_field9', project_workitem_template.custom_field9_title, project_workitem_template.custom_field9_datatype)
			custom_field10 = self.get_field_mapping('custom_field10', project_workitem_template.custom_field10_title, project_workitem_template.custom_field10_datatype)
				
		except ProjectWorkItemTemplate.DoesNotExist:
			pass
		
		except Project.DoesNotExist:
			pass

		except WorkItem.DoesNotExist:
			pass

		except KeyError:
			pass

	def get_field_mapping(self, field, mapping_field, field_type):

		if not mapping_field in (None, ''):
			if field_type == "INTEGER":
				self.fields[field] = forms.IntegerField(label=mapping_field, required=False)
			elif field_type == "DECIMAL":
				self.fields[field] = forms.DecimalField(label=mapping_field, required=False)
			elif field_type == "DATE":
				self.fields[field] = forms.DateField(label=mapping_field, required=False, input_formats=['%d/%m/%Y', '%m/%d/%Y','%Y-%m-%d'])
				self.fields[field].widget = forms.DateInput(format = '%d/%m/%Y')
			elif field_type == "DATETIME":
				self.fields[field] = forms.DateTimeField(label=mapping_field, required=False)
			elif field_type == "STRING":
				self.fields[field] = forms.CharField(label=mapping_field, required=False)
			else:
				self.fields[field] = forms.CharField(rlabel=mapping_field, equired=False)

		else:
			self.fields[field].widget = forms.HiddenInput()
			#self.fields[field] = forms.CharField(widget=forms.HiddenInput(attrs={'style': 'display:none;'}), required=False)


class FileNameWidget(ModelSelect2Widget):
	search_fields = [
		'file_name__icontains',
	]


class WorkItemAssignmentInlineForm(forms.ModelForm):
	
	class Meta:
		model = WorkItemAssignment
		fields = ('start','end','workitem', 'lead', 'agents', 'workitem_status','time_in_min',)


		widgets = {
			
			'lead': NameWidget(attrs={'class': 'input-small', 'style':'display:inline-grid;'}),
			'agents': NameSelect2MultipleWidget(attrs={'class': 'input-medium', 'style':'display:inline-grid;'}),
			'qc_agent': NameWidget(attrs={'class': 'input-medium', 'style':'display:inline-grid;'}),
			'workitem_status': NameWidget(attrs={'class': 'input-small', 'style':'display:inline-grid;'}),
			'workitem': FileNameWidget,
			'time_in_min' : TextInput(attrs={'class': 'input-small', 'style':'display:inline-grid;'}),
		}

	
class WorkItemAssignmentForm(forms.ModelForm):
	number_of_workitems_completed = forms.IntegerField(required=False)
	class Meta:
		model = WorkItemAssignment
		fields = ('start','end','workitem', 'lead', 'agents', 'workitem_status','time_in_min',)

		widgets = {
			'start': SuitSplitDateTimeWidget,
			'end': SuitSplitDateTimeWidget,
			'lead': NameWidget,
			'agents': NameSelect2MultipleWidget,
			'qc_agent': NameWidget,
			'workitem': FileNameWidget,
		}


class QcAssignmentForm(forms.ModelForm):

	class Meta:
		model = WorkItemAssignment
		fields = ('start','end','workitem', 'lead', 'agents', 'workitem_status', 'is_qc_required','qc_agent','qc_status','error_percent')

		widgets = {
			
			'lead': NameWidget,
			'agents': NameSelect2MultipleWidget,
			'qc_agent': NameWidget,
			'workitem': FileNameWidget,
		}


class ProjectTaskTemplateForm(forms.ModelForm):

	class Meta:
		model = ProjectTaskTemplate
		fields = "__all__"

		widgets = {
			
			'project': TitleWidget,
		}

class ProjectWorkItemTemplateForm(forms.ModelForm):

	class Meta:
		model = ProjectWorkItemTemplate
		fields = "__all__"

		widgets = {
			
			'project': TitleWidget,
		}


class QcAttributeTemplateForm(forms.ModelForm):

	class Meta:
		model = QcAttributeTemplate
		fields = "__all__"

		widgets = {
			'project': TitleWidget,
		}



class WorkitemNameWidget(ModelSelect2Widget):
	search_fields = [
		'workitem__file_name__icontains',
	]

class QcAttributeForm(forms.ModelForm):

	class Meta(object):
		model = QcAttribute
		fields = '__all__'
		widgets = {
			'dailytask': WorkitemNameWidget,
		}

	"""docstring for Meta"""
	def __init__(self, *arg, **kwargs):
		super(QcAttributeForm, self).__init__(*arg, **kwargs)
		try:
			get_qc_attribute = QcAttribute.objects.get(id=self.instance.pk)
			print "get_qc_attribute",get_qc_attribute

			get_dailytask = WorkItemAssignment.objects.get(qcattribute=get_qc_attribute)
			print "get_workitem", get_dailytask

			try:
				get_project_task = ProjectTask.objects.filter(workitem__file_name__exact=get_dailytask)
				print "project task", get_project_task
				project = Project.objects.filter(projecttask__in=get_project_task)
				print "printing project name", project
				qcattribute_template = QcAttributeTemplate.objects.get(project=project)
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

			except ProjectTask.DoesNotExist:
				pass
			except Project.DoesNotExist:
				pass
			except QcAttributeTemplate.DoesNotExist:
				pass

		except WorkItemAssignment.DoesNotExist:
			pass
		except QcAttribute.DoesNotExist:
			pass


	def get_field_mapping(self, field, mapping_field):

		if not mapping_field in (None, ''):
			self.fields[field].label = mapping_field
			self.fields[field].required = False 
		else:
			self.fields[field].widget = forms.HiddenInput()


# importing project tasks
class ImportProjectTaskForm(forms.Form):
	file = forms.FileField(label="Csv File")

	def __init__(self, *args, **kwargs):
		super(ImportProjectTaskForm, self).__init__(*args, **kwargs)
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

				if not "project" in headers:
					raise forms.ValidationError("Could not find a column labelled 'project' in that CSV file.")

				if not "title" in headers:
					raise forms.ValidationError("Could not find a column labelled 'title' in that CSV file.")

				if not "project-service" in headers:
					raise forms.ValidationError("Could not find a column labelled 'project-service' in that CSV file.")

				
				# Go through the rest of the CSV file.
				clean_rows = []
				invalid_rows = []
				invalid_cells = []
				"""
				for y_index, row in enumerate(reader, 2):
					row = [cell.decode("utf-8", "ignore").strip() for cell in row]
					try:
						row_data = dict(zip(headers, row))
					except IndexError:
						invalid_rows.append((y_index, row_data))

					# ignore blank rows
					if not ''.join(str(x) for x in row):
						continue

					for x_index, cell_value in enumerate(row):
						try:
							headers[x_index]
						except IndexError:
							continue

						if headers[x_index]:
							if not cell_value:
								invalid_rows.append((headers[x_index], y_index))  
								raise ValidationError(u'Missing required value %s for row %s' %
											(headers[x_index], y_index + 1))
				"""  
			except csv.Error:
				raise forms.ValidationError("Please upload a valid CSV file.")
			# Check that some rows were parsed.
		    
			if not clean_rows and invalid_rows:
				raise forms.ValidationError("No ProjectTasks could be imported, due to errors in that CSV file.")
			# Store the parsed data.
			self.cleaned_data["rows"] = clean_rows
			self.cleaned_data["invalid_rows"] = invalid_rows
		return file
	

#importing work items
class ImportWorkItemForm(forms.Form):
	
	file = forms.FileField(label='CSV File')

	class Meta:
		model = WorkItem
		fields = ('file',)

	def __init__(self, *args, **kwargs):
			super(ImportWorkItemForm, self).__init__(*args, **kwargs)
			self.max_upload_size = 1024*1024 #1 MB
			self.fileformat = None
			self.filename = None

	def clean_file(self):
		"""Parses the CSV file."""
		file = self.cleaned_data.get("file")

		if file._size > self.max_upload_size:
			raise forms.ValidationError(_(u"Uploaded file is too large ( > 1MB )"))

		if file:

			try:
				dialect = csv.Sniffer().sniff(file.read(1024))
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

				if not "project-task" in headers:
					raise forms.ValidationError("Could not find a column labelled 'project-task' in that CSV file.")

				if not "file-name" in headers:
					raise forms.ValidationError("Could not find a column labelled 'file-name' in that CSV file.")

				if not "folder-name" in headers:
					raise forms.ValidationError("Could not find a column labelled 'folder-name' in that CSV file.")

				# Go through the rest of the CSV file.
				clean_rows = []
				invalid_rows = []
				invalid_cells = []
				for y_index, row in enumerate(reader, 2):
					row = [cell.decode("utf-8", "ignore").strip() for cell in row]
					try:
						row_data = dict(zip(headers, row))
					except IndexError:
						invalid_rows.append((y_index, row_data))

					# ignore blank rows
					if not ''.join(str(x) for x in row):
						continue


					for x_index, cell_value in enumerate(row):
						try:
							headers[x_index]
						except IndexError:
							continue

						if headers[x_index]:
							if not cell_value:
								invalid_rows.append((headers[x_index], y_index))  
								raise ValidationError(u'Missing required value %s for row %s' %
											(headers[x_index], y_index + 1))
				  
			except csv.Error:
				raise forms.ValidationError("Please upload a valid CSV file.")
			# Check that some rows were parsed.
		   
			if not clean_rows and invalid_rows:
				raise forms.ValidationError(" Workitems could not be imported, due to errors in that CSV file.")
			# Store the parsed data.
			self.cleaned_data["rows"] = clean_rows
			self.cleaned_data["invalid_rows"] = invalid_rows
		return file
	

# importing workitemassignment or daily tasks 
class ImportDailyTasksForm(forms.Form):
	file = forms.FileField(label="CSV File")

	def __init__(self, *args, **kwargs):
		super(ImportDailyTasksForm, self).__init__(*args, **kwargs)
		self.max_upload_size = 1024*1024 #1 MB
		self.fileformat = None
		self.filename = None

	def clean_file(self):
		"""Parses the CSV file."""
		file = self.cleaned_data.get("file")
		if file:
			try:
				reader = csv.reader(file)
				# Parse the header row.
				try:
					header_row = reader.next()
				except StopIteration:
					raise forms.ValidationError("That CSV file is empty.")
				headers = [
					RE_WHITESPACE.sub("_", cell.decode("utf-8", "ignore").lower().strip())
					for cell in header_row
				]
				# Check the required fields.
				if len(headers) == 0:
					raise forms.ValidationError("That CSV file did not contain a valid header line.")

				if not "lead" in headers:
					raise forms.ValidationError("Could not find a column labelled 'lead' in that CSV file.")
				# Go through the rest of the CSV file.
				clean_rows = []
				invalid_rows = []
				for lineno, row in enumerate(reader, 2):
					row = [cell.decode("utf-8", "ignore").strip() for cell in row]
					try:
						row_data = dict(zip(headers, row))
					except IndexError:
						invalid_rows.append((lineno, row_data))

			except csv.Error:
				raise forms.ValidationError("Please upload a valid CSV file.")
			# Check that some rows were parsed.
		
			# Store the parsed data.
			self.cleaned_data["rows"] = clean_rows
			self.cleaned_data["invalid_rows"] = invalid_rows
		return file





























			

		  

