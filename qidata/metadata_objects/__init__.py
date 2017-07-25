# Third-party libraries
from strong_typing import VersionedStruct as _VS
import enum as _enum

class _QidataEnumMixin(_enum.Enum):
	def __str__(self):
		return self.name

class MetadataObject(_VS):pass

# Import all defined metadata objects
from property import Property
from timestamp import TimeStamp
from transform import Transform

__all__=[
  "Property",
]