# -*- coding: utf-8 -*-
"""
Created on Wed Apr  2 12:09:11 2014

@author: custine
Usage: python makeCovFiles.py exp subjID parName 
Example: python makeCovFiles.py custine cu1 Audio
"""

import sys
import condCodes as cc 

def makeCovFiles(exp, subjID):

    filePrefix = '/home/custine/MEG/data/' + exp + '/' + subjID
    tMin = '-0.1' #Set this Time(in secs) to be the beginning of your epoch
    
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
    #print condDict 
    #print epMaxDict
    for par in parList:
        for run in runDict[par]:
            filename = filePrefix + '/cov/' + subjID + '_' + par + run + '.cov'
            #print filename 
            myFile = open(filename, 'w')
            myFile.close()
            
            myFile = open(filename, 'a')
            myFile.write('cov {\n\n')
            myFile.write('\tname\t\t\"' + par + '\"\n')
            myFile.write('\toutfile\t\t' + subjID + '_' +par+run+ '-cov.fif\n')
            myFile.write('\tlogfile\t\t' + filePrefix + '/logs/' + subjID + '_' + par + run + '-cov.log\n')
            myFile.write('\teventfile\t' + filePrefix + '/eve/' + subjID + '_' + par + run + '.eve\n')
            myFile.write('\n')
            myFile.write('\tgradReject\t' + gradRej + '\n')
            myFile.write('\tmagReject\t' + magRej + '\n')
            myFile.write('\n')
            for item in condDict[par]:
                myFile.write('\tdef {\n')
                myFile.write('\t\tname\t\"' + item[1] +'\"\n')
                myFile.write('\t\tevent\t' + item[0] +'\n')
                myFile.write('\t\tignore\t0\n')
                myFile.write('\t\ttmin\t'+tMin+'\n')
                myFile.write('\t\ttmax\t-0.01\n')
                myFile.write('\t\tbmin\t'+tMin+'\n')
                myFile.write('\t\tbmax\t-0.01\n\t}\n\n')
            myFile.write('}\n')
            
            

if __name__ == "__main__":
    
    makeCovFiles(sys.argv[1], sys.argv[2])
        
        