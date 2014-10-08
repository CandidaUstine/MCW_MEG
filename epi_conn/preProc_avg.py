# -*- coding: utf-8 -*-
"""
Created on Fri Oct  3 11:28:29 2014

@author: custine
Usage: python preProc_avg.py subjID 
Example: python preProc_avg.py EP1 
"""

import sys
import os 
import os.path

def mnepy_avg(subjID,run):
    import mne
    from mne import fiff
    from mne import viz
    #from mne.viz import evoked
    import argparse
    import copy
    import numpy
    
    #######Get Input ##
    print subjID

    
    ########Analysis Parameters##
    ###Event file suffix 
    eveSuffix = '.eve' 
    eve_file = run + eveSuffix #eve + eveSuffix 
    print "You have chosen the event file " + eve_file
    
    ###Projection and Average Reference and Filtering
    projVal = True
    avgRefVal = False
    hp_cutoff = 0.7
    lp_cutoff = 40 
    event_id = None
    #######Experiment specific parameters 
    ###TimeWindow
    tmin = 0
    tmax = 2 ##float(cc.epMax[eve])
    ########Artifact rejection parameters
    ###General
    gradRej = 2000e-13
    magRej = 3000e-15
    magFlat = 1e-14
    gradFlat = 1000e-15
    ####################################
    #######Compute averages for each run 
 #   evoked=[]
    evokedRuns =[]
    ##Setup Subject Speciifc Information
    data_path = '/home/custine/MEG/data/epi_conn/' +subjID
    event_file = data_path + '/eve/' + eve_file
    print event_file
    
    raw_file = data_path + '/' + run +'_raw.fif' ##Change this suffix if you are using SSP 
    avgLog_file = data_path + '/logs/' +run+ '_py-ave.log'
    print raw_file, avgLog_file
#        
    ##Setup Reading fiff data structure
    print 'Reading Raw data... '
    raw = fiff.Raw(raw_file, preload = True)
    events = mne.read_events(event_file)
    #print events
    
    mne.set_log_file(fname = avgLog_file, overwrite = True)
    
    ##Filter raw data 
    fiff.Raw.filter(raw, l_freq = hp_cutoff, h_freq = lp_cutoff)
    
    #Pick all channels 
    picks = []
    for i in range(raw.info['nchan']):
        picks.append(i)
        
    ##Read Epochs and compute Evoked :) 
    print 'Reading Epochs from evoked file...'
    epochs = mne.Epochs(raw, events, event_id, tmin, tmax, baseline = (None,0), proj = True, picks = picks, preload = True, flat = dict(mag = magFlat, grad= gradFlat), reject=dict(mag=magRej, grad=gradRej))
    print epochs
    evoked = [epochs.average(picks =picks)]
    #    #        epochs.plot()
    
    ##Write Evoked 
    print 'Writing Evoked data to -ave.fif file...' 
    fiff.write_evoked(data_path + '/ave_projon/' + run +'-ave.fif', evoked)
    evokedRuns.append(evoked)
    print 'Completed! See ave.fif result in folder', data_path + '/ave_projon/'
#
##    #        ###############################################################################
##    #        #Show the Result - Plotting the evoked data
##    #        mne.viz.evoked.plot_evoked(evoked, exclude = [])
#    
    print len(evokedRuns)
    
    ##Make the Final Grand average of all the runs
    runData = []
    runNave = []

    newEvoked = copy.deepcopy(evoked)
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
        
        runData = []
        runNave = []
    
    ##Write Grand average Evoked     
    fiff.write_evoked(data_path + '/ave_projon/'+subjID+'_' +run +'_All-ave.fif', newEvoked)


if __name__ == "__main__":
    ####### Get Input ########
    subjID = sys.argv[1] #EP1
    run = sys.argv[2] #run1 
    print 
    print "Subject ID:" + subjID

    
    mnepy_avg(subjID, run)
    












