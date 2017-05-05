	# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import json
import xlwt
from django.db import transaction
from django.core.urlresolvers import reverse
from django.shortcuts import render, get_object_or_404 , redirect
from django.utils.translation import ugettext_lazy as _
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required
from django.forms.models import formset_factory, modelform_factory, modelformset_factory
from employee.models import Employee,EmployeeRole
from project import models 
#from inhouseapp.utils.decorators import log, anonymous_required, group_required
from .forms import LeadForm, CustomerForm, FollowupForm1, ExampleFormSetHelper, CountryForm, CurrencyTypeForm, ImportLeadForm
from .models import Lead, Customer, Followup, Country, CurrencyType
from django.contrib import messages
from project import csvimporter

# Create your views here.
@login_required
def leads_list(request):
	if request.user.groups.filter(name='sales manager'):
		leads = Lead.objects.filter(owner__user= request.user).exclude(Q(latest_lead_status="WON") | Q(is_converted_to_customer=True)).order_by('-lead_date')
	elif request.user.groups.filter(name='sales rep'):
		leads = Lead.objects.filter(sales_rep__user= request.user).exclude(Q(latest_lead_status="WON") | Q(is_converted_to_customer=True)).order_by('-lead_date')
	elif request.user.groups.filter(name='management'):
		leads = Lead.objects.exclude(Q(latest_lead_status="WON") | Q(is_converted_to_customer=True)).order_by('-lead_date')

	return render(request,
					"customer/lead_list_partial.html",
					{'leads': leads,
				}
			)


def get_services(request):
	
	if request.method == "POST":
		industry = request.POST.get('industry_id')
		#industry = get_object_or_404(models.Industry, id=industry_id)
		all_services = models.ServiceType.objects.filter(industry=industry)
		services_list = []
		if industry:
			for service_type in all_services:
				service_type_dict = {}
				service_type_dict['pk'] = service_type.pk
				service_type_dict['title'] = service_type.title
				services_list.append(service_type_dict)
			print services_list
		return HttpResponse(json.dumps(services_list), content_type='application/json')


