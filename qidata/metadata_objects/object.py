# -*- coding: utf-8 -*-

"""
This package contains different classes representing structured dataTypes.
"""

from typedlist import TypedList
from metadata_base import MetadataObjectBase


class Object(MetadataObjectBase):
    """
    Contains annotation details for an object.
    It can be a random object or a visual tag
    """
    def __init__(self, type="", value="", id=0):
        """
        Object attributes:
        :param type: redball, qrcode, landmark, ...
        :param value: object description or decyphered value
        :param id: ID of the object
        """
        super(Object, self).__init__()
        self.type = type
        self.value = value
        self.id = id

    def toDict(self):
        """
        Export Object object to a dict structure
        """
        return dict(type=self.type,
                    value=self.value,
                    id=self.id)

    @staticmethod
    def fromDict(tag_data):
        """
        Create an Object from a dict
        """
        # Here we could discriminate how the dict is read, depending
        # on the message's version used.
        if "version" not in tag_data.keys() or float(tag_data["version"]) > 0:
            # type : str
            # value : str
            # position : list
            return Object(tag_data["type"] if "type" in tag_data.keys() else "",
                          tag_data["value"] if "value" in tag_data.keys()
                          else "",
                          tag_data["id"] if "id" in tag_data.keys() else 0)

    @property
    def version(self):
        return 0.1
