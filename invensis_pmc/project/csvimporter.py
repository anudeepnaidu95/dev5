# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import csv
from django.contrib import messages
from django.db import IntegrityError
from django.shortcuts import render_to_response
from django.template.defaultfilters import slugify
from inhouseapp.utils.helpers import unique_slugify
from project import models
from project import widgets
from django.db.models.fields.related import ForeignKey
from employee.models import Employee




class InsensitiveDictReader(csv.DictReader):
	# This class overrides the csv.fieldnames property, which converts all fieldnames without leading and trailing spaces and to lower case.

	@property
	def fieldnames(self):
		return [field.strip().lower() for field in csv.DictReader.fieldnames.fget(self)]

	def next(self):
		return InsensitiveDict(csv.DictReader.next(self))

class InsensitiveDict(dict):
	# This class overrides the __getitem__ method to automatically strip() and lower() the input key

	def __getitem__(self, key):
		return dict.__getitem__(self, key.strip().lower())



def handle_uploaded_file(file):

	file.seek(0)

	# !importtant
	# csv file must be encoded in UTF-8
	sniffdialect = csv.Sniffer().sniff(file.read(10000), delimiters='\t,;')
	file.seek(0)

	#print sniffdialect.fieldnames
	data = csv.reader(file, dialect=sniffdialect)
	#data.fieldnames = [field.strip().lower() for field in data.fields.next()]
	fields = data.next()
	data_lines = []

	for lineno, row in enumerate(data):
		items = dict(zip(fields, row))
		data_lines.append(items)

	return fields,  data_lines



def instance_dict(instance, key_format=None):
	"Returns a dictionary containing field names and values for the given instance"
	
	if key_format:
		assert '%s' in key_format, 'key_format must contain a %s'
	key = lambda key: key_format and key_format % key or key

	d = {}
	for field in instance._meta.fields:
		attr = field.name
		value = getattr(instance, attr)
		if value is not None and isinstance(field, ForeignKey):
			value = value._get_pk_val()
		d[key(attr)] = value
	for field in instance._meta.many_to_many:
		d[key(field.name)] = [obj._get_pk_val() for obj in getattr(instance, field.attname).all()]
	return d



def get_mapping_field(record, fieldname):

	for key, value in record.iteritems():
		#print "key-value data", (key, value)
		if key not in (None, ''):
			if key == fieldname:
				field_data = record[key]
				return field_data
		else:
			field_data = ''
			return field_data


