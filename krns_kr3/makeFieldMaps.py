# -*- coding: utf-8 -*-
"""
Created on Thu Aug 28 16:19:43 2014

@author: custine
makeFieldMaps.py 
"""

import numpy as np
import mne
import argparse
from mne import make_field_map, read_evoked

#example
#run sensor_avgFieldmapinTime.py ga_MaskedMM_All_meg-n21-goodC 4 .350 .450


parser = argparse.ArgumentParser(description='Get input')
parser.add_argument('ave_name', type = str)
parser.add_argument('set',type=int)
parser.add_argument('time1',type=float)
parser.add_argument('time2',type=float)

args=parser.parse_args()

##script for creating average field map

data_path = '/home/custine/MEG/data/krns_kr3/9367/s5/'
evoked_fname = data_path + 'ave_projon/9367_s5_Noun_Place_All-ave.fif'
subjects_dir = '/mnt/file1/binder/KRNS/anatomies/surfaces/'
trans_fname = '/mnt/file1/binder/KRNS/anatomies/surfaces/9367/mri/T1-neuromag/sets/COR-custine-140827-120918.fif'
# If trans_fname is set to None then only MEG estimates can be visualized

condition = 1
evoked = read_evoked(evoked_fname, baseline=(-0.2, 0.0))

# Compute the field maps to project MEG and EEG data to MEG helmet
# and scalp surface
maps = make_field_map(evoked, trans_fname=trans_fname, subject='9367',
                      subjects_dir=subjects_dir, n_jobs=1)

# explore several points in time
[evoked.plot_field(maps, time=time) for time in [0.09, .11]]

evoked.save('/home/custine/MEG/data/krns_kr3/9367/s5/results/fieldmaps/9367_s5_' + str(args.ave_name) + '_All-'+'-'+str(args.time1)+'-'+str(args.time2)+'-ave.fif')
#evoked.save(data_path + args.prefix+'-'+str(args.set)+'-'+str(args.time1)+'-'+str(args.time2)+'-ave.fif')

# evoked = mne.fiff.read_evoked('ga_BaleenHP_All_meg-n24-goodC-ave.fif',setno=6)
# time_idx = np.where((evoked.times >= 0.35) & (evoked.times <= 0.450))[0]
# for x in time_idx:
#    evoked.data[:,x] = data
# 
# evoked.save('ga_BaleenHP_All_meg-n24-goodC-350-450-ave.fif')
