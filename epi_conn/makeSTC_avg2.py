# -*- coding: utf-8 -*-
"""
Created on Thu Oct  9 09:08:51 2014
Read STC files and average them. 

@author: custine
python makeSTC_avg2.py beta Left

"""



print(__doc__)

import numpy as np
import mne
from mne.io import Raw
from mne.minimum_norm import (apply_inverse, apply_inverse_epochs,
                              read_inverse_operator, write_inverse_operator)
from mne.connectivity import seed_target_indices, spectral_connectivity
import argparse 
from mne.viz import circular_layout, plot_connectivity_circle

#####################################3
##Get Inputs 
parser = argparse.ArgumentParser(description='Get input')
parser.add_argument('freq', type = str)
parser.add_argument('group',type=str) 
args=parser.parse_args()
freq = args.freq
print freq
group = args.group
print group 

if group == 'Left':
    subj1 = 'EP1'
    subj2 = 'EP3'
    subj3 = 'EP5'
    subj4 = 'EP7'
elif group == 'Right':
    subj1 = 'EP4'
    subj2 = 'EP6'
    subj3 = 'EP8'
    subj4 = 'EP10'
    


# Set parameters
data_path = '/home/custine/MEG/results/source_level/ConnectivityPlots/' # + subj + '/'
subjects_dir = '/home/custine/MRI/structurals/subjects/'
con1_fname = '/home/custine/MEG/data/epi_conn/'+ subj1 + '/coh/' + subj1 +'_' + freq+ '_subj_plv_ConnectivityMatrix.txt'
con2_fname = '/home/custine/MEG/data/epi_conn/'+ subj2 + '/coh/' + subj2 +'_' + freq+ '_subj_plv_ConnectivityMatrix.txt'
con3_fname = '/home/custine/MEG/data/epi_conn/'+ subj3 + '/coh/' + subj3 +'_' + freq+ '_subj_plv_ConnectivityMatrix.txt'
con4_fname = '/home/custine/MEG/data/epi_conn/'+ subj4 + '/coh/' + subj4 +'_' + freq+ '_subj_plv_ConnectivityMatrix.txt'
conAll_plot_fname = data_path + 'PLV_GrandAvgConnectivityPlot_' + freq + '_' + group  + '.png'
conAll_matrix_fname = data_path + 'PLV_GrandAvgConnectivityMatrix_' + freq + '_' + group + '.txt'

##################################################################################3
################Averaging Conn-coherence matrices #####################################3
con_res1 = np.loadtxt(con1_fname, delimiter = ',')
con_res2 = np.loadtxt(con2_fname, delimiter = ',')
con_res3 = np.loadtxt(con3_fname, delimiter = ',')
con_res4 = np.loadtxt(con4_fname, delimiter = ',')
grand_con = np.mean([con_res1, con_res2, con_res3, con_res4], axis = 0)
print grand_con
np.savetxt(conAll_matrix_fname, grand_con)

##############################################################################################
###############Plotting the average Conn##################
labels, label_colors = mne.labels_from_parc('fsaverage', parc='aparc', subjects_dir=subjects_dir) ##or use read_labels_from_annot() 
print labels
print

#### Now, we visualize the connectivity using a circular graph layout
# First, we reorder the labels based on their location in the left hemi
label_names = [label.name for label in labels]
print label_names[:-1] #### TO GET RID OF UNKNOWN LABEL.LH 
label_names = label_names[:-1]
lh_labels = [name for name in label_names if name.endswith('lh')]
print len(lh_labels)

# Get the y-location of the label
label_ypos = list()
for name in lh_labels:
    idx = label_names.index(name)
    ypos = np.mean(labels[idx].pos[:, 1])
    label_ypos.append(ypos)
print len(label_ypos)

# Reorder the labels based on their location
lh_labels = [label for (ypos, label) in sorted(zip(label_ypos, lh_labels))]

# For the right hemi
rh_labels = [label[:-2] + 'rh' for label in lh_labels]
print rh_labels

# Save the plot order and create a circular layout
node_order = list()
node_order.extend(lh_labels[::-1])  #reverse the order
node_order.extend(rh_labels)

node_angles = circular_layout(label_names, node_order, start_pos=90,
                              group_boundaries=[0, len(label_names) / 2])

# Plot the graph using node colors from the FreeSurfer parcellation. We only
# show the 300 strongest connections.
plot_connectivity_circle(grand_con, label_names, n_lines=300,
                         node_angles=node_angles, node_colors=label_colors,vmin = 0.50, vmax = 1.00,
                         title='All-to-All Connectivity(PLV)- Grand Average - ' + freq)
import matplotlib.pyplot as plt
plt.savefig(conAll_plot_fname, facecolor='black')
plt.show()
## Plot connectivity for both methods in the same plot
#fig = plt.figure(num=None, figsize=(8, 4), facecolor='black')
#no_names = [''] * len(label_names)
#for ii, method in enumerate(con_methods):
#    plot_connectivity_circle(con_res[method], no_names, n_lines=300,
#                             node_angles=node_angles, node_colors=label_colors,
#                             title=method, padding=0, fontsize_colorbar=6,
#                             fig=fig, subplot=(1, 2, ii + 1))
#plt.savefig('/home/custine/MEG/data/epi_conn/' + subj + '/coh/' + subj + '_circle_coh_imcoh_' + freq + '.png', facecolor='black')
##plt.show()
    