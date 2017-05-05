from __future__ import unicode_literals
import json
import xlwt
from django.db import transaction 
from django.core.urlresolvers import reverse
from django.shortcuts import render, get_object_or_404
from django.utils.translation import ugettext_lazy as _
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest
from django.contrib import messages
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required
from django.forms.models import formset_factory, modelform_factory, modelformset_factory
from employee import form1
from employee import models
from project.models import EmployeeAssignment
from django.db import transaction
import collections
from django.db import IntegrityError
# Create your views here.



@login_required
def employee_list(request):

	employees = None

	emp_dict = collections.OrderedDict()

	employees = models.Employee.objects.all()

	if employees:
		roles = models.EmployeeRole.objects.filter(employee__in = employees) 
		print "roles", roles
		emp_exp =  EmployeeAssignment.objects.filter(employee__in = employees)
		print "emp exp", emp_exp

		for employee in employees:
			emp_dict[employee.id] = (employee, [])

		for role in roles:
			if role.employee_id in emp_dict:
				emp_tuple = emp_dict[role.employee_id]
				emp_tuple[1].append(role)

		for exp in emp_exp:
			if exp.employee_id in emp_dict:
				emp_tuple = emp_dict[exp.employee_id]
				#exp_slab = models.ExperienceSlab.objects.filter(title=exp.experience_slab)
				emp_tuple[1].append(exp.experience_slab)
		print "emp_dict", emp_dict.items()


	#for emp in employee: 
	#	role= models.EmployeeRole.objects.filter(employee=emp)
	#	emp_exp = EmployeeAssignment.objects.filter(employee=emp)

	return render(request, 'employee/employee_list_partial.html', locals())



@login_required
def employee_add(request):
	success_dict={}
	
	if request.method == 'POST':
		form = form1.EmployeeForm(request.POST, None)

		user_form = form1.UserForm(request.POST, None)
		emp_assi_exp_form = form1.EmployeeAssignmentForm(request.POST, None)
		role_form=form1.EmployeeRoleForm(request.POST, None)
		
		if form.is_valid() and user_form.is_valid() and emp_assi_exp_form.is_valid() and role_form.is_valid():
			user = user_form.save(commit=False)
			first_name = user_form.cleaned_data.get('first_name')
			user_password = user_form.cleaned_data.get('password')
			#user.is_staff = True
			user.set_password(user_password)
			user.save()

			emp_role = role_form.cleaned_data.get('role')
			#print "role", emp_role
			if emp_role == 'sales_manager':
				user.groups.add(Group.objects.get(name="sales manager"))
			elif emp_role == 'sales_rep':
				user.groups.add(Group.objects.get(name="sales rep"))
			elif emp_role == 'management':
				user.groups.add(Group.objects.get(name="management"))
			elif emp_role == 'ops_manager':
				user.groups.add(Group.objects.get(name="operations manager"))
			elif emp_role == 'hr':
				user.groups.add(Group.objects.get(name="hr"))
			elif emp_role == 'itadmin':
				user.groups.add(Group.objects.get(name="itadmin"))
			elif emp_role == 'lead':
				user.groups.add(Group.objects.get(name="lead"))
			elif emp_role == 'staff':
				user.groups.add(Group.objects.get(name="agent"))
			elif emp_role == 'qc':
				user.groups.add(Group.objects.get(name="qc"))
			else:
				pass
			print "user.group",user.groups

			employee = form.save(commit=False)
			employee.name = first_name
			employee.user = user
			employee.save()

			if employee:
				emp_assi_exp_form_instance = emp_assi_exp_form.save(commit=False)
				emp_assi_exp_form_instance.employee = employee	
				emp_assi_exp_form_instance.save()

				role_form_instance = role_form.save(commit=False)			
				role_form_instance.employee = employee 	
				role_form_instance.save()
			success_dict['success_msg'] = "Successfully Created Employee"
			return HttpResponse(json.dumps(success_dict), content_type='application/json')	
		else:
			error_dict={}
			form_error_dict = {}
			user_form_error_dict = {}
			emp_exp_form_error_dict = {}
			emp_role_form_error_dict = {}

			for error in form.errors:
				e = form.errors[error]
				form_error_dict[error] = unicode(e)
			for error in user_form.errors:
				e = user_form.errors[error]
				user_form_error_dict[error] = unicode(e)
			for error in emp_assi_exp_form.errors:
				e = emp_assi_exp_form.errors[error]
				emp_exp_form_error_dict[error] = unicode(e)
			for error in role_form.errors:
				e = role_form.errors[error]
				emp_role_form_error_dict[error] = unicode(e)
			error_dict['form_error_dict'] = form_error_dict
			error_dict['user_form_error_dict'] = user_form_error_dict
			error_dict['emp_exp_form_error_dict'] = emp_exp_form_error_dict
			error_dict['emp_role_form_error_dict'] = emp_role_form_error_dict


			return HttpResponseBadRequest(json.dumps(error_dict))
			# messages.add_message(request, messages.ERROR, _('Please fix errors bellow.'))		

	else:
		form = form1.EmployeeForm()
		user_form = form1.UserForm()
		emp_assi_exp_form = form1.EmployeeAssignmentForm()
		role_form = form1.EmployeeRoleForm()
	return render(request, 'employee/employee_add_partial.html',locals())

@login_required
def employee_edit(request, id):
	success_dict={}
	employee = get_object_or_404(models.Employee, id=id)
	employee_assign = get_object_or_404(EmployeeAssignment, employee=employee)
	employee_role = get_object_or_404(models.EmployeeRole, employee=employee)

	get_user = get_object_or_404(User, username=employee.user)

	groups=Group.objects.all()

	group_dict = dict([ (grp.name, grp)  for  grp in groups])

	if request.method == "POST":
		form = form1.EmployeeForm(request.POST, instance=employee)

		user_form = form1.UserForm(request.POST, None, instance=get_user)
		emp_assi_exp_form = form1.EmployeeAssignmentForm(request.POST or None, instance=employee_assign)
		role_form = form1.EmployeeRoleForm(request.POST or None, instance=employee_role)
		
		if form.is_valid() and user_form.is_valid() and emp_assi_exp_form.is_valid() and role_form.is_valid():
			user = user_form.save(commit=False)
			first_name = user_form.cleaned_data.get('first_name')
			user_password = user_form.cleaned_data.get('password')

			#user.is_staff = True
			
			user.set_password(user_password)
			user.save()
			user.groups.clear()
			role_form_instance = role_form.save(commit=False)
			emp_role = role_form.cleaned_data.get('role')
			print "role", emp_role
			if emp_role == 'sales_manager':
				user.groups.add(Group.objects.get(name="sales manager"))
			elif emp_role == 'sales_rep':
				user.groups.add(Group.objects.get(name="sales rep"))
			elif emp_role == 'management':
				user.groups.add(Group.objects.get(name="management"))
			elif emp_role == 'ops_manager':
				user.groups.add(Group.objects.get(name="operations manager"))
			elif emp_role == 'hr':
				user.groups.add(Group.objects.get(name="hr"))
			elif emp_role == 'itadmin':
				user.groups.add(Group.objects.get(name="itadmin"))
			elif emp_role == 'lead':
				user.groups.add(Group.objects.get(name="lead"))
			elif emp_role == 'staff':
				user.groups.add(Group.objects.get(name="agent"))
			elif emp_role == 'qc':
				user.groups.add(Group.objects.get(name="qc"))
			else:
				pass

			employee = form.save(commit=False)
			employee.name = first_name
			employee.user = user
			employee.save()
			if employee:			
				emp_assi_exp_form_instance = emp_assi_exp_form.save(commit=False)
				emp_assi_exp_form_instance.employee = employee	
				emp_assi_exp_form_instance.save()

				role_form_instance = role_form.save(commit=False)			
				role_form_instance.employee = employee 
				emp_role = 	role_form.cleaned_data.get('role')
				role_form_instance.save()

			success_dict['success_msg'] = "Successfully Edit Employee"
			return HttpResponse(json.dumps(success_dict), content_type='application/json')
		
		else:
			error_dict={}

			form_error_dict = {}
			user_form_error_dict = {}
			emp_exp_form_error_dict = {}
			emp_role_form_error_dict = {}

			for error in form.errors:
				e = form.errors[error]
				form_error_dict[error] = unicode(e)
			for error in user_form.errors:
				e = user_form.errors[error]
				user_form_error_dict[error] = unicode(e)
			for error in emp_assi_exp_form.errors:
				e = emp_assi_exp_form.errors[error]
				emp_exp_form_error_dict[error] = unicode(e)
			for error in role_form.errors:
				e = role_form.errors[error]
				emp_role_form_error_dict[error] = unicode(e)
			error_dict['form_error_dict'] = form_error_dict
			error_dict['user_form_error_dict'] = user_form_error_dict
			error_dict['emp_exp_form_error_dict'] = emp_exp_form_error_dict
			error_dict['emp_role_form_error_dict'] = emp_role_form_error_dict


			return HttpResponseBadRequest(json.dumps(error_dict))

		
	else:
		form = form1.EmployeeForm(instance=employee)
		user_form = form1.UserForm(instance=get_user)
		emp_assi_exp_form = form1.EmployeeAssignmentForm(instance=employee_assign)
		role_form = form1.EmployeeRoleForm(instance=employee_role)
		
		return render(request, 'employee/employee_add_partial.html', {
										'user_form':user_form,
										'form': form ,
										'emp_assi_exp_form': emp_assi_exp_form ,
										'role_form':role_form,
										'is_edit_mode':True,
										'id':id
									}
								)



