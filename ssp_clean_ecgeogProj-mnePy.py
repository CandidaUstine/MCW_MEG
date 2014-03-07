# -*- coding: utf-8 -*-
"""
Created on Wed Mar  5 13:27:33 2014

@author: custine
SSP Projector creation and application using mne-python method
"""

import mne
from mne import fiff
from mne.fiff import proj
import argparse 
from mne import preprocessing
#from mne.fiff.proj import make_projector, activate_proj

parser = argparse.ArgumentParser(description = "Get Input")
parser.add_argument('subj', type = str)
parser.add_argument('exp', type = str)
parser.add_argument('par', type = str)
parser.add_argument('run', type = str)
parser.add_argument('proj', type = str)
args = parser.parse_args()
subjID = args.subj
exp = args.exp
par = args.par
run = args.run
proj_type = args.proj 
print proj

dataPath = '/home/custine/MEG/data/'+exp+'/'+subjID+'/'
raw_fname = dataPath + subjID + '_' +par + run +'_raw.fif'
raw_ssp_fname = dataPath + 'ssp/' + subjID + '_' +par + run + '_clean_'+proj_type+'_raw.fif'
eve_fname = dataPath + 'ssp/'+ subjID + '_'  +par+run+'_'+proj_type+'-eve.fif'
proj_fname = dataPath + 'ssp/' + subjID + '_' + par + run + '_' + proj_type + '-proj.fif'

raw_in = fiff.Raw(raw_fname, preload = True)

if proj_type =='eog': 
    proj, eog_events = mne.preprocessing.compute_proj_eog(raw_in, n_grad = 1, n_mag = 1, tmin = -0.25, tmax = 0.25, event_id = 202, ch_name = 'EOG061') 
    print eog_events     
    mne.write_events(eve_fname, eog_events)    
    raw_in.add_proj(proj, remove_existing = False)
    raw_in.save(raw_ssp_fname, overwrite = True)
    raw_in.apply_proj()
else:
    proj, ecg_events = mne.preprocessing.compute_proj_ecg(raw_in, n_grad = 1, n_mag = 1, tmin = -0.1, tmax = 0.1, event_id = 402, ch_name = 'ECG064') 
    print ecg_events    
    mne.write_events(eve_fname, ecg_events)    
    raw_in.add_proj(proj, remove_existing = False)
    raw_in.save(raw_ssp_fname, overwrite = True)
    raw_in.apply_proj()