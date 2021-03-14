#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
HACK THE ARCTIC 2021  HACKATHON 
Focus on Svalbard - Challenge
Analysis of Chlorophyll in the Arctic Ocean


Created on Sat Mar 13 22:57:14 2021

@author: Nadine-Cyra Freistetter

Data source: modified from https://cdi.seadatanet.org/search
with chlorophyll_analysis_data_preprocessing.py

"""

import numpy as np
import pandas as pd
import xarray as xr
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit


def please_open(file):   
    data = pd.read_csv(file, sep=';', header=0, index_col=0)
    
    data.index = pd.to_datetime(data.index)
    
    # Extract some time information for easier fitting/plotting
    data['yr'] = data.index.year
    data['yrs_cnt'] = range(len(data))
    
    return data


# Define an exponential function to fit
def exp_decay(x, m, t, b):
    return m * np.exp(-t * x) + b


def fit_n_plot(times, chlor, dpi=300, text=''):
    y = chlor[chlor == chlor]
    x = times[chlor == chlor]
        
    params, cv = curve_fit(exp_decay, x, y) # gives parameters so that sum of squared residuals is minimized and the covariance matrix
    m, t, b = params
    print(f'Model({chlor.name}): y = {m:.5f} * e^(-{t:.5f} * x) + {b:.5f}')
    
    plt.figure(dpi=dpi)
    plt.plot(x, y, '.', label="data")
    plt.plot(x , exp_decay(x, m, t, b), '--', label="fitted")
        
    plt.title(f"Development of Chlorophyll Concentration in the Arctic Ocean \n {text}")
    plt.legend(loc='center right')
    plt.text(x.median(), y.max(), f'y = {m:.2f} * e^(-{t:.2f} * x) + {b:.2f}')
    
    plt.xticks(x, y.index.year.values.astype(str), rotation='vertical')
    plt.xlabel('Years')
    plt.ylabel('Concentration [mg/m^3]')
        
    plt.show()




#Import
datapath = 'data/Chlorophyll'   # CHANGE!
chlor_y = please_open(f'{datapath}/chlorophyll_concentration_arctic_ocean_yearly_bloom_season_means.csv')

chlor_y = chlor_y.drop([pd.to_datetime('1990-12-31')]) # too few observations in this year
chlor_y = chlor_y.drop([pd.to_datetime('1988-12-31')]) # too few observations in this year



fit_n_plot(chlor_y.yrs_cnt, chlor_y.M050, text='for Sea Depth 0-49m')
fit_n_plot(chlor_y.yrs_cnt, chlor_y.M100, text='for Sea Depth 50-100m')
fit_n_plot(chlor_y.yrs_cnt, chlor_y.M000, text='for Sea Depth 100-1000m')












