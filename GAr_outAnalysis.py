#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec  7 09:30:01 2022

@author: leohoinaski
"""

import os
import numpy as np
#import matplotlib.pyplot as plt
import geopandas as gpd
#from datetime import datetime
import netCDF4 as nc
import pandas as pd
import temporalStatistics as tst
import GAr_figs as garfig
import matplotlib
import shutil

#%% INPUTS
path = '/media/leohoinaski/HDD/SC_2019'
borderShape = '/media/leohoinaski/HDD/shapefiles/Brasil.shp'
cityShape='/media/leohoinaski/HDD/shapefiles/BR_Municipios_2020.shp'
fileType='CCTM_CONC'

path = '/home/artaxo/CMAQ_REPO/data/output_CCTM_v532_gcc_SC_2019'
borderShape = '/home/artaxo/shapefiles/Brasil.shp'
cityShape='/home/artaxo/shapefiles/BR_Municipios_2020.shp'

# path = '/media/leohoinaski/HDD/BR_2019'
# borderShape = '/media/leohoinaski/HDD/shapefiles/SouthAmerica.shp'
# cityShape='/media/leohoinaski/HDD/shapefiles/AmazoniaConcervationUnits.shp'
# fileType='CCTM_CONC'


# Trim domain
left = 40
right = 20
top=95
bottom=20

# left = 0
# right = 0
# top=0
# bottom=0


#%%
NO2 = {
  "Pollutant": "$NO_{2}$",
  "Criteria": 0.097414,
  "Unit": 'ppm',
  "Criteria_annual": 0.021266,
  "Criteria_average": '1-h average',
  "tag":'NO2',
  "Criteria_ave": 1,
}

CO = {
  "Pollutant": "CO",
  "Criteria": 9,
  "Unit": 'ppm',
  "Criteria_average": '8-h moving average',
  "tag":'CO',
  "Criteria_ave": 8,
}

O3 = {
  "Pollutant": "$O_{3}$",
  "Criteria":0.050961,
  "Unit": 'ppm',
  "Criteria_average": '8-h moving average',
  "Criteria_ave": 8,
  "tag":'O3'
}

SO2 = {
  "Pollutant": "$SO_{2}$",
  "Criteria": 0.007636,
  "Unit": 'ppm',
  "Criteria_annual": 0.007636,
  "Criteria_average": '24-h average',
  "Criteria_ave": 24,
  "tag":'SO2'
}

PM10 = {
  "Pollutant": "$PM_{10}$",
  "Criteria": 50,
  "Unit": '$\u03BCg.m^{-3}$',
  "Criteria_annual": 20,
  "Criteria_average": '24-h average',
  "tag":'PM10',
  "Criteria_ave": 24,
}

PM25 = {
  "Pollutant": "$PM_{2.5}$",
  "Criteria": 25,
  "Unit": '$\u03BCg.m^{-3}$',
  "Criteria_annual": 10,
  "Criteria_average": '24-h average',
  "tag":'PM25',
  "Criteria_ave": 24,
}

pollutants = [NO2,O3,SO2,CO,PM10,PM25]
#%% Opening data 
print('--------------Start GAr_outAnalysis.py------------')

# Moving to dir
os.chdir(path)
print('Creating folders')

figfolder=path+'/CMAQfigures'
if os.path.isdir(figfolder)==0:
    os.mkdir(figfolder)
else:
    shutil.rmtree(figfolder)
    os.mkdir(figfolder)

tabsfolder=path+'/CMAQtables'
if os.path.isdir(tabsfolder)==0:
    os.mkdir(tabsfolder)
else:
    shutil.rmtree(tabsfolder)
    os.mkdir(tabsfolder)

# Selecting files and variables
prefixed = sorted([filename for filename in os.listdir(path) if filename.startswith(fileType)])

print('Openning netCDF files')
# Opening netCDF files
ds = nc.MFDataset(prefixed)

print('Looping for each variable')
for pol in pollutants:
    print(pol)
    # Selecting variable
    if pol==PM10:
        ATOTI = ds['ASO4I'][:]+ ds['ANO3I'][:]+ ds['ANH4I'][:]+ \
            ds['ANAI'][:]+ ds['ACLI'][:]+ ds['AECI'][:]+ \
                ds['AOTHRI'][:]
                
        ATOTJ = ds['ASO4J'][:]+ ds['ANO3J'][:]+ ds['ANH4J'][:]+ \
            ds['ANAJ'][:]+ ds['ACLJ'][:]+ ds['AECJ'][:]+ \
                ds['AOTHRJ'][:] + ds['AFEJ'][:]+ \
                    ds['ASIJ'][:]+ ds['ATIJ'][:] + ds['ACAJ'][:]+ \
                        ds['AMGJ'][:]+ ds['AMNJ'][:] + ds['AALJ'][:]+ \
                            ds['AKJ'][:]

        ATOTK = ds['ASOIL'][:]+ ds['ACORS'][:]+ ds['ASEACAT'][:]+ \
            ds['ACLK'][:]+ ds['ASO4K'][:]+ ds['ANO3K'][:]+ \
                ds['ANH4K'][:]
        #REVISAR ISTO
        data=ATOTI*1+ATOTJ*1+ATOTK*0.5
        
    elif pol==PM25:
        ATOTI = ds['ASO4I'][:]+ ds['ANO3I'][:]+ ds['ANH4I'][:]+ \
            ds['ANAI'][:]+ ds['ACLI'][:]+ ds['AECI'][:]+ \
                ds['AOTHRI'][:]
                
        ATOTJ = ds['ASO4J'][:]+ ds['ANO3J'][:]+ ds['ANH4J'][:]+ \
            ds['ANAJ'][:]+ ds['ACLJ'][:]+ ds['AECJ'][:]+ \
                ds['AOTHRJ'][:] + ds['AFEJ'][:]+ \
                    ds['ASIJ'][:]+ ds['ATIJ'][:] + ds['ACAJ'][:]+ \
                        ds['AMGJ'][:]+ ds['AMNJ'][:] + ds['AALJ'][:]+ \
                            ds['AKJ'][:]

        ATOTK = ds['ASOIL'][:]+ ds['ACORS'][:]+ ds['ASEACAT'][:]+ \
            ds['ACLK'][:]+ ds['ASO4K'][:]+ ds['ANO3K'][:]+ \
                ds['ANH4K'][:]
         #REVISAR ISTO   
        data=ATOTI*1+ATOTJ*1+ATOTK*0.1
        
    
    else:
        data = ds[pol['tag']][:]
    
    # Get datesTime and removing duplicates
    datesTime, data = tst.getTime(ds,data)
    datesTimeAll = datesTime.copy()
    
    # Get coordinates from ioapi 
    xv,yv,lon,lat = tst.ioapiCoords(ds)
    
    # Trim borders left/right/bottom/top
    dataT,xvT,yvT= tst.trimBorders(data,xv,yv,left,right,top,bottom)
    
    if pol['Criteria_ave']==1:
        aveData = dataT.copy()
    elif pol['Criteria_ave']==8:
        # Daily-maximum 8h-moving average
        aveData = tst.movingAverage(datesTime,dataT,8)
        datesTime = datesTime.groupby(by=['year', 'month', 'day']).size().reset_index()
        datesTime['datetime']=pd.to_datetime(datesTime[['year', 'month', 'day']])
    elif pol['Criteria_ave']==24:
        # Daily averages
        aveData, dailyData = tst.dailyAverage(datesTime,dataT)
        datesTime = datesTime.groupby(by=['year', 'month', 'day']).size().reset_index()
        datesTime['datetime']=pd.to_datetime(datesTime[['year', 'month', 'day']])           
    # Monthly averages
    #monthlyData = tst.monthlyAverage(datesTime,dataT)
    
    # Frequency of violations
    freqExcd= tst.exceedance(aveData,pol['Criteria'])
    
    # Transforming mercator to latlon/degrees
    xlon, ylat = tst.eqmerc2latlon(ds,xvT,yvT)
    
    # Figures
    # Average
    legend = pol['Criteria_average'] + ' ' +pol['Pollutant'] +' ('+ pol['Unit'] + ')'
    #cmap = 'YlOrRd'
    cmap = matplotlib.colors.LinearSegmentedColormap.from_list("", ["azure","lightgray","crimson","darkred"])
    garfig.timeAverageFig(aveData.max(axis=0)[0,:,:],xlon,ylat,legend,cmap,
                          borderShape,figfolder,pol['tag'],pol['Criteria_average'])
    
    # Exceedence
    legend2 = pol['Criteria_average'] +' ' + pol['Pollutant'] + ' - violations'
    #cmap = 'RdPu'
    cmap2 = matplotlib.colors.LinearSegmentedColormap.from_list("", ["azure","lightgray","salmon","red","purple"])
    garfig.exceedanceFig(freqExcd[0,:,:],xlon,ylat,legend2,cmap2,borderShape,
                         figfolder,pol['tag'],pol['Criteria_average'])
    
    # Criteria
    
    cmap3 = matplotlib.colors.LinearSegmentedColormap.from_list("", ["azure","lightgray","salmon","brown"])
    #cmap = 'YlOrBr'     
    garfig.criteriaFig(aveData.max(axis=0)[0,:,:],xlon,ylat,legend,cmap3,
                       borderShape,pol['Criteria'],
                       figfolder,pol['tag'],pol['Criteria_average'])
    
   # Yearly averages
    if "Criteria_annual" in pol:
        yearlyData = tst.yearlyAverage(datesTimeAll,dataT)
        # Frequency of violations
        freqExcdY= tst.exceedance(yearlyData,pol['Criteria_annual'])
        legend3 = 'Annual average ' + pol['Pollutant'] + '('+ pol['Unit']+')'
        cmap4 = matplotlib.colors.LinearSegmentedColormap.from_list("", ["azure","lightgray","crimson","darkred"])        
        garfig.timeAverageFig(yearlyData.max(axis=0)[0,:,:],xlon,ylat,legend3,
                              cmap4,borderShape,
                              figfolder,pol['tag'],'Annual average')
        # Exceedence
        legend4 = 'Annual average ' + pol['Pollutant'] + ' - violations'
        cmap5 = matplotlib.colors.LinearSegmentedColormap.from_list("", ["azure","lightgray","salmon","red","purple"])
        garfig.exceedanceFig(freqExcdY[0,:,:],xlon,ylat,legend4,
                             cmap5,borderShape,
                             figfolder,pol['tag'],'Annual average')
        # Criteria
        cmap6 = matplotlib.colors.LinearSegmentedColormap.from_list("", ["azure","lightgray","salmon","brown"])    
        garfig.criteriaFig(yearlyData.max(axis=0)[0,:,:],xlon,ylat,legend3,
                           cmap6,borderShape,pol['Criteria_annual'],
                           figfolder,pol['tag'],'Annual average')
    
    print('Analyzing by city')
    cities = gpd.read_file(cityShape)
    cities.crs = "EPSG:4326"
    cities = cities[cities['SIGLA_UF']=='SC']
    s,cityMat = tst.citiesINdomain(xlon, ylat, cities)
    matDataAll=aveData.copy()
    matDataAll[:,:,np.isnan(cityMat)]=0
    idxMax = np.unravel_index(np.mean(matDataAll[:,0,:,:],axis=0).argmax(),
                  np.mean(matDataAll[:,0,:,:],axis=0).shape)
    
    # Critical city - highest average
    IBGE_CODEcritical=int(cityMat[idxMax])
    cityData,cityDataPoints,cityDataFrame,matData= tst.dataINcity(
        aveData,datesTime,cityMat,s,IBGE_CODEcritical)
    garfig.cityTimeSeriesMeteo(cityDataFrame,matData,cities,IBGE_CODEcritical,cmap,legend,
                       xlon,ylat,pol['Criteria'],
                       figfolder,pol['tag'],pol['Criteria_average']+'_'+str(IBGE_CODEcritical))
    
    # Critical city - highest average
    IBGE_CODEcritical=4209102 # Joinville
    cityData,cityDataPoints,cityDataFrame,matData= tst.dataINcity(
        aveData,datesTime,cityMat,s,IBGE_CODEcritical)
    garfig.cityTimeSeriesMeteo(cityDataFrame,matData,cities,IBGE_CODEcritical,cmap,legend,
                        xlon,ylat,pol['Criteria'],
                        figfolder,pol['tag'],pol['Criteria_average']+'_'+str(IBGE_CODEcritical))
    
    # Critical city - highest average
    IBGE_CODEcritical=4205407 # Florianópolis
    cityData,cityDataPoints,cityDataFrame,matData= tst.dataINcity(
        aveData,datesTime,cityMat,s,IBGE_CODEcritical)
    garfig.cityTimeSeriesMeteo(cityDataFrame,matData,cities,IBGE_CODEcritical,cmap,legend,
                        xlon,ylat,pol['Criteria'],
                        figfolder,pol['tag'],pol['Criteria_average']+'_'+str(IBGE_CODEcritical))
    
    # Critical city - highest average
    IBGE_CODEcritical=4204202 # Chapeco
    cityData,cityDataPoints,cityDataFrame,matData= tst.dataINcity(
        aveData,datesTime,cityMat,s,IBGE_CODEcritical)
    garfig.cityTimeSeriesMeteo(cityDataFrame,matData,cities,IBGE_CODEcritical,cmap,legend,
                        xlon,ylat,pol['Criteria'],
                        figfolder,pol['tag'],pol['Criteria_average']+'_'+str(IBGE_CODEcritical))
    
    # Critical city - highest average
    IBGE_CODEcritical=4204608 # Criciuma
    cityData,cityDataPoints,cityDataFrame,matData= tst.dataINcity(
        aveData,datesTime,cityMat,s,IBGE_CODEcritical)
    garfig.cityTimeSeriesMeteo(cityDataFrame,matData,cities,IBGE_CODEcritical,cmap,legend,
                        xlon,ylat,pol['Criteria'],
                        figfolder,pol['tag'],pol['Criteria_average']+'_'+str(IBGE_CODEcritical))
    
    # Critical city - highest average
    IBGE_CODEcritical=4209300 # Lages
    cityData,cityDataPoints,cityDataFrame,matData= tst.dataINcity(
        aveData,datesTime,cityMat,s,IBGE_CODEcritical)
    garfig.cityTimeSeriesMeteo(cityDataFrame,matData,cities,IBGE_CODEcritical,cmap,legend,
                        xlon,ylat,pol['Criteria'],
                        figfolder,pol['tag'],pol['Criteria_average']+'_'+str(IBGE_CODEcritical))
    
    
    for IBGE_CODE in cities['CD_MUN']:
        IBGE_CODE=int(IBGE_CODE)
        #tabsfolder=path+'/tables'
        if os.path.isdir(tabsfolder+'/'+pol['tag'])==0:
            os.mkdir(tabsfolder+'/'+pol['tag'])
        cityData,cityDataPoints,cityDataFrame,matData= tst.dataINcity(
            aveData,datesTime,cityMat,s,IBGE_CODEcritical)
        cityDataFrame.to_csv(tabsfolder+'/'+pol['tag']+'/'+pol['tag']+'_'+str(IBGE_CODE)+'.csv')
    
