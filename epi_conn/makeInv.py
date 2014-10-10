# -*- coding: utf-8 -*-
"""
Created on Wed Oct  8 10:52:23 2014

@author: custine
"""


print(__doc__)

import numpy as np
import mne
from mne.io import Raw
from mne.minimum_norm import (apply_inverse, apply_inverse_epochs,
                              read_inverse_operator, write_inverse_operator)
from mne.connectivity import seed_target_indices, spectral_connectivity


import argparse

#####################################3
##Get Inputs 
parser = argparse.ArgumentParser(description='Get input')
parser.add_argument('subj',type=str) ##EP1
args=parser.parse_args()
subj = args.subj
print subj
#######################################

# Set parameters
data_path = '/home/custine/MEG/data/epi_conn/' + subj + '/'
subjects_dir = '/home/custine/MRI/structurals/subjects/'
label_name_lh = 'lh.frontalpole' #label name 

fname_label_lh = subjects_dir + 'labels/%s.label' % label_name_lh 

tmin = 0
tmax = 2.0  # Use a lower tmax to reduce multiple comparisons
gradRej = 5000e-13
magRej = 4000e-15
magFlat = 1e-14
gradFlat = 1000e-15
event_id = None
##
fname_inv = data_path + 'ave_projon/'+ subj + '_run1-ave-7-meg-inv.fif'
fname_fwd = data_path + 'ave_projon/'+ subj + '_run1-ave-7-meg-fwd.fif'

cov_fname = data_path + 'cov/emptyroom-cov.fif'
raw_file = data_path + 'run1_raw.fif'
Log_file = data_path + 'logs/'+ subj + '_makeInv-py.log'
event_file = data_path + 'eve/run1.eve'
stc_file = data_path + 'ave_projon/stc/'+ subj + '_run1-spm-lh.stc' 
mne.set_log_file(fname = Log_file, overwrite = True)
print 'Logging in ' + Log_file
print 

##Load Data
raw = Raw(raw_file, preload = True)
events = mne.read_events(event_file)
#inverse_operator = read_inverse_operator(fname_inv)
label_lh = mne.read_label(fname_label_lh)

# Read epochs
epochs = mne.Epochs(raw, events, event_id, tmin, tmax, baseline = (None,0),proj = True, preload = True, name = 'rest', flat = dict(mag = magFlat, grad= gradFlat), reject=dict(mag=magRej, grad=gradRej))
print epochs
evoked = epochs.average()
print evoked
######################################################################################################33
## ##Make Inverse operator in mne-python And save it as a -inv.fif file 
# Read forward solution 
forward = mne.read_forward_solution(fname_fwd, surf_ori=True)
print forward
# Read noise covariance matrix
cov = mne.read_cov(cov_fname)
cov = mne.cov.regularize(cov, evoked.info)
print cov
inverse_operator = mne.minimum_norm.make_inverse_operator(evoked.info, forward, cov, loose= 0.5, depth = 0.8, fixed = False)
mne.minimum_norm.write_inverse_operator(fname_inv, inverse_operator)
print inverse_operator

print inverse_operator['src']
########################################################################################################
## First, we find the most active vertex in the left auditory cortex, which
## we will later use as seed for the connectivity computation
#snr = 3.0
#lambda2 = 1.0 / snr ** 2
#
#method = "dSPM"  # use dSPM method (could also be MNE or sLORETA)
#sample_vertices = [s['vertno'] for s in inverse_operator['src']]
#
##    Let's average and compute inverse, resampling to speed things up
#print evoked
#print 
#print inverse_operator
#stc = apply_inverse(evoked, inverse_operator, lambda2, method, pick_ori = "normal")
#print stc
##stc = mne.read_source_estimate(stc_file)
##
###########################################################################################
#
#snr = 1.0  # use lower SNR for single epochs
#lambda2 = 1.0 / snr ** 2
#stcs = apply_inverse_epochs(epochs, inverse_operator, lambda2, method,
#                            pick_ori="normal", return_generator=True)
#####################################################################################
