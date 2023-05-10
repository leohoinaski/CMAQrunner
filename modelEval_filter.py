#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May  3 15:08:54 2023

@author: leohoinaski
"""
import numpy as np
import pandas as pd

def fixObs(obs):
    # if obs.shape[1]>1:
    #     obs=obs[:,0]
    nobs = obs[~np.isnan(obs)].shape[0]
    meanObs = np.nanmean(obs)
    stdObs = np.nanstd(obs)
    
    check=np.zeros(obs.shape)
    for ii,val in enumerate(obs):
        if ii<obs.shape[0]-1:
            if obs[ii+1]==val:
                check[ii] = 1
                
    checkObs = np.nansum(check)
    
    
    #bolObs = (obs>(meanObs+4*stdObs)) | (obs<(meanObs-4*stdObs)) | (check==1)
    bolObs = (obs>(meanObs+4*stdObs)) | (obs<(meanObs-4*stdObs)) 
    
    statsOut = np.array([nobs,meanObs,stdObs,checkObs,bolObs.sum(),
                         bolObs.sum()/nobs])
    statsOut = pd.DataFrame(statsOut).transpose()
    statsOut.columns = ["Nobs", "meanObs", "stdObs","equalInSeq","data2remove","aceptData_Proportion"]
    
    return bolObs,statsOut