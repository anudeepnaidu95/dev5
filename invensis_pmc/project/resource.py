# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from __future__ import with_statement
from import_export.admin import ImportExportModelAdmin, ImportMixin, ImportExportMixin
from import_export import fields,resources, formats
from import_export.widgets import ForeignKeyWidget,ManyToManyWidget
from import_export.admin import DEFAULT_FORMATS
from employee.models import Employee
from .models import ProjectTask, WorkItem, WorkItemAssignment,WorkItemStatus

from datetime import datetime
import importlib
import django
from django.contrib import admin
from django.utils import six
from django.utils.translation import ugettext_lazy as _
from django.conf.urls import url
from django.template.response import TemplateResponse
from django.contrib import messages
from django.contrib.admin.models import LogEntry, ADDITION, CHANGE, DELETION
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.conf import settings
from django.template.defaultfilters import pluralize
from import_export.formats import base_formats
from import_export.results import RowResult
from import_export.tmp_storages import TempFolderStorage


from import_export.forms import (
    ImportForm,
    ConfirmImportForm,
    ExportForm,
    export_action_form_factory,
)
from import_export.resources import (
    modelresource_factory,
)

try:
    from django.utils.encoding import force_text
except ImportError:
    from django.utils.encoding import force_unicode as force_text

SKIP_ADMIN_LOG = getattr(settings, 'IMPORT_EXPORT_SKIP_ADMIN_LOG', False)
TMP_STORAGE_CLASS = getattr(settings, 'IMPORT_EXPORT_TMP_STORAGE_CLASS',
                            TempFolderStorage)
if isinstance(TMP_STORAGE_CLASS, six.string_types):
    try:
        # Nod to tastypie's use of importlib.
        parts = TMP_STORAGE_CLASS.split('.')
        module_path, class_name = '.'.join(parts[:-1]), parts[-1]
        module = importlib.import_module(module_path)
        TMP_STORAGE_CLASS = getattr(module, class_name)
    except ImportError as e:
        msg = "Could not import '%s' for import_export setting 'IMPORT_EXPORT_TMP_STORAGE_CLASS'" % TMP_STORAGE_CLASS
        raise ImportError(msg)


DEFAULT_FORMATS = (
    base_formats.CSV,
    base_formats.XLS,
)



class ImportExportMixinBase(object):
    def get_model_info(self):
        # module_name is renamed to model_name in Django 1.8
        app_label = self.model._meta.app_label
        try:
            return (app_label, self.model._meta.model_name,)
        except AttributeError:
            return (app_label, self.model._meta.module_name,)


