# -*- coding: utf-8 -*-
"""
Created on Tue Feb 18 9:03:30 2014

@author: custine
Script to plot the RMS for the gradiometers in regions speciffied by the channel groups
"""

import sys
sys.path.insert(0,'/home/custine/MEG/scripts/mne-python/')
import argparse
import mne
#from mne import viz
from mne.viz import plot_topo
import condCodes as cc
import numpy as np
import matplotlib.pyplot as plt
import pylab as pl

###############################################################
### Get User Input 

parser = argparse.ArgumentParser(description = 'Get user input..')
parser.add_argument('exp', type = str)
parser.add_argument('subjID', type = str)
parser.add_argument('par', type = str)
parser.add_argument('set1', type = str)
parser.add_argument('set2', type = str)

args = parser.parse_args()
exp = args.exp ## msabri
subjID = args.subjID
par = args.par ##Left Right etc.,
set1 = args.set1
set2 = args.set2
condList = [args.set1, args.set2]
#print condList
labels = cc.condLabels[par]
event_id ={}
condName = []
for row in labels: 
    print row[1]
    event_id[row[1]] = int(row[0])
    condName.append(row[1])
    
condName = [args.set1, args.set2]
print condName

####Setup Subject Speciifc Information
data_path = '/home/custine/MEG/data/' +exp
fname = data_path + '/'+subjID + '/ave_projon/' + subjID +'_' +par+'-ave.fif'
print fname
for c in condName:
    evoked = mne.fiff.Evoked(fname, setno = 'epochs_'+c , baseline = (None, 0))
    #evoked = mne.fiff.Evoked(fname, setno = int(c) , baseline = (None, 0))
    badChanSet = set(evoked.info['bads'])
    print c
    sel = mne.fiff.pick_types(evoked.info,meg=True, eeg=False, exclude = 'bads')
    data = evoked.data[sel]
    times = [0.05, 0.1, 0.15, 0.2, 0.25, 0.3]
    times = evoked.times*1000
    #evoked.plot_topomap(times, ch_type = 'mag', size=5)
    
    square = np.power(data, 2)
    meanSquare = np.mean(square, 0)
    rms = np.power(meanSquare, 0.5)
    #rmsGA = np.mean(rms, 0)
    pl.plot(times, rms*1e13)
pl.show()
#evoked = mne.fiff.read_evoked(fname, setno = 0, baseline = (None, 0))
#evoked.plot_topomap(0.1, ch_type = 'mag', size=3)
#times = [0.05, 0.1, 0.15, 0.2, 0.25, 0.3]

#evoked.plot_topomap(times, ch_type='meg')
#evoked.plot_topomap(times, ch_type='grad')

#plot_topo(evoked, title ='Jane')
