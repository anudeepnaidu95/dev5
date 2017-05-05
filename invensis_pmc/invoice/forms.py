from django import forms
from django_select2.forms import ModelSelect2Widget
from django.forms import TextInput, ModelForm, Textarea, Select
# from .models import Invoice,ServiceInvoice, InvoiceLineItem, PaymentReconciliation, InvoiceSetup, CompanyBankAccount, PaymentTerms, WireTransferInfo
from invoice import models
from project.models import Service




class MyWidget(ModelSelect2Widget):
    search_fields = [
        'title__icontains',
    ]

class MyTaskWidget(ModelSelect2Widget):
    search_fields = [
        'name__icontains',
    ]

class InvoiceAdminForm(forms.ModelForm):
    
    class Meta:
    	model=models.Invoice
        fields = '__all__'
        widgets = {
            'project': MyWidget,
            'customer':MyWidget,
            'management_employee':MyTaskWidget,
            
        }

class InvoiceLineItemAdminForm(forms.ModelForm):

    class Meta:
    	model=models.InvoiceLineItem
        fields = '__all__'
        widgets = {
            'employee': MyTaskWidget,
            'billing_type':Select(attrs={'class': 'input-medium'}),
            'billing_units':TextInput(attrs={'class': 'input-small'}),
            'billing_amount_per_unit':TextInput(attrs={'class': 'input-small'}),
            'line_amount':TextInput(attrs={'class': 'input-small'}),
        }


class InvoiceForm(forms.ModelForm):
    start = forms.DateField(label = 'Start Date' , input_formats=['%Y-%m-%d','%d/%m/%Y','%d-%m-%Y'])
    end = forms.DateField(label = 'End Date' ,input_formats=['%Y-%m-%d','%d/%m/%Y','%d-%m-%Y'])
    is_final = forms.BooleanField(label='Is This Final Invoice ?',required=False,initial=False)

    class Meta:
        model = models.Invoice
        fields = ('start', 'end', 'is_final')

    def __init__(self, *args, **kwargs):
        request = kwargs.pop('request', None)
        super(InvoiceForm, self).__init__(*args, **kwargs)
        
        if request.user.groups.filter(name='management').exists():
            self.fields['start'].widget = forms.DateTimeInput(format='%Y-%m-%d', attrs={'readonly':'readonly',})
            self.fields['end'].widget = forms.DateTimeInput(format='%Y-%m-%d', attrs={'readonly':'readonly',})


class ServiceInvoiceForm(forms.ModelForm):
    service = forms.ModelChoiceField(queryset=Service.objects.all(), widget=forms.widgets.Select(attrs={'readonly': 'readonly','disabled':True}))

    class Meta:
        model = models.ServiceInvoice
        fields = "__all__"
        exclude = ('invoice',)
        widgets = {'billing_type': forms.widgets.Select(attrs={'readonly': 'readonly', 'disabled':True})}

    def __init__(self, *args, **kwargs):
        super(ServiceInvoiceForm, self).__init__(*args, **kwargs)
        self.fields['service'].required=False
        self.fields['billing_type'].required = False


class PaymentForm(forms.ModelForm):
    payment_date = forms.DateField(label = 'Payment Date' , input_formats=['%Y-%m-%d','%d/%m/%Y','%d-%m-%Y'])

    class Meta:
        model = models.PaymentReconciliation
        fields = '__all__'
        exclude = ('invoice',)
    
from django_select2.forms import ModelSelect2Widget
class InvoiceNoWidget(ModelSelect2Widget):
    search_fields = [
        'invoice_no__icontains',        
    ]


class PaymentReconciliationForm(forms.ModelForm):
   # invoice = forms.ModelChoiceField(queryset=models.Invoice.objects.filter(is_final=True))
    payment_date = forms.DateField(label = 'Payment Date' , input_formats=['%Y-%m-%d','%d/%m/%Y','%d-%m-%Y'])

    class Meta:
        model = models.PaymentReconciliation
        fields = '__all__'       
    
    
    def __init__(self, *args, **kwargs):
        super(PaymentReconciliationForm, self).__init__(*args, **kwargs)


        
class PaymentModeSetupForm(forms.ModelForm):

    class Meta:
        model = models.PaymentModeSetup
        fields = '__all__'


class ChequeSetupForm(forms.ModelForm):
    """docstring for ChequeSetupForm"""

    class Meta:
        model = models.ChequeSetup
        fields = '__all__'
        exclude = ('payment_mode',)

    # def __init__(self, *args, **kwargs):
    #     super(ChequeSetupForm, self).__init__()


class WiretransferSetupForm(forms.ModelForm):
    """docstring for WiretransferSetupForm"""

    class Meta:
        model = models.WiretransferSetup
        fields = '__all__'
        exclude = ('payment_mode',)
        

class PaypalSetupForm(forms.ModelForm):
    """docstring for PaypalSetupForm"""

    class Meta:
        model = models.PaypalSetup
        fields = '__all__'
        exclude = ('payment_mode',)

        





    