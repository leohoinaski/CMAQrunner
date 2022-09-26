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
import datetime
import argparse
import multiprocessing as mp


# ------------------------------PROCESSING-------------------------------------
def grid2cellPolygon(x,y):
    polygons=[]
    print('Creating grid')
    for ii in range(0,x.shape[0]-1):
        for jj in range(0,y.shape[1]-1):
            xlf = x[ii,jj]
            xrg = x[ii+1,jj]
            ytp = y[ii,jj+1]
            ybt = y[ii,jj]
            polygons.append(Polygon([(xlf,ybt), (xlf,ytp), (xrg,ytp), 
                                     (xrg, ybt)])) 
    grid = gpd.GeoDataFrame({'geometry':polygons})       
    return grid

def clipOcean(grid,newShapefile):
    clipOc=[]
    for ii in range(0,grid.shape[0]):
        clipShp = newShapefile.intersection(grid.geometry[ii])
        #clipShp=clipShp[~clipShp.is_empty]
        clipOc.append(clipShp)  
        print('cell number = '+ str(ii) +' from ' + str(grid.shape[0]))

    return clipOc

def checkOceanLand(grid,dataCell,newShapefile):
    grid['LANDA'] = 0
    grid['SURFA']= 0
    grid['CELLA'] = 0
    for cell in range(0,50):
        grid['CELLA'][cell] = grid.iloc[cell,0].area
        check = np.where(~dataCell[cell].is_empty)
        if np.size(check)>0:
            for cc in check:
                if (newShapefile.TYPE[np.array(cc)]==2).bool():
                    print("LAND in cell")
                    dataCell[cell][np.array(cc)].area
                    grid['LANDA'][cell] = grid['LANDA'][cell]+dataCell[cell][np.array(cc)].area
                    
                else:
                    print("SURFZONE in cell")
                    grid['SURFA'][cell] = grid['SURFA'][cell]+dataCell[cell][np.array(cc)].area
        else:
            print('SURFZONE in cell"')
        return grid


def makeOceanShape(x,y,coast):
    lati = y.min()
    latf = y.max()
    loni = x.min()
    lonf = x.max()
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
    
    # # Creating real domain
    # lat_point_list = [lati,latf,latf,lati]
    # lon_point_list = [loni,loni,lonf,lonf]
    # domain = Polygon(zip(lon_point_list, lat_point_list))
    
    # # Clipping coastal lines inside domain
    # coastDom = gpd.clip(coast['geometry'], domain).reset_index()
    # coastDom=coastDom.drop(columns=['index'])
    
    #newShapefile = gpd.clip(newShapefile, domain).reset_index()
    
    # Ploting data
    # dom = gpd.GeoSeries(domain)
    # dom.crs = "EPSG:4326"
    # fig, ax = plt.subplots()
    #dom.boundary.plot(ax=ax)
    #coast.plot(ax=ax,color='blue')
    #newShapefile.plot(ax=ax,column = 'TYPE')
    #surfzone.boundary.plot(ax=ax,color='red')
    
    # Creating new shapefile
    #newShapefile.to_file(filename=outputFolder+'/SURFZONE_'+gridName+'.shp',
     #                    driver='ESRI Shapefile')
    return newShapefile


def hoinaskiSurfZone(spAllocFolder,gridName,mcipPath):

    outputFolder = spAllocFolder+'/data/shapefiles'

    griddot2d = mcipPath+'/GRIDDOT2D_'+gridName+'.nc'
    
    # Reading shapefile
    coast = gpd.read_file(spAllocFolder+"/gshhg-shp-2.3.7/GSHHS_shp/f/GSHHS_f_L1.shp")
    
    # Reading GRIDDOT2D to extract domain frontiers
    ncGrid = nc.Dataset(griddot2d)
    x = ncGrid['LONU'][0,0,:,:]
    y = ncGrid['LATV'][0,0,:,:]
    grid = grid2cellPolygon(x,y)

    newShapefile = makeOceanShape(x,y,coast)
    newShapefile = gpd.GeoDataFrame(newShapefile, 
                                          geometry=newShapefile.geometry)

    # cpus = mp.cpu_count()-2
    # #cpus = 4
    # cityChunks = np.array_split(grid.iloc[0:100], cpus)
    # pool = mp.Pool(processes=cpus)  
    # chunk_processes = [pool.apply_async(clipOcean, 
    #                                     args=(chunk,newShapefile)) for chunk in cityChunks]                    
    # #new section
    # pool.close()
    # pool.join()  
    #pool.terminate()  
    #dataCell = [chunk.get() for chunk in chunk_processes]
    dataCell = clipOcean(grid,newShapefile)
    
    grid = checkOceanLand(grid,dataCell,newShapefile)    
    #fig, ax = plt.subplots()
    #dom.boundary.plot(ax=ax)
    #coast.plot(ax=ax,color='blue')
    #newShapefile[newShapefile['TYPE']==2].plot(ax=ax,column = 'TYPE' ,legend=True)
    #grid.plot(ax=ax,column = 'LANDA' ,legend=True)
    #surfzone.boundary.plot(ax=ax,color='red')
       
    
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