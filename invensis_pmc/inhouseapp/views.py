from django import http
from django.http import HttpResponseRedirect
from django.views.decorators.cache import cache_page
from django.utils.http import is_safe_url
from django.contrib.admin.views.decorators import staff_member_required
from inhouseapp.utils.decorators import log
from logic import ViewPage
from . import logic

''' Default pages '''


def home(request, template='inhouseapp/home.html', context=None):
    if not context:
        context = {}
    return render(request, template, context)



@cache_page(60 * 1)
def about(request, template='inhouseapp/about.html', context=None):
    if not context:
        context = {}
    return render(request, template, context)


''' Error pages '''


@cache_page(60 * 60)
def error_400(request, template='inhouseapp/error_400.html', context=None):
    if not context:
        context = {}
    return render(request, template, context)


@cache_page(60 * 60)
def error_403(request, template='inhouseapp/error_403.html', context=None):
    if not context:
        context = {}
    return render(request, template, context)


@cache_page(60 * 60)
def error_404(request, template='inhouseapp/error_404.html', context=None):
    if not context:
        context = {}
    return render(request, template, context)


@cache_page(60 * 60)
def error_500(request, template='inhouseapp/error_500.html', context=None):
    if not context:
        context = {}
    return render(request, template, context)


''' Core pages '''


def language(request, code):
    next = request.POST.get('next', request.GET.get('next'))
    if not is_safe_url(url=next, host=request.get_host()):
        next = request.META.get('HTTP_REFERER')
        if not is_safe_url(url=next, host=request.get_host()):
            next = '/'
    response = http.HttpResponseRedirect(next)
    #l = ViewPage(request)
    #l.set_language(code, response=response)
    return response


@staff_member_required
def debug(request, template='inhouseapp/debug.html', context=None):
    if not context:
        context = {}
    return render(request, template, context)



from django.shortcuts import render
