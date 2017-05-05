# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django import forms
from django.forms import TextInput, ModelForm, Textarea, Select
from django_select2.forms import ModelSelect2Widget
from django_select2.forms import ModelSelect2MultipleWidget
from .models import Department, Role, Employee, ExperienceSlab
from project.models import EmployeeAssignment


class TitleSelect2MultipleWidget(ModelSelect2MultipleWidget):
	search_fields = [
		'title__icontains',
	]

class TitleWidget(ModelSelect2Widget):
	search_fields = [
		'title__icontains',
		
	]


class UserNameWidget(ModelSelect2Widget):
	search_fields = ['username__icontains']



class EmployeeAssignmentInlineForm(forms.ModelForm):

	class Meta:
		model= EmployeeAssignment
		fields = '__all__'
		widgets = {
			'project':TitleWidget(attrs={'class': 'input-medium', 'style':'display:inline-grid;'}),
			'experience_slab': Select(attrs={'class': 'input-small'})

		}

	def __init__(self, *args, **kwargs):
		super(EmployeeAssignmentInlineForm, self).__init__(*args, **kwargs)
		self.fields['comments'].required = False

class EmployeeAdminForm(forms.ModelForm):
	class Meta:
		model=Employee
		fields = '__all__'
		widgets = {
			'user': UserNameWidget,
			'roles':TitleSelect2MultipleWidget,
			'project': Select(attrs={'class': 'input-medium'})

		}
