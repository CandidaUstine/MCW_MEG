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
# >>cohLog_file
# License: BSD (3-clause)

print(__doc__)

import numpy as np
import mne
from mne.io import Raw
from mne.minimum_norm import (apply_inverse, apply_inverse_epochs,
                              read_inverse_operator)
from mne.connectivity import seed_target_indices, spectral_connectivity

import surfer
from surfer.viz import Brain
from surfer import Brain
import argparse

#####################################3
##Get Inputs 
parser = argparse.ArgumentParser(description='Get input')
parser.add_argument('subj',type=str) ##EP1
parser.add_argument('freq',type=str) ## alpha or beta or gamma or theta 
args=parser.parse_args()
subj = args.subj
freq = args.freq
print subj
print freq
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
if freq == 'theta':
    fmin = 4. 
    fmax = 8. 
elif freq == 'alpha':
    fmin = 8.
    fmax = 14. 
elif freq == 'beta':
    fmin = 14.
    fmax = 25.
elif freq == 'gamma':
    fmin = 25.
    fmax = 40. 

print fmin
print fmax 
##
fname_inv = data_path + 'ave_projon/'+ subj + '_run1-ave-7-meg-inv.fif'
fname_fwd = data_path + 'ave_projon/'+ subj + '_run1-ave-7-meg-fwd.fif'
evoked_fname = data_path + 'ave_projon/'+ subj + '_run1_All-ave.fif'
cov_fname = data_path + 'cov/emptyroom-cov.fif'
raw_file = data_path + 'run1_raw.fif'
cohLog_file = data_path + 'logs/'+ subj + '_coherence.log'
event_file = data_path + 'eve/run1.eve'
Lbrain_image = data_path + 'coh/run1_%s_left.png' %label_name_lh
Rbrain_image = data_path + 'coh/run1_%s_right.png' %label_name_lh
stc_file = data_path + 'ave_projon/stc/'+ subj + '_run1-spm-lh.stc' 
mne.set_log_file(fname = cohLog_file, overwrite = True)

print evoked_fname 
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
#
######################################################################################################33
## ##Make Inverse operator in mne-python 
# Read forward solution 
forward = mne.read_forward_solution(fname_fwd, surf_ori=True)
# Read noise covariance matrix
cov = mne.read_cov(cov_fname)
cov = mne.cov.regularize(cov, evoked.info)
inverse_operator = mne.minimum_norm.make_inverse_operator(evoked.info, forward, cov, loose= 0.5, depth = 0.8, fixed = False)

#######################################################################################################
# First, we find the most active vertex in the left auditory cortex, which
# we will later use as seed for the connectivity computation
snr = 3.0
lambda2 = 1.0 / snr ** 2

method = "dSPM"  # use dSPM method (could also be MNE or sLORETA)
sample_vertices = [s['vertno'] for s in inverse_operator['src']]

#    Let's average and compute inverse, resampling to speed things up
# #evoked1 = epochs1.average()
# #evoked = mne.read_evokeds(evoked_fname) #, condition = 'epochs_TaggedWord')
print evoked
print 
print inverse_operator
stc = apply_inverse(evoked, inverse_operator, lambda2, method, pick_ori = "normal")
print stc
#stc = mne.read_source_estimate(stc_file)
#
###############
# Restrict the source estimate to the label in the left auditory cortex
stc_label = stc.in_label(label_lh)
print 
print "STC Data..."
print stc 
print 
print "STC data in selected Label..."
print len(stc_label.data)
print stc_label.vertno
#
#################
# Find number and index of vertex with most power
src_pow = np.sum(stc_label.data ** 2, axis=1)
print "src pow"
print len(src_pow)
print src_pow
print np.argmax(src_pow)
print 
seed_vertno = stc_label.vertno[0][np.argmax(src_pow)] #Indices of the vertex with max power in label 
print "Seed Vertex Number:", seed_vertno
seed_idx = np.searchsorted(stc.vertno[0], seed_vertno)  # index in original stc ##np.searchsorted: Find indices where elements should be inserted to maintain order.
print "Seed Index:", seed_idx
# Generate index parameter for seed-based connectivity analysis
n_sources = stc.data.shape[0]
print "N_Sources:", n_sources
indices = seed_target_indices([seed_idx], np.arange(n_sources))#array of seed indices and Targets indices 
#indices = seed_target_indices(np.arange(n_sources), np.arange(n_sources)) RESULTS IN A MEMORY ERROR 
#
print 
#########################################################################################
# Compute inverse solution for each epoch. By using "return_generator=True"
# stcs will be a generator object instead of a list. This allows us so to
# compute the coherence without having to keep all source estimates in memory.

