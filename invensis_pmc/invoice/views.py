import json
import time, timeit
import uuid
import collections
import mimetypes
import cStringIO as StringIO
from cgi import escape
from django.utils.encoding import smart_str
from datetime import datetime, timedelta, date
from django.shortcuts import render
from django.db import IntegrityError
from django.db.models import Q
from django.shortcuts import render,render_to_response, get_object_or_404
from django.utils.translation import ugettext_lazy as _
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest
from django.forms.models import formset_factory, modelform_factory, modelformset_factory
from django.contrib.auth.decorators import login_required
from reportlab.pdfgen import canvas
from xhtml2pdf import pisa
from django.template.loader import get_template
from django.template import Context
from inhouseapp import settings
from invoice import models, forms ,form1
from customer.models import Customer
from project.models import Service, Task, TaskResourcePlan, LeadTask, StaffTask,Project
from employee.models import Employee



@login_required
def invoice_list(request):

	invoices = None
	cust_dict = collections.OrderedDict()
	invoice_dict = collections.OrderedDict()
	if request.user.groups.filter(name__in=['management']).exists():
		customers = Customer.objects.all()

		for customer in customers:
			services = Service.objects.filter(customer=customer).select_related('operations_manager')
			print "services manager", services

		if customers:
			invoice_payment_lists = []
			invoices = models.Invoice.objects.filter(customer__in=customers).exclude(is_final=True)
			invoice_payments = models.PaymentReconciliation.objects.filter(invoice__in=invoices)
			for customer in customers:
				cust_dict[customer.id] = (customer, [])

			for invoice_payment in invoice_payments:
				invoice_payment_lists.append(invoice_payment.payment_amount)
			
			for invoice in invoices:
				invoice_dict[invoice.id] = (invoice, [])

			for invoice in invoices:
				if invoice.customer_id in cust_dict:
					cust_tuple = cust_dict[invoice.customer_id]
					cust_tuple[1].append(invoice)


			payment_amt = models.PaymentReconciliation.objects.filter(invoice__in=invoices)
			for payment in payment_amt:
				if payment.invoice_id in invoice_dict:
					payment_tuple = invoice_dict[payment.invoice_id]
					payment_tuple[1].append(payment.payment_amount)
			print "invoice_dict", invoice_dict

			print cust_dict

		return render(request, 'invoice/invoice_list_partial.html',locals())

# operation manager div
	elif request.user.groups.filter(name__in=['operations manager']).exists():

		emp_owner = Employee.objects.filter(user__username = request.user)
		
		services = Service.objects.filter(operations_manager=emp_owner)
		

		customers  = Customer.objects.filter(service__in = services)
			
		for customer in customers:
			
			services = Service.objects.filter(customer=customer).filter(operations_manager__user=request.user)
			
			for service in services:
				

				if customers:
					invoice_payment_lists = []
					invoices = models.Invoice.objects.filter(customer__in=customers).exclude(is_final=True)
					invoice_payments = models.PaymentReconciliation.objects.filter(invoice__in=invoices)
					for customer in customers:
						cust_dict[customer.id] = (customer, [])

					for invoice_payment in invoice_payments:
						invoice_payment_lists.append(invoice_payment.payment_amount)
					
					for invoice in invoices:
						invoice_dict[invoice.id] = (invoice, [])

					for invoice in invoices:
						if invoice.customer_id in cust_dict:
							cust_tuple = cust_dict[invoice.customer_id]
							cust_tuple[1].append(invoice)
							
					payment_amt = models.PaymentReconciliation.objects.filter(invoice__in=invoices)
					for payment in payment_amt:
						if payment.invoice_id in invoice_dict:
							payment_tuple = invoice_dict[payment.invoice_id]
							payment_tuple[1].append(payment.payment_amount)
					print "invoice_dict", invoice_dict

					print cust_dict

				return render(request, 'invoice/invoice_list_partial.html',locals())

def final_invoice_list(request):
	final_invoices = models.Invoice.objects.filter(is_final=True).order_by('id')

	return render(request, 'invoice/final_invoice_list_partial.html',locals())

def invoice_view_details(request):

	invoices = None
	cust_dict = collections.OrderedDict()
	invoice_dict = collections.OrderedDict()
	if request.user.groups.filter(name__in=['management']).exists():
		customers = Customer.objects.all()

		for customer in customers:
			services = Service.objects.filter(customer=customer).select_related('operations_manager')
			print "services manager", services

		if customers:
			invoice_payment_lists = []
			invoices = models.Invoice.objects.filter(customer__in=customers).exclude(is_final=True)
			invoice_payments = models.PaymentReconciliation.objects.filter(invoice__in=invoices)
			for customer in customers:
				cust_dict[customer.id] = (customer, [])

			for invoice_payment in invoice_payments:
				invoice_payment_lists.append(invoice_payment.payment_amount)
			
			for invoice in invoices:
				invoice_dict[invoice.id] = (invoice, [])

			for invoice in invoices:
				if invoice.customer_id in cust_dict:
					cust_tuple = cust_dict[invoice.customer_id]
					cust_tuple[1].append(invoice)


			payment_amt = models.PaymentReconciliation.objects.filter(invoice__in=invoices)
			for payment in payment_amt:
				if payment.invoice_id in invoice_dict:
					payment_tuple = invoice_dict[payment.invoice_id]
					payment_tuple[1].append(payment.payment_amount)
			print "invoice_dict", invoice_dict

			print cust_dict

		return render(request, 'invoice/invoice_view_details.html',locals())

