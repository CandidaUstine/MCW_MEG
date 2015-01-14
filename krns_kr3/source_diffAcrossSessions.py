# -*- coding: utf-8 -*-
"""
Created on Tue Dec 16 12:35:58 2014

@author: custine

ex: python source_diffAcrossSessions.py 5049 Noun_People Noun_Place .3 .5 spm 5
"""

import copy
import numpy as np
import scipy
import argparse

#import readInput

import mne
from mne.stats import permutation_cluster_1samp_test
from mne import spatial_tris_connectivity, grade_to_tris, spatio_temporal_tris_connectivity
##from scikits.learn.externals.joblib import Memory
from sklearn.externals.joblib import Memory

###############################################################################
## Parameters

parser = argparse.ArgumentParser(description='Get input')
#parser.add_argument('prefix',type=str)
parser.add_argument('subjID',type=str)
parser.add_argument('cond1Name',type=str)
parser.add_argument('cond2Name',type=str)
parser.add_argument('t1',type=float)
parser.add_argument('t2',type=float)
parser.add_argument('model',type=str)
parser.add_argument('threshold',type=float)
args=parser.parse_args()

args = parser.parse_args()
subjID = args.subjID ## 9511
c1 = args.cond1Name  ##Noun_People
c2 = args.cond2Name ##Noun_Place
model = args.model
time_interval = (args.t1,args.t2)  #If you set a real time_interval, you will average across this and do spatial clusters
dec = None
#time_interval = None  #If you set time_interval to None, it will do spatiotemporal clusters
#dec = 10  # this sets the temporal decimation factor. e.g. if you sampled 600Hz and set this to 3, you will downsample the test to every 5 ms
thresholds = [args.threshold]  #This sets the threshold for the first stage of the test. You have the option of including more than one threshold to see what happens when it changes
print thresholds

####Setup Subject Speciifc Information
data_path = '/home/custine/MEG/results/source_level/ga_stc/krns_kr3/'
result_path = '/home/custine/MEG/results/source_level/diff_stc/krns_kr3/' 

stcs1_fname = data_path + 'gaSess_' + subjID + '_' + c1 + '_All_c1M-' +model + '-lh.stc' 
stcs2_fname = data_path + 'gaSess_' + subjID + '_' + c2 + '_All_c1M-' +model + '-lh.stc'  
result_fname = result_path + subjID + '_' + c1 + '-' + c2 + '_' + model + '_diff_of_means'

#def stat_fun(X):
#    return np.mean(X, axis=0)  #This determines what function to use for the first stage of the test (e.g. mean, t-value)
#stat_name = 'mean'

def stat_fun(X):
	return scipy.stats.ttest_1samp(X,0)[0]
stat_name = 'ttest'


n_permutations = 1000
#n_permutations = 1000 #This sets the number of permutations to run

###############################################################################
# Process

mem = Memory(cachedir=None)

import multiprocessing
n_jobs = multiprocessing.cpu_count()
if n_jobs > 20:
    n_jobs = min(n_jobs, 10)
else:
    n_jobs = min(n_jobs, 5)

##inputs
#print args.prefix
#print args.protocol
#prefix = "%s_%s_c%d_c%d_%s" % (args.prefix, args.protocol, args.cond1, args.cond2,args.model)
#print prefix
#



#load the vertex configuration
ico_tris = mne.source_estimate._get_ico_tris(grade=5)
src = [dict(), dict()]
src[0]['use_tris'] = ico_tris
src[1]['use_tris'] = ico_tris

