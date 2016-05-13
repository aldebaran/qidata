# -*- coding: utf-8 -*-

"""
This package contains different classes representing structured dataTypes for annotated datasets.
"""

from person import Person
from face import Face
from typedlist import TypedList

def makeDataObject(dataObjectName, data = None):
    if dataObjectName == "Person":
        return Person() if data is None else Person.fromDict(data)
    elif dataObjectName == "Face":
        return Face() if data is None else Face.fromDict(data)
    else:
        raise TypeError("Required annotation item (%s) does not exist"%dataObjectName)

def printHelp(dataObjectName):
    if dataObjectName == "Person":
        help(Person)
    elif dataObjectName == "Face":
        help(Face)
    else:
        raise TypeError("Required annotation item (%s) does not exist"%dataObjectName)

# ––––––––––––––––––––––––––––
# List of available data types

DataObjectTypes = ["Face", "Person"]

# ––––––––––––––––––––––––––––
# Convenience version variable

import os
VERSION = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), "VERSION")).read().split()[0]

#––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––#