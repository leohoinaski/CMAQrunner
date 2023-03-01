#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec  9 17:49:55 2022

@author: leohoinaski
"""
#import os
import numpy as np
from datetime import datetime
import pandas as pd
#import netCDF4 as nc
#from numpy.lib.stride_tricks import sliding_window_view
import pyproj
from shapely.geometry import Point
import geopandas as gpd
from ismember import ismember
import wrf


def dailyAverage (datesTime,data):
    if len(data.shape)>3:
        daily = datesTime.groupby(['year','month','day']).count()
        dailyData = np.empty((daily.shape[0],data.shape[1],data.shape[2],data.shape[3]))
        for day in range(0,daily.shape[0]):
            findArr = (datesTime['year'] == daily.index[day][0]) & \
                (datesTime['month'] == daily.index[day][1]) & \
                    (datesTime['day'] == daily.index[day][2]) 
            dailyData[day,:,:,:] = data[findArr,:,:,:].mean(axis=0)   
    else:
        daily = datesTime.groupby(['year','month','day']).count()
        dailyData = np.empty((daily.shape[0],data.shape[1],data.shape[2]))
        for day in range(0,daily.shape[0]):
            findArr = (datesTime['year'] == daily.index[day][0]) & \
                (datesTime['month'] == daily.index[day][1]) & \
                    (datesTime['day'] == daily.index[day][2]) 
            dailyData[day,:,:] = data[findArr,:,:].mean(axis=0)   
    daily=daily.reset_index()
    return dailyData,daily

def dailyRainWRF (datesTime,data):
    if len(data.shape)>3:
        daily = datesTime.groupby(['year','month','day']).count()
        dailyData = np.empty((daily.shape[0],data.shape[1],data.shape[2],data.shape[3]))
        for day in range(0,daily.shape[0]):
            findArr = (datesTime['year'] == daily.index[day][0]) & \
                (datesTime['month'] == daily.index[day][1]) & \
                    (datesTime['day'] == daily.index[day][2])
            #findArr=findArr.reset_index()        
            findArr[np.where(findArr)[0][:-1]]=False
            dailyData[day,:,:,:] = data[findArr,:,:,:] 
    else:
        daily = datesTime.groupby(['year','month','day']).count()
        dailyData = np.empty((daily.shape[0],data.shape[1],data.shape[2]))
        for day in range(0,daily.shape[0]):
            findArr = (datesTime['year'] == daily.index[day][0]) & \
                (datesTime['month'] == daily.index[day][1]) & \
                    (datesTime['day'] == daily.index[day][2])
            findArr[np.where(findArr)[0][:-1]]=False
            dailyData[day,:,:] = data[findArr,:,:] 
    daily=daily.reset_index()
    return dailyData,daily

def monthlyAverage (datesTime,data):
    monthly = datesTime.groupby(['year','month']).count()
    monthlyData = np.empty((monthly.shape[0],data.shape[1],data.shape[2],data.shape[3]))
    for month in range(0,monthly.shape[0]):
        findArr = (datesTime['year'] == monthly.index[month][0]) & \
            (datesTime['month'] == monthly.index[month][1]) 
        monthlyData[month,:,:,:] = data[findArr,:,:,:].mean(axis=0)   

    return monthlyData

def yearlyAverage (datesTime,data):
    if len(data.shape)>3:
        yearly = datesTime.groupby(['year']).count()
        yearlyData = np.empty((yearly.shape[0],data.shape[1],data.shape[2],data.shape[3]))
        for year in range(0,yearly.shape[0]):
            if yearly.shape[0]>1:
                findArr = (datesTime['year'] == yearly.index[year])
            else:
                findArr = (datesTime['year'] == yearly.index[year])
            yearlyData[year,:,:,:] = data[findArr,:,:,:].mean(axis=0) 
    else:
        yearly = datesTime.groupby(['year']).count()
        yearlyData = np.empty((yearly.shape[0],data.shape[1],data.shape[2]))
        for year in range(0,yearly.shape[0]):
            if yearly.shape[0]>1:
                findArr = (datesTime['year'] == yearly.index[year])
            else:
                findArr = (datesTime['year'] == yearly.index[year])
            yearlyData[year,:,:] = data[findArr,:,:].mean(axis=0) 
    return yearlyData

def yearlySum (datesTime,data):
    if len(data.shape)>3:
        yearly = datesTime.groupby(['year']).count()
        yearlyData = np.empty((yearly.shape[0],data.shape[1],data.shape[2],data.shape[3]))
        for year in range(0,yearly.shape[0]):
            if yearly.shape[0]>1:
                findArr = (datesTime['year'] == yearly.index[year])
            else:
                findArr = (datesTime['year'] == yearly.index[year])
            yearlyData[year,:,:,:] = data[findArr,:,:,:].sum(axis=0)   
    else:
        yearly = datesTime.groupby(['year']).count()
        yearlyData = np.empty((yearly.shape[0],data.shape[1],data.shape[2]))
        for year in range(0,yearly.shape[0]):
            if yearly.shape[0]>1:
                findArr = (datesTime['year'] == yearly.index[year])
            else:
                findArr = (datesTime['year'] == yearly.index[year])
            yearlyData[year,:,:] = data[findArr,:,:].sum(axis=0)  
            
    return yearlyData



def movingAverage (datesTime,data,w):
    daily = datesTime.groupby(['year','month','day']).count()
    mvAveData = np.empty((daily.shape[0],data.shape[1],data.shape[2],data.shape[3]))
    for day in range(0,daily.shape[0]):
        findArr = (datesTime['year'] == daily.index[day][0]) & \
            (datesTime['month'] == daily.index[day][1]) & \
                (datesTime['day'] == daily.index[day][2]) 
        for ii in range(0,findArr.sum()):
            ddData = data[findArr,:,:,:]
            if w+ii<=findArr.sum():
                dataN = ddData[ii:w+ii,:,:,:].mean(axis=0)
                if ii==0:
                    movData=dataN
                else:
                    movData = np.max([movData,dataN],axis=0)                
        mvAveData[day,:,:,:] = movData
    return mvAveData
    
def datePrepCMAQ(ds):
    tf = np.array(ds['TFLAG'][:][:,1,:])
    date=[]
    for ii in range(0,tf.shape[0]):
        date.append(datetime.strptime(tf[:,0].astype(str)[ii] + (tf[:,1]/10000).astype(int).astype(str)[ii], '%Y%j%H').strftime('%Y-%m-%d %H:00:00'))
    
    date = np.array(date,dtype='datetime64[s]')
    dates = pd.DatetimeIndex(date)
    datesTime=pd.DataFrame()
    datesTime['year'] = dates.year
    datesTime['month'] = dates.month
    datesTime['day'] = dates.day
    datesTime['hour'] = dates.hour
    datesTime['datetime']=dates
    return datesTime

def datePrepWRF(ds):
    date = np.array(wrf.g_times.get_times(ds,timeidx=wrf.ALL_TIMES))
    dates = pd.DatetimeIndex(date)
    datesTime=pd.DataFrame()
    datesTime['year'] = dates.year
    datesTime['month'] = dates.month
    datesTime['day'] = dates.day
    datesTime['hour'] = dates.hour
    datesTime['datetime']=dates
    return datesTime

def ioapiCoords(ds):
    # Latlon
    lonI = ds.XORIG
    latI = ds.YORIG
    
    # Cell spacing 
    xcell = ds.XCELL
    ycell = ds.YCELL
    ncols = ds.NCOLS
    nrows = ds.NROWS
    
    lon = np.arange(lonI,(lonI+ncols*xcell),xcell)
    lat = np.arange(latI,(latI+nrows*ycell),ycell)
    
    xv, yv = np.meshgrid(lon,lat)
    return xv,yv,lon,lat


def exceedance(data,criteria):
    freqExcd = np.sum(data>criteria,axis=0)
    return freqExcd

def eqmerc2latlon(ds,xv,yv):

    mapstr = '+proj=merc +a=%s +b=%s +lat_ts=0 +lon_0=%s' % (
              6370000, 6370000, ds.XCENT)
    #p = pyproj.Proj("+proj=merc +lon_0="+str(ds.P_GAM)+" +k=1 +x_0=0 +y_0=0 +a=6370000 +b=6370000 +towgs84=0,0,0,0,0,0,0 +units=m +no_defs")
    p = pyproj.Proj(mapstr)
    xlon, ylat = p(xv, yv, inverse=True)
    

    return xlon,ylat

def trimBorders (data,xv,yv,left,right,top,bottom):
    if np.size(data.shape)==4:
        dataT = data[:,:,bottom:(data.shape[2]-top),left:(data.shape[3]-right)]
        xvT = xv[bottom:(data.shape[2]-top),left:(data.shape[3]-right)]
        yvT = yv[bottom:(data.shape[2]-top),left:(data.shape[3]-right)]
    if np.size(data.shape)==3:
        dataT = data[:,bottom:(data.shape[1]-top),left:(data.shape[2]-right)]
        xvT = xv[bottom:(data.shape[1]-top),left:(data.shape[2]-right)]
        yvT = yv[bottom:(data.shape[1]-top),left:(data.shape[2]-right)]
    if np.size(data.shape)==2:
        dataT = data[bottom:(data.shape[0]-top),left:(data.shape[1]-right)]
        xvT = xv[bottom:(data.shape[0]-top),left:(data.shape[1]-right)]
        yvT = yv[bottom:(data.shape[0]-top),left:(data.shape[1]-right)]
    
    # xvT = xv[bottom:(data.shape[2]-top),left:(data.shape[3]-right)]
    # yvT = yv[bottom:(data.shape[2]-top),left:(data.shape[3]-right)]
    
    return dataT,xvT,yvT

              
def getTime(ds,data):
    dd = datePrepCMAQ(ds)
    idx2Remove = np.array(dd.drop_duplicates().index)
    data = data[idx2Remove]
    datesTime = dd.drop_duplicates().reset_index(drop=True)
    return datesTime,data

def getTimeWRF(ds,data):
    dd = datePrepWRF(ds)
    idx2Remove = np.array(dd.drop_duplicates().index)
    data = data[idx2Remove]
    datesTime = dd.drop_duplicates().reset_index(drop=True)
    return datesTime,data

def citiesINdomain(xlon,ylat,cities):
    s = gpd.GeoSeries(map(Point, zip(xlon.flatten(), ylat.flatten())))
    s = gpd.GeoDataFrame(geometry=s)
    s.crs = "EPSG:4326"
    s.to_crs("EPSG:4326")
    pointIn = cities.geometry.clip(s).explode()
    pointIn = gpd.GeoDataFrame({'geometry':pointIn}).reset_index()
    lia, loc = ismember(np.array((s.geometry.x,s.geometry.y)).transpose(),
                        np.array((pointIn.geometry.x,pointIn.geometry.y)).transpose(),'rows')
    s['city']=np.nan
    s.iloc[lia,1]=cities['CD_MUN'][pointIn['level_0'][loc]].values
    cityMat = np.reshape(np.array(s.city),(xlon.shape[0],xlon.shape[1])).astype(float)
    return s,cityMat

def dataINcity(aveData,datesTime,cityMat,s,IBGE_CODE):
    #IBGE_CODE=4202404
    if np.size(aveData.shape)==4:
        cityData = aveData[:,:,cityMat==IBGE_CODE]
        cityDataPoints = s[s.city.astype(float)==IBGE_CODE]
        cityData = cityData[:,0,:]
        matData = aveData.copy()
        matData[:,:,cityMat!=IBGE_CODE]=np.nan
        cityDataFrame=pd.DataFrame(cityData)
        cityDataFrame.columns = cityDataPoints.geometry.astype(str)
        cityDataFrame['Datetime']=datesTime.datetime
        cityDataFrame = cityDataFrame.set_index(['Datetime'])
    else:
        cityData = aveData[:,cityMat==IBGE_CODE]
        cityDataPoints = s[s.city.astype(float)==IBGE_CODE]
        cityData = cityData[:,:]
        matData = aveData.copy()
        matData[:,cityMat!=IBGE_CODE]=np.nan
        cityDataFrame=pd.DataFrame(cityData)
        cityDataFrame.columns = cityDataPoints.geometry.astype(str)
        cityDataFrame['Datetime']=datesTime.datetime
        cityDataFrame = cityDataFrame.set_index(['Datetime'])
    return cityData,cityDataPoints,cityDataFrame,matData

