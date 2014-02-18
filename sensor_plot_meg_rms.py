# -*- coding: utf-8 -*-
"""
Created on Tue Feb 18 15:13:54 2014

@author: custine
Script to plot the RMS for the magnetometers and gradiometers 
"""

import sys
sys.path.insert(0,'/home/custine/MEG/scripts/mne-python/')
import argparse
import mne
import condCodes as cc
import numpy as np
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
condList = [args.set1, args.set2] ##If set1 and set2 are condition numbers 
condName = [args.set1, args.set2] ##If set1 and set2 are condition names
colorList = ['k', 'r'] ##First cond: Black, Second cond: Red


####Setup Subject Speciifc Information
data_path = '/home/custine/MEG/data/' +exp
fname = data_path + '/'+subjID + '/ave_projon/' + subjID +'_' +par+'-ave.fif'
print fname

####Reading the Evoked data structure
for (c,l) in zip(condName, colorList):
    print c
    evoked = mne.fiff.Evoked(fname, setno = 'epochs_'+c , baseline = (None, 0))
    #evoked = mne.fiff.Evoked(fname, setno = c , baseline = (None, 0)) ##Use this if you are using condition numbers
    badChanSet = set(evoked.info['bads'])
    print c
    sel = mne.fiff.pick_types(evoked.info,meg=True, eeg=False, exclude = 'bads')
    data = evoked.data[sel]
    times = [0.05, 0.1, 0.15, 0.2, 0.25, 0.3]
    times = evoked.times*1000
    square = np.power(data, 2)
    meanSquare = np.mean(square, 0)
    rms = np.power(meanSquare, 0.5)
    pl.plot(times, rms*1e13, color = l, linewidth=2, label = c)
pl.show()

