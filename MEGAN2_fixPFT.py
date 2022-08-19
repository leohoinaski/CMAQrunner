# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

#Importing libraries
import netCDF4 as nc4
import numpy as np
#from scipy import interpolate
#import xarray
from scipy.interpolate import griddata

# Folder of global PFT fileD
#folder = '/media/leohoinaski/HDD/MEGAN'
folder = '/home/nobre/MEGAN21/inputs'

f1 = nc4.Dataset(folder+'/mksrf_landuse_rc2000_c110913.nc')
f1.variables
data1 = f1['PCT_PFT'][:]
lon=f1['LON'][:]
lat=f1['LAT'][:]

xlimits = [-90, -20]
ylimits = [-40, 10]


x = np.linspace(xlimits[0], xlimits[1], int(abs(xlimits[0]- xlimits[1]/0.005)))
y = np.linspace(ylimits[0], ylimits[1], int(abs(ylimits[0]- ylimits[1]/0.005)))
xx, yy = np.meshgrid(x,y)




indX = np.where((lon > xlimits[0]) & (lon < xlimits[1])) 
indY = np.where((lat > ylimits[0]) & (lat < ylimits[1])) 

lon = lon[min(indX[0][:]):max(indX[0][:])]
lat = lat[min(indY[0][:]):max(indY[0][:])]
xxOrig, yyOrig = np.meshgrid(lon,lat)

orig = np.array([xxOrig.flatten(), yyOrig.flatten()]).transpose()


dataBR = data1[:,min(indY[0][:]):max(indY[0][:]),
              min(indX[0][:]):max(indX[0][:])]



for ii in range (1,data1.shape[0]):
    print('FILE NUMBER = '+ str(ii))	
    if ii<10:
        fileOut = 'pft0'+str(ii)
    else:
        fileOut = 'pft'+str(ii)
        
    # create NetCDF file
    nco = nc4.Dataset(folder + '/'+fileOut+'.nc','w',
                      clobber=True, format='NETCDF3_CLASSIC')
    
    # create dimensions, variables and attributes:
    nco.createDimension('lon',len(x))
    nco.createDimension('lat',len(y))
    
    LON = nco.createVariable('lon',np.float32,('lon'))
    LON.units = 'degrees'
    LON.standard_name = 'longitude'
    LON[:] = x
    
    LAT = nco.createVariable('lat',np.float32,('lat'))
    LAT.units = 'degrees'
    LAT.standard_name = 'latitude'
    LAT[:] = y
    
    # Adding description
    nco.FILEDESC = 'Global PFT netCDF files created by Leonardo Hoinaski '
    
    # Addind data to netCDF file

    VAR  = nco.createVariable(fileOut,np.intc, ('lat','lon'))
    dataInterp = griddata(orig, dataBR[ii,:,:].flatten(), (xx, yy), method='nearest')
    VAR[:,:] = dataInterp
    # VAR[:,:] = data1[ii,min(indY[0][:]):max(indY[0][:]),
    #               min(indX[0][:]):max(indX[0][:])]
    nco.close()
   
