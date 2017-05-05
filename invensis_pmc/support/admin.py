# -*- coding: utf-8 -*-
from django.contrib import admin

from .models import QueryStatus, Query, Conversation
from .forms import ConversationAdminForm,QueryAdminForm,ConversationInlineForm

class QueryStatusAdmin(admin.ModelAdmin):
    list_display = (u'id', 'title', 'description')
admin.site.register(QueryStatus, QueryStatusAdmin)



class ConversationInline(admin.TabularInline):
    '''
    Tabular Inline View for Conversation
    '''
    model = Conversation
    # min_num = 3
    # max_num = 20
    extra = 1
    # raw_id_fields = (,)

    list_display = (
        u'id',
        'created',
        'modified',
        'query',
        'body',
        'customer',
        'employee',
    )
    list_filter = ('created', 'modified', 'query', 'customer', 'employee')
    form=ConversationInlineForm

class QueryAdmin(admin.ModelAdmin):
    inlines = (ConversationInline,)
    list_display = (
        u'id',
        'created',
        'modified',
        'subject',
        'customer',
        'project',
        'task',
        'query_status',
    )
    list_filter = (
        'created',
        'modified',
        'customer',
        'project',
        'task',
        'query_status',
    )
    form=QueryAdminForm
admin.site.register(Query, QueryAdmin)


class ConversationAdmin(admin.ModelAdmin):
    list_display = (
        u'id',
        'created',
        'modified',
        'query',
        'body',
        'customer',
        'employee',
    )
    list_filter = ('created', 'modified', 'query', 'customer', 'employee')
    form=ConversationAdminForm
admin.site.register(Conversation, ConversationAdmin)

