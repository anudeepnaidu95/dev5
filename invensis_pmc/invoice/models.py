from django.db import models
from customer.models import Customer, CURRENCY_TYPES
from project.models import  Service, BILLING_TYPES, Task, LeadTask, StaffTask
from model_utils.models import TimeFramedModel
from employee.models import Employee

class CompanyBankAccount(models.Model):

	# pls give proper verbose names ***
	bank_name = models.CharField( max_length=255, verbose_name='Bank Name')
	account_number = models.CharField( max_length=255, verbose_name='Account Number')
	ifsc_code =  models.CharField( max_length=50, blank=True, null=True)
	micr_code = models.CharField( max_length=50, blank=True,null=True)
	bank_branch = models.CharField( max_length=50, blank=True, null=True)

	addressline1 = models.CharField( max_length=255, blank=True, null=True)
	addressline2 = models.CharField( max_length=255, blank=True, null=True)
	city = models.CharField( max_length=255, blank=True, null=True)
	state = models.CharField( max_length=255, blank=True, null=True)
	pincode = models.CharField( max_length=10, blank=True, null=True)

	class Meta:
	    verbose_name = "CompanyBankAccount"
	    verbose_name_plural = "CompanyBankAccounts"

	def __str__(self):
	    return self.bank_name

# class WireTransferAccount(models.Model):

# 	class Meta:
# 	    verbose_name = "WireTransferAccount"
# 	    verbose_name_plural = "WireTransferAccounts"

# 	def __str__(self):
# 	    return str(self.id)
    
# class PaypalAccount(models.Model):
    
# 	    class Meta:
# 	        verbose_name = "PaypalAccount"
# 	        verbose_name_plural = "PaypalAccounts"

# 	    def __str__(self):
# 	        pass
            
MODE_OF_PAYMENTS = (
	('cheque','Cheque',),
	('wire_transfer','Wire Transfer',),
	('paypal','Paypal',),
	# ('','',),
	# ('','',),
	# ('','',),
	# ('','',),
	)

class Invoice(TimeFramedModel):


	invoice_no = models.CharField( max_length=50, blank=True,null=True)
	
	date = models.DateField()
	# project = models.ForeignKey(Project)
	customer = models.ForeignKey(Customer, related_name='+')
	
	total_amount = models.DecimalField( max_digits=9, decimal_places=2,default=0)

	management_employee = models.ForeignKey(Employee, related_name='+')

	is_final = models.BooleanField(default=False)

	class Meta:
	    verbose_name = "Invoice"
	    verbose_name_plural = "Invoices"

	def __str__(self):
	    return str(self.invoice_no)
    
class ServiceInvoice(models.Model):

	invoice = models.ForeignKey(Invoice, related_name='+')

	service = models.ForeignKey(Service, related_name='+')

	billing_type = models.CharField(choices=BILLING_TYPES, max_length=50)

	pricing = models.DecimalField( max_digits=9, decimal_places=2, default=0)
	invoice_amount = models.DecimalField( max_digits=9, decimal_places=2, default=0)

	no_of_txs = models.IntegerField(default=0)

	no_of_resources = models.DecimalField( max_digits=5, decimal_places=2)

	no_of_working_days = models.DecimalField( max_digits=5, decimal_places=2)

	no_of_hours = models.DecimalField( max_digits=9, decimal_places=2)


	class Meta:
	    verbose_name = "ServiceInvoice"
	    verbose_name_plural = "ServiceInvoices"

	def __str__(self):
	    return str(self.id)
    
class InvoiceLineItem(models.Model):

	service_inv = models.ForeignKey(ServiceInvoice, blank=True, null=True, related_name='+')

	# need to capture project_task ,lead_task , staff_task ids****

	# invoice = models.ForeignKey(Invoice)

	# billing_type =  models.ForeignKey(BillingType)

	# only used if billing type = per person
	# employee =  models.ForeignKey(Employee, blank=True, null=True, related_name='+')
	
	# 
	# billing_units = models.DecimalField( max_digits=9, decimal_places=2, default=0)

	# billing_amount_per_unit = models.DecimalField( max_digits=9, decimal_places=2, default=0)

	# line_amount =  models.DecimalField( max_digits=9, decimal_places=2, default=0)

	task = models.ForeignKey(Task,  blank=True, null=True, related_name='+')
	lead_task = models.ForeignKey(LeadTask,  blank=True, null=True, related_name='+')
	staff_task = models.ForeignKey(StaffTask,  blank=True, null=True, related_name='+')

	# filter only agents under ops mgr*******
	staff = models.ForeignKey(Employee, verbose_name='Agent / Artist', blank=True,null=True, related_name='+')

	# filename = models.FilePathField(max_length=1024, allow_files=True, allow_folders = False, blank=True, null=True)
	# filename = models.FileField(max_length=1024, blank=True, null=True)
	filename = models.CharField(max_length=1024, blank=True, null=True)

	no_of_txs = models.PositiveIntegerField(verbose_name='Number of Transactions', blank=True, null=True, default=0)

	# no_of_txs_completed = models.PositiveIntegerField(verbose_name='Number of Transactions completed', blank=True, default=0, null=True)

	# is this required ???
	# total_time_hours = models.PositiveIntegerField(blank=True, null=True, default=0)
	time_in_min = models.CharField(blank=True, null=True, max_length=20)

	class Meta:
	    verbose_name = "InvoiceLineItem"
	    verbose_name_plural = "InvoiceLineItems"

	def __str__(self):
	    return str(self.id)
    
