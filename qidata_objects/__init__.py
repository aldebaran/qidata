# -*- coding: utf-8 -*-

"""
This package contains different classes representing structured dataTypes.
"""

from person import Person
from face import Face
from typedlist import TypedList

def makeDataObject(qiDataObjectName, data = None):
    """
    QiDataObjects factory
    This is the prefered way to create QiDataObjects. Objects that
    can be created by this method are the ones in `DataObjectTypes`

    @qiDataObjectName : requested object to build's name (str)
    @data           : data to prefill to created object (dict)
    """
    if qiDataObjectName == "Person":
        return Person() if data is None else Person.fromDict(data)
    elif qiDataObjectName == "Face":
        return Face() if data is None else Face.fromDict(data)
    else:
        raise TypeError("Required annotation item (%s) does not exist"%qiDataObjectName)

def printHelp(qiqiDataObjectName):
    """
    Print some help on the requested QiDataObject

    @qiqiDataObjectName : object name on which help is requested
    """
    if qiqiDataObjectName == "Person":
        help(Person)
    elif qiqiDataObjectName == "Face":
        help(Face)
    else:
        raise TypeError("Required annotation item (%s) does not exist"%qiDataObjectName)

# ––––––––––––––––––––––––––––
# List of available data types

DataObjectTypes = ["Face", "Person"]

# ––––––––––––––––––––––––––––
# Convenience version variable

import os
VERSION = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), "VERSION")).read().split()[0]

#––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––#