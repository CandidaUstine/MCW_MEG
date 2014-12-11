# -*- coding: utf-8 -*-
"""
Created on Thu Sep 18 10:44:14 2014

@author: custine
"""
print(__doc__)

import mne
from mne import io
import argparse

parser = argparse.ArgumentParser(description='Get input')
parser.add_argument('subj',type=str)
parser.add_argument('raw',type=str)
args=parser.parse_args()
subjID = args.subj
runName = args.raw
print subjID
print runName

###General
gradRej = 2000e-13
magRej = 3000e-15
eegRej = 100e-6
magFlat = 1e-14
gradFlat = 1000e-15
picks = []
event_id, tmin, tmax = 1, 0.0, 1.0 ##for CRM and DFNAM using 1 sec epochs for others use 2 second 

data_path = '/home/custine/MEG/data/epi_conn/' + subjID + '/'
raw_fname = data_path + runName + '_raw.fif'
event_fname = data_path + 'eve/' + runName + '.eve'
epoch_fname = data_path + 'eve/' + runName + '-epo.fif'
evoked_fname = data_path + 'ave_projon/' + runName + '-ave.fif'

#########
# #Read Raw file 
raw = mne.io.Raw(raw_fname)
print raw.info
print(raw.info['ch_names'])
picks = mne.pick_types(raw.info, meg= True, eeg = False, eog = True, stim = True, exclude = [])
print picks

# #Epoch data into 5s intervals
events = mne.make_fixed_length_events(raw, 1, start=0, stop=None, duration=2.)
mne.write_events(event_fname, events)    
print "Done " + subjID

epochs = mne.Epochs(raw, events, event_id, tmin, tmax, baseline = (None,0), picks = picks, proj = True, name = '2sec', preload = True, flat = dict(mag = magFlat, grad= gradFlat), reject= None) #dict(mag=magRej, grad=gradRej, eeg = eegRej))
print epochs
epochs.save(epoch_fname)

evoked = epochs.average(picks = None)
evoked.save(evoked_fname)
print evoked