@login_required
def lead_add(request):
	"""
	Function for customer enquiry form
	"""
	customer_dict = dict([(cust.title, cust.id) for cust in Customer.objects.all()])
	success_dict={}
	form = LeadForm(request=request)
	FollowupFormset = formset_factory(FollowupForm1, extra=1)
	if request.method == 'POST':
		form = LeadForm(request.POST or None, request=request)

		followup_formset_forms = FollowupFormset(request.POST or None, prefix='followups' )

		for follow_form in followup_formset_forms.deleted_forms:
			followup_form_instance = follow_form.instance
			if followup_form_instance.pk:
				followup_form_instance.delete()
		if form.is_valid() and followup_formset_forms.is_valid():
			enquiry_form = form.save(commit=False)
			enquiry_form.created_by =  request.user
			is_converted_to_cust = form.cleaned_data['is_converted_to_customer']
			all_services = form.cleaned_data['services']

			if request.user.groups.filter(name='sales rep').exists():
				enquiry_form.owner = form.cleaned_data.get('owner')
				enquiry_form.sales_rep = Employee.objects.get(user__username = request.user)
			
			elif request.user.groups.filter(name='sales manager').exists():
				enquiry_form.owner = Employee.objects.get(user__username = request.user)
				#enquiry_form.sales_rep = form.cleaned_data.get('sales_rep')
			
			followup_status_list = []
			converted_to_cust_list = []

			for followup_formset_form in followup_formset_forms:
				if followup_formset_form not in [deleted_form for deleted_form in followup_formset_forms.deleted_forms]:
					followup_formset_instance = followup_formset_form.save(commit=False)
					next_followup = followup_formset_form.cleaned_data.get('next_followup')
					lead_status = followup_formset_form.cleaned_data.get('lead_status')
					converted_to_cust = followup_formset_form.cleaned_data.get('is_converted_to_customer')
					if converted_to_cust:
						enquiry_form.is_converted_to_customer = True
					if next_followup not in ['', None]:
						followup_status_list.append([next_followup, lead_status])
						converted_to_cust_list.append(converted_to_cust)

			if followup_status_list:
				if followup_status_list[-1]:
					enquiry_form.latest_followup_date = followup_status_list[-1][0]
					enquiry_form.latest_lead_status = followup_status_list[-1][1]				
			else:
				enquiry_form.latest_followup_date = None
				enquiry_form.latest_lead_status = None
			enquiry_form.save()
			enquiry_form.services = all_services

			for followup_formset_form in followup_formset_forms:
				followup_formset_instance = followup_formset_form.save(commit=False)
				followup_formset_instance.lead = enquiry_form
				if next_followup not in ['', None]:
					followup_formset_instance.save()

			add_to_cust = Customer(title = form.cleaned_data['title'],
							description  = form.cleaned_data['description'],
							contact_name = form.cleaned_data['contact_name'],
							designation  = form.cleaned_data['designation'],
							email        = form.cleaned_data['email'],
							phone        = form.cleaned_data['phone'],
							addressline1 = form.cleaned_data['addressline1'],
							addressline2 = form.cleaned_data['addressline2'],
							city         = form.cleaned_data['city'],
							state        = form.cleaned_data['state'],
							country      = form.cleaned_data['country'],
							zip_code     = form.cleaned_data['zip_code'],
							requirement  = form.cleaned_data['requirement'],
							industry     = form.cleaned_data['industry'],
							lead_source  = form.cleaned_data['lead_source'],			
							other_lead_source  = form.cleaned_data['other_lead_source'], 
							#created_by   = form.cleaned_data['created_by'],
							sales_rep    = enquiry_form.sales_rep,
							owner    = enquiry_form.owner
					)
			if is_converted_to_cust or True in converted_to_cust_list:
				if enquiry_form.title not in customer_dict:
					add_to_cust.save()
					add_to_cust.services = all_services
				else:
					country = Country.objects.get(name=form.cleaned_data.get('country'))
					existed_customer = Customer.objects.get(title__exact=enquiry_form.title)
					existed_customer.title = form.cleaned_data['title']
					existed_customer.description  = form.cleaned_data['description']
					existed_customer.contact_name = form.cleaned_data['contact_name']
					existed_customer.designation  = form.cleaned_data['designation']
					existed_customer.email        = form.cleaned_data['email']
					existed_customer.phone        = form.cleaned_data['phone']
					existed_customer.addressline1 = form.cleaned_data['addressline1']
					existed_customer.addressline2 = form.cleaned_data['addressline2']
					existed_customer.city         = form.cleaned_data['city']
					existed_customer.state        = form.cleaned_data['state']
					existed_customer.country      = country
					existed_customer.zip_code     = form.cleaned_data['zip_code']
					existed_customer.requirement  = form.cleaned_data['requirement']
					existed_customer.industry     = form.cleaned_data['industry']
					existed_customer.lead_source  = form.cleaned_data['lead_source']
					existed_customer.other_lead_source  = form.cleaned_data['other_lead_source']
					existed_customer.sales_rep    = enquiry_form.sales_rep
					existed_customer.owner    = enquiry_form.owner
					existed_customer.save()
					existed_customer.services = all_services
			else:				
				enquiry_form.save()
				enquiry_form.services = all_services

			success_dict['success_msg'] = "Successfully Created Lead"
			return HttpResponse(json.dumps(success_dict), content_type='application/json')

		else:
			error_dict = {}
			form_error_dict = {}
			formset_error_dict = {}
		
			for error in form.errors:
				e = form.errors[error]
				form_error_dict[error] = unicode(e)

			for f1 in followup_formset_forms:
				if f1.errors:
					for error in f1.errors:
						e = f1.errors[error]
						formset_error_dict[error] = unicode(e)
			error_dict['form_errors'] = form_error_dict
			error_dict['formset_errors'] = formset_error_dict
			return HttpResponseBadRequest(json.dumps(error_dict))
	else:
		form = LeadForm(request=request)
		followup_formset_forms = FollowupFormset(prefix='followups')
		return render(request, 'customer/lead_add_partial.html', locals())

