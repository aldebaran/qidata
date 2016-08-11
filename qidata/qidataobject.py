
class QiDataObject(object):
    """
    Interface class representing a generic "data" element.

    Data can be any piece of raw data (image, audio, text, whatever)
    carrying metadata information.
    """

    @property
    def raw_data(self):
        """
        Object's raw data
        """
        raise NotImplementedError

    @property
    def metadata(self):
        """
        Object's metadata list
        """
        raise NotImplementedError

    @property
    def type(self):
        """
        Object's data type
        """
        raise NotImplementedError