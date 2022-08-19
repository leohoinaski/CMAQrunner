#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug  4 15:21:28 2022

@author: leohoinaski


"""

import os
import argparse
import numpy as np
import netCDF4 as nc
import datetime
import sys


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--verbose', default=0, action='count')
    parser.add_argument('INDinventoryPath')
    parser.add_argument('mcipPath')
    parser.add_argument('GDNAM')
    args = parser.parse_args()

    # Path to functions and BRAVESdatabase_main.py
    rootPath = args.INDinventoryPath
    os.chdir(rootPath)

    sys.path.insert(0, rootPath)
    from data2CubeData import gridSpecMCIP
    from netCDFcreator import createNETCDFtemporalAndLayered
    
    # Path to inputs
    inPath = rootPath +'/Inputs'
    
    outPath = rootPath +'/Outputs/'+args.GDNAM
    if os.path.isdir(outPath)==0:
        os.mkdir(outPath)
    
    gridName = args.GDNAM
    mcipPath = args.mcipPath
    mcipGRIDDOT2DPath = mcipPath+'/GRIDDOT2D_'+gridName+'.nc'
    mcipGRIDCRO2DPath = mcipPath+'/GRIDCRO2D_'+gridName+'.nc'
    mcipMETCRO3Dpath = mcipPath+'/METCRO3D_'+gridName+'.nc'
    mcipMETCRO2Dpath = mcipPath+'/METCRO2D_'+gridName+'.nc' 
    gridId = gridName+'_'+'MCIPgrid' # grid definition identification
    dataTempo=None
    dataTempo = gridSpecMCIP (rootPath,outPath,
                      mcipMETCRO3Dpath,mcipMETCRO2Dpath,
                      mcipGRIDCRO2DPath,mcipGRIDDOT2DPath)

    ds3 = nc.Dataset(mcipMETCRO3Dpath)
    time=ds3['TFLAG'][:]       
    dt0 = datetime.datetime.strptime(str(time[:,0,:][:,0][0]),'%Y%j').date()
    dt1 = datetime.datetime.strptime(str(time[:,0,:][:,0][-1]),'%Y%j').date()
    hours = [np.array(time[:,0,:][:,1]/10000)[0],
                np.array(time[:,0,:][:,1]/10000)[-1]]
    
    name = 'IND2CMAQ'+\
        '_'+str(dt0.year)+'_'+str(dt0.month).zfill(2)+'_'+str(dt0.day).zfill(2)+'_'+str(int(hours[0])).zfill(2)+'00'+\
            '_to_'+str(dt1.year)+'_'+str(dt1.month).zfill(2)+'_'+str(dt1.day).zfill(2)+'_'+str(int(hours[1])).zfill(2)+'00'+'.nc'
    
    createNETCDFtemporalAndLayered(rootPath,outPath,name,dataTempo,mcipMETCRO3Dpath)
