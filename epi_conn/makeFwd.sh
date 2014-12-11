#!/bin/csh -f 

##Created on Mon Mar  3 09:47:21 2014
##@author: custine
##Script for epi_conn pilot study 
##./makeFwd.sh subjID 
## ./makeFwd.sh EP1 

echo "Subject ID: " 
echo $1 
set subj_dir = /home/custine/MEG/data/epi_conn/$1/
set surf_dir = /home/custine/MRI/structurals/subjects/
setenv SUBJECTS_DIR $surf_dir
setenv SUBJECT $1
set log = /home/custine/MEG/data/epi_conn/$1/logs/$1_makeFwd.log

##remove the existing log file
if ( -e $log ) then
    rm $log
endif

echo $1
if ( $#argv == 2 ) then
    touch $log
    echo "Logging to default log..." >>& $log
endif

set runList = (DFNAM-noise CRM-noise) # run 2 run3 run1 CRM DFNAM 

cd $subj_dir/ave_projon/
pwd
#foreach m ('meg' 'eeg')

echo "Computing forward solutions for individual runs..."
foreach m ('meg')
   foreach run ($runList)
      echo $run
      mne_do_forward_solution --subject $1 --bem $1-5120-5120-5120-bem.fif --megonly --meas {$run}-ave.fif --fwd $1_{$run}-ave-7-$m-fwd.fif --overwrite >>& $log
   end
end

echo "Averaging Forward Solutions..."
foreach m ('meg')
	#mne_average_forward_solutions \
	#--fwd $1_run1-ave-7-$m-fwd.fif \
	#--fwd $1_run2-ave-7-$m-fwd.fif \
	#--fwd $1_run3-ave-7-$m-fwd.fif \
	#--out $1_All-ave-7-$m-fwd.fif ##>>&log
end



