# -*- coding: utf-8 -*-
"""
==============================================================
Compute coherence in source space using a MNE inverse solution
==============================================================

This examples computes the coherence between a seed in the left
auditory cortex and the rest of the brain based on single-trial
MNE-dSPM inverse soltions.

"""

# Author: Martin Luessi <mluessi@nmr.mgh.harvard.edu>
#
# License: BSD (3-clause)

print(__doc__)

import numpy as np
import mne
from mne.io import Raw
from mne.minimum_norm import (apply_inverse, apply_inverse_epochs,
                              read_inverse_operator)
from mne.connectivity import seed_target_indices, spectral_connectivity
import condCodes as cc 

import surfer
from surfer.viz import Brain
from surfer import Brain
#######################################
# Set parameters
data_path = '/home/custine/MEG/data/krns_kr3/9367/s5/'
subjects_dir = '/mnt/file1/binder/KRNS/anatomies/surfaces/'
label_name_lh = 'lh.insula' #label name 

fname_label_lh = subjects_dir + 'labels/%s.label' % label_name_lh 

tmin = -0.1
tmax = 0.6  # Use a lower tmax to reduce multiple comparisons
gradRej = 2000e-13
magRej = 3000e-15
magFlat = 1e-14
gradFlat = 1000e-15
####
labelList = cc.condLabels['Noun_People']
event_id = {}
condName = {}
evoked_fname = data_path + 'ave_projon/'+ subj + '_run1_All-ave.fif'
for row in labelList:
    event_id[row[1]] = int(row[0])
    condName[row[1]] = row[1]
print event_id 
##
fname_inv = data_path + 'ave_projon/9367_s5_run1_Noun_People-ave-7-meg-inv.fif'
evoked_fname = data_path + 'ave_projon/9367_s5_run1_Noun_People-ave.fif'
raw_file = data_path + '9367_s5_run1_raw.fif'
event_file = data_path + 'eve/triggers/9367_s5_run1_Noun_People-TriggersMod.eve'
brain_image = data_path + 'coh/9367_s5_run1_Noun_People_%s.png' %label_name_lh

raw = Raw(raw_file, preload = True)
events = mne.read_events(event_file)
#event_id = {'1'}
epochs = mne.Epochs(raw, events, event_id, tmin, tmax, baseline = (None,0),proj = True, preload = True, flat = dict(mag = magFlat, grad= gradFlat), reject=dict(mag=magRej, grad=gradRej))
print epochs

snr = 3.0
lambda2 = 1.0 / snr ** 2
method = "dSPM"  # use dSPM method (could also be MNE or sLORETA)
inverse_operator = read_inverse_operator(fname_inv)
label_lh = mne.read_label(fname_label_lh)
sample_vertices = [s['vertno'] for s in inverse_operator['src']]

#    Let's average and compute inverse, resampling to speed things up
#evoked1 = epochs1.average()
evoked = mne.read_evokeds(evoked_fname, condition = 'epochs_TaggedWord')
print evoked
print 
print inverse_operator
#evoked1.resample(50)
stc = apply_inverse(evoked, inverse_operator, lambda2, method, pick_ori = "normal")

##########################################

# Restrict the source estimate to the label in the left auditory cortex
stc_label = stc.in_label(label_lh)
print 
print "STC Data..."
print stc 
print 
print "STC data in selected Label..."
print len(stc_label.data)
print stc_label.vertno ##Vertices Indices in selected STC label 

# Find number and index of vertex with most power
src_pow = np.sum(stc_label.data ** 2, axis=1)
print "src pow"
print len(src_pow)
print src_pow
print np.argmax(src_pow)
print 
seed_vertno = stc_label.vertno[0][np.argmax(src_pow)] #Indices of the vertex with max power in label 
print seed_vertno
seed_idx = np.searchsorted(stc.vertno[0], seed_vertno)  # index in original stc ##np.searchsorted: Find indices where elements should be inserted to maintain order.
print "Seed Index:", seed_idx
# Generate index parameter for seed-based connectivity analysis
n_sources = stc.data.shape[0]
print "N_Sources:", n_sources
indices = seed_target_indices([seed_idx], np.arange(n_sources))#array of seed indices and Targets indices 


# Compute inverse solution and for each epoch. By using "return_generator=True"
# stcs will be a generator object instead of a list. This allows us so to
# compute the coherence without having to keep all source estimates in memory.

snr = 1.0  # use lower SNR for single epochs
lambda2 = 1.0 / snr ** 2
stcs = apply_inverse_epochs(epochs, inverse_operator, lambda2, method,
                            pick_ori="normal", return_generator=True)

# Now we are ready to compute the coherence in the alpha and beta band.
# fmin and fmax specify the lower and upper freq. for each band, resp.
fmin = (8., 13.)
fmax = (13., 25.)
sfreq = raw.info['sfreq']  # the sampling frequency

# Now we compute connectivity. To speed things up, we use 2 parallel jobs
# and use mode='fourier', which uses a FFT with a Hanning window
# to compute the spectra (instead of multitaper estimation, which has a
# lower variance but is slower). By using faverage=True, we directly
# average the coherence in the alpha and beta band, i.e., we will only
# get 2 frequency bins
coh, freqs, times, n_epochs, n_tapers = spectral_connectivity(stcs,
    method='coh', mode='fourier', indices=indices,
    sfreq=sfreq, fmin=fmin, fmax=fmax, faverage=True, n_jobs=2)

print('Frequencies in Hz over which coherence was averaged for alpha: ')
print(freqs[0])
print('Frequencies in Hz over which coherence was averaged for beta: ')
print(freqs[1])

# Generate a SourceEstimate with the coherence. This is simple since we
# used a single seed. For more than one seeds we would have to split coh.
# Note: We use a hack to save the frequency axis as time
tmin = np.mean(freqs[0])
tstep = np.mean(freqs[1]) - tmin
coh_stc = mne.SourceEstimate(coh, vertices=stc.vertno, tmin=1e-3 * tmin,
                             tstep=1e-3 * tstep, subject='9367')
import os                              
os.environ["subjects_dir"] = "/mnt/file1/binder/KRNS/anatomies/surfaces/"
# Now we can visualize the coherence using the plot method
brain = coh_stc.plot('9367', 'inflated', 'rh', fmin=0.25, fmid=0.4,
                     fmax=0.65, time_label='Coherence %0.1f Hz',
                     subjects_dir=subjects_dir)
brain.set_data_time_index(0)
brain.show_view('lateral')
brain.save_image(brain_image)
brain.show_view('lateral')