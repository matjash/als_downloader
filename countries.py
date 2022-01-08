from PyQt5.QtGui import *
from PyQt5.QtCore import *
from qgis.utils import iface

import os
import tempfile
import shutil
from pathlib import Path

class SiLidarDownload:
    def __init__(self, iface):
        pass

    def window(self):  
        self.w = QWidget()
        self.layout = QVBoxLayout(self.w)
        bt = QPushButton()
        self.layout.addWidget(bt)
        bt.setText("Load fishnet layer")
        bt.clicked.connect(self.load_fishnet)
        self.w.setWindowTitle("Select download folder and data")
        text = QLabel()
        self.layout.addWidget(text)
        text.setText("<a href='http://www.evode.gov.si/index.php?id=87'>More Info</a>")
        text.setAlignment(Qt.AlignCenter)
        text.setOpenExternalLinks(True)
        return self.w
    


