#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
HACK THE ARCTIC 2021  HACKATHON 
Focus on Svalbard - Challenge
Data Preparation for Analysis of Chlorophyll in the Arctic Ocean


Created on Sat Mar 13 11:24:40 2021

@author: Nadine-Cyra Freistetter

Data source: https://cdi.seadatanet.org/search


"""

import numpy as np
import pandas as pd
import xarray as xr
import glob



def convert_time(timestamp):      # depends on data sorce if you need this or not
    Y = timestamp.values[0].year
    M = timestamp.values[0].month
    D = timestamp.values[0].day
    h = timestamp.values[0].hour
    m = timestamp.values[0].minute
    s = timestamp.values[0].second
    return pd.to_datetime(f'{Y}-{M}-{D} {h}:{m}:{s}')



def please_open(file):
    
    data = pd.read_csv(file, sep='\t', header=0, skiprows=12)
    
    data = data[['yyyy-mm-ddThh:mm:ss.sss', 'Depth [meters]', 'Chlorophyll [mg/m3]']]
    
    data = data.rename(columns = {'yyyy-mm-ddThh:mm:ss.sss' : 'datetime',
                                  'Depth [meters]'          : 'deep',
                                  'Chlorophyll [mg/m3]'     : 'chlor'})
        
    return data




def import_all():
        
    observations = []
    problems = []
    
    for file in all_files:
        print(file)
        
        data = please_open(file)
        
        try:
            time = pd.to_datetime(data.datetime[0])
            
            M050 = data.chlor[data.deep < 50].mean()   # sea depth 0-49m
            M100 = data.chlor[(data.deep >= 50) & (data.deep <= 100)].mean() # sea depth 50-100m
            M000 = data.chlor[data.deep > 100].mean()  # sea depth lower than 100m
            
            observations.append([time, M050, M100, M000])
        
        except:
            print(f'{file} <-- SOME PROBLEM WITH THIS FILE')
            problems.append(file)


    return observations, problems


# Define data paths
datapath='data/Chlorophyll'  # CHANGE!!
all_files = (glob.glob(f'{datapath}/part1/*.txt'))
all_files.extend((glob.glob(f'{datapath}/part2/*.txt')))
all_files.extend((glob.glob(f'{datapath}/part3/*.txt')))


# Import
observations, problems = import_all()



# Make a DataFrame
Chlorophyll = pd.DataFrame(observations, index=range(len(observations)), columns=['datetime', 'M050', 'M100', 'M000'])
Chlorophyll = Chlorophyll.set_index('datetime')
Chlorophyll.sort_index(inplace=True)

# Extract bloom season and calculate means
chlor_season = Chlorophyll[Chlorophyll.index.month.isin([4,5,6,7,8,9])]
chlor_y = chlor_season.resample('1Y').mean()



# Export
Chlorophyll.to_csv('Chlorophyll_Arctic_Ocean.csv', sep=';',na_rep='NaN')
chlor_y.to_csv('Yearly_High_Season_Chlorophyll_Concentration_Arctic_Ocean.csv', sep=';',na_rep='NaN')















