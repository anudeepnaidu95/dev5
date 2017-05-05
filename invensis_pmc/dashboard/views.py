import json
import datetime
import math
import itertools
from dateutil import rrule
from datetime import timedelta
from django.utils import timezone
from django.shortcuts import render
from django.shortcuts import render,render_to_response, get_object_or_404
from django.utils.translation import ugettext_lazy as _
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest
from django.forms.models import formset_factory, modelform_factory, modelformset_factory
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Count, Sum, Case, When, IntegerField
from django.db.models import Q
from django.http import JsonResponse
from customer.models import Lead
from invoice.models import Invoice
from models import DashboardSetup, QuerterRevenueSetup 
from dashboard import forms

from django.core.exceptions import ValidationError,MultipleObjectsReturned
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required
from inhouseapp.utils.decorators import group_required


@login_required
def stats_dashboard_list(request):
	if request.method == "POST":
		form = forms.DashboardSetupForm(request.POST or None)
		if form.is_valid():
			stats_dates = form.save(commit=False)
			start_date = form.cleaned_data.get('start_date')
			print "start_date", start_date
			end_date = form.cleaned_data.get('end_date')
			print "end_date", end_date
			stats_dates.save()
		else:
			error_dict={}
			for error in form.errors:
				error_dict[error] = form.errors[error]	
			return HttpResponseBadRequest(json.dumps(error_dict))
	else:
		N = 90
		date_N_days_ago = datetime.datetime.now() - datetime.timedelta(days=N)
		data = {'start_date':date_N_days_ago, 'end_date':datetime.datetime.now().date()}
		form = forms.DashboardSetupForm(initial=data)
	return render(request, 'stats_dashboard/stats_dashboard_list_partial.html', locals())


def leads_by_week_list_data(start_date, end_date):
	leads_by_week_list =[]
	week_date_lists = []
	print type(start_date)
	start_date_monday = (start_date - datetime.timedelta(days=start_date.weekday()))
	num_of_weeks = math.ceil((end_date - start_date_monday).days / 7.0)
	for i in range(int(num_of_weeks)):
		if end_date in week_date_lists:
			week_date_lists.append(week_date_lists[-1] - datetime.timedelta(days=7))
		else:
			week_date_lists.append(end_date)
	new_week_date_lists = week_date_lists.reverse()
	for i in range(int(num_of_weeks)):
		leads_by_week_dict = {}
		if i < int(num_of_weeks)-1:
			lead_values = Lead.objects.filter(lead_date__gte=week_date_lists[i],lead_date__lte=week_date_lists[i+1]).count()
			leads_by_week_dict["date"] = str(week_date_lists[i])
			leads_by_week_dict["value"] = lead_values
			leads_by_week_list.append(leads_by_week_dict)
		else:
			lead_values = Lead.objects.filter(lead_date__gte=week_date_lists[-2],lead_date__lte=week_date_lists[-1]).count()
			leads_by_week_dict["date"] = str(week_date_lists[-1])
			leads_by_week_dict["value"] = lead_values
			leads_by_week_list.append(leads_by_week_dict)

	return leads_by_week_list


