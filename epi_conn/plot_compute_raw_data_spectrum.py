# -*- coding: utf-8 -*-
"""
Created on Fri Sep 19 15:31:01 2014
==================================================
Compute the power spectral density of raw data
==================================================

This script shows how to compute the power spectral density (PSD)
of measurements on a raw dataset. It also show the effect of applying SSP
to the data to reduce ECG and EOG artifacts.
"""
# Authors: Alexandre Gramfort <alexandre.gramfort@telecom-paristech.fr>
#          Martin Luessi <mluessi@nmr.mgh.harvard.edu>
#          Eric Larson <larson.eric.d@gmail.com>
# License: BSD (3-clause)

print(__doc__)

import numpy as np
import matplotlib.pyplot as plt
import argparse
import mne
from mne import read_proj, read_selection, fiff, io
from mne.io import pick
from mne.datasets import sample

###############################################################################
# Get Input 
parser = argparse.ArgumentParser(description='Get input')
parser.add_argument('subj',type=str)
args=parser.parse_args()
subjID = args.subj

# Set parameters
data_path = '/home/custine/MEG/data/epi_conn/'+ subjID + '/' #+ sess +'/'
raw_fname = data_path + 'run3_raw.fif'
fig_fname = data_path + 'fig/' + subjID +'_run3' + '-magonly.png'


# Setup for reading the raw data
#raw = io.Raw(raw_fname, preload=True)
raw = fiff.Raw(raw_fname, preload = True)
raw.info['bads'] += ['MEG 2242']  # bads + 2 more

## Add SSP projection vectors to reduce EOG and ECG artifacts
#projs = read_proj(proj_fname)
#raw.add_proj(projs, remove_existing=True)


tmin, tmax = 0, 500  # use the first 120s of data
fmin, fmax = 2, 100  # look at frequencies between 2 and 300Hz
n_fft = 2048  # the FFT size (n_fft). Ideally a power of 2

plt.ion()

# Let's first check out all channel types
raw.plot_psds(area_mode='range', tmax=10.0)

## Now let's focus on a smaller subset:
## Pick MEG magnetometers in the Left-temporal region
#selection = mne.read_selection("Left-temporal")
#print selection
picks = mne.io.pick.pick_types(raw.info, meg='mag', eeg=False, eog=False,
                        stim=False, exclude='bads') #meg = 'mag' or 'grad'

##Pick all channels 
#picks = []
#for i in range(raw.info['nchan']):
#    picks.append(i)
            
print picks
## Let's just look at the first few channels for demonstration purposes
#picks = picks[:100]

plt.figure()
ax = plt.axes()
raw.plot_psds(tmin=tmin, tmax=tmax, fmin=fmin, fmax=fmax, n_fft=n_fft,
              n_jobs=1, proj=False, ax=ax, color=(0, 0, 1),  picks=picks)

# And now do the same with SSP applied
raw.plot_psds(tmin=tmin, tmax=tmax, fmin=fmin, fmax=fmax, n_fft=n_fft,
              n_jobs=1, proj=True, ax=ax, color=(0, 1, 0), picks=picks)

## And now do the same with SSP + notch filtering
#raw.notch_filter(np.arange(60, 241, 60), picks=picks, n_jobs=1)
#raw.plot_psds(tmin=tmin, tmax=tmax, fmin=fmin, fmax=fmax, n_fft=n_fft,
#              n_jobs=1, proj=True, ax=ax, color=(1, 0, 0), picks=picks)

#ax.set_title('All Channels')
plt.legend(['Without SSP-magonly', 'With SSP', 'SSP + Notch'])
plt.savefig(fig_fname)
#plt.show(block = True) #To keep the graphing window open when running outside ipython environment


