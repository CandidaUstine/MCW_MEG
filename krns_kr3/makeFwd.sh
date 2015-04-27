#!/bin/csh -f 

##Created on Mon Mar  3 09:47:21 2014
##@author: custine
##Script for Krns_kr3 study 
##./makeFwd.sh subjID sessID par
## ./makeFwd.sh 9367 s5 Word/AllItems/Noun/Noun_People/Noun_People_ssp

echo "Subject ID: " 
echo $1 
echo "Session ID: " 
echo $2
set subj_dir = /home/custine/MEG/data/krns_kr3/$1/$2/
set surf_dir = /mnt/file1/binder/KRNS/anatomies/surfaces
setenv SUBJECTS_DIR $surf_dir
setenv SUBJECT $1
set log = /home/custine/MEG/data/krns_kr3/$1/$2/logs/$1_$2_$3_makeFwd.log

##remove the existing log file
if ( -e $log ) then
    rm $log
endif

echo $3
if ( $#argv == 3 ) then
    touch $log
    echo "Logging to default log..." >>& $log
endif

set runList = (run1 run2 run3 run4 run5 run6 run7 run8 run9 run10 run11 run12)  #

cd $subj_dir/ave_projon/
pwd
#foreach m ('meg' 'eeg')

echo "Computing forward solutions for individual runs..."
foreach m ('meg')
   foreach run ($runList)
      echo $run
      mne_do_forward_solution --subject $1 --bem $1-5120-5120-5120-bem.fif --mri COR-custine-$2.fif --megonly --meas $1_$2_{$run}_$3_run-ave.fif --fwd $1_$2_{$run}_$3-ave-7-$m-fwd.fif --overwrite >>& $log
   end
end

echo "Averaging Forward Solutions..."
foreach m ('meg')
	mne_average_forward_solutions \
	--fwd $1_$2_run1_$3-ave-7-$m-fwd.fif \
	--fwd $1_$2_run2_$3-ave-7-$m-fwd.fif \
	--fwd $1_$2_run3_$3-ave-7-$m-fwd.fif \
	--fwd $1_$2_run4_$3-ave-7-$m-fwd.fif \
	--fwd $1_$2_run5_$3-ave-7-$m-fwd.fif \
	--fwd $1_$2_run6_$3-ave-7-$m-fwd.fif \
	--fwd $1_$2_run7_$3-ave-7-$m-fwd.fif \
	--fwd $1_$2_run8_$3-ave-7-$m-fwd.fif \
	--fwd $1_$2_run9_$3-ave-7-$m-fwd.fif \
	--fwd $1_$2_run10_$3-ave-7-$m-fwd.fif \
	--fwd $1_$2_run11_$3-ave-7-$m-fwd.fif \
	--fwd $1_$2_run12_$3-ave-7-$m-fwd.fif \
	--out $1_$2_$3_All-ave-7-$m-fwd.fif >>&log
end




