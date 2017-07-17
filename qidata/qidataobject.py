# -*- coding: utf-8 -*-

from collections import OrderedDict
import copy

# qidata
from textualize import textualize_metadata
from qidata import MetadataType

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
		Return metadata content in the form of a ``collections.OrderedDict`` containing
		metadata object instances or built-in types.
		The returned object is a copy of the real metadata, therefore modifying it has no
		impact on the underlying object.
		"""
		if not hasattr(self, "_annotations"):
			self._annotations = dict()
		return copy.deepcopy(self._annotations)

	@metadata.setter
	def metadata(self, new_metadata):
		## Check new_metadata has the correct shape
		if not isinstance(new_metadata, dict):
			raise AttributeError("Metadata must be a mapping")
		for annotator in new_metadata:
			if not isinstance(new_metadata[annotator], dict):
				msg = "Metadata from annotator {} must be a dict, not {}"
				raise AttributeError(msg.format(annotator, type(new_metadata[annotator]).__name__))
			for type_name in new_metadata[annotator]:
				try:
					obj_type = MetadataType[type_name]
				except KeyError:
					msg = "Type {} in {}'s metadata does not exist"
					raise AttributeError(msg.format(type_name, annotator))

				if not isinstance(new_metadata[annotator][type_name], list):
					msg = "List of {} metadata from annotator {} must be a list"
					raise AttributeError(msg.format(type_name, annotator))

				for annotation in new_metadata[annotator][type_name]:
					if not isinstance(annotation, (tuple, list)):
						msg = "Metadata stored in {}'s metadata list must be a list or tuple, not {}"
						raise AttributeError(msg.format(type_name, type(annotation).__name__))
					if len(annotation) != 2:
						msg = "Metadata of type {0} in {0}'s metadata from {1} must be of size 2"
						raise AttributeError(msg.format(type_name, annotator))
					if type(annotation[0]).__name__ != type_name:
						msg = "{} metadata received instead of {} in {}'s metadata"
						raise AttributeError(msg.format(type(annotation[0]).__name__, type_name, annotator))
					if (annotation[1] is not None) and (not isinstance(annotation[1], list)):
						msg = "Location of metadata of type {0} in {0}'s metadata from {1} is incorrect. "
						msg += "Must be list or None"
						raise AttributeError(msg.format(type_name, annotator))

		## Make a copy of it
		tmp = copy.deepcopy(new_metadata)
		self._annotations = OrderedDict(tmp)

	@property
	def type(self):
		"""
		Object's data type
		"""
		raise NotImplementedError

	@property
	def annotators(self):
		"""
		Return the list of annotators for this file
		"""
		return self.metadata.keys()

	@property
	def read_only(self):
		"""
		States if the object is protected against modification
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
			res_str += "\n"
		return res_str