snr = 1.0  # use lower SNR for single epochs
lambda2 = 1.0 / snr ** 2
method = "dSPM"
stcs = apply_inverse_epochs(epochs, inverse_operator, lambda2, method,
                            pick_ori="normal", return_generator=True)
################################################################################################3
## Now we are ready to compute the coherence in the alpha and beta band.
## fmin and fmax specify the lower and upper freq. for each band, resp.
#fmin = (8., 13.)
#fmax = (13., 25.)
####Only the Alpha Band                                                         
##fmin = 8.
##fmax = 14.                            
#sfreq = raw.info['sfreq']  # the sampling frequency
#
## Now we compute connectivity. To speed things up, we use 2 parallel jobs
## and use mode='fourier', which uses a FFT with a Hanning window
## to compute the spectra (instead of multitaper estimation, which has a
## lower variance but is slower). By using faverage=True, we directly
## average the coherence in the alpha and beta band, i.e., we will only
## get 2 frequency bins
#coh, freqs, times, n_epochs, n_tapers = spectral_connectivity(stcs,
#    method='coh', mode='fourier', indices=indices,
#    sfreq=sfreq, fmin=fmin, fmax=fmax, faverage=True, n_jobs=2)
#
#print('Frequencies in Hz over which coherence was averaged for alpha: ')
#print(freqs[0])
#print('Frequencies in Hz over which coherence was averaged for beta: ')
#print(freqs[1])
#print 
#print coh 
##
#np.savetxt('/home/custine/MEG/data/epi_conn/EP3/coh/coherence.txt', coh, delimiter = ' ')
#################################################################################################3
## Generate a SourceEstimate with the coherence. This is simple since we
## used a single seed. For more than one seeds we would have to split coh.
## Note: We use a hack to save the frequency axis as time
#tmin = np.mean(freqs[0])
#tstep = np.mean(freqs[1]) - tmin
#
#coh_stc = mne.SourceEstimate(coh, vertices=stc.vertno, tmin=1e-3 * tmin,
#                             tstep=1e-3 * tstep, subject='EP3')
#                             
#print coh_stc 
#import os                              
#os.environ["subjects_dir"] = "/home/custine/MRI/structurals/subjects/"
#
## Now we can visualize the coherence using the plot method
#brainR = coh_stc.plot('EP3', 'inflated', 'rh', fmin=0.25, fmid=0.4,
#                     fmax=0.65, time_label='Coherence %0.1f Hz',
#                     subjects_dir=subjects_dir)
#brainR.set_data_time_index(0)
#brainR.show_view('lateral')
#brainR.save_image(Rbrain_image)
#
## Now we can visualize the coherence using the plot method
#brainL = coh_stc.plot('EP3', 'inflated', 'lh', fmin=0.25, fmid=0.4,
#                     fmax=0.65, time_label='Coherence %0.1f Hz',
#                     subjects_dir=subjects_dir)
#brainL.set_data_time_index(0)
#brainL.show_view('lateral')
#brainL.save_image(Lbrain_image)

####################################################################################3
##

