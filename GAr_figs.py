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
#from shapely.geometry import Polygon, Point
#from shapely import wkt
import matplotlib.dates as mdates
#import temporalStatistics as tst


def numFormat(data):
    if np.nanmax(data)<0.01:
        form = "%.2e"
    elif (np.nanmax(data)>=0.01) and (np.nanmax(data)<1) :
        form = "%.2f"
    elif (np.nanmax(data)>=1) and (np.nanmax(data)<100) :
            form = "%.2f"
    else:
            form = "%.2e"
    return form

def timeAverageFig(data,xlon,ylat,legend,cmap,borderShape,folder,pol,aveTime):
    fig, ax = plt.subplots()
    cm = 1/2.54  # centimeters in inches
    fig.set_size_inches(15*cm, 10*cm)
    #cmap = plt.get_cmap(cmap, 6)
    bounds = np.array([np.percentile(data[data>0],1),
                       np.percentile(data[data>0],5),
                       np.percentile(data[data>0],10),
                        np.percentile(data[data>0],25),
                        np.percentile(data[data>0],50),
                        np.percentile(data[data>0],75),
                        np.percentile(data[data>0],90),
                        np.percentile(data[data>0],95),
                        np.percentile(data[data>0],99),
                        np.percentile(data[data>0],100)])
    norm = mpl.colors.BoundaryNorm(bounds, cmap.N)
    heatmap = ax.pcolor(xlon,ylat,data,cmap=cmap,norm=norm)
    cbar = fig.colorbar(heatmap,fraction=0.04, pad=0.02,
                        #extend='both',
                        ticks=bounds,
                        spacing='uniform',
                        orientation='horizontal',
                        norm=norm,
                        ax=ax)

    cbar.ax.tick_params(rotation=30)
    #tick_locator = mpl.ticker.MaxNLocator(nbins=5)
    #cbar.locator = tick_locator
    #cbar.ax.set_xscale('log')
    #cbar.update_ticks()
    
    cbar.ax.set_xlabel(legend, rotation=0,fontsize=6)
    cbar.ax.get_xaxis().labelpad = 2
    cbar.ax.tick_params(labelsize=6)
    #cbar.ax.locator_params(axis='both',nbins=5)
    cbar.ax.minorticks_off()
    br = gpd.read_file(borderShape)
    br.boundary.plot(edgecolor='black',linewidth=0.5,ax=ax)
    ax.set_xlim([xlon.min(), xlon.max()])
    ax.set_ylim([ylat.min(), ylat.max()]) 
    ax.set_xticks([])
    ax.set_yticks([])
    fig.tight_layout()
    fig.savefig(folder+'/timeAverageFig_'+pol+'_'+aveTime+'.png',
                format="png",bbox_inches='tight')
    return fig


def exceedanceFig(data,xlon,ylat,legend,cmap,borderShape,folder,pol,aveTime):
    fig, ax = plt.subplots()
    cm = 1/2.54  # centimeters in inches
    fig.set_size_inches(7.5*cm, 8*cm)
    #cmap = plt.get_cmap(cmap, 4)
    # cmap.set_under('white')
    # cmap.set_over('red')
      
    bounds = np.concatenate((np.array([0,1]),np.linspace(2, np.max([data.max(),8]), 5,dtype=int)))
    
    norm = mpl.colors.BoundaryNorm(bounds, cmap.N)
    #cmap.set_under('white')
    heatmap = ax.pcolor(xlon,ylat,data,cmap=cmap,norm=norm)
    #form = numFormat(data)
    cbar = fig.colorbar(heatmap,fraction=0.04, pad=0.02,format="%.0f",
                        #extend='both', 
                        ticks=bounds,
                        spacing='uniform',
                        orientation='horizontal',
                        norm=norm)
    cbar.ax.set_xticklabels(['{:.0f}'.format(x) for x in bounds],rotation=30)
    cbar.ax.set_xlabel(legend, rotation=0,fontsize=6)
    cbar.ax.get_xaxis().labelpad = 5
    cbar.ax.tick_params(labelsize=6)
    #cbar.ax.locator_params(axis='both',nbins=5)
    br = gpd.read_file(borderShape)
    br.boundary.plot(edgecolor='black',linewidth=0.5,ax=ax)
    ax.set_xlim([xlon.min(), xlon.max()])
    ax.set_ylim([ylat.min(), ylat.max()]) 
    ax.set_xticks([])
    ax.set_yticks([])
    fig.tight_layout()
    fig.savefig(folder+'/exceedanceFig_'+pol+'_'+aveTime+'.png', 
                format="png",bbox_inches='tight')
    return fig

