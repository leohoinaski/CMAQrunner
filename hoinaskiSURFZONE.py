#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 22 16:37:26 2022

shapefile from https://www.ngdc.noaa.gov/mgg/shorelines/


@author: Leonardo Hoinaski - leonardo.hoinaski@ufsc.br

-------------------------------------------------------------------------------
"""
#Importing packages
import geopandas as gpd
import pandas as pd
import numpy as np
from shapely.geometry import Polygon
from matplotlib import pyplot as plt 
import netCDF4 as nc
import subprocess
import datetime
import argparse
#from CMAQ_writeSurfzoneAlloc import CMAQ_surfScript

# --------------------------------INPUTS---------------------------------------


# spAllocFolder = '/media/leohoinaski/Backup/Spatial-Allocator'


# gridName = 'SC_2019'

# mcipFolder = '/media/leohoinaski/Backup/'+gridName



def CMAQ_surfScript (sptAllocPath,mcipPath,gridName):

    striptPath = sptAllocPath+'/scripts'
       
    file1 = open(striptPath + "/alloc_surf_zone_to_oceanfile.csh","w") 
      
    file1.write('#! /bin/csh -f')

    # Adding control text
    str_1 = "\n#******************* Allocate Shapefiles Run Script **************************\
    \n# Allocates a polygon shapefile's data to an I/O API gridded file \
    \n# File created by Leonardo Hoinaski  - leonardo.hoinaski@ufsc.br \
    \n#" + str(datetime.datetime.now())+ '\
    \n#*****************************************************************************\n'
    file1.write(str_1)
    file1.write('\n')

    str_2 = '\nsetenv DEBUG_OUTPUT Y\n\
    \nsetenv SA_HOME '+ sptAllocPath +'\n\
    \nsetenv EXE "$SA_HOME/bin/64bits/allocator.exe"\n\
    \nsetenv DATADIR $SA_HOME/data/shapefiles\n\
    \nsetenv OUTPUT $SA_HOME/data\n\
    \nsetenv MIMS_PROCESSING ALLOCATE\n\
    \nsetenv TIME time\n\
    \nsetenv GRIDDESC '+ mcipPath + '/GRIDDESC\n\
    \nsetenv INPUT_FILE_NAME $DATADIR/SURFZONE_SC_2019\n\
    \nsetenv INPUT_FILE_TYPE ShapeFile\n\
    \nsetenv INPUT_FILE_MAP_PRJN "+proj=latlon"\n\
    \nsetenv INPUT_FILE_ELLIPSOID "+a=6370000.0,+b=6370000.0"\n\
    \nsetenv ALLOCATE_ATTRS TYPE\n\
    \nsetenv ALLOC_MODE_FILE ALL_AREAPERCENT\n\
    \nsetenv ALLOC_ATTR_TYPE  SURF_ZONE\n\
    \nsetenv OUTPUT_FILE_TYPE IoapiFile\n\
    \nsetenv OUTPUT_GRID_NAME '+ gridName +'\n\
    \n#setenv OUTPUT_FILE_MAP_PRJN "+proj=lcc,+lat_1=33,+lat_2=45,+lat_0=40,+lon_0=-97"\n\
    \nsetenv OUTPUT_FILE_ELLIPSOID "+a=6370000.0,+b=6370000.0"\n\
    \nsetenv OUTPUT_FILE_NAME $OUTPUT/ocean_file_${OUTPUT_GRID_NAME}.ncf\n\
    \n$TIME $EXE\n'
    
    file1.write(str_2)
    file1.close()
    
    return file1

def hoinaskiSurfZone(spAllocFolder,gridName,mcipPath):
# ------------------------------PROCESSING-------------------------------------

    outputFolder = spAllocFolder+'/data/shapefiles'
    
    
    griddot2d = mcipPath+'/GRIDDOT2D_'+gridName+'.nc'
    
    # Reading shapefile
    coast = gpd.read_file(spAllocFolder+"/data/shapefiles/gshhg-shp-2.3.7/GSHHS_shp/f/GSHHS_f_L1.shp")
    
    # Reading GRIDDOT2D to extract domain frontiers
    ncGrid = nc.Dataset(griddot2d)
    
    # Domain
    lati = np.unique(ncGrid['LATD'][:]).min()
    latf = np.unique(ncGrid['LATD'][:]).max()
    loni = np.unique(ncGrid['LOND'][:]).min()
    lonf = np.unique(ncGrid['LOND'][:]).max()
    delta = 0.1 #Shifiting domain borders
    
    # Creating polygon from domain with delta
    lat_point_list = [lati-delta,latf+delta,latf+delta,lati-delta]
    lon_point_list = [loni-delta,loni-delta,lonf+delta,lonf+delta]
    domain = Polygon(zip(lon_point_list, lat_point_list))
    
    # Clipping coastal lines inside domain
    coastDom = gpd.clip(coast['geometry'], domain).reset_index()
    coastDom=coastDom.drop(columns=['index'])
    
    # Buffering cliped coastal lines
    coastBuffer = coastDom.to_crs(6933)
    coastBuffer=coastBuffer.buffer(50)
    coastBuffer = coastBuffer.to_crs(4326) #Back to 4326
    
    # CLipping bufferzone/surfzone
    coastLine = []
    for ii in range(0,coastDom.shape[0]):
        cLine = coastBuffer[ii].difference(coastDom.geometry[ii])   
        coastLine.append(cLine)
    
    surfzone = gpd.GeoSeries(coastLine)
    surfzone.crs = "EPSG:4326"
    surfzone = gpd.GeoDataFrame(surfzone)
    surfzone = surfzone.rename(columns={0:'geometry'}).set_geometry('geometry')
    surfzone['TYPE'] = 3
    surfzone['DESCRIP'] = 'SURFZONE'
    coastDom['TYPE'] = 2
    coastDom['DESCRIP'] = 'LAND'
    
    # Concatenating shapefiles
    newShapefile = pd.concat([surfzone, coastDom], ignore_index=True)
    
    # Creating real domain
    lat_point_list = [lati,latf,latf,lati]
    lon_point_list = [loni,loni,lonf,lonf]
    domain = Polygon(zip(lon_point_list, lat_point_list))
    
    # Clipping coastal lines inside domain
    coastDom = gpd.clip(coast['geometry'], domain).reset_index()
    coastDom=coastDom.drop(columns=['index'])
    
    newShapefile = gpd.clip(newShapefile, domain).reset_index()
    
    # Ploting data
    dom = gpd.GeoSeries(domain)
    dom.crs = "EPSG:4326"
    fig, ax = plt.subplots()
    dom.boundary.plot(ax=ax)
    coast.plot(ax=ax,color='blue')
    newShapefile.plot(ax=ax,column = 'TYPE')
    #surfzone.boundary.plot(ax=ax,color='red')
    
    # Creating new shapefile
    newShapefile.to_file(filename=outputFolder+'/SURFZONE_'+gridName+'.shp',
                         driver='ESRI Shapefile')
    
    # Calling CMAQ_surfSript to write the script to run surfzone allocator
    CMAQ_surfScript (spAllocFolder,mcipPath,gridName)
    
    # Calling the surfzone allocator from CMAS
    subprocess.call([spAllocFolder+'/scripts/alloc_surf_zone_to_oceanfile.csh'])
    return outputFolder

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--verbose', default=0, action='count')
    parser.add_argument('spAllocFolder')
    parser.add_argument('GDNAM')
    parser.add_argument('mcipPath')
    args = parser.parse_args()
    spAllocFolder = args.spAllocFolder
    gridName = args.GDNAM
    mcipPath = args.mcipPath
    hoinaskiSurfZone(spAllocFolder,gridName,mcipPath)