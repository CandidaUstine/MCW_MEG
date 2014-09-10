# -*- coding: utf-8 -*-
"""
Created on Fri Aug 22 09:53:50 2014

@author: custine
Usage: prep_WordList.py subjID sessID runID
Example: prep_WordList.py 9367 5 1
"""

import os 
import os.path
import argparse

####### Get Input ########
parser = argparse.ArgumentParser(description='Get input')
parser.add_argument('subj',type=str)
parser.add_argument('sess',type=str) ##5
#parser.add_argument('run',type=str) 
args=parser.parse_args()
subjID = args.subj
sessID = args.sess
#runID = args.run

runs = ['1', '2', '3', '4', '5','6', '7', '8', '9', '10', '11', '12']  # TESTING################################################
print runs

for runID in runs: 

    runID = runID.zfill(2)
    
    print 
    print "Subject ID:" + subjID
    print "Sess ID:" + sessID 
    print "Run Number:" + runID
    #print 
    
    data_path = '/mnt/file1/binder/KRNS/' #kr3/' + subjID + '/' + sessID + '/eprime/'
    sentList_file = data_path + 'info/krns_sentence_list.txt'
    wordList_file = data_path + 'info/krns_word_list.txt'
    eprime_file =  data_path + 'kr3/' + subjID + '/' + sessID + '/eprime/eprime_run' + runID + '.txt'
    eve_file = '/home/custine/MEG/data/krns_kr3/' +subjID+'/s'+sessID+ '/eve/' + subjID + '_s'+ sessID +'_run'+runID + '.eve'
    Modeve_file = '/home/custine/MEG/data/krns_kr3/' +subjID+'/s'+sessID+ '/eve/' + subjID + '_s'+ sessID +'_run'+runID + '_Mod.eve'
    #dataWord_file =  data_path + 'kr3/' + subjID + '/' + 'word_sentences0' + runID + '.txt'
    dataWord_file = '/home/custine/MEG/data/krns_kr3/' +subjID+'/s'+sessID+ '/eve/' + 'word_sentences' + runID + '.txt'
    #print wordList_file
    
    tempA = 1
    tempB = 1
    tempC = 1
    dataTable1 = []
    dataTable2 = []
    dataTable3 = []
    lineTemp = []
    lineTemp_next = []
    
    sentID = []
    probeID = []
    sent_tags = []
    sent_line = []
    word_line = []
    wordID_tags = []
    word_tags = []
    sentNum_tags = []
    sentWord_tags = []
    sentWordLine_tags = []
    
    if os.path.exists(eprime_file):
    
        myFile1 = open(eprime_file, "r")
        myFile2 = open(wordList_file, "r")
        myFile3 = open(sentList_file, "r")
        myFile4 = open(dataWord_file, "w")
        
    ############################ 
    #E Prime spreadsheet
        while tempA: 
            tempA = myFile1.readline()
            temp1 = tempA.strip()
            if temp1:
                temp2 = temp1.split('\t')
                dataTable1.append(temp2)
        myFile1.close()
        for i in range(1, len(dataTable1)): #Neglecting the first row - titles 
            lineTemp = (dataTable1[i]) #total 58 items (including the 3 probe items for each sentence)
            sentID.append(lineTemp[4])
            probeID.append(lineTemp[8])
        print len(sentID)
        print len(probeID)
    
    ############################################### 
    #Word List 
        while tempB:
            tempB = myFile2.readline()
            temp1 = tempB.strip('\t')
            if temp1:
                temp2 = temp1.split()
                dataTable2.append(temp2)
        dataTable2.append(['0', '0', '0', '0']) ## to account for the lineTemp_next line :/ 
        for i in range(0, len(dataTable2)-1):
            lineTemp = (dataTable2[i])
            wordID_tags.append(lineTemp[0])
            word_tags.append(lineTemp[1])   
    #    print (wordID_tags) ##NOTE: word 'Used' is coded as the same 93 tag for both the verb and adverb!!! :) 
    ############################################# 
    #Sentence List
        while tempC:
            tempC = myFile3.readline()
            temp1 = tempC.strip('\t')
            if temp1:
                temp2 = temp1.split()
                dataTable3.append(temp2)
        dataTable3.append(['0', '0', '0', '0'])
        
        for i in range(0, len(dataTable3)-1):
            lineTemp = (dataTable3[i])
            #print lineTemp
            sentWord_tags = []
            sentNum_tags.append(lineTemp[0])
            leng = len(lineTemp)
    #        print lineTemp[leng-1]
            for jj in range(0, leng-1):
                sentWord_tags.append(lineTemp[jj])
            sentWord_tags.append(lineTemp[leng-1].split('.')[0]) ##To remove the full stop at the end of the sentence. 
            sentWordLine_tags.append(sentWord_tags)
    
        myFile4.write('0')
        myFile4.write("\t")
        myFile4.write('0')
        myFile4.write("\n")
        for ii in range(0, len(sentID)): #len(sentID)):
             x = int(sentID[ii])
             new = []
             #l = 0 ##Test for the Number of word items in a sentence  
             new = sentWordLine_tags[x-1] 
             #print new
             for jj in range(1, 10): #not including the sent ID - starting with [1]
                 if jj < len(new):
                     if new[jj] in word_tags:
                            lineNum = int(word_tags.index(new[jj]))  
                            wordID = wordID_tags[lineNum]
                            #print new[jj]
                            #print wordID
                            sentwordID = str(sentID[ii]).zfill(3) + str(wordID).zfill(3)
                            myFile4.write(str(sentwordID))
                            myFile4.write("\t")
                            myFile4.write(new[jj])
                            myFile4.write("\n")
        #                 print int(word_tags.index(new[jj]))
                     elif (new[jj] == 'the') or (new[jj] == 'The') or (new[jj] == 'was') or (new[jj] == 'a'): ##For the words that have no tags ##the and ##was                        
                            sentwordID = str(sentID[ii]).zfill(3) + str('999').zfill(3)
                            myFile4.write(str(sentwordID))
                            myFile4.write("\t")
                            myFile4.write(new[jj])
                            myFile4.write("\n")
                 else:
                     myFile4.write('100') ##Fixation - fillers
                     myFile4.write("\t")
                     myFile4.write('+')
                     myFile4.write("\n")
             if probeID[ii] == '1': ##Probe words (3 in a run)
                myFile4.write('111')
                myFile4.write("\t")
                myFile4.write('PROBE')
                myFile4.write("\n") 
             myFile4.write('110') ##Reset tags - after each sentence - (33 total)
             myFile4.write("\t")             
             myFile4.write('RESET')
             myFile4.write("\n")
    
    print "Done! See resulting file in " + dataWord_file 