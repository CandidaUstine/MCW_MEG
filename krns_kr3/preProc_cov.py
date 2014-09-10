# -*- coding: utf-8 -*-
"""
Created on Wed Aug 27 14:52:52 2014
==============================================
Estimate covariance matrix from a raw FIF file
==============================================

Usage: python preProc_cov.py subjID sessID eve
Example: python preProc_cov.py 9511 s1 Word

"""
# Author: Alexandre Gramfort <alexandre.gramfort@telecom-paristech.fr>
#
# License: BSD (3-clause)

print(__doc__)

import mne
from mne import io
import argparse
import condCodes as cc

parser = argparse.ArgumentParser(description='Get input')
parser.add_argument('subj',type=str)
parser.add_argument('sess',type=str) ##Left, Right etc.,
parser.add_argument('eve',type=str) 
args=parser.parse_args()
subjID = args.subj
sessID = args.sess
eve = args.eve
print subjID
print sessID
print eve

###Event file suffix 
eveSuffix = '-TriggersMod.eve'
eve_file = eve + eveSuffix
print "You have chosen the event file " + eve_file 

labelList = cc.condLabels[eve]
event_id = {}
condName = {}
for row in labelList:
    event_id[row[1]] = int(row[0])
    condName[row[1]] = row[1]
print event_id

#runs = cc.runDict['Word']
runs = ['emptyroom'] #, 'run1', 'run2'] ###For other runs use the baseline and set tmin/tmax using epoched data. 
#print runs
covRuns = []
for runID in runs:
        print runID
        
        data_path = '/home/custine/MEG/data/krns_kr3/' +subjID+'/'+sessID
        fname = data_path +'/'+ subjID + '_'+ sessID +'_'+runID +'_raw.fif'
        print fname
        cname = data_path +'/cov/'+ subjID + '_'+ sessID +'_' + runID + '-cov.fif'
        covLog_file = data_path + '/cov/logs/' +subjID + '_' + sessID+ '_'+runID + '_cov.log'
        event_file = data_path + '/eve/triggers/' + subjID + '_'+ sessID +'_'+runID +'_' + eve_file
        mne.set_log_file(fname = covLog_file, overwrite = True)
        tmin, tmax = -0.2, 0.6
        print covLog_file
        print 'Reading Raw data... '
        raw = io.Raw(fname)
        if runID == "emptyroom":
            cov = mne.compute_raw_data_covariance(raw) #, tmin = None, tmax = 0) #, reject = None, picks = picks)
            print cov
        else:
            
            events = mne.read_events(event_file)
            include = []  # or stim channels ['STI 014']
    #        #raw.info['bads'] += ['EEG 053']  # bads + 1 more
    #        # pick EEG channels
            picks = mne.pick_types(raw.info, meg=True, eeg=False, stim=False, eog=True, include=include, exclude='bads')
            reject = dict(mag = 4e-12, grad = 4000e-13)
            epochs = mne.Epochs(raw, events, event_id, tmin, tmax, baseline = (None,0), picks = picks, proj = True, preload = True, reject=reject)
            print epochs
#            ##Example: reject = dict(grad=4000e-13, # T / m (gradiometers)
#                          mag=4e-12, # T (magnetometers)
#                          eeg=40e-6, # uV (EEG channels)
#                          eog=250e-6 # uV (EOG channels)
#                          )
            
#             Compute the covariance from the raw data or from epochs 
            cov = mne.compute_covariance(epochs, tmin = None, tmax = 0) #Use for runs... 
            print cov
#        covRuns.append(cov)
        mne.write_cov(cname, cov)
#        
#print len(covRuns)
#
###Make the Final Grand average of all the runs
#runData = []
#runNave = []
#newCov = []
#newCov = copy.deepcopy(cov)
#count = 0 
#
#for covRun in covRuns:
#    runData.append(covRun)
###        runNave.append(evRun[c].nave)
#    print 'Jane Here', 
#print runData
#gcovData = numpy.mean(runData,0)
#print gcovData
##newCov.data = gcovData
#
##    
##    runData = []
##    runNave = []
##print newCov

################################################################################
## Show covariance
#fig_cov, fig_svd = mne.viz.plot_cov(cov, raw.info, colorbar=True, proj=True)
## try setting proj to False to see the effect
