#!/bin/csh - f 

##Created on Wed Apr  2 11:59:48 2014
##author: custine
##Usage: ./preProc_cov.sh exp subjID 
##Example: ./preProc_cov.sh custine cu1 

setenv SUBJECT $2
set subj_dir = /home/custine/MEG/data/$1/$2
set log = $subj_dir/logs/$2_preProc_cov.log

##remove the existing log file
if ( -e $log ) then
    rm $log
endif

echo $log 

echo "Making Cov Parameter files... " >>&$log 
cd $subj_dir/ave_projon
python /home/custine/MEG/scripts/makeCovFiles.py $1 $2 

echo "Computing Covariance using cov files..." >>&$log 
date >>&$log 

mne_process_raw --raw ../$2_AudioRun1_raw.fif --raw ../$2_AudioRun2_raw.fif --digtrig STI101 --cov ../cov/$2_AudioRun1.cov --cov ../cov/$2_AudioRun2.cov --gcov $2_Audio_All-cov.fif --projon --lowpass 30 >>&$log 

date >>&$log 
echo "Finished" >>&$log 

echo "Finished. Please see results in subject's covariance folder"

