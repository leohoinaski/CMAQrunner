# -*- coding: utf-8 -*-
"""
Created on Tue Apr 25 14:49:59 2023

@author: Leonardo.Hoinaski
"""

import pandas as pd
import numpy as np
import numpy.matlib
import scipy.stats
#import matplotlib.pyplot as plt
import os 
from shapely import wkt
import geopandas as gpd
import matplotlib as mpl
import modelEval_figs as mefigs
import modelEval_filter as mefil


rootfolder = '/media/leohoinaski/Backup/AQD/'
shpFolder = '/media/leohoinaski/Backup/shapefiles'


#Leo#folder = 'C:/Users/Leonardo.Hoinaski/Documents/CO/CO'
#Leo#shpFolder = 'C:/Users/Leonardo.Hoinaski/Documents/EDGARanalysis/Inputs/shapefiles/estados_2010'

cmaps = [mpl.colors.LinearSegmentedColormap.from_list("", ["red","yellow","lime"]), 
         'RdBu_r',
         mpl.colors.LinearSegmentedColormap.from_list("", ["lime","yellow","red"]),
         mpl.colors.LinearSegmentedColormap.from_list("", ["lime","yellow","red"])]


NO2 = {
  "Pollutant": "$NO_{2}$",
  "Unit": '$\u03BCg.m^{-3}$',
  "conv": 1880,
  "tag":'NO2',
}

CO = {
  "Pollutant": "CO",
  "Unit": '$\u03BCg.m^{-3}$',
  "conv": 1150,
  "tag":'CO',
}

O3 = {
  "Pollutant": "$O_{3}$",
  "Unit": '$\u03BCg.m^{-3}$',
  "conv": 1960,
  "tag":'O3'
}

SO2 = {
  "Pollutant": "$SO_{2}$",
  "Unit": '$\u03BCg.m^{-3}$',
  "conv": 2620,
  "tag":'SO2'
}

PM10 = {
  "Pollutant": "$PM_{10}$",
  "Unit": '$\u03BCg.m^{-3}$',
  "conv": 1,
  "tag":'PM10',
}

PM25 = {
  "Pollutant": "$PM_{2.5}$",
  "Unit": '$\u03BCg.m^{-3}$',
  "conv": 1,
  "tag":'PM25',
}

pollutants=[O3,CO,NO2,PM10,PM25,SO2]
shape = gpd.read_file(shpFolder+'/Brasil.shp')

#%%


def modelEvaluation (model,obs):
    trueNaN = np.isnan(obs[:,0])
    obs=obs[~trueNaN,:]
    model = model.iloc[~trueNaN,:].reset_index(drop=True)
    trueNaNmodel = np.isnan(model.iloc[:,0])
    obs=obs[~trueNaNmodel,:]
    model = model[~trueNaNmodel]
    bias = np.nanmean((model)-obs,axis=0)
    spearman, pv_spearman = scipy.stats.spearmanr(model,obs[:,0],axis=0)
    spearman=spearman[-1,0:model.shape[1]]
    pv_spearman=pv_spearman[-1,0:model.shape[1]]
    idBest = spearman.argmax(axis=0)
    stats=[]
    statsAll=[]
    stats.append(bias[idBest])
    stats.append(spearman[idBest])
    stats.append(pv_spearman[idBest])
    rmse = np.sqrt(((model - obs) ** 2).mean())
    stats.append(rmse[idBest])
    mae = np.nansum(abs(model - obs),axis=0)/obs.shape[0]
    stats.append(mae[idBest])
    stats.append(model.columns[idBest])
    stats.append(obs.shape[0])
    stats = pd.DataFrame(stats).transpose()
    stats.columns = ["Bias", "Spearman", "Spearman_pval","RMSE","MAE","Pixel",'n']
    statsAll.append(bias)
    statsAll.append(spearman)
    statsAll.append(pv_spearman)
    statsAll.append(rmse)
    mae = np.nansum(abs(model - obs),axis=0)/obs.shape[0]
    statsAll.append(mae)
    statsAll.append(model.columns)
    statsAll.append(np.matlib.repmat(obs.shape[0],obs.shape[1],1))
    statsAll = pd.DataFrame(statsAll).transpose()
    statsAll.columns = ["Bias", "Spearman", "Spearman_pval","RMSE","MAE","Pixel",'n']
    return stats,statsAll


