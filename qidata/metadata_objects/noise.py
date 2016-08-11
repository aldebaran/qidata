from metadata_base import MetadataObjectBase

class Noise(MetadataObjectBase):
    """Contains annotation details for a noise"""

    def __init__(self, name="", pid=0):
        super(Noise, self).__init__()
        self.name = name
        self.id = pid

    def toDict(self):
        return dict(name=self.name,  id=self.id)

    @staticmethod
    def fromDict(person_data):
        # Here we could discriminate how the dict is read, depending
        # on the message's version used.
        if not person_data.has_key("version") or float(person_data["version"]) > 0:
            # name : str
            # id : int
            return Person(person_data["name"] if person_data.has_key("name") else "",
                int(person_data["id"]) if person_data.has_key("id") else 0)

    @property
    def version(self):
        return 0.1
