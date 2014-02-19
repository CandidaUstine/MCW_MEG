# -*- coding: utf-8 -*-
"""
Created on Wed Feb 19 14:44:31 2014

@author: custine
Script to plot the evoked data from the gradiometers and magnetometers
"""

import sys
sys.path.insert(0,'/home/custine/MEG/scripts/mne-python/')
import argparse
import mne
#from mne import viz
import condCodes as cc
import matplotlib.pyplot as plt

###############################################################
### Get User Input 

parser = argparse.ArgumentParser(description = 'Get user input..')
parser.add_argument('exp', type = str)
parser.add_argument('subjID', type = str)
parser.add_argument('par', type = str)
#parser.add_argument('set1', type = str)
#parser.add_argument('set2', type = str)

args = parser.parse_args()
exp = args.exp ## msabri
subjID = args.subjID
par = args.par ##Left Right etc.,
#set1 = args.set1
#set2 = args.set2
#condList = [args.set1, args.set2]    
#condName = [args.set1, args.set2]

labels = cc.condLabels[par]
condName = []
for row in labels: 
    print row[1]
    condName.append(row[1])
print condName

####Setup Subject Speciifc Information
data_path = '/home/custine/MEG/data/' +exp
fname = data_path + '/'+subjID + '/ave_projon/' + subjID +'_' +par+'-ave.fif'
print fname
for c in condName:
    evoked = mne.fiff.Evoked(fname, setno = 'epochs_'+c , baseline = (None, 0))
    #evoked = mne.fiff.Evoked(fname, setno = int(c) , baseline = (None, 0))
    #badChanSet = set(evoked.info['bads'])
    sel = mne.fiff.pick_types(evoked.info,meg=True, eeg=False, exclude = 'bads')
    #times = evoked.times*1000
    times = [0.1, 0.2, 0.3, 0.4]
    plt.clf()
    evoked.plot(picks =sel, show= True)
    out_fname = data_path+ '/'+subjID  + '/ave_projon/plots/'+subjID + '_' + par +'_'+c+'_meg_evoked_plot.png'
    plt.savefig(out_fname)
    #plt.show()