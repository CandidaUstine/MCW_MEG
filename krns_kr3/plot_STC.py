# -*- coding: utf-8 -*-
"""
Created on Wed Sep  3 16:50:05 2014

@author: custine
"""



import surfer
from surfer import Brain
import mne
from mne.minimum_norm import read_inverse_operator, apply_inverse
import numpy as np
import pylab as pl

from mne.viz import mne_analyze_colormap

import surfer
from surfer.viz import Brain
from surfer import Brain



stc_file = '/home/custine/MEG/data/krns_kr3/9367/s5/ave_projon/stc/9367_s5_Noun_People_All_c1M-spm-lh.stc'

print stc_file


stc = mne.read_source_estimate(stc_file)
print stc 

colormap = mne.viz.mne_analyze_colormap(limits=[5, 10, 15]) 
brain = stc.plot(subject = 'fsaverage', surface = 'inflated', hemi = 'lh', colormap = 'hot', time_viewer = True)
#brain = stc.plot(‘fsaverage’, ‘inflated’, ‘rh’, colormap) 
#brain.scale_data_colormap(fmin=-1, fmid=10, fmax=15, transparent=False)