#!/bin/csh -f

## INSTRUCTIONS
## This the preliminary step you will have to do to your raw fif file that you get from the scanner. It does the following
##
## 1) makes a data structure within your main data directory for all the results of your analyses so they can be easily retrieved
## 2) removes an inconsistent -eve files from teh current directory 
## 3) renames files - IF NECESSARY
##
## usage: preProc_setup.sh subjID sessID logfile

if ( $#argv == 0 ) then 
    echo "NO SUBJECT ARGUMENT"
    exit 1
endif

if ( $#argv == 3) then
    set log=$3
endif

# if log exists, delete
# if ( -e $log ) then
#   rm $log
# endif


## ## ## ## ## CHANGE HERE: edit this to the directory to where you have saved your raw data. 
cd /home/custine/MEG/data/krns_kr3/$1/$2
set subj_dir = '/home/custine/MEG/data/krns_kr3/'$1'/'$2'/'


mkdir eve -m g+rws
mkdir ave -m g+rws
mkdir cov -m g+rws
mkdir ave_projon -m g+rws
mkdir ave_projoff -m g+rws
mkdir ave_projon/logs -m g+rws
mkdir ave_projon/plots -m g+rws
mkdir ave_projoff/logs -m g+rws
mkdir ave_projoff/plots -m g+rws
mkdir ave_projoff/plots/fieldtrip -m g+rws
mkdir ave_projon/plots/fieldtrip -m g+rws
mkdir ssp -m g+rws
mkdir ssp/fieldtrip -m g+rws
mkdir ssp/mne -m g+rws
mkdir rej -m g+rws
mkdir logs -m g+rws 
mkdir fig -m g+rws

set log = $subj_dir/logs/$1_$2_preProc_setup.log
date >>& $log

################################################################
##Save read-only copy of raw-files and make other ones writeable
#if ( ! -d "raw_backup" ) then
#	mkdir raw_backup
#	mv *.fif raw_backup
#	cp raw_backup/*.fif .
#	chmod ug=rwx *.fif
#endif

##############################################################
## ## ## ## ## CHANGE HERE:
###Change name of Backup runs
mv $1_$2_emptyroom_raw_sss.fif $2_emptyroom_raw.fif
mv $1_$2_run1_raw_sss.fif $1_$2_run1_raw.fif 
mv $1_$2_run2_raw_sss.fif $1_$2_run2_raw.fif 
mv $1_$2_run3_raw_sss.fif $1_$2_run3_raw.fif 
mv $1_$2_run4_raw_sss.fif $1_$2_run4_raw.fif 
mv $1_$2_run5_raw_sss.fif $1_$2_run5_raw.fif 
mv $1_$2_run6_raw_sss.fif $1_$2_run6_raw.fif 
mv $1_$2_run7_raw_sss.fif $1_$2_run7_raw.fif 
mv $1_$2_run8_raw_sss.fif $1_$2_run8_raw.fif 
mv $1_$2_run9_raw_sss.fif $1_$2_run9_raw.fif 
mv $1_$2_run10_raw_sss.fif $1_$2_run10_raw.fif 
mv $1_$2_run11_raw_sss.fif $1_$2_run11_raw.fif 
mv $1_$2_run12_raw_sss.fif $1_$2_run12_raw.fif 

#############################################################
###Extracting events read from .fif files into .eve text files
cd /home/custine/MEG/data/krns_kr3/$1/$2
echo "Extracting events" >>& $log
foreach run ('run1' 'run2' 'run3' 'run4' 'run5' 'run6' 'run7' 'run8' 'run9' 'run10' 'run11' 'run12') 
        echo $run
	if ( -e $1_$2_{$run}_raw.fif ) then  
            mne_process_raw --raw $1_$2_{$run}_raw.fif --eventsout {$subj_dir}/eve/$1_$2_{$run}.eve --digtrig STI102 >>& $log
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
if ( -e $1_$2_bad_chan.txt ) then
	foreach f ( *_raw.fif )
		mne_mark_bad_channels --bad $1_$2_bad_chan.txt $f >>& $log
	end
endif

#############################################################
echo
date >>& $log
echo "Finished preProc - setup" >>& $log
################################################################


