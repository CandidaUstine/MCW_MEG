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
import numpy as np
import pylab as pl
import readInput
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
ymin,ymax = [-.5,15]
xmin,xmax = [-100,400]

####Setup Subject Speciifc Information
data_path = '/home/custine/MEG/data/' +exp+'/'+subjID + '/ave_projon/'
results_path = data_path +'plots/' 
fname = data_path + subjID +'_' +par+'-ave.fif'
out_fname = results_path + subjID + '_' + par +'_'+set1+'-'+set2+'_meg_rms_topo.png'
chan_path = '/home/custine/MEG/scripts/function_inputs/MEG_Chan_Names/'
print out_fname

chan_groups = ['Frontal', 'Parietal', 'Temporal', 'Occipital']
hem = ['L', 'R']

for grp in chan_groups:
    font = {'size': 8}
    pl.rc('font', **font)
    pl.subplots_adjust(hspace=0.5, wspace =0.5) 
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
                pl.subplot(3,4,2)
                pl.title('Left Frontal', fontsize = 'large')
            elif grp == 'Temporal':
                pl.subplot(3,4,5)
                pl.title('Left Temporal', fontsize = 'large')
            elif grp == 'Parietal':
                pl.subplot(3,4,6)
                #pl.title()
                pl.title('Left Parietal', fontsize = 'large')
            elif grp == 'Occipital':
                pl.subplot(3,4,10)
                pl.title('Left Occipital', fontsize = 'large')
               # pl.text(10,20,'Left Frontal')
                
        else:
            if grp == 'Frontal':
                pl.subplot(3,4,3)
                pl.title('Right Frontal', fontsize = 'large')
            elif grp == 'Temporal':
                pl.subplot(3,4,8)
                pl.title('Right Temporal', fontsize = 'large')
            elif grp == 'Parietal':
                pl.subplot(3,4,7)
                pl.title('Right Parietal', fontsize = 'large')
            elif grp == 'Occipital':
                pl.subplot(3,4,11)            
                pl.title('Right Occipital', fontsize = 'large')               
              
        ####Reading the Evoked data structure
        for (c,l) in zip(condName, colorList):
            evoked = mne.fiff.Evoked(fname, setno = 'epochs_'+c , baseline = (None, 0))
            #evoked = mne.fiff.Evoked(fname, setno = c , baseline = (None, 0)) ##Use this if you are using condition numbers
            badChanSet = set(evoked.info['bads'])
            print c
            good_chan=list(set(chan_list))
            sel = mne.fiff.pick_types(evoked.info,meg=False, eeg=False, include = good_chan)
            data = evoked.data[sel]
            ###Computing the MEG RMS from the evoked data for the specified condition
            times = evoked.times*1000
            square = np.power(data, 2)
            meanSquare = np.mean(square, 0)
            rms = np.power(meanSquare, 0.5)
            ###Plotting the MEG rms value for the current condition
            pl.plot(times, rms*1e13, color = l, linewidth=2)
            pl.ylim([ymin,ymax])
            pl.xlim([xmin,xmax])
            pl.box('off')
            pl.tick_params(axis='both',right='off',top='off') 
            pl.yticks(np.array([0.,4.,8.,12.,16.]))
            pl.xticks(np.array([0,100, 200, 300, 400]))    
pl.savefig(out_fname)
pl.show() 


