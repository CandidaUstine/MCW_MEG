#!/bin/csh -f

##Created on Wed Apr  2 14:45:27 2014
##author: custine
## for epi_conn

##Usage: ./makeInv.sh subjID 
##Ex: ./makeInv.sh 9367

echo "Subject ID: " 
echo $1 
set subj_dir = /home/custine/MEG/data/epi_conn/$1/
set surf_dir = /home/custine/MRI/structurals/subjects/
setenv SUBJECTS_DIR $surf_dir
setenv SUBJECT $1
set log = /home/custine/MEG/data/epi_conn/$1/logs/$1_makeInv.log

##Remove the existing log file
if ( -e $log ) then
    rm $log
endif

if ( $#argv == 2 ) then
    touch $log
    echo "Logging to default log..." >>& $log
endif
set runList = (run1 )

cd $subj_dir/ave_projon/
date >>&$log 
pwd
#ls 

##Create Inverse Solutions 
foreach t ('meg')
   foreach run ($runList)
        echo $run
	mne_do_inverse_operator --fwd $1_{$run}-ave-7-$t-fwd.fif --depth --loose 0.5 --$t --senscov ../cov/emptyroom-cov.fif --inv $1_{$run}-ave-7-$t-inv.fif >>&$log 
   end
   #mne_do_inverse_operator --fwd $1_$2_$3_All-ave-7-$t-fwd.fif --depth --loose 0.5 --$t --senscov ../cov/$1_$2_emptyroom-cov.fif --inv $1_$2_$3_All-ave-7-$t-inv.fif >>&$log 
end 

##Create Morph maps between the subject space and fsaverage 
mne_make_morph_maps --from $1 --to fsaverage >>&$log 

date >>&$log 

echo "Finished. Check the Inv solutions in the subject's ave_projon folder" 

