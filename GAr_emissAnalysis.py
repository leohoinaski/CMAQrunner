#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb  7 15:21:34 2023

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
import shutil
#%% INPUTS

fileTypes=['BRAVESdatabase2CMAQ','MEGANv31','FINNv1.5','IND2CMAQ_']

emissType=['Vehicular', 'Biogenic', 'Fire', 'Indutrial']
path = ['/media/leohoinaski/HDD/SC_2019',
        '/media/leohoinaski/HDD/SC_2019',
        '/media/leohoinaski/HDD/SC_2019',
        '/media/leohoinaski/HDD/SC_2019']
borderShape = '/media/leohoinaski/HDD/shapefiles/Brasil.shp'
cityShape='/media/leohoinaski/HDD/shapefiles/BR_Municipios_2020.shp'

fileTypes=['BRAVESdatabase2CMAQ','MEGANv31','FINNv1.5','IND2CMAQ_']
emissType=['Vehicular', 'Biogenic', 'Fire', 'Indutrial']
path = ['/home/artaxo/CMAQ_REPO/PREP/emis/BRAVES_database/Outputs/SC_2019',
        '/home/artaxo/CMAQ_REPO/PREP/emis/MEGAN/MEGANv3.21/Output',
        '/home/artaxo/CMAQ_REPO/PREP/emis/finn2cmaq-master/hourly/2019',
        '/home/artaxo/CMAQ_REPO/PREP/emis/IND_inventory/Outputs/SC_2019']
borderShape = '/home/artaxo/shapefiles/Brasil.shp'
cityShape='/home/artaxo/shapefiles/BR_Municipios_2020.shp'


cmap = [matplotlib.colors.LinearSegmentedColormap.from_list("", ["white","beige","crimson","purple"]),
        matplotlib.colors.LinearSegmentedColormap.from_list("", ["white","beige","lightgreen","darkgreen"]),
        matplotlib.colors.LinearSegmentedColormap.from_list("", ["white","beige","gold","red"]),
        matplotlib.colors.LinearSegmentedColormap.from_list("", ["white","beige","salmon","darkred"])]

# Trim domain
left = 40
right = 20
top=95
bottom=20

#%% List of pollutant emissions

NO2 = {
  "Pollutant": "$NO_{2}$",
  "Unit": '$mol.s{-1}$',
  "tag":'NO2',
}

NO = {
  "Pollutant": "NO",
  "Unit": '$mol.s^{-1}$',
  "tag":'NO',
}

CO = {
  "Pollutant": "CO",
  "Unit": '$mol.s^{-1}$',
  "tag":'CO',
}


SO2 = {
  "Pollutant": "$SO_{2}$",
  "Unit": '$mol.s^{-1}$',
  "tag":'SO2'
}

# PM10 = {
#   "Pollutant": "$PM_{10}$",
#   "Criteria": 50,
#   "Unit": '$\u03BCg.m^{-3}$',
#   "Criteria_annual": 20,
#   "Criteria_average": '24-h average',
#   "tag":'PM10',
#   "Criteria_ave": 24,
# }

# PM25 = {
#   "Pollutant": "$PM_{2.5}$",
#   "Criteria": 25,
#   "Unit": '$\u03BCg.m^{-3}$',
#   "Criteria_annual": 10,
#   "Criteria_average": '24-h average',
#   "tag":'PM25',
#   "Criteria_ave": 24,
# }

pollutants = [NO,CO]

