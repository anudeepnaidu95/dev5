# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.utils.encoding import smart_text
from django.conf import settings

try:
	from django.utils.encoding import force_text
except ImportError:
	from django.utils.encoding import force_unicode as force_text



class Widget(object):
	"""
	A Widget takes care of converting between import and export representations.
	This is achieved by the two methods,
	:meth:`~import_export.widgets.Widget.clean` and
	:meth:`~import_export.widgets.Widget.render`.
	"""

	def clean(self, value):

		"""
		Returns an appropriate Python object for an imported value.
		For example, if you import a value from a spreadsheet,
		:meth:`~import_export.widgets.Widget.clean` handles conversion
		of this value into the corresponding Python object.
		Numbers or dates can be *cleaned* to their respective data types and
		don't have to be imported as Strings.
		"""
		return value

	def render(self, value):
		"""
		Returns an export representation of a Python value.
		For example, if you have an object you want to export,
		:meth:`~import_export.widgets.Widget.render` takes care of converting
		the object's field to a value that can be written to a spreadsheet.
		"""
		return force_text(value)


class ForeignKeyWidget(Widget):
	"""
	Widget for a ``ForeignKey`` field which looks up a related model using
	"natural keys" in both export an import.
	The lookup field defaults to using the primary key (``pk``) as lookup
	criterion but can be customised to use any field on the related model.
	Unlike specifying a related field in your resource like so…
	::
		class Meta:
			fields = ('author__name',)
	…using a :class:`~import_export.widgets.ForeignKeyWidget` has the
	advantage that it can not only be used for exporting, but also importing
	data with foreign key relationships.
	Here's an example on how to use
	:class:`~import_export.widgets.ForeignKeyWidget` to lookup related objects
	using ``Author.name`` instead of ``Author.pk``::
		class BookResource(resources.ModelResource):
			author = fields.Field(
				column_name='author',
				attribute='author',
				widget=ForeignKeyWidget(Author, 'name'))
			class Meta:
				fields = ('author',)
	:param model: The Model the ForeignKey refers to (required).
	:param field: A field on the related model used for looking up a particular object.
	"""
	def __init__(self, model, field='pk', *args, **kwargs):
		self.model = model
		self.field = field
		super(ForeignKeyWidget, self).__init__(*args, **kwargs)

	def clean(self, value):
		val = super(ForeignKeyWidget, self).clean(value)
		return self.model.objects.get(**{self.field: val}) if val else None

	def render(self, value):
		if value is None:
			return ""
		return getattr(value, self.field)



class ManyToManyWidget(Widget):
	"""
	Widget that converts between representations of a ManyToMany relationships
	as a list and an actual ManyToMany field.
	:param model: The model the ManyToMany field refers to (required).
	:param separator: Defaults to ``','``.
	:param field: A field on the related model. Default is ``pk``.
	"""

	def __init__(self, model, separator=None, field=None, *args, **kwargs):
		if separator is None:
			separator = ','
		if field is None:
			field = 'pk'
		self.model = model
		self.separator = separator
		self.field = field
		super(ManyToManyWidget, self).__init__(*args, **kwargs)

	def clean(self, value):
		if not value:
			return self.model.objects.none()
		if isinstance(value, float):
			ids = [int(value)]
		else:
			ids = value.split(self.separator)
		ids = filter(None, value.split(self.separator))
		return self.model.objects.filter(**{
			'%s__in' % self.field: ids
		})

	def render(self, value):
		ids = [smart_text(getattr(obj, self.field)) for obj in value.all()]
		print "my agents id are", ids
		return self.separator.join(ids)