# operation manager div
	elif request.user.groups.filter(name__in=['operations manager']).exists():

		emp_owner = Employee.objects.filter(user__username = request.user)
		
		services = Service.objects.filter(operations_manager=emp_owner)
		

		customers  = Customer.objects.filter(service__in = services)
			
		for customer in customers:
			
			services = Service.objects.filter(customer=customer).filter(operations_manager__user=request.user)
			
			for service in services:
				

				if customers:
					invoice_payment_lists = []
					invoices = models.Invoice.objects.filter(customer__in=customers).exclude(is_final=True)
					invoice_payments = models.PaymentReconciliation.objects.filter(invoice__in=invoices)
					for customer in customers:
						cust_dict[customer.id] = (customer, [])

					for invoice_payment in invoice_payments:
						invoice_payment_lists.append(invoice_payment.payment_amount)
					
					for invoice in invoices:
						invoice_dict[invoice.id] = (invoice, [])

					for invoice in invoices:
						if invoice.customer_id in cust_dict:
							cust_tuple = cust_dict[invoice.customer_id]
							cust_tuple[1].append(invoice)
							
					payment_amt = models.PaymentReconciliation.objects.filter(invoice__in=invoices)
					for payment in payment_amt:
						if payment.invoice_id in invoice_dict:
							payment_tuple = invoice_dict[payment.invoice_id]
							payment_tuple[1].append(payment.payment_amount)
					print "invoice_dict", invoice_dict

					print cust_dict

		return render(request, 'invoice/invoice_view_details.html',locals())

def generate_invoice_line_items(customer_id, start_date, end_date):
	if customer_id:
		customer = Customer.objects.get(pk=customer_id)
	else:
		customer = None
	cust_projects = Service.objects.filter(customer=customer)
	cust_projects_dict = dict([(project.id, project) for project in cust_projects])
	service_invoice_list = []
	service_invoice_dict = {}
	custom_error_dict = {}
	tasks_txs_list = []
	is_tasks = True
	is_inv_exist = False
	existing_invoices =[inv.end for inv in models.Invoice.objects.filter(customer_id=customer_id)]
	for existing_date in existing_invoices:
		inv_existed_date  = str(existing_date).split(" ")[0]
		if str(start_date) <= inv_existed_date:
			is_inv_exist = True

	if not is_inv_exist:
		for service in cust_projects:
			print "Service", service
			print "pricing", service.amount_per_billing_type

			billing_type = service.billing_type
			number_of_resources = service.number_of_resources
			all_tasks = Task.objects.filter(service =service, start__gte=start_date, end__lte=end_date) 		
			tasks_dict = dict([(task.id, task) for task in all_tasks])
			for task in all_tasks:
				if task.service_id in cust_projects_dict:
					tasks_txs_list.append(task.no_of_txs)
			task_resource_plans = TaskResourcePlan.objects.filter(task__in =all_tasks)
			task_resource_plans_list = []
			for task_resource in task_resource_plans:
				if  task_resource.task_id in tasks_dict:
					task_resource_plans_list.append(task_resource.number_of_resources)

			lead_tasks = LeadTask.objects.filter(task__in=all_tasks)
			lead_tasks_dict = dict([(lead_task.id, lead_task) for lead_task in lead_tasks])
			staff_tasks = StaffTask.objects.filter(lead_task__in=lead_tasks, status='completed')
			no_of_staff_tasks_completed = staff_tasks.count()
			staff_tasks_dict = dict([(staff_task.id, staff_task) for staff_task in staff_tasks])

			staff_task_time_in_min_lists = []
			service_line_items_list = []
			for staffTask in staff_tasks:
				service_line_item_dict = {}
				#convert staff task time_in_min to seconds.
				h,m,s = staffTask.time_in_min.split(':')
				time_in_sec = int(h) * 3600 + int(m) * 60 + int(s)
				staff_task_time_in_min_lists.append(time_in_sec)

				lead_task = LeadTask.objects.get(id=staffTask.lead_task_id)
				task = Task.objects.get(id=lead_task.task_id)
				service_line_item_dict['task'] = task.title
				service_line_item_dict['lead_task'] = lead_task.id
				service_line_item_dict['staff_task'] = staffTask.filename
				service_line_item_dict['staff_task_id'] = staffTask.id				
				service_line_item_dict['staff'] = staffTask.staff.name
				service_line_item_dict['filename'] = staffTask.filename
				service_line_item_dict['no_of_txs'] = staffTask.no_of_txs
				service_line_item_dict['time_in_min'] = staffTask.time_in_min		
				#print service_line_item_dict
				service_line_items_list.append(service_line_item_dict)
			total_tasks_time = sum(staff_task_time_in_min_lists)
			total_time_in_hr = total_tasks_time/3600
			print "total timeeeeeeeeeee",total_time_in_hr


			if billing_type == 'per_fte':
				total_amount = service.amount_per_billing_type * number_of_resources
			elif billing_type == 'per_hour':
				total_amount = service.amount_per_billing_type * total_time_in_hr
			elif billing_type == 'per_tx':
				total_amount = service.amount_per_billing_type * sum(tasks_txs_list)

			if all_tasks:
				total_transactions = int(sum(tasks_txs_list))
				service_name = service.title
				service_invoice_dict = {}
				service_invoice_dict['service_id'] = service.id
				service_invoice_dict['service'] = service_name
				service_invoice_dict['billing_type'] = billing_type
				service_invoice_dict['no_of_txs'] = total_transactions
				service_invoice_dict['no_of_resources'] = service.number_of_resources
				service_invoice_dict['no_of_working_days'] = service.workweek_days
				service_invoice_dict['no_of_hours'] = total_time_in_hr
				service_invoice_dict['pricing'] = float(service.amount_per_billing_type)
				service_invoice_dict['invoice_amount'] = float(total_amount)

				service_invoice_dict['invoice_line_items'] = service_line_items_list
				service_invoice_list.append(service_invoice_dict)
			else:		
				is_tasks = False
				custom_error_dict['error'] = "There is no tasks in the selected date range"		
		if is_tasks:
			return service_invoice_list
		else:
			return custom_error_dict
	else:
		custom_error_dict['error'] = "Invoice with Starting date is generated, Please recheck Start Date with existing Invoices"
		return custom_error_dict

