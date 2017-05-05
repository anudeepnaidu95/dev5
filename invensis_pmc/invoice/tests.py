from django.test import TestCase

# Create your tests here.

import os
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import doctemplate, Paragraph, LongTable, Spacer, Image, PageBreak
from reportlab.platypus.tables import GRID_STYLE, BOX_STYLE
from reportlab.platypus import Frame
from reportlab.pdfbase import pdfmetrics
#from reportlab.pdfbase.ttfonts import TTFon

def invoice_generator(request,invoice_id):
	"""
	Prints a list of sponsors and children
	"""
	out_file_path = "somefilename.pdf"
	invoices = models.Invoice.objects.all()
	doct = SimpleDocTemplate(out_file_path)
	style_sheet = getSampleStyleSheet()
	normal_para = lambda x: Paragraph(unicode(x), style=style_sheet["Normal"])
	data = [map(normal_para, [_("Invoice Number"), _("Date"),
							  _("Total Amount"), _("Customer")])]

	for invoice in invoices:
		row = map(normal_para, (invoice.invoice_no,
								u"%s %s" % (invoice.date,
											invoice.customer),
								invoice.total_amount,
								invoice.management_employee))
		data.append(row)
	table = LongTable(data, style=GRID_STYLE)
	page_flowables = [table]
	doct._doSave = 0
	doct.build(page_flowables)

	canvas = doct.canv
	canvas.setTitle(unicode(_("Invoices")))
	print canvas.getpdfdata()
	output_file = out_file_path.split('/')[-1]
 	print "output_file", output_file
	#fs = FileSystemStorage(out_file_path)
  	with open(out_file_path) as pdf:
		response = HttpResponse(content_type='application/pdf')
		response['Content-Disposition'] = 'attachment; filename=%s'% smart_str(output_file	) 
	 	return response

	return response
