#!/bin/csh -f

## INSTRUCTIONS
# This is the wrapper script for SSP using mne. You can enter your preferred tag: if you would like only ecg(ecg), only eog(eog) or both ecg and eog(ecgeog) projection applied together. This script will do the following:
# 1) Detecting Artifact Events and saving as a text file a) ECG events b) EOG events. This is done by calling two individual scripts for detecting the ECG and EOG separately using the ECG 063 and EOG 061 VEOG electrode reference channels. 
# 2) Creating projectors a) ECG projector b) EOG projector. 
# 3) Applying projectors and creating the final projected fif file. 
#
## USAGE: ./preProc_project.sh exp subjID tag nmag ngrad neeg 
## EXAMPLE: ./preProc_project.sh custine ac1 ecgeog 1 1 1

if ( $#argv == 0 ) then 
    echo "Hey dummy! NO ARGUMENT SPECIFIED! Format - ./preProc_project.sh subjID tag nmag ngrad neeg"
    exit 1
endif

## ## ## ## ## CHANGE HERE: edit this to the directory to where you have saved your raw data. 
cd /home/custine/MEG/data/$1/$2
set subj_dir =  /home/custine/MEG/data/$1/$2
set log = $subj_dir/logs/preProc_project.log

#if log exists, delete
if ( -e $log ) then
    rm $log
endif

########## STEP 1: Detecting Events ########## 
echo "Creating the event files - -eve.fif"
if $3 == 'ecgeog' then
	python /home/custine/MEG/scripts/helpers.py $1 $2 ecg
	matlab -nosplash -nodesktop -nodisplay < /home/custine/MEG/data/$1/$2/ssp/ssp_event_creator.m >>& $log
	python /home/custine/MEG/scripts/helpers.py $1 $2 eog
	matlab -nosplash -nodesktop -nodisplay < /home/custine/MEG/data/$1/$2/ssp/ssp_event_creator.m >>& $log
else then
	python /home/custine/MEG/scripts/helpers.py $1 $2 $3
	matlab -nosplash -nodesktop -nodisplay < /home/custine/MEG/data/$1/$2/ssp/ssp_event_creator.m >>& $log
endif
echo 'Event files created , check your ssp folder'

######### STEP 2: Setting Parameters ##########
##Default Parameters
set magrej = 4000
set gradrej = 3000
set eegrej = 500
if $3 == 'ecg' then 
    set lfreq = 35
    set hfreq = 5
    set ngrad = 1
    set nmag = 1 
    set neeg = 0
    set e_tmin = -0.25
    set e_tmax = 0.25
    set h_tmin = -0.1
    set h_tmax = 0.1
else if $3 == 'eog' then
    set lfreq = 35
    set hfreq = 0.3 
    set ngrad = 1 
    set nmag = 1
    set neeg = 1 
    set e_tmin = -0.25
    set e_tmax = 0.25
    set h_tmin = -0.1
    set h_tmax = 0.1
else if $3 == 'ecgeog' then
    set lfreq = 35
    set hfreq = 0.3 
    set e_tmin = -0.2
    set e_tmax = 0.2
    set h_tmin = -0.08
    set h_tmax = 0.08
endif 

######## STEP 3: Creating and Applying Projectors ##########
cd /home/custine/MEG/data/$1/$2/
pwd
foreach i ({$2}_AudioRun1_raw.fif)
    echo $i 
    echo 'Running the python script... Please wait...'
    python  /home/custine/MEG/scripts/ssp_clean_ecgeogProj.py --in_path /home/custine/MEG/data/$1/$2/ -i $i --e_tmin $e_tmin --e_tmax $e_tmax --h_tmin $h_tmin --h_tmax $h_tmax --l-freq $lfreq --h-freq $hfreq --rej-grad $gradrej --rej-mag $magrej --rej-eeg $eegrej --tag $3 -m $4 -g $5 -e $6										   
end

mv /home/custine/MEG/data/$1/$2/{$2}*_eog_proj.fif /home/custine/MEG/data/$1/$2/ssp/
mv /home/custine/MEG/data/$1/$2/{$2}*_ecg_proj.fif /home/custine/MEG/data/$1/$2/ssp/
mv /home/custine/MEG/data/$1/$2/{$2}*_ecgeog_proj.fif /home/custine/MEG/data/$1/$2/ssp/
rm *_raw-eve.fif
echo 'Completed!'

#########################################################
##Remove any existing *eve.fif files for internal consistency
cd /home/custine/MEG/data/$1/$2/ssp/
rm *raw-eve.fif
#rm eve/*.eve

