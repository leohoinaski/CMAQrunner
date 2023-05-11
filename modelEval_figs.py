# -*- coding: utf-8 -*-
"""
Created on Tue Apr 25 14:49:59 2023

@author: Leonardo.Hoinaski
"""


import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
from scipy.stats import gaussian_kde
import scipy.stats
from mpl_toolkits.axes_grid1.inset_locator import zoomed_inset_axes
from mpl_toolkits.axes_grid1.inset_locator import mark_inset
import modelEval_filter as mefil
import matplotlib.dates as mdates
import pandas as pd



def staMetrics_subplots(df, columns, cmaps, shape):
    
    ncols = len(columns)
    cm = 1/2.54  
    fig, axs = plt.subplots(2, 2, figsize=(16*cm, 18*cm), sharex=True, sharey=True)
    fig.subplots_adjust(top = 1, bottom = 0, right = 1, left = 0, 
            hspace = 0, wspace = 0)
    axs = axs.flatten()
    if cmaps is None:
        cmaps = ['Reds'] * len(columns)    
    for i, col in enumerate(columns):
        shape.plot(ax=axs[i],color='gainsboro')
        shape.boundary.plot(ax=axs[i],color='white',linewidth=.2)
        vmin = df[col].min()
        vmax = df[col].max()
        if i==1:
            norm = mpl.colors.Normalize(vmin=vmin, vmax=abs(vmin))
        else:
            norm = mpl.colors.Normalize(vmin=vmin, vmax=vmax)
        scalar_mappable = plt.cm.ScalarMappable(norm=norm, cmap=cmaps[i])
        scalar_mappable.set_array([])
        df.plot(ax=axs[i], column=col, cmap=cmaps[i],s=4)
        #axs[i].set_title(col, fontsize=12)
        axs[i].set_axis_off()
        #fig.colorbar(scalar_mappable, ax=axs[i], shrink=0.6)
        bounds = np.around(np.linspace(vmin, vmax,5),2)
        norm = mpl.colors.BoundaryNorm(bounds, 5)
        cbar=fig.colorbar(scalar_mappable,fraction=0.02, pad=0.02,
                    orientation='horizontal',
                    ticks=bounds,
                    norm=norm,
                    ax=axs[i],
                    shrink=1, 
                    aspect=12,)
        cbar.ax.tick_params(rotation=30)
        tick_locator = mpl.ticker.MaxNLocator(nbins=5)
        cbar.locator = tick_locator
        #cbar.ax.set_xscale('log')
        #cbar.update_ticks()
        cbar.ax.set_xlabel(col, rotation=0,fontsize=8)
        cbar.ax.get_xaxis().labelpad = 2
        cbar.ax.tick_params(labelsize=8)
        #cbar.ax.locator_params(axis='both',nbins=5)
        cbar.ax.minorticks_off()
        #fig.tight_layout()
        from matplotlib import ticker
        # (generate plot here)
        tick_locator = ticker.MaxNLocator(nbins=5)
        cbar.locator = tick_locator
        cbar.update_ticks()
    return fig

def staMetrics_boxplot(df, columns,legend):
    c=['white', 'gainsboro','darkgray','grey']
    ncols = len(columns)
    fig, axs = plt.subplots(1, ncols, figsize=(6,2))
    axs = axs.flatten()
    for i, col in enumerate(columns):
        axs[i].boxplot(df[col],notch=True, patch_artist=True,
            boxprops=dict(facecolor=c[i], color='black'),
            capprops=dict(color='black'),
            whiskerprops=dict(color='black'),
            flierprops=dict(color=c[i], markeredgecolor='black',markersize=5),
            medianprops=dict(color='black'))
        axs[i].tick_params(
            axis='x',          # changes apply to the x-axis
            which='both',      # both major and minor ticks are affected
            bottom=False,      # ticks along the bottom edge are off
            top=False,         # ticks along the top edge are off
            labelbottom=False) # labels along the bottom edge are off
        
        axs[i].set_ylabel(col+' - '+legend, fontsize=8)
        #axs[i].set_axis_off()
        fig.tight_layout()
        axs[i].xaxis.set_tick_params(labelsize=8)
        axs[i].yaxis.set_tick_params(labelsize=8)
    fig.tight_layout()
        
    return fig