@login_required
def lead_edit_orgin(request, id):
	success_dict={}
	lead = get_object_or_404(Lead, id=id)
	followups = Followup.objects.filter(lead=lead)

	customer_dict = dict([(cust.title, cust.id) for cust in Customer.objects.all()])

	FollowupFormset = modelformset_factory(Followup, FollowupForm1, extra=1, can_delete=True)
	followup_formset_forms = FollowupFormset(queryset=Followup.objects.filter(lead=lead), prefix='followups',)
	
	if request.method == "POST":
		form = LeadForm(request.POST, instance=lead)
		#print "printing followup_formset", followup_formset

		if lead:
			followup_formset_forms = FollowupFormset(request.POST or None, queryset=Followup.objects.filter(lead=lead), prefix='followups',)
		# else:
		# 	followup_formset_forms = FollowupFormset(request.POST or None, queryset=Followup.objects.none(), prefix='followups',)

		for followup_formset_form in followup_formset_forms.deleted_forms:
			followup_formset_form_instance = followup_formset_form.instance
			if followup_formset_form_instance.pk:
				followup_formset_form_instance.delete()

		if form.is_valid() and followup_formset_forms.is_valid():

			enquiry_form = form.save(commit=False)
			is_converted_to_cust = form.cleaned_data['is_converted_to_customer']

			#enquiry_form.sales_rep = EmployeeRole.objects.get(user__username = request.user)
			enquiry_form.owner = Employee.objects.get(user__username=request.user)
			all_services = form.cleaned_data['services'] 
			print "all_services", all_services

			add_to_cust = Customer(title = form.cleaned_data['title'],
									description  = form.cleaned_data['description'],
									contact_name = form.cleaned_data['contact_name'],
									designation  = form.cleaned_data['designation'],
									email        = form.cleaned_data['email'],
									phone        = form.cleaned_data['phone'],
									addressline1 = form.cleaned_data['addressline1'],
									addressline2 = form.cleaned_data['addressline2'],
									city         = form.cleaned_data['city'],
									state        = form.cleaned_data['state'],
									country      = form.cleaned_data['country'],
									zip_code     = form.cleaned_data['zip_code'],
									requirement  = form.cleaned_data['requirement'],
									industry     = form.cleaned_data['industry'],
									lead_source  = form.cleaned_data['lead_source'],			
									other_lead_source  = form.cleaned_data['other_lead_source'], 
									#created_by   = form.cleaned_data['created_by'],
									sales_rep    = Employee.objects.get(user__username = request.user),
									owner    = Employee.objects.get(user__username = request.user),
							 )
			followup_status_list = []
			for followup_formset_form in followup_formset_forms:
				if followup_formset_form not in [deleted_form for deleted_form in followup_formset_forms.deleted_forms]:
					followup_formset_instance = followup_formset_form.save(commit=False)
					
					next_followup = followup_formset_form.cleaned_data.get('next_followup')
					lead_status = followup_formset_form.cleaned_data.get('lead_status')
					
					followup_status_list.append([next_followup, lead_status])


					if followup_formset_instance.next_followup:
						enquiry_form.latest_followup_date = followup_formset_instance.next_followup
						enquiry_form.latest_lead_status = followup_formset_instance.lead_status
					#else:
					#	enquiry_form.latest_followup_date = None
					#	enquiry_form.latest_lead_status = None

						
					try:
						converted_to_cust = followup_formset_form.cleaned_data['is_converted_to_customer']
						
						enquiry_form.save()
						enquiry_form.services = all_services
						#for service in all_services:
						#	enquiry_form.services.add(service)
						followup_formset_instance.lead = enquiry_form
						followup_formset_instance.save()
						
						if converted_to_cust and enquiry_form.title not in customer_dict:
							add_to_cust.save()
							add_to_cust.services = all_services
						#else:

						#	customer = Customer.objects.get(title=enquiry_form.title)
						#	print "customer",customer
						#	customer.services = all_services

						#else:
							#messages.add_message(request, messages.ERROR, _('This Customer is aleready existed"'))
					except KeyError:
						pass

			#if enquiry_form.latest_lead_status not in ['', None]:
			enquiry_form.save()
			enquiry_form.services = all_services
			#for service in all_services:
			#	enquiry_form.services.add(service)
			#	print service

			if is_converted_to_cust and not enquiry_form.title in customer_dict:
				add_to_cust.save()
				add_to_cust.services = all_services
			#else:
			#	customer = Customer.objects.get(title=enquiry_form.title)
			#	print "customer",customer
			#	customer.services = all_services


			success_dict['success_msg'] = "Successfully Edit Lead"
			return HttpResponse(json.dumps(success_dict), content_type='application/json')

		else:
			if request.is_ajax():
				error_dict = {}
				form_error_dict = {}
				formset_error_dict = {}
			
				for error in form.errors:
					e = form.errors[error]
					form_error_dict[error] = unicode(e)

				for f1 in followup_formset_forms:
					if f1.errors:
						for error in f1.errors:
							e = f1.errors[error]
							formset_error_dict[error] = unicode(e)
				error_dict['form_errors'] = form_error_dict
				error_dict['formset_errors'] = formset_error_dict

				return HttpResponseBadRequest(json.dumps(error_dict))
			else:
				pass

	else:
		form = LeadForm(instance=lead)
		followup_formset_forms = followup_formset_forms
		return render(request, 'customer/lead_add_partial.html', {
										'form':form,
										'followup_formset_forms':followup_formset_forms,
										'is_edit_mode':True, 
										'id':id}
									)


