# -*- coding: utf-8 -*-
from metadata_base import MetadataObjectBase

from typedlist import TypedList

class Speech(MetadataObjectBase):
    """Contains annotation details for a speech"""

    __slots__ = ["name", "sentence", "id"]

    def __init__(self, name="", sentence="", fid=0):
        super(Speech, self).__init__()
        self.name = name
        self.sentence = sentence
        self.id = fid

    @staticmethod
    def fromDict(speech_data):
        # Here we could discriminate how the dict is read, depending
        # on the message's version used.
        if not speech_data.has_key("version") or float(speech_data["version"]) > 0:
            # name : str
            # sentence : str
            # id : int
            return Speech(speech_data["name"] if speech_data.has_key("name") and speech_data["name"] is not None else "",
                speech_data["sentence"] if speech_data.has_key("sentence") and speech_data["sentence"] is not None else "",
                int(speech_data["id"]) if speech_data.has_key("id") else 0)

    @property
    def version(self):
        return 0.1

