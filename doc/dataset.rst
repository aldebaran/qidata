Organize your metadata: the QiDataSet
=====================================

Now that you have an annotated file, and probably many others, you might want to
make it available to your co-workers. But you might also simply wish to gather
all alike data, like pictures with faces of different persons. These are the
main purposes of QiDataSets.

A folder that contains your QiDataFiles
---------------------------------------

QiDataSet creation
++++++++++++++++++

At first, a QiDataSet is nothing more than a folder containing your QiDataFiles.
Which is why it is the first step to create a QiDataSet. Just add a few
QiDataFiles into a folder, and you're almost ready. The next thing is to open
the folder as a QiDataSet in "w" mode in order to add a special file that will
contain the metadata at the data set level, ``metadata.xmp``.

	>>> from qidata import QiDataSet
	>>> with QiDataSet("path/to/qidataset", "w"):
	...     pass

And that's it. Your first QiDataSet is created and ready to do magic for you.
Add the file annotated previously in a folder and try this out !

QiDataSet content exploration
+++++++++++++++++++++++++++++

Once it is created, the QiDataSet will make its best to concentrate all the
information about your files that can be. You can of course retrieve the list
of files contained by it.

.. autoattribute:: qidata.qidataset.QiDataSet.raw_data

You can also open the files and folders contained in your dataset directly
from it.

.. automethod:: qidata.qidataset.QiDataSet.openChild

But the best part of QiDataSet's API is that you can actually know what is in
your dataset without opening every file in it.

.. autoattribute:: qidata.qidataset.QiDataSet.content

``qidata.qidataset.QiDataSetContent`` comes with four properties and one method

.. autoclass:: qidata.qidataset.QiDataSetContent
    :members: __init__, annotators, annotation_types, file_types, partial_annotations,
              setMetadataAsTotal

Let's try that out shall we ?

	>>> ds = QiDataSet("path/to/folder", "r")
	>>> c = ds.content
	>>> print c.annotators
	[]
	>>> print c.annotation_types
	[]
	>>> print c.file_types
	["IMAGE"]
	>>> print c.partial_annotations
	[("jdoe", "Context")]

For now, all annotations are considered as `partial` because they have been
discovered automatically. A user input is necessary to upgrade an annotation
from `partial` to `total`. For this, let's close our dataset and re-open it in
"w" mode to save the change we are about to make.

	>>> ds = QiDataSet("path/to/folder", "w")
	>>> c = ds.content
	>>> c.setMetadataAsTotal("jdoe", "Context")
	>>> print c.annotators
	["jdoe"]
	>>> print c.annotation_types
	["Context"]
	>>> print c.file_types
	["IMAGE"]
	>>> print c.partial_annotations
	[]
	>>> ds.close()

Now let's assume a new metadata has been added. For instance, another user,
named "jsmith", also made a Context object, linked to our image. Let's also
assume a new file was added, like a WAV file for instance.

	>>> ds = QiDataSet("path/to/folder", "w")
	>>> c = ds.content
	>>> print c.annotators
	["jdoe"]
	>>> print c.annotation_types
	["Context"]
	>>> print c.file_types
	["IMAGE"]
	>>> print c.partial_annotations
	[]

What happened ? Why are the new annotator and new file type not shown ? Well
this is because we don't want to examine each file for new types or annotations
every time the dataset is opened. It is only done when the dataset is created
the first time and when a call to ``examineContent`` is done.

.. automethod:: qidata.qidataset.QiDataSet.examineContent

::

	>>> ds.examineContent()
	>>> print c.annotators
	["jdoe"]
	>>> print c.annotation_types
	["Context"]
	>>> print c.file_types
	["IMAGE", "AUDIO"]
	>>> print c.partial_annotations
	[("jsmith", "Context")]
	>>> ds.close()

You can now easily filter your data sets based on their content. For instance, if
``data_set_list`` contains all your dataset's path, you can retrieve all the
sets totally annotated by "jdoe" like this:

	>>> filtered = []
	>>> for path in data_set_list:
	... 	with QiDataSet(path, "r") as _ds:
	... 		if "jdoe" in _ds.content.annotators:
	... 			filtered.append(f)

Or even easier, you can use the static method ``contentFromPath`` to do so.

.. automethod:: qidata.qidataset.QiDataSet.contentFromPath

::

	>>> filtered = [f for f in data_set_list if "jdoe" in QiDataSet.contentFromPath(f).annotators]

.. note::
	If you want to filter your datasets over several conditions, using the
	first version is better as it will avoid several opening of the same dataset.


A container for global metadata
-------------------------------

Just like on any file, you can add metadata on a QiDataSet. The syntax is
exactly the same as the one used for QiDataFiles::

	>>> from qidata import QiDataSet
	>>> with QiDataSet("path/to/qidataset", "w") as _ds:
	...     annotations = dict()
	...     annotations["jdoe"] = dict() # add "jdoe" annotator
	...     annotations["jdoe"]["Context"] = [(context, None)]
	...     _ds.metadata = annotations

And exactly as for a file, changes in metadata are only saved upon closure,
whether it's via a ``with`` statement or through a call to the ``close()`` method.

.. automethod:: qidata.qidataset.QiDataSet.close

The following code is strictly equivalent to the one above::

	>>> from qidata import QiDataSet
	>>> _ds = QiDataSet("path/to/qidataset", "w")
	>>> annotations = dict()
	>>> annotations["jdoe"] = dict() # add "jdoe" annotator
	>>> annotations["jdoe"]["Context"] = [(context, None)]
	>>> _ds.metadata = annotations
	>>> _ds.close()

The metadata stored at the QiDataSet level is considered applicable to any
QiDataFile contained by the QiDataSet. This can save a lot of time (one
annotation instead of many) and is very convenient for ``Context`` metadata.

Finally, ``QiDataSet`` provides a similar API to QiDataFile:

	.. autoclass:: qidata.qidataset.QiDataSet
	    :members: type, raw_data, mode, path, closed, reloadMetadata


Current limitations
-------------------

Currently, QiDataSet cannot properly handle nested datasets. We advise you to
use only QidataFiles in your data sets for now. This feature will arrive as
soon as we can.

.. Gogo qidata_gui !!