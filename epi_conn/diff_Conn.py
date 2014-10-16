# -*- coding: utf-8 -*-
"""
Created on Mon Oct 13 13:21:59 2014

@author: custine
python diff_Conn.py alpha Left Right

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
##############################################################################################
##############################################################################################
#if group == 'Left':
lsubj1 = 'EP1'
lsubj2 = 'EP3'
lsubj3 = 'EP5'
lsubj4 = 'EP7'
#elif group == 'Right':
rsubj1 = 'EP4'
rsubj2 = 'EP6'
rsubj3 = 'EP8'
rsubj4 = 'EP10'

lcon1_fname = '/home/custine/MEG/data/epi_conn/'+ lsubj1 + '/coh/' + lsubj1 +'_' + freq+ '_subj_connectivityMatrix.txt'
lcon2_fname = '/home/custine/MEG/data/epi_conn/'+ lsubj2 + '/coh/' + lsubj2 +'_' + freq+ '_subj_connectivityMatrix.txt'
lcon3_fname = '/home/custine/MEG/data/epi_conn/'+ lsubj3 + '/coh/' + lsubj3 +'_' + freq+ '_subj_connectivityMatrix.txt'
lcon4_fname = '/home/custine/MEG/data/epi_conn/'+ lsubj4 + '/coh/' + lsubj4 +'_' + freq+ '_subj_connectivityMatrix.txt'
lcon_res1 = np.loadtxt(lcon1_fname, delimiter = ',')
lcon_res2 = np.loadtxt(lcon2_fname, delimiter = ',')
lcon_res3 = np.loadtxt(lcon3_fname, delimiter = ',')
lcon_res4 = np.loadtxt(lcon4_fname, delimiter = ',')

rcon1_fname = '/home/custine/MEG/data/epi_conn/'+ rsubj1 + '/coh/' + rsubj1 +'_' + freq+ '_subj_connectivityMatrix.txt'
rcon2_fname = '/home/custine/MEG/data/epi_conn/'+ rsubj2 + '/coh/' + rsubj2 +'_' + freq+ '_subj_connectivityMatrix.txt'
rcon3_fname = '/home/custine/MEG/data/epi_conn/'+ rsubj3 + '/coh/' + rsubj3 +'_' + freq+ '_subj_connectivityMatrix.txt'
rcon4_fname = '/home/custine/MEG/data/epi_conn/'+ rsubj4 + '/coh/' + rsubj4 +'_' + freq+ '_subj_connectivityMatrix.txt'
rcon_res1 = np.loadtxt(rcon1_fname, delimiter = ',')
rcon_res2 = np.loadtxt(rcon2_fname, delimiter = ',')
rcon_res3 = np.loadtxt(rcon3_fname, delimiter = ',')
rcon_res4 = np.loadtxt(rcon4_fname, delimiter = ',')
######################### 2 sample T test ##########################################################
#conAll_T_matrix_fname = data_path + 'TStat_GrandAvgConnectivityMatrix_' + freq + '_' + gp1 + '-' + gp2 + '.txt'
#conAll_T_plot_fname = data_path + 'TStat_GrandAvgConnectivityPlot_' + freq + '_' + gp1 + '-' + gp2 + '.png'
#
#con_t = np.empty((68,68))
#con_t.fill(0)
#for i in range (0, 68):
#    for j in range(0,68):
#        l_mean = (lcon_res1[i,j] + lcon_res2[i,j] + lcon_res3[i,j] + lcon_res4[i,j] )/4
#        r_mean = (rcon_res1[i,j] + rcon_res2[i,j] + rcon_res3[i,j] + rcon_res4[i,j] )/4
#        l_a = [lcon_res1[i,j], lcon_res2[i,j], lcon_res3[i,j], lcon_res4[i,j]]
#        l_std = float(np.std(l_a))
#        #print l_std
#        r_a = [rcon_res1[i,j], rcon_res2[i,j], rcon_res3[i,j], rcon_res4[i,j]]
#        r_std = float(np.std(r_a))
#        #print r_std
#        l_var = pow(l_std, 2)
#        r_var = pow(r_std, 2)
#        #print l_var, r_var
#        if l_mean == 0 and r_mean == 0:
#            t = float(0)
#        else:
#            s_lr = np.sqrt((l_var + r_var)/2)
#            s_lr = float(s_lr * np.sqrt(0.5))
#            t = (l_mean - r_mean)
#         #   print s_lr
#            t = t/s_lr
#        #print t 
#        con_t[i,j] = t 
#    print 
#print con_t 
#print con_t.T
#np.savetxt(conAll_T_matrix_fname, con_t)
####################################################################################################
######################### 2 sample T test - Hotelling T squared statistic  ##########################################################
tsq_matrix_fname = '/home/custine/MEG/results/source_level/ConnectivityPlots/Hotel-Tsq_GrandAvgConnectivityMatrix_' + freq + '_' + gp1 + '-' + gp2 + '.txt'
tsq_plot_fname = '/home/custine/MEG/results/source_level/ConnectivityPlots/Hotel-Tsq_GrandAvgConnectivityPlot_' + freq + '_' + gp1 + '-' + gp2 + '.png'

tsq = np.loadtxt(tsq_matrix_fname, delimiter = ' ')
print tsq
     
##############################################################################################
##############################################################################################
###############Plotting the Conn - Diff or T test stats##################
labels, label_colors = mne.labels_from_parc('fsaverage', parc='aparc', subjects_dir=subjects_dir) ##or use read_labels_from_annot() 
#print labels
print

#### Now, we visualize the connectivity using a circular graph layout
# First, we reorder the labels based on their location in the left hemi
label_names = [label.name for label in labels]
#print label_names[:-1] #### TO GET RID OF UNKNOWN LABEL.LH 
label_names = label_names[:-1]
for name in label_names:
    print name
np.savetxt('/home/custine/MEG/results/source_level/ConnectivityPlots/label_names.txt', label_names)  
lh_labels = [name for name in label_names if name.endswith('lh')]
#print len(lh_labels)

# Get the y-location of the label
label_ypos = list()
for name in lh_labels:
    idx = label_names.index(name)
    ypos = np.mean(labels[idx].pos[:, 1])
    label_ypos.append(ypos)
#print len(label_ypos)

# Reorder the labels based on their location
lh_labels = [label for (ypos, label) in sorted(zip(label_ypos, lh_labels))]

# For the right hemi
rh_labels = [label[:-2] + 'rh' for label in lh_labels]
#print rh_labels

# Save the plot order and create a circular layout
node_order = list()
node_order.extend(lh_labels[::-1])  #reverse the order
node_order.extend(rh_labels)

print 
print 'Jane Here' 
print 

print node_order
print len(node_order)

node_angles = circular_layout(label_names, node_order, start_pos=90,
                              group_boundaries=[0, len(label_names) / 2])
                              
###############################################################################################
##########Plot the difference 
###############3
## Plot the graph using node colors from the FreeSurfer parcellation. We only
## show the 300 strongest connections.
#plot_connectivity_circle(diff_con, label_names, n_lines=300,
#                         node_angles=node_angles, node_colors=label_colors,vmin = 0.0, vmax = 1.0,
#                         title='Coherence - Difference ('+ gp1 + '-' +gp2 +') - '+ freq)
#import matplotlib.pyplot as plt
#plt.savefig(conAll_diff_plot_fname, facecolor='black')

###########################################################################################
##########Plot the connectivity T stats - 2 sample
## Plot the graph using node colors from the FreeSurfer parcellation. We only
## show the 300 strongest connections.
#plot_connectivity_circle(con_t, label_names, n_lines=300,
#                         node_angles=node_angles, node_colors=label_colors,
#                         title='Coherence - T stats ('+ gp1 + '-' +gp2 +') - '+ freq)
#import matplotlib.pyplot as plt
#plt.savefig(conAll_T_plot_fname, facecolor='black')
##plt.show()
#
##################################################################################################3                              