def criteriaFig(data,xlon,ylat,legend,cmap,borderShape,criteria,
                folder,pol,aveTime):
    fig, ax = plt.subplots()
    cm = 1/2.54  # centimeters in inches
    fig.set_size_inches(7.5*cm, 8*cm)
    cmap = plt.get_cmap(cmap,4)
    cmap.set_under('lightcyan')
    cmap.set_over('red')
    bounds = np.linspace(criteria*0.05, criteria, 5)
    norm = mpl.colors.BoundaryNorm(bounds, cmap.N)
    #norm = mpl.colors.Normalize(vmin=data.min(), vmax=data.max())
    heatmap = ax.pcolor(xlon,ylat,data,cmap=cmap,norm=norm)
    form = numFormat(data)
    cbar = fig.colorbar(heatmap,fraction=0.04, pad=0.02,format=form,
                        extend='both', 
                        ticks=bounds,
                        spacing='uniform',
                        orientation='horizontal',
                        norm=norm)
    cbar.ax.set_xticklabels(['{:.1e}'.format(x) for x in bounds],rotation=30)
    cbar.ax.set_xlabel(legend, rotation=0,fontsize=6)
    cbar.ax.get_xaxis().labelpad = 5
    cbar.ax.tick_params(labelsize=6)
    #cbar.ax.locator_params(axis='both',nbins=5)
    br = gpd.read_file(borderShape)
    br.boundary.plot(edgecolor='black',linewidth=0.5,ax=ax)
    ax.set_xlim([xlon.min(), xlon.max()])
    ax.set_ylim([ylat.min(), ylat.max()]) 
    ax.set_xticks([])
    ax.set_yticks([])
    fig.tight_layout()
    fig.savefig(folder+'/criteriaFig'+pol+'_'+aveTime+'.png', 
                format="png",bbox_inches='tight')
    return fig

def cityTimeSeries(cityDataFrame,matData,cities,IBGE_CODE,cmap,legend,
                   xlon,ylat,criteria,folder,pol,aveTime):
    
    if len(matData.shape)==4:
        aveFigData= np.nanmean(matData,axis=0)[0,:,:]
    else:
        aveFigData= np.nanmean(matData,axis=0)
            
    if (np.nanmax(aveFigData)>0):
            
        cityArea=cities[cities['CD_MUN']==str(IBGE_CODE)]
        #cmap = plt.get_cmap(cmap,5)    
        fig, ax = plt.subplots(1,2,gridspec_kw={'width_ratios': [1, 3]})
        cm = 1/2.54  # centimeters in inches
        fig.set_size_inches(15*cm, 7*cm)
        cmap.set_under('white')
        bounds = np.array([np.percentile(aveFigData[aveFigData>0],3),
                                 np.percentile(aveFigData[aveFigData>0],25),
                                 np.percentile(aveFigData[aveFigData>0],50),
                                 np.percentile(aveFigData[aveFigData>0],75),
                                 np.percentile(aveFigData[aveFigData>0],97),
                                 np.percentile(aveFigData[aveFigData>0],99.9)])
        norm = mpl.colors.BoundaryNorm(bounds, cmap.N)
        heatmap = ax[0].pcolor(xlon,ylat,aveFigData,cmap=cmap,norm=norm)
        cbar = fig.colorbar(heatmap,fraction=0.04, pad=0.02,
                            ticks=bounds,
                            #extend='both',
                            spacing='uniform',
                            orientation='horizontal',
                            norm=norm,
                            ax=ax[0])

        cbar.ax.tick_params(rotation=30)
        #tick_locator = mpl.ticker.MaxNLocator(nbins=5)
        #cbar.locator = tick_locator
        #cbar.ax.set_xscale('log')
        #cbar.update_ticks()
        #cbar.ax.locator_params(axis='both',nbins=5)
        #cbar.ax.set_yscale('log')
        #cbar.update_ticks()
        #cbar.ax.set_xticklabels(['{:.1e}'.format(x) for x in bounds],rotation=30)
        cbar.ax.set_xlabel(cityArea['NM_MUN'].to_string(index=False)+'\nAverage', rotation=0,fontsize=6)
        cbar.ax.get_xaxis().labelpad = 5
        cbar.ax.tick_params(labelsize=6) 
        
        
        ax[0].set_xlim([cityArea.boundary.total_bounds[0],cityArea.boundary.total_bounds[2]])
        ax[0].set_ylim([cityArea.boundary.total_bounds[1],cityArea.boundary.total_bounds[3]])
        ax[0].set_frame_on(False)
        ax[0].set_xticks([])
        ax[0].set_yticks([])
        cityArea.boundary.plot(edgecolor='black',linewidth=0.5,ax=ax[0])
        cities.boundary.plot(edgecolor='gray',linewidth=0.3,ax=ax[0])
        
        ax[1].fill_between(cityDataFrame.mean(axis=1).index,cityDataFrame.max(axis=1), cityDataFrame.min(axis=1),
                         color=cmap(0.8),       # The outline color
                         facecolor=cmap(0.8),
                         edgecolor=None,
                         alpha=0.2,label='Min-Max')          # Transparency of the fill
        ax[1].plot(cityDataFrame.mean(axis=1).index,cityDataFrame.mean(axis=1),
                   color=cmap(0.8),linewidth=1,label='Average')
        ax[1].xaxis.set_tick_params(labelsize=6)
        ax[1].yaxis.set_tick_params(labelsize=6)
        ax[1].set_ylim([np.nanmin(matData)*0.95,np.nanmax(matData)*1.05])
        ax[1].set_xlim([cityDataFrame.index.min(),cityDataFrame.index.max()])
        ax[1].xaxis.set_major_locator(mdates.MonthLocator(interval=1))
        # set formatter
        if criteria!=None:
            ax[1].axhline(y=criteria, color='gray', linestyle='--',linewidth=0.5,
                          label='Air quality standard')
        ax[1].xaxis.set_major_formatter(mdates.DateFormatter('%d-%m-%Y'))
        for label in ax[1].get_xticklabels(which='major'):
            label.set(rotation=30, horizontalalignment='right')
        ax[1].legend(prop={'size': 6})
        ax[1].set_ylabel(cityArea['NM_MUN'].to_string(index=False)+'\n'+legend,fontsize=6)
        fig.tight_layout()
        fig.savefig(folder+'/cityTimeSeries_'+pol+'_'+aveTime+'.png', format="png",
                   bbox_inches='tight')
    return matData.shape
        

