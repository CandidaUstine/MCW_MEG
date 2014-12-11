#!/bin/csh -f 

##Created on Mon Mar  3 09:47:21 2014
##@author: custine
##./makeFwd.sh exp subjID

setenv SUBJECT $2
set subj_dir = /home/custine/MEG/data/$1/$2
set log = $subj_dir/logs/$2_makeFwd.log

##remove the existing log file
if ( -e $log ) then
    rm $log
endif

if ( $#argv == 3 ) then
    touch $log
    echo "Logging to default log..." >>& $log
endif

cd $subj_dir/ave_projon/

echo $subj_dir
#foreach m ('meg' 'eeg')
echo "Computing forward solutions for individual runs..."
foreach m ('meg')
   foreach exp ('AudioRun1' 'AudioRun2')
      echo $exp
      mne_do_forward_solution --subject $2 --bem $2-5120-5120-5120-bem.fif --megonly --meas $2_$exp-ave.fif --fwd $2_$exp-ave-7-$m-fwd.fif --overwrite >>& $log
##      if ($m == 'eeg')
##          mne_do_forward_solution --subject $2 --bem $2-5120-5120-5120-bem.fif --eegonly --meas $2_$exp-ave.fif --fwd $2_$exp-ave-7-$m-fwd.fif --overwrite >>& $log
##      endif
   end
end

echo "Averaging Forward Solutions..."
foreach m ('meg')
	mne_average_forward_solutions --fwd $2_AudioRun1-ave-7-$m-fwd.fif --fwd $2_AudioRun2-ave-7-$m-fwd.fif --out $2_Audio_All-ave-7-$m-fwd.fif >>&log
end

echo "Finished. Please see results in subject's ave_projon folder"
