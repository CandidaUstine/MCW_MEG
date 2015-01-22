# -*- coding: utf-8 -*-
"""
Created on Tue Aug 19 13:46:04 2014

@author: custine
Usage: getTriggers.py subjID sessID TriggerType(Enter 'Sentence' or 'Word')
Example: getTriggers.py 9367 5 Word/Sentence/Category (if Category - specify 'Noun' verb etc.,) 
EX2: python getTriggers.py 9567 s5 PreStim

"""

import sys
import os 
import os.path

def Sentences(subjID, sessID, runID):


    data_path = '/mnt/file1/binder/KRNS/kr3/' + subjID + '/' + sessID + '/eprime/'
#    sent_file = data_path + 'data_sentences0' + runID + '.txt'
    eprime_file = data_path + 'eprime_run' + runID.zfill(2) + '.txt'
#    eve_file = '/home/custine/MEG/data/krns_kr3/' +subjID+'/s'+sessID+ '/eve/' + subjID + '_s'+ sessID +'_run'+runID + '.eve'
    Modeve_file = '/home/custine/MEG/data/krns_kr3/' +subjID+'/s'+sessID+ '/eve/mod/' + subjID + '_s'+ sessID +'_run'+runID + '_Mod.eve'
    trigger_file = '/home/custine/MEG/data/krns_kr3/' +subjID+'/s'+sessID+ '/eve/triggers/' + subjID + '_s'+ sessID +'_run'+runID + '_Sentence-Triggers.eve'
    
    print "Using Modified Eve file: " + Modeve_file
    print 
    
    tempA = 1
    dataTable1 = []
    dataTable2 = []
    tempB = 1
    lineTemp = []
    lineTemp_next = []
    sent_tags = []
    
    if os.path.exists(Modeve_file):
        print "Jane Jane here here"
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
            lineTemp = (dataTable1[i]) #total 58 items 55 + 3 probe items for each sentence)
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

def Words(subjID, sessID, runID):
    
    data_path = '/mnt/file1/binder/KRNS/kr3/' + subjID + '/' + sessID + '/eprime/'
#    sent_file = data_path + 'data_sentences0' + runID + '.txt'
    dataWord_file = data_path + 'eprime_run0' + runID + '.txt'
#    eve_file = '/home/custine/MEG/data/krns_kr3/' +subjID+'/s'+sessID+ '/eve/' + subjID + '_s'+ sessID +'_run'+runID + '.eve'
    Modeve_file = '/home/custine/MEG/data/krns_kr3/' +subjID+'/'+sessID+ '/eve/mod/' + subjID + '_'+ sessID +'_run'+runID + '_Mod.eve'
    trigger_file = '/home/custine/MEG/data/krns_kr3/' +subjID+'/'+sessID+ '/eve/triggers/' + subjID + '_'+ sessID +'_run'+runID + '_Word-Triggers.eve'
    dataWord_file = '/home/custine/MEG/data/krns_kr3/' +subjID+'/'+sessID+ '/eve/' + 'word_sentences' + runID.zfill(2) + '.txt'
    Modtrigger_file = '/home/custine/MEG/data/krns_kr3/' +subjID+'/'+sessID+ '/eve/triggers/' + subjID + '_'+ sessID +'_run'+runID + '_Word-TriggersMod.eve'
    
    tempA = 1
    dataTable1 = []
    dataTable2 = []
    tempB = 1
    lineTemp = []
    word_tags = []
    wordID_tags = []
    sentword = []
    sentwordID = []
    
    if os.path.exists(Modeve_file):
        print "Using Modified Eve file: " + Modeve_file
        print 
        ##Sent File:
        #### SentID Onset and Offset Tags
        myFile1 = open(dataWord_file, "r")
        myFile2 = open(Modeve_file, "r")
        myFile3 = open(trigger_file, "w")
        myFile4 = open(Modtrigger_file, "w")
        
        while tempA: 
            tempA = myFile1.readline()
            temp1 = tempA.strip()
            if temp1:
                temp2 = temp1.split('\t')
                dataTable1.append(temp2)
        myFile1.close()
        for i in range(0, len(dataTable1)): 
            lineTemp = (dataTable1[i])
            #print lineTemp[0]
            wordID_tags.append(lineTemp[0]) ##Word IDs
            word_tags.append(lineTemp[1])
        #print len(wordID_tags)
        ii = 0
        ##Mod Eve File : 
        #### Sent Onset Time point (in samples)
        while tempB:
            tempB = myFile2.readline()
            temp1 = tempB.strip('\t')
            if temp1:
                temp2 = temp1.split()
                dataTable2.append(temp2)
        dataTable2.append(['0', '0', '0', '0']) ## to account for the lineTemp_next line :/ 
        number = 0
        for i in range(0, len(dataTable2)-1):
            lineTemp = (dataTable2[i])        
            sentwordID = wordID_tags[ii]
            sentword = word_tags[ii]
            #print sentword
            if (lineTemp[2] == '100' or lineTemp[2] == '111' or lineTemp[2] == '0'): #######[3] Modified aftER USING MAKEeVEfILES.PY TYO CREATE EVENT FILES. 
                ii = ii+1
            elif  (lineTemp[2] == '110'):
                ii = ii + 1
                #print 'here jane'
                number = 0
            elif (sentword == 'The' or sentword == 'the' or sentword == 'was' or sentword == 'a'):
                ii = ii +1
            else:
                ii = ii+1
                number = number + 1
                word_rank = number * 1000000
                wordranksentwordID = word_rank + int(sentwordID)  ## Rank of Word in Sentence(1 digit) + Sentence ID (3 digits) + Word ID (3 digits) 
                myFile3.write(lineTemp[0])
                myFile3.write("\t")
                myFile3.write(lineTemp[1])
                myFile3.write("\t")
                myFile3.write(str(wordranksentwordID))
                myFile3.write("\n")
    ##Write the Mod Word Trigger File as well... 
                myFile4.write(lineTemp[0])
                myFile4.write("\t")
                myFile4.write(lineTemp[1])
                myFile4.write("\t")
                myFile4.write(str(1))
                myFile4.write("\n")
                
            #print i
        print "Done! See resulting file in " + trigger_file + ' and ' + '\n' + Modtrigger_file
    else:
        print "File not found.... Check your inputs!!"
        
