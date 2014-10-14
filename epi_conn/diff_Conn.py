# -*- coding: utf-8 -*-
"""
Created on Mon Oct 13 13:21:59 2014

@author: custine
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
parser.add_argument('gp1',type=str) 
parser.add_argument('gp2',type=str)  
args=parser.parse_args()
freq = args.freq
print freq
gp1 = args.gp1
print gp1
gp2 = args.gp2
print gp2

# Set parameters
data_path = '/home/custine/MEG/results/source_level/ConnectivityPlots/' # + subj + '/'
subjects_dir = '/home/custine/MRI/structurals/subjects/'

Gp1_conAll_matrix_fname = data_path + 'GrandAvgConnectivityMatrix_' + freq + '_' + gp1 + '.txt'
Gp2_conAll_matrix_fname = data_path + 'GrandAvgConnectivityMatrix_' + freq + '_' + gp2 + '.txt'
conAll_diff_matrix_fname = data_path + 'Difference_GrandAvgConnectivityMatrix_' + freq + '_' + gp1 + '-' + gp2 + '.txt'
conAll_diff_plot_fname = data_path + 'Difference_GrandAvgConnectivityPlot_' + freq + '_' + gp1 + '-' + gp2 + '.png'

##Difference between groups 
con_gp1 = np.loadtxt(Gp1_conAll_matrix_fname, delimiter = ' ')
con_gp2 = np.loadtxt(Gp2_conAll_matrix_fname, delimiter = ' ')
diff_con = con_gp1 - con_gp2 
#print diff_con
np.savetxt(conAll_diff_matrix_fname, diff_con)
###############################################################################################
###############################################################################################
########################## T test ##########################################################
##if group == 'Left':
#subj1 = 'EP1'
#subj2 = 'EP3'
##    subj3 = 'EP5'
##    subj4 = 'EP7'
##elif group == 'Right':
#subj3 = 'EP4'
#subj4 = 'EP6'
##    subj3 = 'EP8'
##    subj4 = 'EP10'
#
#con1_fname = '/home/custine/MEG/data/epi_conn/'+ subj1 + '/coh/' + subj1 +'_' + freq+ '_subj_connectivityMatrix.txt'
#con2_fname = '/home/custine/MEG/data/epi_conn/'+ subj2 + '/coh/' + subj2 +'_' + freq+ '_subj_connectivityMatrix.txt'
#con3_fname = '/home/custine/MEG/data/epi_conn/'+ subj3 + '/coh/' + subj3 +'_' + freq+ '_subj_connectivityMatrix.txt'
#con4_fname = '/home/custine/MEG/data/epi_conn/'+ subj4 + '/coh/' + subj4 +'_' + freq+ '_subj_connectivityMatrix.txt'
#con_res1 = np.loadtxt(con1_fname, delimiter = ',')
#con_res2 = np.loadtxt(con2_fname, delimiter = ',')
#con_res3 = np.loadtxt(con3_fname, delimiter = ',')
#con_res4 = np.loadtxt(con4_fname, delimiter = ',')
#
#con_t = np.empty((68,68))
#con_t.fill(0)
#for i in range (0, 68):
#    print 'new'
#    print 'i', i
#    for j in range(0,68):
#        print 'j', j
#        print con_res1[i,j]
#        print con_res2[i,j]
#        print con_res3[i,j]
#        print con_res4[i,j]
#        l_mean = (con_res1[i,j] + con_res2[i,j])/2
#        r_mean = (con_res3[i,j] + con_res4[i,j])/2
#        l_a = [con_res1[i,j], con_res2[i,j]]
#        l_std = float(np.std(l_a))
#        #print l_std
#        r_a = [con_res3[i,j], con_res4[i,j]]
#        r_std = float(np.std(r_a))
#        #print r_std
#        if l_mean == 0 and r_mean == 0:
#            t = float(0)
#        else:
#            s_lr = np.sqrt((pow(l_std, 2) + pow(r_std,2))/2) 
#            s_lr = s_lr * np.sqrt(2/2)
#            t = (l_mean - r_mean)
#            t = t/s_lr
#        print t 
#        con_t[i,j] = t 
#    print 
##print con_res1[5,5]
##print con_res2[5,5]
#
#print con_t 

##############################################################################################
##############################################################################################
###############Plotting the Conn##################
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
plot_connectivity_circle(diff_con, label_names, n_lines=300,
                         node_angles=node_angles, node_colors=label_colors,vmin = 0.10, vmax = 1.00,
                         title='Coherence Difference ('+ gp1 + '-' +gp2 +') - '+ freq)
import matplotlib.pyplot as plt
plt.savefig(conAll_diff_plot_fname, facecolor='black')
#plt.show()
## Plot connectivity for both methods in the same plot
#fig = plt.figure(num=None, figsize=(8, 4), facecolor='black')
#no_names = [''] * len(label_names)
#for ii, method in enumerate(con_methods):
#    plot_connectivity_circle(con_res[method], no_names, n_lines=300,
#                             node_angles=node_angles, node_colors=label_colors,
#                             title=method, padding=0, fontsize_colorbar=6,
#                             fig=fig, subplot=(1, 2, ii + 1))
#plt.savefig('/home/custine/MEG/data/epi_conn/' + subj + '/coh/' + subj + '_circle_coh_imcoh_' + freq + '.png', facecolor='black')
plt.show()
    
