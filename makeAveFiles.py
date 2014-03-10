# -*- coding: utf-8 -*-
"""
Created on Thu Feb 13 12:59:34 2014

@author: custine
Usage: python makeAveFiles.py subjID projon
"""


###makeAveFiles.py script to create the ave files that are used when creating the ave.fif average files in mne using mne_process_raw


import sys
import os
import condCodes as cc 

def makeAveFiles(exp, subjID, projType):
    
    filePrefix = '/home/custine/MEG/data/' + exp + '/' + subjID
    
    gradRej = "2000e-13"
    magRej = "3000e-15"
    eegRej = "100e-6"
    magFlat = "1e-14"
    gradFlat = "1000e-15"
    eegFlat = "0"
    
    if exp == 'msabri':    
        parList = ['Left', 'LeftDual', 'Right', 'RightDual']
    elif exp == 'custine':
        parList = ['Audio']
        runDict = {'Audio':['Run1', 'Run2']}
        
    condDict = cc.condLabels
    epMaxDict = cc.epMax
    
    for par in parList: 
        for run in runDict[par]:
            filename = filePrefix + '/ave/' + subjID + '_' + par+ run + '.ave'
            print filename
            myFile = open(filename, "w")
            myFile.close()
            
            myFile = open(filename, "a")
            myFile.write('average{\n')
            myFile.write('\tname\t\"'+par+' Averages\"\n')
            myFile.write('\toutfile\t\t'+subjID + '_'+ par + run +'-ave.fif\n')
            myFile.write('\tlogfile\t\t'+filePrefix+'/logs/'+subjID+'_'+par+run+'-ave.log\n')
            
            if projType == 'projon':
                myFile.write('\teventfile\t'+filePrefix+'/eve/'+subjID+'_'+par+run+'.eve\n\n')
                myFile.write('\tgradReject\t'+gradRej+'\n')
                myFile.write('\tmagReject\t'+magRej+'\n')
                myFile.write('\teegReject\t'+eegRej+'\n')
                myFile.write('\tgradFlat\t'+gradFlat+'\n')
                myFile.write('\tmagFlat\t\t'+magFlat+'\n')            
                myFile.write('\teegFlat\t\t'+eegFlat+'\n\n')
                
            for item in condDict[par]:
                myFile.write('\tcategory {\n')
                myFile.write('\t\tname\t'+item[1]+'\n')
                myFile.write('\t\tevent\t'+item[0]+ '\n')
                myFile.write('\t\ttmin\t-0.1\n')
                myFile.write('\t\ttmax\t'+epMaxDict[par]+'\n\t}\n\n')
                
            myFile.write('}\n')
            
        
    
if __name__ == "__main__":
    makeAveFiles(sys.argv[1], sys.argv[2], sys.argv[3])
