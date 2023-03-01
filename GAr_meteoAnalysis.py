#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb  9 17:30:15 2023

@author: leohoinaski
"""


import os
import numpy as np
import geopandas as gpd
#from datetime import datetime
import netCDF4 as nc
#import pandas as pd
import temporalStatistics as tst
import GAr_figs as garfig
import matplotlib
#import wrf
import shutil

#%% INPUTS
fileType='wrfout_d02'
path = '/media/leohoinaski/HDD/SC_2019'
borderShape = '/media/leohoinaski/HDD/shapefiles/Brasil.shp'
cityShape='/media/leohoinaski/HDD/shapefiles/BR_Municipios_2020.shp'

path = '/home/lcqar/CMAQ_REPO/data/WRFout/SC/2019'
borderShape = '/home/lcqar/shapefiles/Brasil.shp'
cityShape='/home/lcqar/shapefiles/BR_Municipios_2020.shp'

# path = '/media/leohoinaski/Backup/SC_2019'
# borderShape = '/media/leohoinaski/Backup/shapefiles/Brasil.shp'
# cityShape='/media/leohoinaski/Backup/shapefiles/BR_Municipios_2020.shp'



# Trim domain
left = 40
right = 20
top=95
bottom=20

year=2019

#%% List of variables and definitions
Q2 = {
  "variable": "Specific Humidity",
  "Unit": '$kg.kg^{-1}$',
  "tag":'Q2',
  'cmap':matplotlib.colors.LinearSegmentedColormap.from_list("", ["lightgray","royalblue","royalblue"])
}

RAIN = {
  "variable": "Precipitation",
  "Unit": 'mm',
  "tag":'RAIN',
  'cmap':matplotlib.colors.LinearSegmentedColormap.from_list("", ["lightblue","aqua","blue"])
}

PATM = {
  "variable": "Pressure",
  "Unit": 'Pa',
  "tag":'PATM',
  'cmap':matplotlib.colors.LinearSegmentedColormap.from_list("", ["moccasin","burlywood","firebrick"])
}


T = {
  "variable": "Temperature",
  "Unit": 'K',
  "tag":'T2',
  'cmap':matplotlib.colors.LinearSegmentedColormap.from_list("", ["lightyellow","gold","red"])
}


PBLH = {
  "variable": "Planetary Boundary Layer Height",
  "Unit": 'm',
  "tag":'PBLH',
  'cmap':matplotlib.colors.LinearSegmentedColormap.from_list("", ["lightgray","turquoise","navy"])
}

WIND = {
  "variable": "Wind Speed",
  "Unit": '$m.s^{-1}$',
  "tag":'WIND',
  'cmap':matplotlib.colors.LinearSegmentedColormap.from_list("", ["lightgray","cyan","purple"])
}
metVars = [Q2,T,PATM,RAIN,PBLH,WIND]
#metVars = [PATM]
#%% --------------------------PROCESSING---------------------------------------

print('--------------Start GAr_meteoAnalysis.py------------')
# Moving to dir
os.chdir(path)

# Creating outputfolders
print('Creating folders')
figfolder=path+'/METEOfigures'
if os.path.isdir(path+'/METEOfigures')==0:
    os.mkdir(figfolder)
else:
    shutil.rmtree(figfolder)
    os.mkdir(figfolder)

tabsfolder=path+'/METEOtables'
if os.path.isdir(path+'/METEOtables')==0:
    os.mkdir(tabsfolder)
else:
    shutil.rmtree(tabsfolder)
    os.mkdir(tabsfolder)

print('Openning netCDF files')
# Selecting files and variables
prefixed = sorted([filename for filename in os.listdir(path) if filename.startswith(fileType)])

# Opening netCDF files
ds = nc.MFDataset(prefixed)

print('Looping for each variable')
# Looping each var
for metVar in metVars:
    print(metVar)
    # Get coordinates 
    xv = ds['XLONG'][0,:,:]
    yv = ds['XLAT'][0,:,:]
    
    # Condition for each variable
    if metVar==RAIN:
        print('Rain data')
        data = ds['RAINC'][:]+ds['RAINSH'][:]+ds['RAINNC'][:]
        
    elif metVar==PATM:
        print('Pressure data')
        data = ds['P'][:,0,:,:]+ds['PB'][:,0,:,:]
        
    elif metVar==WIND:
        print('Wind data')
        U10 = ds['U10'][:] 
        V10= ds['V10'][:]
        data =  (U10**2 + V10**2)**(1/2)

    else:
        print('Other data')
        data = ds[metVar['tag']][:]
    
    # Get datesTime and removing duplicates
    datesTime, data = tst.getTimeWRF(ds,data)
    datesTimeAll = datesTime.copy()
    datesTime = datesTime[datesTime.year==year].reset_index(drop=True)
    
    if len(data.shape)>3:
        data=data[datesTimeAll.year==year,:,:,:]
    else:
        data=data[datesTimeAll.year==year,:,:]
    
    # Trim borders left/right/bottom/top
    dataT,xlon,ylat= tst.trimBorders(data,xv,yv,left,right,top,bottom)

   # Yearly averages
    yearlyData = tst.yearlyAverage(datesTime,dataT)
    dailyAverage,daily = tst.dailyAverage(datesTime,dataT)
    
    
    if metVar==WIND:
        V10,xlon,ylat= tst.trimBorders(V10,xv,yv,left,right,top,bottom)
        dd, V10 = tst.getTimeWRF(ds,V10)
        U10,xlon,ylat= tst.trimBorders(U10,xv,yv,left,right,top,bottom)
        dd, U10 = tst.getTimeWRF(ds,U10)
        yearlyDataV10 = tst.yearlyAverage(datesTime,V10)
        yearlyDataU10 = tst.yearlyAverage(datesTime,U10)
    
    print('Analyzing by city')
    cities = gpd.read_file(cityShape)
    cities.crs = "EPSG:4326"
    cities = cities[cities['SIGLA_UF']=='SC']
    s,cityMat = tst.citiesINdomain(xlon, ylat, cities)
    matDataAll=dataT.copy()
    matDataAll[:,np.isnan(cityMat)]=0
    idxMax = np.unravel_index(np.sum(np.sum(matDataAll[:,:,:],axis=0),axis=0).argmax(),
                  np.mean(matDataAll[:,:,:],axis=0).shape)
    
    # ============================= Figures ===================================

    if metVar == RAIN:
        dailyRain,daily=tst.dailyRainWRF(datesTime,dataT)
        #dailyRain = dailyAverage.copy()
        yearlySumData=tst.yearlySum (daily,dailyRain)
        #yearlySumData
        legend = 'Annual ' + metVar['variable'] + ' ('+ metVar['Unit']+')'
        garfig.spatialMeteoFig(yearlySumData[0,:,:],xlon,ylat,
                               legend,metVar['cmap'],borderShape,figfolder,
                               metVar['tag'],'wrfout')
    elif metVar == WIND:
        legend = 'Annual average of ' + metVar['variable'] + ' ('+ metVar['Unit']+')'
        garfig.spatialWindFig(yearlyData[0,:,:],
                               yearlyDataU10[0,:,:],
                               yearlyDataV10[0,:,:],
                               xlon,ylat,
                               legend,metVar['cmap'],borderShape,figfolder,
                               metVar['tag'],'wrfout')
    else :
        legend = 'Annual average of ' + metVar['variable'] + ' ('+ metVar['Unit']+')'
        garfig.spatialMeteoFig(yearlyData[0,:,:],xlon,ylat,
                               legend,metVar['cmap'],borderShape,figfolder,
                               metVar['tag'],'wrfout')
    
    idxMax = np.unravel_index(np.mean(matDataAll[:,:,:],axis=0).argmax(),
                  np.mean(matDataAll[:,:,:],axis=0).shape)
    
    print('Critical city - highest average')
    IBGE_CODEcritical=int(cityMat[idxMax])
    cityData,cityDataPoints,cityDataFrame,matData= tst.dataINcity(
        dataT,datesTime,cityMat,s,IBGE_CODEcritical)
    legend = metVar['variable'] + ' ('+ metVar['Unit']+')'
    garfig.cityTimeSeriesMeteo(cityDataFrame,matData,cities,IBGE_CODEcritical,metVar['cmap'],legend,
                       xlon,ylat,None,
                       figfolder,metVar['tag'],
                       '_wrfout'+'_'+str(IBGE_CODEcritical))
    

    
