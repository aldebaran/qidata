# -*- coding: utf-8 -*-

from typedlist import TypedList
from typedlist import FacialPartsList
from metadata_base import MetadataObjectBase


class FaceCharacteristics(MetadataObjectBase):
    """
    Contains annotation details for a face characteristics.

    FaceCharacteristics:
        - Expression
        - FacialParts
        - Gender
        - Smile
    """
    def __init__(self, expression=None, facial_parts=None, gender=None,
                 smile=None):
        """
        FaceCharacteristics attributes.

        Args:
            expression (str): associated face expressions
            facial_parts (str): associated facial parts data
            gender (str): associated gender (male, female)
            smile (str): associated smile data
        """
        super(FaceCharacteristics, self).__init__()
        self.expression = expression if expression is not None else ""
        self.facial_parts = facial_parts if facial_parts is not None else ""
        self.gender = gender if gender is not None else ""
        self.smile = smile if smile is not None else ""

    def toDict(self):
        """
        Export Object object to a dict structure.
        """
        return dict(expression=self.expression,
                    facial_parts=self.facial_parts,
                    gender=self.gender,
                    smile=self.smile)

    @staticmethod
    def fromDict(facechar_data):
        """
        Create a FaceCharacteristics object from a dict.

        Args:
            facechar_data (dict): source data dictionary

        Returns:
            :obj:`FaceCharacteristics`: <FaceCharacteristics> object created
                from the given dictionary
        """
        # Here we could discriminate how the dict is read, depending
        # on the message's version used.
        if "version" not in facechar_data.keys() or \
                float(facechar_data["version"]) > 0:
            return FaceCharacteristics(
                facechar_data["expression"] if "expression" in
                                               facechar_data.keys() else "",
                facechar_data["facial_parts"] if "facial_parts" in
                                                 facechar_data.keys() else "",
                facechar_data["gender"] if "gender" in
                                           facechar_data.keys() else "",
                facechar_data["smile"] if "smile" in
                                          facechar_data.keys() else "")

    @property
    def version(self):
        return 0.1


class Face(MetadataObjectBase):
    """
    Contains annotation details for a face.

    Face version 0.2 (Additional attributes):
        - Expression
            Given by FaceCharacteristics: facial expression values.

        - FacialParts
            Given by FaceCharacteristics: positions of different facial parts.

        - Gender
            Gender of the target

        - Smile
            Given by FaceCharacteristics: smile values of the associated face.

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

    def __init__(self,
                 name=None,
                 age=0,
                 gender=None,
                 facial_parts=None,
                 expression=None,
                 smile=None,
                 fid=0):
        super(Face, self).__init__()
        self.name = name if name is not None else ""
        self.age = age
        self.gender = gender if gender is not None else ""
        self.facial_parts = facial_parts if facial_parts is not None \
            else FacialPartsList()
        self.expression = expression if expression is not None \
            else TypedList(float)
        self.smile = smile if smile is not None else TypedList(float)
        self.id = fid

    def toDict(self):
        """
        Export Face object to a dict structure
        """
        return dict(name=self.name,
                    age=self.age,
                    gender=self.gender,
                    facial_parts=self.facial_parts,
                    expression=self.expression,
                    smile=self.smile,
                    id=self.id,
                    )

    @staticmethod
    def fromDict(face_data):
        """
        Create a face from a dict
        """
        # Here we could discriminate how the dict is read, depending
        # on the message's version used.
        if "version" not in face_data.keys() or float(face_data["version"]) > 0:
            # name : str
            # age : int
            # facial parts: FacialPartsList
            # expression: TypedList
            # smile: TypedList
            # id : int
            return Face(face_data["name"] if "name" in face_data.keys() else "",
                        int(face_data["age"]) if "age" in face_data.keys()
                        else 0,
                        face_data["gender"] if "gender" in face_data.keys()
                        else "",
                        face_data["facial_parts"] if "facial_parts" in
                                                     face_data.keys()
                        else FacialPartsList(),
                        face_data["expression"] if "expression" in
                                                   face_data.keys()
                        else TypedList(float),
                        face_data["smile"] if "smile" in face_data.keys()
                        else TypedList(float),
                        int(face_data["id"]) if "id" in face_data.keys() else 0)

    @property
    def version(self):
        return 0.2