class PaymentReconciliation(models.Model):

	invoice = models.ForeignKey(Invoice, related_name='+')

	mode_of_payment = models.CharField(choices=MODE_OF_PAYMENTS, max_length=50)

	bank_account = models.ForeignKey(CompanyBankAccount, related_name='+' , blank=True, null=True)

	payment_date = models.DateField()	
	cheque_no = models.CharField( max_length=50, blank=True,null=True)
	document = models.FileField(upload_to='invoice_documents/',blank=True, null=True, verbose_name='Upload Document')

	transaction_id = models.CharField( max_length=50, blank=True, null=True)

	email_id = models.EmailField(blank=True,null=True, max_length=1024)	

	payment_amount = models.DecimalField( max_digits=9, decimal_places=2, default=0)



	class Meta:
	    verbose_name = "PaymentReconciliation"
	    verbose_name_plural = "PaymentReconciliations"

	def __str__(self):
	    return str(self.id)


class InvoiceSetup(models.Model):

	company_name = models.CharField( max_length=255, blank=True, null=True)
	addressline1 = models.CharField( max_length=255, blank=True, null=True)
	addressline2 = models.CharField( max_length=255, blank=True, null=True)

	city = models.CharField( max_length=50, blank=True, null=True)
	state = models.CharField( max_length=50, blank=True, null=True)
	country = models.CharField( max_length=50, blank=True, null=True)
	pincode = models.CharField( max_length=50, blank=True, null=True)
	
	phone = models.CharField( max_length=50, blank=True, null=True)
	email = models.CharField( max_length=255, blank=True, null=True)


	class Meta:
	    verbose_name = "InvoiceSetup"
	    verbose_name_plural = "InvoiceSetups"

	def __str__(self):
	    pass
    
    
class PaymentTerms(models.Model):
	invoice_setup = models.ForeignKey(InvoiceSetup, related_name='+')

	terms = models.CharField( max_length=1024)

	class Meta:
	    verbose_name = "PaymentTerms"
	    verbose_name_plural = "PaymentTermss"

	def __str__(self):
	    pass
    

class WireTransferInfo(models.Model):
	invoice_setup = models.ForeignKey(InvoiceSetup, related_name='+')
	beneficiary_name = models.CharField( max_length=255, blank=True, null=True)
	bank_name = models.CharField( max_length=255, blank=True, null=True)
	routing_number = models.CharField( max_length=255, blank=True, null=True)
	account_number = models.CharField( max_length=255, blank=True, null=True)
	swift_id = models.CharField(max_length=50, blank=True, null=True)
	# Wire Transfer Details:
	# Beneficiary Name : Invensis, Inc.
	# Bank : PNC 
	# ROUTING NUMBER : 041000124
	# ACCOUNT NUMBER : 4240495012
	# SWIFT ID: PNCCUS33


	class Meta:
	    verbose_name = "WireTransferInfo"
	    verbose_name_plural = "WireTransferInfos"

	def __str__(self):
	    pass
    

    

class PaymentModeSetup(models.Model):


	currency = models.CharField(choices=CURRENCY_TYPES, max_length=10)

	# cheque = models.ForeignKey(ChequeSetup, related_name='+', blank=True, null=True)
	# wiretransfer = models.ForeignKey(WiretransferSetup, related_name='+', blank=True, null=True)
	# paypal = models.ForeignKey(PaypalSetup, related_name='+', blank=True, null=True)


	class Meta:
	    verbose_name = "PaymentModeSetup"
	    verbose_name_plural = "PaymentModeSetups"

	def __str__(self):
	    return self.currency
    
