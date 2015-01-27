# -*- coding: utf-8 -*-
"""
Created on Fri Dec 12 11:08:43 2014

@author: custine

Script to plot the RMS for the magnetometers and gradiometers 
Ex: python sensor_plot_meg_rms.py 5049 run Noun_People Noun_Place s5 ##Use run(One plot per session) or session (one plot per subject)
Ex: python sensor_plot_meg_rms.py 9367 session Noun_Place Verb s(dummy variable)

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
parser.add_argument('subjID', type = str)
parser.add_argument('avgType', type = str) #run(one per session) or session (one per subject)
parser.add_argument('set1', type = str)
parser.add_argument('set2', type = str)
parser.add_argument('sess', type = str)

args = parser.parse_args()
avgType = args.avgType
subjID = args.subjID 
set1 = args.set1 ##Noun_Place, Noun_Place_ssp etc.,
set2 = args.set2 ##Noun_People ...
if avgType == 'run':
    
    sess = args.sess ## s5
    
colorList = ['k', 'r'] ##First cond: Black, Second cond: Red
ymin,ymax = [-.5,30]
xmin,xmax = [-100,600]

if avgType == 'run':
    ####Setup Subject Speciifc Information
    data_path = '/home/custine/MEG/data/krns_kr3/'+subjID + '/' + sess + '/ave_projon/'
    results_path = data_path +'plots/' 
    c1fname = data_path + subjID +'_' + sess + '_' + set1 +'_All-ave.fif' ##Change according to your interest
    c2fname = data_path + subjID +'_' + sess + '_' + set2 +'_All-ave.fif' 
    out_fname = results_path + subjID + '_' + sess+ '_'+set1+'-'+set2+'_meg_rms_topo.png'
    chan_path = '/home/custine/MEG/scripts/function_inputs/MEG_Chan_Names/'
    print out_fname
    
elif avgType == 'session':
    ####Setup Subject Speciifc Information
    data_path = '/home/custine/MEG/results/sensor_level/ga_fif/krns_kr3/'
    results_path = '/home/custine/MEG/results/sensor_level/MEG_rms/krns_kr3/'
    c1fname = data_path + 'gaSess_' + subjID + '_' + set1 +'_All_c1-ave.fif' ##Change according to your interest
    c2fname = data_path + 'gaSess_' + subjID + '_' + set2 +'_All_c1-ave.fif'
    out_fname = results_path + 'gaSess_' + subjID + '_'+set1+'-'+set2+'_meg_rms_topo.png'
    chan_path = '/home/custine/MEG/scripts/function_inputs/MEG_Chan_Names/'
    print out_fname
        
condEveFiles = [c1fname, c2fname]

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
        for (cfname,l) in zip(condEveFiles, colorList):
            evoked = mne.fiff.Evoked(cfname, setno = 'epochs_TaggedWord' , baseline = (None, 0))
            #evoked = mne.fiff.Evoked(fname, setno = c , baseline = (None, 0)) ##Use this if you are using condition numbers
            badChanSet = set(evoked.info['bads'])
#            print c
            good_chan=list(set(chan_list))
            sel = mne.fiff.pick_types(evoked.info,meg=False, eeg=False, include = good_chan)
            print sel
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
            pl.yticks(np.array([0.,4.,8.,12.,16.,20.,24.,28.,32.]))
            pl.xticks(np.array([0, 200, 400, 600]))    
pl.savefig(out_fname)
pl.show() 


