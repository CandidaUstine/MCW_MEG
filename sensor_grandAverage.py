# -*- coding: utf-8 -*-
"""
Created on Fri Feb 14 15:18:20 2014

@author: custine
This scripts generates a new Grand Average of individual subjects across all conditions. A new _ga-ave.fif file is created. 
Usage: python sensor_grandAverage.py exp paradigm
Example: python sensor_grandAverage.py msabri Left 
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
parser.add_argument('exp', type = str)
parser.add_argument('par', type = str)

args = parser.parse_args()
exp = args.exp ## msabri
par = args.par ##Left Right etc., 


####Setup Subject Speciifc Information
data_path = '/home/custine/MEG/data/msabri/'
subjList = readInput.readList('/home/custine/MEG/scripts/function_inputs/'+exp+'_subjList.txt')
result_path = '/home/custine/MEG/results/sensor_level/' + exp + '/'
print subjList

event_id ={}
condName = {}
labels = cc.condLabels[par]
for row in labels: 
#    print row
    event_id[row[1]] = int(row[0])   
    
print event_id
print 'Number of Conditions...'
lenCond = len(event_id)
print lenCond

allData = [ [] for item in range(lenCond)]
allNtrial = [[] for item in range(lenCond)]


####Get individual subject specific evoked data
for subj in subjList: 
    aveFile = data_path + subj + '/ave_projon/' + subj+ '_'+ par + '-ave.fif' 
    evoked = [mne.fiff.read_evoked(aveFile, setno = 'epochs_'+cond ) for cond in event_id]
    #print evoked
    for c in range(lenCond):
        allData[c].append(evoked[c].data)
        allNtrial[c].append(evoked[c].nave)
        
####Grand average across all subject evoked data 
gaveData = [np.mean(allData[cond],0) for cond in range(lenCond)]        
gaveNtrial= [np.sum(allNtrial[cond], 0) for cond in range(lenCond)]

data_file = data_path + subjList[0] + '/ave_projon/' + subjList[0] + '_' + par +'-ave.fif'
result_file = result_path + par + '_ga-ave.fif'

evokeds = [mne.fiff.read_evoked(data_file, setno = 'epochs_'+cond) for cond in event_id]
newEvoked = copy.deepcopy(evokeds)
for c in range(lenCond):
    newEvoked[c].data =gaveData[c]
    newEvoked[c].nave = gaveNtrial[c]
    
####Write result file in results folder
mne.fiff.write_evoked(result_file, newEvoked)
print 'Finished writting evoked data. Check the results folder.'























