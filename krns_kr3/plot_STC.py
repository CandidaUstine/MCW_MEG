# -*- coding: utf-8 -*-
"""
Created on Wed Sep  3 16:50:05 2014

@author: custine
Example: python plot_STC.py 9367 s5 Sentence4W

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
import argparse

###################################################################################
##Get Inputs 
parser = argparse.ArgumentParser(description='Get input')
parser.add_argument('subj',type=str) ##EP1
parser.add_argument('sess',type=str) ##Session s5 
parser.add_argument('tag',type=str)
#parser.add_argument('freq',type=str) ## alpha or beta or gamma or theta 

args=parser.parse_args()
subj = args.subj
sess = args.sess
#freq = args.freq
tag = args.tag
print subj

####################################################P_t = [];
################################
# Set parameters
data_path = '/home/custine/MEG/data/krns_kr3/' + subj + '/' + sess + '/'
subjects_dir = '/mnt/file1/binder/KRNS/anatomies/surfaces/'
stc_fname = data_path + 'ave_projon/stc/' + subj + '_' + sess + '_' + tag + '_All_c1M-spm-lh.stc'

#stc_file = '/home/custine/MEG/data/krns_kr3/9367/s5/ave_projon/stc/stc_py/9367_s5_run1_Sentence-lh.stc' #9367_s5_Noun_People_All_c1M-spm-lh.stc'
stcMAT_fname = data_path + 'ave_projon/stc/' + subj + '_' + sess + '_' + tag + '_All_c1M-spm-lh_AllVertices.txt'
print stc_fname


stc = mne.read_source_estimate(stc_fname)
print stc 
print 'Shape of STC'
print np.shape(stc.data)

j_labels = mne.stc_to_label(stc, src = '9367', subjects_dir = '/mnt/file1/binder/KRNS/anatomies/surfaces/')
print 'Jane Labels' 
print j_labels[0]
print

#np.savetxt(stcMAT_fname, stc.data, delimiter = ',')

vert,sampLen = np.shape(stc.data)
print sampLen

################################################################################################################################
#######################################All Vertices - Computations################################################################
################################################################################################################################
#x = sampLen ## Number of samples in the data (trials)
#
#new = np.empty([0, x])
#print new.shape
#   
#a = stc.data 
#print a 
#a = np.absolute(a)
#a = a.transpose()
#print a.shape
#print 
#print vert
#print sampLen
#for x in range(vert): #vert):
##    print a.shape
#    base = a[1:1001, x]
##    print base.shape
#    base_pow = base ** 2 
#    base_pow = np.mean(base_pow)
##    print base_pow.shape
##    print base_pow
###### ##Baseline normalisation 
#    src = a[:,x]
#    src = np.asmatrix(src)
###    print 'Src shape'
###    print src.shape
#    src_pow = src/base_pow    
#    new = np.append(new, src_pow, 0)
#print new.shape
#np.savetxt(stcMAT_fname, new, delimiter = ',')


################################################################################################################################
#######################################Within Label Computations################################################################
################################################################################################################################
#colormap = mne.viz.mne_analyze_colormap(limits=[5, 10, 15]) 
#brain = stc.plot(subject = 'fsaverage', surface = 'inflated', hemi = 'lh', colormap = 'hot', time_viewer = True)
###brain = stc.plot(‘fsaverage’, ‘inflated’, ‘rh’, colormap) 
###brain.scale_data_colormap(fmin=-1, fmid=10, fmax=15, transparent=False)

from mne.viz import circular_layout, plot_connectivity_circle
# Get labels for FreeSurfer 'aparc' cortical parcellation with 34 labels per hemi
subjects_dir = '/mnt/file1/binder/KRNS/anatomies/surfaces/'################################################################################################################################

labels, label_colors = mne.labels_from_parc(subj, parc='aparc', subjects_dir=subjects_dir) ##or use read_labels_from_annot() 
label_names = [label.name for label in labels]
lh_labels = [name for name in label_names if name.endswith('lh')]

###############################Labels Temporal 
#temporals = ['lh.superiortemporal', 'lh.inferiortemporal' , 'lh.middletemporal',  'lh.transversetemporal', 'lh.entorhinal','lh.temporalpole', 'lh.parahippocampal']
x = sampLen ## Number of samples in the data (trials)

new = np.empty([0, x])
print new.shape
for label_name in lh_labels:
    print 
    fname_label_lh = subjects_dir + subj +'/label/lh.%s.label' % label_name[:-3] 
    print fname_label_lh
    label_lh = mne.read_label(fname_label_lh)
    stc_label = stc.in_label(label_lh)
    a = stc_label.data 
    a = np.absolute(a)
    #    meanA = np.mean(a, axis = 0)
    #    meanA = meanA.transpose()
    #    meanA = np.asmatrix(meanA)
    a = a.transpose() 
    src_pow = a ** 2
    src_pow = np.mean(src_pow, axis = 1)
    src_pow = np.asmatrix(src_pow)
    
    basesrc_pow = src_pow[:, 1:1001]
    basesrc_pow = np.mean(basesrc_pow, axis = 1)
    print basesrc_pow.shape
    src_pow = src_pow/basesrc_pow
    print src_pow.shape
    
    new = np.append(new, src_pow, 0)
    print new.shape

    fname_label_rh = subjects_dir + subj +'/label/rh.%s.label' % label_name[:-3] 
    print fname_label_rh
    label_rh = mne.read_label(fname_label_rh)
    stc_label_rh = stc.in_label(label_rh)
    ar = stc_label.data 
    ar = np.absolute(ar)
#        meanAr = np.mean(ar, axis = 0)
#        meanAr = meanAr.transpose()
#        meanAr = np.asmatrix(meanAr)
    ar = ar.transpose() 
    src_pow_r = ar ** 2  
    src_pow_r = np.mean(src_pow_r, axis = 1)
    src_pow_r = np.asmatrix(src_pow_r)
    
    basesrc_r_pow = src_pow_r[:, 1:1001]
    basesrc_r_pow = np.mean(basesrc_r_pow, axis = 1)
    print basesrc_r_pow.shape
    src_pow_r = src_pow_r/basesrc_r_pow
    print src_pow_r.shape
    
    new = np.append(new, src_pow_r, 0)
    print new.shape    


np.savetxt(stcMAT_fname, new, delimiter = ',')

###############################################################################################################################
###############################################################################################################################
