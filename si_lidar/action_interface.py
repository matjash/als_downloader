import sys
from PyQt5.QtGui import *
from PyQt5.QtCore import *

class DlDialog:
    def __init__(self):
        self.w = QWidget()
        self.layouth = QVBoxLayout(self.w)
        self.f = QgsFileWidget()
        self.layout = QGridLayout()
     
    def window(self):
        self.f.setDialogTitle('Select Download Folder')
        self.f.setStorageMode(1)
        self.layouth.addWidget(self.f)
        self.layouth.addLayout( self.layout )
        

        rb1 = QRadioButton()
        rb1.setText('Download GKOT (laz)')
        self.layout.addWidget(rb1, 0, 0)
        
        rb2 = QRadioButton()
        rb2.setText('Download OTR (laz)')
        self.layout.addWidget(rb2, 1, 0)
        
        rb3 = QRadioButton()
        rb3.setText('Download DEM (asc)')
        self.layout.addWidget(rb3, 2, 0)
        
        self.cb1 = QCheckBox(self.w)
        self.cb1.setText('Include Technical Report')
        self.layout.addWidget(self.cb1, 2, 1)
        
        """
        bt1 = QPushButton()
        self.layout.addWidget(bt1, 100, 20)
        bt1.setText("Show message!")
        """
        
        bt2 = QPushButton()
        self.layouth.addWidget(bt2)
        bt2.setText("Download")
     
        #bt2.clicked.connect(self.on_click)
        bt2.clicked.connect(self.showdialog)
        self.w.setWindowTitle("Select download folder and data")
        return self.w
       
    def on_click(self):
        if self.cb1.isChecked():
            print('true')
        a = self.f.filePath()
        print(a)
            
    def showdialog(self):
        def msgbtn(i):
            print("Button pressed is:",i.text())
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText("This is a message box")
        msg.setInformativeText("This is additional information")
        msg.setWindowTitle("MessageBox demo")
        msg.setDetailedText("The details are as follows:")
        msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        msg.buttonClicked.connect(msgbtn)
        
        retval = msg.exec_()
        print("value of pressed message box button:", retval)


        


dialog = DlDialog()
w = dialog.window()
w.show()
