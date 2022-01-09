from PyQt5.QtGui import *
from PyQt5.QtCore import *
from qgis.PyQt.QtCore import QCoreApplication
from qgis.core import (QgsVectorLayer, QgsProject, QgsApplication, QgsMessageLog)

import os
import tempfile
import shutil
from pathlib import Path

class SiLidarDownload:
    def __init__(self, iface):
        self.iface = iface
        pass

    def tr(self, message):
        """Get the translation for a string using Qt translation API.

        We implement this ourselves since we do not inherit QObject.

        :param message: String for translation.
        :type message: str, QString

        :returns: Translated version of message.
        :rtype: QString
        """
        # noinspection PyTypeChecker,PyArgumentList,PyCallByClass
        return QCoreApplication.translate('LidarDownloader', message)

    def load_fishnet(self): 
        #aa = self.window()
        #aa.close()
        self.iface.messageBar().pushMessage("efefesfeds", duration=5)   
        try:
            tmp = tempfile.mkdtemp()
            src = Path(os.path.dirname(__file__))/'fishnets\SI_LIDAR FISHNET D96.gpkg'
            tmp = Path(tmp)/'SI_LIDAR FISHNET D96.gpkg'
            shutil.copyfile(str(src), str(tmp))
            src = str(tmp)
        except:
            src = Path(os.path.dirname(__file__))/'fishnets\SI_LIDAR FISHNET D96.gpkg'  
        layer = str(src) + "|layername=SI_LIDAR FISHNET D96"
        vlayer = QgsVectorLayer(layer, "SI_LIDAR FISHNET D96", "ogr")
        vlayer.setReadOnly()
        QgsProject.instance().addMapLayer(vlayer)

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
        self.iface.messageBar().pushMessage("sssssssss", duration=5)  
        return self.w
    




        
        