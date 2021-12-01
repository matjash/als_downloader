class downloader():



    def get_lenght(grid_url):
        response = requests.head(url)
        if response.status_code == 200:
            size = int(requests.head(url).headers['content-length'])
            return size

    def get_grid(grid_name, url, dest_folder, transffered, total):
        dest_filename = dest_folder + '\\' + grid_name
        response = requests.get(url, stream=True)
        if response.status_code == 200:
            with open(dest_filename, 'wb') as f:
                feedback.pushDebugInfo(self.tr('Downloading: %s ' % dest_filename))
                for chunk in response.iter_content(chunk_size = 1024):
                    f.write(chunk)
                    transffered = transffered + 1
                    feedback.setProgress(transffered * total)



    
  
zls_list = processing.run("native:dropgeometries", {
        'INPUT': parameters['zls_listi'],
        'OUTPUT': 'memory:'
    }, context=context)['OUTPUT']

total_size = 0
areas = [11, 12, 13, 14, 15, 16, 21, 22, 23, 24, 25, 26, 31, 32, 33, 34, 35, 36, 37]
transffered = 0
def get_lenght(areas, grid):




for a in zls_list.getFeatures():
    total_size = total_size + get_lenght(areas, a[field_list])

total_chunks = total_size/1024
total = 100/total_chunks
size_mb = total_size/1024/1024
feedback.pushDebugInfo(self.tr('Prenašam %s listov (%s Mb)' % (zls_list.featureCount(), round(size_mb,2))))


for a in zls_list.getFeatures():
    get_grid(areas, a[field_list], parameters['laz_out'], transffered, total)
    feedback.pushDebugInfo(str(a[field_list]))



grid_list = parameters['grids']