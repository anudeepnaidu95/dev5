from django.db import models
from django_extensions.db.models import TitleSlugDescriptionModel, \
	TitleDescriptionModel, TimeStampedModel
from model_utils.models import TimeFramedModel
from employee.models import Employee


class FinancialYear(TitleSlugDescriptionModel):


	class Meta:
	    verbose_name = "FinancialYear"
	    verbose_name_plural = "FinancialYears"

	def __str__(self):
	    return self.title


# Create your models here.
class Holiday(TitleSlugDescriptionModel):

	financial_year = models.ForeignKey(FinancialYear)
	date = models.DateField()


	class Meta:
	    verbose_name = "Holiday"
	    verbose_name_plural = "Holidays"

	def __str__(self):
	    return self.title
    
class Notification(TitleSlugDescriptionModel, TimeStampedModel):

	message = models.TextField()


	class Meta:
	    verbose_name = "Notification"
	    verbose_name_plural = "Notifications"

	def __str__(self):
	    return self.title
    


# is leave approved by manager or hr
class EmployeeLeave(TimeFramedModel):

	manager = models.ForeignKey(Employee, related_name='+')

	employee = models.ForeignKey(Employee, related_name='+')

	reason = models.TextField()
	is_approved = models.BooleanField(default=False)



	class Meta:
	    verbose_name = "EmployeeLeave"
	    verbose_name_plural = "EmployeeLeaves"

	def __str__(self):
	    return str(self.id)

