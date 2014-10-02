#!/bin/csh -f

## INSTRUCTIONS
## This the preliminary step you will have to do to your raw fif file that you get from the scanner. It does the following
## FOR EPI_CONN grant pilot study... 
##
## usage: preProc_setup.sh subjID 

if ( $#argv == 0 ) then 
    echo "NO SUBJECT ARGUMENT"
    exit 1
endif

if ( $#argv == 2) then
    set log=$2
endif

## ## ## ## ## CHANGE HERE: edit this to the directory to where you have saved your raw data. 
cd /home/custine/MEG/data/epi_conn/$1/
set subj_dir = '/home/custine/MEG/data/epi_conn/'$1'/'

mkdir eve -m g+rws
mkdir ssp -m g+rws
mkdir ssp/fieldtrip -m g+rws
mkdir cov -m g+rws
mkdir logs -m g+rws
mkdir ave_projon -m g+rws
mkdir ave_projon/logs -m g+rws
mkdir ave_projon/plots -m g+rws
mkdir ave_projon/stc -m g+rws
mkdir fig -m g+rws
mkdir orig -m g+rws

if ( ! -d "orig" ) then
	mkdir orig
	mv *.fif orig
	cp orig/*.fif .
	chmod ug=rwx *.fif
endif

###Change name of Backup runs
mv *emptyroom*.fif emptyroom_raw.fif
mv *spont*.fif run1_raw.fif

#########################################################
##Remove any existing *eve.fif files for internal consistency
rm *raw-eve.fif
#rm eve/*.eve

set log = $subj_dir/logs/$1_preProc_setup.log
date >>& $log

foreach f ( run*.fif )
        echo $f
        mne_rename_channels --fif $f --alias ../../../scripts/epi_conn/function_inputs/alias0.txt >>& $log
	mne_rename_channels --fif $f --alias ../../../scripts/epi_conn/function_inputs/alias_EEG.txt >>& $log
