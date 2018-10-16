#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 26 16:18:10 2017

@author: adminuser
"""

import geoclass as gcls
import os
import matplotlib.pyplot as plt

### Using P.S. plot template
if False:
    mpl_style_file = "/home/psakicki/CODES/GeoXGenesis/lib_geodezyx_toolbox_py3/misc_config/matplotlibrc_PSmod"
    plt.style.use('file://' + mpl_style_file)


### SIMPLE COMPARISON
if True:
    ## Paths of the SP3 (Orbits) files
    p1="/home/psakicki/aaa_FOURBI/wk1989/com19896.sp3"
    p2="/home/psakicki/aaa_FOURBI/wk1989/grm19896.sp3"
    ## (Optionnal) Name for each orbit (the filename will be used instead)
    name1=''
    name2=''
    
    # Save a plot and define its destination
    save_plot=True
    save_plot_dir=os.path.dirname(p1)

    RTNoutput         = True # False only for debug & personal interest !!
    convert_ECEF_ECI  = True # False only for debug !!
    clean_null_values = "any" # Can be "all" , "any", False or True (True => "all")
    save_plot_name    = "auto" # Name for the plot file. if auto : name1_name2_timestamp

    # Selection of the constellation
    sats_used_list = ["G"] # G,E,R,C ...

    #Perform the orbit comparison
    Diff_all    = gcls.compar_orbit(p1,p2,
                                    sats_used_list=sats_used_list,
                                    RTNoutput=RTNoutput,
                                    convert_ECEF_ECI=convert_ECEF_ECI,
                                    name1=name1,name2=name2,
                                    clean_null_values = clean_null_values,
                                    step_data = 900)

    # Plot the previous comparison
    _           = gcls.compar_orbit_plot(Diff_all,
                                        save_plot=save_plot,
                                        save_plot_dir=save_plot_dir,
                                        save_plot_name=save_plot_name)

    # Return a table with simple stats about the comparison (max, min, std ...)
    ComparTable = gcls.compar_orbit_table(Diff_all)

### MORE COMPLEX CASE : LOOP FOR SEARCHING SAME ORBIT NAME IN DIFFERENTS FOLDERS
if False:
    p2_dir_list = ['/home/adminuser/Documents/1709_compar_orbit/data/FINALorbs/FINALmod1',
    '/home/adminuser/Documents/1709_compar_orbit/data/FINALorbs/FINALatx1967ORI',
    '/home/adminuser/Documents/1709_compar_orbit/data/FINALorbs/FINAL',
    '/home/adminuser/Documents/1709_compar_orbit/data/FINALorbs/FINALatx1967MOD',
    '/home/adminuser/Documents/1709_compar_orbit/data/FINALorbs/FINALorig_good']

    orbnam = '/ANA/2017/2017_222/ORB/2017_222_orb_1d.sp3'

    p_ref = '/home/adminuser/Documents/1709_compar_orbit/data/FINALorbs/OFFICIAL/2017_222_orb_1d.sp3'

    for p2_dir in p2_dir_list:
        p2 = p2_dir + orbnam

        D1 = gcls.read_sp3(p_ref)
        D2 = gcls.read_sp3(p2)

        name1 = p_ref.split('/')[7]
        name2 = p2.split('/')[7]

        RTNoutput        = True # False only for debug & personal interest !!
        convert_ECEF_ECI = True # False only for debug !!

        sats_used_list = ['E'] # G,E,R,C ...

        Diff_all    = gcls.compar_orbit(p_ref,p2,
                                    sats_used_list=sats_used_list,
                                    RTNoutput=RTNoutput,
                                    convert_ECEF_ECI=convert_ECEF_ECI,
                                    name1=name1,name2=name2)


        _           = gcls.compar_orbit_plot(Diff_all)
        ComparTable = gcls.compar_orbit_table(Diff_all)