def generate_invoice(request, customer_id=None):
	customer = get_object_or_404(Customer, pk=customer_id)
	if request.is_ajax():
		start_date = request.POST.get('start_date')
		end_date = request.POST.get('end_date')
		if customer.last_invoice_no:
			service_invoice_list = generate_invoice_line_items(customer_id, start_date, end_date)
			return HttpResponse(json.dumps(service_invoice_list), content_type='application/json')
		else:
			custom_error_dict = {}
			custom_error_dict['error'] = "Please Add Customer Last invoice number in customer details to generate invoice"
			return HttpResponse(json.dumps(custom_error_dict), content_type="application/json")	

@login_required
def invoice_add(request, customer_id=None):

	success_dict = {}

	if customer_id:
		customer = Customer.objects.get(pk=customer_id)
	else:
		customer = None
	cust_last_invoice_no = customer.last_invoice_no
	cust_invoice_format = customer.invoice_format
	cust_invoice_company_name = customer.company_name_invoice
	if request.method == 'POST': 
		form = forms.InvoiceForm(request.POST, request=request)
		if form.is_valid():
			invoice = form.save(commit=False)
			start_date = form.cleaned_data.get('start')
			end_date = form.cleaned_data.get('end')
			print start_date,end_date
			service_invoices_list = generate_invoice_line_items(customer_id,start_date,end_date)		
			#try:
				#with transaction.atomic():
			if cust_last_invoice_no:
				cust_last_invoice_no += 1
				customer.last_invoice_no = cust_last_invoice_no
				customer.save()
				year = str(start_date).split('-')[0]
				year_format = "%s-%s"%(year, int(year)+1)
				invoice_number_format = "%s/%s/%s/%s"%(customer.invoice_format, customer.title,str(year_format),cust_last_invoice_no)
				emp_mgmt = Employee.objects.get(user__username=request.user)
				invoice = models.Invoice(
									invoice_no = invoice_number_format,
									date = date.today(),
									customer = customer,
									management_employee = emp_mgmt,
									start = start_date,
									end = end_date
								)
				invoice.save()
				print len(service_invoices_list)
				invoice_amount_list = []
				for x in range(len(service_invoices_list)):
					print service_invoices_list[x]
					service_invoice = models.ServiceInvoice(
										invoice = invoice,
										service = Service.objects.get(title=service_invoices_list[x]['service']),
										billing_type = service_invoices_list[x]['billing_type'],
										pricing = service_invoices_list[x]['pricing'],
										invoice_amount = service_invoices_list[x]['invoice_amount'],
										no_of_txs = service_invoices_list[x]['no_of_txs'],
										no_of_resources = service_invoices_list[x]['no_of_resources'],
										no_of_working_days = service_invoices_list[x]['no_of_working_days'],
										no_of_hours = service_invoices_list[x]['no_of_hours'],
								)
					invoice_amount_list.append(service_invoices_list[x]['invoice_amount'])
					service_invoice.save()
					for y in range(len(service_invoices_list[x]['invoice_line_items'])):
						service_invoice_line_items = models.InvoiceLineItem(
														service_inv = service_invoice,
														task = Task.objects.get(title=service_invoices_list[x]['invoice_line_items'][y]['task']),
														lead_task = LeadTask.objects.get(id=service_invoices_list[x]['invoice_line_items'][y]['lead_task']),
														staff_task = StaffTask.objects.get(id=service_invoices_list[x]['invoice_line_items'][y]['staff_task_id']),
														staff = Employee.objects.get(name=service_invoices_list[x]['invoice_line_items'][y]['staff']),	
														filename = service_invoices_list[x]['invoice_line_items'][y]['filename'],
														no_of_txs = service_invoices_list[x]['invoice_line_items'][y]['no_of_txs'],
														time_in_min = service_invoices_list[x]['invoice_line_items'][y]['time_in_min'],

													)
						service_invoice_line_items.save()
			else:
				custom_error_dict = {}
				errors_dict = {}
				custom_error_dict['error'] = "Please Add Customer Last invoice in customer details to generate invoice"
				errors_dict['custom_error_dict'] = custom_error_dict
				return HttpResponseBadRequest(json.dumps(errors_dict), content_type="application/json")	


			invoice.total_amount = sum(invoice_amount_list)
			invoice.save()
			success_dict['success_msg'] = "Successfully generated customer invoice"
			return HttpResponse(json.dumps(success_dict), content_type="application/json")

 
		else:
			error_dict = {}
			for error in form.errors:
				error_dict[error] = form.errors[error]
			return HttpResponseBadRequest(json.dumps(error_dict))
	else:
		form = forms.InvoiceForm(request=request)

		return render(request, 'invoice/invoice_add_partial.html', {
			'form':form, 
			'customer_id':customer_id,
		}
	)