def create_projecttask_in_db(data_dict):
	
	list_data = []
	newtasks = []
	updated_tasks = []
	rows_error = []
	created_project_tasks = []
	result = False
	#rows_error = 0
	rows_updated = []

	# gt all the prjs in csv***
	project_dict={}
	project_service_slug_dict = {}
	for record in data_dict:
		#print 'in loop 1'
		print record
		try:
			prj_slug = record['project']
			service_slug = record['project-service']
		except KeyError as e:
			reason = "{} not found, please check the {} name in CSV file, ".format(str(e), str(e).upper())
			if not reason in rows_error:
				rows_error.append(reason)
			continue

		if prj_slug in project_dict:
			pass
		else:
			project_dict[prj_slug] = prj_slug
	
		if not service_slug in project_service_slug_dict:
			project_service_slug_dict[service_slug] = service_slug

		

	services_slug = [key for key in project_service_slug_dict.keys()]
	
	project_services_dict = dict([(s.service.slug, s) for s in models.ProjectService.objects.filter(service__slug__in= services_slug)])

	print "print project services", project_services_dict

	project_slugs = [ key for key,value in project_dict.items()]
	# project_qs = models.Project.objects.get(title__in = project_slugs)

	get_project_dict = dict([(p.slug, p) for p in models.Project.objects.filter(slug__in=project_slugs)])

	project_task_template = models.ProjectTaskTemplate.objects.filter(project__slug__in= project_slugs)
	
	prj_task_tmpl_dict = dict([ (tmpl.project.slug, tmpl) for tmpl in project_task_template])	

	all_project_tasks_dict = dict([(p.slug, p) for p in models.ProjectTask.objects.all()])
	print "all_project_tasks_dict", all_project_tasks_dict

	for row_number, record in enumerate(data_dict):
		print '----------------record---------------'
		print record

		try:
			title = record['title']
			project = record['project']
			project_service = record['project-service']
		except KeyError as e:
			reason = "{} not found, please check the {} name in CSV file, ".format(str(e), str(e))
			if not reason in rows_error:
				rows_error.append(reason)
			continue

		try:
			get_project_service = project_services_dict[project_service]
			project_get = get_project_dict[project]

			prj_task_tmpl = prj_task_tmpl_dict[project]


		except KeyError as e:
			reason = "Row Number:-{} Reason:-{} not found, please check the {} name ".format(row_number, str(e), str(e))
			if not reason in rows_error:
				rows_error.append(reason)
			continue
			

		importing_fields_keys = [keys for keys in record.keys()]
		print "importing fields", importing_fields_keys
	
		custom_field1 = get_mapping_field(record, prj_task_tmpl.custom_field1_slug) 
		custom_field2 = get_mapping_field(record, prj_task_tmpl.custom_field2_slug) 
		custom_field3 = get_mapping_field(record, prj_task_tmpl.custom_field3_slug) 
		custom_field4 = get_mapping_field(record, prj_task_tmpl.custom_field4_slug) 
		custom_field5 = get_mapping_field(record, prj_task_tmpl.custom_field5_slug) 
		custom_field6 = get_mapping_field(record, prj_task_tmpl.custom_field6_slug)
		custom_field7 = get_mapping_field(record, prj_task_tmpl.custom_field7_slug) 
		custom_field8 = get_mapping_field(record, prj_task_tmpl.custom_field8_slug) 
		custom_field9 = get_mapping_field(record, prj_task_tmpl.custom_field9_slug)
		custom_field10 = get_mapping_field(record, prj_task_tmpl.custom_field10_slug) 


		projecttask_create = models.ProjectTask(project=project_get,\
												title=title,
												project_service = get_project_service,
												custom_field1 = custom_field1 ,
												custom_field2 = custom_field2,
												custom_field3 = custom_field3,
												custom_field4 = custom_field4,
												custom_field5 = custom_field5,
												custom_field6 = custom_field6,
												custom_field7 = custom_field7,
												custom_field8 = custom_field8,
												custom_field9 = custom_field9,
												custom_field10 = custom_field10,
											
										)
		list_data.append(projecttask_create)

		
		try:
			projecttask_create.save()
			newtasks.append((row_number, projecttask_create))
		except IntegrityError as e:
			#message = e.message
			reason = "Column Title should be unique for Project Service"
			reason += "\nRow Number :-- {} Reason :-- {}".format(row_number, str(e))
			rows_error.append(reason)

	#print "new records",newtasks
	if len(newtasks) == len(data_dict):
		for row in newtasks:
			if not row in rows_updated:
				rows_updated.append(record)
	
		result = True
	
	return result, rows_error, rows_updated




