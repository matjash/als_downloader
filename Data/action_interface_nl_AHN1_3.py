import sys
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import qgis.utils
import requests
from urllib.parse import urlparse
import webbrowser
import shutil
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
        layer_id = '[% @layer_id %]'
        layer = QgsProject().instance().mapLayer(layer_id)
        #layer = self.iface.activeLayer()
    
        self.features = layer.selectedFeatures()
        if len(self.features) == 0:
            feature = [% $id %]
            layer.select(feature)
            self.features = layer.selectedFeatures()
        
        self.grids_list = []
        for f in self.features:
            grid = f
            self.grids_list.append(grid)    
        self.task = QgsTask.fromFunction('Downloading grids', self.download_task, on_finished=self.completed)
        
    
        
    def window(self):       
        self.f.setDialogTitle('Select Download Folder')
        self.f.setStorageMode(1)
        self.layouth.addWidget(self.f)
        self.layouth.addLayout( self.layout )

        #AHN3
        self.rb1 = QRadioButton('Download AHN3_05m_DSM')
        self.rb1.data_column = 14
        self.rb1.setChecked(True)
        self.layout.addWidget(self.rb1, 0, 0)
        
        self.rb2 = QRadioButton('Download AHN3_05m_DTM')
        self.rb2.data_column = 15
        self.layout.addWidget(self.rb2, 1, 0)
        
        self.rb3 = QRadioButton('Download AHN3_5m_DSM')
        self.rb3.data_column = 16
        self.layout.addWidget(self.rb3, 2, 0)

        self.rb4 = QRadioButton('Download AHN3_5m_DTM')
        self.rb4.data_column = 17
        self.layout.addWidget(self.rb4, 3, 0)

        self.rb5 = QRadioButton('Download AHN3_LAZ')
        self.rb5.data_column = 18
        self.layout.addWidget(self.rb5, 4, 0)

        bt2 = QPushButton()
        self.layouth.addWidget(bt2)
        bt2.setText("Download")
     
        source = QLabel()
        self.layouth.addWidget(source)
        source.setText("<a href='https://www.ahn.nl/'>More Info on data</a>")
        source.setAlignment(Qt.AlignCenter)
        source.setOpenExternalLinks(True)
        
        bt2.clicked.connect(self.on_click)
        self.w.setWindowTitle("Select download folder and data")
        return self.w
       
    def on_click(self):
        self.dest_folder = self.f.filePath()
        rbs = (self.rb1, self.rb2, self.rb3, self.rb4, self.rb5)
        for rb in rbs:
            if rb.isChecked():
                self.data_column = rb.data_column

        self.grids_downloaded = 0
        self.total_size = 0
        self.size_downloaded = 0
        self.url_list = []
        self.total_len = len(self.grids_list)
        progressMessageBar = self.iface.messageBar().createMessage('Calculating download size...')
        progress = QProgressBar()
        progress.setMaximum(self.total_len)
        progress.setAlignment(Qt.AlignLeft|Qt.AlignVCenter)
        progressMessageBar.layout().addWidget(progress)
        self.iface.messageBar().pushWidget(progressMessageBar, Qgis.Info)
        progress.setValue(0)
        self.window().close()
        for cur, f in enumerate(self.grids_list):
            url = f[self.data_column]
            response = requests.head(url)
            if response.status_code == 200:
                size = int(requests.head(url).headers['content-length'])
                self.url_list.append(url)
            else:
                text = 'Grid %s not found!' %f[1]
                return Exception(text)
            self.total_size += size  
            progress.setValue((cur-1) + 1)
        self.iface.messageBar().clearWidgets()   
        self.showdialog()

    def format_bytes(self, size):
        power = 2**10
        n = 0
        power_labels = {0 : 'B', 1: 'KB', 2: 'MB', 3: 'GB', 4: 'TB'}
        while size > power:
            size /= power
            n += 1
        size = str(round(size,2)) + ' ' + power_labels[n]
        return size       

    def showdialog(self):
        msg = QMessageBox() 
        if self.dest_folder == '':
            msg.setIcon(QMessageBox.Warning)
            msg.setText('No download folder selected!')
            retval = msg.exec_()
        else:
            total, used, free = shutil.disk_usage(str(self.dest_folder))
            d_size = self.format_bytes(self.total_size)
            free_size = self.format_bytes(free)
            
            if free < self.total_size:
                msg.setIcon(QMessageBox.Warning)
                msg.setText("Not enough space")
                msg.setInformativeText('''Selected %s grids, %s. 
                Free space: %s
                Selected destination folder:
                %s
                ''' %(self.total_len, d_size, free_size, self.dest_folder))   
                retval = msg.exec_()
            else:
                msg.setIcon(QMessageBox.Information)
                msg.setText('Selected %s grids, %s' %(self.total_len,d_size))       
                msg.setInformativeText('Downloading to:\n %s' %(self.dest_folder))         
                msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
                msg.buttonClicked.connect(self.msgbtn)
                retval = msg.exec_()
  

    def download_task(self, task):
        d_size = self.format_bytes(self.total_size)
        size_mb = round(self.total_size/(1024*1024), 2)
        QgsMessageLog.logMessage('Selected %s grids, %s' %(str(self.total_len), d_size),
                               self.MESSAGE_CATEGORY, Qgis.Info)

     
        for url in self.url_list:
            response = requests.get(url, stream=True)
            file_name = urlparse(url)
            file_name = file_name.path.rsplit("/", 1)[-1]
            dest_filename = self.dest_folder + '\\' + file_name
            if response.status_code == 200:
                with open(dest_filename, 'wb') as f:
                    a = 0
                    for chunk in response.iter_content(chunk_size = 1024*1024):
                        f.write(chunk)
                        diff= os.path.getsize(dest_filename)-a
                        a = os.path.getsize(dest_filename)
                        self.size_downloaded += diff/(1024*1024)
                        progressm = round(((100*self.size_downloaded)/size_mb),0)
                        task.setProgress(progressm)
                        if task.isCanceled():
                            self.stopped(task)
                            return None
                self.grids_downloaded += 1
            else:
                QgsMessageLog.logMessage('Url for grid %s not valid, skipping.' % file_name,
                    self.MESSAGE_CATEGORY, Qgis.Warning)
            
        grids_skipped = self.total_len - self.grids_downloaded

        return {'grids_downloaded': self.grids_downloaded, 'grids_skipped': grids_skipped , 'dest_folder':self.dest_folder,
                'task': task.description()}

    

    def msgbtn(self,i):
        if i.text() == 'OK':     
            QgsApplication.taskManager().addTask(self.task)
        elif i.text() == 'Cancel':
            print(i.text())
   
    def open_folder(self):
        webbrowser.open(os.path.realpath(self.dest_folder))

    def completed(self, exception, result=None):
        if exception is None:
            if result is None:
                QgsMessageLog.logMessage(
                    'Completed with no exception and no result \n(probably manually canceled by the user)',
                    self.MESSAGE_CATEGORY, Qgis.Warning)
            else:         
                QgsMessageLog.logMessage(
                    'Download complete', self.MESSAGE_CATEGORY, Qgis.Info)
                widget = self.iface.messageBar().createMessage("Download finished", '' )
                button = QPushButton(widget)
                button.setText("Open download folder")
                button.pressed.connect(self.open_folder)
                widget.layout().addWidget(button)
                self.iface.messageBar().pushWidget(widget, Qgis.Info)
        else:
            QgsMessageLog.logMessage("Exception: %s" %exception,
                                    self.MESSAGE_CATEGORY, Qgis.Critical)
            raise exception
       


    def stopped(self, task):
        QgsMessageLog.logMessage(
            'Task "{name}" was canceled'.format(
                name=task.description()),
            self.MESSAGE_CATEGORY, Qgis.Info)



dialog = DlDialog()
w = dialog.window()
w.show()