@login_required
def invoice_edit(request, invoice_id):
	success_dict={}
	invoice = get_object_or_404(models.Invoice, id=invoice_id)
	ServiceInvoiceFormset   = modelformset_factory(models.ServiceInvoice, forms.ServiceInvoiceForm, extra=0, exclude=('invoice',))

	service_invoice_formset = ServiceInvoiceFormset(queryset=models.ServiceInvoice.objects.filter(invoice=invoice), prefix='service-invoice') 
	#print "service_invoice_formset", service_invoice_formset
	if request.method == "POST":
		form = forms.InvoiceForm(request.POST,request=request, instance=invoice)
		# if invoice:
		# 	service_invoices = models.ServiceInvoice.objects.filter(invoice=invoice).delete()

		service_invoice_formset = ServiceInvoiceFormset(request.POST or None,queryset=models.ServiceInvoice.objects.filter(invoice=invoice), prefix='service-invoice') 
		if form.is_valid() and  service_invoice_formset.is_valid():
			invoice = form.save(commit=False)
			start_date = form.cleaned_data.get('start')
			end_date = form.cleaned_data.get('end')
			#service_invoices_list = generate_invoice_line_items(invoice.customer_id,start_date,end_date)
			# try:
			# 	with transaction.atomic():
			#print "service_invoices_list", service_invoices_list
			is_final = form.cleaned_data.get('is_final', None)
			invoice.date = date.today()
			invoice.management_employee = Employee.objects.get(user__username=request.user)
			invoice.start = start_date
			invoice.end = end_date
			if is_final:
				invoice.is_final = is_final
			total_amount_list = []
			for service_invoice_form in service_invoice_formset:
				service_invoice_instance = service_invoice_form.save(commit=False)
				service_invoice_instance.invoice = invoice
				total_amount = service_invoice_form.cleaned_data.get("invoice_amount")
				total_amount_list.append(float(total_amount))
				service_invoice_instance.save()
			invoice.total_amount = sum(total_amount_list)
			invoice.save()

			success_dict = {}
			success_dict['success_msg'] = "Successfully updated/edited customer invoice"
			return HttpResponse(json.dumps(success_dict), content_type="application/json")

		else:
			error_dict={}
			form_error_dict = {}
			service_invoice_error_dict = {}

			for error in form.errors:
				form_error_dict[error] = form.errors[error]

			for f1 in service_invoice_formset:
				for error in f1.errors:
					#print "error", error
					e = f1.errors[error]
					service_invoice_error_dict[error] = unicode(e)
			error_dict['form_error_dict'] = form_error_dict
			error_dict['service_invoice_error_dict'] = service_invoice_error_dict

			return HttpResponseBadRequest(json.dumps(error_dict), content_type="application/json")
	else:
		form = forms.InvoiceForm(request=request,instance=invoice)
		service_invoice_formset = service_invoice_formset
		customer_id = invoice.customer_id
		is_edit_mode = True
		#service_invoices = models.ServiceInvoice.objects.filter(invoice=invoice)
		return render(request, 'invoice/invoice_add_partial.html', locals())


@login_required
def line_item_list(request, service_id):
	service_name = get_object_or_404(Service, id=service_id)
	start_date = request.POST.get('start_date')
	end_date = request.POST.get('end_date')
	service_tasks = Task.objects.filter(service=service_name, start__gte=start_date, end__lte=end_date)
	service_lead_tasks = LeadTask.objects.filter(task__in=service_tasks)
	service_line_items = StaffTask.objects.filter(lead_task__in=service_lead_tasks) 

	return render(request, 'invoice/invoice_line_item_list.html', locals())		

@login_required
def service_line_item_list(request, service_inv_id, service_id=None):
	if service_inv_id:
		service_invoice_name = get_object_or_404(models.ServiceInvoice, id=service_inv_id)
		service_line_items  = models.InvoiceLineItem.objects.filter(service_inv=service_invoice_name)
		
	return render(request, 'invoice/invoice_line_item_list.html', locals())	

