#!/usr/bin/env python3 
# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

#Importing libraries
import netCDF4 as nc4
import numpy as np
import argparse

def fixLAI(folder,GDNAM):
    # Reading arcGIS grid format files Global, monthly ~1-km LAIv 
    fileIn = '/LAIS46.'+GDNAM+'.ncf'
    fileOut ='/LAIS46.'+GDNAM+'.fixed.ncf'
    f1 = nc4.Dataset(folder+fileIn)
    tflag=f1['TFLAG'][:]
    lais=f1['LAIS'][:]
    
    # create NetCDF file
    nco = nc4.Dataset(folder+fileOut,'w',clobber=True, format='NETCDF3_CLASSIC')
    
    # create dimensions, variables and attributes:
    nco.createDimension('TSTEP',lais.shape[0])
    nco.createDimension('DATE-TIME',2)
    nco.createDimension('LAY',lais.shape[1])
    nco.createDimension('VAR',tflag.shape[1])
    nco.createDimension('ROW',lais.shape[2])
    nco.createDimension('COL',lais.shape[3])
    
    TFLAG = nco.createVariable('TFLAG',np.int32,('TSTEP', 'VAR', 'DATE-TIME'))
    TFLAG.units = "<YYYYDDD,HHMMSS>"
    TFLAG.long_name = "TFLAG"
    TFLAG.var_desc = "Timestep-valid flags:  (1) YYYYDDD or (2) HHMMSS"
    
    # FIXING TFLAGS 
    tflag2 = tflag
    count = 0
    count2 = 0
    for ii in range(0,tflag2.shape[0]):  
        if count > 230000:
            count = 0
            count2 = 1
        tflag2[ii,:,0] = count2
        tflag2[ii,:,1] = count
        count = count + 10000
        #print('date: '+ str(ii)) 
    TFLAG[:,:,:] = tflag2
    
    # FIXING LAIS 
    lais2 =np.array(lais)
    
    for tt in range(0,lais.shape[0]):
        for ii in range(0,lais.shape[2]):
            for jj in range(0,lais.shape[3]):
                if tt<=3:
                    lais2[tt,0,ii,jj] = lais[0,0,ii,jj]
                elif tt>3 and tt<=7:
                    lais2[tt,0,ii,jj] = lais[1,0,ii,jj]
                elif tt>7 and tt<=11:
                    lais2[tt,0,ii,jj] = lais[2,0,ii,jj]
                elif tt>11 and tt<=15:
                    lais2[tt,0,ii,jj] = lais[3,0,ii,jj]
                elif tt>15 and tt<=19:
                    lais2[tt,0,ii,jj] = lais[4,0,ii,jj]
                elif tt>19 and tt<=23:
                    lais2[tt,0,ii,jj] = lais[5,0,ii,jj]
                elif tt>23 and tt<=27:
                    lais2[tt,0,ii,jj] = lais[6,0,ii,jj]   
                elif tt>27 and tt<=31:
                    lais2[tt,0,ii,jj] = lais[7,0,ii,jj]
                elif tt>31 and tt<=35:
                    lais2[tt,0,ii,jj] = lais[8,0,ii,jj]                
                elif tt>35 and tt<=39:
                    lais2[tt,0,ii,jj] = lais[9,0,ii,jj]
                elif tt>39 and tt<=43:
                    lais2[tt,0,ii,jj] = lais[10,0,ii,jj]
                else:
                    lais2[tt,0,ii,jj] = lais[11,0,ii,jj]
                
    
    
    
    # Addind data to netCDF file
    LAIS  = nco.createVariable('LAIS', 'f4', ('TSTEP', 'LAY', 'ROW', 'COL'))
    LAIS[:,:,:,:]= lais2 
    LAIS.long_name="LAIS            "
    LAIS.units= "nondimension    "
    LAIS.var_desc =""
    
    
    # Global attributes
    nco.IOAPI_VERSION = f1.IOAPI_VERSION
    nco.EXEC_ID = f1.EXEC_ID
    nco.FTYPE = f1.FTYPE
    nco.CDATE = f1.CDATE
    nco.CTIME= f1.CTIME
    nco.WDATE= f1.WDATE
    nco.WTIME= f1.WTIME
    nco.SDATE= f1.SDATE
    nco.STIME= f1.STIME
    nco.TSTEP = 10000
    nco.NTHIK = f1.NTHIK
    nco.NCOLS=f1.NCOLS
    nco.NROWS=f1.NROWS
    nco.NLAYS=f1.NLAYS
    nco.NVARS=f1.NVARS
    nco.GDTYP=f1.GDTYP
    nco.P_ALP=f1.P_ALP
    nco.P_BET=f1.P_BET
    nco.P_GAM=f1.P_GAM
    nco.XCENT=f1.XCENT
    nco.YCENT=f1.YCENT
    nco.XORIG=f1.XORIG
    nco.YORIG=f1.YORIG
    nco.XCELL=f1.XCELL
    nco.YCELL=f1.YCELL
    nco.VGTYP=f1.VGTYP
    nco.VGTOP=f1.VGTOP
    nco.VGLVLS=f1.VGLVLS
    nco.GDNAM=f1.GDNAM
    nco.UPNAM=f1.UPNAM
    nco.VAR_LIST= "LAIS            "
    nco.FILEDESC=f1.FILEDESC
    nco.HISTORY=f1.HISTORY
    nco.renameAttribute('VAR_LIST', 'VAR-LIST')
    nco.ncattrs()
    nco.close()
    return nco

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--verbose', default=0, action='count')
    parser.add_argument('MEGANHome')
    parser.add_argument('GDNAM')
    args = parser.parse_args()
    MEGANHome = args.MEGANHome
    GDNAM = args.GDNAM
    folder = MEGANHome+'/inputs'
    fixLAI(folder,GDNAM)
