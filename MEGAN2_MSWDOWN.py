# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

#Importing libraries
import netCDF4 as nc4
import numpy as np
import os


# Folder of global PFT file
folder = '/home/WRFout'
dataMean=[]
for ii in range(1,13):
    if ii <10:
        files = [jj for jj in os.listdir(folder) if os.path.isfile(os.path.join(folder,jj)) and \
                 'wrfout_d01_2016-0'+str(ii) in jj]
    else:
        files = [jj for jj in os.listdir(folder) if os.path.isfile(os.path.join(folder,jj)) and \
                 'wrfout_d01_2016-'+str(ii) in jj]
    
    f1 = nc4.Dataset(folder+'/'+files[0])
    lon=f1['XLONG'][1,1,:]
    lat=f1['XLAT'][1,:,1]
    
    count = 1
    for file in files:
        f1 = nc4.Dataset(folder+'/'+file)
        if count == 1:
            data3= f1['SWDOWN'][:]
            data31= f1['T2'][:]
        else:
            dataN= f1['SWDOWN'][:]
            dataN1= f1['T2'][:]
            data3 = np.concatenate([data3, dataN],0)
            data31 = np.concatenate([data31, dataN1],0)
        count = count +1    

    if ii ==1:
        dataMean = np.mean(data3,0)
        dataMean1 = np.mean(data31,0)
    else:
        dataMean = np.dstack([dataMean, np.mean(data3,0)])
        dataMean1 = np.dstack([dataMean1, np.mean(data31,0)])



# create NetCDF file
nco = nc4.Dataset(folder + '/DW.nc','w',
                  clobber=True, format='NETCDF3_CLASSIC')
nco1 = nc4.Dataset(folder + '/TAS.nc','w',
                  clobber=True, format='NETCDF3_CLASSIC')

# create dimensions, variables and attributes:
nco.createDimension('lon',len(lon))
nco.createDimension('lat',len(lat))
nco.createDimension('times',dataMean.shape[2])
nco1.createDimension('lon',len(lon))
nco1.createDimension('lat',len(lat))
nco1.createDimension('times',dataMean1.shape[2])

LON = nco.createVariable('lon',np.float64,('lon'))
LON.units = 'degrees'
LON.standard_name = 'longitude'
LON[:] = lon

TIME = nco.createVariable('times','S1',('times'))
TIME.units = 'month'
TIME.standard_name = 'month'
teste = np.array(range(1,13))
TIME[:] = teste.astype(str)

TIME1 = nco1.createVariable('times','S1',('times'))
TIME1.units = 'times'
TIME1.standard_name = 'times'
teste = np.array(range(1,13))
TIME1[:] = teste.astype(str)


LON1 = nco1.createVariable('lon',np.float64,('lon'))
LON1.units = 'degrees'
LON1.standard_name = 'longitude'
LON1[:] = lon


LAT = nco.createVariable('lat',np.float64,('lat'))
LAT.units = 'degrees'
LAT.standard_name = 'latitude'
LAT[:] = lat

LAT1 = nco1.createVariable('lat',np.float64,('lat'))
LAT1.units = 'degrees'
LAT1.standard_name = 'latitude'
LAT1[:] = lat

# Adding description
nco.FILEDESC = 'Global PFT netCDF files created by Leonardo Hoinaski '
nco1.FILEDESC = 'Global PFT netCDF files created by Leonardo Hoinaski '

data3F = np.moveaxis(dataMean, 2, 0)
# Addind data to netCDF file
VAR  = nco.createVariable('DSW_AVE', np.float64, ('times','lat','lon'))
VAR[:,:,:] = data3F
nco.close()

data31F = np.moveaxis(dataMean1, 2, 0)
VAR1 = nco1.createVariable('TAS_AVE', np.float64, ('times','lat','lon'))
VAR1[:,:,:] = data31F
nco1.close()
   
