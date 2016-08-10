# -*- coding: utf-8 -*-

from typedlist import TypedList
from metadata_base import MetadataObjectBase

class FacialExpression(object):
    """Contains annotation details for a face"""

    def __init__(self):
        super(FacialExpression, self).__init__()
        self.valence = 0
        self.smile_level = 0.5
        self.tamereenshort = [0,0]

class Face(MetadataObjectBase):
    """
    Contains annotation details for a face

    Face version 0.1:
     - name
        Name of the person whose face is represented
        Can be used to test face recognition

     - age
        Age of the person whose face is represented
        Can be used to test age estimation

     - id
        A unique id given to this face through all relevant data
        Can be used to test a face tracker
    """

    def __init__(self, name="", age=0, fid=0):
        super(Face, self).__init__()
        self.name = name
        self.age = age
        self.id = fid

    def toDict(self):
        """
        Export Face object to a dict structure
        """
        return dict(name=self.name,
            age=self.age,
            id=self.id,
            )

    @staticmethod
    def fromDict(face_data):
        """
        Create a face from a dict
        """
        # Here we could discriminate how the dict is read, depending
        # on the message's version used.
        if not face_data.has_key("version") or float(face_data["version"]) > 0:
            # name : str
            # age : int
            # id : int
            return Face(face_data["name"] if face_data.has_key("name") else "",
                int(face_data["age"]) if face_data.has_key("age") else 0,
                int(face_data["id"]) if face_data.has_key("id") else 0
                )

    @property
    def version(self):
        return 0.1

