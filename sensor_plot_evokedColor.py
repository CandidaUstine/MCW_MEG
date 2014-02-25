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
import readInput 
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

####Setup Subject Speciifc Information
data_path = '/home/custine/MEG/data/' +exp+'/'+subjID + '/ave_projon/'
results_path = data_path +'plots/' 
fname = data_path + subjID +'_' +par+'-ave.fif'
out_fname = results_path + subjID + '_' + par +'_'+set1+'_meg_evoked_color.png'
print out_fname
#chan_path = '/home/custine/MEG/scripts/function_inputs/MEG_Chan_Names/'
chan_fname = '/home/custine/MEG/scripts/function_inputs/MEG_Chan_Number/MEG_chan_number_list-m.txt'
chan_names = readInput.readList(chan_fname)
#chan_list = []
#for item in chan_names:
#    chan_list.append('MEG'+item)
chan_names = [int(chan) for chan in chan_names]

####Reading the Evoked data structure
for c in condName:
    print c
    evoked = mne.fiff.Evoked(fname, setno='epochs_'+c , baseline = (None, 0))
    #evoked = mne.fiff.Evoked(fname, setno = c , baseline = (None, 0)) ##Use this if you are using condition numbers
    #badChanSet = set(evoked.info['bads'])
    sel = chan_names
    #sel = list(set(chan_names) - set(badChanSet))
    print sel
    data = evoked.data[sel]
    print data
    ##Plotting the epochs for all the MEG sensors across time
    plt.ylabel('MEG Sensors')
    plt.xlabel('Time in msec')
    plt.title('Colour map of MEG sensors evoked data')
    #plt.tick_params()
    plt.imshow(data, cmap=get_cmap("hsv"), interpolation=None)
    plt.colorbar()
    #plt.show()
    plt.savefig(out_fname)