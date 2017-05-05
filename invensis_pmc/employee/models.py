# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
from django_extensions.db.models import TitleDescriptionModel, \
	TitleSlugDescriptionModel, TimeStampedModel
from mptt.models import MPTTModel, TreeForeignKey
# from project.models import Project

# class Organization(TitleSlugDescriptionModel):
		

# 	class Meta:
# 	    verbose_name = "Organization"
# 	    verbose_name_plural = "Organizations"

# 	def __str__(self):
# 	    return self.title

class Department(TitleSlugDescriptionModel):
	
	# organization =  models.ForeignKey(Organization)
	class Meta:
	    verbose_name = "Department"
	    verbose_name_plural = "Departments"

	def __str__(self):
	    return self.title
	    	
# #shd this be an enum ?
# class EmployeeType(TitleDescriptionModel):

# 	class Meta:
# 	    verbose_name = "EmployeeType"
# 	    verbose_name_plural = "EmployeeTypes"

# 	def __str__(self):
# 	    return self.title


# enum?

# sales manager
# operations manager

class Role(TitleDescriptionModel):
    
	class Meta:
	    verbose_name = "Role"
	    verbose_name_plural = "Roles"

	def __str__(self):
	    return self.title
            
ROLES = (
		('staff','Agent / Artist'),
		('hr','HR'),
		('itadmin','IT Admin'),
		('lead','Lead'),
		('ops_manager','Operations Manager'),
		('qc','Quality Control'),
		('sales_manager','Sales Manager'),
		('sales_rep', 'Sales Representative'),
		('management','Management'),
		# ('customer',''),
	)


# #shd this be an enum
# #shd role desc be inline to empgrade model
# class EmployeeGrade(TitleDescriptionModel):
# 	role =  models.ForeignKey(RoleDescription)
# 	class Meta:
# 	    verbose_name = "EmployeeGrade"
# 	    verbose_name_plural = "EmployeeGrades"

# 	def __str__(self):
# 	    return self.title
    
# class Employee(models.Model):
class Employee(MPTTModel):
	# name = models.CharField(max_length=50, unique=True)
	parent = TreeForeignKey('self',verbose_name='Manager', null=True, blank=True, related_name='children', db_index=True)

	# organization =  models.ForeignKey(Organization)
	department =  models.ForeignKey(Department)
	name = models.CharField(max_length=255)
	# employee_type =  models.ForeignKey(EmployeeType)
	# employee_grade =  models.ForeignKey(EmployeeGrade)

	# role = models.ForeignKey(Role, blank=True, null=True)
	# 

	# roles = models.ManyToManyField(Role, related_name='+')


	user = models.ForeignKey(User, blank=True, null=True)
	# assignments =  models.ManyToManyField('project.Project', through='EmployeeAssignment', through_fields=('employee', 'project',))

	# assignments =  models.ManyToManyField('project.Project', through='EmployeeAssignment', through_fields=('employee', 'project',))

	class MPTTMeta:
	    order_insertion_by = ['name']

	def __str__(self):
		return self.name

	# def userrole(self):
	# 	return " / ".join([a.title for a in self.roles.all()])

class EmployeeRole(models.Model):
	employee = models.ForeignKey(Employee , related_name='+')
	role = models.CharField(choices=ROLES, max_length=20)
	class Meta:
	    verbose_name = "EmployeeRole"
	    verbose_name_plural = "EmployeeRoles"

	def __str__(self):
	    return self.role
    

class ExperienceSlab(TitleSlugDescriptionModel, TimeStampedModel):

	class Meta:
	    verbose_name = "ExperienceSlab"
	    verbose_name_plural = "ExperienceSlabs"

	def __str__(self):
	    return self.title







    