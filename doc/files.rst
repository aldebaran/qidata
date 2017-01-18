Store your metadata: the QiDataFile
===================================

.. automodule:: qidata.qidatafile

Reading a QiDataFile
--------------------

To open and read a QiDataFile, use the ``open`` method.

.. autofunction:: qidata.qidatafile.open

The object you get is an opened QiDataFile.

The metadata is then accessible through the ``metadata`` property,
which transforms the metadata stored in the file into QiData's metadata
object instances.

.. autoattribute:: qidata.qidatafile.QiDataFile.metadata

You can also access the data of the file itself (not the metadata) as
you would for a regular file using:

.. autoattribute:: qidata.qidatafile.QiDataFile.raw_data

On this day, the data types we can support are the following ones

  .. autoclass:: qidata.DataType
    :inherited-members:

Other types will arrive as soon as we can :)


Updating / writing metadata in a QiDataFile
-------------------------------------------

To write metadata, you must open the file in "w" mode. Retrieve the ``metadata``
property and modify it the way you want.

Pay a particular attention to the structure of the metadata map which looks
like this::

    {
        "annotator's name": {
                "metadata type's name":(
                    "metadata type instance",
                    "annotation location"
                )
        }
    }

* metadata is a map whose keys are the annotators' names
* its values also are maps, whose keys are the names of the available
  metadata types
* Values of these maps must be 2-uple.
* First element of it is the metadata instance
* Second element of it is a list describing metadata's location (which
  is dependent on file type). It can also be None if the annotation does not
  concern a specific area.

Failure to respect this structure will prevent you to modify the metadata to
avoid unability to read the file later on.

:Example:
    If ``context`` is the metadata we created earlier:

        >>> from qidata import qidatafile
        >>> myFile = qidatafile.open("path/to/file", "w")
        >>> annotations = dict()
        >>> annotations["jdoe"] = dict() # add "jdoe" annotator
        >>> annotations["jdoe"]["Context"] = [(context, None)]# add metadata without location
        >>> myFile.metadata = annotations


In case you are not happy with your changes, it is always possible to cancel them
by reloading the file. However, this is only possible if you did not close the file
after changing ``metadata``.

.. automethod:: qidata.qidatafile.QiDataFile.reload

:Example:
    >>> from qidata import qidatafile
    >>> myFile = qidatafile.open("path/to/file", "w")
    >>> annotations = dict()
    >>> annotations["new_annotator"] = dict()
    >>> annotations["new_annotator"]["Context"] = [(context, None)]
    >>> myFile.metadata = annotations
    >>> myFile.reload()
    >>> annotations = myFile.metadata
    >>> annotations.has_key("new_annotator")
    False

When you are satisfied, call ``close`` to write your metadata instances into the
file.

.. automethod:: qidata.qidatafile.QiDataFile.close


It is important to close the file when finished, otherwise your changes won't be
saved. You can use the `with` statement to be sure not to forget, and you can use
the ``closed`` attribute to check if the file is still open.

.. autoattribute:: qidata.qidatafile.QiDataFile.closed


:Example:

    >>> myFile = qidatafile.open("path/to/file")
    >>> myFile.close()
    >>> myFile.closed
    True

    >>> with qidatafile.open("path/to/file") as myFile:
    ...     myFile.metadata # or anything else
    ...
    >>> myFile.closed
    True

Bravo ! Your metadata is now saved !

Other interesting attributes
----------------------------

There are a few other attributes that can be useful when using ``QiDataFile``

.. autoclass:: qidata.qidatafile.QiDataFile
  :members: type, mode, path, annotators


Finally, ``QiDataFile`` inherits from :class:`file`, so you can use the same method
you would use to read the file's data. However, if you need to open the file
differently (e.g. using OpenCV for an image) it must be done on the side.