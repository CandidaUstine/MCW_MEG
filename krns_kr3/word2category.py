# -*- coding: utf-8 -*-
"""
Created on Tue Aug 26 16:21:54 2014

@author: custine
python word2category.py 
"""

import os 

data_path = '/mnt/file1/binder/KRNS/' 
sentList_file = data_path + 'info/krns_sentence_list.txt'
wordList_file = data_path + 'info/krns_word_list.txt'
WordCategory_N_file = '/home/custine/MEG/scripts/krns_kr3/Info/WordCategory_Noun.txt'
WordCategory_A_file = '/home/custine/MEG/scripts/krns_kr3/Info/WordCategory_Adjective.txt'
WordCategory_V_file = '/home/custine/MEG/scripts/krns_kr3/Info/WordCategory_Verb.txt'
WordCategory_P_file = '/home/custine/MEG/scripts/krns_kr3/Info/WordCategory_Preposition.txt'

tempA = 1
dataTable1 = []
lineTemp = []
wordID_tags = []
word_tags = []
noun = []
verb = []
preposition = []
adjective = []
noun_tags = []
verb_tags = []
preposition_tags = []
adjective_tags = []

myFile1 = open(wordList_file, "r")
myFile2 = open(WordCategory_A_file, "w")
myFile3 = open(WordCategory_V_file, "w")
myFile4 = open(WordCategory_N_file, "w")
myFile5 = open(WordCategory_P_file, "w")

############################################### 
#Word List 
while tempA:
    tempA = myFile1.readline()
    temp1 = tempA.strip('\t')
    if temp1:
        temp2 = temp1.split()
        dataTable1.append(temp2)
dataTable1.append(['0', '0', '0', '0']) ## to account for the lineTemp_next line :/ 
for i in range(0, len(dataTable1)-1):
    lineTemp = (dataTable1[i])
    wordID_tags.append(lineTemp[0])
    word_tags.append(lineTemp[1])
    if (lineTemp[2] == 'A'):
        adjective_tags.append(lineTemp[0])
        adjective.append(lineTemp[1])
        myFile2.write(lineTemp[0])
        myFile2.write('\t')
        myFile2.write(lineTemp[1])
        myFile2.write('\n')
    elif (lineTemp[2] == 'V'):
        verb_tags.append(lineTemp[0])
        verb.append(lineTemp[1])
        myFile3.write(lineTemp[0])
        myFile3.write('\t')
        myFile3.write(lineTemp[1])
        myFile3.write('\n')
    elif (lineTemp[2] == 'N'):
        noun_tags.append(lineTemp[0])
        noun.append(lineTemp[1])
        myFile4.write(lineTemp[0])
        myFile4.write('\t')
        myFile4.write(lineTemp[1])
        myFile4.write('\n')
    elif (lineTemp[2] == 'P'):
        preposition_tags.append(lineTemp[0])
        preposition.append(lineTemp[1])
        myFile5.write(lineTemp[0])
        myFile5.write('\t')
        myFile5.write(lineTemp[1])
        myFile5.write('\n')        
print "noun: \n"
print noun


        
    
#    
#for i in range(len(word_tags)):
#    print word_tags[i]
#    
#print len(word_tags)