# -*- coding: utf-8 -*-
"""
Created on Tue Sep 18 15:24:08 2018

@author: sunwy015
"""

import requests
import urllib
from bs4 import BeautifulSoup
import os

os.chdir('C:/Users/sunwy015/Desktop/predispatch_data')

target = 'http://nemweb.com.au/Reports/Archive/P5_Reports/'
page = requests.get(target)
soup = BeautifulSoup(page.text,features='lxml')
rows = soup.find_all('a')
for record in rows:
    download_link = 'http://nemweb.com.au'+record['href']
    urllib.request.urlretrieve(download_link,download_link.split('/')[-1])