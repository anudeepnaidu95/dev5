from django.shortcuts import render

# Create your views here.
"""
This is an example view in views.py that shows all logged users
"""
from django.shortcuts import render_to_response
from django.template import RequestContext
from myutils.models import UserAudit

def logged(request):
  logged_users = UserAudit.objects.all().order_by('username')
  return render_to_response('account/logged_users.html',
                            {'logged_users': logged_users},
                            context_instance=RequestContext(request))