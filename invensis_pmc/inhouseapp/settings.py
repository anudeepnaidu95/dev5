# -*- coding: utf-8 -*-
from __future__ import unicode_literals
"""
Django settings for inhouseapp project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import logging
from datetime import datetime

from django.conf.global_settings import TEMPLATE_CONTEXT_PROCESSORS as TCP
from django.utils.translation import ugettext_lazy as _
from django.contrib.messages import constants as message_constants


BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 's56(l4fgje&*$f_pyk^b7-30sbdh(yeleyq0z%z^-_d$ak$q5%'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1', 'localhost    ']


DJANGO_LOGGER = logging.getLogger('django')
APPLICATION_LOGGER = logging.getLogger('application')
LOGIC_LOGGER = logging.getLogger('logic')

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'inhouseapp.info@gmail.com'
EMAIL_HOST_PASSWORD = 'inhouseapp123'
EMAIL_PORT = 587
EMAIL_USE_TLS = True

# Email configuration
#EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
#EMAIL_HOST = 'localhost'
#EMAIL_PORT = 1025

#EMAIL_HOST_USER = 'user'
#EMAIL_HOST_PASSWORD = 'password'
ADMINS = (
    ('siddu', 'revansbiradar@gmail.com'),
)
MANAGERS = ADMINS


# Application definition

INSTALLED_APPS = (
    'suit',
    'django_select2',
    'social.apps.django_app.default',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_extensions',
    'import_export',
    'crispy_forms',
    'inhouseapp',
    'account',
    'project',
    'employee',
    'customer',
    'invoice',
    'support',
    'mptt',
    'hr',
    'myutils',
    'dashboard',
    'django_filters',
    #'pagination',

)

CRISPY_TEMPLATE_PACK = 'bootstrap3'

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    # 'inhouseapp.middleware.CoreMiddleware',

)



AUTHENTICATION_BACKENDS = (
    'social.backends.google.GoogleOAuth2',
    'social.backends.facebook.Facebook2OAuth2',
    'social.backends.twitter.TwitterOAuth',
    'django.contrib.auth.backends.ModelBackend',
)

ROOT_URLCONF = 'inhouseapp.urls'

WSGI_APPLICATION = 'inhouseapp.wsgi.application'


CRISPY_TEMPLATE_PACK = 'bootstrap3'
# Auth

AUTH_PROFILE_MODULE = 'account.Profile'
LOGIN_URL = '/account/login/'
LOGOUT_URL = '/account/logout/'
ANONYMOUS_USER_ID = -1

# Message

MESSAGE_TAGS = {
    message_constants.DEBUG: 'debug',
    message_constants.INFO: 'info',
    message_constants.SUCCESS: 'success',
    message_constants.WARNING: 'warning',
    message_constants.ERROR: 'danger'
}

# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases


# DATABASES = {
#    'default': {
#        'ENGINE': 'django.db.backends.sqlite3',
#        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#    }
# }

#DATABASES = {
#   'default': {
#        'ENGINE': 'django.db.backends.postgresql_psycopg2', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
#        'NAME': 'inhouseapp_final',                      # Or path to database file if using sqlite3.
#        # The following settings are not used with sqlite3:
#        'USER': 'inhouseapp_final',
#        'PASSWORD': 'inhouseapp_final',
#        'HOST': '127.0.0.1',                      # Empty for localhost through domain sockets or           '127.0.0.1' for localhost through TCP.
#        'PORT': '',                      # Set to empty string for default.
#    }
#}
#
DATABASES = {
    'default': {
         'ENGINE': 'django.db.backends.postgresql_psycopg2', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
         'NAME': 'inhouseapp',                      # Or path to database file if using sqlite3.
         # The following settings are not used with sqlite3:
         'USER': 'inhouseapp',

         'PASSWORD': 'inhouseapp123',

         'HOST': '127.0.0.1',                      # Empty for localhost through domain sockets or           '127.0.0.1' for localhost through TCP.
         'PORT': '',                      # Set to empty string for default.
     }
 }
# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Kolkata'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'assets/static'),
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
  
    )

STATIC_URL = '/static/'

STATIC_ROOT = "/home/dev1/www/inhouseapp/static/"

CURRENT_PATH = os.path.abspath(os.path.dirname(__file__).decode('utf-8'))

 

MEDIA_ROOT = os.path.join(BASE_DIR, 'assets/media/')

MEDIA_URL = '/media/'



# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    #     'django.template.loaders.eggs.load_template_source',
)



TEMPLATE_CONTEXT_PROCESSORS = TCP + [
    'django.core.context_processors.request',
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.request',
    'django.contrib.messages.context_processors.messages',
    'django.core.context_processors.i18n',
    'social.apps.django_app.context_processors.backends',
    'social.apps.django_app.context_processors.login_redirect',
    ]

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(CURRENT_PATH, 'templates'),
)



# Logging

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': "[%(asctime)s %(name)s-%(levelname)s (%(filename)s:%(lineno)s %(funcName)s)]: %(message)s",
            'datefmt': "%d/%b/%Y %H:%M:%S"
        },
        'simple': {
            'format': '[%(asctime)s %(name)s-%(levelname)s]: %(message)s',
            'datefmt': "%d/%b/%Y %H:%M:%S"
        },
    },
    'handlers': {
        'file-django': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'assets/logs/django.log'),
            'formatter': 'verbose'
        },
        'file-application': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'assets/logs/application.log'),
            'formatter': 'verbose'
        },
        'file-logic': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'assets/logs/logic.log'),
            'formatter': 'simple'
        },
    },
    'loggers': {
        # 'django': {
        #     'handlers': ['file-django'],
        #     'propagate': True,
        #     'level': 'DEBUG',
        # },
        'application': {
            'handlers': ['file-application'],
            'propagate': True,
            'level': 'DEBUG',
        },
        'logic': {
            'handlers': ['file-logic'],
            'propagate': True,
            'level': 'DEBUG',
        },
    }
}




# Application Configuration

APPLICATION_URL = 'http://localhost:8000'

APPLICATION_CONFIG = {
    'title': _('Inhouseapp'),
    'short_title': _('EP'),
    'header': _('Employee Performance'),
    #'slogan': _('Code while alive!'),
    'description': _('Project Description.'),

    'copyright': "&copy; {} <a href='http://invensis.net'>asdf.</a>".format(datetime.now().year),
    'google_account': 'google.com/+inhouseapp',
    'facebook_account': 'facebook.com/inhouseapp',
    'twitter_account': '@inhouseapp',
    'google_id': 'google-id',
    'facebook_id': 'facebook-id',
    'twitter_id': 'twitter-id',
    'date_format': 'DD/MM/YYYY HH:mm'
}
APPLICATION_CONTENT_COUNT = 10
APPLICATION_CONTENT_MAXIMUM_COUNT = 20
APPLICATION_DUMMY_DATA_COUNT = 7
APPLICATION_FROM_EMAIL = 'Title <revansbiradar@gmail.com>'
APPLICATION_EMAIL_MANUAL_TIMEOUT = 3  # In minutes
APPLICATION_MONITORING = DEBUG
APPLICATION_MONITOR_STUFF_USERS = DEBUG




#suit config

SUIT_CONFIG = {
    # header
     'ADMIN_NAME': 'PMC',
     'HEADER_DATE_FORMAT': 'l, j, F Y',
     'HEADER_TIME_FORMAT': 'H:i A',

    # forms
     'SHOW_REQUIRED_ASTERISK': True,  # Default True
     'CONFIRM_UNSAVED_CHANGES': True, # Default True

    # menu
     'SEARCH_URL': '/admin/auth/user/',
     'MENU_ICONS': {
        'sites': 'icon-leaf',
        'auth': 'icon-lock',
     },
     'MENU_OPEN_FIRST_CHILD': True, # Default True
     #'MENU_EXCLUDE': ('auth.group',),
     'MENU': (
        'sites',
       
        {'app': 'inhouseapp','label': 'Settings', 'icon': 'icon-cog', 'models': (
            {'model': 'inhouseapp.settings', 'label': 'Setting'},
            {'model': 'inhouseapp.event', 'label': 'Events'},
            {'model': 'inhouseapp.log', 'label': 'Logs'},
            {'model': 'inhouseapp.request', 'label': 'Requests'},

        )},

        # Account
    
        {'app': 'account','label': 'Accounts', 'icon': 'icon-lock', 'models': (
            {'url': 'auth.user','permissions': 'auth.add_user', 'label': 'User'},
            {'model': 'account.profile', 'label': 'Profile'},
            {'url': 'auth.group', 'permissions': 'auth.add_group','label': 'Group'},
            {'model': 'account.request', 'label': 'Requests'},
        )},
         # Hr
    
        {'app': 'hr','label': 'Hr', 'icon': 'icon-th','models': (
            {'model': 'hr.employeeleave','label': 'EmployeeLeaves'},
            {'model': 'hr.financialyear','label': 'FinancialYears'},
            {'model': 'hr.holiday', 'label': 'Holidays'},
            {'model': 'hr.notification','label': 'Notifications'},

        )},
           #employees
      
        {'app': 'employee','label': 'Employees', 'icon': 'icon-user', 'models': (
            {'model': 'employee.employee', 'label': 'Employees', },
            # {'model': 'employee.organization', 'label': 'Organizations', },
            {'model': 'employee.department', 'label': 'Departments',},
            {'model': 'employee.role', 'label': 'Roles',  },
            {'model': 'employee.ExperienceSlab', 'label': 'ExperienceSlabs',},

        )},
        # Customer
    
         {'app': 'customer','label': 'Customers','icon': 'icon-user','models': (
            {'model':'customer.lead','label': 'Enquirys'},
            {'model':'customer.customer','label': 'Customers'},
            {'model':'customer.followup','label': 'Followups'},
            {'model':'customer.country','label': 'Countrys'},
         )},

        #project
     

      
        {'app': 'project','label': 'Project Management', 'icon': 'icon-folder-open', 'models': (
            {'model': 'project.project', 'label': 'Projects',},

            {'model': 'project.industry','label': 'Industry', },
            {'model': 'project.ServiceType', 'label': 'ServiceType'},
            {'model': 'project.projectservice', 'label': 'Project-Services',},
            {'model': 'project.projecttask', 'label': 'ProjectTasks',},
            {'model': 'project.projecttype', 'label': 'ProjectTypes',},
            {'model': 'project.projectplanresource', 'label': 'ResourcePlan', },
            
            {'model': 'project.billingtype', 'label': 'BillingTypes',},
            {'model': 'project.workitemstatus', 'label': 'WorkItemStatus', },
            {'model': 'project.qcstatus', 'label': 'QcStatus', },


            {'model': 'project.ProjectTaskTemplate', 'label': 'ProjectTaskTemplates',},

            {'model': 'project.ProjectWorkItemTemplate', 'label': 'ProjectWorkItemTemplates', },
            {'model': 'project.QcAttributeTemplate', 'label': 'QcAttributeTemplates', },
            
            
        )},

     
        {'app': 'project','label': 'WorkAssignment', 'icon': 'icon-tasks', 'models': (
            
            {'model': 'project.workitem', 'label': 'WorkItems'},
         
            {'model': 'project.NormalWorkItemAssignment', 'label': 'DailyTask',},
            {'model': 'project.QcWorkItemAssignment', 'label': 'QcAssignment', },
            {'model': 'project.QcAttribute', 'label': 'QcAttributes', },
        )},


          #invoices

        {'app': 'invoice','label': 'Invoices', 'icon': 'icon-book', 'models': (
            {'model': 'invoice.invoice', 'label': 'Invoices'},
            {'model': 'invoice.invoicelineitem', 'label': 'InvoiceLineItems'},
        )},

        #Support

        {'app': 'support','label': 'Support', 'icon': 'icon-question-sign', 'models': (
            {'model': 'support.conversation', 'label': 'Conversations'},
            {'model': 'support.querystatus', 'label': 'QueryStatuss'},
            {'model': 'support.query', 'label': 'Querys'},
        )},
      
    ),
    # misc
    'LIST_PER_PAGE': 50
}



# SOCIAL AUTH

SOCIAL_AUTH_URL_NAMESPACE = 'social'
SOCIAL_AUTH_ADMIN_USER_SEARCH_FIELDS = ['username', 'first_name', 'email', ]

SOCIAL_AUTH_FACEBOOK_KEY = 'facebook-key'
SOCIAL_AUTH_FACEBOOK_SECRET = 'facebook-secret'
SOCIAL_AUTH_FACEBOOK_SCOPE = ['email', ]

SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = 'google-key'
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = 'google-secret'
SOCIAL_AUTH_GOOGLE_OAUTH2_SCOPE = ['https://www.googleapis.com/auth/plus.me',
                                   'https://www.googleapis.com/auth/userinfo.email',
                                   'https://www.googleapis.com/auth/userinfo.profile', ]

SOCIAL_AUTH_TWITTER_KEY = 'twitter-key'  # Consumer Key
SOCIAL_AUTH_TWITTER_SECRET = 'twitter-secret'  # Consumer Secret



# prod postgres pwd
# inhouseapp_prod
# inhouseapp_prod
# dd8c08d71a82f5c79e25384171c18fa8