def PreStim(subjID, sessID, runID):
    sessNum = sessID[1:]
    print sessNum
    data_path = '/mnt/file1/binder/KRNS/kr3/' + subjID + '/' + sessNum + '/eprime/'
    sent_file = data_path + 'data_sentences' + runID.zfill(2) + '.txt'
#    dataWord_file = data_path + 'eprime_run0' + runID + '.txt'
    eve_file = '/home/custine/MEG/data/krns_kr3/' +subjID+'/'+sessID+ '/eve/' + subjID + '_'+ sessID +'_run'+runID + '.eve'
    Modeve_file = '/home/custine/MEG/data/krns_kr3/' +subjID+'/'+sessID+ '/eve/mod/' + subjID + '_'+ sessID +'_run'+runID + '_Mod.eve'
    trigger_file = '/home/custine/MEG/data/krns_kr3/' +subjID+'/'+sessID+ '/eve/triggers/' + subjID + '_'+ sessID +'_run'+runID + '_PreStim-Triggers.eve'
#    dataWord_file = '/home/custine/MEG/data/krns_kr3/' +subjID+'/'+sessID+ '/eve/' + 'word_sentences' + runID.zfill(2) + '.txt'
    Modtrigger_file = '/home/custine/MEG/data/krns_kr3/' +subjID+'/'+sessID+ '/eve/triggers/' + subjID + '_'+ sessID +'_run'+runID + '_PreStim-TriggersMod.eve'
    print sent_file
    
    tempA = 1
    dataTable1 = []
    dataTable2 = []
    tempB = 1
    lineTemp = []
    sentID_tags = []
    word_tags = []
    wordID_tags = []
    sentword = []
    sentwordID = []
    
    if os.path.exists(eve_file):
        print "Using Modified Eve file: " + eve_file
        print 
        ##Sent File:
        #### SentID Onset and Offset Tags
        myFile1 = open(Modeve_file, "r")
        myFile2 = open(sent_file, "r")
        myFile3 = open(trigger_file, "w")
        myFile4 = open(Modtrigger_file, "w")
       
       ##Mod Event File 
        while tempA: 
            tempA = myFile1.readline()
            temp1 = tempA.strip()
            #print temp1
            if temp1:
                temp2 = temp1.split("\t")    
                dataTable1.append(temp2)
        myFile1.close()
       
        ##Sentence ID file in mnt/        
        while tempB: 
            tempB = myFile2.readline()
            temp1 = tempB.strip()
            #print temp1
            if temp1:
                temp2 = temp1.split("\t")
                dataTable2.append(temp2[0])
                sentID_tags.append(temp2[0])
        myFile2.close()
        sentID_tags = sentID_tags[0:]
        print sentID_tags
        
        ii = 0
        ##Trigger File wrtiting 
        for i in range(0, len(dataTable1)): 
            lineTemp = (dataTable1[i])
            if lineTemp[2] in str(range(34)):
                ii+=1
                newSamp = str(int(lineTemp[0]) - 1200)
                myFile3.write(newSamp)
                myFile3.write("\t")
                myFile3.write(lineTemp[1])
                myFile3.write("\t")
                myFile3.write(sentID_tags[ii])
                myFile3.write("\n")
                
                myFile4.write(newSamp)
                myFile4.write("\t")
                myFile4.write(lineTemp[1])
                myFile4.write("\t")
                myFile4.write('1')
                myFile4.write("\n")

                
                
