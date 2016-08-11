from enum import Enum

class DataType(Enum):
    """
    Types of data known by qidata
    """
    IMAGE = 0

    def __str__(self):
        return self.name.capitalize()


class MetadataType(Enum):
    """
    Metadata data object types provided by qidata
    """
    FACE = 0
    PERSON = 1

    def __str__(self):
        return self.name.capitalize()


class CheckCompatibility:

    _compatibility_map = dict()
    _compatibility_map[DataType.IMAGE]=[
            MetadataType.FACE,
            MetadataType.PERSON
        ]

    @classmethod
    def getCompatibleMetadataTypes(self, data_type):
        """
        Return a list of metadata types which are compatible
        with the given data type.

        :param data_type: Data on which applicable metadata types
        are requested.
        """
        return self._compatibility_map[data_type]