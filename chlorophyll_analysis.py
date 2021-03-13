#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
HACK THE ARCTIC 2021  HACKATHON 
Focus on Svalbard Challenge
Analysis of Chlorophyll in the Arctic Ocean


Created on Sat Mar 13 11:24:40 2021

@author: freiste

Data source: https://cdi.seadatanet.org/search


"""

import numpy as np
import pandas as pd
import xarray as xr
import glob
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit


datapath = 'data/Chlorophyll'



def convert_time(timestamp):
    Y = timestamp.values[0].year
    M = timestamp.values[0].month
    D = timestamp.values[0].day
    h = timestamp.values[0].hour
    m = timestamp.values[0].minute
    s = timestamp.values[0].second
    return pd.to_datetime(f'{Y}-{M}-{D} {h}:{m}:{s}')



def water_depth(pres):
    P = pres*10000
    rho = 1025
    g = 9.81
    return P / (rho*g) 


def please_open(file):
    
    data = pd.read_csv(file, sep='\t', header=0, skiprows=12)
    
    data = data[['yyyy-mm-ddThh:mm:ss.sss', 'Depth [meters]', 'Chlorophyll [mg/m3]']]
    
    data = data.rename(columns = {'yyyy-mm-ddThh:mm:ss.sss' : 'datetime',
                                  'Depth [meters]'          : 'deep',
                                  'Chlorophyll [mg/m3]'     : 'chlor'})
        
    return data


#all_files = (glob.glob(f'{datapath}/*.nc'))
datapath='data/Chlorophyll'
all_files = (glob.glob(f'{datapath}/part1/*.txt'))
all_files.extend((glob.glob(f'{datapath}/part2/*.txt')))
all_files.extend((glob.glob(f'{datapath}/part3/*.txt')))

test = please_open('data/Chlorophyll/part1/000612_ODV_9566e9a7748541f0b4d941825c28d2ed_V0.txt')


def import_all():
        
    observations = []
    problems = []
    
    for file in all_files:
        print(file)
        
        data = please_open(file)
        
        try:
            time = pd.to_datetime(data.datetime[0])
            
            M050 = data.chlor[data.deep < 50].mean()
            M100 = data.chlor[(data.deep >= 50) & (data.deep <= 100)].mean()
            M000 = data.chlor[data.deep > 100].mean()
            
            observations.append([time, M050, M100, M000])
        
        except:
            print(f'{file} <-- SOME PROBLEM WITH THIS FILE')
            problems.append(file)


    return observations, problems



#observations, problems = import_all()


Chlorophyll = pd.DataFrame(observations, index=range(len(observations)), columns=['datetime', 'M050', 'M100', 'M000'])
Chlorophyll = Chlorophyll.set_index('datetime')
Chlorophyll.sort_index(inplace=True)
#Chlorophyll.to_csv('Chlorophyll_Arctic_Ocean.csv', sep=';',na_rep='NaN')

chlor_season = Chlorophyll[Chlorophyll.index.month.isin([4,5,6,7,8,9])]
chlor_y = chlor_season.resample('1Y').mean()
chlor_y = chlor_y.drop([pd.to_datetime('1990-12-31')])
chlor_y = chlor_y.drop([pd.to_datetime('1988-12-31')])


chlor_y['yr'] = chlor_y.index.year
chlor_y['yrs_since'] = range(len(chlor_y))
#chlor_y.to_csv('Yearly_High_Season_Chlorophyll_Concentration_Arctic_Ocean.csv', sep=';',na_rep='NaN')

x  = chlor_y.yrs_since
y1 = chlor_y.M050
y2 = chlor_y.M100
y3 = chlor_y.M000
# Define an exponential function to fit
def exp_decay(x, m, t, b):
    return m * np.exp(-t * x) + b


params, cv = curve_fit(exp_decay, x, y1) # gives parameters so that sum of squared residuals is minimized and the covariance matrix
m, t, b = params

plt.plot(x, y1, '.', label="data")
plt.plot(x , exp_decay(x, m, t, b), '--', label="fitted")
plt.xticks(x, chlor_y.yr.values.astype(str), rotation='vertical')
plt.title("Fitted Exponential Curve")