#mapping multiple parameters in subplots

    
#%%

for pol in pollutants:
    dfs = []
    statsT = pd.DataFrame()
    statsTall = pd.DataFrame()
    folder = rootfolder+pol['tag']
    files = [f for f in os.listdir(folder) if os.path.isfile(os.path.join(folder, f))]
    for file in files:
        print(file)
        data = pd.read_csv(folder+'/'+file,encoding ='latin-1')
        if data[~data['Valor'].isnull()].shape[0]/8760>0.5:
            model = data.iloc[:,data.columns.str.startswith('POINT')]*pol['conv']
            obs = data['Valor']
            bolObs,statsOut=mefil.fixObs(obs)
            obs = obs[bolObs==False]
            model=model[bolObs==False]
            if data[~data.Unidade.isnull()].reset_index().Unidade[0].replace(" ", "")=='ppm':
                print('UNIDADE EM PPM')
                print(data.Unidade[0])
                obs=obs*pol['conv']          
            if obs.shape[0]>0:
                if model.shape[1]>0:
                    obs = np.matlib.repmat(obs,model.shape[1],1).transpose()
                    stats,statsAll = modelEvaluation (model,obs)
                    stats['Station'] = file.split('.')[0]
                    statsT = pd.concat([statsT,stats])
                    statsTall = pd.concat([statsTall,stats])
                    #statsTall=  statsTall.groupby(by="Pixel").mean().reset_index()
                    statsTall = statsTall.sort_values(by='Spearman', ascending=False)
                    statsTall = statsTall.drop_duplicates(subset='Pixel', keep="first")

                    #select point with best correlation
                    point_col = stats['Pixel'].values[0]
                    point_df = model[point_col]
                    
                    #create new df with point corresponding values
                    new_df = pd.DataFrame({'Valor': obs[:, stats.index[0]]})
                    new_df[point_col] = point_df
                    dfs.append(new_df)
                    #fig = mefigs.modelScatterplot(new_df,file)
                    #fig.savefig(rootfolder+'figures/Scatter_'+pol['tag']+'_'+file+'.png')
    

                    
    statGeo = gpd.GeoDataFrame(statsTall, geometry=statsTall['Pixel'].apply(wkt.loads)).reset_index()
    statGeo.to_csv(rootfolder+'stats_'+pol['tag']+'.csv')
    statGeo['UF'] = np.nan
    for ii,stg in enumerate(statGeo.Station):
        statGeo['UF'][ii]=stg.split('_')[1][0:2]
    
    # F============ FIGURE 6 ============
    fig = mefigs.staMetrics_subplots(statGeo,['Spearman', 'Bias', 'RMSE', 'MAE'],cmaps,shape)
    fig.savefig(rootfolder+'figures/staMetrics_'+pol['tag']+'.png',dpi=300,
                bbox_inches = 'tight',pad_inches = 0)
    #mefigs.singleMetric(statGeo,shape,cmaps)
    fig = mefigs.staMetrics_boxplot(statGeo, ['Spearman', 'Bias', 'RMSE', 'MAE'],pol['Pollutant'])
    fig.savefig(rootfolder+'figures/Boxplot_'+pol['tag']+'.png',dpi=300)
    
    fig = mefigs.staMetrics_boxplotGrouped(statGeo, ['Spearman', 'Bias', 'RMSE', 'MAE'],pol['Pollutant'])
    fig.savefig(rootfolder+'figures/GroupedBoxplot_'+pol['tag']+'.png',dpi=300)

    #============== FIGURE 7 ============
    #prefixed = [filename for filename in os.listdir(folder) if filename.startswith(statGeo.Station[0])]
    #dataBest=pd.read_csv(folder+'/'+prefixed[0],encoding ='latin-1')
    #fig = mefigs.lineplotsCONC(dataBest,pol,statGeo.Pixel[0],prefixed[0])
    
    
    
    
    # for ii,df in enumerate(dfs):
    #     dfs[ii].iloc[:,0]=dfs[ii].iloc[:,0]/np.nanmean(dfs[ii].iloc[:,0]) 
    #     dfs[ii].iloc[:,1]=dfs[ii].iloc[:,1]/np.nanmean(dfs[ii].iloc[:,1]) 
    # dftotal = pd.concat(dfs, ignore_index=True)
    # mefigs.modelScatterplotTOTAL(dftotal,pol)





 