def create_workitems_in_db(dict_data):
	workitem_data = []
	created_workitem_data = []
	daily_task_data = []
	created_daily_tasks = []
	result = False
	rows_error = []
	rows_updated = []

	prj_task_slug_dict = {}
	workitem_slug_dict = {}
	lead_dict = {}
	agents_dict = {}
	# build slug from filename and foldername
	#print dict_data
	for record in dict_data:

		#project_task = record['project_task']
		try:
			file_name = record['file-name']
			folder_name = record['folder-name']
			prj_task = record['project-task']
		except KeyError as e:
			reason = "{} not found, please check the {} name in CSV file, ".format(str(e), str(e))
			if not reason in rows_error:
				rows_error.append(reason)
			pass

		slug_str =  "%s-%s" % (folder_name, file_name)
		slug = slugify( "%s" % slug_str)
		#slug = None
		if slug in workitem_slug_dict:
			pass
		else:
			workitem_slug_dict[slug] = slug

		if prj_task in prj_task_slug_dict:
			pass
		else:
			prj_task_slug_dict[prj_task] = prj_task

		try:
			lead = record['lead']
			agents = record['agents'].split('/')

			if not lead in lead_dict:
				lead_dict[lead] = lead
			for agent in agents:
				if not agent in agents_dict:
					agents_dict[agent] = agent

		except KeyError:
			pass


	prj_tasks =[ k for k,v in prj_task_slug_dict.items()]
	print "print project tasks",prj_tasks

	project_task_qs = models.ProjectTask.objects.filter(slug__in= prj_tasks).select_related('project')
	print "print project_task_qs",project_task_qs

	prj_task_dict = dict([(task.slug, task) for task in project_task_qs])	

	prj_task_slugs = [ task.slug for task in project_task_qs]
	print "project task slugs", prj_task_slugs
	prj_dict = {}

	project_slugs_dict = models.ProjectTask.objects.filter(slug__in=prj_task_slugs)
	pro_protask_slugs = dict([(p.slug, p.project.slug) for p in project_slugs_dict])

	print "pro_protask_slugs", pro_protask_slugs

	for task in project_task_qs:
		if task.project.slug in prj_dict:
			pass
		else:
			prj_dict[task.project.slug] = task.project.slug

	prj_slugs =[ k for k,v in prj_dict.items()]
	print "print  prj_slugs", prj_slugs

	get_project_dict = dict([ (p.slug, p.project) for p in models.ProjectTask.objects.filter(slug__in=prj_slugs)])
	print "printing get_project", get_project_dict

	project_workitem_template_qs = models.ProjectWorkItemTemplate.objects.filter(project__slug__in=prj_slugs).select_related('project')
	print "project_workitem_template_qs", project_workitem_template_qs

	workitem_tmpl_dict = dict([(tmpl.project.slug, tmpl) for tmpl in project_workitem_template_qs])	
	print " workitem_tmpl_dict", workitem_tmpl_dict

	workitem_slugs =[ k for k,v in workitem_slug_dict.items()]
	print "workitem_slugs", workitem_slugs

	# include proj task filter as well***
	workitem_qs= models.WorkItem.objects.filter(slug__in = workitem_slugs, project_task__slug__in =prj_task_slugs).select_related('project_task')
	print "workitem_qs", workitem_qs

	workitem_dict = {}
	workitem_dict = dict([ ("%s_%s" % (wi.project_task.slug , wi.slug) , wi) for wi in workitem_qs])
	print "workitem_dict", workitem_dict

	print "printing lead dict", lead_dict
	employ_leads = Employee.objects.filter(user__username__in=lead_dict)
	
	get_emp_lead =  dict([(u.user.username, u) for u in employ_leads])
	print "get_emp_lead", get_emp_lead

	employee_agents = Employee.objects.filter(user__username__in=agents_dict)

	get_emp_agents = dict([(u.user.username, u) for u in employee_agents])

	all_workitems_dict = dict([(item.file_name, item) for item in models.WorkItem.objects.all()])
	#print "all_workitems_dict", all_workitems_dict

	for row_number, record in enumerate(dict_data):

		try:
			project_task = record['project-task']
			file_name = record['file-name']
			folder_name = record['folder-name']
		except KeyError as e:
			reason = "{} not found, please check the {} name in CSV file, ".format(str(e), str(e))
			if not reason in rows_error:
				rows_error.append(reason)
			continue
			
		#print "--------------------------This is record ---------------------- "
		#print record

		try:
			prj_task = prj_task_dict[project_task]
			print prj_task
		except KeyError as e:
			reason = "Row Number:-- {} Reason :-- {}".format(row_number, str(e))
			reason +="Project task not found, please check the project task name"
			rows_error.append(reason)
			continue

		get_project_name = pro_protask_slugs[project_task]
		workitem_tmpl = workitem_tmpl_dict[get_project_name]
		#print " prin me workitem_tmpl", workitem_tmpl

		custom_field1 = get_mapping_field(record, workitem_tmpl.custom_field1_slug) 
		custom_field2 = get_mapping_field(record, workitem_tmpl.custom_field2_slug) 
		custom_field3 = get_mapping_field(record, workitem_tmpl.custom_field3_slug) 
		custom_field4 = get_mapping_field(record, workitem_tmpl.custom_field4_slug) 
		custom_field5 = get_mapping_field(record, workitem_tmpl.custom_field5_slug) 
		custom_field6 = get_mapping_field(record, workitem_tmpl.custom_field6_slug) 
		custom_field7 = get_mapping_field(record, workitem_tmpl.custom_field7_slug) 
		custom_field8 = get_mapping_field(record, workitem_tmpl.custom_field8_slug) 
		custom_field9 = get_mapping_field(record, workitem_tmpl.custom_field9_slug) 
		custom_field10 = get_mapping_field(record, workitem_tmpl.custom_field10_slug) 

		create_workitem = models.WorkItem(project_task =prj_task,
								   file_name=file_name, 
								   folder_name=folder_name, 
								   #number_of_items=number_of_items,
								   custom_field1 = custom_field1,
								   custom_field2 = custom_field2,
								   custom_field3 = custom_field3,
								   custom_field4 = custom_field4,
								   custom_field5 = custom_field5,
								   custom_field6 = custom_field6,
								   custom_field7 = custom_field7,
								   custom_field8 = custom_field8,
								   custom_field9 = custom_field9,
								   custom_field10 = custom_field10,

								)
		workitem_data.append(create_workitem)

		# build key from prjtask slug and workitem slug(filename, foldernhame)
		wi_slug = "%s-%s" % (folder_name,file_name)
		workitem_slug = slugify("%s" %wi_slug)
		prj_task_slug=None

		slug="%s_%s" % (prj_task_slug, workitem_slug)
		print "current workitem slug", workitem_slug

		if not slug in workitem_dict:		
			# create
			try:
				if not create_workitem in created_workitem_data:
					create_workitem.save()
					created_workitem_data.append(create_workitem)
					#print "printing data_item", create_workitem
				rows_updated.append(record)

			except IntegrityError as e:
				reason = "Row Number:--{},  Reason:--{}".format(row_number, str(e))
				reason += "\nColumns ProjectTask, Folder Name and File Name should be unique together"
				rows_error.append(reason)


		try:
			lead = record['lead']
			#agents = record['agents']
			associates = record['agents'].split('/')
			#print "printing associates", associates
	
			get_lead = get_emp_lead[lead]
			
			print "get workitem name", create_workitem 
			dailytasks = models.WorkItemAssignment(workitem=create_workitem, 
									   lead=get_lead,
									)

			try:
				if not dailytasks in daily_task_data:
					dailytasks.save()
					daily_task_data.append(dailytasks)

				for agent in associates:
					get_agent = get_emp_agents[agent]
					dailytasks.agents.add(get_agent)
			
				models.QcAttribute.objects.get_or_create(dailytask=dailytasks)
			except IntegrityError as e:
				reason = "Row{} Reason:{}".format(row_number, str(e))
				rows_error.append(reason)

		except KeyError as e:
			reason = "Row Number:-- {} Reason :-- {} not found, please check the {} name".format(row_number, str(e), str(e))
			#reason +="\n"
			rows_error.append(reason)

		except Exception as e:
				reason = "Row Number:-- {} Reason :-- {}".format(row_number, str(e))
				#reason +="\nLead not found, please check the lead name"
				rows_error.append(reason)


	if created_workitem_data:
		if len(created_workitem_data) == len(dict_data): 
			if not rows_error:
				result = True

	elif daily_task_data:
		if len(daily_task_data) == len(dict_data):
			if not rows_error:
				result = True
	

	return result, rows_error, rows_updated

