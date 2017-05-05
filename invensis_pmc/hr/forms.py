from django import forms
from .models import FinancialYear, Holiday, Notification, EmployeeLeave
from django_select2.forms import ModelSelect2Widget
import django.contrib.auth.models as auth_models

class NameWidget(ModelSelect2Widget):
    search_fields = [
        'name__icontains',
    ]



class EmployeeLeaveAdminForm(forms.ModelForm):
    class Meta:
    	model=EmployeeLeave
        fields = '__all__'
        widgets = {
            'manager': NameWidget,
            'employee': NameWidget,
            
        }
