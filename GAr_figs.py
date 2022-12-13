#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 13 19:35:02 2022

@author: leohoinaski
"""

import matplotlib.pyplot as plt
from pyproj import Proj, transform

def timeAverageFig(data,xlon,xlon):
    borderShape = '/media/leohoinaski/HDD/HospDisaggregation/Inputs/shapefiles/Brasil.shp'
    fig, ax = plt.subplots()
    ax.pcolor(xlon,ylat,mvAveData[0,0,:,:])
    
    br = gpd.read_file(borderShape)
    br.boundary.plot(edgecolor='black',linewidth=1,ax=ax)
    ax.set_xlim([xlon.min(), xlon.max()])
    ax.set_ylim([ylat.min(), ylat.max()]) 
    