def create_dailytasks_in_db(dict_data):
	daily_task_data = []
	created_daily_tasks = []
	result = False
	rows_error = []
	rows_updated = []

	workitems_dict = {}
	lead_dict = {}
	agents_dict = {}

	for record in dict_data:

		#project_task = record['project_task']
		try:
			item = record['workitem']
			if not item in workitems_dict:
				workitems_dict[item] = item

		except KeyError as e:
			reason = "{} not found, please check the {} name in CSV file, ".format(str(e), str(e))
			if not reason in rows_error:
				rows_error.append(reason)
			pass

		
		try:
			lead = record['lead']
			agents = record['agents'].split('/')

			if not lead in lead_dict:
				lead_dict[lead] = lead
			for agent in agents:
				if not agent in agents_dict:
					agents_dict[agent] = agent

		except KeyError as e:
			reason = "{} not found, please check the {} name in CSV file, ".format(str(e), str(e))
			if not reason in rows_error:
				rows_error.append(reason)
			pass

	get_workitems = [key for key, value in workitems_dict.items()]
	print "get_workitems", get_workitems

	all_workitems_dict = dict([(w.file_name, w) for w in models.WorkItem.objects.filter(file_name__in=get_workitems)])
	print "all_workitems_dict", all_workitems_dict

	print "printing lead dict", lead_dict
	employ_leads = Employee.objects.filter(user__username__in=lead_dict)

	get_emp_lead =  dict([(u.user.username, u) for u in employ_leads])
	print "get_emp_lead", get_emp_lead

	employee_agents = Employee.objects.filter(user__username__in=agents_dict)

	get_emp_agents = dict([(u.user.username, u) for u in employee_agents])


	for row_number, record in enumerate(dict_data):


		try:
			workitem = record['workitem']
			lead = record['lead'].strip('')
			associates = record['agents'].split('/')

			get_workitem = all_workitems_dict[workitem]
			get_lead = get_emp_lead[lead]
		except KeyError as e:
			reason = "{} not found, please check the {} name in CSV file, ".format(str(e), str(e))
			if not reason in rows_error:
				rows_error.append(reason)
			continue


		dailytasks = models.WorkItemAssignment(workitem=get_workitem,
									   lead=get_lead,
									)

		try:
			if not dailytasks in rows_updated:
				dailytasks.save()
				rows_updated.append(dailytasks)

			for agent in associates:
				get_agent = get_emp_agents[agent]
				dailytasks.agents.add(get_agent)
			models.QcAttribute.objects.get_or_create(dailytask=dailytasks)
		except IntegrityError as e:
			reason = "Row{} Reason:{}".format(row_number, str(e))
			rows_error.append(reason)

		except KeyError as e:
			reason = "{} not found, please check the {} name in CSV file, ".format(str(e), str(e))
			if not reason in rows_error:
				rows_error.append(reason)
			continue

	if rows_updated:
		if len(rows_updated) == len(dict_data):
			if not rows_error:
				result = True

	return result, rows_error, rows_updated




