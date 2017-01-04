# -*- coding: utf-8 -*-

"""
    ``qidata`` package
    ==================

    This package contains or will contain in the near future several tools designed to
    facilitate data annotation and datasets handling.

    It provides libraries desgined to easilly construct metadata objects depending on the concerned
    data type and is built on an external library (Adobe's XMP) to store those metadata with the concerned
    file.
    However, using those metadata is not restricted to a file, it could later be simply used to display specific
    information on an data stream for instance.

"""

import os

# ––––––––––––––––––––––––––––
# Convenience version variable

VERSION = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), "VERSION")).read().split()[0]

#––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––#
