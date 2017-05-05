 # -*- coding: utf-8 -*-
from __future__ import unicode_literals
import json
import time, timeit
import uuid
import mimetypes
from inhouseapp import settings
from datetime import datetime, timedelta
from django.shortcuts import render
from django.db import IntegrityError
from django.db.models import Q
from django.forms.models import formset_factory, modelformset_factory
from django.contrib import messages
from django.core.urlresolvers import reverse
from wsgiref.util import FileWrapper
from django.utils.encoding import smart_str
from django.core.exceptions import ValidationError,MultipleObjectsReturned
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.shortcuts import render, get_object_or_404 
from django.utils.translation import ugettext_lazy as _
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest
from django.contrib import messages
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required
import encrypt_decrypt

from inhouseapp.utils.decorators import group_required
from employee.models import Employee, ExperienceSlab
from customer.models import Customer

from project import models
from project import form1,custom_filters 
from project import forms 
from django.db import transaction
import collections
try:
	from cStringIO import StringIO
except:
	from StringIO import StringIO
	

@login_required
@group_required('hr', login_url='/account/login/', raise_exception=True)
def hr_manager_dashboard(request):

	return render(request, 'hr_outline.html', 
					{}
				)



@login_required
@group_required('sales manager', login_url='/account/login/', raise_exception=True)
def sales_manager_dashboard(request):

	return render(request, 'project/crm_outline.html', 
					{}
				)


@login_required
@group_required('sales rep', login_url='/account/login/', raise_exception=True)
def sales_rep_dashboard(request):

	return render(request, 'sales_rep_outline.html', 
					{}
				)

@login_required
def masters_list_dashboard(request):

	return render(request, 'master_list_outline.html', 
					{}
				)
@login_required
def management_crm_dashboard(request):

	return render(request, 'management_outline.html', 
					{}
		)

@login_required
@group_required('operations manager', login_url='/account/login/', raise_exception=True)
def operation_manager_dashboard(request):

	return render(request, 'operation_manager_outline.html', 
					{}
				)

# @login_required
# @group_required('management', login_url='/account/login/', raise_exception=True)
# def management_dashboard(request):
# 	if request.method == "POST":
# 		form = forms.DashboardSetupForm(request.POST or None)
# 		if form.is_valid():
# 			stats_dates = form.save(commit=False)
# 			start_date = form.cleaned_data.get('start_date')
# 			print "start_date", start_date
# 			end_date = form.cleaned_data.get('end_date')
# 			print "end_date", end_date
# 			stats_dates.save()
# 		else:
# 			error_dict={}
# 			for error in form.errors:
# 				error_dict[error] = form.errors[error]	
# 			return HttpResponseBadRequest(json.dumps(error_dict))
# 	else:
# 		N = 90
# 		date_N_days_ago = datetime.datetime.now() - datetime.timedelta(days=N)
# 		data = {'start_date':date_N_days_ago, 'end_date':datetime.datetime.now().date()}
# 		form = forms.DashboardSetupForm(initial=data)
# 	return render(request, 'stats_dashboard/stats_dashboard_list_partial.html', locals())

@login_required
@group_required('lead', login_url='/account/login/', raise_exception=True)
def lead_dashboard(request):

	return render(request, 'lead_outline.html', 
					{}
				)

@login_required
@group_required('agent', login_url='/account/login/', raise_exception=True)
def agent_dashboard(request):

	return render(request, 'agent_outline.html', 
					{}
				)

@login_required
@group_required('qc', login_url='/account/login/', raise_exception=True)
def qc_dashboard(request):

	return render(request, 'project/qc_outline.html', 
					{}
				)



@login_required
def service_type_list(request):

	services = models.ServiceType.objects.all().order_by('id')
	return render(request, 'project/services_type_list_partial.html', 
					{'services': services}
				)

@login_required
def service_type_add(request):
	form = form1.ServiceTypeForm(request.POST)

	if request.method == 'POST':
		if form.is_valid():
			service = form.save(commit=False)
			service.title = form.cleaned_data['title']
			service.description = form.cleaned_data['description']
			service.save()

			return HttpResponse('ok ')
		else:
			error_dict={}
			for error in form.errors:
				error_dict[error] = form.errors[error]
				
			return HttpResponseBadRequest(json.dumps(error_dict))
	else:
		form = form1.ServiceTypeForm()

		return render(request, 'project/service_type_add_partial.html', {'form':form})


@login_required
def service_type_edit(request, slug):
	post = get_object_or_404(models.ServiceType, slug=slug)
	if request.method == "POST":
		form = form1.ServiceTypeForm(request.POST, instance=post)
		if form.is_valid():
			post = form.save(commit=False)
			post.save()

			return HttpResponse('ok ')
		else:
			error_dict={}
			for error in form.errors:
				error_dict[error] = form.errors[error]
				
			return HttpResponseBadRequest(json.dumps(error_dict))
	else:
		form = form1.ServiceTypeForm(instance=post)
	return render(request, 'project/service_type_add_partial.html', {'form': form, 'is_edit_mode' : True , 'slug' : slug,})

@login_required
def industry_list(request):

	industries = models.Industry.objects.all()
	return render(request, 'project/industry_list_partial.html', 
					{'industries': industries}
				)

@login_required
def industry_add(request):
	form = form1.IndustryForm(request.POST, None)
	if request.method == 'POST':
		if form.is_valid():
			indust = form.save(commit=False)
			indust.title = form.cleaned_data['title']
			print "indust.title", indust.title
			indust.description = form.cleaned_data['description']
			all_services = form.cleaned_data['services']
			print "my_services", all_services
			indust.save()
			for service in all_services:
				indust.services.add(service)
			#messages.add_message(request, messages.SUCCESS, _('Successfully Created Industry'))
			return HttpResponse('OK')
			#messages.add_message(request, messages.SUCCESS, _('Successfully Created Industry'))
			
		else:
			error_dict = {}
			for error in form.errors:
				error_dict[error] = form.errors[ error]
			return HttpResponseBadRequest(json.dumps(error_dict))
	else:
		form = form1.IndustryForm

		return render(request, 'project/industry_add_partial.html', {'form':form,
								'services':models.ServiceType.objects.all(),
							}
						)


@login_required
def industry_edit(request, slug):
	post = get_object_or_404(models.Industry, slug=slug)
	if request.method == "POST":
		form = form1.IndustryForm(request.POST, instance=post)
		if form.is_valid():
			industry = form.save(commit=False)
			all_services = form.cleaned_data['services']
			industry.save()

			for service in all_services:
				industry.services.add(service)

			return HttpResponse('ok ')
		else:
			error_dict={}
			for error in form.errors:
				error_dict[error] = form.errors[error]

			return HttpResponseBadRequest(json.dumps(error_dict))
	else:
		form = form1.IndustryForm(instance=post)
	return render(request, 'project/industry_add_partial.html', {'form': form, 'is_edit_mode':True, 'slug':slug})


@login_required
def project_type_list(request):

	project_types = models.ProjectType.objects.all()
	return render(request, 'project/project_types_list_partial.html', 
					{'project_types': project_types}
				)

@login_required
def project_type_add(request):
	form = form1.ProjectTypeForm(request.POST, None)

	if request.method == 'POST':
		if form.is_valid():
			pro_type = form.save(commit=False)
			pro_type.title = form.cleaned_data['title']
			pro_type.description = form.cleaned_data['description']
			pro_type.save()
			#messages.add_message(request, messages.SUCCESS, _('Successfully Created ProjectType'))
			return HttpResponse('OK')
		else:
			error_dict = {}
			for error in form.errors:
				error_dict[error] = form.errors[error]
				
			return HttpResponseBadRequest(json.dumps(error_dict))

			#messages.add_message(request, messages.ERROR, _('Please fix errors bellow.'))
	else:
		form = form1.ProjectTypeForm
		return render(request, 'project/project_type_add_partial.html', {'form':form})



@login_required
def project_type_edit(request, slug):
	post = get_object_or_404(models.ProjectType, slug=slug)
	if request.method == "POST":
		form = form1.ProjectTypeForm(request.POST, instance=post)
		if form.is_valid():
			post = form.save(commit=False)
			post.save()

			return HttpResponse('ok ')
		else:
			error_dict={}
			for error in form.errors:
				error_dict[error] = form.errors[error]

			return HttpResponseBadRequest(json.dumps(error_dict))
	else:
		form = form1.ProjectTypeForm(instance=post)
	return render(request, 'project/project_type_add_partial.html', {'form': form, 'is_edit_mode':True, 'slug':slug})


@login_required
def billing_type_list(request):

	billing_types = models.BillingType.objects.all()
	return render(request, 'project/billing_types_list_partial.html', 
					{'billing_types': billing_types}
				)

@login_required
def billing_type_add(request):

	if request.method == 'POST':
		form = form1.BillingTypeForm(request.POST, None)

		if form.is_valid():
			billing_type = form.save(commit=False)
			billing_type.title = form.cleaned_data['title']
			billing_type.description = form.cleaned_data['description']
			billing_type.save()
			# messages.add_message(request, messages.SUCCESS, _('Successfully Created BillingType'))
			# return HttpResponseRedirect(reverse('billing_types_list'))
			return HttpResponse('OK')
		else:
			error_dict = {}
			for error in form.errors:
				error_dict[error] = form.errors[ error]
			return HttpResponseBadRequest(json.dumps(error_dict))
			# messages.add_message(request, messages.ERROR, _('Please fix errors bellow.'))
	else:
		form = form1.BillingTypeForm()

	return render(request, 'project/billing_type_add_partial.html', {'form':form})



@login_required
def billing_type_edit(request, id):
	billing = get_object_or_404(models.BillingType, id=id)
	if request.method == "POST":
		form = form1.BillingTypeForm(request.POST, instance=billing)
		if form.is_valid():
			billing = form.save(commit=False)
			billing.save()

			return HttpResponse('ok ')
		else:
			error_dict={}
			for error in form.errors:
				error_dict[error] = form.errors[error]
				
			return HttpResponseBadRequest(json.dumps(error_dict))
	else:
		form = form1.BillingTypeForm(instance=billing)

	return render(request, 'project/billing_type_add_partial.html', {'form': form, 'is_edit_mode':True, 'id':id})

@login_required
def service_view(request,id):
	
	service = get_object_or_404(models.Service,id=id)
	sla = models.ServiceSla.objects.filter(service=service)
	documents = models.ServiceDocument.objects.filter(service=service)
	resource=models.ServiceResourcePlan.objects.filter(service=service)

	print"sla",sla
	print"documents",documents
	print "resource",resource
	# sla = get_object_or_404(models.ServiceSla,service=service)
	# documents = get_object_or_404(models.ServiceDocument,service=service)
	# resource = get_object_or_404(models.ServiceResourcePlan,service=service)
	
	return render(request, 'project/service_view_partial.html',locals()

						)

@login_required
def service_list(request):

	services = None
	service_list =[]
	svc_dict = collections.OrderedDict()
	service_document_dict = {}

	if request.user.groups.filter(name='sales manager').exists():
		services = models.Service.objects.filter(created_by=request.user).order_by('created')

		if services:
			service_document_types = models.ServiceDocument.objects.filter(service__in=services)

			for service in services:
				svc_dict[service.id] = (service, [])

			for document_type in service_document_types:
				if document_type.service_id in svc_dict:
					svc_tuple = svc_dict[document_type.service_id]

					if document_type == "other":
						svc_tuple[1].append(document_type.other_document_type)
					else:
						svc_tuple[1].append(document_type)

			print svc_dict.items()
		return render(request, 'project/service_list_partial.html',locals())

	elif request.user.groups.filter(name='operations manager').exists():
		# emp_usr = Employee.objects.get(user =request.user)
		services = models.Service.objects.filter(operations_manager__user=request.user).order_by('created')

	elif request.user.groups.filter(name='lead').exists():
		#emp_usr = Employee.objects.get(user__username =request.user)
		service_ids=models.AssignServiceLead.objects.filter(lead__user = request.user).values_list('service_id', flat=False)
		services = models.Service.objects.filter(id__in = service_ids).order_by('created')

	if services:
		# service_ids = [s.id for s in services]
		tasks = models.Task.objects.filter(service__in = services, status__in=['new', 'pending','qc','rejected'])      

		service_document_types = models.ServiceDocument.objects.filter(service__in=services)

		for service in services:
			svc_dict[service.id] = (service, [])

		for task in tasks:
			if task.service_id in svc_dict:
				svc_tuple = svc_dict[task.service_id]
				svc_tuple[1].append(task)

		print svc_dict.items()

	return render(request, 'project/service_list_partial.html',locals())