def create_dailytasks_in_db(dict_data):
	daily_task_data = []
	created_daily_tasks = []
	result = False
	rows_error = []
	rows_updated = []

	workitems_dict = {}
	lead_dict = {}
	agents_dict = {}

	for record in dict_data:

		#project_task = record['project_task']
		try:
			item = record['workitem']
			if not item in workitems_dict:
				workitems_dict[item] = item

		except KeyError as e:
			reason = "{} not found, please check the {} name in CSV file, ".format(str(e), str(e))
			if not reason in rows_error:
				rows_error.append(reason)
			pass

		
		try:
			lead = record['lead']
			agents = record['agents'].split('/')

			if not lead in lead_dict:
				lead_dict[lead] = lead
			for agent in agents:
				if not agent in agents_dict:
					agents_dict[agent] = agent

		except KeyError as e:
			reason = "{} not found, please check the {} name in CSV file, ".format(str(e), str(e))
			if not reason in rows_error:
				rows_error.append(reason)
			pass

	get_workitems = [key for key, value in workitems_dict.items()]
	print "get_workitems", get_workitems

	all_workitems_dict = dict([(w.file_name, w) for w in models.WorkItem.objects.filter(file_name__in=get_workitems)])
	print "all_workitems_dict", all_workitems_dict

	print "printing lead dict", lead_dict
	employ_leads = Employee.objects.filter(user__username__in=lead_dict)

	get_emp_lead =  dict([(u.user.username, u) for u in employ_leads])
	print "get_emp_lead", get_emp_lead

	employee_agents = Employee.objects.filter(user__username__in=agents_dict)

	get_emp_agents = dict([(u.user.username, u) for u in employee_agents])


	for row_number, record in enumerate(dict_data):


		try:
			workitem = record['workitem']
			lead = record['lead'].strip('')
			associates = record['agents'].split('/')

			get_workitem = all_workitems_dict[workitem]
			get_lead = get_emp_lead[lead]
		except KeyError as e:
			reason = "{} not found, please check the {} name in CSV file, ".format(str(e), str(e))
			if not reason in rows_error:
				rows_error.append(reason)
			continue


		dailytasks = models.WorkItemAssignment(workitem=get_workitem,
									   lead=get_lead,
									)

		try:
			if not dailytasks in rows_updated:
				dailytasks.save()
				rows_updated.append(dailytasks)

			for agent in associates:
				get_agent = get_emp_agents[agent]
				dailytasks.agents.add(get_agent)
			models.QcAttribute.objects.get_or_create(dailytask=dailytasks)
		except IntegrityError as e:
			reason = "Row{} Reason:{}".format(row_number, str(e))
			rows_error.append(reason)

		except KeyError as e:
			reason = "{} not found, please check the {} name in CSV file, ".format(str(e), str(e))
			if not reason in rows_error:
				rows_error.append(reason)
			continue

	if rows_updated:
		if len(rows_updated) == len(dict_data):
			if not rows_error:
				result = True

	return result, rows_error, rows_updated

from django.contrib.auth.models import User

def create_employee(dict_data):

	for record in dict_data: 
		userid = record["employee_id"]
		first_name = record["first_name"]
		last_name = record["last_name"]
		email = record["email"]
		password = record["password"]
		staff_status = record["status"]
		manager = record['manager']
		deparrtment = record['department']
		role = record["role"]
		experience_slab = record["experience_slab"]

		user = User.objects.create_user(username=userid,
								email=email,
								password=password,
								is_active=True,
								is_staff = True,
							)
		user.save()


	if rows_updated:
		if len(rows_updated) == len(dict_data):
			if not rows_error:
				result = True
	return result, rows_error, rows_updated
