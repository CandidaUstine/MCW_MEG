# -*- coding: utf-8 -*-
"""
Created on Fri Sep 12 11:53:19 2014

@author: custine
"""

#import mne
#from mne import io
#
#raw = mne.io.Raw('/home/custine/MEG/data/krns_kr3/9367/s5/9367_s5_run1_raw.fif')
#eve_fname = '/home/custine/MEG/data/krns_kr3/9367/s5/eve/9367_s5_run1.eve'
#print(raw)
#print raw.info['sfreq']
#events = mne.find_events(raw, stim_channel = 'STI102', min_duration = 0.001)
#print(events)
#
#mne.write_events(eve_fname, events)


print(__doc__)

import mne
from mne import io
import argparse

parser = argparse.ArgumentParser(description='Get input')
parser.add_argument('subj',type=str)
parser.add_argument('sess',type=str)
args=parser.parse_args()
subjID = args.subj
sessID = args.sess
print subjID
print sessID

###Event file suffix 
eve_file = '.eve'
runs = ['1', '2', '3', '4', '5','6', '7', '8', '9', '10', '11', '12']  # TESTING################################################
print runs

for runID in runs:  ###For other runs use the baseline and set tmin/tmax using epoched data. 
        runID = 'run' + runID
        print runID
        
        data_path = '/home/custine/MEG/data/krns_kr3/' +subjID+'/'+sessID
        fname = data_path +'/'+ subjID + '_'+ sessID +'_'+runID +'_raw.fif'
        print fname
        event_file = data_path + '/eve/' + subjID + '_'+ sessID +'_'+runID + eve_file
        raw = mne.io.Raw(fname)
        print(raw)
        print raw.info['sfreq']
        events = mne.find_events(raw, stim_channel = 'STI102', min_duration = 0.001)
        print(events)
        
        mne.write_events(event_file, events)    
        print "Done " + runID
        
print "Events written in subject's eve folder..." 
        
        
        