@login_required
@csrf_exempt
def lead_enquires_stat(request):
	leads_by_week_list = []

	if request.is_ajax():
		s_y, s_m, s_d = request.POST.get('start_date').split('-')
		e_y, e_m, e_d = request.POST.get('end_date').split('-')		
		week_date_lists = []
		start_date = datetime.date(int(s_y), int(s_m), int(s_d))
		start_date_monday = (start_date - datetime.timedelta(days=start_date.weekday()))
		end_date = datetime.date(int(e_y), int(e_m), int(e_d))
		num_of_weeks = math.ceil((end_date - start_date_monday).days / 7.0)
		for i in range(int(num_of_weeks)):
			if end_date in week_date_lists:
				week_date_lists.append(week_date_lists[-1] - datetime.timedelta(days=7))
			else:
				week_date_lists.append(end_date)
		new_week_date_lists = week_date_lists.reverse()
		for i in range(int(num_of_weeks)):
			leads_by_week_dict = {}
			if i < int(num_of_weeks)-1:
				lead_values = Lead.objects.filter(lead_date__gte=week_date_lists[i],lead_date__lte=week_date_lists[i+1]).count()
				leads_by_week_dict["date"] = str(week_date_lists[i])
				leads_by_week_dict["value"] = lead_values
				leads_by_week_list.append(leads_by_week_dict)
			else:
				lead_values = Lead.objects.filter(lead_date__gte=week_date_lists[-2],lead_date__lte=week_date_lists[-1]).count()
				leads_by_week_dict["date"] = str(week_date_lists[-1])
				leads_by_week_dict["value"] = lead_values
				leads_by_week_list.append(leads_by_week_dict)

	# qtr_start_date = datetime.now() - datetime.timedelta(days=90)
	# qtr_end_date = datetime.now().date()
	# leads_by_week_list= leads_by_week_list_data(qtr_start_date,qtr_end_date)

	leads_by_status = Lead.objects.filter(latest_lead_status__in=['PROSPECTING','TRIAL','NEGOTIATING']).values_list('latest_lead_status').annotate(Count('id'))
	leads_ten_enquires = Lead.objects.values_list('title')[:10]
	leads_ten_won_enquires = Lead.objects.filter(latest_lead_status='WON').values_list('title')[:10]

	revenue_range_list = []
	revenue_range_dict = {}
	revenue_range = QuerterRevenueSetup.objects.get(id=1)
	revenue_range_dict['red_region'] = revenue_range.red_region
	revenue_range_dict['yellow_region'] = revenue_range.yellow_region
	revenue_range_dict['green_region'] = revenue_range.green_region
	total_invoice_amount = Invoice.objects.aggregate(Sum("total_amount")).values()[0]
	revenue_range_dict["total_amount"] = total_invoice_amount
	revenue_range_list.append(revenue_range_dict)

	s_date_y,s_date_m,s_date_d  = ((datetime.date.today() - datetime.timedelta(365)).isoformat()).split('-')
	one_year_back_date = datetime.date(int(s_date_y), int(s_date_m), int(s_date_d))
	all_months = list(rrule.rrule(rrule.MONTHLY, dtstart=one_year_back_date, until=datetime.datetime.today()))
	leads_by_month_list = []
	for curr_month in range(1, len(all_months)):
		all_months_data_dict = {}
		leads_won_month = Lead.objects.filter(latest_lead_status='WON', lead_date__month=all_months[curr_month].month).count()
		leads_lost_month = Lead.objects.filter(latest_lead_status='LOST', lead_date__month=all_months[curr_month].month).count()
		all_months_data_dict['date'] = str(all_months[curr_month].strftime("%m/%Y"))
		all_months_data_dict['won'] = leads_won_month
		all_months_data_dict['lost'] = leads_lost_month
		leads_by_month_list.append(all_months_data_dict)
	print "leads_by_week_list", leads_by_week_list
	return JsonResponse({
						"leads_by_status":list(leads_by_status),
						"leads_by_month_list":leads_by_month_list,
						"leads_ten_enquires":list(leads_ten_enquires), 
						"leads_ten_won_enquires":list(leads_ten_won_enquires),
						"revenue_range_list":list(revenue_range_list),
						"leads_by_week_list":leads_by_week_list

						},
					safe=False
					)

@login_required
def all_open_leads_list(request):

	open_leads_list = Lead.objects.exclude(latest_lead_status='WON')
	return render(request, 'stats_dashboard/all_open_leads_list_partial.html', 
					{'open_leads_list': open_leads_list}
				)


@login_required
def all_won_leads_list(request):

	won_leads_list = Lead.objects.filter(latest_lead_status='WON')
	return render(request, 'stats_dashboard/all_won_leads_list_partial.html', 
					{'won_leads_list': won_leads_list}
				)


@login_required
def revenue_setup_list(request):

	revenue_setup_list = QuerterRevenueSetup.objects.all()
	return render(request, 'stats_dashboard/revenue_setup_list_partial.html', 
					{'revenue_setup_list': revenue_setup_list}
				)

@login_required
def revenue_setup_add(request):
	form = forms.RevenueSetupForm(request.POST, None)
	if request.method == 'POST':
		if form.is_valid():
			indust = form.save(commit=False)
			indust.save()
			return HttpResponse('OK')			
		else:
			error_dict = {}
			for error in form.errors:
				error_dict[error] = form.errors[ error]
			return HttpResponseBadRequest(json.dumps(error_dict))
	else:
		form = forms.RevenueSetupForm()

		return render(request, 'stats_dashboard/revenue_setup_add_partial.html', {'form':form,})


@login_required
def revenue_setup_edit(request, id):
	revenue_setup = get_object_or_404(QuerterRevenueSetup, id=id)
	if request.method == "POST":
		form = forms.RevenueSetupForm(request.POST, instance=revenue_setup)
		if form.is_valid():
			revenue_setup = form.save(commit=False)
			revenue_setup.save()

			return HttpResponse('ok ')
		else:
			error_dict={}
			for error in form.errors:
				error_dict[error] = form.errors[error]

			return HttpResponseBadRequest(json.dumps(error_dict))
	else:
		form = forms.RevenueSetupForm(instance=revenue_setup)
	return render(request, 'stats_dashboard/revenue_setup_add_partial.html', {'form': form, 'is_edit_mode':True, 'id':id})


@login_required
@group_required('management', login_url='/account/login/', raise_exception=True)
def management_dashboard(request):
	if request.method == "POST":
		form = forms.DashboardSetupForm(request.POST or None)
		if form.is_valid():
			stats_dates = form.save(commit=False)
			start_date = form.cleaned_data.get('start_date')
			print "start_date", start_date
			end_date = form.cleaned_data.get('end_date')
			print "end_date", end_date
			stats_dates.save()
		else:
			error_dict={}
			for error in form.errors:
				error_dict[error] = form.errors[error]	
			return HttpResponseBadRequest(json.dumps(error_dict))
	else:
		N = 90
		date_N_days_ago = datetime.datetime.now() - datetime.timedelta(days=N)
		data = {'start_date':date_N_days_ago, 'end_date':datetime.datetime.now().date()}
		form = forms.DashboardSetupForm(initial=data)
	return render(request, 'stats_dashboard/stats_dashboard_list_partial.html', locals())