def load_data(stcs1_fname, stcs2_fname, dec):
    stcs1 = [mne.read_source_estimate(stcs1_fname)] # for fname in stcs1_fname]
    stcs2 = [mne.read_source_estimate(stcs2_fname)] # for fname in stcs2_fname]
    print stcs1
    print 
    print stcs2
    print 
	#This is just resampling in time, not space
    def resample_stc(stc, dec):
        """Resample stc inplace"""
        stc.data = stc.data[:,::dec].astype(np.float)
        stc.tstep *= dec
        stc.times = stc.times[::dec]
	
    if dec is not None:
        for stc in stcs1 + stcs2:
            resample_stc(stc, dec=dec)
           #stc.crop(.3,.5)
            stc.crop(0.1, None)  #cropping the time-window for faster runtime
    #print "Jane here"


    def average_stcs(stcs):
        mean_stc = copy.deepcopy(stcs[0])
        times = mean_stc.times
        n_sources, n_times = mean_stc.data.shape
        X = np.empty((len(stcs), n_sources, n_times))
        for i, stc in enumerate(stcs):
            if len(times) == len(stc.times):
                X[i] = stc.data
        mean_stc._data = np.mean(X, axis=0)
       #print "Jane here"
        print np.shape(mean_stc)
        return mean_stc, X 
        print 
        
	#X1, X2 are the full time,vertices,subject matrices; mean_stc1 and mean_stc2 are the grand-avgs
    mean_stc1, X1 = average_stcs(stcs1)
    mean_stc2, X2 = average_stcs(stcs2)
    print mean_stc1, X1, mean_stc2, X2
    return mean_stc1, X1, mean_stc2, X2
    

mean_stc1, X1, mean_stc2, X2 = mem.cache(load_data)(stcs1_fname, stcs2_fname, dec)

template_stc = copy.deepcopy(mean_stc1)
stc_diff = copy.deepcopy(template_stc)
stc_diff._data = mean_stc1.data - mean_stc2.data  ##Stc cond 1- Stc cond 2 
stc_diff.save(result_fname)
print 'Resulting file: ' + result_fname + '.stc'

#if time_interval is not None:  # squash time interval
#    tmin, tmax = time_interval
#    times = mean_stc1.times
#    mask = (times >= tmin) & (times <= tmax)
#    X1 = np.mean(X1[:, :, mask], axis=2)[:, :, None]
#    X2 = np.mean(X2[:, :, mask], axis=2)[:, :, None]
#    template_stc = copy.deepcopy(template_stc)
#    template_stc.crop(tmin, tmin + template_stc.tstep)
#
#assert X1.shape == X2.shape
#n_samples, n_vertices, n_times = X1.shape
#print n_times
#print n_vertices
#X1 = np.ascontiguousarray(np.swapaxes(X1, 1, 2).reshape(n_samples, -1))
#X2 = np.ascontiguousarray(np.swapaxes(X2, 1, 2).reshape(n_samples, -1))
#
##connectivity = mne.spatio_temporal_src_connectivity(src, n_times)
#connectivity = mne.spatial_tris_connectivity(grade_to_tris(5))
##connectivity = mne.spatio_temporal_tris_connectivity(grade_to_tris(5), n_times)
#
#
#for t in thresholds:
#    from time import time
#    t0 = time()
#    T_obs, clusters, cluster_pv, H0 = mem.cache(permutation_cluster_1samp_test,
#                                                ignore=['n_jobs'])(X1 - X2,
#                                                threshold=t,
#                                                n_permutations=n_permutations,
#                                                tail=0,
#                                                stat_fun=stat_fun,
#                                                connectivity=connectivity,
#                                                n_jobs=n_jobs, seed=0)
#    print "Time elapsed : %s (s)" % (time() - t0)
#
#    clusters = [c.reshape(n_times, n_vertices).T for c in clusters]
#	#you get a cluster for every single thing that crossed the first-stage threshold
#
#    # stc_log_pv_cluster = copy.deepcopy(mean_stc1)
#    # stc_log_pv_cluster.data = np.zeros_like(stc_log_pv_cluster.data)
#    # for pv, c in zip(cluster_pv, clusters):
#    #     stc_log_pv_cluster.data[c] = -np.log10(pv)
#    # 
#    # stc_log_pv_cluster.save(prefix + 'clusters_pv_%s_%s' % (stat_name, t))
#    
#    stc_cluster = copy.deepcopy(template_stc)
#    #you only write out a cluster to an stc file if it crosses the second-stage threshold
#    for k, c in enumerate(clusters):
#        stc_cluster._data = c
#        if cluster_pv[k] < 0.3:  ##This is the threshold for saving an stc file with cluster
#            stcFileName = '/home/custine/MEG/data/krns_kr3/9367/s5/ave_projon/stc/9367_s5_Noun_People-Place_diff_of_means_clusters' #'/cluster/kuperberg/SemPrMM/MEG/results/source_space/cluster_stats/' + prefix + '%d-%d_cluster%d_%s_thresh_%s_pv_%.3f' % (args.t1*1000,args.t2*1000,k, stat_name, t, cluster_pv[k])
#            print stcFileName
#            stc_cluster.save(stcFileName)
#            #stc_cluster.save('/cluster/kuperberg/SemPrMM/MEG/results/source_space/cluster_stats/' + prefix + '%d-%d_cluster%d_%s_thresh_%s_pv_%.3f' % (args.t1*1000,args.t2*1000,k, stat_name, t, cluster_pv[k]))
#            labelArray = mne.stc_to_label(stc_cluster, 'fsaverage')
#            label = labelArray[0]
#            mne.write_label(stcFileName, label)            
#
#    print 'pv : %s' % np.sort(cluster_pv)[:15]



