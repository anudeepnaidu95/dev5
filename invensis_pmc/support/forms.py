# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django import forms
from .models import QueryStatus, Query, Conversation
from django_select2.forms import ModelSelect2Widget



class MyWidget(ModelSelect2Widget):
    search_fields = [
        'title__icontains',
    ]

class MyTaskWidget(ModelSelect2Widget):
    search_fields = [
        'name__icontains',
    ]

class ConversationAdminForm(forms.ModelForm):
    class Meta:
    	model=Conversation
        fields = '__all__'
        widgets = {
            'customer': MyWidget,
            'employee':MyTaskWidget,
        }


class QueryAdminForm(forms.ModelForm):
    class Meta:
    	model=Query
        fields = '__all__'
        widgets = {
            'customer': MyWidget,
            'project':MyWidget,
            'task':MyWidget,
        }

        
class ConversationInlineForm(forms.ModelForm):
    class Meta:
    	model=Conversation
        fields = '__all__'
        widgets = {
            'customer': MyWidget,
            'employee':MyTaskWidget,
            
        }

def get_urls(self):
        urls = super(WorkItemAssignmentAdmin,self).get_urls()
        add_urls = [
                url(r'upload/$', self.admin_site.admin_view(self.upload), name='project_normalworkitemassignment_upload')
        ]
        return add_urls + urls

def upload(self,request):

    context = {
        'title': 'Upload DailyTasks',
        'app_label': self.model._meta.app_label,
        'opts': self.model._meta,
        'has_change_permission': self.has_change_permission(request)
    }

    # Handle form request
    if request.method == "POST":
        form = ImportDailyTasksForm(request.POST, request.FILES)
        if form.is_valid():

            file = form.cleaned_data['file']
            fields, data_lines = csvimporter.handle_uploaded_file(file)
            csv_result, rows_error, rows_updated = csvimporter.create_dailytasks_in_db(data_lines)

            if csv_result:
                message = 'Successfully imported %d Work items from the csv file to the database.\n' %len(rows_updated)
                #message += 'The system is creating Active Directory Accounts using those information in the background.\n'
                message += 'Please wait...'
                messages.add_message(request, messages.INFO, message)
                context['result'] = csv_result
                context['rows_updated'] = rows_updated

                return HttpResponseRedirect("../")

            else:
                message = 'There are some %d errors occured. Please try again.' %len(rows_error)
                messages.add_message(request, messages.INFO, message)
                context['rows_error'] = rows_error
            
    else:
        form = ImportDailyTasksForm()
    # Render the template.

    context['form'] = form

    context['adminform'] = helpers.AdminForm(form, list([(None, {'fields': form.base_fields})]),
                                             self.get_prepopulated_fields(request))

    return render(request, 'admin/project/projecttask/upload.html', context)


def customfield_to_field(self, field, instanceargs):
        if field.data_type == 'varchar':
            fieldclass = forms.CharField
            instanceargs['max_length'] = field.max_length
        elif field.data_type == 'text':
            fieldclass = forms.CharField
            instanceargs['widget'] = forms.Textarea
            instanceargs['max_length'] = field.max_length
        elif field.data_type == 'integer':
            fieldclass = forms.IntegerField
        elif field.data_type == 'decimal':
            fieldclass = forms.DecimalField
            instanceargs['decimal_places'] = field.decimal_places
            instanceargs['max_digits'] = field.max_length
        elif field.data_type == 'list':
            fieldclass = forms.ChoiceField
            choices = field.choices_as_array
            if field.empty_selection_list:
                choices.insert(0, ('','---------' ) )
            instanceargs['choices'] = choices
        elif field.data_type == 'boolean':
            fieldclass = forms.BooleanField
        elif field.data_type == 'date':
            fieldclass = forms.DateField
        elif field.data_type == 'time':
            fieldclass = forms.TimeField
        elif field.data_type == 'datetime':
            fieldclass = forms.DateTimeField
        elif field.data_type == 'email':
            fieldclass = forms.EmailField
        elif field.data_type == 'url':
            fieldclass = forms.URLField
        elif field.data_type == 'ipaddress':
            fieldclass = forms.IPAddressField
        elif field.data_type == 'slug':
            fieldclass = forms.SlugField

        self.fields['custom_%s' % field.name] = fieldclass(**instanceargs)

