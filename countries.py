# -*- coding: utf-8 -*-

from qgis.PyQt.QtCore import *
from qgis.PyQt.QtGui import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from qgis.core import (QgsVectorLayer, QgsProject, QgsApplication, QgsMessageLog)

import os
import tempfile
import shutil
from pathlib import Path


def si_dialog(self):  
    self.w = QWidget()
    layout = QVBoxLayout(self.w)

    info_text = QLabel()
    layout.addWidget(info_text)
    info_text.setText("""Will load fishnet layer.  
    Last three attributes (points/m2, last point/m2, area) were calculated using lasinfo""")
    info_text.setAlignment(Qt.AlignCenter)


    bt = QPushButton()
    layout.addWidget(bt)
    bt.setText("Load fishnet layer D96TM")
    bt.clicked.connect(self.si_load_fishnet)
    self.w.setWindowTitle("Select download folder and data")
    text = QLabel()
    layout.addWidget(text)
    text.setText("<a href='http://www.evode.gov.si/index.php?id=87'>More Info on Data</a>")
    text.setAlignment(Qt.AlignCenter)
    text.setOpenExternalLinks(True)
    return self.w


def nl_dialog(self):  
    self.w = QWidget()
    layout = QVBoxLayout(self.w)

    info_text = QLabel()
    layout.addWidget(info_text)
    info_text.setText("""Choose series """)
    info_text.setAlignment(Qt.AlignCenter)


    bt = QPushButton()
    layout.addWidget(bt)
    bt.setText("Load fishnet layer for AHN1, AHN2 and AHN3")
    bt.clicked.connect(self.nl_load_AHN3)
    bt2 = QPushButton()
    layout.addWidget(bt2)
    bt2.setText("Load fishnet layer for AHN4")
    bt2.clicked.connect(self.nl_load_AHN4)
    self.w.setWindowTitle("Select download folder and data")
    text = QLabel()
    layout.addWidget(text)
    text.setText("<a href='https://www.ahn.nl/'>More Info on Data</a>")
    text.setAlignment(Qt.AlignCenter)
    text.setOpenExternalLinks(True)
    return self.w





        
        