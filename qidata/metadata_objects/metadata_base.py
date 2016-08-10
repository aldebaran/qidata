

class MetadataObjectBase(object):
    """
    Base class for all metadata objects.

    This class needs to be extended in order to create
    new metadata objects classes.
    """
    def __init__(self):
        pass

    def toDict(self):
        raise NotImplementedError

    @staticmethod
    def fromDict(data = dict()):
        raise NotImplementedError