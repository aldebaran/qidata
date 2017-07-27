# -*- coding: utf-8 -*-

# Third-party libraries
from strong_typing.typed_parameters import (IntegerParameter as _Int,
                                            StringParameter as _Str)

# Local modules
from qidata.metadata_objects import MetadataObject

class Object(MetadataObject):

    __ATTRIBUTES__ = [
                       _Str(name="type",
                            description="redball, qrcode, landmark, ...",
                            default=""),
                       _Str(name="value",
                            description="object description or decyphered value",
                            default=""),
                       _Int(name="id",
                            description="ID of the object",
                            default=0)
    ]

    __ATT_VERSIONS__ = [None, None, None]

    __VERSION__="0.1"
    __DESCRIPTION__="""
    Contains annotation details for an object.
    It can be a random object or a visual tag.
    """