def Category(subjID, sessID, runID, Category):
    #print "Under construction.. :)"
    data_path = '/home/custine/MEG/data/krns_kr3/' +subjID+'/' + sessID
    wordTrigger_file = data_path + '/eve/triggers/' + subjID + '_'+ sessID +'_run' +runID + '_Word-Triggers.eve'
    wordCategory_file = '/home/custine/MEG/scripts/krns_kr3/Info/WordCategory_' + Category + '.txt' 
    ModTrigger_file = '/home/custine/MEG/data/krns_kr3/' +subjID+'/'+sessID+ '/eve/triggers/' + subjID + '_'+ sessID +'_run'+runID + '_' + Category + '-TriggersMod.eve'
    

    tempA = 1
    dataTable1 = []
    dataTable2 = []
    tempB = 1
    lineTemp = []
    word_tags = []
    jane = []
    categorywords = []
    ii = 0
    
    if os.path.exists(wordTrigger_file):
        print "Using Word Trigger Eve file: " + wordTrigger_file
        print 
        print "Creating the " + Category + ' word trigger file for the selected subject, session'
        print 
        ##Sent File:
        #### SentID Onset and Offset Tags
        myFile1 = open(wordTrigger_file, "r")
        myFile2 = open(ModTrigger_file, "w")
        myFile3 = open(wordCategory_file, "r")
        print wordCategory_file
        #######################################################################
        ##Category Word file         
        while tempB: 
            tempB = myFile3.readline()
            temp1 = tempB.strip('\t')
            if temp1:
                temp2 = temp1.split( )
                dataTable2.append(temp2)
        myFile3.close()
        for i in range(0, len(dataTable2)): 
            lineTemp = (dataTable2[i])
            #print lineTemp
            categorywords.append(lineTemp[0])
        #######################################################################
        ## Word Trigger eve file 
        while tempA: 
            tempA = myFile1.readline()
            temp1 = tempA.strip('\t')
            if temp1:
                temp2 = temp1.split( )
                dataTable1.append(temp2)
        myFile1.close()
        for i in range(0, len(dataTable1)): 
            lineTemp = (dataTable1[i])
            jane = lineTemp[2] ##***********[3]#####REMOVED AFTER USING MAKEeVEfILES.PY TYO CREATE EVENT FILES. 
            jane = str(int(jane[3:]))
            word_tags.append(jane)
            if jane in (categorywords):
                ii = ii +1
                myFile2.write(lineTemp[0])
                myFile2.write("\t")
                myFile2.write(lineTemp[1])
                myFile2.write("\t")
#                myFile2.write(lineTemp[2]) ##*****#####REMOVED AFTER USING MAKEeVEfILES.PY TYO CREATE EVENT FILES. 
#                myFile2.write("\t")
                myFile2.write('1')
                myFile2.write("\n")

        print 'Total number of tagged words in the run are ' + str(len(word_tags))
        print 'Number of ' + Category + ' words found are ' + str(ii)
        print 
#        print 'Word tags IDs in the list are below: '
#        print word_tags       
    
if __name__ == "__main__":
    ####### Get Input ########
    subjID = sys.argv[1] ##9367 
    sessID = sys.argv[2] ##s5
    runs = ['1', '2', '3', '4', '5','6', '7', '8', '9', '10', '11', '12']  # TESTING################################################
    Trig_type = sys.argv[3]

    for runID in runs: 
         ##"Sent" or "Word" or "Category"
        print 
        print "Subject ID:" + subjID
        print "Sess ID:" + sessID 
        print "Run Number:" + runID
        print "Asking for " + Trig_type + " Triggers..."
        
        if Trig_type == "Sentence":
            Sentences(subjID, sessID, runID)
            
        elif Trig_type == 'Words': 
            Words(subjID, sessID, runID)
            
        elif Trig_type == 'PreStim':
            PreStim(subjID, sessID, runID)
        else:
            Type = sys.argv[4]
            Category(subjID, sessID, runID, Type)
        