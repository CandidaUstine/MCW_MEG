# -*- coding: utf-8 -*-
"""
Created on Tue Aug 19 13:46:04 2014

@author: custine
Usage: getTriggers.py subjID sessID runID
Example: getTriggers.py 9367 5 1
"""

import os 
import os.path
import argparse

####### Get Input ########
parser = argparse.ArgumentParser(description='Get input')
parser.add_argument('subj',type=str)
parser.add_argument('sess',type=str) ##Left, Right etc.,
parser.add_argument('run',type=str) 
args=parser.parse_args()
subjID = args.subj
sessID = args.sess
runID = args.run
print 
print "Subject ID:" + subjID
print "Sess ID:" + sessID 
print "Run Number:" + runID


data_path = '/mnt/file1/binder/KRNS/kr3/' + subjID + '/' + sessID + '/eprime/'
sent_file = data_path + 'data_sentences0' + runID + '.txt'
eprime_file = sent_file = data_path + 'eprime_run0' + runID + '.txt'
eve_file = '/home/custine/MEG/data/krns_kr3/' +subjID+'/s'+sessID+ '/eve/' + subjID + '_s'+ sessID +'_run'+runID + '.eve'
Modeve_file = '/home/custine/MEG/data/krns_kr3/' +subjID+'/s'+sessID+ '/eve/' + subjID + '_s'+ sessID +'_run'+runID + '_Mod.eve'
trigger_file = '/home/custine/MEG/data/krns_kr3/' +subjID+'/s'+sessID+ '/eve/' + subjID + '_s'+ sessID +'_run'+runID + '_Sentence-Triggers.eve'

print "Using Modified Eve file: " + Modeve_file
print 

tempA = 1
dataTable1 = []
dataTable2 = []
tempB = 1
lineTemp = []
lineTemp_next = []
sent_tags = []
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
    myFile1 = open(eprime_file, "r")
    myFile2 = open(Modeve_file, "r")
    myFile3 = open(trigger_file, "w")
    
    while tempA: 
        tempA = myFile1.readline()
        temp1 = tempA.strip()
        if temp1:
            temp2 = temp1.split('\t')
            dataTable1.append(temp2)
    myFile1.close()
    for i in range(1, len(dataTable1)): #Neglecting the first row - titles 
        lineTemp = (dataTable1[i])
        #print lineTemp #total 58 items 55 + 3 probe items for each sentence)
        sent_tags.append(lineTemp[4]) ##Sentence ID

    ##Eve File : 
    #### Sent Onset Time point (in samples)
    while tempB:
        tempB = myFile2.readline()
        temp1 = tempB.strip('\t')
        if temp1:
            temp2 = temp1.split()
            dataTable2.append(temp2)
    dataTable2.append(['0', '0', '0', '0']) ## to account for the lineTemp_next line :/ 
    
    ii = 0
    j = 0
    for i in range(0, len(dataTable2)-1):
        lineTemp = (dataTable2[i])
        lineTemp_next = dataTable2[i+1]
        lineTemp_prev = dataTable2[i-1]
        
        if ((float(lineTemp[3]) == 110) or (float(lineTemp[3]) == 0)):
            if ((float(lineTemp_next[3]) in range(1, 34)) or (float(lineTemp_next[3]) == 101)):
                jane1 = lineTemp_next[3]
                sent = sent_tags[ii]
                ii = ii + 1
            
        if ((float(lineTemp_prev[3]) == 110) or (float(lineTemp_prev[3]) == 0)):
            if (float(lineTemp[3]) in range(1, 34)):
                myFile3.write(lineTemp[0])
                myFile3.write("\t")
                myFile3.write(lineTemp[1])
                myFile3.write("\t")
                myFile3.write(lineTemp[2])
                myFile3.write("\t")
                myFile3.write(str(sent))
                myFile3.write("\n")
              
        #### Sent Offset time point (in samples)
        if float(lineTemp[3]) in range(66,100):
            if float(lineTemp_next[3]) == 100:
                myFile3.write(lineTemp_next[0])
                myFile3.write("\t")
                myFile3.write(lineTemp_next[1])
                myFile3.write("\t")
                myFile3.write(lineTemp_next[2])
                myFile3.write("\t")
                myFile3.write(str(int(1000+ float(sent))))
                myFile3.write("\n")
#
        #### Probe Onset Time point (in samples) and Tag 
        if ((float(lineTemp_prev[3]) == 110) or (float(lineTemp_prev[3]) == 0)):
            if float(lineTemp[3]) == 101:
                myFile3.write(lineTemp[0])
                myFile3.write("\t")
                myFile3.write(lineTemp[1])
                myFile3.write("\t")
                myFile3.write(lineTemp[2])
                myFile3.write("\t")
                myFile3.write(str(int(2000+ float(sent))))
                myFile3.write("\n")

    #### Probe Offset time point (in samples) and Tag
        if float(lineTemp[3]) in range(101,109):
            if float(lineTemp_next[3]) == 100:
                myFile3.write(lineTemp[0])
                myFile3.write("\t")
                myFile3.write(lineTemp[1])
                myFile3.write("\t")
                myFile3.write(lineTemp[2])
                myFile3.write("\t")
                myFile3.write(str(int(3000 +float(sent))))
                myFile3.write("\n")

    #### Probe in the Sentence Tag                 
        if float(lineTemp[3]) == 111:
            myFile3.write(lineTemp[0])
            myFile3.write("\t")
            myFile3.write(lineTemp[1])
            myFile3.write("\t")
            myFile3.write(lineTemp[2])
            myFile3.write("\t")
            myFile3.write(str(int(4000 +float(sent))))
            myFile3.write("\n")

    #### Reset Tag                 
        if float(lineTemp[3]) == 110:
            myFile3.write(lineTemp[0])
            myFile3.write("\t")
            myFile3.write(lineTemp[1])
            myFile3.write("\t")
            myFile3.write(lineTemp[2])
            myFile3.write("\t")
            myFile3.write(str(int(5000 +float(lineTemp[3]))))
            myFile3.write("\n")
            j = j + 1


myFile3.close()
myFile2.close()
print "Number of Sentences found:"
print j 

print "Done! See resulting file in " + trigger_file