@login_required
def sales_billings(request):
	sales_billing_list = []
	sales_billing_dict = {}

	if request.method == "POST" and request.is_ajax():
		
		number_of_resources = request.POST.get('number_of_resources')
		pricing = request.POST.get('amount_per_billing_type')
		no_of_man_hours_per_month = request.POST.get('no_of_man_hours_per_month')

		customer_name = request.POST.get('customer')
		conversion_rate = request.POST.get('conversion_rate')
		customer_curency_dict = {}
			
		if request.POST.has_key('customer'):
			try:
				customer = Customer.objects.get(id=customer_name)
				customer_currency_type = customer.currency
				customer_curency_dict[customer_currency_type] = customer_currency_type
			except ValueError:
				pass
			sales_billing_dict['customer_curency'] = customer_currency_type
			
			return HttpResponse(json.dumps(sales_billing_dict), content_type='application/json')
		if request.POST.has_key('workweek_start') and request.POST.get('workweek_end'):
			
			workweek_start = request.POST.get('workweek_start')
			workweek_end = request.POST.get('workweek_end')
			work_week_list = ['monday','tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
			# validating input
			if not workweek_start in work_week_list:
				raise "invalid day of the week -%s" % workweek_start
			if not workweek_end in work_week_list:
				raise "invalid day of the week -%s" % workweek_end

			# ***********
			counter = 0
			if workweek_start == workweek_end:
				counter = 1

			else:
				counter_started = False
				counter_ended =False
				for index,day_of_week in enumerate(work_week_list):
					print day_of_week
					if day_of_week == workweek_start :
						counter_started=True
						counter += 1
					elif counter_started and day_of_week == workweek_end :
						counter_ended = True
						counter += 1
						break
					elif counter_started:
						counter += 1

				if counter_started and counter_ended == False:                  
					for index,day_of_week in enumerate(work_week_list):
						if counter_started and day_of_week == workweek_end :
							counter_ended = True
							counter += 1
							break
						elif counter_started:
							counter += 1
			operational_days = counter  
			sales_billing_dict['operations_days'] = counter
			
			return HttpResponse(json.dumps(sales_billing_dict), content_type='application/json')


		if request.POST.has_key('workhours_start') and request.POST.has_key('workhours_end'):
			workhour_start = request.POST.get('workhours_start')
			workhour_end   = request.POST.get('workhours_end')
			s_h, s_m = [int(i) for i in workhour_start.split(':')]
			start_time = 60 * s_h +  s_m
			e_h, e_m = [int(i) for i in workhour_end.split(':')]
			end_time = 60 * e_h +  e_m
			if start_time <= end_time:
				operational_hours = float((end_time - start_time))/60
			else:
				end_time = end_time + 24 * 60
				operational_hours = float((end_time - start_time))/60
	
			sales_billing_dict['operational_hours'] = str(operational_hours)
			sales_billing_list.append(sales_billing_dict)

			return HttpResponse(json.dumps(sales_billing_dict), content_type='application/json')


		if request.POST.has_key('billing_type'):
			billing_type = request.POST.get('billing_type')
			if billing_type == "per_fte":
				projected_prj_value_per_month = int(number_of_resources) * float(pricing) 
				projected_prj_value_per_annum = projected_prj_value_per_month * 12
				fte_cost_per_month = pricing

				sales_billing_dict['projected_prj_value_per_month'] = projected_prj_value_per_month
				sales_billing_dict['projected_prj_value_per_annum'] = projected_prj_value_per_annum
				sales_billing_dict['fte_cost_per_month'] = fte_cost_per_month

			elif billing_type == "per_hour":
				
				projected_prj_value_per_month = int(no_of_man_hours_per_month) * float(pricing) 
				projected_prj_value_per_annum = projected_prj_value_per_month * 12
				fte_cost_per_month = float(projected_prj_value_per_month)
				sales_billing_dict['projected_prj_value_per_month'] = projected_prj_value_per_month
				sales_billing_dict['projected_prj_value_per_annum'] = projected_prj_value_per_annum
				sales_billing_dict['fte_cost_per_month'] = fte_cost_per_month

			elif billing_type == "per_tx" and request.POST.has_key('tx_volume_duration_type'):

				tx_volume_duration_type = request.POST.get('tx_volume_duration_type')
				operational_days  = request.POST.get('operations_days')
				if tx_volume_duration_type == 'per_day' and request.POST.has_key('projected_tx_volume_per_day'):                    
					projected_tx_volume_per_day = request.POST.get('projected_tx_volume_per_day')
					projected_prj_value_per_month = int(projected_tx_volume_per_day) * int(pricing) * int(operational_days) * 4
					projected_prj_value_per_annum = projected_prj_value_per_month * 12

					fte_cost_per_month = float(projected_prj_value_per_month)
					projected_tx_volume_per_week  = int(projected_tx_volume_per_day) * int(operational_days)
					projected_tx_volume_per_month  = projected_tx_volume_per_week * 4
					
					sales_billing_dict['projected_tx_volume_per_week']  = projected_tx_volume_per_week
					sales_billing_dict['projected_tx_volume_per_month'] = projected_tx_volume_per_month

					sales_billing_dict['projected_prj_value_per_month'] = projected_prj_value_per_month
					sales_billing_dict['projected_prj_value_per_annum'] = projected_prj_value_per_annum
					sales_billing_dict['fte_cost_per_month'] = fte_cost_per_month

				elif tx_volume_duration_type == 'per_week' and request.POST.has_key('projected_tx_volume_per_week'):
					projected_tx_volume_per_week = request.POST.get('projected_tx_volume_per_week')
					projected_tx_volume_per_day =  int(projected_tx_volume_per_week) / int(operational_days)
					
					projected_prj_value_per_month = projected_tx_volume_per_day * int(pricing) * int(operational_days) * 4
					projected_prj_value_per_annum = projected_prj_value_per_month * 12 
					fte_cost_per_month = float(projected_prj_value_per_month)

					sales_billing_dict['projected_tx_volume_per_day']  = projected_tx_volume_per_day
					sales_billing_dict['projected_tx_volume_per_month'] = projected_tx_volume_per_day * int(operational_days) * 4 

					sales_billing_dict['projected_prj_value_per_month'] = projected_prj_value_per_month
					sales_billing_dict['projected_prj_value_per_annum'] = projected_prj_value_per_annum
					sales_billing_dict['fte_cost_per_month'] = fte_cost_per_month

				elif tx_volume_duration_type == 'per_month' and request.POST.has_key('projected_tx_volume_per_month'):
					projected_tx_volume_per_month = request.POST.get('projected_tx_volume_per_month')	
					projected_tx_volume_per_day = int(projected_tx_volume_per_month) / ( int(operational_days) * 4)

					projected_prj_value_per_month = projected_tx_volume_per_day *  int(pricing) * int(operational_days) * 4
					projected_prj_value_per_annum = projected_prj_value_per_month * 12
					fte_cost_per_month = float(projected_prj_value_per_month)

					sales_billing_dict['projected_tx_volume_per_day']  = projected_tx_volume_per_day
					sales_billing_dict['projected_tx_volume_per_week'] = projected_tx_volume_per_day * int(operational_days)

					sales_billing_dict['projected_prj_value_per_month'] = projected_prj_value_per_month
					sales_billing_dict['projected_prj_value_per_annum'] = projected_prj_value_per_annum
					sales_billing_dict['fte_cost_per_month'] = fte_cost_per_month

				else:
					pass
			else:
				pass

			customer_currency_type = request.POST.get('customer_currency_type')
			if not customer_currency_type == 'USD' and request.POST.has_key('conversion_rate'):
				conversion_rate = request.POST.get('conversion_rate')
				sales_billing_dict['projected_prj_value_per_month'] = format(float(projected_prj_value_per_month)/float(conversion_rate), '.2f')
				sales_billing_dict['projected_prj_value_per_annum'] = format(float(projected_prj_value_per_annum)/float(conversion_rate), '.2f')
				sales_billing_dict['fte_cost_per_month'] = format(float(fte_cost_per_month)/float(conversion_rate), '.2f')
			else:
				sales_billing_dict['projected_prj_value_per_month'] = projected_prj_value_per_month
				sales_billing_dict['projected_prj_value_per_annum'] = projected_prj_value_per_annum
				sales_billing_dict['fte_cost_per_month'] = fte_cost_per_month

			return HttpResponse(json.dumps(sales_billing_dict), content_type='application/json')


def service_document_download(request, path, document_root):
	tmp_guid = uuid.uuid1()
	tmp_file_path ="temp/new_decryption.txt"

	if path.endswith('.enc'):
		file_path = settings.MEDIA_ROOT + path
		file_name = path.split('/')[-1]
		out_filename = os.path.splitext(file_name)[0]
		out_file_path = settings.MEDIA_ROOT + "temp_decrypt/"+ out_filename
		key_pass = "0123456789asdfgh"
		aescipher = encrypt_decrypt.AESCipher(key_pass)
		decrypt_service_doc = aescipher.decrypt_file(file_path, out_file_path)
		output_file = decrypt_service_doc.split('/')[-1]
		file_wrapper = FileWrapper(file(out_file_path,'rb'))
		file_mimetype = mimetypes.guess_type(out_file_path)
		response = HttpResponse(file_wrapper, content_type=file_mimetype )
		response['X-Sendfile'] = output_file
		response['Content-Length'] = os.stat(out_file_path).st_size
		response['Content-Disposition'] = 'attachment; filename=%s' % smart_str(output_file) 
		if os.path.exists(out_file_path):
			try:
				os.remove(out_file_path)
			except OSError, e:
				print "Error: %s - %s"%(e.filename, e.strerror)
		else:
			print "Sorry, %s not found", out_file_path
		return response	
	else:
		file_path = settings.MEDIA_ROOT + path
		file_mimetype = mimetypes.guess_type(file_path)
		file_wrapper = FileWrapper(file(file_path,'rb'))
 		response = HttpResponse(file_wrapper, content_type=file_mimetype )
		response['X-Sendfile'] = path
		response['Content-Length'] = os.stat(file_path).st_size
		response['Content-Disposition'] = 'attachment; filename=%s' % smart_str(path) 
		return response	

@login_required
def service_add(request):
	success_dict={}
	errors_dict = {}
	ServiceSlaFormset = formset_factory(form1.ServiceSlaInlineForm, extra=1,)
	ServiceDocumentFormset  = formset_factory(form1.ServiceDocumentInlineForm, extra=1,)
	ServiceResourcePlanFormset   = formset_factory(form1.ServiceResourcePlanInlineForm, extra=1,)

	if request.method == 'POST':
		form = form1.ServiceForm(request.POST or None)
		servicesla_formset = ServiceSlaFormset(request.POST or None, prefix='servicesla')
		service_document_formset = ServiceDocumentFormset(request.POST, request.FILES, prefix='servicedoc')
		service_resource_formset = ServiceResourcePlanFormset(request.POST or None,  prefix='resource_plan')


		if form.is_valid() and servicesla_formset.is_valid() and service_resource_formset.is_valid() and  service_document_formset.is_valid():
			#with transaction.atomic():
			service = form.save(commit=False)
			service.created_by = request.user
			pricing = form.cleaned_data.get('amount_per_billing_type')
			projected_prj_value_per_month = form.cleaned_data.get('projected_prj_value_per_month')
			projected_prj_value_per_annum = form.cleaned_data.get('projected_prj_value_per_annum')
			fte_cost_per_month = form.cleaned_data.get('fte_cost_per_month')

			key_pass = "invensis"
			aescipher = encrypt_decrypt.AESCipher(key_pass)

			encrypt_pricing = aescipher.encrypt(str(pricing))
			encrypt_projected_prj_value_per_month = aescipher.encrypt(str(projected_prj_value_per_month))
			encrypt_projected_prj_value_per_annum = aescipher.encrypt(str(projected_prj_value_per_annum))
			encrypt_fte_cost_per_month = aescipher.encrypt(str(fte_cost_per_month))

			service.encrypt_pricing  = encrypt_pricing
			service.encrypt_projected_prj_value_per_month = encrypt_projected_prj_value_per_month
			service.encrypt_projected_prj_value_per_annum = encrypt_projected_prj_value_per_annum
			service.encrypt_fte_cost_per_month = encrypt_fte_cost_per_month
			
			service.amount_per_billing_type = 0
			service.projected_prj_value_per_month = 0
			service.projected_prj_value_per_annum = 0
			service.fte_cost_per_month = 0


			service.save()

			try:

				for service_sla_form in servicesla_formset:
					service_sla_formInstance = service_sla_form.save(commit=False)
					service_sla_formInstance.service = service
					service_sla_formInstance.save()

				for service_resource_form in service_resource_formset:
					service_resource_formInstance = service_resource_form.save(commit=False)
					service_resource_formInstance.service = service
					service_resource_formInstance.save()

			except IntegrityError:
				pass
			for service_document_form in service_document_formset:
				if service_document_form not in [deleted_form for deleted_form in service_document_formset.deleted_forms]:

					service_document_formInstance = service_document_form.save(commit=False)
					service_document_formInstance.service = service

					service_document_type = service_document_form.cleaned_data.get('document_type')
					is_share_with_others = service_document_form.cleaned_data.get('share_with_others')
					service_doc_data = service_document_form.cleaned_data.get('document')

					#print "service_doc_data", service_doc_data.readlines()
					otherdocument = request.POST.get('otherdocument')
					if service_document_type in ['nda', 'sla', 'agreement'] and service_doc_data not in ['', None]:
						if not service_doc_data.name.endswith('.enc'):
							#print service_doc_data.readlines()
							tmp_guid = uuid.uuid1()
							tmp_file_path ="temp/test_encryption_%s.txt" % tmp_guid
							path = default_storage.save(tmp_file_path, ContentFile(service_doc_data.read()))
							service_doc_nam = service_doc_data.name.split('.')
							tmp_encrypted_file_path = "service_documents/%s.%s" % (service_doc_nam[0],service_doc_nam[1]) 
							media_path = os.path.join(settings.MEDIA_ROOT, tmp_encrypted_file_path)
						
							if default_storage.exists(path):
								file_path = os.path.join(settings.MEDIA_ROOT,path)								
								key_pass = "0123456789asdfgh"
								aescipher = encrypt_decrypt.AESCipher(key_pass)
								encrypt_service_doc = aescipher.encrypt_file(file_path, media_path)
								if encrypt_service_doc:
									encrypted_path = encrypt_service_doc.split('/')
									encrypt_file_path = '/'.join((encrypted_path[-2], encrypted_path[-1]))
									service_document_formInstance.document = encrypt_file_path
								default_storage.delete(path)
						service_document_formInstance.other_document_type = otherdocument
						service_document_formInstance.save()
			success_dict['success_msg'] = "Successfully Created Project"
			return HttpResponse(json.dumps(success_dict), content_type='application/json')
		else:

			if request.is_ajax():
				errors_dict = {}
				service_form_error_dict = {}
				service_sla_formset_error_dict = {}
				service_resource_formset_error_dict = {}
				service_document_formset_error_dict = {}
			
				for error in form.errors:
					e = form.errors[error]
					service_form_error_dict[error] = unicode(e)
				try:
					for f1 in servicesla_formset:
						if f1.errors:
							for error in f1.errors:
								e = f1.errors[error]
								service_sla_formset_error_dict[error] = unicode(e)

					for f1 in service_resource_formset:
						if f1.errors:
							for error in f1.errors:
								e = f1.errors[error]
								service_resource_formset_error_dict[error] = unicode(e)

					for f1 in service_document_formset:
						if f1.errors:
							for error in f1.errors:
								e = f1.errors[error]
								service_document_formset_error_dict[error] = unicode(e)

				except ValidationError:
					pass
				errors_dict['form_errors'] = service_form_error_dict
				errors_dict['sla_formset_errors'] = service_sla_formset_error_dict
				errors_dict['resource_formset_errors'] = service_resource_formset_error_dict
				errors_dict['document_formset_errors'] = service_document_formset_error_dict

				return HttpResponseBadRequest(json.dumps(errors_dict))
	else:
		form = form1.ServiceForm()
		servicesla_formset = ServiceSlaFormset(prefix='servicesla')
		service_document_formset  = ServiceDocumentFormset(prefix='servicedoc')
		service_resource_formset  = ServiceResourcePlanFormset(prefix='resource_plan')
		return render(request, 'project/service_add_partial.html', locals())

import os
@login_required
def service_edit_ORING(request, id):
	success_dict={}
	errors_dict = {}
	#success_dict = {}
	service = get_object_or_404(models.Service, id=id)

	#if request.user.groups.filter(name= 'sales manager').exists:
	try:
		key_pass = "invensis"
		aescipher = encrypt_decrypt.AESCipher(key_pass)

		amount_per_billing_type = aescipher.decrypt(service.encrypt_pricing)
		projected_prj_value_per_month = aescipher.decrypt(service.encrypt_projected_prj_value_per_month)
		projected_prj_value_per_annum = aescipher.decrypt(service.encrypt_projected_prj_value_per_annum)
		fte_cost_per_month = aescipher.decrypt(service.encrypt_fte_cost_per_month)

		service.amount_per_billing_type = float(amount_per_billing_type)
		service.projected_prj_value_per_month = float(projected_prj_value_per_month)
		service.projected_prj_value_per_annum = float(projected_prj_value_per_annum)
		service.fte_cost_per_month = float(fte_cost_per_month)

		service.save()
	except UnicodeDecodeError:
		pass

	except ValueError:
		pass


	AssignServiceLeadFormset = modelformset_factory(models.AssignServiceLead,form1.AssignServiceLeadForm, extra=1,exclude=('service',), can_delete=True)
	ServiceSlaFormset = modelformset_factory(models.ServiceSla, form1.ServiceSlaForm, extra=1, exclude=('service',), can_delete=True)
	ServiceDocumentFormset  = modelformset_factory(models.ServiceDocument, form1.ServiceDocumentForm, extra=1, exclude=('service',), can_delete=True )
	ServiceResourcePlanFormset   = modelformset_factory(models.ServiceResourcePlan, form1.ServiceResourcePlanInlineForm, extra=1, exclude=('service',), can_delete=True)



	assign_service_lead_formset = AssignServiceLeadFormset(queryset=models.AssignServiceLead.objects.filter(service=service), prefix='assign_service_lead') 
	servicesla_formset = ServiceSlaFormset(queryset=models.ServiceSla.objects.filter(service=service), prefix='servicesla')
	service_document_formset = ServiceDocumentFormset(queryset=models.ServiceDocument.objects.filter(service=service), prefix='servicedoc')
	service_resource_formset = ServiceResourcePlanFormset(queryset=models.ServiceResourcePlan.objects.filter(service=service), prefix='resource_plan')

	if request.method == "POST":
		if request.user.groups.filter(name="sales manager"):
			form = form1.ServiceForm(request.POST, instance=service)

			if service:
				servicesla_formset = ServiceSlaFormset(request.POST or None,  queryset=models.ServiceSla.objects.filter(service=service), prefix='servicesla')
				service_document_formset = ServiceDocumentFormset(request.POST or None, request.FILES, queryset=models.ServiceDocument.objects.filter(service=service), prefix='servicedoc')
				service_resource_formset = ServiceResourcePlanFormset(request.POST or None, queryset=models.ServiceResourcePlan.objects.filter(service=service), prefix='resource_plan')
				#assign_service_lead_formset = AssignServiceLeadFormset(request.POST or None, queryset=models.AssignServiceLead.objects.filter(service=service), prefix='assign_service_lead')	
			else:
				servicesla_formset = ServiceSlaFormset(request.POST or None,  queryset=models.ServiceSla.objects.none(), prefix='servicesla')
				service_document_formset = ServiceDocumentFormset(request.POST or None, request.FILES, queryset=models.ServiceDocument.objects.none(), prefix='servicedoc')
				service_resource_formset = ServiceResourcePlanFormset(request.POST or None, queryset=models.ServiceResourcePlan.objects.none(), prefix='resource_plan')
				#assign_service_lead_formset = AssignServiceLeadFormset(request.POST or None, queryset=models.AssignServiceLead.objects.none(), prefix='assign_service_lead')	


			for service_sla_form in servicesla_formset.deleted_forms:
				service_sla_form_instance = service_sla_form.instance
				if service_sla_form_instance.pk:
					service_sla_form_instance.delete()
			
			if request.user.groups.filter(name='sales manager').exists():
				for service_document_form in service_document_formset.deleted_forms:
					service_document_form_instance = service_document_form.instance
					if service_document_form_instance.pk:
						service_document_form_instance.delete()

			for service_resource_form in service_resource_formset.deleted_forms:
				service_resource_form_instance = service_resource_form.instance
				if service_resource_form_instance.pk:
					service_resource_form_instance.delete()


			if form.is_valid() and servicesla_formset.is_valid() and service_resource_formset.is_valid():

				service_instance = form.save(commit=False)
				service_instance.fte_cost_per_month = service.fte_cost_per_month
				service_instance.billing_interval_in_days = service.billing_interval_in_days

				service_instance.save()
				try:
					for service_sla_form in servicesla_formset:
						service_sla_formInstance = service_sla_form.save(commit=False)
						service_sla_formInstance.service = service_instance
						service_sla_formInstance.save()

					for service_resource_form in service_resource_formset:
						service_resource_formInstance = service_resource_form.save(commit=False)
						service_resource_formInstance.service = service_instance
						service_resource_formInstance.save()
				except IntegrityError:
					pass
				

				
				if request.user.groups.filter(name='sales manager').exists:

					if service_document_formset.is_valid():
						print "-===="
						for service_document_form in service_document_formset:
							#if service_document_form not in [deleted_form for deleted_form in service_document_formset.deleted_forms]:

							service_document_formInstance = service_document_form.save(commit=False)
							service_document_formInstance.service = service_instance
							service_document_type = service_document_form.cleaned_data.get('document_type')
							is_share_with_others = service_document_form.cleaned_data.get('share_with_others')
							service_doc_data = service_document_form.cleaned_data.get('document')
							#service_doc_data = request.FILES.get('document')
							print "service_doc_data", service_doc_data
							otherdocument = request.POST.get('otherdocument')
							print "otherdocument", otherdocument

							if service_document_type in ['nda', 'sla', 'agreement'] and service_doc_data not in ['', None]:
								if not service_doc_data.name.endswith('.enc'):
									#print service_doc_data.readlines()
									tmp_guid = uuid.uuid1()
									tmp_file_path ="temp/test_encryption_%s.txt" % tmp_guid
									print "service_doc_data before", service_doc_data.name
									path = default_storage.save(tmp_file_path, ContentFile(service_doc_data.read()))
									print "path", path

									#if service_doc_data.name.startswith('service_documents'):
									#	service_doc_data.name = service_doc_data.name.split('/')[-1]
									#	print "service_doc_data.name.split('/')", service_doc_data.name
									#	print "service_doc_data on split", type(service_doc_data)
									#else:
									#	service_doc_data = service_doc_data

									#print "service_doc_data after", service_doc_data.name

									#print "default_storage.exists(path)",default_storage.exists(path)
									#print "service_doc_data on split", service_doc_data.name.split('/')
									service_doc_nam = service_doc_data.name.split('.')
									print "service_doc_nam", service_doc_nam
									tmp_encrypted_file_path = "service_documents/%s.%s" % (service_doc_nam[0],service_doc_nam[1]) 
									media_path = os.path.join(settings.MEDIA_ROOT, tmp_encrypted_file_path)
									#media_path = "assets/media/" + tmp_encrypted_file_path 
									
									if default_storage.exists(path):
										#with default_storage.open(path, 'rb') as in_file, open(media_path, 'wb') as out_file:
											#encrypt_service_doc = encrypt_decrypt.encrypt_file(in_file, out_file, str('invensis'))
											#print "encrypt_service_doc", encrypt_service_doc
										file_path = os.path.join(settings.MEDIA_ROOT,path)
										print "file_path", file_path
										
										key_pass = "0123456789asdfgh"
										aescipher = encrypt_decrypt.AESCipher(key_pass)
										encrypt_service_doc = aescipher.encrypt_file(file_path, media_path)
										print "encrypt_service_doc", encrypt_service_doc

										if encrypt_service_doc:
											encrypted_path = encrypt_service_doc.split('/')
											encrypt_file_path = '/'.join((encrypted_path[-2], encrypted_path[-1]))
											service_document_formInstance.document = encrypt_file_path

										default_storage.delete(path)

								service_document_formInstance.other_document_type = otherdocument
								service_document_formInstance.save()


								#with open(path, 'r') as in_file:
								#	key_pass = "invensis"
								#	aescipher = encrypt_decrypt.AESCipher(key_pass)

								#	filesize = os.path.getsize(in_file)
								#	print "filesize", filesize
								#	encrypt_service_doc = aescipher.encrypt_file(in_file)
								#	print "encrypt_service_doc again", encrypt_service_doc
								service_document_formInstance.save()
						else:
							service_document_formset_error_dict = {}
							for f1 in service_document_formset:
								if f1.errors:
									for error in f1.errors:
										e = f1.errors[error]
										service_document_formset_error_dict[error] = unicode(e)
							errors_dict['document_formset_errors'] = service_document_formset_error_dict
				

				success_dict['success_msg'] = "Successfully Edited Project Details"
				return HttpResponse(json.dumps(success_dict), content_type='application/json')
			else:

				if request.is_ajax():
					errors_dict = {}
					service_form_error_dict = {}
					service_sla_formset_error_dict = {}
					service_resource_formset_error_dict = {}
				
					for error in form.errors:
						e = form.errors[error]
						service_form_error_dict[error] = unicode(e)
					try:
						for f1 in servicesla_formset:
							if f1.errors:
								for error in f1.errors:
									e = f1.errors[error]
									service_sla_formset_error_dict[error] = unicode(e)

						for f1 in service_resource_formset:
							if f1.errors:
								for error in f1.errors:
									e = f1.errors[error]
									service_resource_formset_error_dict[error] = unicode(e)


					except ValidationError:
						pass
					errors_dict['form_errors'] = service_form_error_dict
					print "service form errors", service_form_error_dict
					errors_dict['sla_formset_errors'] = service_sla_formset_error_dict
					errors_dict['resource_formset_errors'] = service_resource_formset_error_dict
		
					return HttpResponseBadRequest(json.dumps(errors_dict))
		
		if request.user.groups.filter(name__in=['operations manager', 'lead']).exists():
			assign_service_lead_formset = AssignServiceLeadFormset(request.POST or None, queryset=models.AssignServiceLead.objects.filter(service=service), prefix='assign_service_lead')	

			for assign_service_lead_form in assign_service_lead_formset.deleted_forms:
				assign_service_lead_form_instance = assign_service_lead_form.instance
				if assign_service_lead_form_instance.pk:
					assign_service_lead_form_instance.delete()

			if assign_service_lead_formset.is_valid():

				for assign_service_lead_form in assign_service_lead_formset:
					if assign_service_lead_form not in [deleted_form for deleted_form in assign_service_lead_formset.deleted_forms]:
						assign_service_lead_form_instance = assign_service_lead_form.save(commit=False)
						assign_service_lead_form_instance.service = service
						lead = assign_service_lead_form.cleaned_data.get('lead')

						if lead not in ['', None]:
							assign_service_lead_form_instance.save()
				
				success_dict['success_msg'] = "Successfully assigned project to lead"
				return HttpResponse(json.dumps(success_dict), content_type='application/json')

			else:
				assign_service_lead_form_error_dict = {}
				for f1 in assign_service_lead_formset:
					if f1.errors:
						for error in f1.errors:
							e = f1.errors[error]
							assign_service_lead_form_error_dict[error] = unicode(e)
				errors_dict['assign_service_lead_form_errors'] = assign_service_lead_form_error_dict
				return HttpResponseBadRequest(json.dumps(errors_dict), content_type='application/json')

	else:
		form = form1.ServiceForm(instance=service)
		servicesla_formset = servicesla_formset
		service_document_formset  = service_document_formset
		service_resource_formset  = service_resource_formset
		#if request.user.groups.filter(name='operations manager').exists():
		assign_service_lead_formset = assign_service_lead_formset
		resource_plans = models.ServiceResourcePlan.objects.filter(service=service)
		if request.method == "GET":

			download_doc = request.GET.get('document')
			print "download_doc", download_doc

		return render(request, 'project/service_add_partial.html', {'form': form ,
									'assign_service_lead_formset':assign_service_lead_formset,
									'servicesla_formset':servicesla_formset,
									'service_document_formset':service_document_formset,
									'service_resource_formset' : service_resource_formset,
									'service':service,
									'resource_plans':resource_plans,
									'is_edit_mode':True,
									'id':id
								}
					)

from django.core.files.uploadedfile import SimpleUploadedFile
def service_edit(request, id):
	success_dict={}
	errors_dict = {}
	success_dict = {}
	service = get_object_or_404(models.Service, id=id)

	#if request.user.groups.filter(name= 'sales manager').exists:
	try:
		key_pass = "invensis"
		aescipher = encrypt_decrypt.AESCipher(key_pass)

		amount_per_billing_type = aescipher.decrypt(service.encrypt_pricing)
		projected_prj_value_per_month = aescipher.decrypt(service.encrypt_projected_prj_value_per_month)
		projected_prj_value_per_annum = aescipher.decrypt(service.encrypt_projected_prj_value_per_annum)
		fte_cost_per_month = aescipher.decrypt(service.encrypt_fte_cost_per_month)

		service.amount_per_billing_type = float(amount_per_billing_type)
		service.projected_prj_value_per_month = float(projected_prj_value_per_month)
		service.projected_prj_value_per_annum = float(projected_prj_value_per_annum)
		service.fte_cost_per_month = float(fte_cost_per_month)

		service.save()
	except UnicodeDecodeError:
		pass

	except ValueError:
		pass

	AssignServiceLeadFormset = modelformset_factory(models.AssignServiceLead,form1.AssignServiceLeadForm, extra=1,exclude=('service',), can_delete=True)
	ServiceSlaFormset = modelformset_factory(models.ServiceSla, form1.ServiceSlaForm, extra=1, exclude=('service',), can_delete=True)
	ServiceDocumentFormset  = modelformset_factory(models.ServiceDocument, form1.ServiceDocumentInlineForm, extra=1, exclude=('service',), can_delete=True )
	ServiceResourcePlanFormset   = modelformset_factory(models.ServiceResourcePlan, form1.ServiceResourcePlanInlineForm, extra=1, exclude=('service',), can_delete=True)


	assign_service_lead_formset = AssignServiceLeadFormset(queryset=models.AssignServiceLead.objects.filter(service=service), prefix='assign_service_lead') 
	servicesla_formset = ServiceSlaFormset(queryset=models.ServiceSla.objects.filter(service=service), prefix='servicesla')
	service_document_formset = ServiceDocumentFormset(queryset=models.ServiceDocument.objects.filter(service=service), prefix='servicedoc')
	service_resource_formset = ServiceResourcePlanFormset(queryset=models.ServiceResourcePlan.objects.filter(service=service), prefix='resource_plan')

	if request.method == "POST":
		if request.user.groups.filter(name="sales manager").exists():
			form = form1.ServiceForm(request.POST, instance=service, customer=service.customer, billing_choice=service.billing_type)

			if service:
				servicesla_formset = ServiceSlaFormset(request.POST or None,  queryset=models.ServiceSla.objects.filter(service=service), prefix='servicesla')
				service_document_formset = ServiceDocumentFormset(request.POST or None, request.FILES, queryset=models.ServiceDocument.objects.filter(service=service), prefix='servicedoc')
				service_resource_formset = ServiceResourcePlanFormset(request.POST or None, queryset=models.ServiceResourcePlan.objects.filter(service=service), prefix='resource_plan')
				#assign_service_lead_formset = AssignServiceLeadFormset(request.POST or None, queryset=models.AssignServiceLead.objects.filter(service=service), prefix='assign_service_lead')	
			else:
				servicesla_formset = ServiceSlaFormset(request.POST or None,  queryset=models.ServiceSla.objects.none(), prefix='servicesla')
				service_document_formset = ServiceDocumentFormset(request.POST or None, request.FILES, queryset=models.ServiceDocument.objects.none(), prefix='servicedoc')
				service_resource_formset = ServiceResourcePlanFormset(request.POST or None, queryset=models.ServiceResourcePlan.objects.none(), prefix='resource_plan')
				#assign_service_lead_formset = AssignServiceLeadFormset(request.POST or None, queryset=models.AssignServiceLead.objects.none(), prefix='assign_service_lead')	

			print "servicesla_formset.deleted_forms", servicesla_formset.deleted_forms
			for service_sla_form in servicesla_formset.deleted_forms:
				#if followup_formset_form.cleaned_data.get('DELETE') and followup_formset_form.instance.pk:
				service_sla_form_instance = service_sla_form.instance
				if service_sla_form_instance.pk:
					service_sla_form_instance.delete()

			if request.user.groups.filter(name='sales manager').exists():
				for service_document_form in service_document_formset.deleted_forms:
					service_document_form_instance = service_document_form.instance
					if service_document_form_instance.pk:
						service_document_form_instance.delete()

			for service_resource_form in service_resource_formset.deleted_forms:
				service_resource_form_instance = service_resource_form.instance
				if service_resource_form_instance.pk:
					service_resource_form_instance.delete()


			if form.is_valid() and servicesla_formset.is_valid() and service_resource_formset.is_valid() and service_document_formset.is_valid():

				service_instance = form.save(commit=False)

				#service_instance.fte_cost_per_month = service.fte_cost_per_month
				service_instance.billing_interval_in_days = service.billing_interval_in_days

				pricing = form.cleaned_data.get('amount_per_billing_type')
				projected_prj_value_per_month = form.cleaned_data.get('projected_prj_value_per_month')
				projected_prj_value_per_annum = form.cleaned_data.get('projected_prj_value_per_annum')
				fte_cost_per_month = form.cleaned_data.get('fte_cost_per_month')

				key_pass = "invensis"
				aescipher = encrypt_decrypt.AESCipher(key_pass)

				encrypt_pricing = aescipher.encrypt(str(pricing))
				encrypt_projected_prj_value_per_month = aescipher.encrypt(str(projected_prj_value_per_month))
				encrypt_projected_prj_value_per_annum = aescipher.encrypt(str(projected_prj_value_per_annum))
				encrypt_fte_cost_per_month = aescipher.encrypt(str(fte_cost_per_month))

				service_instance.encrypt_pricing  = encrypt_pricing
				service_instance.encrypt_projected_prj_value_per_month = encrypt_projected_prj_value_per_month
				service_instance.encrypt_projected_prj_value_per_annum = encrypt_projected_prj_value_per_annum
				service_instance.encrypt_fte_cost_per_month = encrypt_fte_cost_per_month
				
				# service_instance.amount_per_billing_type = 0
				# service_instance.projected_prj_value_per_month = 0
				# service_instance.projected_prj_value_per_annum = 0
				# service_instance.fte_cost_per_month = 0
				service_instance.save()

				for service_sla_form in servicesla_formset:
					if service_sla_form not in [deleted_form for deleted_form in servicesla_formset.deleted_forms]:
						service_sla_formInstance = service_sla_form.save(commit=False)
						service_sla_formInstance.service = service_instance
						sla_type = service_sla_form.cleaned_data.get('sla_type')
						if sla_type not in  ['', None]:
							service_sla_formInstance.save()

				for service_resource_form in service_resource_formset:
					if service_resource_form not in [deleted_form for deleted_form in service_resource_formset.deleted_forms]:
						service_resource_formInstance = service_resource_form.save(commit=False)
						service_resource_formInstance.service = service_instance
						exp_slab = service_resource_form.cleaned_data.get('experience_slab')
						if exp_slab not in ['', None]:
							service_resource_formInstance.save()
				for service_document_form in service_document_formset:
					if service_document_form not in [deleted_form for deleted_form in service_document_formset.deleted_forms]:
						service_document_formInstance = service_document_form.save(commit=False)
						service_document_formInstance.service = service_instance
						service_document_type = service_document_form.cleaned_data.get('document_type')
						is_share_with_others = service_document_form.cleaned_data.get('share_with_others')
						service_doc_data = service_document_form.cleaned_data.get('document')
						otherdocument = request.POST.get('otherdocument')

						if service_document_type in ['nda', 'sla', 'agreement'] and service_doc_data not in ['', None]:
							if not service_doc_data.name.endswith('.enc'):
								#print service_doc_data.readlines()
								tmp_guid = uuid.uuid1()
								tmp_file_path ="temp/test_encryption_%s.txt" % tmp_guid
								path = default_storage.save(tmp_file_path, ContentFile(service_doc_data.read()))
								service_doc_nam = service_doc_data.name.split('.')
								tmp_encrypted_file_path = "service_documents/%s.%s" % (service_doc_nam[0],service_doc_nam[1]) 
								media_path = os.path.join(settings.MEDIA_ROOT, tmp_encrypted_file_path)								
								if default_storage.exists(path):
									file_path = os.path.join(settings.MEDIA_ROOT,path)									
									key_pass = "0123456789asdfgh"
									aescipher = encrypt_decrypt.AESCipher(key_pass)
									encrypt_service_doc = aescipher.encrypt_file(file_path, media_path)
									if encrypt_service_doc:
										encrypted_path = encrypt_service_doc.split('/')
										encrypt_file_path = '/'.join((encrypted_path[-2], encrypted_path[-1]))
										service_document_formInstance.document = encrypt_file_path
									default_storage.delete(path)
						service_document_formInstance.other_document_type = otherdocument

						if service_doc_data not in ['', None]:
							service_document_formInstance.save()
				success_dict['success_msg'] = "Successfully Edited Project Details"
				return HttpResponse(json.dumps(success_dict), content_type='application/json')
			else:
				if request.is_ajax():
					errors_dict = {}
					service_form_error_dict = {}
					service_sla_formset_error_dict = {}
					service_resource_formset_error_dict = {}
					service_document_formset_error_dict = {}
					for error in form.errors:
						e = form.errors[error]
						service_form_error_dict[error] = unicode(e)
					for f1 in service_document_formset:
						if f1.errors:
							for error in f1.errors:
								e = f1.errors[error]
								service_document_formset_error_dict[error] = unicode(e)
					try:
						for f1 in servicesla_formset:
							if f1.errors:
								for error in f1.errors:
									e = f1.errors[error]
									service_sla_formset_error_dict[error] = unicode(e)
						for f1 in service_resource_formset:
							if f1.errors:
								for error in f1.errors:
									e = f1.errors[error]
									service_resource_formset_error_dict[error] = unicode(e)
					except ValidationError:
						pass
					errors_dict['form_errors'] = service_form_error_dict
					errors_dict['sla_formset_errors'] = service_sla_formset_error_dict
					errors_dict['resource_formset_errors'] = service_resource_formset_error_dict
					errors_dict['document_formset_errors'] = service_document_formset_error_dict		
					return HttpResponseBadRequest(json.dumps(errors_dict))
		
		if request.user.groups.filter(name__in=['operations manager', 'lead']).exists():
			assign_service_lead_formset = AssignServiceLeadFormset(request.POST or None, form_kwargs={'request': request},queryset=models.AssignServiceLead.objects.filter(service=service), prefix='assign_service_lead')	

			for assign_service_lead_form in assign_service_lead_formset.deleted_forms:
				assign_service_lead_form_instance = assign_service_lead_form.instance
				if assign_service_lead_form_instance.pk:
					assign_service_lead_form_instance.delete()

			if assign_service_lead_formset.is_valid():
				for assign_service_lead_form in assign_service_lead_formset:
					if assign_service_lead_form not in [deleted_form for deleted_form in assign_service_lead_formset.deleted_forms]:
						assign_service_lead_form_instance = assign_service_lead_form.save(commit=False)
						assign_service_lead_form_instance.service = service
						lead = assign_service_lead_form.cleaned_data.get('lead')
						if lead not in ['', None]:
							assign_service_lead_form_instance.save()
					else:
						success_dict['success_msg'] = "Successfully removed project lead"
						return HttpResponse(json.dumps(success_dict), content_type='application/json')
				success_dict['success_msg'] = "Successfully assigned project to lead"
				return HttpResponse(json.dumps(success_dict), content_type='application/json')
			else:
				assign_service_lead_form_error_dict = {}
				for f1 in assign_service_lead_formset:
					if f1.errors:
						for error in f1.errors:
							e = f1.errors[error]
							assign_service_lead_form_error_dict[error] = unicode(e)
				errors_dict['assign_service_lead_form_errors'] = assign_service_lead_form_error_dict
				return HttpResponseBadRequest(json.dumps(errors_dict), content_type='application/json')
	else:
		form = form1.ServiceForm(instance=service, customer=service.customer, billing_choice=service.billing_type)
		servicesla_formset = servicesla_formset
		service_document_formset  = service_document_formset
		service_resource_formset  = service_resource_formset
		assign_service_lead_formset = AssignServiceLeadFormset(queryset=models.AssignServiceLead.objects.filter(service=service),form_kwargs={'request': request}, prefix='assign_service_lead')	
		resource_plans = models.ServiceResourcePlan.objects.filter(service=service)

		return render(request, 'project/service_add_partial.html', {'form': form ,
									'assign_service_lead_formset':assign_service_lead_formset,
									'servicesla_formset':servicesla_formset,
									'service_document_formset':service_document_formset,
									'service_resource_formset' : service_resource_formset,
									'service':service,
									'resource_plans':resource_plans,
									'is_edit_mode':True,
									'id':id
								}
					)



@login_required
def workweek_list(request):

	workweeks = models.WorkWeekType.objects.all()
	return render(request, 'project/workweeks_list_partial.html', 
					{'workweeks': workweeks}
				)


@login_required
def workweek_add(request):

	if request.method == 'POST':
		form = form1.WorkWeekTypeForm(request.POST, None)

		if form.is_valid():
			workweek = form.save(commit=False)
			#service_sla.title = form.cleaned_data['title']         
			workweek.save()
			# messages.add_message(request, messages.SUCCESS, _('Successfully Created BillingType'))
			# return HttpResponseRedirect(reverse('billing_types_list'))
			return HttpResponse('OK')
		else:
			error_dict = {}
			for error in form.errors:
				error_dict[error] = form.errors[ error]
			return HttpResponseBadRequest(json.dumps(error_dict))
			# messages.add_message(request, messages.ERROR, _('Please fix errors bellow.'))
	else:
		form = form1.WorkWeekTypeForm()

		return render(request, 'project/workweek_add_partial.html', {'form':form})


@login_required
def workweek_edit(request, id):
	workweek = get_object_or_404(models.WorkWeekType, id=id)
	if request.method == "POST":
		form = form1.WorkWeekTypeForm(request.POST, instance=workweek)
		if form.is_valid():
			workweek = form.save(commit=False)
			workweek.save()
			return HttpResponse('ok ')
		else:
			error_dict={}
			for error in form.errors:
				error_dict[error] = form.errors[error]
				
			return HttpResponseBadRequest(json.dumps(error_dict))
	else:
		form = form1.WorkWeekTypeForm(instance=workweek)

	return render(request, 'project/workweek_add_partial.html', {'form': form ,'is_edit_mode':True,'id':id})




@login_required
def service_sla_list(request):


	service_sla = models.ServiceSla.objects.all()
	return render(request, 'project/service_sla_list_partial.html', 
					{'service_sla': service_sla}

				)


@login_required
def service_sla_add(request):

	if request.method == 'POST':
		form = form1.ServiceSlaForm(request.POST, None)

		if form.is_valid():
			service_sla = form.save(commit=False)
			#service_sla.title = form.cleaned_data['title']
			
			service_sla.save()
			# messages.add_message(request, messages.SUCCESS, _('Successfully Created BillingType'))
			# return HttpResponseRedirect(reverse('billing_types_list'))
			return HttpResponse('OK')
		else:
			error_dict = {}
			for error in form.errors:
				error_dict[error] = form.errors[ error]

			return HttpResponseBadRequest(json.dumps(error_dict))
			# messages.add_message(request, messages.ERROR, _('Please fix errors bellow.'))


	else:
		form = form1.ServiceSlaForm()

		return render(request, 'project/service_sla_add_partial.html', {'form':form})


@login_required
def service_sla_edit(request, id):
	service_sla = get_object_or_404(models.ServiceSla, id=id)
	if request.method == "POST":
		form = form1.ServiceSlaForm(request.POST, instance=service_sla)
		if form.is_valid():
			service_sla = form.save(commit=False)
			service_sla.save()
			return HttpResponse('ok ')
		else:
			error_dict={}
			for error in form.errors:
				error_dict[error] = form.errors[error]
				
			return HttpResponseBadRequest(json.dumps(error_dict))
	else:
		form = form1.ServiceSlaForm(instance=service_sla)

	return render(request, 'project/service_sla_add_partial.html', {'form': form ,'is_edit_mode':True,'id':id})




@login_required
def sla_list(request):

	sla = models.Sla.objects.all()
	return render(request, 'project/sla_list_partial.html', 
					{'sla': sla}
				)

@login_required
def sla_add(request):

	if request.method == 'POST':
		form = form1.SlaForm(request.POST, None)

		if form.is_valid():
			sla = form.save(commit=False)
			sla.title = form.cleaned_data['title']
			sla.description = form.cleaned_data['description']
			sla.save()
			# messages.add_message(request, messages.SUCCESS, _('Successfully Created BillingType'))
			# return HttpResponseRedirect(reverse('billing_types_list'))
			return HttpResponse('OK')
		else:
			error_dict = {}
			for error in form.errors:
				error_dict[error] = form.errors[ error]

			return HttpResponseBadRequest(json.dumps(error_dict))
			# messages.add_message(request, messages.ERROR, _('Please fix errors bellow.'))


	else:
		form = form1.SlaForm()


		return render(request, 'project/sla_add_partial.html', {'form':form})
@login_required
def sla_edit(request, slug):
	sla = get_object_or_404(models.Sla, slug=slug)
	if request.method == "POST":
		form = form1.SlaForm(request.POST, instance=sla)
		if form.is_valid():
			sla = form.save(commit=False)
			sla.save()
			return HttpResponse('ok ')
		else:
			error_dict={}
			for error in form.errors:
				error_dict[error] = form.errors[error]
				
			return HttpResponseBadRequest(json.dumps(error_dict))
	else:
		form = form1.SlaForm(instance=sla)

	return render(request, 'project/sla_add_partial.html', {'form': form ,'is_edit_mode':True,'slug':slug})



@login_required
def service_document_list(request):

	service_document = models.ServiceDocument.objects.all()
	return render(request, 'project/service_document_list_partial.html', 
					{'service_document': service_document}
				)

@login_required
def service_document_add(request):

	if request.method == 'POST':

		form = form1.ServiceDocumentForm(request.POST or None, request.FILES )



		if form.is_valid():
			service_document = form.save(commit=False)
			
			service_document.save()
			# messages.add_message(request, messages.SUCCESS, _('Successfully Created BillingType'))
			# return HttpResponseRedirect(reverse('billing_types_list'))
			return HttpResponse('OK')
		else:
			error_dict = {}
			for error in form.errors:
				error_dict[error] = form.errors[ error]

			return HttpResponseBadRequest(json.dumps(error_dict))
			# messages.add_message(request, messages.ERROR, _('Please fix errors bellow.'))


	else:

		form = form1.ServiceDocumentForm()



		return render(request, 'project/service_document_add_partial.html', {'form':form})
@login_required

def service_document_edit(request, id):
	service_document = get_object_or_404(models.ServiceDocument, id=id)
	if request.method == "POST":

		form = form1.ServiceDocumentForm(request.POST or None,request.FILES, instance=service_document)

		if form.is_valid():
			service_document = form.save(commit=False)
			service_document.save()
			return HttpResponse('ok ')
		else:
			error_dict={}
			for error in form.errors:
				error_dict[error] = form.errors[error]
				
			return HttpResponseBadRequest(json.dumps(error_dict))
	else:

		form = form1.ServiceDocumentForm(instance=service_document)

	return render(request, 'project/service_document_add_partial.html', {'form': form ,'is_edit_mode':True,'id':id})



@login_required
def resource_plan_list(request):


	resource_plan = models.ServiceResourcePlan.objects.all()

	return render(request, 'project/resource_plan_list_partial.html', 
					{'resource_plan': resource_plan}
				)


@login_required
def resource_plan_add(request):

	if request.method == 'POST':
		form = form1.ServiceResourcePlanForm(request.POST, None)

		if form.is_valid():
			resource_plan = form.save(commit=False)
			resource_plan.experience_slab = form.cleaned_data['experience_slab']

			resource_plan.save()

			return HttpResponse('OK')
		else:
			error_dict = {}
			for error in form.errors:
				error_dict[error] = form.errors[ error]
			return HttpResponseBadRequest(json.dumps(error_dict))
	else:
		form = form1.ServiceResourcePlanForm()

		return render(request, 'project/resource_plan_add_partial.html', {'form':form})


@login_required
def resource_plan_edit(request, id):
	resource_plan = get_object_or_404(models.ServiceResourcePlan, id=id)
	if request.method == "POST":
		form = form1.ServiceResourcePlanForm(request.POST, instance=resource_plan)
		if form.is_valid():
			resource_plan = form.save(commit=False)
			resource_plan.save()
			return HttpResponse('ok ')
		else:
			error_dict={}
			for error in form.errors:
				error_dict[error] = form.errors[error]
			return HttpResponseBadRequest(json.dumps(error_dict))
	else:
		form = form1.ServiceResourcePlanForm(instance=resource_plan)
		return render(request, 'project/resource_plan_add_partial.html', {'form': form ,'is_edit_mode':True,'id':id})


@login_required
def task_list(request):
	if request.user.groups.filter(name='operations manager').exists():
		emp_usr = Employee.objects.filter(user__username=request.user)
		tasks = models.Task.objects.filter(service__operations_manager=emp_usr, status__in=['new', 'pending']).order_by('created')
		
		return render(request, 'project/task_list_partial.html', locals())


@login_required
def assign_lead(request, task_id=None):

	if not task_id:
		raise "task_id needs to be provided !"
	# LeadTaskFormset = formset_factory(form1.LeadTaskInlineForm, extra=1)
	get_task = get_object_or_404(models.Task, id=task_id)
	lead_tasks = models.LeadTask.objects.filter(task_id = task_id).select_related()

	lead_task_form_infos = []
	counter = 0
	# existing tasks
	"""
	if lead_tasks:

		LeadTaskResourceFormset = modelformset_factory(models.LeadTaskResourcePlan, form1.LeadTaskResourceInlineForm, extra=1, exclude=('lead_task',))
		if request.method == "POST":
			for lead_task in lead_tasks:
				lead_task_form =form1.LeadTaskForm(request.POST,instance=lead_task, prefix='lead_task_%s' % lead_task.id )
				resource_plan_formset = LeadTaskResourceFormset(request.POST or None, \
					queryset= models.LeadTaskResourcePlan.objects.filter(lead_task = lead_task), prefix='resource_formset_%s' % lead_task.id)
				lead_task_form_infos.append((task_id, lead_task.id, lead_task_form, resource_plan_formset ,))
				counter += 1
				# update*************
				for resource_plan_form in resource_plan_formset.deleted_forms:
					resource_plan_form_instance = resource_plan_form.instance
					if resource_plan_form_instance.pk:
						resource_plan_form_instance.delete

				if lead_task_form.is_valid() and resource_plan_formset.is_valid():
					lead_task_instance = lead_task_form.save(commit=False)
					lead_task_instance.task = get_task
					lead_task_instance.save()

					for resource_plan_form in resource_plan_formset:
						resource_plan_form_instance = resource_plan_form.save(commit=False)
						resource_plan_form_instance.lead_task = lead_task_instance
						resource_plan_form_instance.save()

					return HttpResponse('Successfully changed task and LeadTask')
				else:
					error_dict = {}
					lead_task_form_errors = {}
					resource_plan_formset_errors = {}
					
					for error in lead_task_form.errors:
						lead_task_form_errors[error] = lead_task_form.errors[error]

					for f1 in resource_plan_formset:
						if f1:
							for error in f1.errors:
								e = f1.errors[error]
								resource_plan_formset_errors[error] = unicode(e)
					error_dict['form_errors'] = lead_task_form_errors
					error_dict['formset_errors'] = resource_plan_formset_errors

					return HttpResponseBadRequest(json.dumps(error_dict))
		else:
			for lead_task in lead_tasks:
				lead_task_form =form1.LeadTaskForm( instance=lead_task, prefix='lead_task_%s' % lead_task.id)
				resource_plan_formset = LeadTaskResourceFormset( \
					prefix='resource_formset_%s' % lead_task.id, queryset= models.LeadTaskResourcePlan.objects.filter(lead_task = lead_task) )
				lead_task_form_infos.append( (task_id, lead_task.id, lead_task_form, resource_plan_formset ,))
				counter += 1
	else:
	""" # new tasks
	LeadTaskResourceFormset = formset_factory(form1.LeadTaskResourceInlineForm, extra=1,)
	if request.method == "POST":
		lead_task_form =form1.LeadTaskForm(request.POST,  prefix = 'lead_task_%s' % '0' )
		resource_plan_formset = LeadTaskResourceFormset(request.POST or None, \
			prefix='resource_formset_%s' % '0' )
		lead_task_form_infos.append( (task_id, 0, lead_task_form, resource_plan_formset ,))
		counter += 1
		# add ***************************
		for resource_plan_form in resource_plan_formset.deleted_forms:
			resource_plan_form_instance = resource_plan_form.instance
			if resource_plan_form_instance.pk:
				resource_plan_form_instance.delete

		if lead_task_form.is_valid() and resource_plan_formset.is_valid():
			lead_task_instance = lead_task_form.save(commit=False)
			lead_task_instance.task = get_task
			lead_task_instance.save()

			for resource_plan_form in resource_plan_formset:
				resource_plan_form_instance = resource_plan_form.save(commit=False)
				resource_plan_form_instance.lead_task = lead_task_instance
				resource_plan_form_instance.save()
			return HttpResponse('Successfully created LeadTasks')
		else:
			error_dict = {}
			lead_task_form_errors = {}
			resource_plan_formset_errors = {}
			
			for error in lead_task_form.errors:
				lead_task_form_errors[error] = lead_task_form.errors[error]

			for f1 in resource_plan_formset:
				if f1:
					for error in f1.errors:
						e = f1.errors[error]
						resource_plan_formset_errors[error] = unicode(e)
			error_dict['form_errors'] = lead_task_form_errors
			error_dict['formset_errors'] = resource_plan_formset_errors

			return HttpResponseBadRequest(json.dumps(error_dict))

	else:
		lead_task_form =form1.LeadTaskForm(prefix='lead_task_%s' % '0')
		resource_plan_formset = LeadTaskResourceFormset( \
			prefix='resource_formset_%s' % '0' )
		lead_task_form_infos.append( (task_id, 0, lead_task_form, resource_plan_formset ,))
		counter += 1
		print "lead_task_form_infos", lead_task_form_infos
	return render(request, 'project/assign_lead_partial.html', locals())


@login_required
def assign_lead_update(request, task_id=None, lead_task_id=None):

	if not task_id:
		raise "task_id needs to be provided !"

	# LeadTaskFormset = formset_factory(form1.LeadTaskInlineForm, extra=1)
	get_task = get_object_or_404(models.Task, id=task_id)
	lead_task_form_infos = []
	counter = None
	lead_task = None
	if lead_task_id:
		# update ***
		LeadTaskResourceFormset = modelformset_factory(models.LeadTaskResourcePlan, form1.LeadTaskResourceInlineForm, extra=1, exclude=('lead_task',))
		try:
			lead_task = models.LeadTask.objects.get(task_id=task_id, id=lead_task_id)
			
			if request.method == 'POST':
				lead_task_form = from1.LeadTaskForm(request.POST or None, instance=lead_task)
				resource_plan_formset = LeadTaskResourceFormset(request.POST or None, \
					queryset=models.LeadTaskResourcePlan.objects.filter(lead_task=lead_task),prefix='resource_formset_%s' % lead_task.id)
				lead_task_form_infos.append((task_id, lead_task.id, lead_task_form, resource_plan_formset ,))
				counter += 1

				for resource_plan_form in resource_plan_formset.deleted_forms:
					resource_plan_form_instance = resource_plan_form.instance
					if resource_plan_form_instance.pk:
						resource_plan_form_instance.delete

				if lead_task_form.is_valid() and resource_plan_formset.is_valid():

					lead_task_instance = lead_task_form.save(commit=False)
					lead_task_instance.task = get_task
					lead_task_instance.save()

					for resource_plan_form in resource_plan_formset:
						resource_plan_form_instance = resource_plan_form.save(commit=False)
						resource_plan_form_instance.lead_task= lead_task_form_instance
						resource_plan_form_instance.save()

					return HttpResponse('Successfully Updated lead_task details')
				else:

					error_dict = {}
					lead_task_form_error = {}
					resource_plan_formset_errors = {}

					for error in lead_task_form.errors:
						lead_task_form_error[error] = lead_task_form.errors[error]

					for f1 in resource_plan_formset:
						if f1:
							for error in f1.errors:
								e = f1.errors[error]
								resource_plan_formset_errors[error] = unicode(e)
					error_dict['form_errors'] = lead_task_form_error
					error_dict['formset_errors'] = resource_plan_formset_errors

					return HttpResponseBadRequest(json.dumps(error_dict))
		except models.LeadTask.DoesNotExist:
			lead_task = None
		except models.LeadTask.MultipleObjectsReturned:
			pass
							
	else:
		# add *********
		pass

	lead_task_form_infos = []
	counter = 0
	# existing tasks
	if lead_task:
		LeadTaskResourceFormset = modelformset_factory(models.LeadTaskResourcePlan, form1.LeadTaskResourceInlineForm, extra=1, exclude=('lead_task',))
		if request.method == "POST":
			lead_task_form =form1.LeadTaskForm(request.POST, instance=lead_task, prefix = 'lead_task_%s' % lead_task.id )
			resource_plan_formset = LeadTaskResourceFormset(request.POST or None, \
				prefix='resource_formset_%s' % lead_task.id, queryset= models.LeadTaskResourcePlan.objects.filter(lead_task = lead_task) )
			
			lead_task_form_infos.append((task_id, lead_task.id, lead_task_form, resource_plan_formset ,))
			counter += 1

			# update*************
			for resource_plan_form in resource_plan_formset.deleted_forms:
				resource_plan_form_instance = resource_plan_form.instance
				if resource_plan_form_instance.pk:
					resource_plan_form_instance.delete

			if lead_task_form.is_valid() and resource_plan_formset.is_valid():
				lead_task_form_instance = lead_task_form.save(commit=False)
				lead_task_form_instance.task = get_task
				lead_task_form_instance.save()

				for resource_plan_form in resource_plan_formset:
					resource_plan_form_instance = resource_plan_form.save(commit=False)
					resource_plan_form_instance.lead_task= lead_task_form_instance
					resource_plan_form_instance.save()

				return HttpResponse("Successfully updated LeadTask")
			else:
				error_dict = {}
				lead_task_form_error = {}
				resource_plan_formset_errors = {}

				for error in lead_task_form.errors:
					lead_task_form_error[error] = lead_task_form.errors[error]

				for f1 in resource_plan_formset:
					if f1:
						for error in f1.errors:
							e = f1.errors[error]
							resource_plan_formset_errors[error] = unicode(e)
				error_dict['form_errors'] = lead_task_form_error
				error_dict['formset_errors'] = resource_plan_formset_errors

				return HttpResponseBadRequest(json.dumps(error_dict))

		else:
			lead_task_form =form1.LeadTaskForm( instance=lead_task, prefix='lead_task_%s' % lead_task.id)
			resource_plan_formset = LeadTaskResourceFormset( \
				prefix='resource_formset_%s' % lead_task.id, queryset= models.LeadTaskResourcePlan.objects.filter(lead_task = lead_task) )
				

	else:
		# new tasks
		if request.method == "POST":
			lead_task_form =form1.LeadTaskForm(request.POST,  prefix = 'lead_task_%s' % '0' )
			resource_plan_formset = LeadTaskResourceFormset(request.POST or None, \
				prefix='resource_formset_%s' % '0' )
			lead_task_form_infos.append( (task_id, 0, lead_task_form, resource_plan_formset ,))
			counter += 1

			# add ***************************
			
			for resource_plan_form in resource_plan_formset.deleted_forms:
				resource_plan_form_instance = resource_plan_form.instance
				if resource_plan_form_instance.pk:
					resource_plan_form_instance.delete

			if lead_task_form.is_valid() and resource_plan_formset.is_valid():
				lead_task_form_instance = lead_task_form.save(commit=False)
				lead_task_form_instance.task = get_task
				lead_task_form_instance.save()

				for resource_plan_form in resource_plan_formset:
					resource_plan_form_instance = resource_plan_form.save(commit=False)
					resource_plan_form_instance.lead_task= lead_task_form_instance
					resource_plan_form_instance.save()

				return HttpResponse("Successfully added LeadTask")
			else:
				error_dict = {}
				lead_task_form_error = {}
				resource_plan_formset_errors = {}

				for error in lead_task_form.errors:
					lead_task_form_error[error] = lead_task_form.errors[error]

				for f1 in resource_plan_formset:
					if f1:
						for error in f1.errors:
							e = f1.errors[error]
							resource_plan_formset_errors[error] = unicode(e)
				error_dict['form_errors'] = lead_task_form_error
				error_dict['formset_errors'] = resource_plan_formset_errors

				return HttpResponseBadRequest(json.dumps(error_dict))

		else:
			lead_task_form =form1.LeadTaskForm(  prefix='lead_task_%s' % '0')
			resource_plan_formset = LeadTaskResourceFormset( \
				prefix='resource_formset_%s' % '0' )
			

	return render(request, 'project/assign_lead_partial.html', locals())


@login_required
def task_add_orig(request, service_id=None):

	errors_dict ={}
	success_dict = {}
	lead_task_form_infos=[]
	task_id='new_task'
	#counter = 1
	# validate input
	if not service_id:
		raise "invalid service id"
	service_name = get_object_or_404(models.Service, id=service_id)
	#TaskResourceFormset = formset_factory(form1.TaskResourcePlanForm, extra=1)
	LeadTaskResourceFormset = formset_factory(form1.LeadTaskResourceInlineForm, extra=1,)

	if request.method == 'POST':
		# lead_task_form_infos=[]
		counter = request.POST.get('add_lead_counter', None)
		print 'counter', counter
		if counter:
			for c in range(1, int(counter)+1):
				lead_task_form =form1.LeadTaskForm(request.POST,  prefix = 'lead_task_new-%s' % str(c) )
				lead_task_resource_plan_formset = LeadTaskResourceFormset(request.POST or None, \
					prefix='resource_formset_new-%s' % str(c) )
				lead_task_form_infos.append( (task_id, 'new-%s' % str(c), lead_task_form, lead_task_resource_plan_formset ,))
					
				if lead_task_form.is_valid() and lead_task_resource_plan_formset.is_valid():
					pass
				else:
					lead_task_form_errors = {}
					lead_resource_plan_formset_errors = {}
					
					for lead_task_form in lead_task_form_infos:
						for error in lead_task_form[2].errors:
							lead_task_form_errors[error] = lead_task_form[2].errors[error]
					try:
						for lead_task_resource_formset in lead_task_form_infos:
							for f1 in lead_task_resource_formset[3]:
								for error in f1.errors:
									e = f1.errors[error]
									lead_resource_plan_formset_errors[error] = unicode(e)
					except ValidationError:
						pass
					errors_dict['lead_task_form_errors'] = lead_task_form_errors
					errors_dict['lead_resource_plan_formset_errors'] = lead_resource_plan_formset_errors

		form = form1.TaskForm(request.POST, None)
		if form.is_valid():
			with transaction.atomic():
				task = form.save(commit=False)
				task.service_id = service_id
				task.created_by = request.user
				number_of_transactions = form.cleaned_data.get('no_of_txs')

				print "---------------------"
				print lead_task_form_infos
				total_leads_transactions = []
				is_lead_resource_plan_equal = False
				lead_transactions_plan_equal = False
				total_resource_plan_list = []
				task_resource_form_lists = []
				lead_resource_plan_list = []
				task_resource_form_dict = {}
				form_wise_resource_list = []
				resource_usage_list = []
				form_wise_resource_dict ={}
				custom_error_dict = {}
		
				if counter:
					for i, form_info in enumerate(lead_task_form_infos):
						print "form infos",form_info
						lead_task_form = form_info[2]
						resource_plan_formset = form_info[3]

						for resource_plan_form in resource_plan_formset.deleted_forms:
							 resource_plan_form_instance = resource_plan_form.instance
							 if resource_plan_form_instance.pk:
								resource_plan_form_instance.delete()

						if lead_task_form.is_valid() and resource_plan_formset.is_valid():
							lead_task_instance = lead_task_form.save(commit=False)
							#lead_task_instance.task = task
							lead_form_transactions = lead_task_form.cleaned_data.get('no_of_txs')
							#lead_task_instance.save()

							for resource_plan_form in resource_plan_formset:
								if resource_plan_form not in [deleted_form for deleted_form in resource_plan_formset.deleted_forms]:
									resource_plan_form_instance = resource_plan_form.save(commit=False)
									resource_plan_form_instance.lead_task = lead_task_instance
									experience_slab = resource_plan_form.cleaned_data.get('experience_slab', None)
									number_of_resource = resource_plan_form.cleaned_data.get('number_of_resources', None)
									output_count_per_resource = resource_plan_form.cleaned_data.get('output_count_per_resource', None)

									print "++++++++++++++++++"
									if number_of_resource and output_count_per_resource not in ['', None]:
										resource_target_per_plan = number_of_resource * output_count_per_resource
										form_wise_resource_list.append(resource_target_per_plan)

										total_resource_plan_list.append(resource_target_per_plan)
										print "printing total_resource_plan_list", total_resource_plan_list
										exp_slab = ExperienceSlab.objects.get(title=experience_slab)
										resource_usage_list.append(number_of_resource)
										task_resource_form_lists.append([exp_slab, number_of_resource, output_count_per_resource, resource_target_per_plan])
										#print "printing task_resource_form_lists at saving", task_resource_form_lists
							
							form_wise_resource_dict[i] = sum(form_wise_resource_list)
							if form_wise_resource_list:
								print "lead_form_transactions",lead_form_transactions
								print "total_resource_plan_list per lead", sum(form_wise_resource_list)
								print "form_wise_resource_dict", form_wise_resource_dict

								project_resource = service_name.number_of_resources
								print "project_resource", project_resource
								print "resource_usage_list", resource_usage_list

								#if not sum(resource_usage_list) > project_resource:
								if lead_form_transactions == sum(form_wise_resource_list):
									is_lead_resource_plan_equal = True
									print "is_lead_resource_plan_equal", is_lead_resource_plan_equal
									form_wise_resource_list = []
									print "form_wise_resource_list", form_wise_resource_list

									task.save()
									lead_task_instance.task = task
									lead_task_instance.save()
									try:
										for resource_plan_form in resource_plan_formset:
											if resource_plan_form not in [deleted_form for deleted_form in resource_plan_formset.deleted_forms]:
												resource_plan_form_instance = resource_plan_form.save(commit=False)
												resource_plan_form_instance.lead_task = lead_task_instance
												resource_plan_form_instance.save()
									except IntegrityError:
										pass
								else:
									raise Exception("Lead resource plan is not equal to numbber of transaction")

									#custom_error_dict['error'] = "Lead resource plan is not equal to numbber of transaction"
									#errors_dict['custom_error_dict'] = custom_error_dict
									#return HttpResponseBadRequest(json.dumps(errors_dict), content_type="application/json")		
								#else:
								#	custom_error_dict['error'] = "Number of resource usage is more than project resources"
								#	errors_dict['custom_error_dict'] = custom_error_dict
								#	return HttpResponseBadRequest(json.dumps(errors_dict), content_type="application/json")		

						else:
							lead_task_form_errors = {}
							lead_resource_plan_formset_errors = {}
							
							for error in form_info[2].errors:
									lead_task_form_errors[error] = form_info[2].errors[error]
							try:
								for f1 in form_info[3]:
									for error in f1.errors:
										e = f1.errors[error]
										lead_resource_plan_formset_errors[error] = unicode(e)
								errors_dict['lead_task_form_errors'] = lead_task_form_errors
								errors_dict['lead_resource_plan_formset_errors'] = lead_resource_plan_formset_errors
							except ValidationError:
								pass
					
					print "total_resource_plan_list per lead", sum(total_resource_plan_list)
					print "number_of_transactions", number_of_transactions

					if number_of_transactions == sum(total_resource_plan_list):
						lead_transactions_plan_equal = True

						for i, task_resource_plan_list in enumerate(task_resource_form_lists):
							#print "task_resource_plan_list[0]", task_resource_plan_list[0]
							if task_resource_form_dict:
								print "task_resource_form_dict start", task_resource_form_dict
								if task_resource_plan_list[0] in task_resource_form_dict:
									no_of_total_resource = task_resource_form_dict[task_resource_plan_list[0]][0] + task_resource_plan_list[1]
									total_resource_target =  task_resource_form_dict[task_resource_plan_list[0]][1] + task_resource_plan_list[2]

									resource_mul_target =  task_resource_form_dict[task_resource_plan_list[0]][2] + task_resource_plan_list[3]
									#avg_target_per_resource = float(format(resource_mul_target/no_of_total_resource, '.2f'))
									#print "avg_target_per_resource", avg_target_per_resource								
									task_resource_form_dict[task_resource_plan_list[0]] = [no_of_total_resource,  total_resource_target, resource_mul_target]
								else:
									task_resource_form_dict[task_resource_plan_list[0]] = [task_resource_plan_list[1] , task_resource_plan_list[2], task_resource_plan_list[3]]
							else:
								task_resource_form_dict[task_resource_plan_list[0]] = [task_resource_plan_list[1] , task_resource_plan_list[2], task_resource_plan_list[3]]

						#print "task_resource_form_dict on complete", task_resource_form_dict	


					if is_lead_resource_plan_equal and lead_transactions_plan_equal:
						if number_of_transactions == sum(total_resource_plan_list):
							for key, val in task_resource_form_dict.items():
								print "value at saving", val
								task_resource_plan = models.TaskResourcePlan(
														task = task,
														experience_slab = key,
														number_of_resources = val[0],
														output_count_per_resource = float(format(val[2]/val[0], '.2f'))
								)

								task_resource_plan.save()

						else:
							custom_error_dict['error'] = "Number of tansactions of task and number of lead transactions are not matching,"
							errors_dict['custom_error_dict'] = custom_error_dict
							return HttpResponseBadRequest(json.dumps(errors_dict), content_type="application/json")		
					else:
						custom_error_dict['error'] = "Number of tansactions, Resource plan is not matching,"
						errors_dict['custom_error_dict'] = custom_error_dict
						return HttpResponseBadRequest(json.dumps(errors_dict), content_type="application/json")	

			success_dict['success_msg'] = "Successfully created lead tasks"
			return HttpResponse(json.dumps(success_dict), content_type='application/json')

		else:
			form_error_dict = {}
			task_formset_error_dict = {}
			for error in form.errors:
				form_error_dict[error] = form.errors[error]

			#for f1 in task_resource_formset_forms:
			#	if f1:
			#		for error in f1.errors:
			#			e= f1.errors[error]
			#			task_formset_error_dict[error] = unicode(e)
			errors_dict['form_errors'] = form_error_dict
			#errors_dict['task_formset_error_dict'] = task_formset_error_dict

			return HttpResponseBadRequest(json.dumps(errors_dict))
	else:
		form = form1.TaskForm(initial={'title': '%s--dailytask--%s' %(service_name, datetime.now())})
		#task_resource_formset_forms = TaskResourceFormset(prefix='task_resource_plan')
		counter = 1
		lead_task_form =form1.LeadTaskForm(prefix='lead_task_%s' % 'new-%s' %str(counter))
		resource_plan_formset = LeadTaskResourceFormset( prefix='resource_formset_new-%s' %str(counter) )
		lead_task_form_infos.append( (task_id, 'new-%s' %str(counter), lead_task_form, resource_plan_formset ,))
		
		#print "lead_task_form_infos", lead_task_form_infos

		return render(request, 'project/task_add_partial.html', locals())


@login_required
def exp_based_employees_list(request):
	if request.is_ajax():
		exp_slab = ExperienceSlab.objects.get(id=request.POST.get('exp_slab'))

		try:
			emp_exp = models.EmployeeAssignment.objects.filter(experience_slab=exp_slab)
			print "emp_exp", emp_exp
			data_dict = {"emp_exp":emp_exp}
		except models.EmployeeAssignment.DoesNotExist:
			staff_exp_dict['emp_not_exist'] = "Experience does not exist"
			pass


	return render(request,'project/exp_based_employees_list_partial.html', locals())


@login_required
def task_add(request, service_id=None):

	errors_dict ={}
	success_dict = {}
	lead_task_form_infos=[]
	task_id='new_task'
	#counter = 1
	# validate input
	if not service_id:
		raise "invalid service id"
	service_name = get_object_or_404(models.Service, id=service_id)
	#TaskResourceFormset = formset_factory(form1.TaskResourcePlanForm, extra=1)
	LeadTaskResourceFormset = formset_factory(form1.LeadTaskResourceInlineForm, extra=1,)

	if request.method == 'POST':
		# lead_task_form_infos=[]
		counter = request.POST.get('add_lead_counter', None)
		if counter:
			for c in range(1, int(counter)+1):
				lead_task_form =form1.LeadTaskForm(request.POST, request=request, prefix = 'lead_task_new-%s' % str(c) )
				lead_task_resource_plan_formset = LeadTaskResourceFormset(request.POST or None, \
					prefix='resource_formset_new-%s' % str(c) )
				lead_task_form_infos.append( (task_id, 'new-%s' % str(c), lead_task_form, lead_task_resource_plan_formset ,))
					
				if lead_task_form.is_valid() and lead_task_resource_plan_formset.is_valid():
					pass
				else:
					lead_task_form_errors = {}
					lead_resource_plan_formset_errors = {}
					
					for lead_task_form in lead_task_form_infos:
						for error in lead_task_form[2].errors:
							lead_task_form_errors[error] = lead_task_form[2].errors[error]
					try:
						for lead_task_resource_formset in lead_task_form_infos:
							for f1 in lead_task_resource_formset[3]:
								for error in f1.errors:
									e = f1.errors[error]
									lead_resource_plan_formset_errors[error] = unicode(e)
					except ValidationError:
						pass
					errors_dict['lead_task_form_errors'] = lead_task_form_errors
					errors_dict['lead_resource_plan_formset_errors'] = lead_resource_plan_formset_errors

		form = form1.TaskForm(request.POST, None)
		if form.is_valid():

			task = form.save(commit=False)
			task.service_id = service_id
			task.created_by = request.user
			number_of_transactions = form.cleaned_data.get('no_of_txs')

			total_leads_transactions = []
			is_lead_resource_plan_equal = False
			lead_transactions_plan_equal = False
			total_resource_plan_list = []
			task_resource_form_lists = []
			lead_resource_plan_list = []
			task_resource_form_dict = {}
			form_wise_resource_list = []
			resource_usage_list = []
			form_wise_resource_dict ={}
			custom_error_dict = {}
	
			if counter:
				try:
					with transaction.atomic():
						for i, form_info in enumerate(lead_task_form_infos):
							lead_task_form = form_info[2]
							resource_plan_formset = form_info[3]

							for resource_plan_form in resource_plan_formset.deleted_forms:
								 resource_plan_form_instance = resource_plan_form.instance
								 if resource_plan_form_instance.pk:
									resource_plan_form_instance.delete()

							if lead_task_form.is_valid() and resource_plan_formset.is_valid():
								lead_task_instance = lead_task_form.save(commit=False)
								lead_form_transactions = lead_task_form.cleaned_data.get('no_of_txs')

								for resource_plan_form in resource_plan_formset:
									if resource_plan_form not in [deleted_form for deleted_form in resource_plan_formset.deleted_forms]:
										resource_plan_form_instance = resource_plan_form.save(commit=False)
										resource_plan_form_instance.lead_task = lead_task_instance
										experience_slab = resource_plan_form.cleaned_data.get('experience_slab', None)
										number_of_resource = resource_plan_form.cleaned_data.get('number_of_resources', None)
										output_count_per_resource = resource_plan_form.cleaned_data.get('output_count_per_resource', None)

										if number_of_resource and output_count_per_resource not in ['', None]:
											resource_target_per_plan = number_of_resource * output_count_per_resource
											form_wise_resource_list.append(resource_target_per_plan)

											total_resource_plan_list.append(resource_target_per_plan)
											print "printing total_resource_plan_list", total_resource_plan_list
											exp_slab = ExperienceSlab.objects.get(title=experience_slab)
											resource_usage_list.append(number_of_resource)
											task_resource_form_lists.append([exp_slab, number_of_resource, output_count_per_resource, resource_target_per_plan])
											#print "printing task_resource_form_lists at saving", task_resource_form_lists
								
								form_wise_resource_dict[i] = sum(form_wise_resource_list)
								if form_wise_resource_list:
									print "lead_form_transactions",lead_form_transactions
									print "total_resource_plan_list per lead", sum(form_wise_resource_list)
									print "form_wise_resource_dict", form_wise_resource_dict

									project_resource = service_name.number_of_resources

									if lead_form_transactions == sum(form_wise_resource_list):
										is_lead_resource_plan_equal = True
										print "is_lead_resource_plan_equal", is_lead_resource_plan_equal
										form_wise_resource_list = []
										print "form_wise_resource_list", form_wise_resource_list

							else:
								lead_task_form_errors = {}
								lead_resource_plan_formset_errors = {}
								
								for error in form_info[2].errors:
										lead_task_form_errors[error] = form_info[2].errors[error]
								try:
									for f1 in form_info[3]:
										for error in f1.errors:
											e = f1.errors[error]
											lead_resource_plan_formset_errors[error] = unicode(e)
									errors_dict['lead_task_form_errors'] = lead_task_form_errors
									errors_dict['lead_resource_plan_formset_errors'] = lead_resource_plan_formset_errors
								except ValidationError:
									pass
						
						print "total_resource_plan_list per lead", sum(total_resource_plan_list)
						print "number_of_transactions", number_of_transactions

						for i, task_resource_plan_list in enumerate(task_resource_form_lists):
							if task_resource_form_dict:
								print "task_resource_form_dict start", task_resource_form_dict
								if task_resource_plan_list[0] in task_resource_form_dict:
									no_of_total_resource = task_resource_form_dict[task_resource_plan_list[0]][0] + task_resource_plan_list[1]
									total_resource_target =  task_resource_form_dict[task_resource_plan_list[0]][1] + task_resource_plan_list[2]
									resource_mul_target =  task_resource_form_dict[task_resource_plan_list[0]][2] + task_resource_plan_list[3]
									task_resource_form_dict[task_resource_plan_list[0]] = [no_of_total_resource,  total_resource_target, resource_mul_target]
								else:
									task_resource_form_dict[task_resource_plan_list[0]] = [task_resource_plan_list[1] , task_resource_plan_list[2], task_resource_plan_list[3]]
							else:
								task_resource_form_dict[task_resource_plan_list[0]] = [task_resource_plan_list[1] , task_resource_plan_list[2], task_resource_plan_list[3]]
						print "task_resource_form_dict on complete", task_resource_form_dict	

						if is_lead_resource_plan_equal:
							if number_of_transactions == sum(total_resource_plan_list):
								for i, form_info in enumerate(lead_task_form_infos):
									print "form infos",form_info
									lead_task_form = form_info[2]
									resource_plan_formset = form_info[3]

									task.save()
									lead_task_instance = lead_task_form.save(commit=False)
									lead_task_instance.task = task
									lead_task_instance.save()
									try:
										for resource_plan_form in resource_plan_formset:
											if resource_plan_form not in [deleted_form for deleted_form in resource_plan_formset.deleted_forms]:
												resource_plan_form_instance = resource_plan_form.save(commit=False)
												resource_plan_form_instance.lead_task = lead_task_instance
												resource_plan_form_instance.save()
									except IntegrityError:
										pass

								for key, val in task_resource_form_dict.items():
									print "value at saving", val
									task_resource_plan = models.TaskResourcePlan(
															task = task,
															experience_slab = key,
															number_of_resources = val[0],
															output_count_per_resource = float(format(val[2]/val[0], '.2f'))
									)

									task_resource_plan.save()

							else:
								custom_error_dict['error'] = "Number of tansactions of task and number of lead transactions are not matching,"
								errors_dict['custom_error_dict'] = custom_error_dict
								return HttpResponseBadRequest(json.dumps(errors_dict), content_type="application/json")		
						else:
							custom_error_dict['error'] = "Number of tansactions, Resource plan is not matching,"
							errors_dict['custom_error_dict'] = custom_error_dict
							return HttpResponseBadRequest(json.dumps(errors_dict), content_type="application/json")	
				except Exception:
					custom_error_dict['error'] = "Number of tansactions, Resource plan is not matching,"
					errors_dict['custom_error_dict'] = custom_error_dict
					return HttpResponseBadRequest(json.dumps(errors_dict), content_type="application/json")	

			success_dict['success_msg'] = "Successfully created lead tasks"
			return HttpResponse(json.dumps(success_dict), content_type='application/json')

		else:
			form_error_dict = {}
			task_formset_error_dict = {}
			for error in form.errors:
				form_error_dict[error] = form.errors[error]

			errors_dict['form_errors'] = form_error_dict

			return HttpResponseBadRequest(json.dumps(errors_dict))
	else:
		form = form1.TaskForm(initial={'title': '%s--dailytask--%s' %(service_name, datetime.now())})
		counter = 1
		lead_task_form =form1.LeadTaskForm(request=request, prefix='lead_task_%s' % 'new-%s' %str(counter))
		resource_plan_formset = LeadTaskResourceFormset( prefix='resource_formset_new-%s' %str(counter) )
		lead_task_form_infos.append( (task_id, 'new-%s' %str(counter), lead_task_form, resource_plan_formset ,))
		
		return render(request, 'project/task_add_partial.html', locals())


@login_required
def assign_lead_empty(request):
	
	counter=None

	task_id='new_task'
	LeadTaskResourceFormset = formset_factory(form1.LeadTaskResourceInlineForm, extra=1,)


	if request.GET:
		counter = request.GET.get('counter', None)

	lead_task_form_infos=[]
	if counter:
		counter = int(counter)+1
	else:
		counter = 1

	lead_task_form =form1.LeadTaskForm(request=request, prefix='lead_task_new-%s' %  str(counter))
	resource_plan_formset = LeadTaskResourceFormset(prefix='resource_formset_new-%s' % str(counter))

	lead_task_form_infos.append( (task_id, 'new-%s' % str(counter), lead_task_form, resource_plan_formset ,))
	# counter += 1
	return render(request, 'project/assign_lead_empty.html', locals())

@login_required
def task_edit(request, task_id):

	error_dict ={}
	errors_dict ={}
	success_dict = {}
	lead_task_form_infos=[]
	#task_id='new_task'
	#counter = 1
	# validate input

	task = get_object_or_404(models.Task, id=task_id) 
	service_name = get_object_or_404(models.Service, id=task.service_id)

	lead_tasks = models.LeadTask.objects.filter(task=task)
	form = form1.TaskForm()

	LeadTaskResourceFormset = modelformset_factory(models.LeadTaskResourcePlan, form1.LeadTaskResourceInlineForm, extra=0,)

	task_form = form1.TaskForm(instance=task)

	if request.method == 'POST':
		# lead_task_form_infos=[]
		counter = request.POST.get('add_lead_counter', None)
		lead_tasks = [lead_task for lead_task in lead_tasks]
		if lead_tasks:
			for i, leadtask in enumerate(lead_tasks):
				lead_task_id = leadtask.id
				lead_task_form =form1.LeadTaskForm(request.POST,instance=leadtask, request=request, prefix = 'lead_task_%s' % str(lead_task_id) )

				print models.LeadTaskResourcePlan.objects.filter(lead_task=leadtask)

				lead_task_resource_plan_formset = LeadTaskResourceFormset(request.POST, queryset=models.LeadTaskResourcePlan.objects.filter(lead_task=leadtask),\
					prefix='resource_formset_%s' % str(lead_task_id) )

				lead_task_form_infos.append( (task_id, '%s' % str(lead_task_id), lead_task_form, lead_task_resource_plan_formset ,))
				
				if lead_task_form.is_valid() and lead_task_resource_plan_formset.is_valid():
					pass
				else:
					lead_task_form_errors = {}
					lead_resource_plan_formset_errors = {}
					
					for lead_task_form in lead_task_form_infos:
						for error in lead_task_form[2].errors:
							lead_task_form_errors[error] = lead_task_form[2].errors[error]
					try:
						for lead_task_resource_formset in lead_task_form_infos:
							for f1 in lead_task_resource_formset[3]:
								for error in f1.errors:
									e = f1.errors[error]
									lead_resource_plan_formset_errors[error] = unicode(e)
							errors_dict['lead_task_form_errors'] = lead_task_form_errors
							errors_dict['lead_resource_plan_formset_errors'] = lead_resource_plan_formset_errors
					except ValidationError:
						pass
					
		if counter:
			for c in range(1, int(counter)+1):
				lead_task_form = form1.LeadTaskForm(request.POST, request=request, prefix='lead_task_new-%s' %str(c))
				lead_task_resource_plan_formset = LeadTaskResourceFormset(request.POST, prefix='resource_formset_new-%s' %str(c))
				lead_task_form_infos.append((task_id, 'new-%s' %str(c), lead_task_form, lead_task_resource_plan_formset))
		
		form = form1.TaskForm(request.POST or None, instance=task)

		if form.is_valid():
			with transaction.atomic():
				task = form.save(commit=False)
				number_of_transactions = form.cleaned_data.get('no_of_txs')
				#task.save()

				total_resource_plan_list = []
				task_resource_form_lists = []
				lead_transactions_list = []
				task_resource_form_dict ={}
				form_wise_resource_dict = {}
				form_wise_resource_list = []
				resource_usage_list = []
				lead_transactions_plan_equal = False
				is_lead_resource_plan_equal = False
				custom_error_dict = {}
				if lead_task_form_infos:
					for i, form_info in enumerate(lead_task_form_infos):
						print "form infos",form_info
						lead_task_form = form_info[2]
						resource_plan_formset = form_info[3]


						#print "resource_plan_formset.deleted_forms", resource_plan_formset.deleted_forms
						#for resource_plan_form in resource_plan_formset.deleted_forms:
						#	resource_plan_form_instance = resource_plan_form.instance
						#	if resource_plan_form_instance.pk:
						#		resource_plan_form_instance.delete()


						if lead_task_form.is_valid() and resource_plan_formset.is_valid():
							lead_task_instance = lead_task_form.save(commit=False)
							#lead_task_instance.task = task
							lead_form_transactions = lead_task_form.cleaned_data.get('no_of_txs')
							lead_transactions_list.append(lead_form_transactions)
							for resource_plan_form in resource_plan_formset:
								resource_plan_form_instance = resource_plan_form.save(commit=False)
								#resource_plan_form_instance.lead_task = lead_task_instance
								id = resource_plan_form.cleaned_data.get('id')
								#print "id", id
								experience_slab = resource_plan_form.cleaned_data.get('experience_slab', None)
								number_of_resource = resource_plan_form.cleaned_data.get('number_of_resources', None)
								output_count_per_resource = resource_plan_form.cleaned_data.get('output_count_per_resource', None)

								if number_of_resource and output_count_per_resource not in ['', None]:
									resource_target_per_plan = number_of_resource * output_count_per_resource
									form_wise_resource_list.append(resource_target_per_plan)

									total_resource_plan_list.append(resource_target_per_plan)
									print "printing total_resource_plan_list", total_resource_plan_list
									exp_slab = ExperienceSlab.objects.get(title=experience_slab)
									resource_usage_list.append(number_of_resource)
									task_resource_form_lists.append([exp_slab, number_of_resource, output_count_per_resource, resource_target_per_plan, id])
							
							form_wise_resource_dict[i] = sum(form_wise_resource_list)
							if form_wise_resource_list:
								project_resource = service_name.number_of_resources
								if lead_form_transactions == sum(form_wise_resource_list):
									is_lead_resource_plan_equal = True
									form_wise_resource_list[:] = []

									task.save()
									lead_task_instance.task = task
									lead_task_instance.save()
									for resource_plan_form in resource_plan_formset:

										if resource_plan_form not in [deleted_form for deleted_form in resource_plan_formset.deleted_forms]:
											if resource_plan_form not in ['', None]:
												resource_plan_form_instance = resource_plan_form.save(commit=False)
												resource_plan_form_instance.lead_task = lead_task_instance
												experience_slab = resource_plan_form.cleaned_data.get('experience_slab', None)

												if experience_slab not in ['', None]:
													resource_plan_form_instance.save()	
											else:
												custom_error_dict['error'] = "Please add resource plan"
												error_dict['custom_error_dict'] = custom_error_dict
												return HttpResponseBadRequest(json.dumps(error_dict), content_type="application/json")							
										else:
											resource_plan_form_instance = resource_plan_form.instance
											if resource_plan_form_instance.pk:
												resource_plan_form_instance.delete()

								else:
									custom_error_dict['error'] = "Lead resource plan is not equal to number of transaction"
									error_dict['custom_error_dict'] = custom_error_dict
									return HttpResponseBadRequest(json.dumps(error_dict), content_type="application/json")							
							else:
								custom_error_dict['error'] = "Please add resource plan to lead %s" %str(i+1)
								error_dict['custom_error_dict'] = custom_error_dict
								return HttpResponseBadRequest(json.dumps(error_dict), content_type="application/json")	

						else:
							lead_task_form_errors = {}
							lead_resource_plan_formset_errors = {}
							
							for error in form_info[2].errors:
									lead_task_form_errors[error] = form_info[2].errors[error]
							try:
								for f1 in form_info[3]:
									for error in f1.errors:
										e = f1.errors[error]
										lead_resource_plan_formset_errors[error] = unicode(e)
								errors_dict['lead_task_form_errors'] = lead_task_form_errors
								errors_dict['lead_resource_plan_formset_errors'] = lead_resource_plan_formset_errors
							except ValidationError:
								pass
					

					for i, task_resource_plan_list in enumerate(task_resource_form_lists):
						if task_resource_form_dict:
							if task_resource_plan_list[0] in task_resource_form_dict:
								no_of_total_resource = task_resource_form_dict[task_resource_plan_list[0]][0] + task_resource_plan_list[1]
								total_resource_target =  task_resource_form_dict[task_resource_plan_list[0]][1] + task_resource_plan_list[2]

								resource_mul_target =  task_resource_form_dict[task_resource_plan_list[0]][2] + task_resource_plan_list[3]
								#avg_target_per_resource = float(format(resource_mul_target/no_of_total_resource, '.2f'))
								#print "avg_target_per_resource", avg_target_per_resource								
								task_resource_form_dict[task_resource_plan_list[0]] = [no_of_total_resource,  total_resource_target, resource_mul_target]
							else:
								task_resource_form_dict[task_resource_plan_list[0]] = [task_resource_plan_list[1] , task_resource_plan_list[2], task_resource_plan_list[3]]
						else:
							task_resource_form_dict[task_resource_plan_list[0]] = [task_resource_plan_list[1] , task_resource_plan_list[2], task_resource_plan_list[3]]

					task_resource_plans = models.TaskResourcePlan.objects.filter(task=task)
					task_resource_lists = [r_plan for r_plan in task_resource_plans]
					task_resource_plan_dict = dict([(r_plan.experience_slab, r_plan.id) for r_plan in task_resource_plans])

					if is_lead_resource_plan_equal:
						print "lead_transactions_list sum", sum(lead_transactions_list)
						if number_of_transactions == sum(lead_transactions_list):						
							for key, val in task_resource_plan_dict.items():
								if key not in task_resource_form_dict:
									task_resource_plan = models.TaskResourcePlan.objects.get(id=task_resource_plan_dict[key])
									task_resource_plan.delete()

							for x, y in task_resource_form_dict.items():
								if x not in task_resource_plan_dict:
									task_resource_plan = models.TaskResourcePlan(
													task = task,
													experience_slab = x,
													number_of_resources = y[0],
													output_count_per_resource = float(format(y[2]/y[0], '.2f'))
												)
									task_resource_plan.save()
								else:
									print "task_resource_plan_dict[x]", task_resource_plan_dict[x]
									get_task_resource_plan = models.TaskResourcePlan.objects.get(id=task_resource_plan_dict[x])
									get_task_resource_plan.experience_slab = x
									get_task_resource_plan.number_of_resources = y[0]
									get_task_resource_plan.output_count_per_resource = float(format(y[2]/y[0], '.2f'))
									get_task_resource_plan.save()
									print "get_task_resource_plan", get_task_resource_plan
						else:
							#custom_error_dict['error'] = "Number of tansactions, Resource plan is not matching,"
							custom_error_dict['error'] = "Number of tansactions of task and number of lead transactions are not matching,"
							error_dict['custom_error_dict'] = custom_error_dict
							return HttpResponseBadRequest(json.dumps(error_dict), content_type="application/json")		
						
						#all_task_resource_dict = {}
						#all_task_resource_plan = models.TaskResourcePlan.objects.filter(task=task)
						#print "all_task_resource_plan", all_task_resource_plan
						#all_task_resource_dict = dict([(task.task_id, task) for task in all_task_resource_plan])
						#return HttpResponse(json.dumps(all_task_resource_dict), content_type='application/json')


				#custom_success_dict['success_msg'] = "Successfully updated lead tasks"
				success_dict['success_msg'] = "Successfully updated lead tasks"
				return HttpResponse(json.dumps(success_dict), content_type="application/json")
			raise Exception("asdf")

		else:
			form_error_dict = {}
			task_formset_error_dict = {}
			for error in form.errors:
				form_error_dict[error] = form.errors[ error]

			#for f1 in task_resource_formset_forms:
			#	if f1:
			#		for error in f1.errors:
			#			e= f1.errors[error]
			#			task_formset_error_dict[error] = unicode(e)
			errors_dict['form_errors'] = form_error_dict
			#errors_dict['formset_errors'] = task_formset_error_dict

			return HttpResponseBadRequest(json.dumps(errors_dict))
	else:
		form = task_form
		task_resource_forms = models.TaskResourcePlan.objects.filter(task=task)
		lead_tasks = [lead_task for lead_task in lead_tasks]
		counter = 0
		if lead_tasks:
			for c, leadtask in enumerate(lead_tasks):
				lead_task_id = leadtask.id
				lead_task_form =form1.LeadTaskForm(request=request, prefix='lead_task_%s' % str(lead_task_id), instance=leadtask)
				print models.LeadTaskResourcePlan.objects.filter(lead_task=leadtask)
				resource_plan_formset = LeadTaskResourceFormset(queryset=models.LeadTaskResourcePlan.objects.filter(lead_task=leadtask),prefix='resource_formset_%s' % str(lead_task_id) )
				lead_task_form_infos.append( (task_id, '%s' %str(lead_task_id), lead_task_form, resource_plan_formset ,))
		#else:
		#	counter = 1 
		#	lead_task_form =form1.LeadTaskForm(prefix='lead_task_new-%s' % str(counter))
		#	resource_plan_formset = LeadTaskResourceFormset(queryset=models.LeadTaskResourcePlan.objects.none(), prefix='resource_formset_new-%s' % str(counter))
		#	lead_task_form_infos.append( (task_id, 'new-%s' %str(counter), lead_task_form, resource_plan_formset ,))
		print "lead_task_form_infos", lead_task_form_infos
	return render(request, 'project/task_add_partial.html', {
													'counter':counter,
													'form': form, 
													'task_resource_forms':task_resource_forms,
													#'task_resource_formset_forms':task_resource_formset_forms,
													'lead_task_form_infos':lead_task_form_infos,
													'is_edit_mode':True,
													'id':task_id
												}
											)
		


		
@login_required
def task_edit_original(request, task_id):

	errors_dict ={}
	lead_task_form_infos=[]
	#task_id='new_task'
	#counter = 1
	# validate input

	task = get_object_or_404(models.Task, id=task_id) 

	lead_tasks = models.LeadTask.objects.filter(task=task)
	form = form1.TaskForm()

	LeadTaskResourceFormset = modelformset_factory(models.LeadTaskResourcePlan, form1.LeadTaskResourceInlineForm, extra=0,)

	task_form = form1.TaskForm(instance=task)

	if request.method == 'POST':
		# lead_task_form_infos=[]
		counter = request.POST.get('add_lead_counter', None)
		print 'counter', counter
		if counter:
			for leadtask in lead_tasks:
				for c in range(1, int(counter)+1):
					lead_task_form =form1.LeadTaskForm(request.POST,instance=leadtask, prefix = 'lead_task_new-%s' % str(c) )

					print models.LeadTaskResourcePlan.objects.filter(lead_task=leadtask)

					lead_task_resource_plan_formset = LeadTaskResourceFormset(request.POST, queryset=models.LeadTaskResourcePlan.objects.filter(lead_task=leadtask),\
						prefix='resource_formset_new-%s' % str(c) )

					lead_task_form_infos.append( (task_id, 'new-%s' % str(c), lead_task_form, lead_task_resource_plan_formset ,))
					
					if lead_task_form.is_valid() and lead_task_resource_plan_formset.is_valid():
						pass
					else:
						lead_task_form_errors = {}
						lead_resource_plan_formset_errors = {}
						
						for lead_task_form in lead_task_form_infos:
							for error in lead_task_form[2].errors:
								lead_task_form_errors[error] = lead_task_form[2].errors[error]
						try:
							for lead_task_resource_formset in lead_task_form_infos:
								for f1 in lead_task_resource_formset[3]:
									for error in f1.errors:
										e = f1.errors[error]
										lead_resource_plan_formset_errors[error] = unicode(e)
						except ValidationError:
							pass
						errors_dict['lead_task_form_errors'] = lead_task_form_errors
						errors_dict['lead_resource_plan_formset_errors'] = lead_resource_plan_formset_errors
					
		form = form1.TaskForm(request.POST or None, instance=task)

		if form.is_valid():
			with transaction.atomic():
				task = form.save(commit=False)
				number_of_transactions = form.cleaned_data.get('no_of_txs')
				#task.save()

				print "---------------------"
				print lead_task_form_infos
				total_resource_plan_list = []
				task_resource_form_lists = []
				task_resource_form_dict ={}
				form_wise_resource_dict = {}
				form_wise_resource_list = []
				lead_transactions_plan_equal = False
				is_lead_resource_plan_equal = False
				custom_error_dict = {}
				if counter:
					for i, form_info in enumerate(lead_task_form_infos):
						print "form infos",form_info
						lead_task_form = form_info[2]
						resource_plan_formset = form_info[3]

						if lead_task_form.is_valid() and resource_plan_formset.is_valid():
							lead_task_instance = lead_task_form.save(commit=False)
							#lead_task_instance.task = task
							lead_form_transactions = lead_task_form.cleaned_data.get('no_of_txs')
							
							for resource_plan_form in resource_plan_formset:
								resource_plan_form_instance = resource_plan_form.save(commit=False)
								#resource_plan_form_instance.lead_task = lead_task_instance
								experience_slab = resource_plan_form.cleaned_data.get('experience_slab', None)
								number_of_resource = resource_plan_form.cleaned_data.get('number_of_resources', None)
								output_count_per_resource = resource_plan_form.cleaned_data.get('output_count_per_resource', None)

								print "++++++++++++++++++"
								if number_of_resource and output_count_per_resource not in ['', None]:
									resource_target_per_plan = number_of_resource * output_count_per_resource
									form_wise_resource_list.append(resource_target_per_plan)

									total_resource_plan_list.append(resource_target_per_plan)
									print "printing total_resource_plan_list", total_resource_plan_list
									exp_slab = ExperienceSlab.objects.get(title=experience_slab)

									task_resource_form_lists.append([exp_slab, number_of_resource, output_count_per_resource, resource_target_per_plan])
									#print "printing task_resource_form_lists at saving", task_resource_form_lists
							
							form_wise_resource_dict[i] = sum(form_wise_resource_list)
							if form_wise_resource_list:
								print "lead_form_transactions",lead_form_transactions
								print "form_wise_resource_list per lead", sum(form_wise_resource_list)
								print "form_wise_resource_dict", form_wise_resource_dict

								if lead_form_transactions == sum(form_wise_resource_list):
									is_lead_resource_plan_equal = True
									print "is_lead_resource_plan_equal", is_lead_resource_plan_equal
									form_wise_resource_list[:] = []
									print "form_wise_resource_list", form_wise_resource_list

									task.save()
									lead_task_instance.task = task
									lead_task_instance.save()
									for resource_plan_form in resource_plan_formset:
										resource_plan_form_instance = resource_plan_form.save(commit=False)
										resource_plan_form_instance.lead_task = lead_task_instance
										resource_plan_form_instance.save()

										print resource_plan_form_instance
								else:
									custom_error_dict['lead_resource_plan_not_equal'] = "Lead resource plan is not equal to numbber of transaction"
						
									return HttpResponse(json.dumps(custom_error_dict), content_type="application/json")							

						else:
							lead_task_form_errors = {}
							lead_resource_plan_formset_errors = {}
							
							for error in form_info[2].errors:
									lead_task_form_errors[error] = form_info[2].errors[error]
							try:
								for f1 in form_info[3]:
									for error in f1.errors:
										e = f1.errors[error]
										lead_resource_plan_formset_errors[error] = unicode(e)
								errors_dict['lead_task_form_errors'] = lead_task_form_errors
								errors_dict['lead_resource_plan_formset_errors'] = lead_resource_plan_formset_errors
							except ValidationError:
								pass
					
					print "total_resource_plan_list per lead", sum(total_resource_plan_list)
					print "number_of_transactions", number_of_transactions


					for i, task_resource_plan_list in enumerate(task_resource_form_lists):
						#print "task_resource_plan_list[0]", task_resource_plan_list[0]
						if task_resource_form_dict:
							print "task_resource_form_dict start", task_resource_form_dict
							if task_resource_plan_list[0] in task_resource_form_dict:
								no_of_total_resource = task_resource_form_dict[task_resource_plan_list[0]][0] + task_resource_plan_list[1]
								total_resource_target =  task_resource_form_dict[task_resource_plan_list[0]][1] + task_resource_plan_list[2]

								resource_mul_target =  task_resource_form_dict[task_resource_plan_list[0]][2] + task_resource_plan_list[3]
								avg_target_per_resource = float(format(resource_mul_target/no_of_total_resource, '.2f'))
								#print "avg_target_per_resource", avg_target_per_resource								
								task_resource_form_dict[task_resource_plan_list[0]] = [no_of_total_resource,  total_resource_target, avg_target_per_resource]
							else:
								task_resource_form_dict[task_resource_plan_list[0]] = [task_resource_plan_list[1] , task_resource_plan_list[2], task_resource_plan_list[3]]
						else:
							task_resource_form_dict[task_resource_plan_list[0]] = [task_resource_plan_list[1] , task_resource_plan_list[2], task_resource_plan_list[3]]

					print "task_resource_form_dict on complete", task_resource_form_dict	
					task_resource_plans = models.TaskResourcePlan.objects.filter(task=task)
					task_resource_plan_dict = dict([(r_plan.experience_slab,r_plan.id) for r_plan in task_resource_plans])


					print "task_resource_plan_dict", task_resource_plan_dict
					if is_lead_resource_plan_equal:
						if task_resource_plan_list:
							for task_resource_plan in task_resource_plans:
								for key, val in task_resource_form_dict.items():
									if key in task_resource_plan_dict:
										print "value at saving", val
										task_resource_plan.experience_slab = key
										task_resource_plan.number_of_resources = val[0]
										task_resource_plan.output_count_per_resource = val[2]
										task_resource_plan.save()
									else:
										task_resource_plan.experience_slab = key
										task_resource_plan.number_of_resources = val[0]
										task_resource_plan.output_count_per_resource = val[2]
										task_resource_plan.save()

						else:
							for key, val in task_resource_form_dict.items():
								print "value at saving", val
								task_resource_plan.experience_slab = key
								task_resource_plan.output_count_per_resource = val[2]
								task_resource_plan = models.TaskResourcePlan(
														task = task,
														experience_slab = key,
														number_of_resources = val[0],
														output_count_per_resource = val[2]
								)
								task_resource_plan.save()

						raise Exception("asdf")
					else:
						custom_error_dict['transactions_plan_not_equal'] = "Number of tansactions, Resource plan is not matching,"
						return HttpResponse(json.dumps(custom_error_dict), content_type="application/json")	

			return HttpResponse("successfully updated task")
		else:
			form_error_dict = {}
			task_formset_error_dict = {}
			for error in form.errors:
				form_error_dict[error] = form.errors[ error]

			#for f1 in task_resource_formset_forms:
			#	if f1:
			#		for error in f1.errors:
			#			e= f1.errors[error]
			#			task_formset_error_dict[error] = unicode(e)
			errors_dict['form_errors'] = form_error_dict
			#errors_dict['formset_errors'] = task_formset_error_dict

			return HttpResponseBadRequest(json.dumps(errors_dict))
	else:
		form = task_form
		#task_resource_formset_forms = task_resource_formset_forms
		task_resource_forms = models.TaskResourcePlan.objects.filter(task=task)
		print "task_resource_forms", task_resource_forms
		counter = len(lead_tasks)
		print "-------------------------------------"
		lead_tasks = [lead_task for lead_task in lead_tasks]
		print "lead_tasks", lead_tasks
		print "counter", counter

		if counter:
			for c, leadtask in enumerate(lead_tasks):
				lead_task_form =form1.LeadTaskForm(prefix='lead_task_new-%s' % str(c+1), instance=leadtask)
				print models.LeadTaskResourcePlan.objects.filter(lead_task=leadtask)
				resource_plan_formset = LeadTaskResourceFormset(queryset=models.LeadTaskResourcePlan.objects.filter(lead_task=leadtask),prefix='resource_formset_new-%s' % str(c+1) )
				lead_task_form_infos.append( (task_id, 'new-%s' %str(c+1), lead_task_form, resource_plan_formset ,))
		else:
			counter = 1 
			lead_task_form =form1.LeadTaskForm(prefix='lead_task_new-%s' % str(counter))
			resource_plan_formset = LeadTaskResourceFormset(queryset=models.LeadTaskResourcePlan.objects.none(), prefix='resource_formset_new-%s' % str(counter))
			lead_task_form_infos.append( (task_id, 'new-%s' %str(counter), lead_task_form, resource_plan_formset ,))
		print "lead_task_form_infos", lead_task_form_infos
	return render(request, 'project/task_add_partial.html', {
													'counter':counter,
													'form': form, 
													'task_resource_forms':task_resource_forms,
													#'task_resource_formset_forms':task_resource_formset_forms,
													'lead_task_form_infos':lead_task_form_infos,
													'is_edit_mode':True,
													'id':task_id
												}
											)


@login_required
def lead_task_hist(request):
	if request.user.groups.filter(name='lead').exists():
		lead_tasks = models.LeadTask.objects.filter(lead__user__username=request.user,status__in=['completed','rejected'])[:10]

	elif request.user.groups.filter(name='operations manager').exists():
		ops_empl=Employee.objects.get(user__username=request.user)
		ops_leads=ops_empl.get_children()
		leads=[lead for lead in ops_leads]
		lead_tasks = models.LeadTask.objects.filter(lead__name__in=leads)

	return render(request, 'project/lead_task_hist_list_partial.html', 
					{'lead_tasks': lead_tasks}
				)


def lead_task_hist_list(request):
	try:
		ops_empl=Employee.objects.get(user__username=request.user)

	except Employee.DoesNotExist:
		pass
	if request.user.groups.filter(name='lead').exists():
		f = custom_filters.LeadTaskFilter(request.GET, queryset=models.LeadTask.objects.filter(lead__user__username=request.user,status__in=['completed','rejected']))
	
	elif request.user.groups.filter(name='operations manager').exists():
		ops_empl=Employee.objects.get(user__username=request.user)
		ops_leads=ops_empl.get_children()
		leads=[lead for lead in ops_leads]
		f = custom_filters.LeadTaskFilter(request.GET, queryset=models.LeadTask.objects.filter(lead__name__in=leads,status__in=['completed']))

	return render(request, 'project/lead_task_hist_list_partial.html', {'filter': f})


@login_required
def lead_task_list(request):

	try:
		ops_empl=Employee.objects.get(user__username=request.user)

	except Employee.DoesNotExist:
		pass

	if request.user.groups.filter(name='lead').exists():
		lead_tasks = models.LeadTask.objects.filter(lead__user__username=request.user,status__in=['new','pending'])
		#lead_tasks_in_ascending_order = reversed(lead_tasks)

	elif request.user.groups.filter(name='lead').exists():
			ops_leads=ops_empl.get_children()
			leads=[lead for lead in ops_leads]
			lead_tasks = models.LeadTask.objects.filter(lead__name__in=leads,status__in=['new','pending'])
		#lead_tasks_in_ascending_order = reversed(lead_tasks)
	elif request.user.groups.filter(name='operations manager').exists():
#		ops_empl=Employee.objects.get(user__username=request.user)
		ops_leads=ops_empl.get_children()
		leads=[lead for lead in ops_leads]
		lead_tasks = models.LeadTask.objects.filter(lead__name__in=leads,status__in=['new','pending'])


	return render(request, 'project/lead_task_list_partial.html', 
					{'lead_tasks': lead_tasks}
				)


@login_required
def lead_task_add(request):
	success_dict={}
	LeadTaskResourceFormset = formset_factory(form1.LeadTaskResourceInlineForm, extra=1)
	StaffTaskFormset = formset_factory(form1.StaffTaskInlineForm, extra=1, )

	if request.method == 'POST':
		form = form1.LeadTaskForm(request.POST, None)
		lead_task_resource_formset_forms = LeadTaskResourceFormset(request.POST or None)
		staff_task_formset_forms = StaffTaskFormset(request.POST or None)

		for lead_task_resource_form in lead_task_resource_formset_forms.deleted_forms:
			lead_task_resource_form_instance = lead_task_resource_form.instance
			if lead_task_resource_form_instance.pk:
				lead_task_resource_form_instance.delete
		for staff_task_form in staff_task_formset_forms.deleted_forms:
			staff_task_form_instance = staff_task_form.instance
			if staff_task_form_instance.pk:
				staff_task_form_instance.delete

		if form.is_valid() and lead_task_resource_formset_forms.is_valid() and staff_task_formset_forms.is_valid():
			lead_task = form.save(commit=False)
			lead_task.save()

			for lead_task_resource_form in lead_task_resource_formset_forms:
				lead_task_resource_form_instance = lead_task_resource_form.save(commit=False)
				lead_task_resource_form_instance.lead_task = lead_task
				lead_task_resource_form_instance.save()

			for staff_task_form in staff_task_formset_forms:
				staff_task_form_instance = staff_task_form.save(commit=False)
				staff_task_form_instance.lead_task = lead_task
				staff_task_form_instance.save()

			
		else:
			error_dict = {}
			form_error_dict = {}
			lead_task_resource_formset_error_dict = {}
			staff_task_formset_error_dict = {}

			for error in form.errors:
				form_error_dict[error] = form.errors[ error]

			for f1 in lead_task_formset_forms:
				if f1:
					for error in f1.errors:
						e = f1.errors[error]
						lead_task_formset_error_dict[error] = unicode(e)

			for f1 in staff_task_formset_forms:
				if f1:
					for error in f1.errors:
						e = f1.errors[error]
						staff_task_formset_error_dict[error] = unicode(e)

			error_dict['form_errors'] = form_error_dict
			error_dict['lead_task_formset_error_dict'] = lead_task_formset_error_dict
			error_dict['staff_task_formset_error_dict'] = staff_task_formset_error_dict
			return HttpResponseBadRequest(json.dumps(error_dict))
		success_dict['success_msg'] = "Successfully Created Lead"
		return HttpResponse(json.dumps(success_dict), content_type='application/json')
	else:
		form = form1.LeadTaskForm()
		lead_task_resource_formset_forms = LeadTaskResourceFormset()
		staff_task_formset_forms = StaffTaskFormset()
		return render(request, 'project/lead_task_add_partial.html', {
										'form':form,
										'lead_task_resource_formset_forms':lead_task_resource_formset_forms,
										'staff_task_formset_forms':staff_task_formset_forms
									}
								)



@login_required
def lead_task_edit(request, id):
	success_dict={}
	error_dict = {}
	exception_error_dict = {}
	lead_task = get_object_or_404(models.LeadTask, id=id)
	
		#lead_t = 
	get_task = lead_task.task
	print "get_task", get_task
	
	lead_task_resources = models.LeadTaskResourcePlan.objects.filter(lead_task=lead_task)
	#LeadTaskResourceFormset = modelformset_factory(models.LeadTaskResourcePlan, form1.LeadTaskResourceInlineForm, extra=1)
	StaffTaskFormset = modelformset_factory(models.StaffTask, form1.StaffTaskInlineForm, extra=1, exclude=('lead_task', ))

	#lead_task_resource_formset_forms = LeadTaskResourceFormset(queryset=models.LeadTaskResourcePlan.objects.filter(lead_task=lead_task), prefix='lead_task_resource')
	staff_task_formset_forms = StaffTaskFormset(queryset = models.StaffTask.objects.filter(lead_task=lead_task), prefix='staff_task_form', form_kwargs={'request': request})

	if request.method == "POST":

		#form = form1.LeadTaskForm(request.POST, instance=lead_task)
		#lead_task_resource_formset_forms = LeadTaskResourceFormset(request.POST or None, \
			#		queryset=models.LeadTaskResourcePlan.objects.filter(lead_task=lead_task), prefix='lead_task_resource')
		staff_task_formset_forms = StaffTaskFormset(request.POST or None, \
					queryset = models.StaffTask.objects.filter(lead_task=lead_task), prefix='staff_task_form', form_kwargs={'request': request})


		#for lead_task_resource_form in lead_task_resource_formset_forms.deleted_forms:
		#	lead_task_resource_form_instance = lead_task_resource_form.instance
		#	if lead_task_resource_form_instance.pk:
		#		lead_task_resource_form_instance.delete

		for staff_task_form in staff_task_formset_forms.deleted_forms:
			staff_task_form_instance = staff_task_form.instance
			if staff_task_form_instance.pk:
				staff_task_form_instance.delete

		staff_task_resource_list = []
		staff_transactions_list = []
		emp_staff_list = []

		qc_required_tasks_list = []
		if staff_task_formset_forms.is_valid():
			
			for staff_task_form in staff_task_formset_forms:
				staff_task_form_instance = staff_task_form.save(commit=False)
				staff_task_form_instance.lead_task = lead_task
				staff = staff_task_form.cleaned_data.get('staff')

				file_name = staff_task_form.cleaned_data.get('filename')
				number_of_transaction = staff_task_form.cleaned_data.get('no_of_txs', None)
				is_qc_required = staff_task_form.cleaned_data.get('is_qc_required')

				#qc_required_tasks_list.append([file_name, is_qc_required])
				if number_of_transaction not in ['0', None, '']:
					staff_transactions_list.append(number_of_transaction)

				if staff and number_of_transaction not in ['', None]:
					emp_staff_list.append([staff, number_of_transaction])

		else:
			staff_task_formset_error_dict = {}
			for f1 in staff_task_formset_forms:
				if f1:
					for error in f1.errors:
						e = f1.errors[error]
						staff_task_formset_error_dict[error] = unicode(e)
			error_dict['staff_task_formset_error_dict'] = staff_task_formset_error_dict
			return HttpResponseBadRequest(json.dumps(error_dict))
		

		staff_resource_tran_dict = {}
		if emp_staff_list:
			print "emp_staff_list", emp_staff_list
			for i, emp in enumerate(emp_staff_list):
				try:
					employee_staff_assignment = models.EmployeeAssignment.objects.get(employee=emp[0])
					employee_staff_experience = ExperienceSlab.objects.get(title=employee_staff_assignment.experience_slab)
					print 'employee_staff_experience', employee_staff_experience

					if staff_resource_tran_dict:
						print "staff_resource_tran_dict", staff_resource_tran_dict
						if employee_staff_experience in staff_resource_tran_dict:
							count += 1 
							staff_resource_tran_dict[employee_staff_experience] = [count, emp[0], emp[1]] 	
						else:
							count = 1
							staff_resource_tran_dict[employee_staff_experience] = [count, emp[0], emp[1]]
					else:
						count = 1
						staff_resource_tran_dict[employee_staff_experience] = [count, emp[0], emp[1]]
				except models.EmployeeAssignment.DoesNotExist:
					exception_error_dict['emp_exp_not_exit'] = "Employee experience does not exit"
					return HttpResponseBadRequest(json.dumps(exception_error_dict))
		else:
			msg = "Please assign the tasks to agents"
			exception_error_dict['transaction_not_matching'] = msg
			error_dict['exception_error_dict'] = exception_error_dict
			return HttpResponseBadRequest(json.dumps(error_dict), content_type='application/json')

		print "staff_resource_tran_dict", staff_resource_tran_dict
		lead_task_resource_dict = dict([(lead_task_resource.experience_slab, lead_task_resource.number_of_resources) for lead_task_resource in lead_task_resources])
		print "lead_task_resource_dict",lead_task_resource_dict

		for key, val in staff_resource_tran_dict.items():
			if key in lead_task_resource_dict:
				if lead_task_resource_dict[key] == val[0]:
					print "resource plan is matching"
					lead_transactions = lead_task.no_of_txs
					staff_transations_total = sum(staff_transactions_list)

					if lead_transactions == staff_transations_total:
						try:
							for staff_task_form in staff_task_formset_forms:
								staff_task_form_instance = staff_task_form.save(commit=False)
								staff_task_form_instance.lead_task = lead_task
								#if staff not in ['', None]:
								staff_task_form_instance.save()
						except IntegrityError:
							pass
						#return HttpResponse('ok ')
					else:
						msg = "Total number of resource transactions are not matching with lead transactions"
						exception_error_dict['transaction_not_matching'] = msg
						error_dict['exception_error_dict'] = exception_error_dict
						return HttpResponseBadRequest(json.dumps(error_dict), content_type='application/json')

				elif lead_task_resource_dict[key] > val[0]:
					msg = "Number of resource usage less than matching experience "
					exception_error_dict['transaction_not_matching'] = msg
					error_dict['exception_error_dict'] = exception_error_dict
					return HttpResponseBadRequest(json.dumps(error_dict), content_type='application/json')

				elif lead_task_resource_dict[key] < val[0]:
					msg = "Number of resource usage more than matching experience "
					exception_error_dict['transaction_not_matching'] = msg
					error_dict['exception_error_dict'] = exception_error_dict
					return HttpResponseBadRequest(json.dumps(error_dict), content_type='application/json')

				else:
					#print "number of resource and planing not matching"
					msg = "Number of staffs exp and target are not matching with Lead resource planing experience and transactions"
					exception_error_dict['transaction_not_matching'] = msg
					error_dict['exception_error_dict'] = exception_error_dict
					return HttpResponseBadRequest(json.dumps(error_dict), content_type='application/json')
			else:
				msg = "Selected employee experience should match as per resource planing experience slab"
				exception_error_dict['transaction_not_matching'] = msg
				error_dict['exception_error_dict'] = exception_error_dict
				return HttpResponseBadRequest(json.dumps(error_dict), content_type='application/json')

		success_dict['success_msg'] = "Successfully updated staff tasks"
		return HttpResponse(json.dumps(success_dict), content_type='application/json')
	

	else:
		
		staff_task_formset_forms = staff_task_formset_forms
		return render(request, 'project/lead_task_add_partial.html', {
									'task':get_task,
									'lead_task':lead_task,
									'lead_task_resources':lead_task_resources,
									'staff_task_formset_forms':staff_task_formset_forms,    
									'is_edit_mode':True,
									'id':id
								}
							)


@login_required
def task_template_list(request):

	task_templates = models.TaskTemplate.objects.all()
	return render(request, 'project/task_template_list_partial.html', 
					{'task_templates': task_templates}
				)


@login_required
def task_template_add(request):

	if request.method == 'POST':
		form = form1.TaskTemplateForm(request.POST, None)

		if form.is_valid():
			task_template = form.save(commit=False)
			task_template.save()

			return HttpResponse('OK')
		else:
			error_dict = {}
			for error in form.errors:
				error_dict[error] = form.errors[ error]
			return HttpResponseBadRequest(json.dumps(error_dict))
	else:
		form = form1.TaskTemplateForm()

		return render(request, 'project/task_template_add_partial.html', {'form':form})


@login_required
def task_template_edit(request, id):
	task_template = get_object_or_404(models.TaskTemplate, id=id)
	if request.method == "POST":
		form = form1.TaskTemplateForm(request.POST, instance=task_template)
		if form.is_valid():
			task_template = form.save(commit=False)
			task_template.save()
			return HttpResponse('ok ')
		else:
			error_dict={}
			for error in form.errors:
				error_dict[error] = form.errors[error]
				
			return HttpResponseBadRequest(json.dumps(error_dict))
	else:
		form = form1.TaskTemplateForm(instance=task_template)

	return render(request, 'project/task_template_add_partial.html', {'form': form, 'is_edit_mode':True, 'id':id})

@login_required
def staff_task_hist(request):

	try:
		employee = Employee.objects.get(user__username=request.user)
	except Employee.DoesNotExist:
		pass

	if request.user.groups.filter(name='agent').exists():
		staff_tasks = models.StaffTask.objects.filter(staff__user__username=request.user,status__in=['completed','rejected'])[:10]
		
	if request.user.groups.filter(name='lead').exists():
#		lead_employee = Employee.objects.get(user__username=request.user)
		lead_agents = employee.get_children()
		print "lead_agents", lead_agents
		staffs = [staff for staff in lead_agents]
		print "staffs", staffs

		staff_tasks = models.StaffTask.objects.filter(staff__name__in=staffs,status__in=['completed','cancelled'])[:10]
	

	elif request.user.groups.filter(name='operations manager').exists():
		operations_agents = operations_employee.get_children()
		print "operations_agents", operations_agents
		staffs = [staff for staff in operations_agents]
		print "staffs", staffs

		staff_tasks = models.StaffTask.objects.filter(staff__name__in=staffs,status__in=['completed','cancelled'])

	return render(request, 'project/staff_task_hist_list_partial.html', 
					locals()
					)


@login_required
def staff_task_hist_list(request):
	
	try:
		ops_employee = Employee.objects.get(user__username=request.user)
	except Employee.DoesNotExist:
		pass
	if request.user.groups.filter(name='agent').exists():
		f = custom_filters.StaffTaskFilter(request.GET, queryset=models.StaffTask.objects.filter(staff__user__username=request.user,status__in=['completed']))
	
	elif request.user.groups.filter(name='lead').exists():

		f = custom_filters.StaffTaskFilter(request.GET, queryset=models.StaffTask.objects.filter(lead_task__lead__user__username=request.user,status__in=['completed']))

	elif request.user.groups.filter(name='operations manager').exists():
		operation_employee = Employee.objects.get(user__username=request.user)
		operation_agents = ops_employee.get_descendants()
		operation_staffs = [staff for staff in operation_agents]
		f = custom_filters.StaffTaskFilter(request.GET, queryset=models.StaffTask.objects.filter(staff__name__in=operation_staffs,status__in=['completed']))

	return render(request, 'project/staff_task_hist_list_partial.html', {'filter': f})

@login_required
def staff_task_history(request):
	task_done_dict = {}
	task_pending_dict = {}

	if request.user.groups.filter(name=['operations manager','lead']).exists():
		related_staff_tasks_completed = models.StaffTask.objects.filter(Q(status='completed'), lead_task=get_lead_task_id).select_related('lead_task')
		print "all_related_staff_tasks", related_staff_tasks_completed

		counter = 0

		if related_staff_tasks_completed == completed:
			counter += 1

		else:
			counter_started = False
			counter_ended =False
			for staff_task_status in enumerate(staff_task_status):
				print "yyyyyyyyyyyyyyyyyyyyy",staff_task_status
				if staff_task_status == completed :
					counter_started=True
					counter1 += 1
				elif counter_started and staff_task_status != completed :
					counter_started = True
					counter2 += 1
					
			no_of_tasks_done = counter1  
			task_done_dict['no_of_tasks_done'] = counter1
			return HttpResponse(json.dumps(task_done_dict), content_type='application/json')

			no_of_tasks_pendind = counter2
			task_pending_dict['no_of_tasks_pending'] = counter2
			return HttpResponse(json.dumps(task_pending_dict), content_type='application/json')


			# elif request.POST.has_key('complete'):
			# 	if staff_task_get.is_workedon:
			# 		staff_task_get.is_workedon = False
			# 		complete = request.POST.get('complete')
			# 		print "complete", complete

# @login_required
# def staff_task_history(request):

#     IDnumber = int(request.args.get('ID'))

#     with db:
#         cur = db.cursor()
#         cur.execute("SELECT AnimalID, AdoptionProbability FROM Demo_Data WHERE AnimalID = '" + str(IDnumber) + "' LIMIT 1")
#         query_results = cur.fetchall()

#     thePercent= str(int(query_results[0][1])) 
#     theDog = "static/PetPics/" + str(int(query_results[0][0]))
#     print thePercent

#     return render_template("predictions.html", thePercent=thePercent, theDog = theDog)



@login_required
def staff_task_list(request):
	

	if request.user.groups.filter(name__in=['agent','qc']).exists():
		staff_tasks = models.StaffTask.objects.filter(staff__user__username=request.user,status__in=['new','pending', 'rejected']).order_by('-priority')

	elif request.user.groups.filter(name='operations manager').exists():

		ops_empl = Employee.objects.get(user__username=request.user)
		ops_leads = ops_empl.get_descendants()
		staffs = [staff for staff in ops_leads]
		staff_tasks = models.StaffTask.objects.filter(staff__name__in=staffs,status__in=['new','pending', 'rejected'])
	
		
	elif request.user.groups.filter(name='lead').exists():
		lead_employee = Employee.objects.get(user__username=request.user)
		print "lead_employee", lead_employee
		lead_agents = lead_employee.get_children()
		staffs  =  [staff for staff in lead_agents]
		staff_tasks = models.StaffTask.objects.filter(staff__name__in=staffs,status__in=['new','pending', 'qc', 'rejected'])

	#elif request.user.groups.filter(name='operations manager').exists():
		#staff_tasks = models.StaffTask.objects.filter(created_by=request.user).order_by('created')
	
		
	return render(request, 'project/staff_task_list_partial.html', 
					locals()
				)

@login_required
def tasks_assigned_to_lead(request):

	if request.user.groups.filter(name='lead').exists():
		lead_employee = Employee.objects.get(user__username=request.user)
		print "lead_employee", lead_employee
		lead_agents = lead_employee.get_children()
		staffs  =  [staff for staff in lead_agents]
		staff_tasks = models.StaffTask.objects.filter(staff__name=lead_employee,status__in=['new','pending', 'qc', 'rejected'])
		
	return render(request, 'project/tasks_assigned_to_lead_partial.html', 
					locals()
				)


@login_required
def staff_experience(request):
	staff_exp_dict = {}
	if request.method == 'POST' and request.is_ajax():

		staff = request.POST.get('staff')

		if staff not in ['', None]:
			emp_staff = Employee.objects.get(id=staff)
			print "emp_staff", emp_staff
			if emp_staff:
				try:
					emp_exp = models.EmployeeAssignment.objects.get(employee=emp_staff)
					if emp_exp:
						employee_experience = ExperienceSlab.objects.get(title=emp_exp.experience_slab)
						print "employee_experience", employee_experience
						staff_exp_dict['emp_exp'] = str(employee_experience)
				except models.EmployeeAssignment.DoesNotExist:
					staff_exp_dict['emp_not_exist'] = "Employee experience does not exist"
					pass
		else:
			staff_exp_dict['emp_exp'] = ''

	return HttpResponse(json.dumps(staff_exp_dict), content_type='application/json')


@login_required
def staff_task_add(request):
	success_dict={}
	if request.method == 'POST':
		form = form1.StaffTaskForm(request.POST, None)

		if form.is_valid():
			staff_task = form.save(commit=False)
			staff_task.save()
		else:
			error_dict = {}
			for error in form.errors:
				error_dict[error] = form.errors[ error]
			return HttpResponseBadRequest(json.dumps(error_dict))
		success_dict['success_msg'] = "Successfully Edited Lead"
		return HttpResponse(json.dumps(success_dict), content_type='application/json')
	else:
		form = form1.StaffTaskForm()

		return render(request, 'project/staff_task_add_partial.html', {'form':form})


def time_diff(start, end):

	fmt = '%Y-%m-%d %H:%M:%S.%f'
	#d1 = datetime.strptime('2010-01-01 17:31:22', fmt)
	#d2 = datetime.strptime('2010-01-03 20:15:14', fmt)
	
	d1 = datetime.strptime(start, fmt)
	d2 = datetime.strptime(end, fmt)
	# convert to unix timestamp
	d1_ts = time.mktime(d1.timetuple())
	d2_ts = time.mktime(d2.timetuple())

	seconds = d2_ts-d1_ts
	print "total_time_in_sec", seconds

	# they are now in seconds, subtract and then divide by 60 to get minutes.
	hours = seconds // (60*60)
	seconds %= (60*60)
	minutes = seconds // 60
	seconds %= 60
	return "%02i:%02i:%02i" % (hours, minutes, seconds)


def time_sum(timeList):
	import datetime
	sum = datetime.timedelta()
	for i in timeList:
		(h, m, s) = i.split(':')
		d = datetime.timedelta(hours=int(h), minutes=int(m), seconds=int(s))
		sum += d
	print(str(sum))

	return str(sum)



def qc_task_status(request):
	time_in_min_dict = {}
	task_time_dict = {}
	task_idle_time_dict = {}
	task_time_list = []
	task_time_history_list = []
	all_time_history_lists = []
	if request.method == "POST" and request.is_ajax():

		staff_task_get = get_object_or_404(models.StaffTask, id=request.POST.get('s_task_id'))
		status = staff_task_get.status

		if status == 'qc' or staff_task_get.qc_status == 'new':
			if request.POST.has_key('start'):
				if not staff_task_get.is_workedon:
					staff_task_get.is_workedon = True
					start = request.POST.get('start')
					task_start_time = datetime.now()
					if staff_task_get.qc_time_history not in ['', None] :
						pause_time_history_list = []
						task_time_history_list = json.loads(staff_task_get.qc_time_history)
	 
						if task_time_history_list[0]['idle_time'] not in ['', None, 0]:
							pause_time_list = []
							time_sum_list = []
							if task_time_history_list[0]['all_time_history']:
								pause_time_list = task_time_history_list[0]['all_time_history'][-1]
								pause_time_history_list = pause_time_list[0].split('--')
								if pause_time_history_list[0] == 'pause':
									time_sum_list.append(task_time_history_list[0]['idle_time'])
									idle_time_diff = time_diff(str(pause_time_list[1]), str(task_start_time))
									time_sum_list.append(idle_time_diff)
									task_time_history_list[0]['idle_time'] =  time_sum(time_sum_list)

						else:
							pause_time_list = []
							if task_time_history_list[0]['all_time_history']:
								pause_time_list = task_time_history_list[0]['all_time_history'][-1]
								pause_time_history_list = pause_time_list[0].split('--')
								if pause_time_history_list[0] == 'pause':
									idle_time_diff = time_diff(str(pause_time_list[1]),str(task_start_time))
									task_time_history_list[0]['idle_time'] = idle_time_diff

						task_time_history_list[0]['all_time_history'].append([start, str(task_start_time)])
						task_idle_time_dict['idle_time_min'] = task_time_history_list[0]['idle_time']
						staff_task_get.qc_time_history = json.dumps(task_time_history_list)
						staff_task_get.save()
	 
					else:
						task_time_list.append([start, str(task_start_time)])
						all_time_history_lists = [{'all_time_history':task_time_list, 'time_diff':None, 'idle_time':None} ]
						staff_task_get.qc_time_history = json.dumps(all_time_history_lists)
						staff_task_get.save()
	 
					return HttpResponse(json.dumps(task_idle_time_dict), content_type='application/json')
				else:
					task_error_dict = {}
					task_error_dict['error'] = "Your already working on other task"
					return HttpResponseBadRequest(json.dumps(task_error_dict), content_type='application/json')

			elif request.POST.has_key('status'):
				if staff_task_get.is_workedon:
					staff_task_get.is_workedon = False

					pause = request.POST.get('status')
					pause_option = request.POST.get('options')
					get_time_history = staff_task_get.qc_time_history
					
					if not pause_option in ['rejected', 'cancelled']:
						task_pause_time = datetime.now()

						if staff_task_get.qc_time_history not in ['', None]:
							task_time_history_list = json.loads(staff_task_get.qc_time_history)

							if task_time_history_list[0]['time_diff'] not in ['', None, 0]:
								start_time_hist = []
								time_sum_list = []
								if task_time_history_list[0]['all_time_history']:
									start_time_hist = task_time_history_list[0]['all_time_history'][-1]
									print "latest start_time_hist", start_time_hist
									if start_time_hist[0] == 'start':
										time_sum_list.append(task_time_history_list[0]['time_diff'])
										get_time_diff = time_diff(str(start_time_hist[1]), str(task_pause_time))
										time_sum_list.append(get_time_diff)
										task_time_history_list[0]['time_diff'] =  time_sum(time_sum_list)
							else:
								start_time_hist = []
								if task_time_history_list[0]['all_time_history']:
									start_time_hist = task_time_history_list[0]['all_time_history'][-1]
									print "latest start_time_hist", start_time_hist
									if start_time_hist[0] == 'start':
										get_time_diff = time_diff(str(start_time_hist[1]), str(task_pause_time))
										task_time_history_list[0]['time_diff'] = get_time_diff
						
							task_time_history_list[0]['all_time_history'].append(['%s--%s' %(pause,pause_option), str(task_pause_time)])
							staff_task_get.qc_time_history = json.dumps(task_time_history_list)
							staff_task_get.qc_time_in_min = task_time_history_list[0]['time_diff']
							staff_task_get.save()
					else:
						if pause_option == 'rejected':
							staff_task_get.qc_status = 'rejected'
							staff_task_get.status = 'rejected'
							staff_task_get.save()
						elif pause_option == 'cancelled':
							staff_task_get.qc_status = 'cancelled'
							#staff_task_get.status = 'cancelled'
							staff_task_get.save()
						else:
						#elif pause_option == 'cancelled':
						#	staff_task_get.status = 'rejected'
						#else:
							pass

					print "returning time", task_time_history_list[0]['time_diff']
					task_time_dict['time_in_min'] = task_time_history_list[0]['time_diff']

					return HttpResponse(json.dumps(task_time_dict), content_type='application/json')

			elif request.POST.has_key('complete'):
				if staff_task_get.is_workedon:
					staff_task_get.is_workedon = False

					complete = request.POST.get('complete')

					task_complete_time = datetime.now()
					qc_required = staff_task_get.is_qc_required
					
					if staff_task_get.qc_time_history not in ['', None]:
						task_time_history_list = json.loads(staff_task_get.qc_time_history)

						if task_time_history_list[0]['time_diff'] not in ['', None]:
							start_time_hist = []
							if task_time_history_list[0]['all_time_history']:
								start_time_hist = task_time_history_list[0]['all_time_history'][-1]
								if start_time_hist[0] == 'start':
									get_time_diff = time_diff(str(start_time_hist[1]), str(task_complete_time))
									print "get_time_diff", get_time_diff

									task_time_history_list[0]['time_diff'] = task_time_history_list[0]['time_diff'] + get_time_diff
						else:
							start_time_hist = []
							if task_time_history_list[0]['all_time_history']:
								start_time_hist = task_time_history_list[0]['all_time_history'][-1]
								print "latest start_time_hist", start_time_hist
								if start_time_hist[0] == 'start':
									get_time_diff = time_diff(str(start_time_hist[1]), str(task_complete_time))
									print "get_time_diff", get_time_diff

									task_time_history_list[0]['time_diff'] = get_time_diff
						
						task_time_history_list[0]['all_time_history'].append([complete, str(task_complete_time)])
						staff_task_get.qc_time_history = json.dumps(task_time_history_list)
						staff_task_get.qc_time_in_min = task_time_history_list[0]['time_diff']
						staff_task_get.status = 'completed'
						staff_task_get.qc_status = 'completed'
						staff_task_get.save()
						print "staff_task_get.qc_time_in_min", staff_task_get.qc_time_in_min

						#print "staff_task_get.time_history after complete", staff_task_get.time_history

					get_lead_task_id = staff_task_get.lead_task_id
					print "get_lead_task_id", get_lead_task_id

					all_related_staff_tasks = models.StaffTask.objects.filter(lead_task=get_lead_task_id).select_related('lead_task')
					print "all_related_staff_tasks", all_related_staff_tasks
					total_related_tasks = len(all_related_staff_tasks)
					print "total_related_tasks", total_related_tasks

					related_staff_tasks_completed = models.StaffTask.objects.filter(Q(status='completed')|Q(qc_status='completed'), lead_task=get_lead_task_id).select_related('lead_task')
					print "all_related_staff_tasks", related_staff_tasks_completed
					total_related_tasks_completed = len(related_staff_tasks_completed)
					print "total_related_tasks_completed", total_related_tasks_completed

					if total_related_tasks == total_related_tasks_completed:
						leadtask = get_object_or_404(models.LeadTask, id=get_lead_task_id)
						leadtask.status = 'completed'
						leadtask.save()

					all_lead_tasks = models.LeadTask.objects.filter(task=staff_task_get.lead_task.task_id).select_related('task')
					total_lead_tasks = all_lead_tasks.count()
					print "total_lead_tasks", total_lead_tasks
					all_lead_tasks_completed = models.LeadTask.objects.filter(task=staff_task_get.lead_task.task_id, status__in=['completed', 'cancelled'])
					total_lead_tasks_completed = all_lead_tasks_completed.count()

					if total_lead_tasks == total_lead_tasks_completed:
						task = get_object_or_404(models.Task, id=staff_task_get.lead_task.task_id)
						task.status = 'completed'
						task.save()

			else:
				pass

		else:
			pass

		print "task_time_dict", task_time_dict
		return HttpResponse(json.dumps(task_time_dict), content_type='application/json')


def staff_task_status(request):
	time_in_min_dict = {}
	task_time_dict = {}
	task_idle_time_dict = {}
	task_time_list = []
	task_time_history_list = []
	all_time_history_lists = []
	if request.method == "POST" and request.is_ajax():

		print "get object", request.POST.get('s_task_id')
		staff_task_get = get_object_or_404(models.StaffTask, id=request.POST.get('s_task_id'))
		status = staff_task_get.status
		is_working = request.POST.get('workedon')

		if status in ['new', 'pending', 'rejected']:
			if request.POST.has_key('start'):
				if not staff_task_get.is_workedon:
					staff_task_get.is_workedon = True
					start = request.POST.get('start')
					task_start_time = datetime.now()

					if staff_task_get.time_history not in ['', None] :
						pause_time_history_list = []
						task_time_history_list = json.loads(staff_task_get.time_history)	 
						if task_time_history_list[0]['idle_time'] not in ['', None, 0]:
							pause_time_list = []
							time_sum_list = []
							if task_time_history_list[0]['all_time_history']:
								pause_time_list = task_time_history_list[0]['all_time_history'][-1]

								pause_time_history_list = pause_time_list[0].split('--')
								#print "latest pause pause_time_history_list", pause_time_history_list
								if pause_time_history_list[0] == 'pause':
									time_sum_list.append(task_time_history_list[0]['idle_time'])
									idle_time_diff = time_diff(str(pause_time_list[1]), str(task_start_time))
									print "idle_time_diff", idle_time_diff
									time_sum_list.append(idle_time_diff)
									task_time_history_list[0]['idle_time'] =  time_sum(time_sum_list)

						else:
							pause_time_list = []
							if task_time_history_list[0]['all_time_history']:
								pause_time_list = task_time_history_list[0]['all_time_history'][-1]
								print "latest pause time", pause_time_list[0]
								pause_time_history_list = pause_time_list[0].split('--')
								print "latest pause pause_time_history_list", pause_time_history_list
								if pause_time_history_list[0] == 'pause':
									idle_time_diff = time_diff(str(pause_time_list[1]),str(task_start_time))
									print "idle_time_diff", idle_time_diff
									task_time_history_list[0]['idle_time'] = idle_time_diff

						task_time_history_list[0]['all_time_history'].append([start, str(task_start_time)])
						task_idle_time_dict['idle_time'] = task_time_history_list[0]['idle_time']
						staff_task_get.time_history = json.dumps(task_time_history_list)
						staff_task_get.save()
	 
					else:
						task_time_list.append([start, str(task_start_time)])
						#all_time_history_lists = [{'all_time_history':task_time_list, 'time_diff':None} ]
						all_time_history_lists = [{'all_time_history':task_time_list, 'time_diff':None, 'idle_time':None} ]
						staff_task_get.time_history = json.dumps(all_time_history_lists)
						staff_task_get.save()
					print "staff_task_get.time_history", staff_task_get.time_history
	 
					return HttpResponse(json.dumps(task_idle_time_dict), content_type='application/json')
				else:
					task_error_dict = {}
					task_error_dict['error'] = "Your already working on other task"
					return HttpResponseBadRequest(json.dumps(task_error_dict), content_type='application/json')


			elif request.POST.has_key('status'):
				if staff_task_get.is_workedon:
					staff_task_get.is_workedon = False

					pause = request.POST.get('status')
					pause_option = request.POST.get('options')
					print 'pause', pause

					get_time_history = staff_task_get.time_history
					print "get_time_history", get_time_history
					
					if not pause_option in ['cancelled']:
						task_pause_time = datetime.now()
						print "task_pause_time", task_pause_time

						if staff_task_get.time_history not in ['', None]:
							task_time_history_list = json.loads(staff_task_get.time_history)
							print "task_time_history_list", task_time_history_list

							if task_time_history_list[0]['time_diff'] not in ['', None, 0]:
								start_time_hist = []
								time_sum_list = []
								if task_time_history_list[0]['all_time_history']:
									start_time_hist = task_time_history_list[0]['all_time_history'][-1]
									print "latest start_time_hist", start_time_hist
									if start_time_hist[0] == 'start':
										time_sum_list.append(task_time_history_list[0]['time_diff'])
										get_time_diff = time_diff(str(start_time_hist[1]), str(task_pause_time))
										print "get_time_diff", get_time_diff
										time_sum_list.append(get_time_diff)
										task_time_history_list[0]['time_diff'] =  time_sum(time_sum_list)
							else:
								start_time_hist = []
								if task_time_history_list[0]['all_time_history']:
									start_time_hist = task_time_history_list[0]['all_time_history'][-1]
									print "latest start_time_hist", start_time_hist
									if start_time_hist[0] == 'start':
										get_time_diff = time_diff(str(start_time_hist[1]), str(task_pause_time))
										print "get_time_diff", get_time_diff

										task_time_history_list[0]['time_diff'] = get_time_diff
							
							if pause_option == 'pending':
								staff_task_get.status = 'pending'

							task_time_history_list[0]['all_time_history'].append(['%s--%s' %(pause,pause_option), str(task_pause_time)])
							staff_task_get.time_history = json.dumps(task_time_history_list)
							staff_task_get.time_in_min = task_time_history_list[0]['time_diff']
							staff_task_get.save()
						print "staff_task_get.time_history after pausing", staff_task_get.time_history
					else:
						if pause_option == 'cancelled':
							staff_task_get.status = 'cancelled'
						else:
							pass
					staff_task_get.save()
					print "returning time", task_time_history_list[0]['time_diff']
					task_time_dict['time_in_min'] = task_time_history_list[0]['time_diff']

					return HttpResponse(json.dumps(task_time_dict), content_type='application/json')

			elif request.POST.has_key('complete'):
				if staff_task_get.is_workedon:
					staff_task_get.is_workedon = False
					complete = request.POST.get('complete')
					print "complete", complete

					task_complete_time = datetime.now()
					qc_required = staff_task_get.is_qc_required
					
					if qc_required:
						staff_task_get.status = 'qc'
						staff_task_get.qc_status = 'new'
					else:
						staff_task_get.status = 'completed'
						#staff_task_get.save()

					if staff_task_get.time_history not in ['', None]:
						task_time_history_list = json.loads(staff_task_get.time_history)
						print "task_time_history_list", task_time_history_list

						if task_time_history_list[0]['time_diff'] not in ['', None]:
							start_time_hist = []
							time_sum_list = []
							if task_time_history_list[0]['all_time_history']:
								start_time_hist = task_time_history_list[0]['all_time_history'][-1]
								print "latest start_time_hist", start_time_hist
								if start_time_hist[0] == 'start':
									time_sum_list.append(task_time_history_list[0]['time_diff'])
									get_time_diff = time_diff(str(start_time_hist[1]), str(task_complete_time))
									print "get_time_diff", get_time_diff
									time_sum_list.append(get_time_diff)
									task_time_history_list[0]['time_diff'] = time_sum(time_sum_list)
						else:
							start_time_hist = []
							if task_time_history_list[0]['all_time_history']:
								start_time_hist = task_time_history_list[0]['all_time_history'][-1]
								print "latest start_time_hist", start_time_hist
								if start_time_hist[0] == 'start':
									get_time_diff = time_diff(str(start_time_hist[1]), str(task_complete_time))
									print "get_time_diff", get_time_diff
									task_time_history_list[0]['time_diff'] = get_time_diff
						
						task_time_history_list[0]['all_time_history'].append([complete, str(task_complete_time)])
						staff_task_get.time_history = json.dumps(task_time_history_list)
						staff_task_get.time_in_min = task_time_history_list[0]['time_diff']
						staff_task_get.save()
						print "staff_task_get.time_in_min", staff_task_get.time_in_min

						#print "staff_task_get.time_history after complete", staff_task_get.time_history

					get_lead_task_id = staff_task_get.lead_task_id
					print "get_lead_task_id", get_lead_task_id

					all_related_staff_tasks = models.StaffTask.objects.filter(lead_task=get_lead_task_id).select_related('lead_task')
					print "all_related_staff_tasks", all_related_staff_tasks
					total_related_tasks = len(all_related_staff_tasks)
					print "total_related_tasks", total_related_tasks

					related_staff_tasks_completed = models.StaffTask.objects.filter(lead_task=get_lead_task_id, status='completed')
					print "all_related_staff_tasks", related_staff_tasks_completed
					total_related_tasks_completed = len(related_staff_tasks_completed)
					print "total_related_tasks_completed", total_related_tasks_completed

					if total_related_tasks == total_related_tasks_completed:
						leadtask = get_object_or_404(models.LeadTask, id=get_lead_task_id)
						leadtask.status = 'completed'
						leadtask.save()

					all_lead_tasks = models.LeadTask.objects.filter(task=staff_task_get.lead_task.task_id).select_related('task')
					total_lead_tasks = all_lead_tasks.count()
					print "total_lead_tasks", total_lead_tasks
					all_lead_tasks_completed = models.LeadTask.objects.filter(task=staff_task_get.lead_task.task_id, status__in=['completed', 'cancelled'])
					total_lead_tasks_completed = all_lead_tasks_completed.count()

					if total_lead_tasks == total_lead_tasks_completed:
						task = get_object_or_404(models.Task, id=staff_task_get.lead_task.task_id)
						task.status = 'completed'
						task.save()
			else:
				pass
		else:
			pass

		#print "task_time_dict", task_time_dict
		return HttpResponse(json.dumps(task_time_dict), content_type='application/json')


def staff_task_status_ORIG(request):
	time_in_min_dict = {}
	task_time_dict = {}
	task_idle_time_dict = {}
	task_time_list = []
	task_time_history_list = []
	all_time_history_lists = []
	if request.method == "POST" and request.is_ajax():

		print "get object", request.POST.get('s_task_id')
		staff_task_get = get_object_or_404(models.StaffTask, id=request.POST.get('s_task_id'))
		print "staff_task_get", staff_task_get

		status = staff_task_get.status
		print "status", status

		is_working = request.POST.get('workedon')
		print "is_working", is_working

		if status in ['new', 'pending', 'rejected']:
			if request.POST.has_key('start'):
				if not staff_task_get.is_workedon:
					staff_task_get.is_workedon = True

					start = request.POST.get('start')
					print "starting", start
					task_start_time = datetime.now()
					print "task_start_time", task_start_time

					if staff_task_get.time_history not in ['', None] :
						pause_time_history_list = []
	 
						task_time_history_list = json.loads(staff_task_get.time_history)
						print "task_time_history_list", task_time_history_list
	 
						if task_time_history_list[0]['idle_time'] not in ['', None, 0]:
							pause_time_list = []
							time_sum_list = []
							if task_time_history_list[0]['all_time_history']:
								pause_time_list = task_time_history_list[0]['all_time_history'][-1]

								print "==========================="
								print "pause_time_list", pause_time_list
								print "latest pause time", pause_time_list[0]
								pause_time_history_list = pause_time_list[0].split('--')
								print "latest pause pause_time_history_list", pause_time_history_list
								if pause_time_history_list[0] == 'pause':
									time_sum_list.append(task_time_history_list[0]['idle_time'])

									idle_time_diff = time_diff(str(pause_time_list[1]), str(task_start_time))
									print "idle_time_diff", idle_time_diff
									time_sum_list.append(idle_time_diff)
									task_time_history_list[0]['idle_time'] = time_sum(time_sum_list)
									print "task_time_history_list[0]['idle_time']", task_time_history_list[0]['idle_time']

									#task_time_history_list[0]['idle_time'] = task_time_history_list[0]['idle_time'] + idle_time_diff

						else:
							pause_time_list = []
							if task_time_history_list[0]['all_time_history']:
								pause_time_list = task_time_history_list[0]['all_time_history'][-1]
								print "latest pause time", pause_time_list[0]
								pause_time_history_list = pause_time_list[0].split('--')
								print "latest pause pause_time_history_list", pause_time_history_list
								if pause_time_history_list[0] == 'pause':
									idle_time_diff = time_diff(str(pause_time_list[1]),str(task_start_time))
									print "idle_time_diff", idle_time_diff
									task_time_history_list[0]['idle_time'] = idle_time_diff

						task_time_history_list[0]['all_time_history'].append([start, str(task_start_time)])
						task_idle_time_dict['idle_time'] = task_time_history_list[0]['idle_time']
						staff_task_get.time_history = json.dumps(task_time_history_list)
						staff_task_get.save()
	 
					else:
						task_time_list.append([start, str(task_start_time)])
						#all_time_history_lists = [{'all_time_history':task_time_list, 'time_diff':None} ]
						all_time_history_lists = [{'all_time_history':task_time_list, 'time_diff':None, 'idle_time':None} ]
						staff_task_get.time_history = json.dumps(all_time_history_lists)
						staff_task_get.save()
					print "staff_task_get.time_history", staff_task_get.time_history
	 
					return HttpResponse(json.dumps(task_idle_time_dict), content_type='application/json')
				else:
					task_error_dict = {}
					task_error_dict['error'] = "Your already working on other task"
					return HttpResponseBadRequest(json.dumps(task_error_dict), content_type='application/json')

			elif request.POST.has_key('status'):
				if staff_task_get.is_workedon:
					staff_task_get.is_workedon = False
					pause = request.POST.get('status')
					pause_option = request.POST.get('options')
					print 'pause', pause

					get_time_history = staff_task_get.time_history
					print "get_time_history", get_time_history
					
					if not pause_option in ['pending', 'cancelled']:
						task_pause_time = datetime.now()
						print "task_pause_time", task_pause_time

						if staff_task_get.time_history not in ['', None]:
							task_time_history_list = json.loads(staff_task_get.time_history)
							print "task_time_history_list", task_time_history_list

							if task_time_history_list[0]['time_diff'] not in ['', None, 0]:
								start_time_hist = []
								time_sum_list = []
								if task_time_history_list[0]['all_time_history']:
									start_time_hist = task_time_history_list[0]['all_time_history'][-1]
									print "latest start_time_hist", start_time_hist
									if start_time_hist[0] == 'start':
										time_sum_list.append(task_time_history_list[0]['time_diff'])
										get_time_diff = time_diff(str(start_time_hist[1]), str(task_pause_time))
										print "get_time_diff", get_time_diff
										time_sum_list.append(get_time_diff)
										print "time_sum_list", time_sum_list
										task_time_history_list[0]['time_diff'] = time_sum(time_sum_list)

										#task_time_history_list[0]['time_diff'] = task_time_history_list[0]['time_diff'] + get_time_diff
							else:
								start_time_hist = []
								if task_time_history_list[0]['all_time_history']:
									start_time_hist = task_time_history_list[0]['all_time_history'][-1]
									print "latest start_time_hist", start_time_hist
									if start_time_hist[0] == 'start':
										get_time_diff = time_diff(str(start_time_hist[1]), str(task_pause_time))
										print "get_time_diff", get_time_diff

										task_time_history_list[0]['time_diff'] = get_time_diff
							
							task_time_history_list[0]['all_time_history'].append(['%s--%s' %(pause,pause_option), str(task_pause_time)])
							staff_task_get.time_history = json.dumps(task_time_history_list)
							staff_task_get.save()
						print "staff_task_get.time_history after pausing", staff_task_get.time_history
					else:
						if pause_option == 'pending':
							staff_task_get.status = 'pending'
						elif pause_option == 'cancelled':
							staff_task_get.status = 'rejected'
						else:
							pass
					staff_task_get.save()
					print "returning time", task_time_history_list[0]['time_diff']
					task_time_dict['time_in_min'] = task_time_history_list[0]['time_diff']

					return HttpResponse(json.dumps(task_time_dict), content_type='application/json')
				else:
					return HttpResponseBadRequest('error')

			elif request.POST.has_key('complete'):
				complete = request.POST.get('complete')
				print "complete", complete

				task_complete_time = datetime.now()
				qc_required = staff_task_get.is_qc_required
				
				if qc_required:
					staff_task_get.status = 'qc'
					staff_task_get.qc_status = 'new'
				else:
					staff_task_get.status = 'completed'
					#staff_task_get.save()

				if staff_task_get.time_history not in ['', None]:
					task_time_history_list = json.loads(staff_task_get.time_history)
					print "task_time_history_list", task_time_history_list

					if task_time_history_list[0]['time_diff'] not in ['', None]:
						start_time_hist = []
						if task_time_history_list[0]['all_time_history']:
							start_time_hist = task_time_history_list[0]['all_time_history'][-1]
							print "latest start_time_hist", start_time_hist
							if start_time_hist[0] == 'start':
								get_time_diff = time_diff(str(start_time_hist[1]), str(task_complete_time))
								print "get_time_diff", get_time_diff
								task_time_history_list[0]['time_diff'] = task_time_history_list[0]['time_diff'] + get_time_diff
					else:
						start_time_hist = []
						if task_time_history_list[0]['all_time_history']:
							start_time_hist = task_time_history_list[0]['all_time_history'][-1]
							print "latest start_time_hist", start_time_hist
							if start_time_hist[0] == 'start':
								get_time_diff = time_diff(str(start_time_hist[1]), str(task_complete_time))
								print "get_time_diff", get_time_diff
								task_time_history_list[0]['time_diff'] = get_time_diff
					
					task_time_history_list[0]['all_time_history'].append([complete, str(task_complete_time)])
					staff_task_get.time_history = json.dumps(task_time_history_list)
					staff_task_get.time_in_min = task_time_history_list[0]['time_diff']
					staff_task_get.save()
					print "staff_task_get.time_in_min", staff_task_get.time_in_min

					#print "staff_task_get.time_history after complete", staff_task_get.time_history

				get_lead_task_id = staff_task_get.lead_task_id
				print "get_lead_task_id", get_lead_task_id

				all_related_staff_tasks = models.StaffTask.objects.filter(lead_task=get_lead_task_id).select_related('lead_task')
				print "all_related_staff_tasks", all_related_staff_tasks
				total_related_tasks = len(all_related_staff_tasks)
				print "total_related_tasks", total_related_tasks

				related_staff_tasks_completed = models.StaffTask.objects.filter(lead_task=get_lead_task_id, status='completed')
				print "all_related_staff_tasks", related_staff_tasks_completed
				total_related_tasks_completed = len(related_staff_tasks_completed)
				print "total_related_tasks_completed", total_related_tasks_completed

				if total_related_tasks == total_related_tasks_completed:
					leadtask = get_object_or_404(models.LeadTask, id=get_lead_task_id)
					leadtask.status = 'completed'
					leadtask.save()

			else:
				pass

		else:
			pass

		print "task_time_dict", task_time_dict
		return HttpResponse(json.dumps(task_time_dict), content_type='application/json')




@login_required
def staff_task_edit(request, id):
	success_dict={}
	staff_task = get_object_or_404(models.StaffTask, id=id)
	if request.method == "POST":

		form = form1.StaffTaskForm(request.POST, instance=staff_task)
		if form.is_valid():
			staff_task = form.save(commit=False)
			is_qc_required = staff_task.is_qc_required
			status = form.cleaned_data.get('status')

			#if is_qc_required and status=='completed':
			#	qc_agent = staff_task.qc_lead
			#	if qc_status == 'completed':
			#		lead_task_id = staff_task.lead_task_id

			#		lead_task = models.LeadTask.objects.filter(id=lead_task_id)

			staff_task.save()
			

		else:
			error_dict={}
			for error in form.errors:
				error_dict[error] = form.errors[error]
				
			return HttpResponseBadRequest(json.dumps(error_dict))

		success_dict['success_msg'] = "Successfully Edited Lead"
		return HttpResponse(json.dumps(success_dict), content_type='application/json')
	else:
		form = form1.StaffTaskForm(instance=staff_task)

	return render(request, 'project/staff_task_add_partial.html', {'form': form, 'is_edit_mode':True, 'id':id})



@login_required
def project_add(request):

	if request.method == 'POST':
		form = forms.ProjectAdminForm(request.POST, None)

		if form.is_valid():
			project = form.save(commit=False)
			project.title = form.cleaned_data['title']
			project.description = form.cleaned_data['description']
			project.save()

			return HttpResponse('OK')
		else:
			error_dict = {}
			for error in form.errors:
				error_dict[error] = form.errors[ error]
			return HttpResponseBadRequest(json.dumps(error_dict))
	else:
		form = forms.ProjectAdminForm()

		return render(request, 'project/project_add_partial.html', {'form':form})


@login_required
def project_edit(request, id):
	project = get_object_or_404(models.Project, id=id)
	if request.method == "POST":
		form = forms.ProjectAdminForm(request.POST, instance=project)
		if form.is_valid():
			project = form.save(commit=False)
			project.save()
			return HttpResponse('ok ')
		else:
			error_dict={}
			for error in form.errors:
				error_dict[error] = form.errors[error]
				
			return HttpResponseBadRequest(json.dumps(error_dict))
	else:
		form = forms.ProjectAdminForm(instance=project)

	return render(request, 'project/project_add_partial.html', {'form': form, 'is_edit_mode':True, 'id':id})


@login_required
def project_list(request):

	project = models.Project.objects.all()
	return render(request, 'project/project_list_partial.html', 
					{'project': project}
				)




@login_required
def project_task_add(request):

	if request.method == 'POST':
		form = form1.ProjectTaskForm(request.POST, None)

		if form.is_valid():
			project_task = form.save(commit=False)
			
			project_task.save()
			# messages.add_message(request, messages.SUCCESS, _('Successfully Created BillingType'))
			# return HttpResponseRedirect(reverse('billing_types_list'))
			return HttpResponse('OK')
		else:
			error_dict = {}
			for error in form.errors:
				error_dict[error] = form.errors[ error]

			return HttpResponseBadRequest(json.dumps(error_dict))
			# messages.add_message(request, messages.ERROR, _('Please fix errors bellow.'))


	else:
		form = form1.ProjectTaskForm()


		return render(request, 'project/project_task_add_partial.html', {'form':form})

@login_required
def project_task_edit(request, id):
	project_task = get_object_or_404(models.ProjectTask, id=id)
	if request.method == "POST":
		form = form1.ProjectTaskForm(request.POST, instance=project_task)
		if form.is_valid():
			project_task = form.save(commit=False)
			project_task.save()
			return HttpResponse('ok ')
		else:
			error_dict={}
			for error in form.errors:
				error_dict[error] = form.errors[error]
				
			return HttpResponseBadRequest(json.dumps(error_dict))
	else:
		form = form1.ProjectTaskForm(instance=project_task)

	return render(request, 'project/project_task_add_partial.html', {'form': form ,'is_edit_mode':True,'id':id})


@login_required
def project_task_list(request):

	project_task = models.ProjectTask.objects.all()
	return render(request, 'project/project_task_list_partial.html', 
					{'project_task': project_task}
				)

@login_required
def project_service_add(request):

	if request.method == 'POST':
		form = forms.ProjectServiceAdminForm(request.POST, None)

		if form.is_valid():
			project_service = form.save(commit=False)
			
			project_service.save()
			# messages.add_message(request, messages.SUCCESS, _('Successfully Created BillingType'))
			# return HttpResponseRedirect(reverse('billing_types_list'))
			return HttpResponse('OK')
		else:
			error_dict = {}
			for error in form.errors:
				error_dict[error] = form.errors[ error]

			return HttpResponseBadRequest(json.dumps(error_dict))
			# messages.add_message(request, messages.ERROR, _('Please fix errors bellow.'))


	else:
		form = forms.ProjectServiceAdminForm()


		return render(request, 'project/project_service_add_partial.html', {'form':form})

@login_required
def project_service_edit(request, id):
	project_service = get_object_or_404(models.ProjectService, id=id)
	if request.method == "POST":
		form = forms.ProjectServiceAdminForm(request.POST, instance=project_service)
		if form.is_valid():
			project_service = form.save(commit=False)
			
			project_service.save()
			return HttpResponse('ok ')
		else:
			error_dict={}
			for error in form.errors:
				error_dict[error] = form.errors[error]
				
			return HttpResponseBadRequest(json.dumps(error_dict))
	else:
		form = forms.ProjectServiceAdminForm(instance=project_service)

	return render(request, 'project/project_service_add_partial.html', {'form': form ,'is_edit_mode':True,'id':id})


@login_required
def project_service_list(request):

	project_service = models.ProjectService.objects.filter(operations_manager__user=request.user)
	return render(request, 'project/project_service_list_partial.html', 
					{'project_service': project_service}
				)


@login_required
def workitem_add(request):

	if request.method == 'POST':
		form = form1.WorkItemForm(request.POST, None)

		if form.is_valid():
			workitem = form.save(commit=False)
			

			workitem.save()
			# messages.add_message(request, messages.SUCCESS, _('Successfully Created BillingType'))
			# return HttpResponseRedirect(reverse('billing_types_list'))
			return HttpResponse('OK')
		else:
			error_dict = {}
			for error in form.errors:
				error_dict[error] = form.errors[ error]

			return HttpResponseBadRequest(json.dumps(error_dict))
			# messages.add_message(request, messages.ERROR, _('Please fix errors bellow.'))


	else:
		form = form1.WorkItemForm()


		return render(request, 'project/workitem_add_partial.html', {'form':form})


@login_required
def workitem_edit(request, id):
	workitem = get_object_or_404(models.WorkItem, id=id)
	if request.method == "POST":
		form = form1.WorkItemForm(request.POST, instance=workitem)
		if form.is_valid():
			workitem = form.save(commit=False)
			workitem.save()
			return HttpResponse('ok ')
		else:
			error_dict={}
			for error in form.errors:
				error_dict[error] = form.errors[error]
				
			return HttpResponseBadRequest(json.dumps(error_dict))
	else:
		form = form1.WorkItemForm(instance=workitem)

	return render(request, 'project/workitem_add_partial.html', {'form': form ,'is_edit_mode':True,'id':id})

@login_required
def workitem_list(request):

	workitem = models.WorkItem.objects.all()
	return render(request, 'project/workitem_list_partial.html', 
					{'workitem': workitem}
				)


@login_required
def qc_assign_add(request):

	if request.method == 'POST':
		form = form1.QcAssignmentForm(request.POST, None)

		if form.is_valid():
			qc_assign = form.save(commit=False)
		
			
			qc_assign.save()
			# messages.add_message(request, messages.SUCCESS, _('Successfully Created BillingType'))
			# return HttpResponseRedirect(reverse('billing_types_list'))
			return HttpResponse('OK')
		else:
			error_dict = {}
			for error in form.errors:
				error_dict[error] = form.errors[ error]

			return HttpResponseBadRequest(json.dumps(error_dict))
			# messages.add_message(request, messages.ERROR, _('Please fix errors bellow.'))


	else:
		form = form1.QcAssignmentForm()


	return render(request, 'project/qc_assign_add_partial.html', {'form':form})

@login_required
def qc_assign_edit(request, id):
	qc_assign = get_object_or_404(models.WorkItemAssignment, id=id)
	if request.method == "POST":
		form = form1.QcAssignmentForm(request.POST, instance=qc_assign)
		if form.is_valid():
			qc_assign = form.save(commit=False)
			qc_assign.save()
			return HttpResponse('ok ')
		else:
			error_dict={}
			for error in form.errors:
				error_dict[error] = form.errors[error]
				
			return HttpResponseBadRequest(json.dumps(error_dict))
	else:
		form = form1.QcAssignmentForm(instance=qc_assign)

		return render(request, 'project/qc_assign_add_partial.html', {'form': form ,'is_edit_mode':True,'id':id})

@login_required
def qc_assign_list(request):

	qc_assign = models.WorkItemAssignment.objects.all()
	return render(request, 'project/qc_assign_list_partial.html', 
					{'qc_assign': qc_assign}
				)

@login_required
def daily_task_add(request):

	if request.method == 'POST':
		form = form1.WorkItemAssignmentForm(request.POST, None)

		if form.is_valid():
			daily_task = form.save(commit=False)
			daily_task.title = form.cleaned_data['title']
			
			daily_task.save()
			# messages.add_message(request, messages.SUCCESS, _('Successfully Created BillingType'))
			# return HttpResponseRedirect(reverse('billing_types_list'))
			return HttpResponse('OK')
		else:
			error_dict = {}
			for error in form.errors:
				error_dict[error] = form.errors[ error]

			return HttpResponseBadRequest(json.dumps(error_dict))
			# messages.add_message(request, messages.ERROR, _('Please fix errors bellow.'))


	else:
		form = form1.WorkItemAssignmentForm()



		return render(request, 'project/daily_task_add_partial.html', {'form':form})

@login_required
def daily_task_edit(request, id):
	daily_task = get_object_or_404(models.WorkItemAssignment, id=id)
	if request.method == "POST":
		form = form1.WorkItemAssignmentForm(request.POST, instance=daily_task)
		if form.is_valid():
			daily_task = form.save(commit=False)
			daily_task.save()
			return HttpResponse('ok ')
		else:
			error_dict={}
			for error in form.errors:
				error_dict[error] = form.errors[error]
				
			return HttpResponseBadRequest(json.dumps(error_dict))
	else:
		form = form1.WorkItemAssignmentForm(instance=daily_task)

	return render(request, 'project/daily_task_add_partial.html', {'form': form ,'is_edit_mode':True,'id':id})

@login_required
def daily_task_list(request):

	daily_task = models.WorkItemAssignment.objects.all()
	return render(request, 'project/daily_task_list_partial.html', 
					{'daily_task': daily_task}
				)

def qc_task_hist_list(request):
	
	f = custom_filters.QcTaskFilter(request.GET, queryset=models.StaffTask.objects.filter(qc_lead__user__username=request.user,status__in=['completed']))

	return render(request, 'project/qc_task_hist_list_partial.html', {'filter': f})

	
@login_required
def qc_task_list(request):
	#qc_task = models.StaffTask.objects.all()
	if request.user.groups.filter(name='qc').exists():
		qc_task =models.StaffTask.objects.filter(Q(status='qc') | Q(qc_status='new'), qc_lead__user__username=request.user, )
		#qc_task =models.StaffTask.objects.filter(Q(status='qc') | Q(qc_status='new'), qc_lead__user__username=request.user)
	
	
	return render(request, 'project/qc_task_list_partial.html', 
					{'qc_task': qc_task}
				)

@login_required
def qc_task_add(request):

	if request.method == 'POST':
		form = form1.QcTaskForm(request.POST, None)

		if form.is_valid():
			qc_task = form.save(commit=False)
			qc_task.save()

			return HttpResponse('OK')
		else:
			error_dict = {}
			for error in form.errors:
				error_dict[error] = form.errors[ error]
			return HttpResponseBadRequest(json.dumps(error_dict))
	else:
		form = form1.QcTaskForm()

		return render(request, 'project/qc_task_add_partial.html', {'form':form})


@login_required
def qc_task_edit(request, id):
	success_dict={}
	qc_task = get_object_or_404(models.StaffTask, id=id)
	get_lead_task_id = models.LeadTask.objects.get(id=qc_task.lead_task_id)
	print "get_lead_task_id", get_lead_task_id
	get_task_id = models.Task.objects.get(id=get_lead_task_id.task_id)
	print "get_task_id", get_task_id

	get_service_id = models.Service.objects.get(id=get_task_id.service_id)
	print "get_service_id", get_service_id

	qc_checklist = models.StaffTaskQc.objects.get(staff_task=qc_task)

	if request.method == "POST":
		form = form1.QcTaskForm(request.POST, instance=qc_task)
		qc_checklist_form = form1.StaffTaskQcForm(request.POST or None,instance=qc_checklist, service_name=get_service_id)
		if form.is_valid():
			qc_task = form.save(commit=False)
			qc_task.save()
			qc_checklist = qc_checklist_form.save(commit=False)
			qc_checklist.staff_task = qc_task
			qc_checklist.save()

			success_dict['success_msg'] = "Successfully Edited Qc"
			return HttpResponse(json.dumps(success_dict), content_type='application/json')
		
		else:
			error_dict={}
			for error in form.errors:
				error_dict[error] = form.errors[error]
			return HttpResponseBadRequest(json.dumps(error_dict))
	else:
		form = form1.QcTaskForm(instance=qc_task)
		qc_checklist_form = form1.StaffTaskQcForm(instance=qc_checklist,service_name=get_service_id)
	return render(request, 'project/qc_task_add_partial.html', {
									'form': form,
									'qc_checklist_form':qc_checklist_form, 
									'is_edit_mode':True, 
									'id':id
								}
							)
@login_required
def qc_template_list(request):
	
	qc_template =models.QcTemplate.objects.all()
	
	
	return render(request, 'project/qc_template_list_partial.html', 
					{'qc_template': qc_template}
				)

@login_required
def qc_template_add(request):
	success_dict={}
	if request.method == 'POST':
		form = form1.QcTemplateForm(request.POST, None)

		if form.is_valid():
			qc_template = form.save(commit=False)
			qc_template.save()

			
		else:
			error_dict = {}
			for error in form.errors:
				error_dict[error] = form.errors[ error]
			return HttpResponseBadRequest(json.dumps(error_dict))
		success_dict['success_msg'] = "Successfully Edited Qc"
		return HttpResponse(json.dumps(success_dict), content_type='application/json')
	else:
		form = form1.QcTemplateForm()

		return render(request, 'project/qc_template_add_partial.html', {'form':form})


@login_required
def qc_template_edit(request, id):
	success_dict={}
	qc_template = get_object_or_404(models.QcTemplate, id=id)
	if request.method == "POST":
		form = form1.QcTemplateForm(request.POST, instance=qc_template)
		if form.is_valid():
			qc_template = form.save(commit=False)
			
			qc_template.save()
			
		
		else:
			error_dict={}
			for error in form.errors:
				error_dict[error] = form.errors[error]
				
			return HttpResponseBadRequest(json.dumps(error_dict))
		success_dict['success_msg'] = "Successfully Edited Qc"
		return HttpResponse(json.dumps(success_dict), content_type='application/json')
	else:
		form = form1.QcTemplateForm(instance=qc_template)

	return render(request, 'project/qc_template_add_partial.html', {'form': form, 'is_edit_mode':True, 'id':id})
