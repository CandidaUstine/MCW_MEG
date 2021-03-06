# -*- coding: utf-8 -*-
"""
Created on Thu Aug 21 10:50:57 2014

@author: custine
Usage: fixTriggers.py subjID sessID
Example: fixTriggers.py 9367 5 
"""

import os 
import os.path
import argparse
from email.mime.text import MIMEText
import smtplib

####### Get Input ########
parser = argparse.ArgumentParser(description='Get input')
parser.add_argument('subj',type=str)
parser.add_argument('sess',type=str) ##Left, Right etc.,
#parser.add_argument('run',type=str) 
args=parser.parse_args()
subjID = args.subj
sessID = args.sess
#runID = args.run
#runID = runID.zfill(2)

runs = ['1', '2', '3', '4', '5','6', '7', '8', '9', '10', '11', '12']  # TESTING################################################
print runs

for runID in runs: 

    
    print 
    print "Subject ID:" + subjID
    print "Sess ID:" + sessID 
    print "Run Number:" + runID
    print 
    
    data_path = '/mnt/file1/binder/KRNS/kr3/' + subjID + '/' + sessID + '/eprime/'
    sent_file = data_path + 'data_sentences' + runID.zfill(2) + '.txt'
    eprime_file = data_path + 'eprime_run' +  runID.zfill(2) + '.txt'
    eve_file = '/home/custine/MEG/data/krns_kr3/' +subjID+'/s'+sessID+ '/eve/' + subjID + '_s'+ sessID +'_run'+runID + '.eve'
    Modeve_file = '/home/custine/MEG/data/krns_kr3/' +subjID+'/s'+sessID+ '/eve/mod/' + subjID + '_s'+ sessID +'_run'+runID + '_Mod.eve'
    tempModeve_file = '/home/custine/MEG/data/krns_kr3/' +subjID+'/s'+sessID+ '/eve/mod/' + subjID + '_s'+ sessID +'_run'+runID + '_tempMod.eve'
    
    tempA = 1
    tempB = 1
    dataTable1 = []
    dataTable2 = []
    lineTemp = []
    lineTemp_next = []
    
    sent_tags = []
    sent_line = []
    
    
    if os.path.exists(eprime_file):
        ##Sent File:
        #### SentIDs
        myFile1 = open(eprime_file, "r")
        while tempA: 
            tempA = myFile1.readline()
            temp1 = tempA.strip()
            if temp1:
                temp2 = temp1.split('\t')
                dataTable1.append(temp2)
        myFile1.close()
        #sent_tags.append('0') #####REMOVED AFTER USING MAKEeVEfILES.PY TYO CREATE EVENT FILES. 
        for i in range(1, len(dataTable1)): #Neglecting the first row - titles 
            lineTemp = (dataTable1[i])
            #print lineTemp #total 58 items (including the 3 probe items for each sentence)
            #sent_tags.append(lineTemp[4])
            sent_tags.append(lineTemp[13])
            sent_tags.append(lineTemp[18])
            sent_tags.append(lineTemp[23])
            sent_tags.append(lineTemp[28])
            sent_tags.append(lineTemp[33])
            sent_tags.append(lineTemp[38])
            sent_tags.append(lineTemp[43])
            sent_tags.append(lineTemp[48])
            sent_tags.append(lineTemp[53])
            if len(lineTemp) > 55:
                sent_tags.append('111')
            sent_tags.append('110')
            sent_line.append(sent_tags)
    
    error = 0   
    if os.path.exists(eprime_file):    
        myFile2 = open(eve_file, "r")
        myFile3 = open(Modeve_file, "w")
        myFile4 = open(tempModeve_file, "w")
        
        ##Eve File : 
        while tempB:
            tempB = myFile2.readline()
            temp1 = tempB.strip('\t')
            if temp1:
                temp2 = temp1.split()
                dataTable2.append(temp2)
        dataTable2.append(['0', '0', '0', '0']) ## to account for the lineTemp_next line :/
        ii = 0
        
        for i in range(0, len(dataTable2)-1):
            lineTemp = (dataTable2[i])
    #        lineTemp[3] = sent_tags[ii]
            myFile3.write(lineTemp[0])
            myFile3.write("\t")
            myFile3.write(lineTemp[1])
            myFile3.write("\t")
#            myFile3.write(lineTemp[2]) #####REMOVED AFTER USING MAKEeVEfILES.PY TYO CREATE EVENT FILES. 
#            myFile3.write("\t")
            if lineTemp[2] == sent_tags[ii]:
                myFile3.write(str(lineTemp[2]))
            else:
                myFile3.write(sent_tags[ii])
                error = error + 1 
            myFile3.write("\n")
            ii = ii + 1
            ##Write the Mod Word Trigger File as well...
            myFile4.write(lineTemp[0])
            myFile4.write("\t")
            myFile4.write(lineTemp[1])
            myFile4.write("\t")
#            myFile4.write(lineTemp[2]) #####REMOVED AFTER USING MAKEeVEfILES.PY TYO CREATE EVENT FILES. 
#            myFile4.write("\t")
            myFile4.write(str(1))
            myFile4.write("\n")
            
        print "Number of Trigger errors when data was recorded = " + str(error)                
                
        print "Done! See resulting file in " + Modeve_file      
    
    
#construct the message
sender = "candida.ustine@gmail.com"
receiver = "candy.ustine@gmail.com"
message = Modeve_file
msg = MIMEText(message)
msg["From"] = sender
msg["To"] = receiver
msg["Subject"] = "Ready Jane"    
   
server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls() 

server.sendmail(sender, receiver, msg.as_string())

server.quit()
    
    
    
    
    
    
    
    
    
    
    
    