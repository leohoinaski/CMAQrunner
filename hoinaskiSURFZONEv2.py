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
#import datetime
import argparse
#import multiprocessing as mp
import time
import netCDF4 as nc4
# ------------------------------PROCESSING-------------------------------------
def grid2cellPolygon(x,y):
    polygons=[]
    print('Creating grid')
    for ii in range(0,x.shape[0]-1):
        for jj in range(0,y.shape[1]-1):
            xlf = x[ii,jj]
            xrg = x[ii,jj+1]
            ytp = y[ii+1,jj]
            ybt = y[ii,jj]
            polygons.append(Polygon([(xlf,ybt), (xlf,ytp), (xrg,ytp), 
                                     (xrg, ybt)])) 
    grid = gpd.GeoDataFrame({'geometry':polygons})       
    return grid

def clipOcean(grid,newShapefile):
    #dataCell=[]
    for ii in range(0,grid.shape[0]):
        clipShp = newShapefile.intersection(grid.geometry[ii])
        #clipShp[~clipShp.is_empty]=0
        #dataCell.append(clipShp)  
        print('cell number = '+ str(ii) +' from ' + str(grid.shape[0]))
        grid['CELLA'][ii] = grid.iloc[ii,0].area
        check = np.where(~clipShp.is_empty)
        if np.size(check)>0:
            for jj in range(0,np.size(np.array(check))):
                if (newShapefile.TYPE[np.array(check[0][jj])]==2):
                    print("LAND in cell")
                    clipShp[np.array(check[0][jj])].area
                    grid['LANDA'][ii] = grid['LANDA'][ii]+clipShp[np.array(check[0][jj])].area
                    
                else:
                    print("SURFZONE in cell")
                    grid['SURFA'][ii] = grid['SURFA'][ii]+clipShp[np.array(check[0][jj])].area
        else:
            print('OCEAN"')
    return grid

# def checkOceanLand(grid,dataCell,newShapefile):
#     # grid['LANDA'] = 0
#     # grid['SURFA']= 0
#     # grid['CELLA'] = 0
#     for cell in range(0,len(dataCell)):
#         grid['CELLA'][cell] = grid.iloc[cell,0].area
#         check = np.where(~dataCell[cell].is_empty)
#         if np.size(check)>0:
#             for ii in range(0,np.size(np.array(check))):
#                 if (newShapefile.TYPE[np.array(check[0][ii])]==2):
#                     print("LAND in cell")
#                     dataCell[cell][np.array(check[0][ii])].area
#                     grid['LANDA'][cell] = grid['LANDA'][cell]+dataCell[cell][np.array(check[0][ii])].area
                    
#                 else:
#                     print("SURFZONE in cell")
#                     grid['SURFA'][cell] = grid['SURFA'][cell]+dataCell[cell][np.array(check[0][ii])].area
#         else:
#             print('SURFZONE in cell"')
#     return grid

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
    # Creating new shapefile
    #newShapefile.to_file(filename=outputFolder+'/SURFZONE_'+gridName+'.shp',
     #                    driver='ESRI Shapefile')
    return newShapefile

#%%
def hoinaskiSurfZone(spAllocFolder,gridName,mcipPath):

    #outputFolder = spAllocFolder+'/data/shapefiles'

    griddot2d = mcipPath+'/GRIDDOT2D_'+gridName+'.nc'
    
    # Reading shapefile
    coast = gpd.read_file(spAllocFolder+"/data/shapefiles/gshhg-shp-2.3.7/GSHHS_shp/f/GSHHS_f_L1.shp")
    
    # Reading GRIDDOT2D to extract domain frontiers
    ncGrid = nc.Dataset(griddot2d)
    x = ncGrid['LOND'][0,0,:,:]
    y = ncGrid['LATD'][0,0,:,:]
    grid = grid2cellPolygon(x,y)

    newShapefile = makeOceanShape(x,y,coast)
    newShapefile = gpd.GeoDataFrame(newShapefile, 
                                          geometry=newShapefile.geometry)
    
    #newShapefile['AREA'] = newShapefile.area
    #world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
    #sa = world[world.continent == 'South America']
    #sa=sa.dissolve(by='continent')
    # cpus = mp.cpu_count()-2
    # #cpus = 4
    # gridChunks = np.array_split(grid, cpus)
    # pool = mp.Pool(processes=cpus)  
    # chunk_processes = [pool.apply_async(clipOcean,args=(gridChunks[ii],newShapefile)) 
    #                     for ii in range(0,len(gridChunks))]
    # #new section
    # pool.close()
    # pool.join()  
    # pool.terminate()  
    # dataCell = [chunk.get() for chunk in chunk_processes]
    # dataCell = [chunk_processes[0].get()]
    grid['LANDA'] = 0
    grid['SURFA']= 0
    grid['CELLA'] = 0
    t0 = time.time()
    grid = clipOcean(grid,newShapefile)
    print (time.time() - t0)

                    
    #grid = checkOceanLand(grid,dataCell,newShapefile)    
    grid['SUM'] = grid['LANDA']+grid['SURFA']
    grid['OCEANA']=grid['CELLA'] - grid['SUM']  
    grid['OCEANP']=grid['OCEANA']/grid['CELLA'] 
    grid['SURFP']=grid['SURFA']/grid['CELLA'] 
    
    
    dataMat = np.zeros([1,2,x.shape[0]-1, x.shape[1]-1])
    
    dataMat[0,0,:,:] = np.reshape(np.array(grid['SURFP']),(x.shape[0]-1, x.shape[1]-1))
    dataMat[0,1,:,:] = np.reshape(np.array(grid['OCEANP']),(x.shape[0]-1, x.shape[1]-1))
    # for ii in range(0,dataMat.shape[2]):
    #     for jj in range(0,dataMat.shape[3]):
    #         dataMat[:,ii,jj]= dataEmiss.iloc[:,ii]
    fig, ax = plt.subplots()
    #dom.boundary.plot(ax=ax)
    #coast.plot(ax=ax,color='blue')
    #newShapefile[newShapefile['TYPE']==2].plot(ax=ax,column = 'TYPE' ,legend=True)
    #grid.plot(ax=ax,column = 'LANDA' ,legend=True)
    #surfzone.boundary.plot(ax=ax,color='red')
    #sa.boundary.plot(ax=ax,color='black')  
    grid.plot(ax=ax,column='SURFP')
    
    return dataMat
    
