from metadata_base import MetadataObjectBase

class Person(MetadataObjectBase):
    """
    Contains annotation details for a person

    Person version 0.1:
     - name
        Name of the person represented
        Can be used to test person recognition

     - id
        A unique id given to this person through all relevant data
        Can be used to test a person tracker
    """

    def __init__(self, name="", pid=0):
        super(Person, self).__init__()
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
