# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django import forms
import django.contrib.auth.models as auth_models
from django.contrib.auth.models import User, Group
from django.forms import TextInput, ModelForm, Textarea, Select

#from .models import Department, Role, Employee, ExperienceSlab,EmployeeRole
from project.models import EmployeeAssignment

from employee import models

class EmployeeForm(forms.ModelForm):
	
	class Meta:
		model = models.Employee
		fields = '__all__'

		exclude = ('name', 'user')
	
	def __init__(self, *args, **kwargs):
		super(EmployeeForm, self).__init__(*args, **kwargs)


class EmployeeAssignmentForm(forms.ModelForm):
	
	class Meta:
		model = EmployeeAssignment
		fields = ('experience_slab','comments')
		exclude=('employee', )

	def __init__(self, *args, **kwargs):

		super(EmployeeAssignmentForm, self).__init__(*args, **kwargs)
		#self.fields['experience_slab'].widget.attrs['class'] = 'datefield'

	
		self.fields['comments'].required = False
	
class EmployeeRoleForm(forms.ModelForm):
	
	class Meta:
		model = models.EmployeeRole
		fields = '__all__'
		exclude=('employee', )


		#self.fields['comments'].required=False
class UserForm(forms.ModelForm):
	#password = forms.CharField(widget=forms.PasswordInput(), required=False)
	groups = forms.ModelChoiceField(queryset=Group.objects.all(), required=False)
	first_name = forms.CharField(required=True)

	class Meta:
		model = auth_models.User
		fields = ['username', 'email', 'password', 'first_name', 'last_name', 'is_staff','groups']
	   # exclude = ('group',)

	def __init__(self, *args, **kwargs):
		super(UserForm, self).__init__(*args, **kwargs)
		self.fields['is_staff'].help_text = "Designates whether the user can log into this site"


class DepartmentForm(forms.ModelForm):

	class Meta:
		model = models.Department
		fields = '__all__'

class ExperienceSlabForm(forms.ModelForm):

	class Meta:
		model = models.ExperienceSlab
		fields = '__all__'

