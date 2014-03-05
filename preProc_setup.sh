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

if ( $#argv == 2) then
    set log=$2
endif

# if log exists, delete
if ( -e $log ) then
    rm $log
endif


## ## ## ## ## CHANGE HERE: edit this to the directory to where you have saved your raw data. 
cd /home/custine/MEG/data/$1/$2
set subj_dir = '/home/custine/MEG/data/'$1'/'$2


mkdir eve -m g+rws
mkdir ave -m g+rws
mkdir cov -m g+rws
mkdir ave_projon -m g+rws
mkdir ave_projoff -m g+rws
mkdir ave_projon/logs -m g+rws
mkdir ave_projon/plots -m g+rws
mkdir ave_projoff/logs -m g+rws
mkdir ave_projoff/plots -m g+rws
mkdir ssp -m g+rws
mkdir rej -m g+rws
mkdir logs -m g+rws 

set log = $subj_dir/logs/$2_preProc_setup.log
date >>& $log

################################################################
##Save read-only copy of raw-files and make other ones writeable
if ( ! -d "raw_backup" ) then
	mkdir raw_backup
	mv *.fif raw_backup
	cp raw_backup/*.fif .
	chmod ug=rwx *.fif
endif

##############################################################
## ## ## ## ## CHANGE HERE:
###Change name of Backup runs
mv $2_EmptyRoom_raw_sss.fif $2_EmptyRoom_raw.fif
mv $2_AudioRun1_raw_sss.fif $2_AudioRun1_raw.fif
mv $2_AudioRun2_raw_sss.fif $2_AudioRun2_raw.fif
mv $2_VisualRun1_raw_sss.fif $2_VisualRun1_raw.fif
mv $2_VisualRun2_raw_sss.fif $2_VisualRun2_raw.fif
mv $2_VisualRun3_raw_sss.fif $2_VisualRun3_raw.fif

#############################################################
###Extracting events read from .fif files into .eve text files
cd /home/custine/MEG/data/$1/$2
echo "Extracting events" >>& $log
foreach run ('AudioRun1' 'AudioRun2' 'VisualRun1' 'VisualRun2' 'VisualRun3') 
        echo $run
	if ( -e $2_{$run}_raw.fif ) then  
            mne_process_raw --raw $2_{$run}_raw.fif --eventsout {$subj_dir}/eve/$2_{$run}.eve --digtrig STI101 --digtrigmask 49407 >>& $log
        endif
end
echo "Extracted events saved in the /eve folder" >>& $log 

#########################################################
##Remove any existing *eve.fif files for internal consistency
rm *raw-eve.fif
#rm eve/*.eve


#############################################################
###Marking bad channels
echo
echo "Marking bad channels" >>& $log
if ( -e $2_bad_chan.txt ) then
	foreach f ( *_raw.fif )
		mne_mark_bad_channels --bad $2_bad_chan.txt $f >>& $log
	end
endif

#############################################################
echo
date >>& $log
echo "Finished preProc - setup" >>& $log
################################################################




















