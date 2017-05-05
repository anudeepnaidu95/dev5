# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django_extensions.db.models import TitleDescriptionModel, TitleSlugDescriptionModel, TimeStampedModel
from employee.models import Employee
from django.contrib.auth.models import User


LEAD_SOURCES = (

	('web','Web'),
	('sales-team','Sales Team'),
	('reference','Reference'),
	('other','Other'),
	# ('',''),
	# ('',''),
	# ('',''),

	)

CURRENCY_TYPES = (
		('AED',	'United Arab Emirates Dirham',),
		('AFN',	'Afghanistan Afghani',),
		('ALL',	'Albania Lek',),
		('AMD',	'Armenia Dram',),
		('ANG',	'Netherlands Antilles Guilder',),
		('AOA',	'Angola Kwanza',),
		('ARS',	'Argentina Peso',),
		('AUD',	'Australia Dollar',),
		('AWG',	'Aruba Guilder',),
		('AZN',	'Azerbaijan New Manat',),
		('BAM',	'Bosnia and Herzegovina Convertible Marka',),
		('BBD',	'Barbados Dollar',),
		('BDT',	'Bangladesh Taka',),
		('BGN',	'Bulgaria Lev',),
		('BHD',	'Bahrain Dinar',),
		('BIF',	'Burundi Franc',),
		('BMD',	'Bermuda Dollar',),
		('BND',	'Brunei Darussalam Dollar',),
		('BOB',	'Bolivia Bolíviano',),
		('BRL',	'Brazil Real',),
		('BSD',	'Bahamas Dollar',),
		('BTN',	'Bhutan Ngultrum',),
		('BWP',	'Botswana Pula',),
		('BYN',	'Belarus Ruble',),
		('BZD',	'Belize Dollar',),
		('CAD',	'Canada Dollar',),
		('CDF',	'Congo/Kinshasa Franc',),
		('CHF',	'Switzerland Franc',),
		('CLP',	'Chile Peso',),
		('CNY',	'China Yuan Renminbi',),
		('COP',	'Colombia Peso',),
		('CRC',	'Costa Rica Colon',),
		('CUC',	'Cuba Convertible Peso',),
		('CUP',	'Cuba Peso',),
		('CVE',	'Cape Verde Escudo',),
		('CZK',	'Czech Republic Koruna',),
		('DJF',	'Djibouti Franc',),
		('DKK',	'Denmark Krone',),
		('DOP',	'Dominican Republic Peso',),
		('DZD',	'Algeria Dinar',),
		('EGP',	'Egypt Pound',),
		('ERN',	'Eritrea Nakfa',),
		('ETB',	'Ethiopia Birr',),
		('EUR',	'Euro Member Countries',),
		('FJD',	'Fiji Dollar',),
		('FKP',	'Falkland Islands (Malvinas) Pound',),
		('GBP',	'United Kingdom Pound',),
		('GEL',	'Georgia Lari',),
		('GGP',	'Guernsey Pound',),
		('GHS',	'Ghana Cedi',),
		('GIP',	'Gibraltar Pound',),
		('GMD',	'Gambia Dalasi',),
		('GNF',	'Guinea Franc',),
		('GTQ',	'Guatemala Quetzal',),
		('GYD',	'Guyana Dollar',),
		('HKD',	'Hong Kong Dollar',),
		('HNL',	'Honduras Lempira',),
		('HRK',	'Croatia Kuna',),
		('HTG',	'Haiti Gourde',),
		('HUF',	'Hungary Forint',),
		('IDR',	'Indonesia Rupiah',),
		('ILS',	'Israel Shekel',),
		('IMP',	'Isle of Man Pound',),
		('INR',	'India Rupee',),
		('IQD',	'Iraq Dinar',),
		('IRR',	'Iran Rial',),
		('ISK',	'Iceland Krona',),
		('JEP',	'Jersey Pound',),
		('JMD',	'Jamaica Dollar',),
		('JOD',	'Jordan Dinar',),
		('JPY',	'Japan Yen',),
		('KES',	'Kenya Shilling',),
		('KGS',	'Kyrgyzstan Som',),
		('KHR',	'Cambodia Riel',),
		('KMF',	'Comoros Franc',),
		('KPW',	'Korea (North) Won',),
		('KRW',	'Korea (South) Won',),
		('KWD',	'Kuwait Dinar',),
		('KYD',	'Cayman Islands Dollar',),
		('KZT',	'Kazakhstan Tenge',),
		('LAK',	'Laos Kip',),
		('LBP',	'Lebanon Pound',),
		('LKR',	'Sri Lanka Rupee',),
		('LRD',	'Liberia Dollar',),
		('LSL',	'Lesotho Loti',),
		('LYD',	'Libya Dinar',),
		('MAD',	'Morocco Dirham',),
		('MDL',	'Moldova Leu',),
		('MGA',	'Madagascar Ariary',),
		('MKD',	'Macedonia Denar',),
		('MMK',	'Myanmar (Burma) Kyat',),
		('MNT',	'Mongolia Tughrik',),
		('MOP',	'Macau Pataca',),
		('MRO',	'Mauritania Ouguiya',),
		('MUR',	'Mauritius Rupee',),
		('MVR',	'Maldives (Maldive Islands) Rufiyaa',),
		('MWK',	'Malawi Kwacha',),
		('MXN',	'Mexico Peso',),
		('MYR',	'Malaysia Ringgit',),
		('MZN',	'Mozambique Metical',),
		('NAD',	'Namibia Dollar',),
		('NGN',	'Nigeria Naira',),
		('NIO',	'Nicaragua Cordoba',),
		('NOK',	'Norway Krone',),
		('NPR',	'Nepal Rupee',),
		('NZD',	'New Zealand Dollar',),
		('OMR',	'Oman Rial',),
		('PAB',	'Panama Balboa',),
		('PEN',	'Peru Sol',),
		('PGK',	'Papua New Guinea Kina',),
		('PHP',	'Philippines Peso',),
		('PKR',	'Pakistan Rupee',),
		('PLN',	'Poland Zloty',),
		('PYG',	'Paraguay Guarani',),
		('QAR',	'Qatar Riyal',),
		('RON',	'Romania New Leu',),
		('RSD',	'Serbia Dinar',),
		('RUB',	'Russia Ruble',),
		('RWF',	'Rwanda Franc',),
		('SAR',	'Saudi Arabia Riyal',),
		('SBD',	'Solomon Islands Dollar',),
		('SCR',	'Seychelles Rupee',),
		('SDG',	'Sudan Pound',),
		('SEK',	'Sweden Krona',),
		('SGD',	'Singapore Dollar',),
		('SHP',	'Saint Helena Pound',),
		('SLL',	'Sierra Leone Leone',),
		('SOS',	'Somalia Shilling',),
		('SPL', 'Seborga Luigino',),
		('SRD',	'Suriname Dollar',),
		('STD',	'São Tomé and Príncipe Dobra',),
		('SVC',	'El Salvador Colon',),
		('SYP',	'Syria Pound',),
		('SZL',	'Swaziland Lilangeni',),
		('THB',	'Thailand Baht',),
		('TJS',	'Tajikistan Somoni',),
		('TMT',	'Turkmenistan Manat',),
		('TND',	'Tunisia Dinar',),
		('TOP',	'Tonga Pa''anga',),
		('TRY',	'Turkey Lira',),
		('TTD',	'Trinidad and Tobago Dollar',),
		('TVD',	'Tuvalu Dollar',),
		('TWD',	'Taiwan New Dollar',),
		('TZS',	'Tanzania Shilling',),
		('UAH',	'Ukraine Hryvnia',),
		('UGX',	'Uganda Shilling',),
		('USD',	'United States Dollar',),
		('UYU',	'Uruguay Peso',),
		('UZS',	'Uzbekistan Som',),
		('VEF',	'Venezuela Bolivar',),
		('VND',	'Viet Nam Dong',),
		('VUV',	'Vanuatu Vatu',),
		('WST',	'Samoa Tala',),
		('XAF',	'Communauté Financière Africaine (BEAC) CFA Franc BEAC',),
		('XCD',	'East Caribbean Dollar',),
		('XDR',	'International Monetary Fund (IMF) Special Drawing Rights',),
		('XOF',	'Communauté Financière Africaine (BCEAO) Franc',),
		('XPF',	'Comptoirs Français du Pacifique (CFP) Franc',),
		('YER',	'Yemen Rial',),
		('ZAR',	'South Africa Rand',),
		('ZMW',	'Zambia Kwacha',),
		('ZWD',	'Zimbabwe Dollar',),	

	)