#%% ------------------------------PROCESSING-----------------------------------
print('--------------Start GAr_emissAnalysis.py------------')
#Looping each fileTypes
for count, fileType in enumerate(fileTypes):
    print(fileType)
    # Moving to dir
    os.chdir(path[count])
    print('creating folder')
    # Creating output folders
    figfolder=path[count]+'/EMISfigures_'+emissType[count]
    if os.path.isdir(figfolder)==0:
        os.mkdir(figfolder)
    else:
        shutil.rmtree(figfolder)
        os.mkdir(figfolder)
        
    tabsfolder=path[count]+'/EMIStables_'+emissType[count]
    if os.path.isdir(tabsfolder)==0:
        os.mkdir(tabsfolder)
    else:
        shutil.rmtree(tabsfolder)
        os.mkdir(tabsfolder)
    
    # Selecting files and variables
    prefixed = sorted([filename for filename in os.listdir(path[count]) if filename.startswith(fileType)])
    
    # Opening netCDF files
    ds = nc.MFDataset(prefixed)
    
    #Looping each pollutant
    for pol in pollutants:
        print(pol)
        # Selecting variable
        data = ds[pol['tag']][:]
        data = np.nansum(data,axis=1)
        
        # Get datesTime and removing duplicates
        datesTime, data = tst.getTime(ds,data)
        datesTimeAll = datesTime.copy()
        
        # Get coordinates from ioapi 
        xv,yv,lon,lat = tst.ioapiCoords(ds)
        
        # Trim borders left/right/bottom/top
        dataT,xvT,yvT= tst.trimBorders(data,xv,yv,left,right,top,bottom)
        
        # Transforming mercator to latlon/degrees
        xlon, ylat = tst.eqmerc2latlon(ds,xvT,yvT)
        
        #Yearly averages
        yearlyData = tst.yearlySum(datesTimeAll,dataT)
        
        # Analyzing by city
        cities = gpd.read_file(cityShape)
        cities.crs = "EPSG:4326"
        cities = cities[cities['SIGLA_UF']=='SC']
        s,cityMat = tst.citiesINdomain(xlon, ylat, cities)
        matDataAll=dataT.copy()
        matDataAll[:,np.isnan(cityMat)]=0
        idxMax = np.unravel_index(np.sum(matDataAll[:,:,:],axis=0).argmax(),
                      np.mean(matDataAll[:,:,:],axis=0).shape)
        
        # ============================Figures==================================
        
        # Spatial distribution
        legend = 'Annual '+emissType[count]+' emission of ' + pol['Pollutant'] + ' ('+'$mol.year^{-1}$'+')'
        garfig.spatialEmissFig(np.nansum(yearlyData[:,:,:],axis=0),xlon,ylat,
                               legend,cmap[count],borderShape,figfolder,
                               pol['tag'],emissType[count])
                          
        
        # Critical city - highest average
        IBGE_CODEcritical=int(cityMat[idxMax])
        cityData,cityDataPoints,cityDataFrame,matData= tst.dataINcity(
            dataT,datesTime,cityMat,s,IBGE_CODEcritical)
        legend = emissType[count]+' emission of '+ pol['Pollutant'] + ' ('+ pol['Unit']+')'
        garfig.cityTimeSeries(cityDataFrame,matData,cities,IBGE_CODEcritical,
                              cmap[count],legend,
                              xlon,ylat,None,
                              figfolder,pol['tag'],emissType[count]+
                              '_emissions'+'_'+str(IBGE_CODEcritical))
        
        # Critical city - highest average
        IBGE_CODEcritical=4209102 # Joinville
        cityData,cityDataPoints,cityDataFrame,matData= tst.dataINcity(
            dataT,datesTime,cityMat,s,IBGE_CODEcritical)
        legend = emissType[count]+' emission of '+ pol['Pollutant'] + ' ('+ pol['Unit']+')'
        garfig.cityTimeSeries(cityDataFrame,matData,cities,IBGE_CODEcritical,
                              cmap[count],legend,
                              xlon,ylat,None,
                              figfolder,pol['tag'],emissType[count]+
                              '_emissions'+'_'+str(IBGE_CODEcritical))
        
        # Critical city - highest average
        IBGE_CODEcritical=4205407 # Florianópolis
        cityData,cityDataPoints,cityDataFrame,matData= tst.dataINcity(
            dataT,datesTime,cityMat,s,IBGE_CODEcritical)
        legend = emissType[count]+' emission of '+ pol['Pollutant'] + ' ('+ pol['Unit']+')'
        garfig.cityTimeSeries(cityDataFrame,matData,cities,IBGE_CODEcritical,
                              cmap[count],legend,
                              xlon,ylat,None,
                              figfolder,pol['tag'],emissType[count]+
                              '_emissions'+'_'+str(IBGE_CODEcritical))
        
        # Critical city - highest average
        IBGE_CODEcritical=4204202 # Chapeco
        cityData,cityDataPoints,cityDataFrame,matData= tst.dataINcity(
            dataT,datesTime,cityMat,s,IBGE_CODEcritical)
        legend = emissType[count]+' emission of '+ pol['Pollutant'] + ' ('+ pol['Unit']+')'
        garfig.cityTimeSeries(cityDataFrame,matData,cities,IBGE_CODEcritical,
                              cmap[count],legend,
                              xlon,ylat,None,
                              figfolder,pol['tag'],emissType[count]+
                              '_emissions'+'_'+str(IBGE_CODEcritical))
        
        # Critical city - highest average
        IBGE_CODEcritical=4204608 # Criciuma
        cityData,cityDataPoints,cityDataFrame,matData= tst.dataINcity(
            dataT,datesTime,cityMat,s,IBGE_CODEcritical)
        legend = emissType[count]+' emission of '+ pol['Pollutant'] + ' ('+ pol['Unit']+')'
        garfig.cityTimeSeries(cityDataFrame,matData,cities,IBGE_CODEcritical,
                              cmap[count],legend,
                              xlon,ylat,None,
                              figfolder,pol['tag'],emissType[count]+
                              '_emissions'+'_'+str(IBGE_CODEcritical))
        
        # Critical city - highest average
        IBGE_CODEcritical=4209300 # Lages
        cityData,cityDataPoints,cityDataFrame,matData= tst.dataINcity(
            dataT,datesTime,cityMat,s,IBGE_CODEcritical)
        legend = emissType[count]+' emission of '+ pol['Pollutant'] + ' ('+ pol['Unit']+')'
        garfig.cityTimeSeries(cityDataFrame,matData,cities,IBGE_CODEcritical,
                              cmap[count],legend,
                              xlon,ylat,None,
                              figfolder,pol['tag'],emissType[count]+
                              '_emissions'+'_'+str(IBGE_CODEcritical))
        
        # # Saving data for each city
        # for IBGE_CODE in cities['CD_MUN']:
        #     IBGE_CODE=int(IBGE_CODE)
        #     if os.path.isdir(tabsfolder+'/'+pol['tag'])==0:
        #         os.mkdir(tabsfolder+'/'+pol['tag'])
        #     cityData,cityDataPoints,cityDataFrame,matData= tst.dataINcity(
        #         dataT,datesTime,cityMat,s,IBGE_CODE)
        #     cityDataFrame.to_csv(tabsfolder+'/'+pol['tag']+'/'+pol['tag']+'_'+str(IBGE_CODE)+'.csv')
        