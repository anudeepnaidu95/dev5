from django import forms
from dashboard import models


class DashboardSetupForm(forms.ModelForm):
	"""docstring for DashboardSetupForm"""

	class Meta:
		model = models.DashboardSetup
		fields = '__all__'

		

class RevenueSetupForm(forms.ModelForm):
	"""docstring for RevenueSetupForm"""

	class Meta:
		model = models.QuerterRevenueSetup
		fields = '__all__'