def cityTimeSeriesMeteo(cityDataFrame,matData,cities,IBGE_CODE,cmap,legend,
                   xlon,ylat,criteria,folder,pol,aveTime):
    
    if len(matData.shape)==4:
        aveFigData= np.nanmean(matData,axis=0)[0,:,:]
    else:
        aveFigData= np.nanmean(matData,axis=0)
            
    if (np.nanmax(aveFigData)>0):
            
        cityArea=cities[cities['CD_MUN']==str(IBGE_CODE)]
        #cmap = plt.get_cmap(cmap,6)    
        #cmap.set_under('white')
        fig, ax = plt.subplots(1,2,gridspec_kw={'width_ratios': [1, 3]})
        cm = 1/2.54  # centimeters in inches
        fig.set_size_inches(15*cm, 7*cm)
        bounds = np.array([np.percentile(aveFigData[aveFigData>0],3),
                                 np.percentile(aveFigData[aveFigData>0],25),
                                 np.percentile(aveFigData[aveFigData>0],50),
                                 np.percentile(aveFigData[aveFigData>0],75),
                                 np.percentile(aveFigData[aveFigData>0],97),
                                 np.percentile(aveFigData[aveFigData>0],99.9)])
        norm = mpl.colors.BoundaryNorm(bounds, cmap.N)
        # print(bounds)
        heatmap = ax[0].pcolor(xlon,ylat,aveFigData,cmap=cmap,norm=norm)
        cbar = fig.colorbar(heatmap,fraction=0.04, pad=0.02,
                            ticks=bounds,
                            #extend='both',
                            spacing='uniform',
                            orientation='horizontal',
                            norm=norm,
                            ax=ax[0])

        cbar.ax.tick_params(rotation=30)
        #tick_locator = mpl.ticker.MaxNLocator(nbins=5)
        #cbar.locator = tick_locator
        #cbar.ax.set_xscale('log')
        #cbar.update_ticks()
        #cbar.ax.locator_params(axis='both',nbins=5)
        #cbar.ax.set_xticklabels(['{:.1e}'.format(x) for x in bounds],rotation=30)
        cbar.ax.set_xlabel(cityArea['NM_MUN'].to_string(index=False)+'\nAverage', rotation=0,fontsize=6)
        cbar.ax.get_xaxis().labelpad = 5
        cbar.ax.tick_params(labelsize=6) 
        
        
        ax[0].set_xlim([cityArea.boundary.total_bounds[0],cityArea.boundary.total_bounds[2]])
        ax[0].set_ylim([cityArea.boundary.total_bounds[1],cityArea.boundary.total_bounds[3]])
        ax[0].set_frame_on(False)
        ax[0].set_xticks([])
        ax[0].set_yticks([])
        cityArea.boundary.plot(edgecolor='black',linewidth=0.5,ax=ax[0])
        cities.boundary.plot(edgecolor='gray',linewidth=0.3,ax=ax[0])
        
        ax[1].fill_between(cityDataFrame.mean(axis=1).index,np.nanmax(cityDataFrame,axis=1), np.nanmin(cityDataFrame,axis=1),
                         color=cmap(0.8),       # The outline color
                         facecolor=cmap(0.8),
                         edgecolor=None,
                         alpha=0.2,label='Min-Max')          # Transparency of the fill
        ax[1].plot(cityDataFrame.mean(axis=1).index,np.nanmean(cityDataFrame,axis=1),
                   color=cmap(0.8),linewidth=1,label='Average')
        ax[1].xaxis.set_tick_params(labelsize=6)
        ax[1].yaxis.set_tick_params(labelsize=6)
        ax[1].set_ylim([np.nanmin(matData)*0.95,np.nanmax(matData)*1.05])
        #print(np.nanmin(cityDataFrame.index))
        #print(np.nanmax(cityDataFrame.index))
        ax[1].set_xlim([cityDataFrame.index.min(),cityDataFrame.index.max()])
        ax[1].xaxis.set_major_locator(mdates.MonthLocator(interval=1))
        # set formatter
        if criteria!=None:
            ax[1].axhline(y=criteria, color='gray', linestyle='--',linewidth=0.5,
                          label='Air quality standard')
        ax[1].xaxis.set_major_formatter(mdates.DateFormatter('%d-%m-%Y'))
        for label in ax[1].get_xticklabels(which='major'):
            label.set(rotation=30, horizontalalignment='right')
        ax[1].legend(prop={'size': 6})
        ax[1].set_ylabel(cityArea['NM_MUN'].to_string(index=False)+'\n'+legend,fontsize=6)
        fig.tight_layout()
        fig.savefig(folder+'/cityTimeSeries_'+pol+'_'+aveTime+'.png', format="png",
                   bbox_inches='tight')
    return matData.shape

