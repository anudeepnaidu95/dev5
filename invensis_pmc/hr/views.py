from __future__ import unicode_literals
import json
from django.db import IntegrityError
from django.shortcuts import render, get_object_or_404
from django.utils.translation import ugettext_lazy as _
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest
from django.contrib import messages
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required
# Create your views here.




@login_required
def users_list(request):

	user_list = User.objects.all().order_by('id')
	return render(request, 'hr/user_list_partial.html', 
					{'user_list': user_list}
				)

@login_required
def user_add(request):
	form = forms.UserForm(request.POST)

	if request.method == 'POST':
		if form.is_valid():
			user = form.save(commit=False)

			user.save()

			return HttpResponse('Successfully Created User ')
		else:
			error_dict={}
			for error in form.errors:
				error_dict[error] = form.errors[error]
				
			return HttpResponseBadRequest(json.dumps(error_dict))
	else:
		form = forms.UserForm()

		return render(request, 'project/service_type_add_partial.html', {'form':form})


@login_required
def users_edit(request, id):

	if request.method == "POST":
		form = forms.UserForm(request.POST, instance=request.user)
		if form.is_valid():
			user = form.save(commit=False)
			user.save()

			return HttpResponse('Successfully Updated user information ')
		else:
			error_dict={}
			for error in form.errors:
				error_dict[error] = form.errors[error]
				
			return HttpResponseBadRequest(json.dumps(error_dict))
	else:
		form = form1.ServiceTypeForm(instance=post)
	return render(request, 'project/service_type_add_partial.html', {'form': form, 'is_edit_mode' : True , 'slug' : slug,})
