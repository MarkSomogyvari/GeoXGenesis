#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 17 16:29:30 2018

@author: psakicki
"""

from megalib import *

import geoclass as gcls
import geodetik as geok
import numpy as np
import os
import matplotlib.pyplot as plt
import datetime
import platform
import mds

if platform.node() == 'TPX1-GFZ':
    pp = "/home/psakicki/GFZ_WORK/PROJECTS_OTHERS/1810_GeoX_Autumn_School/1810_CHALLANGE/DATA/MGEX_orbits_small_2_tree_kept/wk1990"
    os.chdir(pp)
    



p1="../../MGEX_orbits_small_2_tree_kept/wk1990/com19902.sp3"
p2="../../MGEX_orbits_small_2_tree_kept/wk1990/grm19902.sp3"
p3="../../MGEX_orbits_small_2_tree_kept/wk1990/igs19902.sp3"
p4="../../MGEX_orbits_small_2_tree_kept/wk1990/gbm19902.sp3"
p5="../../MGEX_orbits_small_2_tree_kept/wk1990/igr19902.sp3"
p6="../../MGEX_orbits_small_2_tree_kept/wk1990/wum19902.sp3"


COM_data = gcls.read_sp3(p1)
GRM_data = gcls.read_sp3(p2)
IGS_data = gcls.read_sp3(p3)
GBM_data = gcls.read_sp3(p4)
IGR_data = gcls.read_sp3(p5)
#WUM_data = gcls.read_sp3(p6)


COM_data.sort_values(by=["epoch","sat"],inplace=True)
GRM_data.sort_values(by=["epoch","sat"],inplace=True)
IGS_data.sort_values(by=["epoch","sat"],inplace=True)
GBM_data.sort_values(by=["epoch","sat"],inplace=True)
IGR_data.sort_values(by=["epoch","sat"],inplace=True)

def AC_equiv_vals(AC1,AC2):
    ### 1) Merge the 2 DF to find common lines
    ACmerged = pd.merge(AC1 , AC2 , how='inner', on=['epoch', 'sat'])
    ### 2) Extract merged epoch & sv
    common_epoch = ACmerged["epoch"]
    common_sat   = ACmerged["sat"]
    ### 3) Create a boolean line based on common epoch / sv
    common_sat_epoch_AC1 = (AC1["epoch"].isin(common_epoch)) & (AC1["sat"].isin(common_sat))
    common_sat_epoch_AC2 = (AC2["epoch"].isin(common_epoch)) & (AC2["sat"].isin(common_sat))
    ### 4) Get epoch and sv in the combined sol which correspond to the SP3
    AC1new = AC1[common_sat_epoch_AC1].copy()
    AC2new = AC2[common_sat_epoch_AC2].copy()
    ### 5) A sort to compare the same things
    AC1new.sort_values(by=['sat','sv'],inplace=True)
    AC2new.sort_values(by=['sat','sv'],inplace=True)
    
    ### Check for > 99999 vals
    AC1_bad_bool = (AC1new["x"] > 9999) & (AC1new["y"] > 9999) & (AC1new["z"] > 9999)
    AC1_bad_bool = np.logical_not(np.array(AC1_bad_bool))

    AC2_bad_bool = (AC2new["x"] > 9999) & (AC2new["y"] > 9999) & (AC2new["z"] > 9999)
    AC2_bad_bool = np.logical_not(np.array(AC2_bad_bool))

    AC12_bad_bool = np.array(np.logical_and(AC1_bad_bool , AC2_bad_bool))

    AC1_ok = AC1new[AC12_bad_bool]
    AC2_ok = AC2new[AC12_bad_bool]
    
    return AC1_ok , AC2_ok


DC_DF_list = [COM_data,GRM_data,IGS_data,GBM_data,IGR_data]
DC_names   = ["COM","GRM","IGS","GBM","IGR"]

n_AC = 5#len(DC_DF_list)
distance   = np.zeros([n_AC,n_AC])
good_ratio = np.zeros([n_AC,n_AC])

for (i_AC1 , i_AC2) in itertools.permutations(range(n_AC),2):
    AC1 = DC_DF_list[i_AC1]
    AC2 = DC_DF_list[i_AC2]
    print(DC_names[i_AC1],DC_names[i_AC2])
    
    AC1_ok , AC2_ok = AC_equiv_vals(AC1,AC2)
        
    difference = np.nanmean(np.abs(AC1_ok["x"].values - AC2_ok["x"].values))
    
    distance[i_AC1,i_AC2]   = difference
    #good_ratio[i_AC1,i_AC2] = np.sum(AC12_bad_bool) / len(AC12_bad_bool)

#MC enriching data
rate = 100
#distance_rich = np.zeros([len(distance),len(distance)])
#np.random.seed(1)
#distance_rich1 = np.hstack([np.ones([rate,rate])*distance[0,0],np.ones([rate,rate])*distance[0,1],np.ones([rate,rate])*distance[0,2]])
#distance_rich2 = np.hstack([np.ones([rate,rate])*distance[1,0],np.ones([rate,rate])*distance[1,1],np.ones([rate,rate])*distance[1,2]])
#distance_rich3 = np.hstack([np.ones([rate,rate])*distance[2,0],np.ones([rate,rate])*distance[2,1],np.ones([rate,rate])*distance[2,2]])
#distance_rich = np.vstack([distance_rich1,distance_rich2,distance_rich3])+np.random.normal(0,10**-5,[len(distance)*rate,len(distance)*rate])
#np.fill_diagonal(distance_rich, 0)

[Y,e] = mds.cmdscale(distance*1000)   

plt.scatter(Y[:,0],Y[:,1])
xlim()       