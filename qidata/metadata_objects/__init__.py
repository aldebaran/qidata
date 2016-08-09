# -*- coding: utf-8 -*-

"""
This package contains different classes representing metadata.
"""

from person import Person
from face import Face
from typedlist import TypedList

def makeMetadataObject(metadata_object_name, data = None):
    """
    MetadataObjects factory
    This is the prefered way to create MetadataObjects. Objects that
    can be created by this method are the ones in `qidata.types.metadataTypes`

    :param metadata_object_name: requested object to build's name (str)
    :param data: data to prefill to created object (dict)
    """
    if metadata_object_name == "Person":
        return Person() if data is None else Person.fromDict(data)
    elif metadata_object_name == "Face":
        return Face() if data is None else Face.fromDict(data)
    else:
        raise TypeError("Required annotation item (%s) does not exist"%metadata_object_name)

def printHelp(metadata_object_name):
    """
    Print some help on the requested QiDataObject

    :param metadata_object_name: object name on which help is requested
    """
    if metadata_object_name == "Person":
        help(Person)
    elif metadata_object_name == "Face":
        help(Face)
    else:
        raise TypeError("Required annotation item (%s) does not exist"%metadata_object_name)

# ––––––––––––––––––––––––––––
# List of available data types

DataObjectTypes = ["Face", "Person"]


#––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––#