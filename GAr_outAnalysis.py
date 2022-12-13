#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec  7 09:30:01 2022

@author: leohoinaski
"""

import os
import numpy as np
import matplotlib.pyplot as plt
import geopandas as gpd
from datetime import datetime
import netCDF4 as nc
import pandas as pd
import temporalStatistics

path = '/media/leohoinaski/HDD/SC_2019'

fileType='CCTM_CONC'

pollutants = ['O3', 'CO', 'SO2', 'NO2']

#%%
NO2 = {
  "Pollutant": "Nitrogen dioxide ($NO_{2}$)",
  "Criteria": 0.097414,
  "Unit": 'ppm',
  "Criteria_annual": 0.021266,
  "Criteria_average": '1-h average',
}

CO = {
  "Pollutant": "Carbon monoxide (CO)",
  "Criteria": 9,
  "Unit": 'ppm',
  "Criteria_average": '8-h moving average',
}

O3 = {
  "Pollutant": "Ozone ($O_{3}$)",
  "Criteria":0.050961,
  "Unit": 'ppm',
  "Criteria_average": '8-h moving average',
}

SO2 = {
  "Pollutant": "Sulphur dioxide ($SO_{2}$)",
  "Criteria": 0.007636,
  "Unit": 'ppm',
  "Criteria_annual": 0.007636,
  "Criteria_average": '24-h average',
}

PM10 = {
  "Pollutant": "Particulate Matter ($PM_{10}$)",
  "Criteria": 50,
  "Unit": '$\u03BCg m_{3}$',
  "Criteria_annual": 20,
  "Criteria_average": '24-h average',
}

PM25 = {
  "Pollutant": "Particulate Matter ($PM_{2.5}$)",
  "Criteria": 25,
  "Unit": '$\u03BCg m_{3}$',
  "Criteria_annual": 10,
  "Criteria_average": '24-h average',
}

#%% Opening data 

# Moving to dir
os.chdir(path)

# Selecting files and variables
prefixed = sorted([filename for filename in os.listdir(path) if filename.startswith(fileType)])

ds = nc.MFDataset(prefixed)
dsMet = nc.Dataset('GRIDCRO2D_SC_2019.nc')

data = ds['O3'][:]

datesTime = temporalStatistics.datePrepCMAQ(ds)

idx2Remove = np.array(datesTime.drop_duplicates().index)

data = data[idx2Remove]

datesTime = datesTime.drop_duplicates().reset_index(drop=True)

dailyData = temporalStatistics.dailyAverage(datesTime,data)

monthlyData = temporalStatistics.monthlyAverage(datesTime,data)

mvAveData = temporalStatistics.movingAverage(datesTime,data,8)

xv,yv,lon,lat = temporalStatistics.ioapiCoords(ds)

xlon, ylat = temporalStatistics.eqmerc2latlon(ds,xv,yv)

freqExcd= temporalStatistics.exceedance(mvAveData,0.07)


