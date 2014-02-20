# -*- coding: utf-8 -*-
"""
Created on Thu Feb 13 16:59:34 2014

@author: custine
Usage: python preProc_avg.py subjID expName
Example: python preProc_avg.py ac1 Left 
"""

import mne
from mne import fiff
#from mne import viz
#from mne.viz import plot_evoked
import argparse
import condCodes as cc


#######Get Input ##

parser = argparse.ArgumentParser(description='Get input')
parser.add_argument('subj',type=str)
parser.add_argument('exp',type=str) ##Left, Right etc., 
args=parser.parse_args()
subjID = args.subj
exp = args.exp
print subjID
print exp

########Analysis Parameters##
###Event file suffix 
evSuffix = '_mod.eve'

###Projection and Average Reference 
projVal = True
avgRefVal = False

###Filtering
hp_cutoff = 0.7
lp_cutoff = 20

#######Experiment specific parameters 
###EventLabels
labelList = cc.condLabels[exp]
event_id = {}
condName = {}
for row in labelList:
    #print row[1]
    event_id[row[1]] = int(row[0])
    condName[row[1]] = row[1]
print event_id

###TimeWindow
tmin = -.1
tmax = float(cc.epMax[exp])


########Artifact rejection parameters
###General
gradRej = 2000e-13
magRej = 3000e-15
eegRej = 100e-6
magFlat = 1e-14
gradFlat = 1000e-15

#####################################
########Compute averages for each run

evoked=[]
#print ev 

##Setup Subject Speciifc Information
data_path = '/home/custine/MEG/data/msabri/' +subjID
event_file = data_path + '/eve/' + subjID + '_'+ exp + evSuffix
print event_file

raw_file = data_path +'/'+ subjID +'_' +exp + '_raw.fif' ##Change this suffix if you are using SSP 
avgLog_file = data_path + '/ave_projon/logs/' +subjID + '_' + exp + '_py-ave.log'


##Setup Reading fiff data structure
print 'Reading Raw data... '
raw = fiff.Raw(raw_file, preload = True)
events = mne.read_events(event_file)

raw_skip = raw.first_samp
mne.set_log_file(fname = avgLog_file, overwrite = True)

##Filter raw data 
fiff.Raw.filter(raw, l_freq = hp_cutoff, h_freq = lp_cutoff)

##Pick all channels 
picks = []
for i in range(raw.info['nchan']):
    picks.append(i)
    
##Read Epochs and compute Evoked :) 
print 'Reading Epochs from raw file...'
epochs = mne.Epochs(raw, events, event_id, tmin, tmax, baseline = (None,0), picks = picks, proj = True, name = condName, preload = True, flat = dict(mag = magFlat, grad= gradFlat), reject=dict(mag=magRej, grad=gradRej))
print epochs
evoked = [epochs[cond].average(picks =picks) for cond in event_id]

##Write Evoked 
print 'Writing Evoked data to -ave.fif file...' 
fiff.write_evoked(data_path + '/ave_projon/'+subjID+'_' +exp+'-ave.fif', evoked)

print 'Completed! See ave.fif result in folder', data_path + '/ave_projon/'

##Show the Result - Plotting the evoked data
#mne.viz.plot_evoked(evoked, exclude = [])
























