
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 18 9:03:30 2014

@author: custine
Script to plot the evoked data rom the gradiometers and magnetometers
Only for visualisation purpose
"""

import sys
sys.path.insert(0,'/home/custine/MEG/scripts/mne-python/')
import argparse
import mne
#from mne import viz

###############################################################
### Get User Input 

parser = argparse.ArgumentParser(description = 'Get user input..')
parser.add_argument('exp', type = str)
parser.add_argument('subjID', type = str)
parser.add_argument('par', type = str)
parser.add_argument('cond', type = str)


args = parser.parse_args()
exp = args.exp ## msabri
subjID = args.subjID
par = args.par ##Left Right etc.,
cond = args.cond
print cond

####Setup Subject Speciifc Information
data_path = '/home/custine/MEG/data/' +exp
fname = data_path + '/'+subjID + '/ave_projon/' + subjID +'_' +par+'-ave.fif'
print fname
evoked = mne.fiff.Evoked(fname, setno = 'epochs_'+cond , baseline = (None, 0))
#evoked = mne.fiff.Evoked(fname, setno = int(cond) , baseline = (None, 0))
#badChanSet = set(evoked.info['bads'])
sel = mne.fiff.pick_types(evoked.info,meg=True, eeg=False, exclude = 'bads')
times = [0.1, 0.2,0.3, 0.4]
evoked.plot_topomap(times, ch_type = 'mag', size=5)
evoked.plot_topomap(times, ch_type= 'grad', size=5)
#evoked.plot(picks = sel, show = True)
    
