
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 13 16:59:34 2014

@author: custine
Usage: python preProc_avg.py subjID sessID eve
Example: python preProc_avg.py 9511 s1 Word/AllItems/Noun/Verb/Noun_People/Sentence4W
"""

import sys
import os 
import os.path

def mnepy_avg(subjID, sessID, eve, ssp_type):
    import mne
    from mne import fiff
    from mne import viz
    from mne.viz import evoked
    import argparse
    import condCodes as cc
    import copy
    import numpy
    
    #######Get Input ##
    print subjID
    print sessID
    print eve
    data_path = '/home/custine/MEG/data/krns_kr3/' +subjID+'/'+sessID
    if ssp_type == 'run':
        raw_data_path = '/home/custine/MEG/data/krns_kr3/' +subjID+'/'+sessID
        runSuffix = '_raw.fif'
    elif ssp_type == 'ecg' or ssp_type == 'eog':
        raw_data_path = '/home/custine/MEG/data/krns_kr3/' +subjID+'/'+sessID + '/ssp/mne'
        runSuffix = '_clean_' + ssp_type + '_raw.fif'
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
    runs = cc.runDict[eve] ##TESTING################################################
    print runs
    labelList = cc.condLabels[eve]
    event_id = {}
    condName = {}
    for row in labelList:
        event_id[row[1]] = int(row[0])
        condName[row[1]] = row[1]
    print event_id 
    ###TimeWindow
    tmin = -.5
    tmax = float(cc.epMax[eve])
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
    for runID in runs:
            print runID
            ##Setup Subject Speciifc Information
            
            event_file = data_path + '/eve/triggers/' + subjID + '_'+ sessID +'_'+runID +'_' + eve_file
            print event_file
            
            raw_file = raw_data_path + '/' + subjID + '_' + sessID+ '_' + runID + runSuffix ##Change this suffix if you are using SSP ##_clean_ecg_
            avgLog_file = data_path + '/ave_projon/logs/' +subjID + '_' + sessID+ '_'+runID + '_'+eve+'_' + ssp_type +'-ave.log'
            print raw_file, avgLog_file
            
            ##Setup Reading fiff data structure
            print 'Reading Raw data... '
            raw = fiff.Raw(raw_file, preload = True)
            events = mne.read_events(event_file)
            print events
            
            mne.set_log_file(fname = avgLog_file, overwrite = True)
            
            ##Filter raw data 
            fiff.Raw.filter(raw, l_freq = hp_cutoff, h_freq = lp_cutoff)
            
            ##Pick all channels 
            picks = []
            for i in range(raw.info['nchan']):
                picks.append(i)
                
            ##Read Epochs and compute Evoked :) 
            print 'Reading Epochs from evoked raw file...'
            epochs = mne.Epochs(raw, events, event_id, tmin, tmax, baseline = (-0.5,0), picks = picks, proj = True, name = condName, preload = True, flat = dict(mag = magFlat, grad= gradFlat), reject=dict(mag=magRej, grad=gradRej))
            print epochs
            evoked = [epochs[cond].average(picks =picks) for cond in event_id]
#    #        epochs.plot()
            
            ##Write Evoked 
            print 'Writing Evoked data to -ave.fif file...' 
            fiff.write_evoked(data_path + '/ave_projon/' + subjID+'_' + sessID+'_'+runID+'_' + eve +'_' + ssp_type+'-ave.fif', evoked)
            evokedRuns.append(evoked)
            print 'Completed! See ave.fif result in folder', data_path + '/ave_projon/'

            ###############################################################################
            ##Show the Result - Plotting the evoked data
            #mne.viz.evoked.plot_evoked(evoked, exclude = [])
    
    print len(evokedRuns)
    
    ##Make the Final Grand average of all the runs
    runData = []
    runNave = []

    newEvoked = copy.deepcopy(evoked)
    print newEvoked
    numCond = len(newEvoked)
    print 'Length', numCond
    for c in range(numCond):
        for evRun in evokedRuns:
            runData.append(evRun[c].data)
            runNave.append(evRun[c].nave)
        print 'Jane Here', c, runNave    
        gaveData = numpy.mean(runData,0)
        gaveNave = numpy.sum(runNave)
        print 'Sum', sum(runNave)
    
        newEvoked[c].data = gaveData
        newEvoked[c].nave = gaveNave
        
#        runData = []
#        runNave = []
    print newEvoked[0].nave
    
    ##Write Grand average Evoked     
    fiff.write_evoked(data_path + '/ave_projon/'+subjID+'_' + sessID+'_' + eve +'_' + ssp_type+'_All-ave.fif', newEvoked)


if __name__ == "__main__":
    ####### Get Input ########
    subjID = sys.argv[1]
    sessID = sys.argv[2]
    Trig_type = sys.argv[3]
    ssp_type = sys.argv[4] #run or ecg or eog 
    print 
    print "Subject ID:" + subjID
    print "Sess ID:" + sessID 
    print "Asking for " + Trig_type + " Triggers..."
    
    
    mnepy_avg(subjID, sessID, Trig_type, ssp_type)
    
#    if Trig_type == "Sentence":
#       mnepy_avg(subjID, sessID)
#        
#    elif Trig_type == 'Words':
#        mnepy_avg(subjID, sessID)
#        
#    elif Trig_type == 'Category':
#        Type = sys.argv[4]
#        mnepy_avg(subjID, sessID, Trig_type, Type)












