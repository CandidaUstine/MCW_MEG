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
from mne.preprocessing import compute_proj_ecg, compute_proj_eog
from mne.fiff.proj import make_projector, activate_proj
from mne import Epochs

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
raw_fname = dataPath + subjID + '_' +par+run+'_raw.fif'
eve_fname = dataPath + 'ssp/'+ subjID + '_'  +par+run+'_'+proj_type+'-eve.fif'
proj_fname = dataPath + 'ssp/' + subjID + '_' + par + run + '_' + proj_type + '-proj.fif'

raw_in = fiff.Raw(raw_fname, preload = True)
if proj_type =='eog': 
    projs_eog, events = compute_proj_eog(raw_in, n_mag = 1, n_grad = 1, bads = [])
    print projs_eog
    projs_eog = fiff.proj.activate_proj(projs_eog)
    fid = fiff.write.start_file(proj_fname)
    print fid
    fiff.write.write_proj(fid, projs_eog)
    fiff.write.end_file(fid)
    #projs_fname = fiff.proj.make_projector(projs_eog, raw_in.ch_names, bads = [])
else:
    projs_ecg, events = compute_proj_ecg(raw_in, chans= raw_in.ch_names, bads = [])
    projs_ecg = fiff.proj.activate_proj(projs_ecg)
    projs_ecg = fiff.proj.make_projector()
    

