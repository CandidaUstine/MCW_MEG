# -*- coding: utf-8 -*-
"""
Created on Thu Oct 23 17:00:34 2014

@author: custine
"""

# -*- coding: utf-8 -*-
"""
==============================================================
power envelope
==============================================================
example: python source_mne_label_power-envelope.py EP6 beta CRM-noise
"""


print(__doc__)

import numpy as np
import matplotlib.pyplot as plt
import mne
from mne.io import Raw
from mne.minimum_norm import (apply_inverse, apply_inverse_epochs,
                              read_inverse_operator)
from mne.connectivity import seed_target_indices, spectral_connectivity
from mne import read_labels_from_annot

import surfer
from surfer.viz import Brain
from surfer import Brain
import argparse

#####################################3
##Get Inputs 
parser = argparse.ArgumentParser(description='Get input')
parser.add_argument('subj',type=str) ##EP1
parser.add_argument('freq',type=str) ## alpha or beta or gamma or theta 
parser.add_argument('run',type=str)

args=parser.parse_args()
subj = args.subj
freq = args.freq
run = args.run
print subj
print freq
#######################################

# Set parameters
data_path = '/home/custine/MEG/data/epi_conn/' + subj + '/'
subjects_dir = '/home/custine/MRI/structurals/subjects/'

gradRej = 5000e-13
magRej = 4000e-15
magFlat = 1e-14
gradFlat = 1000e-15

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

event_id = 1
tmin = 0
tmax = 2.0 
#################################3
#############VARIABLES##############
###################################
if run == 'CRM':
    event_id = 2
    tmin = 0
    tmax = 1.0  
elif run == 'DFNAM':
    event_id = 2
    tmin = 0
    tmax = 2.0

#fname_inv = data_path + 'ave_projon/'+ subj + '_run1-ave-7-meg-inv.fif'
fname_fwd = data_path + 'ave_projon/'+ subj + '_' + run + '-noise-ave-7-meg-fwd.fif' #for EP2 _All For EP% and EP^ also do CRM and DFNAM incl run1 
#evoked_fname = data_path + 'ave_projon/'+ subj + '_' + run + '_All-ave.fif' #for EP2 All
#coh_fname = data_path + 'coh/' + subj + '_' + freq + '_subj_connectivityMatrix.txt'
#plv_fname = data_path + 'coh/' + subj+ '_' + freq + '_subj_plv_ConnectivityMatrix.txt'
#pli_fname = data_path + 'coh/' + subj+ '_' + freq + '_subj_pli_ConnectivityMatrix.txt'
cov_fname = data_path + 'cov/emptyroom-cov.fif'
raw_file = data_path + run + '_raw.fif'
cohLog_file = data_path + 'logs/'+ subj + '_' + freq + '_' + run + '_coherence.log'
event_file = data_path + 'eve/' + run + '.eve' 
mne.set_log_file(fname = cohLog_file, overwrite = True)
stc_fname = data_path + 'ave_projon/stc_py/'+ subj + '_' + run
powenv_fname = data_path + 'coh/' + subj +'_' + freq + '_' + run + '-noise_powEnv_LabelsMatrix.txt'
print fname_fwd 
print 

##Load Data
raw = Raw(raw_file, preload = True)
raw.filter(fmin, fmax, picks = None)
print raw.info 
print 'Raw data filtered to the desired freq band: ' + freq
events = mne.read_events(event_file)
#inverse_operator = read_inverse_operator(fname_inv)
#label_lh = mne.read_label(fname_label_lh)

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
##################################################################
# ##Let's average and compute inverse, resampling to speed things up
# #evoked1 = epochs1.average()
# #evoked = mne.read_evokeds(evoked_fname) #, condition = 'epochs_TaggedWord')
print evoked
print 
print inverse_operator
stc = apply_inverse(evoked, inverse_operator, lambda2, method, pick_ori = "normal")
print stc
stc.save(stc_fname)
################
## Restrict the source estimate to the label in the left auditory cortex
#stc_label = stc.in_label(label_lh)
#print 
#print "STC Data..."
#print stc 
#print 
#print "STC data in selected Label..."
#print len(stc_label.data)
#print stc_label.vertno
##
##################src_pow = np.sum(stc_label.data ** 2, axis=1)
## Find number and index of vertex with most power
#src_pow = np.sum(stc_label.data ** 2, axis=1)
#print "src pow"
#print len(src_pow)
#print src_pow
#print np.argmax(src_pow)
#print 
#seed_vertno = stc_label.vertno[0][np.argmax(src_pow)] #Indices of the vertex with max power in label 
#print "Seed Vertex Number:", seed_vertno
#seed_idx = np.searchsorted(stc.vertno[0], seed_vertno)  # index in original stc ##np.searchsorted: Find indices where elements should be inserted to maintain order.
#print "Seed Index:", seed_idx
## Generate index parameter for seed-based connectivity analysis
#n_sources = stc.data.shape[0]
#print "N_Sources:", n_sources
#indices = seed_target_indices([seed_idx], np.arange(n_sources))#array of seed indices and Targets indices 
##indices = seed_target_indices(np.arange(n_sources), np.arange(n_sources)) RESULTS IN A MEMORY ERROR 
##
#print 
##########################################################################################
## Compute inverse solution for each epoch. By using "return_generator=True"
## stcs will be a generator object instead of a list. This allows us so to
## compute the coherence without having to keep all source estimates in memory.
#
#snr = 1.0  # use lower SNR for single epochs
#lambda2 = 1.0 / snr ** 2
#method = "dSPM"
#stcs = apply_inverse_epochs(epochs, inverse_operator, lambda2, method,
#                            pick_ori="normal", return_generator=True)
#
##vertices_to = mne.grade_to_vertices('fsaverage', grade = 5)                            
##stcs  = mne.morph_data(subj, 'fsaverage', stcs_orig, grade = vertices_to)
##teststc_fname = data_path + 'ave_projon/stc/'+ subj + '_run1-spm-test-lh.stc' 
###stcs.save(teststc_fname)
##
########################################################################################3
########Connectivity Circle Plotting############
#print inverse_operator['src']
from mne.viz import circular_layout, plot_connectivity_circle
# Get labels for FreeSurfer 'aparc' cortical parcellation with 34 labels per hemi
labels, label_colors = mne.labels_from_parc(subj, parc='aparc', subjects_dir=subjects_dir) ##or use read_labels_from_annot() 
print labels

