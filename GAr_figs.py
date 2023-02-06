#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 13 19:35:02 2022

@author: leohoinaski
"""

import matplotlib.pyplot as plt
import geopandas as gpd
import matplotlib as mpl
import numpy as np
from shapely.geometry import Polygon, Point
from shapely import wkt
import matplotlib.dates as mdates
#import temporalStatistics as tst

def timeAverageFig(data,xlon,ylat,legend,cmap,borderShape,folder,pol,aveTime):
    fig, ax = plt.subplots()
    cm = 1/2.54  # centimeters in inches
    fig.set_size_inches(15*cm, 10*cm)
    cmap = plt.get_cmap(cmap, 9)
    # cmap.set_under('white')
    # cmap.set_over('red')
    bounds = np.logspace(np.log10(data.min()) , np.log10(data.max()) , num=10)
    #bounds = np.linspace(data.min(), data.max(), 10)
    #norm = mpl.colors.BoundaryNorm(bounds, cmap.N)
    norm = mpl.colors.LogNorm(vmin=data.min(), vmax=data.max())
    #cmap.set_under('white')
    heatmap = ax.pcolor(xlon,ylat,data,cmap=cmap,norm=norm)
    if data.min()<0.1:
        cbar = fig.colorbar(heatmap,fraction=0.03, pad=0.02,format="%.1e",
                            extend='both', 
                            ticks=bounds,
                            spacing='proportional',
                            orientation='vertical',
                            norm=norm)
    elif (data.min()>0.1) and (data.min()<1):
        cbar = fig.colorbar(heatmap,fraction=0.03, pad=0.02,format="%.2f",
                            extend='both', 
                            ticks=bounds,
                            spacing='proportional',
                            orientation='vertical',
                            norm=norm
                            )
    elif (data.min()>=1) and (data.min()<100):  
        cbar = fig.colorbar(heatmap,fraction=0.03, pad=0.02,format="%.2f",
                            extend='both', 
                            ticks=bounds,
                            spacing='proportional',
                            orientation='vertical',
                            norm=norm)
    else:
        cbar = fig.colorbar(heatmap,fraction=0.03, pad=0.02,format="%.1e",
                            extend='both', 
                            ticks=bounds,
                            spacing='proportional',
                            orientation='vertical',
                            norm=norm)
    cbar.ax.set_ylabel(legend, rotation=270,fontsize=8)
    cbar.ax.get_yaxis().labelpad = 20
    cbar.ax.tick_params(labelsize=8)
    cbar.ax.minorticks_off()
    br = gpd.read_file(borderShape)
    br.boundary.plot(edgecolor='black',linewidth=0.5,ax=ax)
    ax.set_xlim([xlon.min(), xlon.max()])
    ax.set_ylim([ylat.min(), ylat.max()]) 
    ax.set_xticks([])
    ax.set_yticks([])
    fig.tight_layout()
    fig.savefig(folder+'/timeAverageFig_'+pol+'_'+aveTime+'.png', format="png")
    return fig


def exceedanceFig(data,xlon,ylat,legend,cmap,borderShape,folder,pol,aveTime):
    fig, ax = plt.subplots()
    cm = 1/2.54  # centimeters in inches
    fig.set_size_inches(15*cm, 10*cm)
    cmap = plt.get_cmap(cmap, 9)
    # cmap.set_under('white')
    # cmap.set_over('red')
    bounds = np.concatenate((np.array([0,1]),np.linspace(2, np.max([data.max(),8]), 7,dtype=int)))
    norm = mpl.colors.BoundaryNorm(bounds, cmap.N)
    #cmap.set_under('white')
    heatmap = ax.pcolor(xlon,ylat,data,cmap=cmap,norm=norm)
    
    cbar = fig.colorbar(heatmap,fraction=0.03, pad=0.02,
                        extend='both', 
                        ticks=bounds,
                        #spacing='proportional',
                        orientation='vertical')
    cbar.ax.set_ylabel(legend, rotation=270,fontsize=8)
    cbar.ax.get_yaxis().labelpad = 20
    cbar.ax.tick_params(labelsize=8)
    br = gpd.read_file(borderShape)
    br.boundary.plot(edgecolor='black',linewidth=0.5,ax=ax)
    ax.set_xlim([xlon.min(), xlon.max()])
    ax.set_ylim([ylat.min(), ylat.max()]) 
    ax.set_xticks([])
    ax.set_yticks([])
    fig.tight_layout()
    fig.savefig(folder+'/exceedanceFig_'+pol+'_'+aveTime+'.png', format="png")
    return fig

def criteriaFig(data,xlon,ylat,legend,cmap,borderShape,criteria,
                folder,pol,aveTime):
    fig, ax = plt.subplots()
    cm = 1/2.54  # centimeters in inches
    fig.set_size_inches(15*cm, 10*cm)
    cmap = plt.get_cmap(cmap,9)
    cmap.set_under('white')
    cmap.set_over('red')
    bounds = np.linspace(criteria*0.05, criteria, 10)
    norm = mpl.colors.BoundaryNorm(bounds, cmap.N)
    #norm = mpl.colors.Normalize(vmin=data.min(), vmax=data.max())
    heatmap = ax.pcolor(xlon,ylat,data,cmap=cmap,norm=norm)
    if data.min()<0.1:
        cbar = fig.colorbar(heatmap,fraction=0.03, pad=0.02,format="%.1e",
                            extend='both', 
                            ticks=bounds,
                            spacing='proportional',
                            orientation='vertical')
    elif (data.min()>0.1) and (data.min()<1):
        cbar = fig.colorbar(heatmap,fraction=0.03, pad=0.02,format="%.2f", 
                            extend='both', 
                            ticks=bounds,
                            spacing='proportional',
                            orientation='vertical')
    elif (data.min()>=1) and (data.min()<100):  
        cbar = fig.colorbar(heatmap,fraction=0.03, pad=0.02,format="%.2f", 
                            extend='both', 
                            ticks=bounds,
                            spacing='proportional',
                            orientation='vertical')
    else:
        cbar = fig.colorbar(heatmap,fraction=0.03, pad=0.02,format="%.1e",
                            extend='both', 
                            ticks=bounds,
                            spacing='proportional',
                            orientation='vertical')
    cbar.ax.set_ylabel(legend, rotation=270,fontsize=8)
    cbar.ax.get_yaxis().labelpad = 20
    cbar.ax.tick_params(labelsize=8)
    br = gpd.read_file(borderShape)
    br.boundary.plot(edgecolor='black',linewidth=0.5,ax=ax)
    ax.set_xlim([xlon.min(), xlon.max()])
    ax.set_ylim([ylat.min(), ylat.max()]) 
    ax.set_xticks([])
    ax.set_yticks([])
    fig.tight_layout()
    fig.savefig(folder+'/criteriaFig'+pol+'_'+aveTime+'.png', format="png")
    return fig

def cityTimeSeries(cityDataFrame,matData,cities,IBGE_CODE,cmap,legend,
                   xlon,ylat,criteria,folder,pol,aveTime):
    cityArea=cities[cities['CD_MUN']==str(IBGE_CODE)]
    cmap = plt.get_cmap(cmap,4)    
    fig, ax = plt.subplots(1,2,gridspec_kw={'width_ratios': [1, 3]})
    cm = 1/2.54  # centimeters in inches
    fig.set_size_inches(16*cm, 7*cm)

    heatmap = ax[0].pcolor(xlon,ylat,np.nanmean(matData,axis=0)[0,:,:],cmap=cmap)
    bounds = np.logspace(np.log10(np.nanmin(matData)) , np.log10(np.nanmax(matData)) , num=4)
    cbar = fig.colorbar(heatmap,fraction=0.07, pad=0.05,format="%.1e",
                        extend='both', 
                        ticks=bounds,
                        spacing='proportional',
                        orientation='horizontal',ax=ax[0])
    cbar.ax.set_xlabel(cityArea['NM_MUN'].to_string(index=False)+'\nAverage', rotation=0,fontsize=8)
    cbar.ax.get_xaxis().labelpad =5
    cbar.ax.tick_params(labelsize=6) 
    
    ax[0].set_xlim([cityArea.boundary.total_bounds[0],cityArea.boundary.total_bounds[2]])
    ax[0].set_ylim([cityArea.boundary.total_bounds[1],cityArea.boundary.total_bounds[3]])
    ax[0].set_frame_on(False)
    ax[0].set_xticks([])
    ax[0].set_yticks([])
    cityArea.boundary.plot(edgecolor='black',linewidth=0.5,ax=ax[0])
    cities.boundary.plot(edgecolor='gray',linewidth=0.3,ax=ax[0])
    
    ax[1].fill_between(cityDataFrame.mean(axis=1).index,cityDataFrame.max(axis=1), cityDataFrame.min(axis=1),
                     color=None,       # The outline color
                     facecolor="Orange",
                     alpha=0.2,label='Min-Max')          # Transparency of the fill
    ax[1].plot(cityDataFrame.mean(axis=1).index,cityDataFrame.mean(axis=1),
               color='Orange',linewidth=1,label='Average')
    ax[1].xaxis.set_tick_params(labelsize=7)
    ax[1].yaxis.set_tick_params(labelsize=8)
    ax[1].set_ylim([0,np.nanmax(matData)*1.1])
    ax[1].set_xlim([np.min(cityDataFrame.mean(axis=1).index),np.nanmax(cityDataFrame.mean(axis=1).index)])
    ax[1].xaxis.set_major_locator(mdates.MonthLocator(interval=1))
    # set formatter
    if criteria!=None:
        ax[1].axhline(y=criteria, color='gray', linestyle='--',linewidth=0.5,
                      label='Air quality standard')
    ax[1].xaxis.set_major_formatter(mdates.DateFormatter('%d-%m-%Y'))
    for label in ax[1].get_xticklabels(which='major'):
        label.set(rotation=30, horizontalalignment='right')
    ax[1].legend(prop={'size': 6})
    ax[1].set_ylabel(cityArea['NM_MUN'].to_string(index=False)+'\n'+legend,fontsize=8)
    fig.tight_layout()
    fig.savefig(folder+'/cityTimeSeries_'+pol+'_'+aveTime+'.png', format="png")
    return fig
        
