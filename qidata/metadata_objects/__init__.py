# -*- coding: utf-8 -*-

"""
This package contains different classes representing metadata.
"""

from person import Person
from face import Face
from object import Object
from speech import Speech
from noise import Noise
from qidata.types import MetadataType


def makeMetadataObject(metadata_object_type, data=None):
    """
    MetadataObjects factory
    This is the prefered way to create MetadataObjects. Objects that
    can be created by this method are the ones in `qidata.types.metadataTypes`

    :param metadata_object_type: requested object to build's name (qidata.types)
    :param data: data to prefill to created object (dict)
    """
    if metadata_object_type == MetadataType.PERSON:
        return Person() if data is None else Person.fromDict(data)
    elif metadata_object_type == MetadataType.FACE:
        return Face() if data is None else Face.fromDict(data)
    elif metadata_object_type == MetadataType.OBJECT:
        return Object() if data is None else Object.fromDict(data)
    elif metadata_object_type == MetadataType.NOISE:
        return Noise() if data is None else Noise.fromDict(data)
    elif metadata_object_type == MetadataType.SPEECH:
        return Speech() if data is None else Speech.fromDict(data)
    else:
        raise TypeError("Required metadata object (%s) does not exist"
                        % metadata_object_type)

#––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––#
