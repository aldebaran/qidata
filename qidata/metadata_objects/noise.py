from metadata_base import MetadataObjectBase

class Noise(MetadataObjectBase):
    """Contains annotation details for a noise"""

    __slots__ = ["name", "id"]

    def __init__(self, name="", pid=0):
        super(Noise, self).__init__()
        self.name = name
        self.id = pid

    def toDict(self):
        return dict(name=self.name,  id=self.id)

    @staticmethod
    def fromDict(noise_data):
        # Here we could discriminate how the dict is read, depending
        # on the message's version used.
        if not noise_data.has_key("version") or float(noise_data["version"]) > 0:
            # name : str
            # id : int
            return Noise(noise_data["name"] if noise_data.has_key("name") and noise_data["name"] is not None else "",
                int(noise_data["id"]) if noise_data.has_key("id") else 0)

    @property
    def version(self):
        return 0.1
