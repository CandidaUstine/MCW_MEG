# -*- coding: utf-8 -*-
"""
Created on Wed Feb 19 16:54:10 2014

@author: custine
"""

import sys
sys.path.insert(0,'/home/custine/MEG/scripts/mne-python/')
import argparse
import mne
import numpy as np
import matplotlib.pyplot as plt
from pylab import imshow, show, get_cmap

###############################################################
### Get User Input 

parser = argparse.ArgumentParser(description = 'Get user input..')
parser.add_argument('exp', type = str)
parser.add_argument('subjID', type = str)
parser.add_argument('par', type = str)
parser.add_argument('set1', type = str)

args = parser.parse_args()
exp = args.exp ## msabri
subjID = args.subjID
par = args.par ##Left Right etc.,
set1 = args.set1
condName = [args.set1] ##If set1 and set2 are condition names
colorList = ['k', 'r'] ##First cond: Black, Second cond: Red
ymin,ymax = [-.5,15]
xmin,xmax = [-100,400]

####Setup Subject Speciifc Information
data_path = '/home/custine/MEG/data/' +exp+'/'+subjID + '/ave_projon/'
results_path = data_path +'plots/' 
fname = data_path + subjID +'_' +par+'-ave.fif'
out_fname = results_path + subjID + '_' + par +'_'+set1+'_meg_evoked_color.png'
print out_fname

####Reading the Evoked data structure
for c in condName:
    print c
    evoked = mne.fiff.Evoked(fname, setno = 'epochs_'+c , baseline = (None, 0))
    #evoked = mne.fiff.Evoked(fname, setno = c , baseline = (None, 0)) ##Use this if you are using condition numbers
    badChanSet = set(evoked.info['bads'])
    print c
    sel = mne.fiff.pick_types(evoked.info,meg=True, eeg=False, exclude = 'bads')
    data = evoked.data[sel]
    ##Plotting the epochs for all the MEG sensors across time
    plt.ylabel('MEG Sensors')
    plt.xlabel('Time in msec')
    plt.title('Colour map of MEG sensors evoked data')
    plt.imshow(data, cmap=get_cmap("Jet"), interpolation=None)
    #show()
    plt.savefig(out_fname)