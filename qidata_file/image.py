# -*- coding: utf-8 -*-

# Qt
from PySide.QtGui import QPixmap

# Local
from .qidatafile import QiDataFile

class Image(QiDataFile):

    # ───────────
    # Constructor

    def __init__(self, source_path):
        super(Image, self).__init__(source_path, True)
