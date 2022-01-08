import sys
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import qgis.utils
import requests
from urllib.parse import urlparse
import webbrowser
from qgis.core import (
    QgsApplication, QgsTask, QgsMessageLog)


class DlDialog:
    def __init__(self):
        self.MESSAGE_CATEGORY = 'Lidar downloader'
        self.w = QWidget()
        self.layouth = QVBoxLayout(self.w)
        self.f = QgsFileWidget()
        self.layout = QGridLayout()

        self.iface=qgis.utils.iface
        #layer_id = '[%@layer_id%]'
        #layer = QgsProject().instance().mapLayer(layer_id)
        layer = self.iface.activeLayer()

        self.features = layer.selectedFeatures()
        if len(self.features) == 0:
            feature = '[% $id %]'
            layer.select(feature)
            self.features = layer.selectedFeatures()

        self.grids_list = []
        self.areas = set()
        for f in self.features:
            grid = [f[2], f[22]]
            self.grids_list.append(grid)
            self.areas.add(f[22])
        self.task = QgsTask.fromFunction('Downloading grids', self.download_task, on_finished=completed)
     
    def window(self):       
        self.f.setDialogTitle('Select Download Folder')
        self.f.setStorageMode(1)
        self.layouth.addWidget(self.f)
        self.layouth.addLayout( self.layout )
        

        self.rb1 = QRadioButton('Download GKOT (laz)')
        self.rb1.data = 'gkot'
        self.layout.addWidget(self.rb1, 0, 0)
        
        self.rb2 = QRadioButton('Download OTR (laz)')
        self.rb2.data = 'otr'
        self.layout.addWidget(self.rb2, 1, 0)
        
        self.rb3 = QRadioButton('Download DEM (asc)')
        self.rb3.data = 'asc'
        self.layout.addWidget(self.rb3, 2, 0)
        
        self.cb1 = QCheckBox(self.w)
        self.cb1.setText('Include Technical Report')
        self.layout.addWidget(self.cb1, 2, 1)
                
        bt2 = QPushButton()
        self.layouth.addWidget(bt2)
        bt2.setText("Download")
     
        source = QLabel()
        self.layouth.addWidget(source)
        source.setText("<a href='http://www.evode.gov.si/index.php?id=87'>More Info</a>")
        source.setAlignment(Qt.AlignCenter)
        source.setOpenExternalLinks(True)
        
        bt2.clicked.connect(self.on_click)
        self.w.setWindowTitle("Select download folder and data")
        return self.w
       
    def on_click(self):
        if self.cb1.isChecked():
            self.include_report = True
        else:
            self.include_report = False
        self.dest_folder = self.f.filePath()
        rbs = (self.rb1, self.rb2, self.rb3)
        for rb in rbs:
            if rb.isChecked():
                self.d_type = rb.data
        self.window().close()
        self.showdialog()

        a = self.f.filePath()
        print(a)
        

            
    def showdialog(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText("This is a message box")
        msg.setInformativeText("This is additional information")
        msg.setWindowTitle("MessageBox demo")
        msg.setDetailedText("The details are as follows:")
        msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        msg.buttonClicked.connect(self.msgbtn)
        retval = msg.exec_()
  

    def download_task(self, task):
        grids_downloaded = 0
        total_size = 0
        size_downloaded = 0
        url_list = []
        total_len = len(self.grids_list)
        for grid in self.grids_list:
            url = self.dl_url(self.d_type, str(grid[0]), str(grid[1]))
            response = requests.head(url)
            if response.status_code == 200:
                size = int(requests.head(url).headers['content-length'])
                url_list.append(url)
            else:
                text = 'Grid %s not found!' %grid
                return Exception(text)
            total_size += size  
            
        
        total_size = round((total_size/1000000), 2)
        
        QgsMessageLog.logMessage('Selected %s grids, %s MB' %(str(total_len), str(total_size)),
                               self.MESSAGE_CATEGORY, Qgis.Info)

     
        for url in url_list:
            response = requests.get(url, stream=True)
            print(url)
            file_name = urlparse(url)
            file_name = file_name.path.rsplit("/", 1)[-1]
            print(file_name)
            dest_filename = self.dest_folder + '\\' + file_name
            print(dest_filename)
            if response.status_code == 200:
                with open(dest_filename, 'wb') as f:
                    a = 0
                    for chunk in response.iter_content(chunk_size = 1024*1024):
                        f.write(chunk)
                        diff= os.path.getsize(dest_filename)-a
                        a = os.path.getsize(dest_filename)
                        size_downloaded += diff/(1024*1024)
                        progress = round(((100*size_downloaded)/total_size),0)
                        task.setProgress(progress)
                        if task.isCanceled():
                            stopped(task)
                            return None
                grids_downloaded += 1
            else:
                QgsMessageLog.logMessage('Url for grid %s not valid, skipping.' % file_name,
                    self.MESSAGE_CATEGORY, Qgis.Warning)
            
        grids_skipped = total_len - grids_downloaded

        return {'grids_downloaded': grids_downloaded, 'grids_skipped': grids_skipped , 'dest_folder':self.dest_folder,
                'task': task.description()}

    

    def msgbtn(self,i):
        if i.text() == 'OK':
            if self.include_report:
                get_report(self.areas, self.dest_folder)       

            QgsApplication.taskManager().addTask(self.task)
        elif i.text() == 'Cancel':
            print(i.text())
   

    #downloading stuff
    def dl_url(self, d_type, grid, area):
        if d_type == 'gkot':
            url = 'http://gis.arso.gov.si/lidar/%s/laz/%s/D96TM/TM_%s.laz' % (d_type, area, grid)
        elif d_type == 'otr':
            url = 'http://gis.arso.gov.si/lidar/%s/laz/%s/D96TM/TMR_%s.laz' % (d_type, area, grid)
        elif d_type == 'dmr1':
            url = 'http://gis.arso.gov.si/lidar/%s/%s/D96TM/TM1_%s.txt' % (d_type, area, grid)
        elif d_type == 'report':
            url = 'http://gis.arso.gov.si/related/lidar_porocila/%s_izdelava_izdelkov.pdf' % (area)
        return url
            

    def get_report(self, areas, dest_folder):
        areas = list(areas)
        for a in areas:
            url = dl_url('report', '', a)
            dest_filename = '%s\\%s_izdelava_izdelkov.pdf' % (dest_folder, a)
            response = requests.get(url, stream=True)
            if response.status_code == 200:
                with open(dest_filename, 'wb') as f:
                    for chunk in response.iter_content(chunk_size = 5000):
                        f.write(chunk)


 
    def open_folder(self):
        webbrowser.open(os.path.realpath(self.dest_folder))

    def completed(self, exception, result=None):
        if exception is None:
            if result is None:
                QgsMessageLog.logMessage(
                    'Completed with no exception and no result '\
                    '(probably manually canceled by the user)',
                    MESSAGE_CATEGORY, Qgis.Warning)
            else:
                QgsMessageLog.logMessage(
                    'Task {name} completed\n'
                    'Total {grids_downloaded} grids downloaded to: {dest_folder} ( with {grids_skipped} '
                    'grids skipped)'.format(
                        name=result['task'],
                        grids_downloaded=result['grids_downloaded'],
                        grids_skipped =result['grids_skipped'],
                        dest_folder =result['dest_folder']),
                    MESSAGE_CATEGORY, Qgis.Info)

                widget = iface.messageBar().createMessage("Grids downloaded.")
                button = QPushButton(widget)
                button.setText("Open Download Folder")
                button.pressed.connect(open_folder)
                widget.layout().addWidget(button)
                iface.messageBar().pushWidget(widget, Qgis.Info, duration=10)




        else:
            QgsMessageLog.logMessage("Exception: {}".format(exception),
                                    MESSAGE_CATEGORY, Qgis.Critical)
            raise exception



    def stopped(self, task):
        QgsMessageLog.logMessage(
            'Task "{name}" was canceled'.format(
                name=task.description()),
            MESSAGE_CATEGORY, Qgis.Info)


    """
    grids_list = self.grids_list
    d_type = self.d_type
    dest_folder = self.dest_folder
    """




dialog = DlDialog()
w = dialog.window()
w.show()
