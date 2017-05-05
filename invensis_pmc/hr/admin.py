# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import admin

from .models import FinancialYear, Holiday, Notification, EmployeeLeave
from .forms import EmployeeLeaveAdminForm


class HolidayInline(admin.TabularInline):
    '''
    Tabular Inline View for Holiday
    '''
    model = Holiday
    # min_num = 3
    # max_num = 20
    extra = 1
    # raw_id_fields = (,)

    list_display = (
        u'id',
        'title',
        'description',
        #'slug',
        'financial_year',
        'date',
    )
    list_filter = ('financial_year', 'date')
    search_fields = ('slug',)

class FinancialYearAdmin(admin.ModelAdmin):
    inlines = (HolidayInline,)
    list_display = (u'id', 'title', 'description', 'slug')
    search_fields = ('slug',)
admin.site.register(FinancialYear, FinancialYearAdmin)


class HolidayAdmin(admin.ModelAdmin):
    list_display = (
        u'id',
        'title',
        'description',
        #'slug',
        'financial_year',
        'date',
    )
    list_filter = ('financial_year', 'date')
    search_fields = ('slug',)
admin.site.register(Holiday, HolidayAdmin)


class NotificationAdmin(admin.ModelAdmin):
    list_display = (
        u'id',
        'created',
        'modified',
        'title',
        'description',
        #'slug',
        'message',
    )
    list_filter = ('created', 'modified')
    search_fields = ('slug',)
admin.site.register(Notification, NotificationAdmin)


class EmployeeLeaveAdmin(admin.ModelAdmin):
    list_display = (
        u'id',
        'start',
        'end',
        'manager',
        'employee',
        'reason',
        'is_approved',
    )
    list_filter = ('start', 'end', 'manager', 'employee', 'is_approved')
    form=EmployeeLeaveAdminForm
admin.site.register(EmployeeLeave, EmployeeLeaveAdmin)

# do we need to define shifts and associate to employees

# do we need to define weekend days

# do we need to capture attendance data

# do we need to arrive at the number of leave days