@login_required
def lead_edit(request, id):
	success_dict={}
	lead = get_object_or_404(Lead, id=id)
	followups = Followup.objects.filter(lead=lead)
	company_name = lead.title
	customer_dict = dict([(cust.title, cust.id) for cust in Customer.objects.all()])
	FollowupFormset = modelformset_factory(Followup,FollowupForm1, extra=1,can_order=True,can_delete=True)
	followup_formset_forms = FollowupFormset(queryset=Followup.objects.filter(lead=lead), prefix='followups',)
	
	if request.method == "POST":
		form = LeadForm(request.POST, instance=lead, request=request)

		if lead:
			followup_formset_forms = FollowupFormset(request.POST or None, queryset=Followup.objects.filter(lead=lead), prefix='followups',)
		else:
			followup_formset_forms = FollowupFormset(request.POST or None, queryset=Followup.objects.none(), prefix='followups',)

		for followup_formset_form in followup_formset_forms.deleted_forms:
			followup_formset_form_instance = followup_formset_form.instance
			if followup_formset_form_instance.pk:
				followup_formset_form_instance.delete()

		if form.is_valid() and followup_formset_forms.is_valid():

			enquiry_form = form.save(commit=False)
			is_converted_to_cust = form.cleaned_data['is_converted_to_customer']

			if request.user.groups.filter(name='sales rep').exists():
				enquiry_form.sales_rep = Employee.objects.get(user__username = request.user)
			
			elif request.user.groups.filter(name='sales manager').exists():
				enquiry_form.owner = Employee.objects.get(user__username = request.user)
				
			all_services = form.cleaned_data['services'] 
			print "all_services", all_services

			followup_status_list = []
			converted_to_cust_list = []

			for followup_formset_form in followup_formset_forms:
				if followup_formset_form not in [deleted_form for deleted_form in followup_formset_forms.deleted_forms]:
					followup_formset_instance = followup_formset_form.save(commit=False)
					next_followup = followup_formset_form.cleaned_data.get('next_followup')
					lead_status = followup_formset_form.cleaned_data.get('lead_status')
					converted_to_cust = followup_formset_form.cleaned_data.get('is_converted_to_customer')

					if next_followup not in ['', None]: 
						followup_status_list.append([next_followup, lead_status])
						converted_to_cust_list.append(converted_to_cust)

			if followup_status_list:
				if followup_status_list[-1]:
					enquiry_form.latest_followup_date = followup_status_list[-1][0]
					enquiry_form.latest_lead_status = followup_status_list[-1][1]				
			# else:
			# 	enquiry_form.latest_followup_date = None
			# 	enquiry_form.latest_lead_status = None
 
			enquiry_form.save()
			enquiry_form.services = all_services
			
			for followup_formset_form in followup_formset_forms:
				if followup_formset_form not in [deleted_form for deleted_form in followup_formset_forms.deleted_forms]:
					followup_formset_instance = followup_formset_form.save(commit=False)
					followup_formset_instance.lead = enquiry_form
					if next_followup not in ['', None]:
						followup_formset_instance.save()
			
			add_to_cust = Customer(title = form.cleaned_data['title'],
						description  = form.cleaned_data['description'],
						contact_name = form.cleaned_data['contact_name'],
						designation  = form.cleaned_data['designation'],
						email        = form.cleaned_data['email'],
						phone        = form.cleaned_data['phone'],
						addressline1 = form.cleaned_data['addressline1'],
						addressline2 = form.cleaned_data['addressline2'],
						city         = form.cleaned_data['city'],
						state        = form.cleaned_data['state'],
						country      = form.cleaned_data['country'],
						zip_code     = form.cleaned_data['zip_code'],
						requirement  = form.cleaned_data['requirement'],
						industry     = form.cleaned_data['industry'],
						lead_source  = form.cleaned_data['lead_source'],			
						other_lead_source  = form.cleaned_data['other_lead_source'], 
						#created_by   = form.cleaned_data['created_by'],
						sales_rep = enquiry_form.sales_rep,
						owner = enquiry_form.owner
				 )
			print "converted_to_cust_list", converted_to_cust_list
			if is_converted_to_cust or True in converted_to_cust_list:
				if company_name not in customer_dict:
					add_to_cust.save()
					add_to_cust.services = all_services
				else:
					country = Country.objects.get(name=form.cleaned_data.get('country'))
					existed_customer = Customer.objects.get(title__exact=company_name)
					existed_customer.title = form.cleaned_data.get('title')
					existed_customer.description  = form.cleaned_data['description']
					existed_customer.contact_name = form.cleaned_data['contact_name']
					existed_customer.designation  = form.cleaned_data['designation']
					existed_customer.email        = form.cleaned_data['email']
					existed_customer.phone        = form.cleaned_data['phone']
					existed_customer.addressline1 = form.cleaned_data['addressline1']
					existed_customer.addressline2 = form.cleaned_data['addressline2']
					existed_customer.city         = form.cleaned_data['city']
					existed_customer.state        = form.cleaned_data['state']
					existed_customer.country      = form.cleaned_data.get('country')
					existed_customer.zip_code     = form.cleaned_data['zip_code']
					existed_customer.requirement  = form.cleaned_data['requirement']
					existed_customer.industry     = form.cleaned_data['industry']
					existed_customer.lead_source  = form.cleaned_data['lead_source']
					existed_customer.other_lead_source  = form.cleaned_data['other_lead_source']
					existed_customer.sales_rep = enquiry_form.sales_rep
					existed_customer.owner = enquiry_form.owner
					existed_customer.save()
					existed_customer.services = all_services
			else:
				enquiry_form.save()
				enquiry_form.services = all_services

			success_dict['success_msg'] = "Successfully Edit Lead"
			return HttpResponse(json.dumps(success_dict), content_type='application/json')

		else:
			
			error_dict = {}
			form_error_dict = {}
			formset_error_dict = {}
		
			for error in form.errors:
				e = form.errors[error]
				form_error_dict[error] = unicode(e)

			for f1 in followup_formset_forms:
				if f1.errors:
					for error in f1.errors:
						e = f1.errors[error]
						formset_error_dict[error] = unicode(e)
			error_dict['form_errors'] = form_error_dict
			error_dict['formset_errors'] = formset_error_dict

			return HttpResponseBadRequest(json.dumps(error_dict))

	else:
		form = LeadForm(instance=lead, request=request)
		followup_formset_forms = FollowupFormset(queryset=Followup.objects.filter(lead=lead), prefix='followups',)
		return render(request, 'customer/lead_add_partial.html', {
										'form':form,
										'followup_formset_forms':followup_formset_forms,
										'is_edit_mode':True, 
										'id':id}
									)



