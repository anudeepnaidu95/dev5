from django.conf.urls import patterns, include, url


urlpatterns = patterns('dashboard.views',
  # url(r'^vendor/get/$', 'get_preferred_vendors' ),

    url(r'^dashboard/$', 'stats_dashboard_list', name='stats_dashboard_list'),
    url(r'^lead-enquires-stats/$', 'lead_enquires_stat', name='lead_enquires_stat'),


    url(r'^revenue-setup-list/$', 'revenue_setup_list', name='revenue_setup_list'),
    url(r'^revenue-setup-add/$', 'revenue_setup_add', name='revenue_setup_add'),
    url(r'^revenue-setup-edit/(?P<id>\d+)/$', 'revenue_setup_edit', name='revenue_setup_edit'),
    

    url(r'^all-open-leads-list/$', 'all_open_leads_list', name='all_open_leads_list'),
    url(r'^all-won-leads-list/$', 'all_won_leads_list', name='all_won_leads_list'),

    url(r'^management-dashboard/$', 'management_dashboard', name='management_dashboard'),

)