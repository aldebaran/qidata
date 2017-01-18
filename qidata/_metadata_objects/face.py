# -*- coding: utf-8 -*-

from distutils.version import StrictVersion

# strong_typing
from strong_typing import VersionedStruct
from strong_typing.typed_parameters import (IntegerParameter,
                                            StringParameter,
                                            EnumParameter,
                                            VectorParameter,
                                            FloatParameter)

class FacialPart(VersionedStruct):

    __ATTRIBUTES__ = [
                       VectorParameter(name="coordinates",
                                       description="Coordinates of the face part",
                                       type=int,
                                       default=[]),
                       FloatParameter(name="confidence",
                                       description="",
                                       default=0.0)
    ]

    __ATT_VERSIONS__ = [None, None]

    __VERSION__="0.1"
    __DESCRIPTION__="Contains a face part location with detection confidence"


class Face(VersionedStruct):
    """
    Face (current version: 0.2):
        - name:
            Name of the person whose face is represented
            Can be used to test face recognition

        - age:
            Age of the person whose face is represented
            Can be used to test age estimation

        - id:
            A unique id given to this face through all relevant data
            Can be used to test a face tracker

        - Expression (appeared in version 0.2):
            Given by FaceCharacteristics: facial expression values.

        - FacialParts (appeared in version 0.2):
            Given by FaceCharacteristics: positions of different facial parts.

        - Gender (appeared in version 0.2):
            Gender of the target

        - Smile (appeared in version 0.2):
            Given by FaceCharacteristics: smile values of the associated face.
    """

    __ATTRIBUTES__ = [
                       StringParameter(name="name",
                                       description="Name of the face's owner",
                                       default=""),
                       IntegerParameter(name="age",
                                       description="Age of the face's owner",
                                       default=0),
                       VectorParameter(name="expression",
                                       description="Name of the person represented",
                                       type=float,
                                       default=[]),
                       VectorParameter(name="facial_parts",
                                       description="Name of the person represented",
                                       type=FacialPart,
                                       default=[]),
                       EnumParameter(name="gender",
                                       description="Name of the person represented",
                                       choices=["female", "male"],
                                       default="male"),
                       VectorParameter(name="smile",
                                       description="Name of the person represented",
                                       type=float,
                                       default=[]),
    ]

    __ATT_VERSIONS__ = [None, None,"0.2","0.2","0.2","0.2"]

    __VERSION__="0.3"
    __DESCRIPTION__="Contains annotation details for a face"

    __DEPRECATED_ATT_N_VERSIONS__ = [
                       (IntegerParameter(name="id",
                                        description="A unique id given to this face through all relevant data",
                                        default=0), None, "0.3")
    ]

    # ───────────────────
    # Retro-compatibility

    @classmethod
    def _fromOldDict(cls, data, version):
        if version == StrictVersion("0.1"):
            data.pop("id")
        elif version == StrictVersion("0.2"):
            data.pop("fid")
            fps_in = data.pop("facial_parts")
            fps_out = list()
            for fp in fps_in:
                new_fp = FacialPart.fromDict(dict(coordinates=fp[0], confidence=fp[1], version="0.1"))
                fps_out.append(new_fp)
            data["facial_parts"] = fps_out
        return cls(**data)
