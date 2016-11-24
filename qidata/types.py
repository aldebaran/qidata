from enum import Enum


class DataType(Enum):
    """
    Types of data known by qidata
    """
    IMAGE = 0
    AUDIO = 1

    def __str__(self):
        return self.name.capitalize()


class MetadataType(Enum):
    """
    Metadata data object types provided by qidata
    """
    FACE = 0
    Face = 0
    PERSON = 1
    Person = 1
    SPEECH = 2
    Speech = 2
    NOISE = 3
    Noise = 3
    OBJECT = 4
    Object = 4

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
            MetadataType.NOISE
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
