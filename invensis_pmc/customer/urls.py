# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.conf.urls import patterns, include, url
#from .models import WorkItem, WorkItemAssignment

urlpatterns = patterns('customer.views',

    url(r'^leads/$', 'leads_list', name='leads_list'),
    url(r'^lead/add/$', 'lead_add', name='lead_add'),
    url(r'^leads/view/(?P<id>\d+)/$', 'leads_view', name='leads_view'),
    url(r'^lead/edit/(?P<id>\d+)/$', 'lead_edit', name='lead_edit'),

    url(r'^customers/$', 'customers_list', name='customers_list'),
    url(r'^customer/add/$', 'customer_add', name='customer_add'),
    url(r'^customers/view/(?P<id>\d+)/$', 'customers_view', name='customers_view'),
    url(r'^customer/edit/(?P<id>\d+)/$', 'customer_edit', name='customer_edit'),
    
    url(r'^customer/(?P<slug>[\w-]+)/$', 'customer_detail', name='customer_detail'),
    
    url(r'^country/$', 'country_list', name='country_list'),
    url(r'^country/add/$', 'country_add', name='country_add'),
    url(r'^country/edit/(?P<id>\d+)/$', 'country_edit', name='country_edit'),

    url(r'^currency-types/$', 'currency_type_list', name='currency_type_list'),
    url(r'^currency-type/add/$', 'currency_type_add', name='currency_type_add'),
    url(r'^currency-type/edit/(?P<id>\d+)/$', 'currency_type_edit', name='currency_type_edit'),

    url(r'^get/services/$', 'get_services', name='get_services'),
    url(r'^export_leads_xls/$', 'export_leads_xls', name='export_leads_xls'),
    url(r'^export_leads_form/$', 'export_leads_form', name='export_leads_form'),
    url(r'^ImportWorkItem/$', 'ImportWorkItem', name='ImportWorkItem'),

    
)