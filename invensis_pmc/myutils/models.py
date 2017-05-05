from __future__ import unicode_literals
import datetime
from django.db import models
from django.contrib.auth.signals import user_logged_in, user_logged_out 

EVENT_TYPES = (
	('LOGIN','Login'),
	('LOGOUT','Logout'),
	('PWD_CHANGE','Password Change'),
	# ('',''),
	# ('',''),

	)

# Create your models here.
class UserAudit(models.Model):
	username = models.CharField(max_length=30, primary_key=True)
	event = models.CharField(choices=EVENT_TYPES, max_length=20)
	created = models.DateTimeField(auto_now_add=True)
	ip_address = models.CharField( max_length=20)

	def __unicode__(self):
		return self.username

def login_user(sender, request, user, **kwargs):
	x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
	if x_forwarded_for:
		ip = x_forwarded_for.split(',')[0]
	else:
		ip = request.META.get('REMOTE_ADDR')

	UserAudit(username=user.username, event='Login', ip_address=ip, created=datetime.datetime.now().strftime("%Y-%m-%d %H:%M")).save()

def logout_user(sender, request, user, **kwargs):
	x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
	if x_forwarded_for:
		ip = x_forwarded_for.split(',')[0]
	else:
		ip = request.META.get('REMOTE_ADDR')

	UserAudit(username=user.username, event='Logout', ip_address=ip, created=datetime.datetime.now().strftime("%Y-%m-%d %H:%M")).save()
	
	# try:
	# 	u = UserAudit.objects.get(pk=user.username)
	# 	u.delete()
	# except UserAudit.DoesNotExist:
	# 	pass

		