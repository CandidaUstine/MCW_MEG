###makeAveFiles.py script to create the ave files that are used when creating the ave.fif average files in mne using mne_process_raw


import sys
import os
import condCodes as cc 

def makeAveFiles(subjID, projType):
    
    filePrefix = 'home/custine/MEG/data/msabri/' + subjID
    
    gradRej = "2000e-13"
    magRej = "3000e-15"
    eegRej = "100e-6"
    magFlat = "1e-14"
    gradFlat = "1000e-15"
    
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
        myFile.write('\tname\t\"'+exp+'averages\"\n')
        myFile.write('\toutfile\t\t'+subjID+'_'+exp+'-ave.fif\n')
        myFile.write('\t\tlogfile\t\t./logs/'+subjID+'_'+exp+'-ave.log\n')
        myFile.write('\n')
        
        if projType == 'projon':
            myFile.write('\t\teventfile\t\t'+filePrefix+'/eve/'+subjID+'_mod.eve\n\n')
            myFile.write('\tgradReject\t'+gradRej+'\n\n')
            myFile.write('\tmagReject\t'+magRej+'\n\n')
            myFile.write('\teegReject\t'+eegRej+'\n\n')
            myFile.write('\tgradFlat\t'+gradFlat+'\n\n')
            myFile.write('\tmagFlat\t'+magFlat+'\n\n')            
            myFile.write('\teegFlat\t'+gradFlat+'\n\n')
            
            
            
        
    
if __name__ == "__main__":
    makeAveFiles(sys.argv[1], sys.argv[2])
