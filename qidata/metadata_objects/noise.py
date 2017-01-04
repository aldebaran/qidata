
# strong_typing
from strong_typing import VersionedStruct
from strong_typing.typed_parameters import (IntegerParameter,
                                            StringParameter)

## SHAME THIS IS JUST A COPY PASTE AND IT HAS BEEN RELEASED !!

class Noise(VersionedStruct):

    __ATTRIBUTES__ = [
                       StringParameter(name="name",
                                       description="",
                                       default=""),
                       IntegerParameter(name="id",
                                        description="",
                                        default=0)
    ]

    __ATT_VERSIONS__ = [None, None]

    __VERSION__="0.1"
    __DESCRIPTION__="Contains annotation details for a noise"
