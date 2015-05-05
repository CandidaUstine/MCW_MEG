# -*- coding: utf-8 -*-
"""
Created on Tue Apr 28 15:05:29 2015

@author: custine
Usage: python preProc_avg_singleWord.py subjID type
Example: python preProc_avg_singleWord.py 9511 run/ssp
"""

import sys
import os 
import os.path

def mnepy_avg_allw(subjID): #, sessID, eve, ssp_type):
    import mne
    from mne import fiff
    from mne import viz
    from mne.viz import evoked
    import argparse
    import condCodes as cc
    import copy
    import numpy as np
    from scipy import io
    import readTable
    
    #######Get Input ##
    print subjID
    eve = 'Word'
    runSuffix = '_raw.fif'
    
    ########Analysis Parameters##
    ###Event file suffix 
    eveSuffix = '-Triggers.eve' 
    eve_file = eve + eveSuffix #eve + eveSuffix 
    print "You have chosen the event file " + eve_file
    
    ###Projection and Average Reference and Filtering
    projVal = True
    avgRefVal = False
    hp_cutoff = 0.7
    lp_cutoff = 50 
    #######Experiment specific parameters 
    ###EventLabels and Runs
#    runs = cc.runDict[eve] ##TESTING################################################
#    print runs
    runs = ['run', 'run2', 'run3', 'run4', 'run5', 'run6', 'run7', 'run8', 'run9', 'run10', 'run11', 'run12'] #'run1', 'run2'] #
    sess = ['s5', 's6', 's7', 's8']
    labelList = cc.condLabels[eve]
    event_id = {}
    condName = {}
    for row in labelList:
        event_id[row[1]] = int(row[0])
        condName[row[1]] = row[1]
    print event_id 
    ###TimeWindow
    tmin = -.1
    tmax = float(cc.epMax[eve])
    tmax = 0.6
#    tmax = 3.00 #4Words Category 
    ########Artifact rejection parameters
    ###General
    gradRej = 4000e-13
    magRej = 4000e-12
    magFlat = 1e-14
    gradFlat = 1000e-15
    ####################################
    ######Compute averages for each run 
    evoked=[]
    evokedRuns =[]
    epochsRuns =[]

    
    
    for sessID in sess:
        raw_data_path = '/home/custine/MEG/data/krns_kr3/' +subjID+'/'+sessID
        data_path = '/home/custine/MEG/data/krns_kr3/' +subjID+'/'+sessID
        for runID in runs:
                print runID
                ##Setup Subject Speciifc Information
                event_file = data_path + '/eve/triggers/' + subjID + '_'+ sessID +'_'+runID +'_' + eve_file
                print event_file
                test_file = data_path + '/eve/triggers/' + subjID + '_'+ sessID +'_'+runID + '-epochs.mat'
                
                raw_file = raw_data_path + '/' + subjID + '_' + sessID+ '_' + runID + runSuffix ##Change this suffix if you are using SSP ##_clean_ecg_
                avgLog_file = data_path + '/ave_projon/logs/' +subjID + '_' + sessID+ '_'+runID + '_'+eve+'_' + ssp_type +'-ave.log'
                print raw_file, avgLog_file
            
                ##Setup Reading fiff data structure
                print 'Reading Raw data... '
                raw = fiff.Raw(raw_file, preload = True)
                events = mne.read_events(event_file)
#                print events
#            
#            mne.set_log_file(fname = avgLog_file, overwrite = True)
#            
#            ##Filter raw data 
#            fiff.Raw.filter(raw, l_freq = hp_cutoff, h_freq = lp_cutoff)
#            
                ##Pick all channels 
                picks = []
                for i in range(raw.info['nchan']):
                    picks.append(i)
#
                ## #Read Epochs and compute Evoked :) 
                event_id = 45
                print 'Reading Epochs from evoked raw file...'
                epochs = mne.Epochs(raw, events, event_id, tmin, tmax, baseline = (-0.1,0),preload = True,reject=dict(mag=magRej, grad=gradRej))
                print epochs
                epochsRuns = copy.deepcopy(epochs)
                epochs_data = epochs.get_data()
                
                print epochs_data.shape
                print test_file
                io.savemat(test_file, dict(epochs_data = epochs_data), oned_as = 'row')
                    

if __name__ == "__main__":
    ####### Get Input ########
    subjID = sys.argv[1]

    print 
    print "Subject ID:" + subjID
    
    
    mnepy_avg_allw(subjID)













