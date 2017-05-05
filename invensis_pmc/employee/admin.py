# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import admin
from django.db import models
from django import forms
from django.forms.models import BaseModelFormSet
from django.contrib.auth.models import User
from import_export.admin import ImportExportModelAdmin, ImportMixin, ImportExportMixin
from import_export import fields,resources, formats
from import_export.widgets import ForeignKeyWidget,ManyToManyWidget
from import_export.admin import DEFAULT_FORMATS
from suit.admin import SortableModelAdmin
from mptt.admin import MPTTModelAdmin
from .models import Department, Role, Employee, ExperienceSlab, EmployeeRole

from project.models import EmployeeAssignment, Project
from .forms import EmployeeAdminForm, EmployeeAssignmentInlineForm


class EmployeeResource(resources.ModelResource):
   
    formats = DEFAULT_FORMATS

    user = fields.Field(column_name='user', attribute='user',
                       widget=ForeignKeyWidget(User, field ='username'))

    department = fields.Field(column_name='department', attribute='department',
                       widget=ForeignKeyWidget(Department, field ='title'))

    # organization = fields.Field(column_name='organization', attribute='organization',
    #                    widget=ForeignKeyWidget(Organization, field ='title'))


    parent = fields.Field(column_name='reporting to', attribute='parent',
                       widget=ForeignKeyWidget(Employee, field ='name'))

    roles = fields.Field(column_name='roles', attribute='roles',
                       widget=ManyToManyWidget(Role, field ='title'))

    class Meta:
        model = Employee
        skip_unchanged = True
        report_skipped = True
        import_id_fields = ('user',)
        fields = ('name','user','department','roles','parent',)
        export_order = ('name','user','department','roles','parent',)
      



# class OrganizationAdmin(admin.ModelAdmin):
#     list_display = (u'id', 'title', 'description', )
#     search_fields = ('slug',)
# admin.site.register(Organization, OrganizationAdmin)


class DepartmentAdmin(admin.ModelAdmin):
    list_display = (u'id', 'title', 'description', )
    # list_filter = (,)
    search_fields = ('slug',)
admin.site.register(Department, DepartmentAdmin)


class EmployeeRoleAdmin(admin.ModelAdmin):
    list_display = (u'id', 'employee', 'role', )
    # list_filter = (,)
    search_fields = ('role',)
admin.site.register(EmployeeRole, EmployeeRoleAdmin)


class RoleAdmin(admin.ModelAdmin):
    list_display = (u'id', 'title', 'description')
admin.site.register(Role, RoleAdmin)

class EmployeeAssignmentInline(admin.TabularInline):
    '''
    Tabular Inline View for EmployeeAssignment
    '''
    model = EmployeeAssignment
    # min_num = 3
    # max_num = 20
    extra = 1
    # raw_id_fields = (,)

    form = EmployeeAssignmentInlineForm

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "project":
            kwargs["queryset"] = Project.objects.filter(projectservice__operations_manager__user=request.user)
        return super(EmployeeAssignmentInline, self).formfield_for_foreignkey(db_field, request, **kwargs)
  


class EmployeeAdmin(ImportExportModelAdmin, MPTTModelAdmin,SortableModelAdmin, admin.SimpleListFilter):

    inlines = (EmployeeAssignmentInline,)
    resource_class = EmployeeResource
    list_display = (
        u'id',
        'parent',
        'department',
        'name',
        # 'userrole',
        'user',
        u'lft',
        u'rght',
        u'tree_id',
        u'level',
    )
    list_filter = ('parent'
        , 'department'
        # , 'role'
        , 'user')
    search_fields = ('name',)

    sortable = u'id'
    #raw_id_fields = ('user',)

    mptt_level_indent = 20
    form = EmployeeAdminForm

    def queryset(self, request):

        qs = super(EmployeeAdmin, self).queryset(request)
        if request.user.is_superuser:
            # It is mine, all mine. Just return everything.
            return qs

        groups=request.user.groups.all()
        group_dict = dict([ (grp.name, grp)  for  grp in groups])

        if 'management' in  group_dict :
            return qs

        elif 'operations manager' in group_dict:
            related_employes = Employee.objects.get(user=request.user)
            qs = related_employes.get_descendants()
            return qs

        return qs


admin.site.register(Employee, EmployeeAdmin)


class ExperienceSlabAdmin(admin.ModelAdmin):
    list_display = (
        u'id',
        #'created',
        #'modified',
        'title',
        'description',
    )
    list_filter = ('created', 'modified')
    search_fields = ('slug',)
admin.site.register(ExperienceSlab, ExperienceSlabAdmin)

