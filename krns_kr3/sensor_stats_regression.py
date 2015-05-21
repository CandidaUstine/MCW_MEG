# -*- coding: utf-8 -*-
"""
Created on Thu May 14 15:34:58 2015

@author: custine

Usage: python sensor_stats_regression.py subjID
Example: python sensor_stats_regression.py 9367
"""
#from mne.viz import plot_topomap
from scipy import io 
import numpy as np
from mne.stats import regression
import mne 
import matplotlib.pyplot as plt
from mne import evoked

#mean = io.loadmat('/home/custine/MEG/data/krns_kr3/9367/9367_meanSel-epochs.mat')
#data = mean['epochsRsel']
#
#dm = io.loadmat('/home/custine/MEG/data/krns_kr3/9367/5attributeRatings.mat')
#dm = dm['rat']
##
##print np.size(data)
#print np.shape(data)
#print np.shape(dm)
##print data[1,1,1] ##numpy array 
##
##
#beta, stderr, t_val, p_val, mlog10_p_val = regression._fit_lm(data,dm, names = None)
#
##def plot_topomap(x, unit):
##    x.plot_topomap(ch_type='mag', scale=1, size=1.5, vmax=np.max, unit=unit,
##                   times=np.linspace(0.1, 0.2, 5))
#
#print beta['x1']
#
##plot_topomap(beta, unit='z (beta)')
#
#
#
#print len(beta)



##############################################################################
                
#epochs = mne.read_epochs('/home/custine/MEG/data/krns_kr3/9367/new-epo.fif')
## Run regression
#
#names = ['intercept', 'trial-count']
#
#intercept = np.ones((len(epochs),), dtype=np.float)
#design_matrix = np.column_stack([intercept,  # intercept
#                                 np.linspace(0, 1, len(intercept))])
#
## also accepts source estimates
#lm = regression.linear_regression(epochs, design_matrix, names)
#
#
#
        
def plot_topomap(x, unit, times):
    fig = x.plot_topomap(ch_type='mag', scale=1, size=1.5, vmax=np.max, unit=unit,
                   times= times)
    fig_fname = '/home/custine/MEG/data/krns_kr3/9511/BetaRegression/9511_Beta_1Colour.png'
    fig.savefig(fig_fname)
#
#trial_count = lm['trial-count']
#print trial_count
#
#print (trial_count.t_val)
#
#plot_topomap(ev, unit='z (beta)')
#
#plot_topomap(trial_count.t_val, unit='t')
#
#plot_topomap(trial_count.mlog10_p_val, unit='-log10 p')
#
#plot_topomap(trial_count.stderr, unit='z (error)')
    
evoked = mne.read_evokeds('/home/custine/MEG/data/krns_kr3/9511/BetaRegression/beta_regression_1Colour-ave.fif')
#evoked = mne.read_evokeds('/home/custine/MEG/data/krns_kr3/9511/BetaRegression/beta_regression_2Motion-ave.fif')
#evoked = mne.read_evokeds('/home/custine/MEG/data/krns_kr3/9511/BetaRegression/beta_regression_3Shape-ave.fif')
#evoked = mne.read_evokeds('/home/custine/MEG/data/krns_kr3/9511/BetaRegression/beta_regression_4Sound-ave.fif')
#evoked = mne.read_evokeds('/home/custine/MEG/data/krns_kr3/9511/BetaRegression/beta_regression_5UpperLimb-ave.fif')
#evoked = mne.read_evokeds('/home/custine/MEG/data/krns_kr3/9511/BetaRegression/t_1Colour-ave.fif')
#evoked = mne.read_evokeds('/home/custine/MEG/data/krns_kr3/9511/BetaRegression/t_2Motion-ave.fif')
#evoked = mne.read_evokeds('/home/custine/MEG/data/krns_kr3/9511/BetaRegression/t_3Shape-ave.fif')
#evoked = mne.read_evokeds('/home/custine/MEG/data/krns_kr3/9511/BetaRegression/t_4Sound-ave.fif')
#evoked = mne.read_evokeds('/home/custine/MEG/data/krns_kr3/9511/BetaRegression/t_5UpperLimb-ave.fif')



print 
ev = evoked[0]
print ev
print 
times=np.arange(-.1, 0.6, 0.05)
print times

import matplotlib.pyplot as plt
plot_topomap(ev, unit = 'z (beta)', times = times)
#plot_topomap(ev, unit = 't', times = times)

#fig.savefig()
#plt.show()
#plt.savefig('test.png')
#fig.savefig('test.png')

#ev.plot_topomap(times=np.linspace(0.1, 0.2, 5), ch_type='mag', scale = 1, unit = 'ev', show = True)




