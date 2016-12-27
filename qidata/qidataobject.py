# -*- coding: utf-8 -*-

# qidata
from textualize import textualize_metadata

class QiDataObject(object):
	"""
	Interface class representing a generic "data" element.

	Data can be any piece of raw data (image, audio, text, whatever)
	carrying metadata information.
	"""

	# ──────────
	# Properties

	@property
	def raw_data(self):
		"""
		Object's raw data
		"""
		raise NotImplementedError

	@property
	def metadata(self):
		"""
		Object's metadata list
		"""
		raise NotImplementedError

	@property
	def type(self):
		"""
		Object's data type
		"""
		raise NotImplementedError

	# ──────────────
	# Textualization

	def __str__(self):
		return unicode(self).encode(encoding="utf-8")

	def __unicode__(self):
		res_str = ""
		res_str += "Object type: " + self.type.name + "\n"
		for annotator in self.metadata:
			annotator_str = "Annotator: " + unicode(annotator)
			res_str += annotator_str
			res_str += textualize_metadata(self.metadata[annotator])
		return res_str