def modelScatterplot(new_df,file):
    #Scatterplots
    #select range os stations
    fig, ax = plt.subplots(figsize=(4,4))
    
    xy = np.vstack([new_df.iloc[:,0],new_df.iloc[:,1]])
    new_df = new_df.iloc[~np.any(np.isnan(xy), axis=0).transpose(),:]
    xy = xy[:,~np.any(np.isnan(xy), axis=0)]
    z = gaussian_kde(xy)(xy)
    new_df = new_df.iloc[~np.any(np.isnan(xy), axis=0).transpose(),:]
    ax.scatter(new_df.iloc[:,0],new_df.iloc[:,1],c=z,s=15,alpha=.5)
    
    ###calculate Spearman correlation using new_df
    corr, p_value = scipy.stats.spearmanr(new_df.iloc[:,0], new_df.iloc[:,1])
   
    ###insert text with Spearman correlation
    ax.annotate('ρ = {:.2f}'.format(corr), 
            xy=(0.70, 0.9), xycoords='axes fraction', 
            fontsize=8, ha='left', va='center')
    
    
    ax.set_xlabel('Observation\n'+file.split('.')[0],fontsize=9)
    ax.set_ylabel('CMAQ',fontsize=9)
    ax.xaxis.set_tick_params(labelsize=8)
    ax.yaxis.set_tick_params(labelsize=8)
    ax.set_xlim([new_df.min().min(),new_df.max().max()])
    ax.set_ylim([new_df.min().min(),new_df.max().max()])
    ax.set_aspect('equal')
    ax.plot([new_df.min().min(), new_df.max().max()],
             [new_df.min().min(), new_df.max().max()], 'k-', lw=1,dashes=[2, 2])
    ax.fill_between(np.linspace(new_df.min().min(),new_df.max().max(),new_df.shape[0]), 
                    np.linspace(new_df.min().min(),new_df.max().max(),new_df.shape[0])*0.5,
                    alpha=0.2,facecolor='gray',edgecolor=None)
    ax.fill_between(np.linspace(new_df.min().min(),new_df.max().max(),new_df.shape[0]),
                    np.linspace(new_df.max().max(),new_df.max().max(),new_df.shape[0]),
                    np.linspace(new_df.min().min(),new_df.max().max(),new_df.shape[0])*2,
                    alpha=0.2,facecolor='gray',edgecolor=None)
    fig.tight_layout()
    #ax.set_yscale('log')
    #ax.set_xscale('log')
    return fig
    
    
