# -*- coding: utf-8 -*-
from django.contrib import admin

from .models import Invoice, InvoiceLineItem
from .forms import InvoiceAdminForm,InvoiceLineItemAdminForm

class InvoiceLineItemInline(admin.TabularInline):
    '''
    Tabular Inline View for InvoiceLineItem
    '''
    model = InvoiceLineItem
    # min_num = 3
    # max_num = 20
    #extra = 1
    # raw_id_fields = (,)

    # list_display = (
    #     u'id',
    #     'invoice',
    #     'billing_type',
    #     'employee',
    #     'billing_units',
    #     'billing_amount_per_unit',
    #     'line_amount',
    # )
    # list_filter = ('invoice', 'billing_type', 'employee')
    # form=InvoiceLineItemAdminForm

    
class InvoiceAdmin(admin.ModelAdmin):
    #inlines= (InvoiceLineItemInline,)
    list_display = (
        u'id',
        'start',
        'end',
        'date',
        #'project',
        'customer',
        'total_amount',
    )
    list_filter = ('start', 'end', 'date','customer')
    form=InvoiceAdminForm
admin.site.register(Invoice, InvoiceAdmin)


class InvoiceLineItemAdmin(admin.ModelAdmin):
    list_display = (
        u'id',
        #'invoice',
        #'billing_type',
        #'employee',
       # 'billing_units',
       # 'billing_amount_per_unit',
       # 'line_amount',
    )
    #list_filter = ('employee')
    form=InvoiceLineItemAdminForm
admin.site.register(InvoiceLineItem, InvoiceLineItemAdmin)

