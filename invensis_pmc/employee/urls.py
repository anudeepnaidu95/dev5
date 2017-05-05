from __future__ import unicode_literals
from django.conf.urls import patterns, include, url



urlpatterns = patterns('employee.views',
  # url(r'^vendor/get/$', 'get_preferred_vendors' ),
  	url(r'^employee/$', 'employee_list', name='employee_list'),
    # url(r'^export_employee_details/$', 'export_employee_details', name='export_employee_details'),
    # url(r'^export_employee_form/$', 'export_employee_form', name='export_employee_form'),
    url(r'^add/employee/$', 'employee_add', name='employee_add'),
    url(r'^export/employee/$', 'employee_export', name='employee_export'),
    url(r'^edit/employee/(?P<id>\d+)/$', 'employee_edit', name='employee_edit'),

    url(r'^department/$', 'department_list', name='department_list'),
    url(r'^add/department/$', 'department_add', name='department_add'),
    url(r'^edit/department/(?P<id>\d+)/$', 'department_edit', name='department_edit'),

    url(r'^experience_slab/$', 'experience_slab_list', name='experience_slab_list'),
    url(r'^add/experience_slab/$', 'experience_slab_add', name='experience_slab_add'),
    url(r'^edit/experience_slab/(?P<id>\d+)/$', 'experience_slab_edit', name='experience_slab_edit'),
    url(r'^employee-exp-range/(?P<exp_slab_id>\d+)/$', "employee_exp_range_list", name="employee_exp_range_list")

   
)