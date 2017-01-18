from enum import EnumMeta, Enum

class CapEnum(EnumMeta):
    def __getitem__(cls, name):
        if isinstance(name, str):
            return EnumMeta.__getitem__(cls, name.upper())
        else:
            return EnumMeta.__getitem__(cls, name)


class DataType(Enum):
    """
    Types of data known by qidata
    """
    __metaclass__ = CapEnum
    AUDIO   = 0
    DATASET = 1
    IMAGE   = 2

    def __str__(self):
        return self.name.capitalize()


class MetadataType(Enum):
    """
    Metadata data object types provided by qidata
    """
    __metaclass__ = CapEnum
    FACE = 0
    PERSON = 1
    SPEECH = 2
    OBJECT = 4

    def __str__(self):
        return self.name.capitalize()


class CheckCompatibility:

    _compatibility_map = dict()
    _compatibility_map[DataType.IMAGE] = [
            MetadataType.FACE,
            MetadataType.PERSON,
            MetadataType.OBJECT
        ]
    _compatibility_map[DataType.AUDIO] = [
            MetadataType.SPEECH,
        ]

    @classmethod
    def getCompatibleMetadataTypes(cls, data_type):
        """
        Return a list of metadata types which are compatible
        with the given data type.

        :param data_type: Data on which applicable metadata types
        are requested.
        """
        return cls._compatibility_map[data_type]
