# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.conf import settings
from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView, RedirectView
from django.views.decorators.cache import cache_page
from django.templatetags.static import static
from django.contrib import admin
from django.contrib.sitemaps import views as sitemaps_views
from django.contrib.auth.signals import user_logged_in, user_logged_out  
from myutils.views import logged
from myutils.models import login_user, logout_user
from . import sitemaps as inhouseapp_sitemaps
#from inhouseapp.admin import admin_site

admin.autodiscover()

user_logged_in.connect(login_user)
user_logged_out.connect(logout_user)

# Root url patterns
urlpatterns = patterns('',
    # Admin and 3rd party applications
    url(r'^admin/', include(admin.site.urls)),
    url(r'^social/', include('social.apps.django_app.urls', namespace='social')),
    url(r'^select2/', include('django_select2.urls')),
    # inhouseapp

    url(r'^$', 'inhouseapp.views.home', name='home'),
    url(r'^about/$', 'inhouseapp.views.about', name='about'),
    url(r'^error/400/$', 'inhouseapp.views.error_400', name='error_400'),
    url(r'^error/403/$', 'inhouseapp.views.error_403', name='error_403'),
    url(r'^error/404/$', 'inhouseapp.views.error_404', name='error_404'),
    url(r'^error/500/$', 'inhouseapp.views.error_500', name='error_500'),

    url(r'^static-page/$', TemplateView.as_view(template_name='user/inhouseapp/static_page.html'), name='static_page'),
    url(r'^debug/$', 'inhouseapp.views.debug', name='debug'),
    #url(r'^language/(?P<code>\w+)/$', 'inhouseapp.views.language', name='language'),
   
    url(r'audits/$','myutils.views.logged', name='logged_users'),

    # Applications
    url(r'^account/', include('account.urls')),
    url(r'^c/', include('customer.urls')),
    url(r'^e/', include('employee.urls')),
    url(r'^p/', include('project.urls')),
    url(r'^h/', include('hr.urls')),
    url(r'^i/', include('invoice.urls')),
    url(r'^s/', include('support.urls')),
    url(r'^d/',include('dashboard.urls')),


    # SEO
    #url(r'^favicon\.ico$', RedirectView.as_view(url=static('favicon.ico'), permanent=True), name="favicon.ico"),
    #url(r'^robots\.txt$', RedirectView.as_view(url=static('robots.txt'), permanent=True), name="robots.txt"),
    #url(r'^sitemap\.xml$',
     #   cache_page(60 * 10)(sitemaps_views.index),  # cache for 10 minutes
      #  {'sitemaps': inhouseapp_sitemaps.sitemaps_dict}),
    #url(r'^sitemap-(?P<section>.+)\.xml$',
     #   cache_page(60 * 10)(sitemaps_views.sitemap),  # cache for 10 minutes
      #  {'sitemaps': inhouseapp_sitemaps.sitemaps_dict}),
)

# Serve static files
urlpatterns += patterns('',
    url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
)

# Serve media files
urlpatterns += patterns('',
    #url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),

    url(r'^media/(?P<path>.*)$', 'project.views.service_document_download', {'document_root': settings.MEDIA_ROOT}),

    

)

# Configure error handlers
handler400 = 'inhouseapp.views.error_400'  # Request cannot be fulfilled due to bad syntax
handler403 = 'inhouseapp.views.error_403'  # Server refuses to respond to request
handler404 = 'inhouseapp.views.error_404'  # Requested resource could not be found
handler500 = 'inhouseapp.views.error_500'  # Server generic error message