@login_required
def leads_view(request,id):

	lead = get_object_or_404(Lead, id=id)
	followups = Followup.objects.filter(lead=lead)

	return render(request, 'customer/lead_view_partial.html', locals()

						)




@login_required
def customers_view(request,id):

	customer = get_object_or_404(Customer, id=id)
	
	if request.method == "POST":
		form = CustomerForm(request.POST, instance=customer, request=request)
		if form.is_valid():
			customer = form.save(commit=False)
			customer.save()

		else:
			#messages.add_message(request, messages.ERROR, _('Please fix errors bellow.'))
			if request.is_ajax():
				error_dict={}
				if form.errors:
					for error in form.errors:
						e  = form.errors[error]
						error_dict[error] = unicode(e)
					return HttpResponseBadRequest(json.dumps(error_dict))
			else:
				pass
	else:
		form = CustomerForm(instance=customer)
	return render(request, 'customer/customer_view_partial.html', locals()

						)

@login_required
def customers_list(request):
	emp_owner = Employee.objects.filter(user__username = request.user)
	print "em owner", emp_owner

	if request.user.groups.filter(name='sales manager').exists():
		customers = Customer.objects.filter(owner__user= request.user)

		leads = Lead.objects.filter(owner__user = request.user)
	
		return render(request,"customer/customer_list_partial.html",locals())

	elif request.user.groups.filter(name='management').exists():
		customers = Customer.objects.all()
	


		return render(request,"customer/customer_list_partial.html",locals())