class Country(models.Model):
	name = models.CharField( max_length=255)
	code =  models.CharField( max_length=3)
	class Meta:
		unique_together = ("name",)
		verbose_name = "Country"
		verbose_name_plural = "Countrys"

	def __str__(self):
		return self.name
	


class CurrencyType(TitleSlugDescriptionModel):

	class Meta:
		unique_together = ("title",)
		verbose_name = "CurrencyType"
		verbose_name_plural = "CurrencyTypes"

	def __str__(self):
		return self.title
	

class Customer( TimeStampedModel):

	title = models.CharField(verbose_name='Company Name', max_length=255)
	description = models.CharField( max_length=255, blank=True, null=True)

	# user =  models.ForeignKey(User, blank=True, null=True)
	# organization =  models.ForeignKey(Organization)

	contact_name = models.CharField(max_length=100, blank=True, null=True)
	designation = models.CharField(max_length=100, blank=True, null=True)
	email = models.EmailField(blank=True,null=True)
	phone = models.CharField(max_length=50, blank=True, null=True)

	# address fields***********
	addressline1 = models.CharField( max_length=255, blank=True, null=True)
	addressline2 = models.CharField( max_length=255, blank=True, null=True)
	city = models.CharField( max_length=255, blank=True, null=True)
	zip_code = models.CharField( max_length=20, blank=True, null=True)
	state = models.CharField( max_length=255, blank=True, null=True)
	country =  models.ForeignKey(Country, blank=True,null=True)

	requirement =models.TextField(blank=True, null=True)

	industry =models.ForeignKey('project.Industry', blank=True, null=True, related_name='+')    
	# services_required = models.ManyToManyField('project.Service')

	services = models.ManyToManyField('project.ServiceType', related_name='+', verbose_name='Services Required')
	# only sales_managers role
	owner = models.ForeignKey(Employee, blank=True, null=True)

	lead_source =models.CharField(choices=LEAD_SOURCES, blank=True, null=True, max_length=20)
	# field to hold sales rep if lead soure is from sales team*****
	sales_rep = models.ForeignKey(Employee, blank=True, null=True, related_name='+')
	
	other_lead_source =models.CharField( blank=True, null=True, max_length=100)

	created_by = models.ForeignKey(User, blank=True,null=True)
	# is_converted_to_customer = models.BooleanField(default=False)

	# currency = models.ForeignKey(CurrencyType, blank=True, null=True)

	# base currency is always - USD
	# mandatory field
	currency = models.CharField(choices=CURRENCY_TYPES, max_length=10, blank=True, null=True,default='USD')

	conversion_rate = models.DecimalField(default=0, max_digits=5, decimal_places=2)
	
	# invoice related info***

	last_invoice_no = models.IntegerField(default=0)
	# {company_name_invoice}-inv-{currentyear}-{nextyear}-{invno}
	invoice_format = models.CharField( max_length=255, blank=True,null=True)
	company_name_invoice = models.CharField( max_length=50, blank=True,null=True)

	class Meta:
		unique_together = ("title",)
		verbose_name = "Customer"
		verbose_name_plural = "Customers"

	def __str__(self):
		return self.title

	# def service(self):
	# 	return " / ".join([a.title for a in self.services_required.all()])

	# def Company(self):
	# 	return self.title
