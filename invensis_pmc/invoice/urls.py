from django.conf.urls import patterns, include, url


urlpatterns = patterns('invoice.views',
  # url(r'^vendor/get/$', 'get_preferred_vendors' ),

    url(r'^invoices/$', 'invoice_list', name='invoices_list'),
    url(r'^final-invoices/$', 'final_invoice_list', name='final_invoices_list'),
    url(r'^invoice-view-detail/$', 'invoice_view_details', name='invoice_view_details'),
    url(r'^invoice/add/(?P<customer_id>\d+)/$', 'invoice_add', name='invoice_add'),
    url(r'^invoice/edit/(?P<invoice_id>\d+)/$', 'invoice_edit', name='invoice_edit'),

    url(r'^invoice-line-items/(?P<service_inv_id>\d+)/$', 'service_line_item_list', name='service_line_item_list'),
    url(r'^line-item-lists/(?P<service_id>\d+)/$', 'line_item_list', name='line_item_lists'),
    
    url(r'^invoice/generate/(?P<customer_id>\d+)/$', 'generate_invoice', name='generate_invoice'),

    url(r'^generator/(?P<invoice_id>\d+)/$', 'invoice_generator', name='invoice_generator'),
    url(r'^payments/(?P<invoice_id>\d+)/$', 'payments_list', name='payments_lists'),
    url(r'^payments-add/(?P<invoice_id>\d+)/$', 'payment_list_and_add', name='payment_list_and_add'),
    
    #paymanet reconciliations
    url(r'^paymants-lists/$', 'paymant_reconciliation_list', name='paymant_reconciliation_list'),    
    url(r'^payments-recon/add/$', 'paymant_reconciliation_add', name='paymant_reconciliation_add'),
    url(r'^payments-recon/edit/(?P<id>\d+)/$', 'paymant_reconciliation_edit', name='paymant_reconciliation_edit'),


    url(r'^invoice-setup/$', 'invoice_setup_list', name='invoice_setup_list'),
    url(r'^invoice-setup/add/$', 'invoice_setup_add', name='invoice_setup_add'),
    url(r'^invoice-setup/edit/(?P<id>\d+)/$', 'invoice_setup_edit', name='invoice_setup_edit'),
    
    url(r'^bank-details-list/$', 'bank_details_list', name='bank_details_list'),
    url(r'^bank-details/add/$', 'bank_details_add', name='bank_details_add'),
    url(r'^bank-details/edit/(?P<id>\d+)/$', 'bank_details_edit', name='bank_details_edit'),

    url(r'^payment-modes-list/$', 'payment_modes_list', name='payment_modes_list'),
    url(r'^payment-mode/add/$', 'payment_mode_add', name='payment_mode_add'),
    url(r'^payment-mode/edit/(?P<id>\d+)/$', 'payment_mode_edit', name='payment_mode_edit'),

)