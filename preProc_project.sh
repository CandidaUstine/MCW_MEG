#!/bin/csh -f

## INSTRUCTIONS
# This is the wrapper script for SSP using mne. You can enter your preferred tag: if you would like only ecg(ecg), only eog(eog) or both ecg and eog(ecgeog) projection applied together. This script will do the following:
# 1) Detecting Artifact Events and saving as a text file a) ECG events b) EOG events. This is done by calling two individual scripts for detecting the ECG and EOG separately using the ECG 063 and EOG 061 VEOG electrode reference channels. 
# 2) Creating projectors a) ECG projector b) EOG projector. 
# 3) Applying projectors and creating the final projected fif file. 
#
## USAGE: ./preProc_project.sh subjID tag par nmag ngrad neeg 
## EXAMPLE: ./preProc_project.sh ac1 ecgeog ATLLoc 1 1 1

if ( $#argv == 0 ) then 
    echo "NO ARGUMENT SPECIFIED: Format - subjID tag paradigm"
    exit 1
endif

## ## ## ## ## CHANGE HERE: edit this to the directory to where you have saved your raw data. 
cd /home/custine/MEG/data/msabri/$1
set subj_dir =  /home/custine/MEG/data/msabri/$1
set log = $subj_dir/logs/preProc_project.log
######### STEP 1: Detecting Events ##########  

if $2 == 'ecg' then 
 matlab -nosplash -nodesktop -nodisplay < /home/custine/MEG/scripts/ssp_find_ecg_event.m >>& $log 
else if $2 == 'eog' then 
# matlab -nosplash -nodesktop -nodisplay < /home/custine/MEG/scripts/ssp_find_eog_event.m >>& $log 
else
 matlab -nosplash -nodesktop -nodisplay < /home/custine/MEG/scripts/ssp_find_ecg_event.m >>& $log 
 matlab -nosplash -nodesktop -nodisplay < /home/custine/MEG/scripts/ssp_find_eog_event.m >>& $log 

endif

######### STEP 2: Setting Parameters ##########

if $2 == 'ecg' then 
    set lfreq = 35
    set hfreq = 5
    set projtmin = -0.08
    set projtmax = 0.08
    set ngrad = 1
    set nmag = 1 
    set neeg = 0
    set e_tmin = -0.2
    set e_tmax = 0.2
    set h_tmin = -0.08
    set h_tmax = 0.08
else if $2 == 'eog' then
    set lfreq = 35
    set hfreq = 0.3 
    set projtmin = -0.2
    set projtmax = 0.2
    set ngrad = 1 
    set nmag = 1
    set neeg = 1 
    set e_tmin = -0.02
    set e_tmax = 0.02
    set h_tmin = -0.08
    set h_tmax = 0.08
else if $2 == 'ecgeog' then
    set lfreq = 35
    set hfreq = 0.3 
    set e_tmin = -0.2
    set e_tmax = 0.2
    set h_tmin = -0.08
    set h_tmax = 0.08
endif 


######## STEP 3: Creating and Applying Projectors ##########

foreach i ({$1}*_raw.fif)
 echo $i
#	python  /cluster/kuperberg/SemPrMM/MEG/scripts/ssp_clean_ecgeogProj.py --in_path /cluster/kuperberg/SemPrMM/MEG/data/$1/ -i $i -c "ECG 061" --e_tmin $e_tmin --e_tmax $e_tmax --h_tmin $h_tmin --h_tmax $h_tmax --l-freq $lfreq --h-freq $hfreq --rej-grad $gradrej --rej-mag $magrej --rej-eeg $eegrej --tag $2 -g $5 -m $4 -e $6											   
end