##coh, freqs, times, n_epochs, n_tapers = spectral_connectivity(stcs, method='coh', mode='fourier', indices=indices, sfreq=sfreq, 
##                                                              fmin=fmin, fmax=fmax, faverage=True, n_jobs=2)
##print coh    
##print freqs
##print n_epochs
##print n_tapers
##print 
##    
##np.savetxt('/home/custine/MEG/data/epi_conn/EP3/coh/coherence.txt', coh, delimiter = ' ')
##    
#######################################################################################3
#######Connectivity Circle Plotting############
print inverse_operator['src']
from mne.viz import circular_layout, plot_connectivity_circle
# Get labels for FreeSurfer 'aparc' cortical parcellation with 34 labels per hemi
labels, label_colors = mne.labels_from_parc(subj, parc='aparc', subjects_dir=subjects_dir) ##or use read_labels_from_annot() 
print labels
print 
src = inverse_operator['src']
label_ts = mne.extract_label_time_course(stcs, labels, src,mode = 'mean', return_generator=True)
print label_ts
###################################33

#################################################3333
# Now we are ready to compute the connectivity in the alpha band. Notice
# from the status messages, how mne-python: 1) reads an epoch from the raw
# file, 2) applies SSP and baseline correction, 3) computes the inverse to
# obtain a source estimate, 4) averages the source estimate to obtain a
# time series for each label, 5) includes the label time series in the
# connectivity computation, and then moves to the next epoch. This
# behaviour is because we are using generators and allows us to
# compute connectivity in computationally efficient manner where the amount
# of memory (RAM) needed is independent from the number of epochs.
#fmin = 4.
#fmax = 8.
sfreq = raw.info['sfreq']  # the sampling frequency
con_methods = ['coh', 'imcoh']
con, freqs, times, n_epochs, n_tapers = spectral_connectivity(label_ts,
        method=con_methods, mode='fourier', sfreq=sfreq, fmin=fmin,
        fmax=fmax, faverage=True, n_jobs=2)
        
print len(con)
#np.savetxt('/home/custine/MEG/data/epi_conn/EP3/coh/coherence.txt', con)
# con is a 3D array, get the connectivity for the first (and only) freq. band
# for each method
con_res = dict()
for method, c in zip(con_methods, con):
    con_res[method] = c[:, :, 0]
print len(con_res)

#### Now, we visualize the connectivity using a circular graph layout
# First, we reorder the labels based on their location in the left hemi
label_names = [label.name for label in labels]
lh_labels = [name for name in label_names if name.endswith('lh')]

# Get the y-location of the label
label_ypos = list()
for name in lh_labels:
    idx = label_names.index(name)
    ypos = np.mean(labels[idx].pos[:, 1])
    label_ypos.append(ypos)

# Reorder the labels based on their location
lh_labels = [label for (ypos, label) in sorted(zip(label_ypos, lh_labels))]

# For the right hemi
rh_labels = [label[:-2] + 'rh' for label in lh_labels]

# Save the plot order and create a circular layout
node_order = list()
node_order.extend(lh_labels[::-1])  #reverse the order
node_order.extend(rh_labels)

node_angles = circular_layout(label_names, node_order, start_pos=90,
                              group_boundaries=[0, len(label_names) / 2])

# Plot the graph using node colors from the FreeSurfer parcellation. We only
# show the 300 strongest connections.
plot_connectivity_circle(con_res['coh'], label_names, n_lines=300,
                         node_angles=node_angles, node_colors=label_colors,
                         title='All-to-All Connectivity(Coherence)')
import matplotlib.pyplot as plt
plt.savefig('/home/custine/MEG/data/epi_conn/' + subj + '/coh/' + subj + '_circle_' + freq + '.png', facecolor='black')

# Plot connectivity for both methods in the same plot
fig = plt.figure(num=None, figsize=(8, 4), facecolor='black')
no_names = [''] * len(label_names)
for ii, method in enumerate(con_methods):
    plot_connectivity_circle(con_res[method], no_names, n_lines=300,
                             node_angles=node_angles, node_colors=label_colors,
                             title=method, padding=0, fontsize_colorbar=6,
                             fig=fig, subplot=(1, 2, ii + 1))
plt.savefig('/home/custine/MEG/data/epi_conn/' + subj + '/coh/' + subj + '_circle_coh_imcoh_' + freq + '.png', facecolor='black')
#plt.show()
    