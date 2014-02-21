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
chan_path = '/home/custine/MEG/scripts/function_inputs/MEG_Chan_Names/'
#chan_names = readInput.readList(chan_fname)
chan_list = []
#for item in chan_names:
#    chan_list.append('MEG'+item)
#grp_list = ['Vertex', 'Left-frontal','Left-temporal', 'Left-parietal', 'Left-occipital', 'Right-frontal', 'Right-temporal', 'Right-parietal', 'Right-occipital']

chan_groups = ['Frontal', 'Parietal', 'Temporal', 'Occipital']
hem = ['L', 'R']
data = []
for grp in chan_groups:
    font = {'size': 8}
    plt.rc('font', **font)
    plt.subplots_adjust(hspace=0.2, wspace =0.2) 
    #pl.axes(frameon=False)
    for h in hem : 
        chan_list =[]
        chan_fname = chan_path + 'chan_' + h + grp +'.txt'
        chan_names = readInput.readList(chan_fname)
        for item in chan_names:
            chan_list.append('MEG'+item)

        #print chan_list
        if h == 'L':
            if grp == 'Frontal':
                plt.subplot(3,4,2)
                #plt.title('Left Frontal', fontsize = 'large')
            elif grp == 'Temporal':
                plt.subplot(3,4,5)
                #plt.title('Left Temporal', fontsize = 'large')
            elif grp == 'Parietal':
                plt.subplot(3,4,6)
                #pl.title()
                #plt.title('Left Parietal', fontsize = 'large')
            elif grp == 'Occipital':
                plt.subplot(3,4,10)
                #plt.title('Left Occipital', fontsize = 'large')
               # pl.text(10,20,'Left Frontal')
                
        else:
            if grp == 'Frontal':
                plt.subplot(3,4,3)
                #plt.title('Right Frontal', fontsize = 'large')
            elif grp == 'Temporal':
                plt.subplot(3,4,8)
                #plt.title('Right Temporal', fontsize = 'large')
            elif grp == 'Parietal':
                plt.subplot(3,4,7)
                #plt.title('Right Parietal', fontsize = 'large')
            elif grp == 'Occipital':
                plt.subplot(3,4,11)            
                #plt.title('Right Occipital', fontsize = 'large')  

        ####Reading the Evoked data structure
        for c in condName:
            print c
            evoked = mne.fiff.Evoked(fname, setno='epochs_'+c , baseline = (None, 0))
            #evoked = mne.fiff.Evoked(fname, setno = c , baseline = (None, 0)) ##Use this if you are using condition numbers
            badChanSet = set(evoked.info['bads'])
            print c
            sel = mne.fiff.pick_channels(evoked.ch_names,include=chan_list)
            #sel = mne.fiff.pick_types(evoked.info,meg=True, eeg=False, exclude = 'bads')
            #sel = mne.read_selection(name = grp_list)
            print sel
            data.append(evoked.data[sel])
            #evoked.data
            print data
            ##Plotting the epochs for all the MEG sensors across time
            #plt.ylabel('MEG Sensors')
            #plt.xlabel('Time in msec')
            #plt.title('Colour map of MEG sensors evoked data')
            plt.imshow(data, cmap=get_cmap("Jet"), interpolation=None)
plt.colorbar()
plt.show()
plt.savefig(out_fname)