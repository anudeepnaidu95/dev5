# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django import forms

from django.contrib.admin import widgets
	

from django.forms import  ModelForm
from .models import Invoice, InvoiceLineItem, PaymentReconciliation, InvoiceSetup, CompanyBankAccount, PaymentTerms, WireTransferInfo



class PaymentTermsForm(forms.ModelForm):

    class Meta:
        model = PaymentTerms
        fields = ('terms',)
        exclude = ('invoice_setup',)
    def __init__(self, *args, **kwargs):
        super(PaymentTermsForm, self).__init__(*args, **kwargs)
        self.fields['terms'].required = True

class InvoiceSetupForm(forms.ModelForm):

    class Meta:
        model = InvoiceSetup
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super(InvoiceSetupForm, self).__init__(*args, **kwargs)
        self.fields['company_name'].required = True
        self.fields['phone'].required = True
        self.fields['email'].required = True


class BankDetailsForm(forms.ModelForm):

    class Meta:
        model = CompanyBankAccount
        fields = "__all__"

    



class WireTransferInfoForm(forms.ModelForm):

    class Meta:
        model = WireTransferInfo
        fields = "__all__"
        exclude = ('invoice_setup',)

    def __init__(self, *args, **kwargs):
        super(WireTransferInfoForm, self).__init__(*args, **kwargs)
        self.fields['beneficiary_name'].required = True
        self.fields['bank_name'].required = True
        self.fields['account_number'].required = True
        self.fields['swift_id'].required = True

