# -*- coding: utf-8 -*-
"""
Created on Mon Aug  8 13:34:25 2022

@author: Nadine
"""

# NAA Data
import requests
# import zipfile
import gzip
import shutil
# url = 'http://psddb.nerc-bas.ac.uk/data/access/download.php?searchterm=ny-alesund&cat=item&%0Byear=2009&class=232&type=ULTRA&site=Ny-Alesund&v=Data&page=1&year=2009'
# r = requests.get(url)
# r = requests.get(url, allow_redirects=True)
# open('d.ico', 'wb').write(r.content)

# output_directory = 'C:\Users\Nadine\Documents\Universitaet\Master\ISWC\0_Praxis\data'
# file_path = os.path.join(output_directory, 'asdsad906010.csv')
receiver = 'NAA'
url = 'http://psddb.nerc-bas.ac.uk/data/psddata/atmos/space/vlf/ultra/nyalesund//' #2009/data/ #NAA20090101.txt.gz
import datetime
# for i in range(365):
for year in ['2015']:#['2008','2009']
    for month in range(1,13): #(1,13)
        for day in range(1,32): #(1,32)
            # 
            url_download = url+str(year)+'/data/'+receiver+str(year)+'{:0>2}'.format(month)+'{:0>2}'.format(day)+'.txt.gz'
            print(url_download)
            # download as binary into variable r
            r = requests.get(url_download)
            if not r.ok:
                continue
            # write r to zip file named "File.txt.gz"
            with open("data/File.txt.gz",'wb') as f:
                f.write(r.content)
            
            # name of unziped txt-file
            filename_unzipped = 'data/'+receiver+str(year)+'{:0>2}'.format(month)+'{:0>2}'.format(day)+'.txt'
            # unzip zip file and save as txt
            with gzip.open('data/File.txt.gz', 'rb') as f_in:
                with open(filename_unzipped, 'wb') as f_out:
                    shutil.copyfileobj(f_in, f_out)
                    
                    
                    
                    
                    
                    
                    