class ImportMixin(ImportExportMixinBase):
    """
    Import mixin.
    """

    #: template for change_list view
    change_list_template = 'admin/import_export/change_list_import.html'
    #: template for import view
    import_template_name = 'admin/import_export/import.html'
    #: resource class
    resource_class = None
    #: available import formats
    formats = DEFAULT_FORMATS
    #: import data encoding
    from_encoding = "utf-8"
    skip_admin_log = None
    # storage class for saving temporary files
    tmp_storage_class = None

    def get_skip_admin_log(self):
        if self.skip_admin_log is None:
            return SKIP_ADMIN_LOG
        else:
            return self.skip_admin_log

    def get_tmp_storage_class(self):
        if self.tmp_storage_class is None:
            return TMP_STORAGE_CLASS
        else:
            return self.tmp_storage_class

    def get_urls(self):
        urls = super(ImportMixin, self).get_urls()
        info = self.get_model_info()
        my_urls = [
            url(r'^process_import/$',
                self.admin_site.admin_view(self.process_import),
                name='%s_%s_process_import' % info),
            url(r'^import/$',
                self.admin_site.admin_view(self.import_action),
                name='%s_%s_import' % info),
        ]
        return my_urls + urls

    def get_resource_class(self):
        if not self.resource_class:
            return modelresource_factory(self.model)
        else:
            return self.resource_class

    def get_import_resource_class(self):
        """
        Returns ResourceClass to use for import.
        """
        return self.get_resource_class()

    def get_import_formats(self):
        """
        Returns available import formats.
        """
        return [f for f in self.formats if f().can_import()]

    def process_import(self, request, *args, **kwargs):
        '''
        Perform the actual import action (after the user has confirmed he
        wishes to import)
        '''
        opts = self.model._meta
        resource = self.get_import_resource_class()()
        total_imports = 0
        total_updates = 0

        confirm_form = ConfirmImportForm(request.POST)
        if confirm_form.is_valid():
            import_formats = self.get_import_formats()
            input_format = import_formats[
                int(confirm_form.cleaned_data['input_format'])
            ]()
            tmp_storage = self.get_tmp_storage_class()(name=confirm_form.cleaned_data['import_file_name'])
            data = tmp_storage.read(input_format.get_read_mode())
            if not input_format.is_binary() and self.from_encoding:
                data = force_text(data, self.from_encoding)
            dataset = input_format.create_dataset(data)

            result = resource.import_data(dataset, dry_run=False,
                                          raise_errors=True,
                                          file_name=confirm_form.cleaned_data['original_file_name'],
                                          user=request.user)

            if not self.get_skip_admin_log():
                # Add imported objects to LogEntry
                logentry_map = {
                    RowResult.IMPORT_TYPE_NEW: ADDITION,
                    RowResult.IMPORT_TYPE_UPDATE: CHANGE,
                    RowResult.IMPORT_TYPE_DELETE: DELETION,
                }
                content_type_id = ContentType.objects.get_for_model(self.model).pk
                for row in result:
                    if row.import_type != row.IMPORT_TYPE_SKIP:
                        LogEntry.objects.log_action(
                            user_id=request.user.pk,
                            content_type_id=content_type_id,
                            object_id=row.object_id,
                            object_repr=row.object_repr,
                            action_flag=logentry_map[row.import_type],
                            change_message="%s through import_export" % row.import_type,
                        )
                    if row.import_type == row.IMPORT_TYPE_NEW:
                        total_imports += 1
                    elif row.import_type == row.IMPORT_TYPE_UPDATE:
                        total_updates += 1

            success_message = u'Import finished, with {} new {}{} and ' \
                              u'{} updated {}{}.'.format(total_imports, opts.model_name, pluralize(total_imports),
                                                         total_updates, opts.model_name, pluralize(total_updates))

            messages.success(request, success_message)
            tmp_storage.remove()

            url = reverse('admin:%s_%s_changelist' % self.get_model_info(),
                          current_app=self.admin_site.name)
            return HttpResponseRedirect(url)
    def import_action(self, request, *args, **kwargs):
        '''
        Perform a dry_run of the import to make sure the import will not
        result in errors.  If there where no error, save the user
        uploaded file to a local temp file that will be used by
        'process_import' for the actual import.
        '''
        resource = self.get_import_resource_class()()

        context = {}

        import_formats = self.get_import_formats()
        form = ImportForm(import_formats,
                          request.POST or None,
                          request.FILES or None)

        if request.POST and form.is_valid():
            input_format = import_formats[
                int(form.cleaned_data['input_format'])
            ]()
            import_file = form.cleaned_data['import_file']
            # first always write the uploaded file to disk as it may be a
            # memory file or else based on settings upload handlers
            tmp_storage = self.get_tmp_storage_class()()
            data = bytes()
            for chunk in import_file.chunks():
                data += chunk

            tmp_storage.save(data, input_format.get_read_mode())

            # then read the file, using the proper format-specific mode
            # warning, big files may exceed memory
            try:
                data = tmp_storage.read(input_format.get_read_mode())
                if not input_format.is_binary() and self.from_encoding:
                    data = force_text(data, self.from_encoding)
                dataset = input_format.create_dataset(data)
            except UnicodeDecodeError as e:
                return HttpResponse(_(u"<h1>Imported file has a wrong encoding: %s</h1>" % e))
            except Exception as e:
                return HttpResponse(_(u"<h1>%s encountered while trying to read file: %s</h1>" % (type(e).__name__, import_file.name)))
            result = resource.import_data(dataset, dry_run=True,
                                          raise_errors=False,
                                          file_name=import_file.name,
                                          user=request.user)

            context['result'] = result

            if not result.has_errors():
                context['confirm_form'] = ConfirmImportForm(initial={
                    'import_file_name': tmp_storage.name,
                    'original_file_name': import_file.name,
                    'input_format': form.cleaned_data['input_format'],
                })

        if django.VERSION >= (1, 8, 0):
            context.update(self.admin_site.each_context(request))
        elif django.VERSION >= (1, 7, 0):
            context.update(self.admin_site.each_context())

        context['form'] = form
        context['opts'] = self.model._meta
        context['fields'] = [f.column_name for f in resource.get_fields()]

        request.current_app = self.admin_site.name
        return TemplateResponse(request, [self.import_template_name],
                                context)


class WorkItemWidget(ForeignKeyWidget):
    def clean(self, value):
        return self.model.objects.get(title = value)


class WorkItemResource(resources.ModelResource):
   
    formats = DEFAULT_FORMATS

    project_task = fields.Field(column_name='project_task', attribute='project_task',
                       widget=WorkItemWidget(ProjectTask, 'title'))

    class Meta:
        model = WorkItem
        skip_unchanged = True
        report_skipped = True
        import_id_fields = ('file_name',)
        fields = ('project_task','file_name','file_path',)
        export_order = ('project_task','file_name','file_path')
        widgets = {
            'published': {'format': '%d.%m.%Y'},
            }


class ProjectTaskWidget(ForeignKeyWidget):
    def clean(self, value):
        return self.model.objects.get(project_task__title = value)

from .models import ProjectTaskTemplate

class WorkItemAssignmentResource(resources.ModelResource):

    #project_task_name = ProjectTask.objects.get(project)

    #project_task_template = ProjectTaskTemplate.objects.get(project='')

    project_task = fields.Field(column_name='project_task', attribute='project_task',
                       widget=ProjectTaskWidget(WorkItem, field='project_task'))

    folder_name = fields.Field(column_name='folder_name', attribute='folder_name',
                        widget=ForeignKeyWidget(WorkItem, field='folder_name'))

    file_name = fields.Field(column_name='file_name', attribute='file_name',
                        widget=ForeignKeyWidget(WorkItem, field='file_name'))


    number_of_items = fields.Field(column_name='number_of_items', attribute='number_of_items',
                       widget=ForeignKeyWidget(WorkItem, field ='number_of_items'))



    custom_field1 = fields.Field(column_name='custom_field1_title', attribute='custom_field1',
                       widget=ForeignKeyWidget(WorkItem, field ='custom_field1'))


    custom_field2 = fields.Field(column_name='custom_field2_title', attribute='custom_field2',
                       widget=ForeignKeyWidget(WorkItem, field ='custom_field2'))




    lead = fields.Field(column_name='lead', attribute='lead',
                       widget=ForeignKeyWidget(Employee, 'name'))

    agents = fields.Field(column_name='agents', attribute='agents',
                       widget=ManyToManyWidget(Employee, separator="/",field='name'))


    class Meta:
        model = WorkItemAssignment
        skip_unchanged = True
        report_skipped = True

        import_id_fields = ('workitem',)
        fields = ('workitem','lead','agents',)
        export_order = ('workitem','lead','agents',)