#%%
def createNETCDF(folder,name,dataMat,mcipPath):
    print('===================STARTING netCDFcreator=======================')
          
    f2 = nc4.Dataset(folder+'/'+name+'.ncf','w', format='NETCDF3_CLASSIC') #'w' stands for write   
    #Add global attributes
    f2.IOAPI_VERSION ='$Id: @(#) ioapi library version 3.1 $'
    f2.EXEC_ID = '???????????????'
    f2.FTYPE =  1
    griddot2d = mcipPath+'/GRIDDOT2D_'+gridName+'.nc'
    ds3 = nc4.Dataset(griddot2d)
    for gatr in ds3.ncattrs() :
        setattr(f2, gatr, ds3.getncattr(gatr))
    
    strVAR = ''
    for ids in ['SURF', 'OPEN']:
        strVAR = strVAR + ids.ljust(16)
    #strVAR ='ACET            ACROLEIN        ALD2            ALD2_PRIMARY    ALDX            BENZ            BUTADIENE13     CH4             CH4_INV         CL2             CO              CO2_INV         ETH             ETHA            ETHY            ETOH            FORM            FORM_PRIMARY    HCL             HONO            IOLE            ISOP            KET             MEOH            N2O_INV         NAPH            NH3             NH3_FERT        NO              NO2             NVOL            OLE             PAL             PAR             PCA             PCL             PEC             PFE             PH2O            PK              PMC             PMG             PMN             PMOTHR          PNA             PNCOM           PNH4            PNO3            POC             PRPA            PSI             PSO4            PTI             SO2             SOAALK          SULF            TERP            TOL             UNK             UNR             VOC_INV         XYLMN           '
    setattr(f2, 'VAR-LIST', strVAR)
    f2.NROWS=dataMat.shape[2]
    f2.NCOLS=dataMat.shape[3]

    f2.NVARS= dataMat.shape[1]
    f2.FILEDESC= 'OCEAN created by Leonardo Hoinaski '
    f2.HISTORY =''
    f2.createDimension('TSTEP', 1 )
    f2.createDimension('DATE-TIME', 2)
    f2.createDimension('LAY', 1)
    f2.createDimension('VAR', 2)
    f2.createDimension('ROW', dataMat.shape[2])
    f2.createDimension('COL', dataMat.shape[3])
    # Building variables
    TFLAG = f2.createVariable('TFLAG', 'i4', ('TSTEP', 'VAR', 'DATE-TIME'))
    SURF = f2.createVariable('SURF', np.float32, ('TSTEP', 'LAY','ROW','COL'))
    OPEN = f2.createVariable('OPEN', np.float32, ('TSTEP', 'LAY','ROW','COL'))
    # Passing data into variables
    TFLAG[:,:,:] = np.zeros((1,2,2))
    TFLAG.units = '<YYYYDDD,HHMMSS>'
    TFLAG.var_desc = 'Timestep-valid flags:  (1) YYYYDDD or (2) HHMMSS'
    SURF[:,:,:] = dataMat[0,0,:,:]
    SURF.units = 'UNKNOWN'
    SURF.var_desc = 'SURF'  
    OPEN[:,:,:] = dataMat[0,1,:,:]
    OPEN.units = 'UNKNOWN'
    OPEN.var_desc = 'OPEN'
    f2.close()
    print('OCEAN FILE in netCDF format is ready for CMAQ!')
#%%
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
    dataMat=hoinaskiSurfZone(spAllocFolder,gridName,mcipPath)
    createNETCDF(spAllocFolder+'/data','ocean_file_'+gridName,dataMat,mcipPath)