def lineplotsCONC(dataBest,pol,Pixel,station):
    #%%
    trueNaN = dataBest['Valor'].isnull()
    cm = 1/2.54
    fig, ax = plt.subplots(3,1,figsize=(9.5*cm, 20*cm))
    ax = ax.flatten()
    tt = station.split(".")[-2].split('_')[-1]
    model = dataBest.iloc[:,dataBest.columns.str.startswith('POINT')]*pol['conv']
    obs = dataBest['Valor']
    bolObs,statsOut=mefil.fixObs(obs)
    obs = obs[bolObs==False]
    model=model[bolObs==False]
    date=dataBest.Datetime[bolObs==False]
    
    date = pd.DataFrame(date)
    model['Datetime']= pd.to_datetime(date['Datetime'], format='%Y-%m-%d %H:%M:%S')
    model['OBS'] = obs
    model = model.sort_values('Datetime')
    ax[2].plot(model['Datetime'],model.iloc[:,model.columns==Pixel],color='red',
            linewidth=.3,label='Model',alpha=0.8)
    ax[2].annotate('c) Raw data at '+ tt, 
            xy=(0.05, 0.90), xycoords='axes fraction', 
            fontsize=8, ha='left', va='center')
    ax[2].fill_between(model['Datetime'], np.min(model.iloc[:,model.columns.str.startswith('POINT')], axis=1),
                    np.max(model.iloc[:,model.columns.str.startswith('POINT')], axis=1),
                    alpha=0.3,facecolor='red',edgecolor=None)
    ax[2].scatter(model['Datetime'],model['OBS'], c='gray',s=1,
                  edgecolors='black',label='Observations')
    ax[2].xaxis.set_major_formatter(mdates.DateFormatter('%d-%b'))
    ax[2].xaxis.set_major_locator(mdates.MonthLocator(interval=1))
    #ax.set_xlabel('Time',fontsize=10)
    ax[2].set_ylabel(pol['Pollutant']+' ('+pol['Unit']+')',fontsize=8)
    ax[2].set_xlim([model['Datetime'].min(), model['Datetime'].max()])
    ax[2].set_ylim([0,np.max([model.iloc[:,-3].max(), model['OBS'].max()])*1.4])
    ax[2].xaxis.set_tick_params(labelsize=8)
    ax[2].yaxis.set_tick_params(labelsize=8)
    ob = model['OBS'][~trueNaN]
    md=model.iloc[:,model.columns.str.startswith('POINT')][~trueNaN]*pol['conv']
    trueNaN2 = np.isnan(md.iloc[:,0])
    corr, p_value = scipy.stats.spearmanr(ob[~trueNaN2],md[~trueNaN2])
    best = np.nanargmax(corr[1:-1,0])
    
    ###insert text with Spearman correlation
    # ax.annotate(tt,
    #         xy=(0.77, 0.95), xycoords='axes fraction', 
    #         fontsize=8, ha='left', va='center')
    ax[2].annotate('ρ = {:.2f}'.format(corr[1:-1,0].max()), 
            xy=(0.55, 0.90), xycoords='axes fraction', 
            fontsize=8, ha='left', va='center')
    ax[2].annotate('Bias = {:.2f}'.format(np.nanmean(model.iloc[:,best]-model['OBS']))+' '+pol['Unit'], 
            xy=(0.55, 0.80), xycoords='axes fraction', 
            fontsize=8, ha='left', va='center')
    for label in ax[2].get_xticklabels(which='major'):
        label.set(rotation=30, horizontalalignment='right')
        
    # ----------------------------MONTHLY--------------------------------
    model['month'] = pd.to_datetime(model['Datetime'].dt.month, format='%m')
    mm = model.groupby(['month']).mean()
    mm0 = model.groupby(['month']).quantile(0.25)
    mm2 = model.groupby(['month']).quantile(0.75)
    ax[0].annotate('a) Montly average', 
            xy=(0.05, 0.90), xycoords='axes fraction', 
            fontsize=8, ha='left', va='center')
    ax[0].plot(mm.index,mm.iloc[:,mm.columns==Pixel],color='red',
            linewidth=.3,label='Model')
    ax[0].fill_between(mm.index, np.min(mm.iloc[:,mm.columns.str.startswith('POINT')], axis=1),
                    np.max(mm.iloc[:,mm.columns.str.startswith('POINT')], axis=1),
                    alpha=0.3,facecolor='red',edgecolor=None)
    ax[0].fill_between(mm.index, mm0['OBS'],mm2['OBS'], 
                    alpha=0.3,facecolor='gray',edgecolor=None)
    ax[0].scatter(mm.index,mm['OBS'], c='gray',s=1,edgecolors='black',
                  label='Observations')
    myFmt = mdates.DateFormatter('%b')
    ax[0].xaxis.set_major_formatter(myFmt)
    #ax.set_xlabel('Time',fontsize=10)
    ax[0].set_ylabel(pol['Pollutant']+' ('+pol['Unit']+')',fontsize=8)
    ax[0].set_xlim([mm.index.min(), mm.index.max()])
    ax[0].set_ylim([0,mm.max().max()*1.4])
    ax[0].xaxis.set_tick_params(labelsize=8)
    ax[0].yaxis.set_tick_params(labelsize=8)
    ax[0].legend(fontsize=8,frameon=False,loc='upper right')
    #----------------------HOURLY--------------------------------
    model['hour'] = pd.to_datetime(model['Datetime'].dt.hour, format='%H')
    mm0 = model.groupby(['hour']).quantile(0.25)
    mm2 = model.groupby(['hour']).quantile(0.75)
    mm = model.groupby(['hour']).mean()
    ax[1].annotate('b) Hourly average', 
            xy=(0.05, 0.90), xycoords='axes fraction', 
            fontsize=8, ha='left', va='center')
    ax[1].plot(mm.index,mm.iloc[:,mm.columns==Pixel],color='red',
            linewidth=.3,label='Model')
    ax[1].fill_between(mm.index, np.min(mm.iloc[:,mm.columns.str.startswith('POINT')], axis=1),
                    np.max(mm.iloc[:,mm.columns.str.startswith('POINT')], axis=1),
                    alpha=0.3,facecolor='red',edgecolor=None)
    ax[1].fill_between(mm.index, mm0['OBS'],mm2['OBS'], 
                    alpha=0.3,facecolor='gray',edgecolor=None)
    ax[1].scatter(mm.index,mm['OBS'], c='gray',s=1,edgecolors='black',label='Observations')
    myFmt = mdates.DateFormatter('%H:00')
    ax[1].xaxis.set_major_formatter(myFmt)
    #ax.set_xlabel('Time',fontsize=10)
    ax[1].set_ylabel(pol['Pollutant']+' ('+pol['Unit']+')',fontsize=8)
    ax[1].set_xlim([mm.index.min(), mm.index.max()])
    ax[1].set_ylim([0,mm.max().max()*1.4])
    ax[1].xaxis.set_tick_params(labelsize=8)
    ax[1].yaxis.set_tick_params(labelsize=8)
    fig.tight_layout()
    #%%
    
    return fig
    