@login_required
def payments_list(request, invoice_id):
	payments_lists = models.PaymentReconciliation.objects.filter(invoice_id=invoice_id)
	return render(request, "invoice/payments_list_partial.html", locals())

@login_required
def payment_list_and_add(request, invoice_id):
	success_dict={}
	payments_dict = {}
	payments_list = []
	invoice = get_object_or_404(models.Invoice, id=invoice_id)
	payments_lists = models.PaymentReconciliation.objects.filter(invoice_id=invoice_id)

	form = forms.PaymentForm(request.POST)
	if request.method == 'POST':
		if form.is_valid():
			payment = form.save(commit=False)
			payment.invoice = invoice
			payment.save()
			paymet_detail = models.PaymentReconciliation.objects.get(id=payment.id) 
			company_bank_acc = models.CompanyBankAccount.objects.get(id=payment.bank_account_id )
			payments_dict['id'] = payment.id 
			payments_dict['payment_date'] = str(payment.payment_date)
			payments_dict['payment_amount'] = float(payment.payment_amount)
			payments_dict['cheque_no'] = payment.cheque_no 
			payments_dict['transaction_id'] = payment.transaction_id 
			payments_dict['email_id'] = payment.email_id 
			payments_dict['mode_of_payment'] = payment.mode_of_payment 
			payments_dict['bank_account'] = str(company_bank_acc.bank_name)
			payments_list.append(payments_dict)

			return HttpResponse(json.dumps(payments_dict), content_type="application/json")

		else:
			error_dict={}
			for error in form.errors:
				error_dict[error] = form.errors[error]	
			return HttpResponseBadRequest(json.dumps(error_dict))
	else:
		form = forms.PaymentForm()
		payments_lists = models.PaymentReconciliation.objects.filter(invoice_id=invoice_id)

	return render(request, 'invoice/payment_list_and_add.html', locals())		


def render_to_pdf(template_src, context_dict):
	template = get_template(template_src)
	context = Context(context_dict)
	html  = template.render(context)
	result = StringIO.StringIO()
	pdf = pisa.pisaDocument(StringIO.StringIO(html.encode("UTF-8")), result)
	if not pdf.err:
		response = HttpResponse(result.getvalue(), content_type='application/pdf')
		#response['Content-Disposition'] = 'attachment; filename=%s'%smart_str(context['file_name'])
		return response
	return HttpResponse('We had some errors<pre>%s</pre>' % escape(html))


def invoice_generator(request, invoice_id):
	invoice_list = models.Invoice.objects.get(id=invoice_id)
	service_invoices = models.ServiceInvoice.objects.filter(invoice=invoice_list)
	invoice_setup = models.InvoiceSetup.objects.get(id=1)
	payment_term = models.PaymentTerms.objects.filter(invoice_setup=invoice_setup)
	wire_tranfer_info = models.WireTransferInfo.objects.get(invoice_setup=invoice_setup)
	customer=Customer.objects.get(id=invoice_list.customer_id)
	month_year = str(invoice_list.start).split('-')
	filename = "%s_Invoice_%s_%s-Invensis"%(customer.title, month_year[1], month_year[0])

	context_dict = {
                'pagesize':'A4',
                'invoice_list': invoice_list,
                'service_invoices':service_invoices,
                'invoice_setup':invoice_setup,
                'payment_term':payment_term,
                'wire_tranfer_info':wire_tranfer_info,
                'customer':customer,
                'file_name':filename
            }
	try:
		payment_modes = models.PaymentModeSetup.objects.get(currency=customer.currency)
		if payment_modes:
			cheque_setup_mode = models.ChequeSetup.objects.get(payment_mode=payment_modes)
			wiretransfer_setup_mode = models.WiretransferSetup.objects.get(payment_mode=payment_modes)
			paypal_setup_mode = models.PaypalSetup.objects.get(payment_mode=payment_modes)

			if cheque_setup_mode.is_applicable:
				context_dict['cheque_setup_mode'] = cheque_setup_mode
			if wiretransfer_setup_mode.is_applicable:
				context_dict['wiretransfer_setup_mode'] = wiretransfer_setup_mode
			if paypal_setup_mode.is_applicable:
				context_dict['paypal_setup_mode'] = paypal_setup_mode
				payble_amount =  invoice_list.total_amount + (invoice_list.total_amount * paypal_setup_mode.surcharge_percent)/100
				context_dict['payble_amount'] = payble_amount

	except models.PaymentModeSetup.DoesNotExist:
		pass
	
	return render_to_pdf(
 			'invoice/invoice_pdf.html',
 			context_dict
        )


@login_required
def invoice_setup_list(request):

	setup_lists = models.InvoiceSetup.objects.all()
	return render(request, 'invoice/invoice_setup_list_partial.html', 
					{'setup_lists': setup_lists}
				)


