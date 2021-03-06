# -*- coding: utf-8 -*-
"""
Created on Wed Feb 26 10:43:57 2014

@author: custine
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
parser.add_argument('par', type = str)
parser.add_argument('set1', type = str)
parser.add_argument('set2', type = str)

args = parser.parse_args()
exp = args.exp ## msabri
#subjID = args.subjID
par = args.par ##Left Right etc.,
set1 = args.set1
set2 = args.set2
condList = [args.set1, args.set2] ##If set1 and set2 are condition numbers 
condName = [args.set1, args.set2] ##If set1 and set2 are condition names
colorList = ['k', 'r'] ##First cond: Black, Second cond: Red
ymin,ymax = [-.5,15]
xmin,xmax = [-100,400]

####Setup Subject Speciifc Information
data_path = '/home/custine/MEG/data/' +exp + '/'
results_path = '/home/custine/MEG/results/sensor_level/MEG_rms/'
chan_path = '/home/custine/MEG/scripts/function_inputs/MEG_Chan_Names/'
out_fname = results_path + exp + '_subjList_' + par +'_'+set1+'-'+set2+'_meg_rms_topo.png'
subjList = readInput.readList('/home/custine/MEG/scripts/function_inputs/'+exp+'_subjList.txt')
print out_fname

chan_groups = ['Frontal', 'Parietal', 'Temporal', 'Occipital']
hem = ['L', 'R']

for grp in chan_groups:
    font = {'size': 8}
    pl.rc('font', **font)
    pl.subplots_adjust(hspace=0.5, wspace =0.5) 
    for h in hem : 
        chan_list =[]
        chan_fname = chan_path + 'chan_' + h + grp +'.txt'
        chan_names = readInput.readList(chan_fname)
        for item in chan_names:
            chan_list.append('MEG'+item)

        if h == 'L':
            if grp == 'Frontal':
                pl.subplot(3,4,2)
                pl.title('Left Frontal', fontsize = 'large')
            elif grp == 'Temporal':
                pl.subplot(3,4,5)
                pl.title('Left Temporal', fontsize = 'large')
            elif grp == 'Parietal':
                pl.subplot(3,4,6)
                pl.title('Left Parietal', fontsize = 'large')
            elif grp == 'Occipital':
                pl.subplot(3,4,10)
                pl.title('Left Occipital', fontsize = 'large')             
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

        #for (c,l) in zip(condName, colorList):   
        for c in range(2):    
            for subj in subjList: 
                aveFile = data_path + subj + '/ave_projon/' + subj+ '_'+ par + '-ave.fif'  
                print condName[c], colorList[c]
                ####Reading the Evoked data structure
                evoked = mne.fiff.Evoked(aveFile, setno = 'epochs_'+condName[c] , baseline = (None, 0))
                #evoked = mne.fiff.Evoked(fname, setno = c , baseline = (None, 0)) ##Use this if you are using condition numbers
                badChanSet = set(evoked.info['bads'])
                print c
                good_chan=list(set(chan_list)- badChanSet)
                sel = mne.fiff.pick_types(evoked.info,meg=False, eeg=False, include = good_chan)
                data = evoked.data[sel]
                ###Computing the MEG RMS from the evoked data for the specified condition
                times = evoked.times*1000
                square = np.power(data, 2)
                meanSquare = np.mean(square, 0)
                rmsSubj = np.power(meanSquare, 0.5)
                if subj == subjList[0]:
                    rmsAll = rmsSubj 
                else: 
                    rmsAll = np.vstack((rmsAll, rmsSubj))
            rmsGA = np.mean(rmsAll, 0)
            
            ###Plotting the MEG rms value for the current condition
            pl.plot(times, rmsGA*1e13, color = colorList[c], linewidth=2)
            pl.ylim([ymin,ymax])
            pl.xlim([xmin,xmax])
            pl.box('off')
            pl.tick_params(axis='both',right='off',top='off') 
            pl.yticks(np.array([0.,4.,8.,12.,16.]))
            pl.xticks(np.array([0,100, 200, 300, 400]))    
pl.savefig(out_fname)
pl.show() 

