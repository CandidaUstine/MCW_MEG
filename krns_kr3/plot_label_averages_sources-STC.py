# -*- coding: utf-8 -*-
"""
Created on Wed Sep  3 10:36:57 2014
====================================================
Extracting the time series of activations in a label
====================================================

We first apply a dSPM inverse operator to get signed activations
in a label (with positive and negative values) and we then
compare different strategies to average the times series
in a label. We compare a simple average, with an averaging
using the dipoles normal (flip mode) and then a PCA,
also using a sign flip.
"""
# Author: Alexandre Gramfort <alexandre.gramfort@telecom-paristech.fr>
#
# License: BSD (3-clause)

print(__doc__)

import mne
from mne.minimum_norm import read_inverse_operator, apply_inverse
import numpy as np
import pylab as pl


stc_file = '/home/custine/MEG/data/krns_kr3/9367/s5/ave_projon/stc/9367_s5_Noun_People_All_c1M-spm-lh.stc'

print stc_file


stc = mne.read_source_estimate(stc_file)

n_vertices, n_samples = stc.data.shape
print("stc data size: %s (nb of vertices) x %s (nb of samples)"
      % (n_vertices, n_samples))

## View source activations
#import matplotlib.pyplot as plt
#plt.plot(stc.times, stc.data[::100, :].T)
#plt.xlabel('time (ms)')
#plt.ylabel('Source amplitude')
#plt.show()

##########################################################################################################
#
#data_path = sample.data_path()
#label = 'Aud-lh'
label_fname = '/home/custine/MEG/data/krns_kr3/9367/s5/ave_projon/stc/label/lh.insula.label'
fname_inv = '/home/custine/MEG/data/krns_kr3/9367/s5/ave_projon/9367_s5_Noun_People_All-ave-7-meg-inv.fif'
fname_evoked = '/home/custine/MEG/data/krns_kr3/9367/s5/ave_projon/9367_s5_Noun_People_All-ave.fif'
#
snr = 3.0
lambda2 = 1.0 / snr ** 2
method = "dSPM"  # use dSPM method (could also be MNE or sLORETA)
#
## Load data
evoked = mne.read_evokeds(fname_evoked, condition=0, baseline=(None, 0))
inverse_operator = read_inverse_operator(fname_inv)
src = inverse_operator['src']
#
## Compute inverse solution
pick_ori = "normal"  # Get signed values to see the effect of sign filp
stc = apply_inverse(evoked, inverse_operator, lambda2, method)
#
label = mne.read_label(label_fname)
#######################################################################################################3
#
##################################################FROM SEMPRMM ELEN SCRIPT.########################### 
#values1, times1, vertices1 = mne.label_time_courses(label_fname, stc_file)
#values1 = np.mean(values1,0)
##print values1.shape
#print "Number of vertices : %d" % len(vertices1)
#
#times1=times1*1000
#
#####Plotting Parameters####
#xmin,xmax = [-100, 610]
#ymin,ymax = [0, 8]
#lWidth = 4
#
#color1 = 'k'
#lineStyle1 = 'solid'
#lineLabel1 = 'dir related'
#
##        'weight' : 'bold',
#font = {'size'   : 20}
#
#pl.rc('font', **font)
#
##########################
## View source activations
#
#pl.clf()
#pl.plot(times1, values1.T,color=color1,linewidth=lWidth,linestyle=lineStyle1)
#
#pl.plot(times1,values1.T*0,color='k')
##pl.legend((lineLabel1,lineLabel2),loc="upper left")
#pl.axvline(x=0,ymin=0,ymax=1,color='k')
#pl.ylim([ymin,ymax])
#pl.xlim([xmin,xmax])
#pl.box('off') # turn off the box frame 
#pl.axhline(y=0,xmin=0,xmax=1,color='k',linewidth=2) #draw a thicker horizontal line at 0			
#pl.axvline(x=0,ymin=0,ymax=1,color='k',linewidth=2) #draw a vertical line at 0 that goes 1/8 of the range in each direction from the middle (e.g., if the range is -8:8, =16, 1/8 of 16=2, so -2:2).
#pl.tick_params(axis='both',right='off',top='off',left='off')
#pl.yticks(np.array([]))
#pl.axhline(y=5,xmin=.12,xmax=.16,color='k',linewidth=1)
#pl.axvline(x=100,ymin=0,ymax=.03,color='k')
#pl.axvline(x=300,ymin=0,ymax=.03,color='k')
#pl.axvline(x=500,ymin=0,ymax=.03,color='k')
#pl.xticks(np.array([]))
#
#pl.xlabel('time (ms)')
#pl.ylabel('Source amplitude')
#pl.axvspan(300, 500, color='k', alpha=0.1)
##pl.title('Activations in Label : %s' % label1)
#pl.ticklabel_format(style='plain',axis='x')
#pl.rcParams.update({'font.size': 12})
#pl.show()


######################################################################################################
#################mne - py sceript continued... 
#
stc_label = stc.in_label(label)
mean = stc.extract_label_time_course(label, src, mode='mean')
mean_flip = stc.extract_label_time_course(label, src, mode='mean_flip')
pca = stc.extract_label_time_course(label, src, mode='pca_flip')
#
print("Number of vertices : %d" % len(stc_label.data))

# View source activations
import matplotlib.pyplot as plt
plt.figure()
plt.plot(1e3 * stc_label.times, stc_label.data.T, 'k', linewidth=0.5)
h0, = plt.plot(1e3 * stc_label.times, mean.T, 'r', linewidth=3)
h1, = plt.plot(1e3 * stc_label.times, mean_flip.T, 'g', linewidth=3)
h2, = plt.plot(1e3 * stc_label.times, pca.T, 'b', linewidth=3)
plt.legend([h0, h1, h2], ['mean', 'mean flip', 'PCA flip'])
plt.xlabel('Time (ms)')
plt.ylabel('Source amplitude')
plt.title('Activations in Label : %s' % label)
#plt.show()

#######################################################################################








