# -*- coding: utf-8 -*-

from qgis.PyQt.QtCore import QSettings, QTranslator, QCoreApplication
from qgis.PyQt.QtGui import QIcon, QPixmap
from qgis.PyQt.QtWidgets import (QAction,
                                QMenu,
                                QDialogButtonBox,
                                QCheckBox)
from qgis.core import (QgsProject,
                       QgsRasterLayer,
                       QgsVectorLayer,
                       QgsLayerDefinition,
                       QgsCoordinateReferenceSystem,
                       QgsLayerTreeLayer

                       )
import tempfile
import shutil


# Initialize Qt resources from file resources.py
from ..resources import *
# Import the code for the dialog
from .lidar_slovenia_dialog import LidarSloveniaDialog
import os.path
from pathlib import Path

import tempfile
import shutil

class LidarSlovenia:
    """QGIS Plugin Implementation."""

    def __init__(self, iface):
        """Constructor.

        :param iface: An interface instance that will be passed to this class
            which provides the hook by which you can manipulate the QGIS
            application at run time.
        :type iface: QgsInterface
        """
        # Save reference to the QGIS interface
        self.iface = iface
        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)
        # initialize locale
        locale = QSettings().value('locale/userLocale')[0:2]
        locale_path = os.path.join(
            self.plugin_dir,
            'i18n',
            'ArheoloskiGis_{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)
            QCoreApplication.installTranslator(self.translator)

        self.dlg = ArheoloskiGisLoadDialog()


        self.dlg.buttonBox.button(QDialogButtonBox.Cancel).clicked.connect(self.dlg.close)
        self.dlg.buttonBox.button(QDialogButtonBox.Ok).clicked.connect(self.load_layers)
        self.dlg.buttonBox.button(QDialogButtonBox.Ok).clicked.connect(self.dlg.close)
        self.dlg.remove_layers.clicked.connect(self.remove_layers)


        logo_path = path('icons')/"loader_logo_small"
        self.dlg.label_2.setPixmap(QPixmap(str(logo_path)))
        # Declare instance attributes
        self.actions = []
        self.first_start = None

    # noinspection PyMethodMayBeStatic
    def tr(self, message):
        """Get the translation for a string using Qt translation API.

        We implement this ourselves since we do not inherit QObject.

        :param message: String for translation.
        :type message: str, QString

        :returns: Translated version of message.
        :rtype: QString
        """
        # noinspection PyTypeChecker,PyArgumentList,PyCallByClass
        return QCoreApplication.translate('ArheoloskiGis', message)


    def add_action(
        self,
        icon_path,
        text,
        callback,
        enabled_flag=True,
        add_to_menu=True,
        add_to_toolbar=True,
        status_tip=None,
        whats_this='aaa',
        parent=None):

        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        action.setEnabled(enabled_flag)

        if status_tip is not None:
            action.setStatusTip(status_tip)

        if whats_this is not None:
            action.setWhatsThis(whats_this)

        if add_to_toolbar:
            # Adds plugin icon to Plugins toolbar
            self.iface.addToolBarIcon(action)

        if add_to_menu:
            self.iface.addPluginToMenu(
                self.menu,
                action)

        self.actions.append(action)

        return action

    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""

        icon_path = ':/plugins/agis/icons/icon.png'
        self.add_action(
            icon_path,
            text=self.tr(u'AGIS'),
            callback=self.run,
            parent=self.iface.mainWindow())
        # will be set False in run()

        self.first_start = True

    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        for action in self.actions:
            self.iface.removePluginMenu(
                self.tr(u'&Slovenia'),
                action)
       


    def run(self):
        """Run method that performs all the real work"""
        if self.first_start == True:
            self.first_start = False
        # show the dialog
        self.dlg.show()
        # Run the dialog event loop
        result = self.dlg.exec_()
        # See if OK was pressed
        if result:
            # Do something useful here - delete the line containing pass and
            # substitute with your code.
            pass



   
    def load_layers(self):
        root = QgsProject.instance().layerTreeRoot()
        crs = QgsCoordinateReferenceSystem("EPSG:3794")

        if access(self):
            self.iface.messageBar().pushMessage(self.tr("Povezava s podatkovno bazo CPA uspešna.."))
        else:
            self.iface.messageBar().pushMessage(self.tr("Nalagam brez CPA slojev.."))

        #To prevent folder locking of Plugin directory
        try:
            tmp = tempfile.mkdtemp()
            src = path('qlrs')
            shutil.rmtree(tmp)
            shutil.copytree(str(src), tmp)
            styles_path = Path(tmp)
        except:
            self.iface.messageBar().pushMessage(self.tr('Berem qlr iz mape vtičnika...'))





        vlayer = postgis_connect(self, "public", "Katalog najdišč", "geom", "kid")
        QgsProject.instance().addMapLayer(vlayer, False)  
        arheo_group.insertChildNode(0, QgsLayerTreeLayer(vlayer))
