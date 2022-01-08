from qgis.PyQt.QtCore import QSettings, QCoreApplication
from qgis.PyQt.QtGui import QIcon, QPixmap
from qgis.PyQt.QtWidgets import (QDialogButtonBox,
                                QCheckBox)
from qgis.core import (QgsProject,
                       QgsRasterLayer,
                       QgsVectorLayer,
                       QgsLayerDefinition,
                       QgsCoordinateReferenceSystem,
                       QgsLayerTreeLayer

                       )

from ld_folder_select import LDFolderSelect


class si_dl:
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
        print(LDFolderSelect)
        self.dlg = LDFolderSelect()



        """
        self.dlg.buttonBox.button(QDialogButtonBox.Cancel).clicked.connect(self.dlg.close)
        self.dlg.buttonBox.button(QDialogButtonBox.Ok).clicked.connect(self.load_layers)
        self.dlg.buttonBox.button(QDialogButtonBox.Ok).clicked.connect(self.dlg.close)
        self.dlg.remove_layers.clicked.connect(self.remove_layers)
        self.dlg.label_2.setPixmap(QPixmap(str(logo_path)))
        # Declare instance attributes
        self.first_start = None
        """

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
