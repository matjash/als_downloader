import qgis.utils
from qgis.core import (
    QgsApplication, QgsTask, QgsMessageLog)
from qgis.PyQt.QtWidgets import QPushButton
import requests
import os   
from urllib.parse import urlparse
import webbrowser


iface=qgis.utils.iface
MESSAGE_CATEGORY = 'Lidar downloader'

###varibles

#layer_id = '[%@layer_id%]'
#layer = QgsProject().instance().mapLayer(layer_id)
layer = iface.activeLayer()

dest_folder = 'd:\\'
###


features = layer.selectedFeatures()

grids_list = []
areas = set()
for f in features:
    grid = [f[2], f[22]]
    grids_list.append(grid)
    areas.add(f[22])
    
    
    
def dl_url(d_type, grid, area):
    if d_type == 'gkot':
        url = 'http://gis.arso.gov.si/lidar/%s/laz/%s/D96TM/TM_%s.laz' % (d_type, area, grid)
    elif d_type == 'otr':
        url = 'http://gis.arso.gov.si/lidar/%s/laz/%s/D96TM/TMR_%s.laz' % (d_type, area, grid)
    elif d_type == 'dmr1':
        url = 'http://gis.arso.gov.si/lidar/%s/%s/D96TM/TM1_%s.txt' % (d_type, area, grid)
    elif d_type == 'report':
        url = 'http://gis.arso.gov.si/related/lidar_porocila/%s_izdelava_izdelkov.pdf' % (area)
    return url
        

def get_report(areas, dest_folder):
    areas = list(areas)
    for a in areas:
        url = dl_url('report', '', a)
        dest_filename = '%s\\%s_izdelava_izdelkov.pdf' % (dest_folder, a)
        response = requests.get(url, stream=True)
        if response.status_code == 200:
            with open(dest_filename, 'wb') as f:
                for chunk in response.iter_content(chunk_size = 5000):
                    f.write(chunk)
 

#get_report(areas, dest_folder) 




def download_task(task, grids_list, d_type, dest_folder):
    grids_downloaded = 0
    total_size = 0
    size_downloaded = 0
    for grid in grids_list:
        url = dl_url(d_type, str(grid[0]), str(grid[1]))
        response = requests.head(url)
        if response.status_code == 200:
            size = int(requests.head(url).headers['content-length'])
        else:
            text = 'Grid %s not found!' %grid
            return Exception(text)
        total_size += size  
    total_len = len(grids_list)
    total_size = round((total_size/1000000), 2)
    QgsMessageLog.logMessage('Selected %s grids, %s MB' %(str(total_len), str(total_size)),
                             MESSAGE_CATEGORY, Qgis.Info)




    for grid in grids_list:
        url = dl_url(d_type, str(grid[0]), str(grid[1])) 
        response = requests.get(url, stream=True)
        file_name = urlparse(url)
        file_name = file_name.path.rsplit("/", 1)[-1]
        dest_filename = dest_folder + '\\' + file_name
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
                MESSAGE_CATEGORY, Qgis.Warning)
        
    grids_skipped = total_len - grids_downloaded

    return {'grids_downloaded': grids_downloaded, 'grids_skipped': grids_skipped , 'dest_folder':dest_folder,
            'task': task.description()}
 
def open_folder():
    webbrowser.open(os.path.realpath(dest_folder))

def completed(exception, result=None):
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



def stopped(task):
    QgsMessageLog.logMessage(
        'Task "{name}" was canceled'.format(
            name=task.description()),
        MESSAGE_CATEGORY, Qgis.Info)




task = QgsTask.fromFunction('Downloading grids', download_task,
                             on_finished=completed, grids_list=grids_list, d_type='gkot', dest_folder=dest_folder)
QgsApplication.taskManager().addTask(task)






#iface.messageBar().pushMessage("Ime sloja.", grid[0])    
    
    

   
   
                            
"""

layer_name = layer.name()
iface.messageBar().pushMessage("Ime sloja.", layer_name, level=Qgis.Critical)
"""