label_names = [label.name for label in labels]
#for label in label_names:
#    print label 
    
lh_labels = [name for name in label_names if name.endswith('lh')]

###############################Labels Temporal 
import numpy as np
#temporals = ['lh.superiortemporal', 'lh.inferiortemporal' , 'lh.middletemporal',  'lh.transversetemporal', 'lh.entorhinal','lh.temporalpole', 'lh.parahippocampal']
num_plots = 20
if subj == 'EP1':
    x = 4001
elif subj == 'EP8':
    x = 2001
else: x = 3001

if run == 'CRM': x = 1001 #for CRM and DFNAM 
elif run == 'DFNAM': x = 2001


new = np.empty([0, x])
print new.shape
colormap = plt.cm.hsv ##http://matplotlib.org/1.2.1/examples/pylab_examples/show_colormaps.html
plt.gca().set_color_cycle([colormap(i) for i in np.linspace(0, 0.9, num_plots)]) 
for label_name in lh_labels:
   
    fname_label_lh = subjects_dir + subj +'/label/lh.%s.label' % label_name[:-3] 
    print fname_label_lh
    label_lh = mne.read_label(fname_label_lh)
    stc_label = stc.in_label(label_lh)
    a = stc_label.data 
    a = a.transpose() 
    src_pow = a ** 2
    print src_pow.shape
    src_pow = np.mean(src_pow, axis = 1)
    print src_pow
    src_pow = np.asmatrix(src_pow)
    print src_pow.shape   
    new = np.append(new, src_pow, 0)
    print new.shape

    print 
    fname_label_rh = subjects_dir + subj +'/label/rh.%s.label' % label_name[:-3] 
    print fname_label_rh
    label_rh = mne.read_label(fname_label_rh)
    stc_label_rh = stc.in_label(label_rh)
    ar = stc_label_rh.data 
    ar = ar.transpose() 
    src_pow_r = ar ** 2  
    print src_pow_r.shape
    src_pow_r = np.mean(src_pow_r, axis = 1)
    print src_pow_r
    src_pow_r = np.asmatrix(src_pow_r)
    print src_pow_r.shape   
    new = np.append(new, src_pow_r, 0)
    print new.shape    


np.savetxt(powenv_fname, new, delimiter = ',')
    
    
########## PLOTTING #################   
#    #src_po = stc_label.data ** 2 
#    #np.savetxt('temp.txt', a)
#    print len(src_pow)
#    #np.savetxt('temp_pow.txt', src_pow.mean(1))
#    plt.figure()
#    print len(stc_label.times)
#    plt.ylim(0, 20)
#    plt.plot(stc_label.times, src_pow.mean(1))
##    plt.legend(label_name, loc='upper center', 
##           bbox_to_anchor=[0.5, 1.1], 
##           columnspacing=1.0, labelspacing=0.0,
##           handletextpad=0.0, handlelength=1.5,
##           fancybox=True, shadow=True)
#    plt.ylim(0, 20)
#
#    plt.xlabel('Time (s)')
#    plt.ylabel('mean source power across all vertices within label')
#    plt.savefig('/home/custine/MEG/data/epi_conn/' + subj + '/coh/' + subj + '_power_envelope_' + freq + '_' + label_name + '.png', facecolor='white')
#   # plt.show()