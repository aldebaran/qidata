Key concepts
============

``qidata`` is made to handle data. But what kind of data ? Well, theoretically
all kinds. And if we missed one, please let us know [mail link].

But most importantly, it is made to handle data **on** data, what is commonly
called *metadata*. You probably have already heard of it. It is the "Artist" and
"Album" of a song, it is the "exposure", "ISO" or "timestamp" of a picture. All
this information that comes along with the real data, songs or pictures.

The QiDataObject interface
--------------------------

``qidata`` aims to generalize those common metadata to more atypic data type, like
laser scans or sonar data, but also to a mixture of several contents. As a result,
the most basic item in qidata is what we called a ``QiDataObject``.

  .. autoclass:: qidata.qidataobject.QiDataObject
    :members:

This class helps us to handle any piece of information containing both data and
metadata, without any prior assumption on the data type.

QiDataSets and QiDataFiles
--------------------------

Remember we wanted to use all available data for many purposes ? This means all
this data must be stored somewhere, along with its annotations. This is where
``QiDataFile`` and ``QiDataSet`` enter the game.

Both of them are implementations of :class:`QiDataObject`. ``QiDataFile`` stores
the annotations along with the data in the same file if it's possible, and
``QiDataSet`` contains several ``QiDataFile`` and has its own annotations that are
considered valid for all the data it contains.

:Example:
  If a QiDataSet has an annotation stating *"Peter's face is in the data"*, it means
  that every ``QiDataFile`` stored in the data set has Peter's face in it **even if
  it is not an image**. This kind of feature is actually pretty useful for contextual
  annotation like environmental conditions, or for a description of the recording
  device.
