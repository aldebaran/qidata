# -*- coding: utf-8 -*-

# strong_typing
from strong_typing import VersionedStruct
from strong_typing.typed_parameters import (IntegerParameter,
                                            StringParameter)


class Object(VersionedStruct):

    __ATTRIBUTES__ = [
                       StringParameter(name="type",
                                       description="redball, qrcode, landmark, ...",
                                       default=""),
                       StringParameter(name="value",
                                       description="object description or decyphered value",
                                       default=""),
                       IntegerParameter(name="id",
                                        description="ID of the object",
                                        default=0)
    ]

    __ATT_VERSIONS__ = [None, None, None]

    __VERSION__="0.1"
    __DESCRIPTION__="""
    Contains annotation details for an object.
    It can be a random object or a visual tag.
    """
