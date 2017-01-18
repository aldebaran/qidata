Start with metadata objects
===========================

And here begins the serious stuff. Now that you are a bit more comfortable with our
vocabulary, we can start creating metadata !

The containers for metadata
---------------------------

Metadata is stored in special classes inherited from a :mod:`strong_typing` class
called :class:`strong_typing.VersionedStruct`. Without getting into details too much,
those classes allow to define a precise structure, with specific attributes of
a certain type. This guarantees a certain homogeneity between different annotators.
Besides, ``VersionedStruct`` can handle different versions of the same class. We will
talk more about this later and see why it is crucial.

For more specific information on ``VersionedStruct``, you can have a look :here:

Fill in a metadata object
-------------------------

To add a piece of information about a data object, we first need to create an
appropriate metadata object. To make this more interactive, we encourage you
to take a picture on the side and follow our guidelines. We will do the same,
with this picture:

.. image:: lenna.png

Let's try to add a few information on this picture ! First we will add some
contextual information.

    >>> from qidata.metadata_objects.context import *
    >>> context = Context()

Let's see what's available in this ``Context`` object.

.. autoclass:: qidata.metadata_objects.context.Context

.. autoclass:: qidata.metadata_objects.context.SpatialLocation

.. autoclass:: qidata.metadata_objects.context.Country

    All countries are present but the list is not displayed here
    as it is a very long one

.. autoclass:: qidata.metadata_objects.context.TimeLocation

.. autoclass:: qidata.metadata_objects.context.RecordingDevice

.. autoclass:: qidata.metadata_objects.context.DeviceModel
    :undoc-members:
    :inherited-members:

.. autoclass:: qidata.metadata_objects.context.EnvironmentalDescription

.. autoclass:: qidata.metadata_objects.context::EnvironmentalDescription.Category
    :undoc-members:
    :inherited-members:

.. autoclass:: qidata.metadata_objects.context.EnvironmentalLightConditions

.. autoclass:: qidata.metadata_objects.context::EnvironmentalLightConditions.FromOutdoor
    :undoc-members:
    :inherited-members:

.. autoclass:: qidata.metadata_objects.context::EnvironmentalLightConditions.FromIndoor
    :undoc-members:
    :inherited-members:

.. autoclass:: qidata.metadata_objects.context.EnvironmentalSoundConditions


We have no specific information on the recording's location, or datetime.
The recording device is also unknown (besides the picture is not directly out from
the camera but was scanned afterwards so...). Finally, it would probably be possible
to find the photographer's name, but I was lazy :).

    >>> context.recorder_names.append("M.Photographer")

``environmental_description`` is finally something we should be able to fill, at least
partially. Let's take a look at what information is needed.

    >>> # The scene seems to be indoor, probably a private house
    >>> context.environmental_description.category = EnvironmentalDescription.Category.INDOOR_HOUSE
    >>>
    >>> # Sun light is clearly coming from outside, but it is hard to guess if there
    >>> # is also an indoor lighting (there probably is but we can't say)
    >>> context.environmental_description.light_conditions.outdoor_light = EnvironmentalLightConditions.FromOutdoor.SUNNY_DAY_LIGHT
    >>> context.environmental_description.light_conditions.indoor_light = EnvironmentalLightConditions.FromIndoor.UNSPECIFIED

Finally, we have no information about the sound environmental conditions (it is a picture..)
so we leave it blank. And that's it ! You just made your first metadata object !


More metadata !
---------------

How about having more metadata on this picture ? We could for instance report that this
picture contains a Face, or a Person. There are several types available for annotation.

  .. autoclass:: qidata.MetadataType
    :undoc-members:
    :inherited-members:
