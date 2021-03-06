# -*- coding: utf-8 -*-
"""
Created on Thu Dec 11 15:16:37 2014

@author: custine

This scripts generates a new Grand Average of sessions within a subject. A new _gaSess-ave.fif file is created. 
Usage: python sensor_grandAverage.py exp paradigm
Example: python sensor_avgAcrossSessions.py 9511 Noun_Place

"""

import numpy as np 
import mne
import argparse
import copy 
import readInput 
import condCodes as cc

###############################################################
### Get User Input 

parser = argparse.ArgumentParser(description = 'Get user input..')
parser.add_argument('subjID', type = str)
parser.add_argument('par', type = str)

args = parser.parse_args()
subjID = args.subjID ## 9511
par = args.par  ##Noun_People_All

sessions = ['s5', 's6', 's7', 's8'] 

####Setup Subject Speciifc Information
data_path = '/home/custine/MEG/data/krns_kr3/' + subjID + '/'
#subjList = readInput.readList('/home/custine/MEG/scripts/function_inputs/'+exp+'_subjList.txt')
result_path = '/home/custine/MEG/results/sensor_level/ga_fif/krns_kr3/' 

event_id ={}
condName = {}
labels = cc.condLabels[par]
for row in labels: 
    event_id[row[1]] = int(row[0])   
    
print event_id
print 'Number of Conditions...'
lenCond = len(event_id)
print lenCond

allData = [ [] for item in range(lenCond)]
allNtrial = [[] for item in range(lenCond)]


####Get individual subject specific evoked data
for sess in sessions: 
    aveFile = data_path + sess + '/ave_projon/' + subjID + '_'+ sess+ '_' + par + '_All-ave.fif' 
    evoked = [mne.fiff.read_evoked(aveFile, setno = 'epochs_'+cond ) for cond in event_id]
    print evoked
    for c in range(lenCond):
        allData[c].append(evoked[c].data)
        allNtrial[c].append(evoked[c].nave)
print allData        
####Grand average across all subject evoked data 
gaveData = [np.mean(allData[cond],0) for cond in range(lenCond)]        
gaveNtrial= [np.sum(allNtrial[cond], 0) for cond in range(lenCond)]

data_file = data_path + sessions[0] + '/ave_projon/' + subjID + '_' + sessions[0] + '_' + par +'_All-ave.fif'
result_file = result_path + 'gaSess_' + subjID + '_' + par + '_All_c1-ave.fif'

evokeds = [mne.fiff.read_evoked(data_file, setno = 'epochs_'+cond) for cond in event_id]
newEvoked = copy.deepcopy(evokeds)
for c in range(lenCond):
    newEvoked[c].data =gaveData[c]
    newEvoked[c].nave = gaveNtrial[c]
    
####Write result file in results folder
mne.fiff.write_evoked(result_file, newEvoked)
print 'Finished writting evoked data. Check the results folder.'