@login_required
def invoice_setup_add(request):
	success_dict={}
	form = form1.InvoiceSetupForm(request.POST)
	PaymentTermsFormset = formset_factory(form1.PaymentTermsForm)
	wireform = form1.WireTransferInfoForm(request.POST)
	
	if request.method == 'POST':
		form = form1.InvoiceSetupForm(request.POST or None)
		wireform = form1.WireTransferInfoForm(request.POST)
		paymentterms_formset = PaymentTermsFormset(request.POST or None)

		for payment_term_form in paymentterms_formset.deleted_forms:
			payment_term_form_instance = payment_term_form.instance
			if payment_term_form_instance.pk:
				payment_term_form_instance.delete()
					
		if form.is_valid() and paymentterms_formset.is_valid() and wireform.is_valid():
			invoice_setup = form.save(commit=False)
			invoice_setup.save()
			wireform_instance = wireform.save(commit=False)
			wireform_instance.invoice_setup = invoice_setup	
			wireform_instance.save()
	
			for payment_term_form in paymentterms_formset:
				if payment_term_form not in [deleted_form for deleted_form in paymentterms_formset.deleted_forms]:
					payment_term_formInstance = payment_term_form.save(commit=False)
					payment_term_formInstance.invoice_setup = invoice_setup
					#payment_term_formInstance.save()
					terms = payment_term_form.cleaned_data.get('terms')

					if terms not in ['', None]:
						payment_term_formInstance.save()
			
			success_dict['success_msg'] = "Successfully Created InvoiceSetup"
			return HttpResponse(json.dumps(success_dict), content_type='application/json')
		else:
			error_dict={}
			wiretransfer_info_form_error_dict={}
			paymentterms_formset_error_dict={}
		
			for error in form.errors:
				error_dict[error] = form.errors[error]
			for error in wireform.errors:
				error_dict[error] = wireform.errors[error]
				
				error_dict['wiretransfer_info_form_error_dict'] = wiretransfer_info_form_error_dict
				error_dict['paymentterms_formset_error_dict'] = paymentterms_formset_error_dict
			return HttpResponseBadRequest(json.dumps(error_dict))
	else:
		form = form1.InvoiceSetupForm()
		wireform = form1.WireTransferInfoForm()
		paymentterms_formset = PaymentTermsFormset()
	return render(request, 'invoice/invoice_setup_add_partial.html', locals())

		
@login_required
def invoice_setup_edit(request, id):
	success_dict={}
	invoice_setup = get_object_or_404(models.InvoiceSetup, id=id)
	invoice_setup_wire = get_object_or_404(models.WireTransferInfo, invoice_setup=invoice_setup)
	PaymentTermsFormset = modelformset_factory(models.PaymentTerms, form1.PaymentTermsForm,exclude=('invoice_setup',))

	
	if request.method == "POST":
		form = form1.InvoiceSetupForm(request.POST, instance=invoice_setup)
		wireform = form1.WireTransferInfoForm(request.POST , instance=invoice_setup_wire)
		paymentterms_formset = PaymentTermsFormset(request.POST ,queryset = models.PaymentTerms.objects.filter(invoice_setup=invoice_setup))
		
		for payment_term_form in paymentterms_formset.deleted_forms:
			payment_term_form_instance = payment_term_form.instance
			if payment_term_form_instance.pk:
				payment_term_form_instance.delete()

				
		if form.is_valid() and paymentterms_formset.is_valid() and wireform.is_valid():
			invoice_setup = form.save(commit=False)
			invoice_setup.save()
			wireform_instance = wireform.save(commit=False)
			wireform_instance.invoice_setup = invoice_setup	
			wireform_instance.save()
				
			
			for payment_term_form in paymentterms_formset:
				if payment_term_form not in [deleted_form for deleted_form in paymentterms_formset.deleted_forms]:
					payment_term_formInstance = payment_term_form.save(commit=False)
					payment_term_formInstance.invoice_setup = invoice_setup
					#payment_term_formInstance.save()
					terms = payment_term_form.cleaned_data.get('terms')

					if terms not in ['', None]:
						payment_term_formInstance.save()
			
			success_dict['success_msg'] = "Successfully Edit InvoiceSetup"
			return HttpResponse(json.dumps(success_dict), content_type='application/json')
		else:
			error_dict={}
			paymentterms_formset_error_dict={}
			wiretransfer_info_form_error_dict={}
			for error in form.errors:
				error_dict[error] = form.errors[error]
			for error in wireform.errors:
				error_dict[error] = wireform.errors[error]
				error_dict['paymentterms_formset_error_dict'] = paymentterms_formset_error_dict
				error_dict['wiretransfer_info_form_error_dict'] = wiretransfer_info_form_error_dict
			return HttpResponseBadRequest(json.dumps(error_dict))
	else:
		form = form1.InvoiceSetupForm(instance=invoice_setup)
		wireform = form1.WireTransferInfoForm(instance=invoice_setup_wire)
		paymentterms_formset = PaymentTermsFormset(queryset=models.PaymentTerms.objects.filter(invoice_setup=invoice_setup),)
	return render(request, 'invoice/invoice_setup_add_partial.html', {'form': form, 'wireform':wireform,'paymentterms_formset':paymentterms_formset,'is_edit_mode' : True , 'id' : id,})