def spatialEmissFig(data,xlon,ylat,legend,cmap,borderShape,folder,pol,emissType):
    fig, ax = plt.subplots()
    cm = 1/2.54  # centimeters in inches
    fig.set_size_inches(15*cm, 10*cm)
    #cmap = plt.get_cmap(cmap, 6)
    #cmap.set_under('white')
    # cmap.set_over('red')
    print(str(data.min())+'--'+str(data.max()))
    bounds = np.array([np.percentile(data[data>0],1),
                       np.percentile(data[data>0],5),
                       np.percentile(data[data>0],10),
                        np.percentile(data[data>0],25),
                        np.percentile(data[data>0],50),
                        np.percentile(data[data>0],75),
                        np.percentile(data[data>0],90),
                        np.percentile(data[data>0],95),
                        np.percentile(data[data>0],99),
                        np.percentile(data[data>0],100)])
    norm = mpl.colors.BoundaryNorm(bounds, cmap.N)
    #bounds=np.linspace(np.nanmax(data)*0.05,np.nanmax(data),num=5)
    heatmap = ax.pcolor(xlon,ylat,data,cmap=cmap,norm=norm)
    cbar = fig.colorbar(heatmap,fraction=0.04, pad=0.02,
                        #extend='both',
                        ticks=bounds,
                        spacing='uniform',
                        orientation='horizontal',
                        norm=norm,
                        ax=ax)

    cbar.ax.tick_params(rotation=30)
    #tick_locator = mpl.ticker.MaxNLocator(nbins=5)
    #cbar.locator = tick_locator
    #cbar.ax.set_xscale('log')
    #cbar.update_ticks()
    #cbar.ax.locator_params(axis='both',nbins=5)
    cbar.ax.set_xlabel(legend, rotation=0,fontsize=6)
    cbar.ax.get_xaxis().labelpad = 2
    cbar.ax.tick_params(labelsize=6)
    cbar.ax.minorticks_off() 

    br = gpd.read_file(borderShape)
    br.boundary.plot(edgecolor='black',linewidth=0.5,ax=ax)
    ax.set_xlim([xlon.min(), xlon.max()])
    ax.set_ylim([ylat.min(), ylat.max()]) 
    ax.set_xticks([])
    ax.set_yticks([])
    fig.tight_layout()
    fig.savefig(folder+'/spatialEmissFig_'+pol+'_'+emissType+'.png',
                format="png",bbox_inches='tight')
    return fig

