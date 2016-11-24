# -*- coding: utf-8 -*-

"""
This package contains different classes representing metadata.
"""

from metadata_base import MetadataObjectBase
from person import Person
from face import Face
from object import Object
from speech import Speech
from noise import Noise
from object import Object
from typedlist import TypedList, FacialPartsList
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
    elif metadata_object_type == MetadataType.OBJECT:
        return Object() if data is None else Object.fromDict(data)
    else:
        raise TypeError("Required metadata object (%s) does not exist"
                        % metadata_object_type)


def printHelp(metadata_object_type):
    """
    Print some help on the requested QiDataObject

    :param metadata_object_type: object name on which help is requested
    """
    if metadata_object_type == MetadataType.PERSON:
        help(Person)
    elif metadata_object_type == MetadataType.FACE:
        help(Face)
    elif metadata_object_type == MetadataType.OBJECT:
        help(Object)
    elif metadata_object_type == MetadataType.NOISE:
        help(Noise)
    elif metadata_object_type == MetadataType.SPEECH:
        help(Speech)
    elif metadata_object_type == MetadataType.OBJECT:
        help(Object)
    else:
        raise TypeError("Required metadata object (%s) does not exist"
                        % metadata_object_type)

#––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––#