@login_required
def department_list(request):

	departments = models.Department.objects.all()
	return render(request, 'employee/departments_list_partial.html', 
					{'departments': departments}
				)



@login_required
def department_add(request):

	if request.method == 'POST':
		success_dict = {}
		form = form1.DepartmentForm(request.POST, None)

		if form.is_valid():
			department = form.save(commit=False)		      
			department.save()
	
			success_dict['success_msg'] = "Successfully Created Department"
			return HttpResponse(json.dumps(success_dict), content_type='application/json')
		else:
			error_dict = {}
			for error in form.errors:
				error_dict[error] = form.errors[ error]
			return HttpResponseBadRequest(json.dumps(error_dict))
			# messages.add_message(request, messages.ERROR, _('Please fix errors bellow.'))
	else:
		form = form1.DepartmentForm()

		return render(request, 'employee/department_add_partial.html', {'form':form})


@login_required
def department_edit(request, id):
	success_dict = {}
	department = get_object_or_404(models.Department, id=id)

	if request.method == "POST":
		form = form1.DepartmentForm(request.POST, instance=department)
		if form.is_valid():
			department = form.save(commit=False)
			department.save()
			
			success_dict['success_msg'] = "Successfully Edited Department"
			return HttpResponse(json.dumps(success_dict), content_type='application/json')
		else:
			error_dict={}
			for error in form.errors:
				error_dict[error] = form.errors[error]
				
			return HttpResponseBadRequest(json.dumps(error_dict))
	else:
		form = form1.DepartmentForm(instance=department)

	return render(request, 'employee/department_add_partial.html', {'form': form ,'is_edit_mode':True,'id':id})




@login_required
def experience_slab_list(request):

	experience_slabs = models.ExperienceSlab.objects.all()
	return render(request, 'employee/experience_slab_list_partial.html', 
					{'experience_slabs': experience_slabs}
				)