@login_required
def customer_add(request):
	success_dict = {}
	form = CustomerForm(request.POST, None)
	if request.method == 'POST':
		if form.is_valid():

			cust = form.save(commit=False)
			cust.title = form.cleaned_data['title']
			cust.description = form.cleaned_data['description']

			cust.owner = Employee.objects.get(user__username = request.user)
			cust.created_by =  request.user
			all_services = form.cleaned_data['services']
			cust.save()
			cust.services = all_services
			#messages.add_message(request, messages.SUCCESS, _('Successfully Created Industry'))
			success_dict['success_msg'] = "Successfully Created Customer"
			return HttpResponse(json.dumps(success_dict), content_type='application/json')

		else:
			#messages.add_message(request, messages.ERROR, _('Please fix errors bellow.'))
			if request.is_ajax():
				error_dict={}
				if form.errors:
					for error in form.errors:
						e  = form.errors[error]
						error_dict[error] = unicode(e)
					return HttpResponseBadRequest(json.dumps(error_dict))
			else:
				pass
	else:
		form = CustomerForm()

	return render(request, 'customer/customer_add_partial.html', {'form':form,}
						)


@login_required
def customer_edit(request, id):
	success_dict = {}
	customer = get_object_or_404(Customer, id=id)
	if request.method == "POST":
		form = CustomerForm(request.POST, instance=customer)
		if form.is_valid():
			customer = form.save(commit=False)
			customer.sales_manager = request.user
			#post.published_date = timezone.now()
			all_services = form.cleaned_data['services']
			customer.save()
			customer.services = all_services 
			success_dict['success_msg'] = "Successfully Edit customer"
			return HttpResponse(json.dumps(success_dict), content_type='application/json')
		else:
			error_dict={}
			for error in form.errors:
				error_dict[error] = form.errors[error]
			
			return HttpResponseBadRequest(json.dumps(error_dict))
	else:
		form = CustomerForm(instance=customer)	
	return render(request, 'customer/customer_add_partial.html', {'form': form, 'is_edit_mode':True, 'id':id})