@login_required
def bank_details_list(request):

	bank_details_lists = models.CompanyBankAccount.objects.all()
	return render(request, 'invoice/bank_details_list_partial.html', 
					{'bank_details_lists': bank_details_lists}
				)


@login_required
def bank_details_add(request):
	form = form1.BankDetailsForm(request.POST)
	if request.method == 'POST':
		if form.is_valid():
			bank_details = form.save(commit=False)
			bank_details.save()
			success_dict['success_msg'] = "Successfully Created BankDetails"
			return HttpResponse(json.dumps(success_dict), content_type='application/json')
		else:
			error_dict={}
			for error in form.errors:
				error_dict[error] = form.errors[error]
				
			return HttpResponseBadRequest(json.dumps(error_dict))
	else:
		form = form1.BankDetailsForm()

	return render(request, 'invoice/bank_details_add_partial.html', locals())


@login_required
def bank_details_edit(request, id):
	bank_details = get_object_or_404(models.CompanyBankAccount, id=id)
	if request.method == "POST":
		form = form1.BankDetailsForm(request.POST, instance=bank_details)
		if form.is_valid():
			bank_details = form.save(commit=False)
			bank_details.save()

			success_dict['success_msg'] = "Successfully Edit BankDetails"
			return HttpResponse(json.dumps(success_dict), content_type='application/json')
		else:
			error_dict={}
			for error in form.errors:
				error_dict[error] = form.errors[error]
				
			return HttpResponseBadRequest(json.dumps(error_dict))
	else:
		form = form1.BankDetailsForm(instance=bank_details)
	return render(request, 'invoice/bank_details_add_partial.html', {'form': form, 'is_edit_mode' : True , 'id' : id,})



@login_required
def payment_modes_list(request):

	payment_modes_lists = models.PaymentModeSetup.objects.all()
	return render(request, 'invoice/payment_modes_list_partial.html', 
					{'payment_modes_lists': payment_modes_lists}
				)


@login_required
def payment_mode_add(request):

	if request.method == 'POST':
		form = forms.PaymentModeSetupForm(request.POST)
		cheque_setup_form = forms.ChequeSetupForm(request.POST or None)
		wiretransefer_setup_form = forms.WiretransferSetupForm(request.POST or None)
		paypal_setup_form = forms.PaypalSetupForm(request.POST or None)

		if form.is_valid() and cheque_setup_form.is_valid() and wiretransefer_setup_form.is_valid() and paypal_setup_form.is_valid():
			payment_mode = form.save(commit=False)
			payment_mode.save()
		
			cheque_setup = cheque_setup_form.save(commit=False)
			cheque_setup.payment_mode = payment_mode
			cheque_setup.save()

			wiretransefer_setup = wiretransefer_setup_form.save(commit=False)
			wiretransefer_setup.payment_mode = payment_mode
			wiretransefer_setup.save()

			paypal_setup = paypal_setup_form.save(commit=False)
			paypal_setup.payment_mode = payment_mode
			paypal_setup.save()
			success_dict ={}
			success_dict['success_msg'] = "Successfully Added Payment Setup"
			return HttpResponse(json.dumps(success_dict), content_type='application/json')
		else:
			error_dict={}
			form_error_dict = {}
			cheque_setup_form_error_dict = {}
			wiretransefer_setup_form_errors = {}
			paypal_setup_form_errors = {}

			for error in form.errors:
				form_error_dict[error] = form.errors[error]
				
			for error in cheque_setup_form.errors:
				e = cheque_setup_form.errors[error]
				cheque_setup_form_error_dict[error] = unicode(e)

			for error in wiretransefer_setup_form.errors:
				e = wiretransefer_setup_form.errors[error]
				wiretransefer_setup_form_errors[error] = unicode(e)

			for error in paypal_setup_form.errors:
				e = paypal_setup_form.errors[error]
				paypal_setup_form_errors[error] = unicode(e)

			error_dict['form_error_dict'] = form_error_dict
			error_dict['cheque_setup_form_error_dict'] = cheque_setup_form_error_dict
			error_dict['wiretransefer_setup_form_errors'] = wiretransefer_setup_form_errors
			error_dict['paypal_setup_form_errors'] = paypal_setup_form_errors
			return HttpResponseBadRequest(json.dumps(error_dict), content_type='application/json')
	else:
		form = forms.PaymentModeSetupForm()
		cheque_setup_form = forms.ChequeSetupForm()
		wiretransefer_setup_form = forms.WiretransferSetupForm()
		paypal_setup_form = forms.PaypalSetupForm()

	return render(request, 'invoice/payment_mode_add_partial.html', locals())


