#!/bin/csh -f

## INSTRUCTIONS
## This the preliminary step you will have to do to your raw fif file that you get from the scanner. It does the following
##
## 1) makes a data structure within your main data directory for all the results of your analyses so they can be easily retrieved
## 2) removes an inconsistent -eve files from teh current directory 
## 3) renames files - IF NECESSARY
##
## usage: preProc_setup.sh subjID logfile

if ( $#argv == 0 ) then 
    echo "NO SUBJECT ARGUMENT"
    exit 1
endif

if ( $#argv == 1 ) then
    set log='./preProc_setup.log'
    echo "Logging to default log..." >>& $log
endif

if ( $#argv == 2) then
    set log=$2
endif

# if log exists, delete
if ( -e $log ) then
    rm $log
endif


## ## ## ## ## CHANGE HERE: edit this to the directory to where you have saved your raw data. 
cd /home/custine/MEG/data/msabri/$1

date >>& $log

mkdir eve -m g+rws
mkdir ave -m g+rws
mkdir cov -m g+rws
mkdir ave_projon -m g+rws
mkdir ave_projoff -m g+rws
mkdir ave_projon/logs -m g+rws
mkdir ave_projoff/logs -m g+rws
mkdir ssp -m g+rws
mkdir rej -m g+rws
mkdir logs -m g+rws 

#########################################################
##Remove any existing *eve.fif files for internal consistency
rm *raw-eve.fif
#rm eve/*.eve

################################################################
##Save read-only copy of raw-files and make other ones writeable
if ( ! -d "raw_backup" ) then
	mkdir raw_backup
	mv *.fif raw_backup
	cp raw_backup/*.fif .
endif


chmod ug=rwx *.fif

################################################################
## ## ## ## ## CHANGE HERE:
##Change name of Backup runs
mv run00_emptyroom_raw_sss.fif $1_EmptyRoom_raw.fif
mv run01_sponteyesopen_raw_sss.fif $1_SpontEyeOpen_raw.fif
mv run02_oddball_left_raw_sss_xtraClean_raw.fif $1_Left_raw.fif
mv run03_dual_oddball_left_raw_sss_xtraClean_raw.fif $1_LeftDual_raw.fif
mv run04_oddball_right_raw_sss.fif $1_Right_raw.fif 
mv run03_dual_oddball_right_raw_sss_xtraClean_raw.fif $1_RightDual_raw.fif

#############################################################
##Extracting events read from .fif files into .eve text files

echo "Extracting events" >>& $log
foreach run ('EmptyRoom', 'SpontEyeOpen', 'Left', 'LeftDual', 'Right', 'RightDual')

	if ( -e $1_{$run}_raw.fif ) then  
            mne_process_raw --raw $1_{$run}_raw.fif --eventsout eve/$1_{$run}.eve --digtrig STI014 >>& $log
        endif
end
echo "Extracted events saved in the /eve folder" >>& $log 

#############################################################
###Marking bad channels

echo
echo "Marking bad channels" >>& $log

if ( -e $1_bad_chan.txt ) then
	foreach f ( *_raw.fif )
		mne_mark_bad_channels --bad $1_bad_chan.txt $f >>& $log
	end
endif

#############################################################
echo
date
echo "Finished preProc - setup" >>& $log
################################################################

mv /home/custine/MEG/data/msabri/$1/preProc_setup.log /home/custine/MEG/data/msabri/$1/logs/preProc_setup.log
