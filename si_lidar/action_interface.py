import sys
from PyQt5.QtGui import *
from PyQt5.QtCore import *

class DlDialog:
    def __init__(self):
        self.w = QWidget()
        self.tex = QLineEdit(self.w)
        self.layout = QGridLayout(self.w)
     
    def window(self):
        bt1 = QPushButton()
        self.layout.addWidget(bt1, 3, 0)
        bt1.setText("Show message!")
        bt1.move(50,50)
        
        bt2 = QPushButton(self.w)
        bt2.setText("Select download folder")
        bt2.move(250,10)
        radiobutton = QRadioButton(self.w)
        radiobutton.move(300,30)
        radiobutton.setText('ssds')
        self.layout.addWidget(radiobutton, 0, 0)
        radiobutton2 = QRadioButton(self.w)
        radiobutton2.move(300,35)
        radiobutton2.setText('cdscsds')
        
        self.cb1 = QCheckBox(self.w)
        self.cb1.setText('ssds')
        self.cb1.move(30,30)
        
        
        bt2.clicked.connect(self.on_click)
        bt1.clicked.connect(self.showdialog)
        self.w.setWindowTitle("Lidar Downloader")
        return self.w, self.tex


    def file_dialog():
        dlg = QFileDialog()
        dlg.setFileMode(dlg.Directory)
        dlg.show()

        if dlg.exec_():
            filenames = dlg.selectedFiles()
            print(filenames)
        
    def on_click(self):
        if self.cb1.isChecked():
            print('true')
        print('ssss')
            
    def showdialog():
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

        def msgbtn(i):
            print("Button pressed is:",i.text())


dialog = DlDialog()
w = dialog.window()[0]
w.show()