################################################################################################################33333333
#for t in thresholds:
#    from time import time
#    t0 = time()
#    T_obs, clusters, cluster_pv, H0 = mem.cache(permutation_cluster_1samp_test,
#                                                ignore=['n_jobs'])(X1 - X2,
#                                                threshold=t,
#                                                n_permutations=n_permutations,
#                                                tail=0,
#                                                stat_fun=stat_fun,
#                                                connectivity=connectivity,
#                                                n_jobs=n_jobs, seed=0)
#    print "Time elapsed : %s (s)" % (time() - t0)
#    clusters = [c.reshape(n_times, n_vertices).T for c in clusters]
#	#you get a cluster for every single thing that crossed the first-stage threshold
#
#    # stc_log_pv_cluster = copy.deepcopy(mean_stc1)
#    # stc_log_pv_cluster.data = np.zeros_like(stc_log_pv_cluster.data)
#    # for pv, c in zip(cluster_pv, clusters):
#    #     stc_log_pv_cluster.data[c] = -np.log10(pv)
#    # 
#    # stc_log_pv_cluster.save(prefix + 'clusters_pv_%s_%s' % (stat_name, t))
#    
#    stc_cluster = copy.deepcopy(template_stc)
#    #you only write out a cluster to an stc file if it crosses the second-stage threshold
#    for k, c in enumerate(clusters):
#        stc_cluster._data = c
#        if cluster_pv[k] < 0.3:  ##This is the threshold for saving an stc file with cluster
#            stcFileName = '/home/custine/MEG/data/krns_kr3/9367/s5/ave_projon/stc/9367_s5_Noun_People-Place_diff_of_means_clusters' # '/cluster/kuperberg/SemPrMM/MEG/results/source_space/cluster_stats/hp-filt_1/' + prefix + '%d-%d_cluster%d_%s_thresh_%s_pv_%.3f' % (args.t1*1000,args.t2*1000,k, stat_name, t, cluster_pv[k])
#            print stcFileName
#            stc_cluster.save(stcFileName)
#            #stc_cluster.save('/cluster/kuperberg/SemPrMM/MEG/results/source_space/cluster_stats/' + prefix + '%d-%d_cluster%d_%s_thresh_%s_pv_%.3f' % (args.t1*1000,args.t2*1000,k, stat_name, t, cluster_pv[k]))
#            labelArray = mne.stc_to_label(stc_cluster, 'fsaverage')
#            label = labelArray[0]
#            mne.write_label(stcFileName, label)            
#
#    print 'pv : %s' % np.sort(cluster_pv)[:5]