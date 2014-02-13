# -*- coding: utf-8 -*-
"""
Created on Thu Feb 13 16:59:34 2014

@author: custine
"""

import mne
from mne import fiff
import numpy
import argparse
import copy
import condCodes as cc


#######Get Input ##

parser = argparse.ArgumentParser(description='Get input')
parser.add_argument('subj',type=str)
parser.add_argument('exp',type=str) ##Left, Right etc., 
args=parser.parse_args()
subjID = args.subj
exp = args.exp
print subjID
print exp

########Analysis Parameters##
###Event file suffix 
evSuffix = '_mod.eve'

###Projection and Average Reference 
projVal = True
avgRefVal = False

###Filtering
hp_cutoff = 0.5
lp_cutoff = 20

#######Experiment specific parameters 
###EventLabels
labelList = cc.condLabels[exp]
event_id = {}
for row in labelList:
    event_id[row[1]] = int(row[0])
print event_id

###TimeWindow
tmin = -.1
tmax = float(cc.epMax[exp])


########Artifact rejection parameters
###General
gradRej = 2000e-13
magRej = 3000e-15
eegRej = 100e-6
magFlat = 1e-14
gradFlat = 1000e-15

#####################################
########Compute averages for each run

evoked=[]
#print ev 
data_path = '/home/custine/MEG/data/msabri/' +subjID
event_file = data_path + '/eve/' + subjID + '_'+ exp + evSuffix
print event_file






