LEAD_STATUSES = (
	# ("COLD", "Cold"),
	# ("WARM", "Warm"),
	# ("HOT", "Hot"),
	# ("WON", "Won"),
	# ("LOST", "Lost")

	("PROSPECTING", "Prospecting"), #BLUE
	("TRIAL", "Trial"), #GREEN
	("NEGOTIATING", "Negotiating"), #ORANGE
	("WON", "Won"),  #??
	("LOST", "Lost")  , #RED

)

class Lead(TimeStampedModel):

	# user =  models.ForeignKey(User, blank=True, null=True)
	# organization =  models.ForeignKey(Organization)
	title = models.CharField(verbose_name='Company Name' , max_length=255)
	description = models.CharField( max_length=255, blank=True, null=True)

	contact_name = models.CharField(max_length=100, blank=True, null=True)
	designation = models.CharField(max_length=100, blank=True, null=True)
	email = models.EmailField(blank=True,null=True)
	phone = models.CharField(max_length=50, blank=True, null=True)

	# address fields***********
	addressline1 = models.CharField( max_length=255, blank=True, null=True)
	addressline2 = models.CharField( max_length=255, blank=True, null=True)
	city = models.CharField( max_length=255, blank=True, null=True)
	zip_code = models.CharField( max_length=20, blank=True, null=True)
	state = models.CharField( max_length=255, blank=True, null=True)
	country =  models.ForeignKey(Country, blank=True,null=True)

	requirement =models.TextField(blank=True, null=True)

	industry =models.ForeignKey('project.Industry', blank=True, null=True, related_name='+')    

	# services_required = models.ManyToManyField('project.Service')
	services = models.ManyToManyField('project.ServiceType', related_name='+', verbose_name='Services Required')

	# only sales_managers role
	owner = models.ForeignKey(Employee, blank=True, null=True)

	lead_source =models.CharField(choices=LEAD_SOURCES, blank=True, null=True, max_length=20)
	# field to hold sales rep if lead soure is from sales team*****
	lead_date = models.DateField(blank=True, null=True)
	
	sales_rep = models.ForeignKey(Employee, blank=True, null=True, related_name='+')
	other_lead_source =models.CharField( blank=True, null=True, max_length=100)

	is_converted_to_customer = models.BooleanField(default=False)

	created_by = models.ForeignKey(User, blank=True,null=True)

	currency = models.ForeignKey(CurrencyType, blank=True, null=True)

	latest_followup_date = models.DateField(blank=True, null=True)

	latest_lead_status = models.CharField(max_length=20, blank=True, null=True, choices=LEAD_STATUSES)

	class Meta:
		unique_together = ("title",)
		verbose_name = "Enquiry"
		verbose_name_plural = "Enquiries"

	def __str__(self):
		return self.title

	# def service(self):
	# 	return " / ".join([a.title for a in self.services_required.all()])

	# def Company(self):
	# 	return self.title
	

# CONVERSION_STATUSES = (
#     ("WON", "Won"),
#     ("LOST", "Lost"),
# )

PERCENT_STATUSES = (
	("10", "10"),
	("20", "20"),
	("30", "30"),
	("40", "40"),
	("50", "50"),
	("60", "60"),
	("70", "70"),
	("80", "80"),
	("90", "90"),
	("100", "100"),
)

class Followup(TimeStampedModel):
	# customer = models.ForeignKey(Customer)
	lead = models.ForeignKey(Lead, blank=True, null=True)

	next_followup = models.DateField(blank=True, null=True)

	lead_status = models.CharField(max_length=20, blank=True,choices=LEAD_STATUSES)

	is_converted_to_customer = models.BooleanField(default=False, verbose_name='Converted')
	# status = models.CharField(max_length=20, blank=True,choices=CONVERSION_STATUSES)

	# validation - 0 to 100
	percentage=models.CharField(max_length=10, blank=True, choices=PERCENT_STATUSES)

	remarks = models.TextField(blank=True, null=True, verbose_name='Notes')


	def __str__(self):
		return str(self.id)




 