def spatialMeteoFig(data,xlon,ylat,legend,cmap,borderShape,folder,pol,emissType):
    fig, ax = plt.subplots()
    cm = 1/2.54  # centimeters in inches
    fig.set_size_inches(15*cm, 10*cm)
    cmap = plt.get_cmap(cmap, 6)
    #cmap.set_under('white')
    bounds = np.array([np.percentile(data[data>0],1),
                       np.percentile(data[data>0],5),
                       np.percentile(data[data>0],10),
                        np.percentile(data[data>0],25),
                        np.percentile(data[data>0],50),
                        np.percentile(data[data>0],75),
                        np.percentile(data[data>0],90),
                        np.percentile(data[data>0],95),
                        np.percentile(data[data>0],99),
                        np.percentile(data[data>0],100)])
    norm = mpl.colors.BoundaryNorm(bounds, cmap.N)
    heatmap = ax.pcolor(xlon,ylat,data,cmap=cmap,norm=norm)
    cbar = fig.colorbar(heatmap,fraction=0.04, pad=0.02,
                        ticks=bounds,
                        #extend='both',
                        spacing='uniform',
                        orientation='horizontal',
                        norm=norm,
                        ax=ax)

    cbar.ax.tick_params(rotation=30)
    #tick_locator = mpl.ticker.MaxNLocator(nbins=5)
    #cbar.locator = tick_locator
    #cbar.ax.set_xscale('log')
    #cbar.update_ticks()
    #cbar.ax.locator_params(axis='both',nbins=5)
    cbar.ax.set_xlabel(legend, rotation=0,fontsize=6)
    cbar.ax.get_xaxis().labelpad = 2
    cbar.ax.tick_params(labelsize=6)
    cbar.ax.minorticks_off() 

    br = gpd.read_file(borderShape)
    br.boundary.plot(edgecolor='black',linewidth=0.5,ax=ax)
    ax.set_xlim([xlon.min(), xlon.max()])
    ax.set_ylim([ylat.min(), ylat.max()]) 
    ax.set_xticks([])
    ax.set_yticks([])
    fig.tight_layout()
    fig.savefig(folder+'/spatialEmissFig_'+pol+'_'+emissType+'.png',
                format="png",bbox_inches='tight')
    return fig


def spatialWindFig(data,U10,V10,xlon,ylat,legend,cmap,borderShape,folder,pol,emissType):
    fig, ax = plt.subplots()
    cm = 1/2.54  # centimeters in inches
    fig.set_size_inches(15*cm, 10*cm)
    cmap = plt.get_cmap(cmap, 6)
    #cmap.set_under('white')
    # cmap.set_over('red')
    bounds = np.array([np.percentile(data[data>0],1),
                       np.percentile(data[data>0],5),
                       np.percentile(data[data>0],10),
                        np.percentile(data[data>0],25),
                        np.percentile(data[data>0],50),
                        np.percentile(data[data>0],75),
                        np.percentile(data[data>0],90),
                        np.percentile(data[data>0],95),
                        np.percentile(data[data>0],99),
                        np.percentile(data[data>0],100)])
    norm = mpl.colors.BoundaryNorm(bounds, cmap.N)
    heatmap = ax.pcolor(xlon,ylat,data,cmap=cmap,norm=norm)
    cbar = fig.colorbar(heatmap,fraction=0.04, pad=0.02,
                        #extend='both',
                        ticks=bounds,
                        spacing='uniform',
                        orientation='horizontal',
                        norm=norm,
                        ax=ax)
    
    cbar.ax.tick_params(rotation=30)
    #tick_locator = mpl.ticker.MaxNLocator(nbins=5)
    #cbar.locator = tick_locator
    #cbar.ax.set_xscale('log')
    #cbar.update_ticks()
    #cbar.ax.locator_params(axis='both',nbins=5)
    cbar.ax.set_xlabel(legend, rotation=0,fontsize=6)
    cbar.ax.get_xaxis().labelpad = 2
    cbar.ax.tick_params(labelsize=6)
    cbar.ax.minorticks_off() 
    br = gpd.read_file(borderShape)
    br.boundary.plot(edgecolor='black',linewidth=0.5,ax=ax)
    heatmap1 = ax.quiver(xlon[::10,::10],ylat[::10,::10],
                        U10[::10,::10],V10[::10,::10],
                        data[::10,::10],cmap='Greys',
                      minshaft=1,clim=(0,6))
    ax.set_xlim([xlon.min(), xlon.max()])
    ax.set_ylim([ylat.min(), ylat.max()]) 
    ax.set_xticks([])
    ax.set_yticks([])
    
    fig.tight_layout()
    fig.savefig(folder+'/spatialEmissFig_'+pol+'_'+emissType+'.png',
                format="png",bbox_inches='tight')
    return fig