# -*- coding: utf-8 -*-

# Copyright (c) 2017, Softbank Robotics Europe
# All rights reserved.

# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:

# * Redistributions of source code must retain the above copyright notice, this
#   list of conditions and the following disclaimer.

# * Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution.

# * Neither the name of the copyright holder nor the names of its
#   contributors may be used to endorse or promote products derived from
#   this software without specific prior written permission.

# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

from distutils.version import StrictVersion

# Third-party libraries
from strong_typing.typed_parameters import (IntegerParameter as _Int,
                                            StringParameter as _Str,
                                            EnumParameter as _Enum,
                                            VectorParameter as _Vect,
                                            FloatParameter as _Float)

# Local modules
from qidata.metadata_objects import MetadataObject

class FacialPart(MetadataObject):

    __ATTRIBUTES__ = [
                       _Vect(name="coordinates",
                             description="Coordinates of the face part",
                             type=int,
                             default=[]),
                       _Float(name="confidence",
                              description="",
                              default=0.0)
    ]

    __ATT_VERSIONS__ = [None, None]

    __VERSION__="0.1"
    __DESCRIPTION__="Contains a face part location with detection confidence"

class Face(MetadataObject):

    __ATTRIBUTES__ = [
                       _Str(name="name",
                            description="Name of the face's owner",
                            default=""),
                       _Int(name="age",
                            description="Age of the face's owner",
                            default=0),
                       _Enum(name="gender",
                             description="Gender of the face's owner",
                             choices=["female", "male"],
                             default="male"),
    ]

    __ATT_VERSIONS__ = [None, None,"0.2"]

    __VERSION__="0.4"
    __DESCRIPTION__="Contains annotation details for a face"

    __DEPRECATED_ATT_N_VERSIONS__ = [
                       (_Int(name="id",
                             description="A unique id given to this face through all relevant data",
                             default=0), None, "0.3"),
                       (_Vect(name="expression",
                              description="Estimation of the person's expression",
                              type=float,
                              default=[]), "0.2", "0.4"),
                       (_Vect(name="facial_parts",
                              description="Positions of faces features",
                              type=FacialPart,
                              default=[]), "0.2", "0.4"),
                       (_Vect(name="smile",
                              description="Smile intensity",
                              type=float,
                              default=[]), "0.2", "0.4"),
    ]

    # ───────────────────
    # Retro-compatibility

    @classmethod
    def _fromOldDict(cls, data, version):
        if version == StrictVersion("0.1"):
            data.pop("id")
        elif version == StrictVersion("0.2"):
            data.pop("fid") # An error turned "id" into "fid" on version 0.2
            data.pop("facial_parts") # facial_parts was changed in version 0.3, removed in version 0.4
            data.pop("expression") # removed in version 0.4
            data.pop("smile") # removed in version 0.4
        elif version == StrictVersion("0.3"):
            msg = "Warning: expression, facial_parts and smile have been recently removed from Face. "
            msg += "If you had any annotation there you need to keep, close your file without saving it "
            msg += "and contact maintainer."
            print msg
            data.pop("expression")
            data.pop("facial_parts")
            data.pop("smile")

        return cls(**data)
