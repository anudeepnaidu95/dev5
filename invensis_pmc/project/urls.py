# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.conf import settings
from django.conf.urls import patterns, include, url
from .models import WorkItem, WorkItemAssignment,StaffTask
from django_filters.views import FilterView

urlpatterns = patterns('project.views',

    url(r'^sales-manager-dashboard/$', 'sales_manager_dashboard', name='sales_manager_dashboard'),
    url(r'^sales-rep-dashboard/$', 'sales_rep_dashboard', name='sales_rep_dashboard'),
    url(r'^masters-list/$', 'masters_list_dashboard', name='masters_list_dashboard'),
    url(r'^operation-manager-dashboard/$', 'operation_manager_dashboard', name='operation_manager_dashboard'),
    url(r'^lead-dashboard/$', 'lead_dashboard', name='lead_dashboard'),
    url(r'^agent-dashboard/$', 'agent_dashboard', name='agent_dashboard'),
    url(r'^qc-dashboard/$', 'qc_dashboard', name='qc_dashboard'),
    url(r'^hr-dashboard/$', 'hr_manager_dashboard', name='hr_dashboard'),
    # url(r'^management-dashboard/$', 'management_dashboard', name='management_dashboard'),
    url(r'^management-crm-dashboard/$', 'management_crm_dashboard', name='management_crm_dashboard'),

    #ajax data urls
    url(r'^get/sales-billings/$', 'sales_billings', name='get_sales_billings'),
	
    url(r'^service/$', 'service_list', name='service_list'),
    url(r'^add/service/$', 'service_add', name='service_add'),
    url(r'^view/service/(?P<id>\d+)/$', 'service_view', name='service_view'),
    url(r'^edit/service/(?P<id>\d+)/$', 'service_edit', name='service_edit'),
    
    url(r'^service-type/$', 'service_type_list', name='service_types_list'),
	url(r'^add/service-type/$', 'service_type_add', name='service_type_add'),
    url(r'^edit/service-type/(?P<slug>[\w-]+)/$', 'service_type_edit', name='service_type_edit'),

    url(r'^industry/$', 'industry_list', name='industry_list'),
    url(r'^add/industry/$', 'industry_add', name='industry_add'),
    url(r'^edit/industry/(?P<slug>[\w-]+)/$', 'industry_edit', name='industry_edit'),

    url(r'^project-types/$', 'project_type_list', name='project_types_list'),
    url(r'^add/project-type/$', 'project_type_add', name='project_type_add'),
    url(r'^edit/project-type/(?P<slug>[\w-]+)/$', 'project_type_edit', name='project_type_edit'),

	url(r'^billing-types/$', 'billing_type_list', name='billing_types_list'),
    url(r'^add/billing-type/$', 'billing_type_add', name='billing_type_add'),
    url(r'^edit/billing-type/(?P<id>\d+)/$', 'billing_type_edit', name='billing_type_edit'),

    url(r'^project/$', 'project_list', name='project_list'),
    url(r'^add/project/$', 'project_add', name='project_add'),
    url(r'^edit/project/(?P<id>\d+)/$', 'project_edit', name='project_edit'),

    url(r'^project_task/$', 'project_task_list', name='project_task_list'),
    url(r'^add/project_task/$', 'project_task_add', name='project_task_add'),
    url(r'^edit/project_task/(?P<id>\d+)/$', 'project_task_edit', name='project_task_edit'),


    url(r'^project_service/$', 'project_service_list', name='project_service_list'),
    url(r'^add/project_service/$', 'project_service_add', name='project_service_add'),
    url(r'^edit/project_service/(?P<id>\d+)/$', 'project_service_edit', name='project_service_edit'),

    url(r'^workitem/$', 'workitem_list', name='workitem_list'),
    url(r'^add/workitem/$', 'workitem_add', name='workitem_add'),
    url(r'^edit/workitem/(?P<id>\d+)/$', 'workitem_edit', name='workitem_edit'),

    url(r'^resource_plan/$', 'resource_plan_list', name='resource_plan_list'),
    url(r'^add/resource_plan/$', 'resource_plan_add', name='resource_plan_add'),
    url(r'^edit/resource_plan/(?P<id>\d+)/$', 'resource_plan_edit', name='resource_plan_edit'),


    url(r'^qc_assign/$', 'qc_assign_list', name='qc_assign_list'),
    url(r'^add/qc_assign/$', 'qc_assign_add', name='qc_assign_add'),
    url(r'^edit/qc_assign/(?P<id>\d+)/$', 'qc_assign_edit', name='qc_assign_edit'),

    url(r'^daily_task/$', 'daily_task_list', name='daily_task_list'),
    url(r'^add/daily_task/$', 'daily_task_add', name='daily_task_add'),
    url(r'^edit/daily_task/(?P<id>\d+)/$', 'daily_task_edit', name='daily_task_edit'),

    url(r'^service_sla/$', 'service_sla_list', name='service_sla_list'),
    url(r'^add/service_sla/$', 'service_sla_add', name='service_sla_add'),
    url(r'^edit/service_sla/(?P<id>\d+)/$', 'service_sla_edit', name='service_sla_edit'),

    url(r'^sla/$', 'sla_list', name='sla_list'),
    url(r'^add/sla/$', 'sla_add', name='sla_add'),
    url(r'^edit/sla/(?P<slug>[\w-]+)/$', 'sla_edit', name='sla_edit'),

    url(r'^service_document/$', 'service_document_list', name='service_document_list'),
    url(r'^add/service_document/$', 'service_document_add', name='service_document_add'),
    url(r'^edit/service_document/(?P<id>\d+)/$', 'service_document_edit', name='service_document_edit'),
   # url(r'^download/doc/(?P<file_name>[\w-]+)/$', 'service_document_download', name='download_document'),

    url(r'^work-weeks/$', 'workweek_list', name='workweeks_list'),
    url(r'^add/workweek/$', 'workweek_add', name='workweek_add'),
    url(r'^edit/workweek/(?P<id>\d+)/$', 'workweek_edit', name='workweek_edit'),

    #model task urls
    url(r'^tasks/$', 'task_list', name='tasks_list'),
    url(r'^add/task/(?P<service_id>\d+)/$', 'task_add', name='task_add'),
    url(r'^edit/task/(?P<task_id>\d+)/$', 'task_edit', name='task_edit'),

    # model leadTask urls
    url(r'^assign_lead/(?P<task_id>\d+)/$', 'assign_lead', name='assign_lead'),
    url(r'^assign_lead_update/(?P<task_id>\d+)/(?P<lead_task_id>\d+)/$', 'assign_lead_update', name='assign_lead_update'),

    url(r'^assign_lead_empty/$', 'assign_lead_empty', name='assign_lead_empty'),

    url(r'^lead-tasks/$', 'lead_task_list', name='lead_tasks_list'),
    url(r'^add/lead-task/$', 'lead_task_add', name='lead_task_add'),
    url(r'^edit/lead-task/(?P<id>\d+)/$', 'lead_task_edit', name='lead_task_edit'),

    url(r'^lead-tasks_hist/$', 'lead_task_hist_list', name='lead_tasks_hist_list'),


    # model Tasktemplate urls
    url(r'^task-templates/$', 'task_template_list', name='task_templates_list'),
    url(r'^add/task-template/$', 'task_template_add', name='task_template_add'),
    url(r'^edit/task-template/(?P<id>\d+)/$', 'task_template_edit', name='task_template_edit'),

    #model stafftask urls
    url(r'^staff_task/$', 'staff_task_list', name='staff_task_list'),
    url(r'^tasks-assigned-to-lead/$', 'tasks_assigned_to_lead', name="tasks_assigned__to_lead"),
    url(r'^add/staff_task/$', 'staff_task_add', name='staff_task_add'),
    url(r'^edit/staff_task/(?P<id>\d+)/$', 'staff_task_edit', name='staff_task_edit'),
    url(r'^get/staff-task-exp/$', 'staff_experience', name='staff_task_exp'),
    
    url(r'^staff_task_hist/$', 'staff_task_hist_list', name='staff_task_hist_list'),
    #url(r'^staff_task_hist/$', FilterView.as_view(model=StaffTask)),
    url(r'staff_task_status/$', 'staff_task_status', name='staff_task_status'),
    url(r'staff_task_history/$', 'staff_task_history', name='staff_task_history'),

    #model qctask urls
    url(r'^qc_task/$', 'qc_task_list', name='qc_task_list'),
    url(r'^add/qc_task/$', 'qc_task_add', name='qc_task_add'),
    url(r'^edit/qc_task/(?P<id>\d+)/$', 'qc_task_edit', name='qc_task_edit'),
    url(r'qc_task_status/$', 'qc_task_status', name='qc_task_status'),

    url(r'^qc_task_hist/$', 'qc_task_hist_list', name='qc_task_hist_list'),

    #model qctemplate urls
    url(r'^qc_template/$', 'qc_template_list', name='qc_template_list'),
    url(r'^add/qc_template/$', 'qc_template_add', name='qc_template_add'),
    url(r'^edit/qc_template/(?P<id>\d+)/$', 'qc_template_edit', name='qc_template_edit'),

    url(r'^exp_based_employees_list/$','exp_based_employees_list', name='exp_based_employees_list')

    
)