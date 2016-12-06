# -*- coding: utf-8 -*-


class TypedList(list):
    """
    Contains a list of typed objects.
    """

    # ───────────
    # Constructor

    def __init__(self, typename, args=[]):
        """
        Create a TypedList

        :param typename: Type to be accepted in the list (type or class)
        :param args: List of initialization arguments (can be empty)
        :raises: TypeError if argument type is invalid
        """
        self.__typename = typename
        for element in args:
            if not isinstance(element, self.__typename):
                msg = "TypedList: list elements are expected to be %s. %s received"
                msg = msg % (self.__typename, type(element))
                raise TypeError(msg)
        super(TypedList, self).__init__(args)


    # ───────
    # Methods

    def append(self, element=None):
        if element is None:
            return
        if isinstance(element, self.__typename):
            super(TypedList, self).append(element)
        else:
            msg = "TypedList: list elements are expected to be %s. %s received"
            msg = msg%(self.__typename, type(element))
            raise TypeError(msg)

    def appendDefault(self):
        self.append(self.__typename())

    # ──────────
    # Properties

    @property
    def typename(self):
        return self.__typename


class FacialPartsList(list):
    """
    List of typed objects, for FacialParts provided by FaceCharacteristics:
        [TypedList(int), float] which corresponds to [[coordinates], confidence]
    """
    def __init__(self, typedlist_ini=None, float_ini=float()):
        """
        Create a FacialPartsList.

        Args:
            typedlist_ini: initialization value for the TypedList object.
            float_ini: initial value for the float element.

        Raises:
            TypeError: if initial value type does not match given
                typename.
            ValueError: if initial values are not given to all elements.
                (either no initial values are given or either initial values are
                given to all elements)
        """
        self.__typename = [TypedList, float]
        super(FacialPartsList, self).__init__()
        if typedlist_ini is not None:
            self.append([TypedList(int, args=typedlist_ini), float_ini])

    def append(self, p_object):
        """
        Verify type and append object to the typed list.

        Args:
            p_object: object to append.

        Raises:
            ValueError: if object size does not match the MixedTypedList
                signature.
            TypeError: if object type is invalid.
        """
        # Check p_object type:
        if not isinstance(p_object, list):
            raise TypeError("FacialPartsList: Only lists can be appended.")

        # Check size of the the element to append
        if len(self.__typename) != len(p_object):
            raise ValueError("FacialPartsList: Not enough element in the "
                             "object <{}> to append. Got {} instead of {}."
                             .format(p_object,
                                     len(p_object),
                                     len(self.__typename)))

        # Check types of elements in the object to append
        for _type, _value in zip(self. __typename, p_object):
            if not isinstance(_value, _type):
                raise TypeError("FacialPartsList: Unexpected type for element "
                                "<{}>. Got {} instead of {}."
                                .format(_value, type(_value), _type))

        # Append
        super(FacialPartsList, self).append(p_object)

    def appendDefault(self):
        self.append([TypedList(int), float()])

    @property
    def typename(self):
        return self.__typename
