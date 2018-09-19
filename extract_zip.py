# -*- coding: utf-8 -*-
"""
Created on Tue Sep 18 16:04:11 2018

@author: sunwy015
"""

import zipfile
import csv
import os
import io

#os.chdir('C:/Users/sunwy015/Desktop/predispatch_data')
#parent_path = 'C:/Users/sunwy015/Desktop/predispatch_data'
unzip_path = 'C:/Users/sunwy015/Desktop/predispatch_data/unzipped'
#region_list = ['NSW1','VIC1','QLD1','SA1','TAS1']

#parent_file_list = os.listdir()
#for file in parent_file_list:
#    if file.endswith('zip'):
#        zf = zipfile.ZipFile(file)
#        zf.extractall(path=unzip_path)
#
os.chdir(unzip_path)
#file_list = os.listdir()
#for file in file_list:
#    if file.endswith('zip'):
#        zf1 = zipfile.ZipFile(file)
#        zf1.extractall(path=unzip_path)

file_list = os.listdir()
for file in file_list:
    if file.endswith('zip'):
        try:
            zf = zipfile.ZipFile(file)
            zf.extractall(path='C:/Users/sunwy015/Desktop/predispatch_data/csvfiles')
        except:
            print('FAILED '+file)


                    