@login_required
def experience_slab_add(request):
	success_dict = {}
	if request.method == 'POST':
		form = form1.ExperienceSlabForm(request.POST, None)

		if form.is_valid():
			exp_slab = form.save(commit=False)
     
			exp_slab.save()
			
			success_dict['success_msg'] = "Successfully Created ExperienceSlab"
			return HttpResponse(json.dumps(success_dict), content_type='application/json')
		else:
			error_dict = {}
			for error in form.errors:
				error_dict[error] = form.errors[ error]
			return HttpResponseBadRequest(json.dumps(error_dict))
	else:
		form = form1.ExperienceSlabForm()

		return render(request, 'employee/experience_slab_add_partial.html', {'form':form})


@login_required
def experience_slab_edit(request, id):
	success_dict = {}
	exp_slab = get_object_or_404(models.ExperienceSlab, id=id)

	if request.method == "POST":
		form = form1.ExperienceSlabForm(request.POST, instance=exp_slab)
		if form.is_valid():
			exp_slab = form.save(commit=False)
			exp_slab.save()
			
			success_dict['success_msg'] = "Successfully Edited ExperienceSlab"
			return HttpResponse(json.dumps(success_dict), content_type='application/json')
		else:
			error_dict={}
			for error in form.errors:
				error_dict[error] = form.errors[error]
				
			return HttpResponseBadRequest(json.dumps(error_dict))
	else:
		form = form1.ExperienceSlabForm(instance=exp_slab)

	return render(request, 'employee/experience_slab_add_partial.html', {'form': form ,'is_edit_mode':True,'id':id})

def employee_exp_range_list(request, exp_slab_id):
	curr_empl = models.Employee.objects.get(user__username=request.user)
	if request.user.groups.filter(name='lead'):
		manager_employees = curr_empl.parent.get_descendants()
		employee_assignment = EmployeeAssignment.objects.filter(experience_slab_id=exp_slab_id, employee__in=manager_employees).select_related("employee")
	return render(request, 'employee/employee_experience_slab_partial_list.html',locals())



# def export_employee_details(request):
# 	if request.method=="POST":
# 		if request.POST.has_key("leads_start_date") and request.POST.has_key("leads_end_date"):
# 			start_date = request.POST.get('leads_start_date')
# 			end_date = request.POST.get('leads_end_date')

# 			response = HttpResponse(content_type='application/ms-excel')
# 			response['Content-Disposition'] = 'attachment; filename="Leads_from_%s_to_%s.xls"'%(start_date, end_date)

# 			wb = xlwt.Workbook(encoding='utf-8')
# 			ws = wb.add_sheet('Users')

# 			# Sheet header, first row
# 			row_num = 0

# 			font_style = xlwt.XFStyle()
# 			font_style.font.bold = True

# 			columns = ['Sl No','username', 'firstname', 'lastname', 'email', 'Manager', 'Department',
# 						'Role','Experianceslab'
# 					]

# 			for col_num in range(len(columns)):
# 				ws.write(row_num, col_num, columns[col_num], font_style)

# 			# Sheet body, remaining rows
# 			font_style = xlwt.XFStyle()
# 			rows = models.Employee.objects.filter('Employee_list').values_list('Sl No','username', 'firstname', 'lastname', 'email', 'Manager', 'Department',
# 						'Role','Experianceslab')
# 			for row in rows:
# 				row_num += 1
# 				for col_num in range(len(row)):
# 					ws.write(row_num, col_num, row[col_num], font_style)

# 			wb.save(response)
# 			return response

# def export_employee_form(request):
	
# 	return render(request,'employee/export_employee_csv.html', {})
	

@login_required
def employee_export(request):
	success_dict={}
	
	if request.method == 'POST':
		form = form1.EmployeeForm(request.POST, None)
	
		if form.is_valid():
			return HttpResponse(json.dumps(success_dict), content_type='application/json')	
		else:
			error_dict={}
			form_error_dict = {}

			for error in form.errors:
				e = form.errors[error]
				form_error_dict[error] = unicode(e)
		
			error_dict['form_error_dict'] = form_error_dict

			return HttpResponseBadRequest(json.dumps(error_dict))	
	else:
		form = form1.EmployeeForm()
	return render(request, 'employee/export_employee_csv.html',locals())	