@login_required
def customer_detail(request, slug):
	post = get_object_or_404(Customer, slug=slug)
	if request.method == "POST":
		form = CustomerForm(request.POST, instance=post)
		if form.is_valid():
			post = form.save(commit=False)
			post.sales_manager = request.user
			#post.published_date = timezone.now()
			post.save()
			messages.add_message(request, messages.SUCCESS, _('Successfully Changed Customer Details'))
			return HttpResponseRedirect(reverse('customers_list'))
	else:
		form = CustomerForm(instance=post)
	return render(request, 'customer/customer_edit.html', {'form': form})




@login_required
def customer_route(request, id):
	id = int(id)
	project = get_object_or_404(Project, id=id)

	groups=request.user.groups.all()

	group_dict = dict([ (grp.name, grp)  for  grp in groups])

	if request.user.groups.filter(name='customer').exists():
		return render(request,"project/project_detail.html",{'project': project})

	elif request.user.groups.filter(name='operations manager').exists():
		return render(request,"project/project_detail.html",{'project': project})


	return render(request,"project/project_detail.html",{'project': project})




@login_required
def country_list(request):

	countries = Country.objects.all()
	return render(request, 'customer/country_list_partial.html', 
					{'countries': countries}
				)

@login_required
def country_add(request):
	success_dict={}
	form = CountryForm(request.POST, None)
	if request.method == 'POST':
		if form.is_valid():
			country = form.save(commit=False)
			country.save()
			success_dict['success_msg'] = "Successfully Created Country"
			return HttpResponse(json.dumps(success_dict), content_type='application/json')
			#messages.add_message(request, messages.SUCCESS, _('Successfully Created Industry'))
			
		else:
			error_dict = {}
			for error in form.errors:
				error_dict[error] = form.errors[ error]
			return HttpResponseBadRequest(json.dumps(error_dict))
	else:
		form = CountryForm

		return render(request, 'customer/country_add_partial.html', {'form':form,})


@login_required
def country_edit(request, id):
	success_dict={}
	country = get_object_or_404(Country, id=id)
	if request.method == "POST":
		form = CountryForm(request.POST, instance=country)
		if form.is_valid():
			country = form.save(commit=False)
			country.save()

			success_dict['success_msg'] = "Successfully Edit Country"
			return HttpResponse(json.dumps(success_dict), content_type='application/json')
		else:
			error_dict={}
			for error in form.errors:
				error_dict[error] = form.errors[error]

			return HttpResponseBadRequest(json.dumps(error_dict))
	else:
		form = CountryForm(instance=country)
	return render(request, 'customer/country_add_partial.html', {'form': form, 'is_edit_mode':True, 'id':id})



@login_required
def currency_type_list(request):

	currencies = CurrencyType.objects.all()
	return render(request, 'customer/currency_type_list_partial.html', 
					{'currencies': currencies}
				)