#%%
#mapping single parameter with manual norm and cbar
def singleMetric(statGeo,shape,cmaps):
    fig, ax = plt.subplots(figsize=(7,7))
    fig.subplots_adjust(left=0.1, right=1, top=0.2, bottom=0.1)
    shape.plot(ax=ax,color='gainsboro')
    shape.boundary.plot(ax=ax,color='white',linewidth=.3)
    norm = mpl.colors.Normalize(vmin=np.min(statGeo.Spearman),vmax=np.max(statGeo.Spearman))
    cbar = plt.cm.ScalarMappable(norm=norm, cmap=cmaps[0])
    statGeo.plot(ax=ax,column='Spearman',cmap=cmaps[0],s=8) #select column parameter
    plt.axis(False)
    figBar = ax.get_figure()
    cax = fig.add_axes([0.3, 0.24, 0.012, 0.2])
    sm = plt.cm.ScalarMappable(cmap=plt.cm.get_cmap(cmaps[0], 5), norm = norm)
    cb = figBar.colorbar(sm,cax=cax,orientation='vertical', 
                         ticks = np.linspace(np.min(statGeo.Spearman),
                                             np.max(statGeo.Spearman),5),format="%.2f")
    cax.tick_params(axis='both', which = 'major', labelsize=8, 
                    color='k', length=0, pad=3, labelcolor='k')
    cb.ax.set_title('Spearman\nRank', fontsize=8, pad=6, color='k')
    cb.ax.tick_params(size=0)
    cb.outline.set_visible(False)
    ax.margins(.1, .5) 
    axins = zoomed_inset_axes(ax, 3,loc='lower right', bbox_to_anchor=(700,150), 
                              borderpad=1 ) # zoom = 6
    shape.plot(ax=axins,color='gainsboro')
    shape.boundary.plot(ax=axins,color='white',linewidth=.3)
    statGeo.plot(ax=axins,column='Spearman',cmap=cmaps[0],s=8) 
    # sub region of the original image
    axins.set_xlim(-48, -40)
    axins.set_ylim(-24, -19)
    plt.xticks(visible=False)
    plt.yticks(visible=False)
    axins.tick_params(
        axis='x',          # changes apply to the x-axis
        which='both',      # both major and minor ticks are affected
        bottom=False,      # ticks along the bottom edge are off
        top=False,         # ticks along the top edge are off
        labelbottom=False)
    axins.tick_params(
        axis='y',          # changes apply to the x-axis
        which='both',      # both major and minor ticks are affected
        bottom=False,      # ticks along the bottom edge are off
        top=False,         # ticks along the top edge are off
        labelbottom=False) 
    #axins.axis('off')
    # draw a bbox of the region of the inset axes in the parent axes and
    # connecting lines between the bbox and the inset axes area
    mark_inset(ax, axins, loc1=1, loc2=3, fc="none", ec="0.5")
    fig.tight_layout()

#%%
def modelScatterplotTOTAL(new_df,pol):
    #Scatterplots
    #select range os stations
    fig, ax = plt.subplots(figsize=(4,4))
    
    
    xy = np.vstack([new_df.iloc[:,0],new_df.iloc[:,1]])
    new_df = new_df.iloc[~np.any(np.isnan(xy), axis=0).transpose(),:]
    xy = xy[:,~np.any(np.isnan(xy), axis=0)]
    z = gaussian_kde(xy)(xy)
    new_df = new_df.iloc[~np.any(np.isnan(xy), axis=0).transpose(),:]
    ax.scatter(new_df.iloc[:,0],new_df.iloc[:,1],c=z,s=15,alpha=.5)
    
    ###calculate Spearman correlation using new_df
    corr, p_value = scipy.stats.spearmanr(new_df.iloc[:,0], new_df.iloc[:,1])
   
    ###insert text with Spearman correlation
    ax.annotate('ρ = {:.2f}'.format(corr), 
            xy=(0.05, 0.85), xycoords='axes fraction', 
            fontsize=8, ha='left', va='center')
    
    
    ax.set_xlabel('Observation\n'+pol['tag']+ ' ('+pol['Unit']+')' ,fontsize=9)
    ax.set_ylabel('CMAQ',fontsize=9)
    ax.xaxis.set_tick_params(labelsize=8)
    ax.yaxis.set_tick_params(labelsize=8)
    ax.set_xlim([new_df.min().min(),new_df.max().max()])
    ax.set_ylim([new_df.min().min(),new_df.max().max()])
    ax.set_aspect('equal')
    ax.plot([new_df.min().min(), new_df.max().max()],
             [new_df.min().min(), new_df.max().max()], 'k-', lw=1,dashes=[2, 2])
    ax.fill_between(np.linspace(new_df.min().min(),new_df.max().max(),new_df.shape[0]), 
                    np.linspace(new_df.min().min(),new_df.max().max(),new_df.shape[0])*0.5,
                    alpha=0.2,facecolor='gray',edgecolor=None)
    ax.fill_between(np.linspace(new_df.min().min(),new_df.max().max(),new_df.shape[0]),
                    np.linspace(new_df.max().max(),new_df.max().max(),new_df.shape[0]),
                    np.linspace(new_df.min().min(),new_df.max().max(),new_df.shape[0])*2,
                    alpha=0.2,facecolor='gray',edgecolor=None)
    fig.tight_layout()
    #ax.set_yscale('log')
    #ax.set_xscale('log')