# -*- coding: utf-8 -*-
"""
Created on Tue Aug 19 13:46:04 2014

@author: custine
Usage: getTriggers.py subjID sessID runID
Example: getTriggers.py 9367 5 1
"""

import sys
import os 
import os.path
import readInput
import mne
from mne import fiff
import argparse
import csv

####### Get Input ########
parser = argparse.ArgumentParser(description='Get input')
parser.add_argument('subj',type=str)
parser.add_argument('sess',type=str) ##Left, Right etc.,
parser.add_argument('run',type=str) 
args=parser.parse_args()
subjID = args.subj
sessID = args.sess
runID = args.run
print subjID
print sessID
print runID


data_path = '/mnt/file1/binder/KRNS/kr3/' + subjID + '/' + sessID + '/eprime/'
sent_file = data_path + 'data_sentences0' + runID + '.txt'
eve_file = '/home/custine/MEG/data/krns_kr3/' +subjID+'/s'+sessID+ '/eve/' + subjID + '_s'+ sessID +'_run'+runID + '.eve'
print sent_file
trigger_file = '/home/custine/MEG/data/krns_kr3/' +subjID+'/s'+sessID+ '/eve/' + subjID + '_s'+ sessID +'_run'+runID + '_Sentence-Triggers.csv'
#sent_list = readInput.readList(sent_file)
#print sent_list

tempA = 1
dataTable1 = []
dataTable2 = []
tempB = 1
lineTemp = []
lineTemp_next = []
sentID = []
sentOnset = []
sentOffset = []
probeOnset = []
probeOffset = []
sentOnset_tag = []
sentOffset_tag =[]
probe_tag = []
probeOnset_tag = []
probeOffset_tag = []
resetOnset = []
reset_tag = []

if os.path.exists(sent_file):
    ##Sent File:
    #### SentID Onset and Offset Tags
    myFile1 = open(sent_file, "r")
    while tempA: 
        tempA = myFile1.readline()
        temp1 = tempA.strip('\t')
        if temp1:
            temp2 = temp1.split()
            dataTable1.append(temp2)
    myFile1.close()
    for i in range(1, len(dataTable1)):
        lineTemp = (dataTable1[i])
        sentID.append(lineTemp[0]) ##Sentence ID
        sentOnset_tag.append(lineTemp[0]) ##Sentence Onset ID - same as Sent ID
        sentOffset_tag.append(int(1000 + float(lineTemp[0]))) #Sentence Offset Tag 
 
    ##Eve File : 
    #### Sent Onset Time point (in samples)
    myFile2 = open(eve_file, "r")
    while tempB:
        tempB = myFile2.readline()
        temp1 = tempB.strip('\t')
        if temp1:
            temp2 = temp1.split()
            dataTable2.append(temp2)
    dataTable2.append(['0', '0', '0', '0']) ## to account for the lineTemp_next line :/ 
    myFile2.close()
    for i in range(0, len(dataTable2)-1):
        lineTemp = (dataTable2[i])
        lineTemp_next = dataTable2[i+1]
        for ii in range(1, 34):
            if float(lineTemp[3]) == ii:
                sentOnset.append(lineTemp[0])
                
    #### Sent Offset time point (in samples)
        if float(lineTemp[3]) in range(66,100):
            if float(lineTemp_next[3]) == 100:
                #print lineTemp_next[0]
                sentOffset.append(lineTemp_next[0])

    #### Probe Onset Time point (in samples) and Tag               
        if float(lineTemp[3]) == 101:
            probe_tag.append(4000 +float(lineTemp[3]))
            probeOnset.append(lineTemp[0])
            probeOnset_tag.append(int(2000 +float(lineTemp[3])))

    #### Probe Offset time point (in samples) and Tag
        if float(lineTemp[3]) in range(101,109):
            if float(lineTemp_next[3]) == 100:
                probeOffset_tag.append(int(3000 +float(lineTemp[3])))
                #print int(3000 +float(lineTemp[3]))
                probeOffset.append(lineTemp_next[0])

    #### Reset Tag                 
        if float(lineTemp[3]) == 110:
            resetOnset.append(lineTemp[0])
            reset_tag.append(int(float(lineTemp[3]) + 5000))

## Write the Data to a Text File 
with open(trigger_file, "wb") as myFile3:
    a = csv.writer(myFile3, delimiter = ' ')
#    a.writerow(reset_tag)
    a.writerow(['SentID','sentOnset_tag', 'sentOnset', 'sentOffset_tag', 'sentOffset', 'reset_tag', 'resetOnset'])
    rows = zip(sentID, sentOnset_tag, sentOnset, sentOffset_tag, sentOffset, reset_tag, resetOnset)
    for row in rows:
        a.writerow(row)
   
    a.writerow(['probe_tag', 'probeOnset', 'probeOffset'])
    rows_probe = zip(probe_tag, probeOnset, probeOffset)
    for row in rows_probe:
        a.writerow(row)
#    b = csv.writer(myFile3, delimiter = '\n')
#    b.writerow(probeOffset)







