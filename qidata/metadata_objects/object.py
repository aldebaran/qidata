# -*- coding: utf-8 -*-

"""
This package contains different classes representing structured dataTypes.
"""

from metadata_base import MetadataObjectBase


class Object(MetadataObjectBase):
    """
    Contains annotation details for an object.
    It can be a random object or a visual tag.
    """

    __slots__ = ["type", "value", "id"]

    def __init__(self, obj_type=None, value=None, obj_id=0):
        """
        Object attributes:

        Args:
            obj_type (str): redball, qrcode, landmark, ...
            value (str): object description or decyphered value
            obj_id (int): ID of the object
        """
        super(MetadataObjectBase, self).__init__()
        self.type = obj_type if obj_type is not None else ""
        self.value = value if value is not None else ""
        self.id = obj_id

    @staticmethod
    def fromDict(tag_data):
        """
        Create an Object object from a dict.

        Args:
            tag_data (dict): source data dictionary

        Returns:
            :obj:`Object`: <Object> object created from the given dictionary
        """
        # Here we could discriminate how the dict is read, depending
        # on the message's version used.
        if "version" not in tag_data.keys() or float(tag_data["version"]) > 0:
            return Object(tag_data["type"] if "type" in tag_data.keys() else "",
                          tag_data["value"] if "value" in tag_data.keys()
                          else "",
                          tag_data["id"] if "id" in tag_data.keys() else 0)

    @property
    def version(self):
        return 0.1
