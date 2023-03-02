#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug  5 09:00:25 2022

@author: leohoinaski
"""
import argparse
import pandas as pd
from timezonefinder import TimezoneFinder
import netCDF4 as nc4
import os
import subprocess
import parmap
import numpy as np
import numpy.matlib

MMIFhome='/media/leohoinaski/Backup/MMIFv4.0'
outPath='/media/leohoinaski/Backup/SC_2019/METFILES'
wrf_dir='/media/leohoinaski/Backup/SC_2019'
STARTDAY='2019-01-01'
ENDDAY='2019-01-02'

def writeMMIFinput(ii,jj,xv,yv,MMIFhome,outPath,wrf_dir,STARTDAY,ENDDAY):  
    #iijj = np.array(list(iijj))
    # lat = yv[iijj[0],iijj[1]]
    # lon = xv[iijj[0],iijj[1]]
    print(str(ii) +' - -' + str(jj))
    lat = yv[ii,jj]
    lon = xv[ii,jj]
    prefixed = sorted([filename for filename in os.listdir(wrf_dir) if filename.startswith('wrfout_')])
    test_naive = pd.date_range('2019-01-01', '2019-04-07', freq='4H')
    tf = TimezoneFinder(in_memory=True)
    local_time_zone = tf.timezone_at(lng=lon, lat=lat)
    ltc = float(test_naive.tz_localize(local_time_zone).strftime('%Z')[-1])
    
    file1 = open(MMIFhome + '/mmif'+str(lat)+'_'+str(lon)+'.inp',"w", newline='\n') 
    file1.write('Start  '+STARTDAY+'_00:00:00\n')
    file1.write('Stop   '+ENDDAY+'_00:00:00\n')
    file1.write('TimeZone   '+str(int(ltc))+'\n')
    file1.write('CALSCI_MIXHT MMIF\n')
    file1.write('point IJ '+str(ii)+' '+str(jj)+'\n') 
    file1.write('aer_layers 1 1\n')
    file1.write('output aermod Useful '+outPath+'/METEO_'+str(lat)+'_'+str(lon)+'.info\n')
    file1.write('output aermod sfc    '+outPath+'/METEO_'+str(lat)+'_'+str(lon)+'.sfc\n')
    file1.write('output aermod pfl    '+outPath+'/METEO_'+str(lat)+'_'+str(lon)+'.pfl\n')
    
    for pr in prefixed:
        file1.write('input '+wrf_dir+'/'+pr+'\n')
    file1.close()
    
    subprocess.run([MMIFhome+'/mmif ' + MMIFhome+'/mmif'+str(lat)+'_'+str(lon)+'.inp' ],shell=True)
    os.remove(MMIFhome+'/mmif'+str(lat)+'_'+str(lon)+'.inp')
    return



if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--verbose', default=0, action='count')
    parser.add_argument('MMIFhome')
    parser.add_argument('wrf_dir')
    parser.add_argument('outPath')
    parser.add_argument('STARTDAY')
    parser.add_argument('ENDDAY')
    args = parser.parse_args()
    MMIFhome = args.MMIFhome
    outPath = args.outPath
    wrf_dir = args.wrf_dir
    STARTDAY = args.STARTDAY
    ENDDAY = args.ENDDAY

    prefixed = sorted([filename for filename in os.listdir(wrf_dir) if filename.startswith('wrfout_')])
    ds=nc4.Dataset(wrf_dir+'/'+prefixed[0])
    xv = ds['XLONG'][0,:,:]
    yv = ds['XLAT'][0,:,:]
    
    if os.path.isdir(outPath)==0:
        os.mkdir(outPath)
    else:
        os.rmdir(outPath)
        os.mkdir(outPath)

    
    # for ii in range(6,xv.shape[0]-6):
    #     for jj in range(6,xv.shape[1]-6): 
    #         
    #         writeMMIFinput(ii,jj,MMIFhome,outPath,wrf_dir,STARTDAY,ENDDAY,lat,lon)
    #         #proc = subprocess.run([MMIFhome+'/mmif ' + MMIFhome+'/mmif.inp' ],shell=True)
    ii = np.matlib.repmat(list(range(6,xv.shape[0]-6)),xv.shape[1]-6,1).flatten().tolist()
    jj = np.matlib.repmat(list(range(6,xv.shape[1]-6)),xv.shape[0]-6,1).transpose().flatten().tolist()
    
    
    parmap.starmap(writeMMIFinput,zip(ii,jj),xv,yv,MMIFhome,outPath,wrf_dir,STARTDAY,ENDDAY)
