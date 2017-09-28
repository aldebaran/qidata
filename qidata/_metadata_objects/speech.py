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

# Standard libraries
from distutils.version import StrictVersion

# Third-party libraries
from strong_typing.typed_parameters import (IntegerParameter as _Int,
                                            StringParameter as _Str)

# Local modules
from qidata.metadata_objects import MetadataObject

class Speech(MetadataObject):

    __ATTRIBUTES__ = [
                       _Str(name="name",
                            description="Name of the speaker",
                            default=""),
                       _Str(name="sentence",
                            description="Sentence pronounced",
                            default="")
    ]

    __ATT_VERSIONS__ = [None, None, None]

    __VERSION__="0.2"
    __DESCRIPTION__="Contains annotation details for a speech"

    __DEPRECATED_ATT_N_VERSIONS__ = [
                                      (_Int(name="id",
                                            description="",
                                            default=0), None, "0.2")
    ]

    # ───────────────────
    # Retro-compatibility

    @classmethod
    def _fromOldDict(cls, data, version):
        if version == StrictVersion("0.1"):
            data.pop("id")
        return cls(**data)