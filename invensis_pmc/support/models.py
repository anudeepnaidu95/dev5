from django.db import models
from django_extensions.db.models import TimeStampedModel, TitleDescriptionModel
from customer.models import Customer
from employee.models import Employee
from project.models import Project, ProjectTask

#shd this be an enum?
class QueryStatus(TitleDescriptionModel):

	class Meta:
	    verbose_name = "QueryStatus"
	    verbose_name_plural = "QueryStatuss"

	def __str__(self):
		return self.title

# who will be  responding to queries ???
# assumption: ops manager
class Query(TimeStampedModel):

	subject = models.CharField( max_length=255, blank=True,null=True)
	customer =  models.ForeignKey(Customer)
	project = models.ForeignKey(Project)
	task =  models.ForeignKey(ProjectTask)
	query_status = models.ForeignKey(QueryStatus)


	class Meta:
	    verbose_name = "Query"
	    verbose_name_plural = "Querys"

	def __str__(self):
	    return self.subject
    
class Conversation(TimeStampedModel):
	query =  models.ForeignKey(Query)
	body = models.TextField(blank=True, null=True)

	customer = models.ForeignKey(Customer, blank=True, null=True)
	employee = models.ForeignKey(Employee, blank=True,null=True)

	class Meta:
	    verbose_name = "Conversation"
	    verbose_name_plural = "Conversations"

	def __str__(self):
		return str(self.id)
    