@login_required
def currency_type_add(request):
	success_dict={}

	form = CurrencyTypeForm(request.POST, None)
	if request.method == 'POST':
		if form.is_valid():
			currency_type = form.save(commit=False)
			currency_type.save()
			success_dict['success_msg'] = "Successfully Created CurrencyType"
			return HttpResponse(json.dumps(success_dict), content_type='application/json')
			#messages.add_message(request, messages.SUCCESS, _('Successfully Created Industry'))
			
		else:
			error_dict = {}
			for error in form.errors:
				error_dict[error] = form.errors[ error]
			return HttpResponseBadRequest(json.dumps(error_dict))
	else:
		form = CurrencyTypeForm

		return render(request, 'customer/currency_type_add_partial.html', {'form':form,
							}
						)


@login_required
def currency_type_edit(request, id):
	success_dict={}
	currency_type = get_object_or_404(CurrencyType, id=id)
	if request.method == "POST":
		form = CurrencyTypeForm(request.POST, instance=currency_type)
		if form.is_valid():
			currency_type = form.save(commit=False)

			currency_type.save()
			success_dict['success_msg'] = "Successfully Edited CurrencyType"
			return HttpResponse(json.dumps(success_dict), content_type='application/json')
		else:
			error_dict={}
			for error in form.errors:
				error_dict[error] = form.errors[error]

			return HttpResponseBadRequest(json.dumps(error_dict))
	else:
		form = CurrencyTypeForm(instance=currency_type)
	return render(request, 'customer/currency_type_add_partial.html', {'form': form, 'is_edit_mode':True, 'id':id})

def export_leads_xls(request):
	if request.method=="POST":
		if request.POST.has_key("leads_start_date") and request.POST.has_key("leads_end_date"):
			start_date = request.POST.get('leads_start_date')
			end_date = request.POST.get('leads_end_date')

			response = HttpResponse(content_type='application/ms-excel')
			response['Content-Disposition'] = 'attachment; filename="Leads_from_%s_to_%s.xls"'%(start_date, end_date)

			wb = xlwt.Workbook(encoding='utf-8')
			ws = wb.add_sheet('Users')

			# Sheet header, first row
			row_num = 0

			font_style = xlwt.XFStyle()
			font_style.font.bold = True

			columns = ['title', 'description', 'contact_name', 'designation', 'email', 'phone', 'addressline1',
						'addressline2', 'city', 'state', 'country', 'zip_code', 'industry', 'services', 'requirement',
						'lead_source', 'sales_rep', 'other_lead_source', 'is_converted_to_customer',
						'lead_date', 'owner'
					]

			for col_num in range(len(columns)):
				ws.write(row_num, col_num, columns[col_num], font_style)

			# Sheet body, remaining rows
			font_style = xlwt.XFStyle()
			rows = Lead.objects.filter(lead_date__gte=start_date, lead_date__lte=end_date).values_list('title', 'description', 'contact_name', 'designation', 'email', 'phone', 'addressline1',
						'addressline2', 'city', 'state', 'country', 'zip_code', 'industry', 'services', 'requirement',
						'lead_source', 'sales_rep', 'other_lead_source', 'is_converted_to_customer',
						'lead_date', 'owner')
			for row in rows:
				row_num += 1
				for col_num in range(len(row)):
					ws.write(row_num, col_num, row[col_num], font_style)

			wb.save(response)
			return response

def export_leads_form(request):
	
	return render(request, 'customer/export_lead_partial.html', {})


def ImportWorkItem(request):
 
		# Handle form request
		success_dict= {}
		if request.method == 'POST':
			
			form = ImportLeadForm(request.POST, request.FILES)
			# success_dict['success_msg'] = "successfully uploded"
			# return HttpResponse(json.dumps(success_dict))
			print form
			if form.is_valid():
				# success_dict={}
				# Do CSV processing and create ProductKey recordss

				file = form.cleaned_data['file']
				fields, data_lines = csvimporter.handle_uploaded_file(file)
				print file
				print fields
				success_dict['success_msg'] = "Successfully uploded"
				print success_dict

			return redirect('sales_manager_dashboard')
				
		else:
			

			form =ImportLeadForm()
 
		return render(request, 'customer/ImportWorkItem.html', {'form':form},)		



