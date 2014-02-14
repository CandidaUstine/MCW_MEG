# -*- coding: utf-8 -*-
"""
Created on Thu Feb 13 12:59:34 2014

@author: custine
"""


###makeAveFiles.py script to create the ave files that are used when creating the ave.fif average files in mne using mne_process_raw


import sys
import os
import condCodes as cc 

def makeAveFiles(subjID, projType):
    
    filePrefix = '/home/custine/MEG/data/msabri/' + subjID
    
    gradRej = "2000e-13"
    magRej = "3000e-15"
    eegRej = "100e-6"
    magFlat = "1e-14"
    gradFlat = "1000e-15"
    eegFlat = "0"
    
    expList = ['Left', 'LeftDual', 'Right', 'RightDual']
    condDict = cc.condLabels
    epMaxDict = cc.epMax
    
    for exp in expList: 
        filename = filePrefix + '/ave/' + subjID + '_' + exp + '.ave'
        print filename
        myFile = open(filename, "w")
        myFile.close()
        
        myFile = open(filename, "a")
        myFile.write('average{\n')
        myFile.write('\tname\t\"'+exp+' Averages\"\n')
        myFile.write('\toutfile\t\t'+subjID+'_'+exp+'-ave.fif\n')
        myFile.write('\tlogfile\t\t'+filePrefix+'/logs/'+subjID+'_'+exp+'-ave.log\n')
        
        if projType == 'projon':
            myFile.write('\teventfile\t'+filePrefix+'/eve/'+subjID+'_mod.eve\n\n')
            myFile.write('\tgradReject\t'+gradRej+'\n')
            myFile.write('\tmagReject\t'+magRej+'\n')
            myFile.write('\teegReject\t'+eegRej+'\n')
            myFile.write('\tgradFlat\t'+gradFlat+'\n')
            myFile.write('\tmagFlat\t\t'+magFlat+'\n')            
            myFile.write('\teegFlat\t\t'+eegFlat+'\n\n')
            
        for item in condDict[exp]:
            myFile.write('\tcategory {\n')
            myFile.write('\t\tname\t\"'+item[1]+'\"\n')
            myFile.write('\t\tevent\t'+item[0]+ '\n')
            myFile.write('\t\ttmin\t-0.1\n')
            myFile.write('\t\ttmax\t'+epMaxDict[exp]+'\n\t}\n\n')
            
        myFile.write('}\n')
            
        
    
if __name__ == "__main__":
    makeAveFiles(sys.argv[1], sys.argv[2])
