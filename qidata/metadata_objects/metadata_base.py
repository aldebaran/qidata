# -*- coding: utf-8 -*-

# qidata
from qidata.textualize import textualize_dict

class MetadataObjectBase(object):
	"""
	Base class for all metadata objects.

	This class needs to be extended in order to create
	new metadata objects classes.
	"""
	__slots__ = []

	def __init__(self):
		pass

	def toDict(self):
		raise NotImplementedError

	@staticmethod
	def fromDict(data=dict()):
		raise NotImplementedError

	# ─────────
	# Operators

	def __eq__(self, other):
		for attribute_name in self.__slots__:
			if getattr(self, attribute_name) != getattr(other, attribute_name):
				return False

		return True

	# ──────────────
	# Textualization

	def __str__(self):
		return str(self.toDict())

	def __unicode__(self):
		return textualize_dict(self.toDict())