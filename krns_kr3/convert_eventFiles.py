# -*- coding: utf-8 -*-
"""
Created on Fri Jan  9 14:32:44 2015
Saving .eve text files as -eve.fif files 
@author: custine
Ex: python convert_eventFiles.py 9567 s5 Noun_Place
"""

print(__doc__)

import mne
import argparse
import condCodes as cc

parser = argparse.ArgumentParser(description='Get input')
parser.add_argument('subj',type=str)
parser.add_argument('sess',type=str) ##Left, Right etc.,
parser.add_argument('tag',type=str) 
args=parser.parse_args()
subjID = args.subj
sessID = args.sess
tag = args.tag
print subjID
print sessID
print tag

        
data_path = '/home/custine/MEG/data/krns_kr3/' +subjID+'/'+sessID
runs = cc.runDict[tag]
print runs 

###Event file suffix 
txt_eveSuffix = '-TriggersMod.eve' 
fif_eveSuffix = '-TriggersMod-eve.fif' 
eve_txt_file = tag + txt_eveSuffix #eve + eveSuffix 
eve_fif_file = tag + fif_eveSuffix
print "You have chosen the event file " + eve_txt_file
runs = ['run1']
for runID in runs:
        print runID
        raw_fname = data_path +'/'+ subjID + '_'+ sessID +'_' + runID + '_raw.fif'
        print raw_fname 
        eve_txt_fname = data_path + '/eve/triggers/' + subjID + '_'+ sessID +'_'+runID +'_' + eve_txt_file
        eve_fif_fname = data_path + '/eve/triggers/' + subjID + '_'+ sessID +'_'+runID +'_' + eve_fif_file
        print eve_txt_fname
        events = mne.read_events(eve_txt_fname)
        print events 
        mne.write_events(eve_fif_fname, events)
        
        events = mne.read_events(eve_fif_fname)
        print events 
        print 
        events = mne.read_events('/home/custine/MEG/data/krns_kr3/9567/s6/eve/triggers/9567_s6_run1_Noun_People-TriggersMod.eve')
        print events 
        
        
        
        