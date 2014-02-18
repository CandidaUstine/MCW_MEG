# -*- coding: utf-8 -*-
"""
Created on Tue Feb 18 9:03:30 2014

@author: custine
Script to plot the RMS for the gradiometers in regions speciffied by the channel groups
"""

import numpy as np 
import os
import sys
sys.path.insert(0,'/home/custine/MEG/scripts/mne-python/')
import argparse
import mne
from mne import viz
from mne.viz import plot_topo
sys.path.insert(0,'/home/custine/MEG/scripts/mne-python/')

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

####Setup Subject Speciifc Information
data_path = '/home/custine/MEG/data/' +exp
fname = data_path + '/'+subjID + '/ave_projon/' + subjID +'_' +par+'-ave.fif'
print fname

evoked = mne.fiff.read_evoked(fname, setno = 0, baseline = (None, 0))
evoked.plot_topomap(0.1, ch_type = 'mag', size=3)
times = [0.05, 0.1, 0.15, 0.2, 0.25, 0.3]

evoked.plot_topomap(times, ch_type='meg')
evoked.plot_topomap(times, ch_type='grad')

#plot_topo(evoked, title ='Jane')
