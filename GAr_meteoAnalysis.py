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


#%% INPUTS
fileType='wrfout_d02'
path = '/media/leohoinaski/HDD/SC_2019'
borderShape = '/media/leohoinaski/HDD/shapefiles/Brasil.shp'
cityShape='/media/leohoinaski/HDD/shapefiles/BR_Municipios_2020.shp'

# path = '/home/lcqar/CMAQ_REPO/data/WRFout/SC/2019'
# borderShape = '/home/lcqar/shapefiles/Brasil.shp'
# cityShape='/home/lcqar/shapefiles/BR_Municipios_2020.shp'

# Trim domain
left = 40
right = 20
top=95
bottom=20

#%% List of variables and definitions
Q2 = {
  "variable": "Specific Humidity",
  "Unit": '$kg.kg^{-1}$',
  "tag":'Q2',
  'cmap':matplotlib.colors.LinearSegmentedColormap.from_list("", ["white","lightgray","royalblue","royalblue"])
}

RAIN = {
  "variable": "Precipitation",
  "Unit": 'mm',
  "tag":'RAIN',
  'cmap':matplotlib.colors.LinearSegmentedColormap.from_list("", ["white","lightblue","aqua","blue"])
}

PATM = {
  "variable": "Pressure",
  "Unit": 'Pa',
  "tag":'PATM',
  'cmap':matplotlib.colors.LinearSegmentedColormap.from_list("", ["white","moccasin","burlywood","firebrick"])
}


T = {
  "variable": "Temperature",
  "Unit": 'K',
  "tag":'T2',
  'cmap':matplotlib.colors.LinearSegmentedColormap.from_list("", ["white","lightyellow","gold","red"])
}


PBLH = {
  "variable": "Planetary Boundary Layer Height",
  "Unit": 'm',
  "tag":'PBLH',
  'cmap':matplotlib.colors.LinearSegmentedColormap.from_list("", ["white","lightgray","turquoise","navy"])
}

WIND = {
  "variable": "Wind Speed",
  "Unit": '$m.s^{-1}$',
  "tag":'WIND',
  'cmap':matplotlib.colors.LinearSegmentedColormap.from_list("", ["white","lightgray","cyan","purple"])
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
    os.mkdir(path+'/METEOfigures')

tabsfolder=path+'/METEOtables'
if os.path.isdir(path+'/METEOtables')==0:
    os.mkdir(path+'/METEOtables')

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
    
    # Trim borders left/right/bottom/top
    dataT,xlon,ylat= tst.trimBorders(data,xv,yv,left,right,top,bottom)

   # Yearly averages
    yearlyData = tst.yearlyAverage(datesTimeAll,dataT)
    dailyAverage,daily = tst.dailyAverage(datesTimeAll,dataT)
    
    
    if metVar==WIND:
        V10,xlon,ylat= tst.trimBorders(V10,xv,yv,left,right,top,bottom)
        datesTime, V10 = tst.getTimeWRF(ds,V10)
        U10,xlon,ylat= tst.trimBorders(U10,xv,yv,left,right,top,bottom)
        datesTime, U10 = tst.getTimeWRF(ds,U10)
        yearlyDataV10 = tst.yearlyAverage(datesTimeAll,V10)
        yearlyDataU10 = tst.yearlyAverage(datesTimeAll,U10)
    
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
        dailyRain = dailyAverage*24
        yearlySumData=tst.yearlySum (daily,dailyRain)
        yearlySumData
        legend = 'Annual ' + metVar['variable'] + ' ('+ metVar['Unit']+')'
        garfig.spatialEmissFig(np.sum(yearlySumData[:,:,:],axis=0),xlon,ylat,
                               legend,metVar['cmap'],borderShape,figfolder,
                               metVar['tag'],'wrfout')
    elif metVar == WIND:
        legend = 'Annual average of ' + metVar['variable'] + ' ('+ metVar['Unit']+')'
        garfig.spatialWindFig(np.sum(yearlyData[:,:,:],axis=0),
                               np.sum(yearlyDataU10[:,:,:],axis=0),
                               np.sum(yearlyDataV10[:,:,:],axis=0),
                               xlon,ylat,
                               legend,metVar['cmap'],borderShape,figfolder,
                               metVar['tag'],'wrfout')
    else :
        legend = 'Annual average of ' + metVar['variable'] + ' ('+ metVar['Unit']+')'
        garfig.spatialEmissFig(np.sum(yearlyData[:,:,:],axis=0),xlon,ylat,
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
    

    