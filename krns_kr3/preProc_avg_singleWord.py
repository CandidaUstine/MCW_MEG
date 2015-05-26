# -*- coding: utf-8 -*-
"""
Created on Tue Apr 28 15:05:29 2015
@author: custine
Usage: python preProc_avg_singleWord.py subjID
Example: python preProc_avg_singleWord.py 9511 
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
    from readTable import readTable 
    
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
    ###SessIDs and Runs
    runs = ['run1', 'run2','run3', 'run4', 'run5', 'run6', 'run7', 'run8', 'run9', 'run10', 'run11', 'run12'] #'run1', 'run2'] #
    sess = ['s5', 's6', 's7', 's8']
    ###Word TimeWindow
    tmin = -.1
    tmax = 0.6 
    ########Artifact rejection parameters
    gradRej = 4000e-13
    magRej = 4000e-12
    magFlat = 1e-14
    gradFlat = 1000e-15
    
    ####################################
    ######Compute averages for each run 
#    newArr = [0]*257
    evoked=[]
    evokedRuns =[]
    epochsRuns =[]
    newadd = np.zeros((258,325,1401))
    meanArr = np.zeros((258,325,1401))
    sumArr = np.zeros((258,325,1401))
    newlenArr = np.zeros((258,))
    
    count = 0
    (ID, word, role) = readTable('/mnt/file1/binder/KRNS/info/krns_word_list.txt')
    ID = [int(i) for i in ID]
    epochs_file = '/home/custine/MEG/data/krns_kr3/' + subjID + '/' + subjID + '_20150525_filtered_sum-epochs.mat'
    epochsMean_file = '/home/custine/MEG/data/krns_kr3/' + subjID + '/' + subjID + '_20150525_filtered_mean-epochs.mat'
    epochsLen_file = '/home/custine/MEG/data/krns_kr3/' + subjID + '/' + subjID + '_20150525_filtered_len-epochs.mat'
    print epochs_file
    
    new = np.zeros((257,325,1401)) 
    newNum = np.zeros(257)
    
    for sessID in sess:
        raw_data_path = '/home/custine/MEG/data/krns_kr3/' +subjID+'/'+sessID
        data_path = '/home/custine/MEG/data/krns_kr3/' +subjID+'/'+sessID
#        epochs_sess_file = '/home/custine/MEG/data/krns_kr3/' + subjID + '_'+ sessID + '-epochs.mat'
        for runID in runs:
                print runID                 
                count = count + 1
                print 'Count' + str(count)
                ##Setup Subject Speciifc Information
                event_file = data_path + '/eve/triggers/' + subjID + '_'+ sessID +'_'+runID +'_' + eve_file
                print event_file

                raw_file = raw_data_path + '/' + subjID + '_' + sessID+ '_' + runID + runSuffix ##Change this suffix if you are using SSP ##_clean_ecg_
                avgLog_file = data_path + '/ave_projon/logs/' +subjID + '_' + sessID+ '_'+runID + '_'+eve+'-ave.log'
            
                ##Setup Reading fiff data structure
                print 'Reading Raw data... '
                raw = fiff.Raw(raw_file, preload = True)
                events = mne.read_events(event_file)
                
    #            mne.set_log_file(fname = avgLog_file, overwrite = True)
                ##Filter raw data 
                fiff.Raw.filter(raw, l_freq = hp_cutoff, h_freq = lp_cutoff)
########################################################################                            
                ##Check if the event exists in the run else save empty mat file. 
                (x, y, run_eveID) = readTable(event_file)
#                if evid in run_eveID:
#                print "EventID exists in the run... " 
                ##Pick all channels 
                picks = []
                for i in range(raw.info['nchan']):
                    picks.append(i)
########################################################################                                    
                ##Create epochs.mat file for specified event ID 
                print 'Reading Epochs from evoked raw file...'
                epochs = mne.Epochs(raw, events,ID , tmin, tmax, baseline = (-0.1,0), preload = True,reject=dict(mag=magRej, grad=gradRej))
                print epochs.__len__
##########################################################################                
                ##Save the epochs data as a array 
                for evID,i,j in zip(ID, range(1,258), range(0,257)):## 1,258 Starts from 1 to 257 (first item is 0s but not incl in this counter) append.##258 total Items but 257 unique codes (so 0 to 256)
                    ev = i
                    lenNum = len(epochs[str(ev)].events) #Number of events in each condition. :) 
                    data = np.asarray(([epochs[str(ev)].get_data()]))
                    data = np.squeeze(data)
                    if len(data) == 0: 
                        data = np.zeros((1,325,1401)) ##'No epochs for this condition'
                    elif len(data) == 325:
                         data = np.expand_dims(data, axis = 0)
                    data = np.sum(data, axis = 0)
                    data = np.expand_dims(data, axis = 0)
#                    print data.shape ## (1, 325, 1401)
                    new[j,:,:] = new[j,:,:] + data
                    print data

                    newNum[j] = newNum[j] + lenNum
                print new.shape ##(257, 325, 1401) 257 items (used and used same item) 
                print newNum.shape

#                
#########################################################################                                
    ##Creating the mean of (individual) epochs across runs(and)sessions. 
#    print newadd[1,1,1]
    print count
    for i in range(0, 257): ##range(0,258):Starts from 0 to 257 - 258 items - same length as new and newadd. Since item93 is repeated twice - as verb and as as adj  (condition - 'used') 
        newitem = np.divide((new[i,:,:]), float(newNum[i]))
        meanArr[i] = np.expand_dims(np.array(newitem.astype(float)), axis = 0)
        print i 
    print meanArr.shape #(258, 325, 1401) with last row as zeros - can modify... 
    print meanArr[1,1,1]
         
##########################################################################    
    io.savemat(epochs_file, dict(sumArr = new), oned_as = 'row')
    io.savemat(epochsLen_file, dict(lenArr = newNum), oned_as = 'row')
    io.savemat(epochsMean_file, dict(meanArr = meanArr), oned_as = 'row')




if __name__ == "__main__":
    ####### Get Input ########
    subjID = sys.argv[1]

    print 
    print "Subject ID:" + subjID
    
    
    mnepy_avg_allw(subjID)
