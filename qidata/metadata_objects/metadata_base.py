

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

	def __eq__(self, other):
		for attribute_name in self.__slots__:
			if getattr(self, attribute_name) != getattr(other, attribute_name):
				return False

		return True