class ChequeSetup(models.Model):

	payment_mode = models.ForeignKey(PaymentModeSetup, related_name='+')

	is_applicable = models.BooleanField(default=True)
	company_name = models.CharField( max_length=255)

	bank = models.CharField( max_length=255)

	account_number = models.CharField( max_length=20)

	# cheque mailing address
	addressline1 = models.CharField( max_length=255, blank=True, null=True)
	addressline2 = models.CharField( max_length=255, blank=True, null=True)

	city = models.CharField( max_length=50, blank=True, null=True)
	state = models.CharField( max_length=50, blank=True, null=True)
	country = models.CharField( max_length=50, blank=True, null=True)
	pincode = models.CharField( max_length=50, blank=True, null=True)
	
	phone = models.CharField( max_length=50, blank=True, null=True)
	email = models.CharField( max_length=255, blank=True, null=True)


	class Meta:
	    verbose_name = "ChequeSetup"
	    verbose_name_plural = "ChequeSetups"

	def __str__(self):
	    return str(self.id)
    
class WiretransferSetup(models.Model):
	payment_mode = models.ForeignKey(PaymentModeSetup, related_name='+')	
	is_applicable = models.BooleanField(default=True)

	show_only_beneficiary_details = models.BooleanField(default=False)	
	# 1
	# CORRESPONDENT Bank's Name, Account No. & Swift Code
	# THE BANK OF NOVASCOTIA
	# Toronto, Canada
	# Swift Code:  asdf
	# Account No.1234
	correspondent_bank_label = models.CharField( max_length=255 , blank=True, null=True)

	correspondent_bank_name = models.CharField( max_length=255, blank=True, null=True)
	correspondent_bank_address = models.CharField( max_length=255, blank=True, null=True)
	correspondent_bank_account_number = models.CharField( max_length=30, blank=True, null=True)
	correspondent_bank_swift_code = models.CharField(max_length=30, blank=True, null=True)
	
	# 2
	# Beneficiary's Banker's Name & Swift code
	# KOTAK MAHINDRA BANK LTD
	# International Banking Division Mumbai
	# Swift Code: asdf
	beneficiary_banker_label = models.CharField( max_length=255 , blank=True, null=True)

	beneficiary_banker_name = models.CharField( max_length=255, blank=True, null=True)
	beneficiary_banker_address = models.CharField( max_length=255, blank=True, null=True)
	beneficiary_banker_swift_code = models.CharField(max_length=30, blank=True, null=True)

	 
	# Further credit to                                      
	# KOTAK MAHINDRA BANK LTD
	# M.G. ROAD BRANCH,
	# BANGALORE  560 001, India
	further_credit_to_label = models.CharField( max_length=255 , blank=True, null=True)

	further_credit_to_bank = models.CharField( max_length=255, blank=True, null=True)
	further_credit_to_bank_address = models.CharField( max_length=255, blank=True, null=True)

	 
	# Beneficiary's Name, Bank Account No and Branch Name 
	# INVENSIS TECHNOLOGIES (P) LTD.,
	# A/C.No.1234
	# Branch Name.  V V PURAM,
	# BANGALORE - 560 004  India.

	# Wire Transfer Details:
	# Beneficiary Name : Invensis, Inc.
	# Bank : PNC 
	# ROUTING NUMBER : 041000124
	# ACCOUNT NUMBER : 4240495012
	# SWIFT ID: PNCCUS33
	beneficiary_label = models.CharField( max_length=255 , blank=True, null=True)
	beneficiary_name = models.CharField( max_length=255)
	beneficiary_bank_name = models.CharField( max_length=255, blank=True, null=True)
	beneficiary_bank_address = models.CharField( max_length=255, blank=True, null=True)
	beneficiary_routing_number = models.CharField( max_length=30, blank=True, null=True)
	beneficiary_account_number = models.CharField( max_length=30, blank=True, null=True)
	beneficiary_swift_code = models.CharField(max_length=30, blank=True, null=True)


	class Meta:
	    verbose_name = "WiretransferSetup"
	    verbose_name_plural = "WiretransferSetups"

	def __str__(self):
	    return str(self.id)
    
class PaypalSetup(models.Model):
	payment_mode = models.ForeignKey(PaymentModeSetup, related_name='+')	
	# details here
	is_applicable = models.BooleanField(default=True)	
	surcharge_percent = models.DecimalField( max_digits=5, decimal_places=2 , default=0)

	payable_to_email = models.CharField( max_length=100 )

	class Meta:
	    verbose_name = "PaypalSetup"
	    verbose_name_plural = "PaypalSetups"

	def __str__(self):
	    return str(self.id)

