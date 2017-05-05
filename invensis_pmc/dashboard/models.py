from __future__ import unicode_literals

from django.db import models

# Create your models here.

class DashboardSetup(models.Model):
	"""docstring for DashboardSetup"""
	start_date = models.DateField(blank=True, null=True)
	end_date = models.DateField(blank=True, null=True)
	
		

class QuerterRevenueSetup(models.Model):
	"""docstring for QuerterRevenueSetup"""
	red_region = models.IntegerField(default=0, blank=True, null=True)
	yellow_region = models.IntegerField(default=0, blank=True, null=True)
	green_region = models.IntegerField(default=0, blank=True, null=True)


		