# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import csv
import numpy as np
import os
from typing import Dict
from collections import defaultdict
from datetime import datetime

os.chdir('C:/Users/sunwy015/Downloads/bid_data')
print(os.listdir())
file_list = os.listdir()
# set price_bid dict
#venue - fueltype - DUID - settlement datetime - price
price_bid = Dict[str,Dict[str,Dict[str,Dict[str,list]]]]
price_bid = defaultdict(lambda: defaultdict(lambda:defaultdict(lambda: defaultdict(list))))
#set capacity_bid dict
#venue - fueltype - DUID - settlement datetime - capacity 
capacity_bid = Dict[str,Dict[str,Dict[str,Dict[str,list]]]]
capacity_bid = defaultdict(lambda: defaultdict(lambda:defaultdict(lambda: defaultdict(list)))) 
#set registered capacity dict
#registered_capacity = Dict[str,int]
#registered_capacity = defaultdict(int)
#set dict for bid VWOV
#venue - fueltype - settlement date - VWOV_list
VWOV = Dict[str,Dict[str,Dict[str,list]]]
VWOV = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: list)))
#venue - fueltype - pre / post - settlement hour - VWOV_list
VWOV_hourly = Dict[str,Dict[str,Dict[str,Dict[str,list]]]]
VWOV_hourly = defaultdict(lambda: defaultdict(lambda:defaultdict(lambda: defaultdict(list))))
#read csv and put into dict
#only keep the latest price for a given date
#only keep the latest capacity for a given half-hour interval
for file in file_list:
    if file.startswith('intraday_price'):
        with open(file) as price_file:
            reader = csv.DictReader(price_file)
            for row in reader:
                if (row['region'] == 'SA1') & (row['dispatch_type'] == 'GENERATOR'):
                    
                    price_bid[row['venue']][row['co2e_energy_source']][row['DUID']][datetime.strptime(row['settlement_datetime'],'%Y-%m-%d %H:%M:%S')]=\
                    [float(row['price_band_1']),float(row['price_band_2']),float(row['price_band_3']),
                     float(row['price_band_4']),float(row['price_band_5']),float(row['price_band_6']),
                     float(row['price_band_7']),float(row['price_band_8']),float(row['price_band_9']),
                     float(row['price_band_10'])]
    elif file.startswith('intraday_capacity'):
        with open(file) as capacity_file:
            reader = csv.DictReader(capacity_file)
            for row in reader:
                if (row['region'] == 'SA1') & (row['dispatch_type'] == 'GENERATOR'):
                    capacity_bid[row['venue']][row['co2e_energy_source']][row['DUID']][datetime.strptime(row['settlement_datetime'],'%Y-%m-%d %H:%M:%S')]= \
                    [float(row['capacity_band_1']),float(row['capacity_band_2']),float(row['capacity_band_3']),
                     float(row['capacity_band_4']),float(row['capacity_band_5']),float(row['capacity_band_6']),
                     float(row['capacity_band_7']),float(row['capacity_band_8']),float(row['capacity_band_9']),
                     float(row['capacity_band_10'])]

#calculate VOWV and put into dict
#use the keys in price_bid
#for venue in price_bid.keys():
#    for fueltype in price_bid[venue].keys():
#        for DUID in price_bid[venue][fueltype].keys():
#            for settlement_datetime_price in price_bid[venue][fueltype][DUID].keys():
#                price_list = price_bid[venue][fueltype][DUID][settlement_datetime_price]   
#                settledate = settlement_datetime_price.date()
#
#                VWOV[venue][fueltype][settledate] = []
#                for settlement_datetime_capacity in capacity_bid[venue][fueltype][DUID].keys():
#                    if settlement_datetime_capacity.date() == settledate:
#                        capacity_list = capacity_bid[venue][fueltype][DUID][settlement_datetime_capacity]
#                        VWOV[venue][fueltype][settledate].append(np.dot(price_list,capacity_list)/np.sum(capacity_list))

#get hourly average VWOV
for venue in price_bid.keys():
    for fueltype in price_bid[venue].keys():
        for DUID in price_bid[venue][fueltype].keys():
            for settlement_datetime_price in price_bid[venue][fueltype][DUID].keys():
                price_list = price_bid[venue][fueltype][DUID][settlement_datetime_price]   
                settledate = settlement_datetime_price.date()
                
                for settlement_datetime_capacity in capacity_bid[venue][fueltype][DUID].keys():
                    if (settlement_datetime_capacity.date() <= datetime(2017,11,30).date()) and settlement_datetime_capacity.date() == settledate:
                        settlehour = settlement_datetime_capacity.hour
                        capacity_list = capacity_bid[venue][fueltype][DUID][settlement_datetime_capacity]
                        VWOV_hourly[venue][fueltype]['pre'][settlehour].append(np.dot(price_list,capacity_list)/np.sum(capacity_list))
                    elif (settlement_datetime_capacity.date() > datetime(2017,11,30).date()) and settlement_datetime_capacity.date() == settledate:
                        settlehour = settlement_datetime_capacity.hour
                        capacity_list = capacity_bid[venue][fueltype][DUID][settlement_datetime_capacity]
                        VWOV_hourly[venue][fueltype]['post'][settlehour].append(np.dot(price_list,capacity_list)/np.sum(capacity_list))

with open('prepost_hourly_VWOV.csv','w',newline='') as target:
    writer = csv.writer(target)                       
    for venue in VWOV_hourly.keys():
        for fueltype in VWOV_hourly[venue].keys():
            for prepost in VWOV_hourly[venue][fueltype].keys():
                for hour in list(range(0,24)):
                    row = [venue,fueltype,prepost,hour,np.mean(VWOV_hourly[venue][fueltype][prepost][hour])]
                    writer.writerow(row)

with open('prepost_hourly_VWOV_ttest.csv','w',newline='') as target:
    writer = csv.writer(target)                       
    for venue in VWOV_hourly.keys():
        for fueltype in VWOV_hourly[venue].keys():
            for prepost in VWOV_hourly[venue][fueltype].keys():
                for hour in list(range(0,24)):
                    row = [venue,fueltype,prepost,hour,VWOV_hourly[venue][fueltype][prepost][hour]]
                    writer.writerow(row)
                     
        

##check the mean of VWOV
#for venue in VWOV.keys():
#    for fueltype in VWOV[venue].keys():
#        print(venue,fueltype)
#        locals()[venue+'_'+fueltype+'_VWOV_pre'] = []
#        locals()[venue+'_'+fueltype+'_VWOV_post'] = []
#        for date in VWOV[venue][fueltype].keys():
#            if date <= datetime(2017,11,30).date():
#                locals()[venue+'_'+fueltype+'_VWOV_pre'] += VWOV[venue][fueltype][date]
#            else:
#                locals()[venue+'_'+fueltype+'_VWOV_post'] += VWOV[venue][fueltype][date]
#        print(len(locals()[venue+'_'+fueltype+'_VWOV_pre']))
#        print(len(locals()[venue+'_'+fueltype+'_VWOV_post']))
#        print('Pre-battery',np.mean(locals()[venue+'_'+fueltype+'_VWOV_pre']))
#        print('Post-battery',np.mean(locals()[venue+'_'+fueltype+'_VWOV_post']))
                
           