@login_required
def payment_mode_edit(request, id):
	payment_mode = get_object_or_404(models.PaymentModeSetup, id=id)
	cheque_setup = models.ChequeSetup.objects.get(payment_mode=payment_mode)
	paypal_setup = models.PaypalSetup.objects.get(payment_mode=payment_mode)
	wiretransefer_setup = models.WiretransferSetup.objects.get(payment_mode=payment_mode)

	if request.method == "POST":
		form = forms.PaymentModeSetupForm(request.POST, instance=payment_mode)
		cheque_setup_form = forms.ChequeSetupForm(request.POST or None, instance=cheque_setup)
		wiretransefer_setup_form = forms.WiretransferSetupForm(request.POST or None, instance=wiretransefer_setup)
		paypal_setup_form = forms.PaypalSetupForm(request.POST or None, instance=paypal_setup)

		if form.is_valid() and cheque_setup_form.is_valid() and wiretransefer_setup_form.is_valid() and paypal_setup_form.is_valid():
			payment_mode = form.save(commit=False)
			payment_mode.save()
		
			cheque_setup = cheque_setup_form.save(commit=False)
			cheque_setup.payment_mode = payment_mode
			cheque_setup.save()

			wiretransefer_setup = wiretransefer_setup_form.save(commit=False)
			wiretransefer_setup.payment_mode = payment_mode
			wiretransefer_setup.save()

			paypal_setup = paypal_setup_form.save(commit=False)
			paypal_setup.payment_mode = payment_mode
			paypal_setup.save()
			success_dict = {}
			success_dict['success_msg'] = "Successfully Edited Payment Setup"
			return HttpResponse(json.dumps(success_dict), content_type='application/json')
		else:
			error_dict={}
			form_error_dict = {}
			cheque_setup_form_error_dict = {}
			wiretransefer_setup_form_errors = {}
			paypal_setup_form_errors = {}

			for error in form.errors:
				form_error_dict[error] = form.errors[error]
				
			for error in cheque_setup_form:
				e = cheque_setup_form.errors[error]
				cheque_setup_form_error_dict[error] = unicode(e)

			for error in wiretransefer_setup_form:
				e = wiretransefer_setup_form.errors[error]
				wiretransefer_setup_form_errors[error] = unicode(e)

			for error in paypal_setup_form:
				e = paypal_setup_form.errors[error]
				paypal_setup_form_errors[error] = unicode(e)

			error_dict['form_error_dict'] = form_error_dict
			error_dict['cheque_setup_form_error_dict'] = cheque_setup_form_error_dict
			error_dict['wiretransefer_setup_form_errors'] = wiretransefer_setup_form_errors
			error_dict['paypal_setup_form_errors'] = paypal_setup_form_errors
			return HttpResponseBadRequest(json.dumps(error_dict), content_type='application/json')
	else:
		form = forms.PaymentModeSetupForm(instance=payment_mode)
		cheque_setup_form = forms.ChequeSetupForm(instance=cheque_setup)
		wiretransefer_setup_form = forms.WiretransferSetupForm(instance=wiretransefer_setup)
		paypal_setup_form = forms.PaypalSetupForm(instance=paypal_setup)

	return render(request, 'invoice/payment_mode_add_partial.html', {
												'form': form, 
												'is_edit_mode' : True ,
												'id' : id,
												'cheque_setup_form':cheque_setup_form,
												'wiretransefer_setup_form':wiretransefer_setup_form,
												'paypal_setup_form':paypal_setup_form
											}
										)




@login_required
def paymant_reconciliation_list(request):

	paymant_reconciliation_lists = models.PaymentReconciliation.objects.all()
	return render(request, 'invoice/payment_reconciliation_list_partial.html', 
					{'paymant_reconciliation_lists': paymant_reconciliation_lists}
				)


@login_required
def paymant_reconciliation_add(request):
	form = forms.PaymentReconciliationForm(request.POST, request.FILES,)
	if request.method == 'POST':
		if form.is_valid():
			payments = form.save(commit=False)
			payments.save()
			success_dict = {}
			success_dict['success_msg'] = "Successfully Created PaymentReconciliation"
			return HttpResponse(json.dumps(success_dict), content_type='application/json')
		else:
			error_dict={}
			for error in form.errors:
				error_dict[error] = form.errors[error]
				
			return HttpResponseBadRequest(json.dumps(error_dict))
	else:
		form = forms.PaymentReconciliationForm()

	return render(request, 'invoice/payment_reconciliation_add_partial.html', locals())


@login_required
def paymant_reconciliation_edit(request, id):
	payment_reconciliation = get_object_or_404(models.PaymentReconciliation, id=id)
	if request.method == "POST":
		form = forms.PaymentReconciliationForm(request.POST, request.FILES, instance=payment_reconciliation)
		if form.is_valid():
			payments = form.save(commit=False)
			docu = form.cleaned_data.get('document')
			print "docu", docu
			payments.save()
			success_dict = {}
			success_dict['success_msg'] = "Successfully Edited PaymentReconciliation"
			return HttpResponse(json.dumps(success_dict), content_type='application/json')
		else:
			error_dict={}
			for error in form.errors:
				error_dict[error] = form.errors[error]
				
			return HttpResponseBadRequest(json.dumps(error_dict))
	else:
		form = forms.PaymentReconciliationForm(instance=payment_reconciliation)
	return render(request, 'invoice/payment_reconciliation_add_partial.html', {'form': form, 'is_edit_mode' : True , 'id' : id,})
