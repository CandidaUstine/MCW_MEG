# -*- coding: utf-8 -*-
"""
Created on Thu Aug 28 14:10:45 2014
makeFwd.py
======================================================
Create a forward operator and display sensitivity maps
======================================================
"""
# Author: Eric Larson <larson.eric.d@gmail.com>
#
# License: BSD (3-clause)

print(__doc__)

import mne
from mne import viz
from mne.viz import evoked
import argparse
import condCodes as cc

parser = argparse.ArgumentParser(description='Get input')
parser.add_argument('subj',type=str)
parser.add_argument('sess',type=str) ##Left, Right etc.,
parser.add_argument('eve',type=str) 
args=parser.parse_args()
subjID = args.subj
sessID = args.sess
eve = args.eve
print subjID
print sessID
print eve

        
data_path = '/home/custine/MEG/data/krns_kr3/' +subjID+'/'+sessID
raw_fname = data_path +'/'+ subjID + '_'+ sessID +'_run1_raw.fif'
trans = '/mnt/file1/binder/KRNS/anatomies/surfaces/9367/mri/T1-neuromag/sets/COR-custine-140827-120918.fif'
src = '/mnt/file1/binder/KRNS/anatomies/surfaces/9367/bem/9367-7-src.fif'
bem = '/mnt/file1/binder/KRNS/anatomies/surfaces/9367/bem/9367-5120-5120-5120-bem-sol.fif'
subjects_diro = '/mnt/file1/binder/KRNS/anatomies/surfaces/'
fname = data_path + '/ave_projon/9367_s5_run1_Word_py-ave-7-meg-fwd.fif'

fwd = mne.make_forward_solution(raw_fname, mri=trans, src=src, bem=bem,
                                fname=fname, meg=True,
                                n_jobs=2, overwrite=True)

# convert to surface orientation for better visualization
fwd = mne.convert_forward_solution(fwd, surf_ori=True)
leadfield = fwd['sol']['data']

print("Leadfield size : %d x %d" % leadfield.shape)

grad_map = mne.sensitivity_map(fwd, ch_type='grad', mode='fixed')
mag_map = mne.sensitivity_map(fwd, ch_type='mag', mode='fixed')
#eeg_map = mne.sensitivity_map(fwd, ch_type='eeg', mode='fixed')

###############################################################################
# Show gain matrix a.k.a. leadfield matrix with sensitivity map

import matplotlib.pyplot as plt
picks_meg = mne.pick_types(fwd['info'], meg=True, eeg=False)

fig, axes = plt.subplots(1, 1, figsize=(10, 8), sharex=True)
fig.suptitle('Lead field matrix (500 dipoles only)', fontsize=14)
ax = axes
ch_type = 'meg'
picks = picks_meg
#for ax, picks, ch_type in (axes, picks_meg, 'meg'):
im = ax.imshow(leadfield[picks, :500], origin='lower', aspect='auto')
ax.set_title(ch_type.upper())
ax.set_xlabel('sources')
ax.set_ylabel('sensors')
plt.colorbar(im, ax=ax, cmap='RdBu_r')
plt.show()

plt.figure()
plt.hist([grad_map.data.ravel(), mag_map.data.ravel()],
         bins=20, label=['Gradiometers', 'Magnetometers'],
         color=['c', 'b'])
plt.legend()
plt.title('Normal orientation sensitivity')
plt.xlabel('sensitivity')
plt.ylabel('count')
plt.show()
#
print grad_map
args = dict(fmin=0.1, fmid=0.5, fmax=0.9, smoothing_steps=5)
mne.viz.plot_source_estimates(grad_map, subject='9367', subjects_dir = subjects_diro, surface = 'inflated', hemi = 'lh', time_label='Gradiometer sensitivity',fmin=0.1, fmid=0.5, fmax=0.9, smoothing_steps=5)
