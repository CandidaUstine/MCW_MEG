#!/bin/csh -f

##Created on Wed Apr  2 14:45:27 2014
##author: custine
##Usage: ./makeInv.sh exp subjID 
##Ex: ./makeInv.sh custine cu1 

setenv SUBJECT $2
set subj_dir = /home/custine/MEG/data/$1/$2
set log = $subj_dir/logs/$2_makeInv.log

##Remove the existing log file
if ( -e $log ) then
    rm $log
endif

if ( $#argv == 3 ) then
    touch $log
    echo "Logging to default log..." >>& $log
endif

cd $subj_dir/ave_projon/
date >>&$log 
setenv SUBJECT $2 

##Create Inverse Solutions 
foreach t ('meg')
	mne_do_inverse_operator --fwd $2_Audio_All-ave-7-$t-fwd.fif --depth --loose 0.5 --$t --senscov $2_Audio_All-cov.fif --inv $2_Audio_All-ave-7-$t-inv.fif >>&$log 
end 

##Create Morph maps between the subject space and fsaverage 
mne_make_morph_maps --from $2 --to fsaverage >>&$log 

date >>&$log 

echo "Finished. Check the Inv solutions in the subject's ave_projon folder" 
