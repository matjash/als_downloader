# -*- coding: utf-8 -*-

from qgis.PyQt.QtCore import *
from qgis.PyQt.QtGui import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from qgis.core import (QgsVectorLayer, QgsProject, QgsApplication, QgsMessageLog)

import os
import tempfile
import shutil
from pathlib import Path


def si_dialog(self):  
    self.w = QWidget()
    layout = QVBoxLayout(self.w)
    bt = QPushButton()
    layout.addWidget(bt)
    bt.setText("Load fishnet layer")
    bt.clicked.connect(self.si_load_fishnet)
    self.w.setWindowTitle("Select download folder and data")
    text = QLabel()
    layout.addWidget(text)
    text.setText("<a href='http://www.evode.gov.si/index.php?id=87'>More Info</a>")
    text.setAlignment(Qt.AlignCenter)
    text.setOpenExternalLinks(True)
    return self.w




        
        