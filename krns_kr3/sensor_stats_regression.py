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
import sys


def stats(subjID, coeff, atrb):
    if coeff == 'beta':
        c = 'beta_regression'
    elif coeff == 't':
        c = 't'
    else:
        print "Coefficient chosen not available..." 
        
    evoked_fname = '/home/custine/MEG/data/krns_kr3/' +subjID+'/BetaRegression/' + c + '_' + atrb + '_20150525-ave.fif' 
    print evoked_fname 
    fig_fname = '/home/custine/MEG/data/krns_kr3/' +subjID+'/BetaRegression/' + subjID + '_'+ c + '_' + atrb + '_20150525.png'
    print fig_fname
    
    evoked = mne.read_evokeds(evoked_fname)
    print evoked
    ev = evoked[0]
    print ev

    times=np.arange(-.1, 0.6, 0.05)
    print times
    
#    import matplotlib.pyplot as plt
    plot_topomap(ev, unit = coeff , times = times, fig_fname = fig_fname)

##############################################################################
                
def plot_topomap(x, unit, times, fig_fname):
    fig = x.plot_topomap(ch_type='mag', scale=1, size=1.5, vmax=np.max, unit=unit,
                   times= times)
    fig.savefig(fig_fname)

##############################################################################

if __name__ == "__main__":
    ####### Get Input ########
    subjID = sys.argv[1]
    coeff = sys.argv[2] #beta or t 
    atrb = sys.argv[3] #attribute 1Colour. 2Motion.. etc., 
    print 
    print "Subject ID:" + subjID
    
    
    stats(subjID, coeff, atrb)
