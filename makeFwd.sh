#!/bin/csh -f 

##Created on Mon Mar  3 09:47:21 2014
##@author: custine
##./makeFwd.sh exp subjID

setenv SUBJECT $2
set subj_dir = /home/custine/MRI/structurals/subjects/$2
set log = $subj_dir/logs/$2_preProc_setup.log

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
foreach m ('meg' 'eeg')
   foreach exp ('Left' 'Right' 'LeftDual' 'SponEyeOpen')
      echo $exp
      mne_do_forward_solution --bem $2-5120-5120-5120-bem.fif --megonly --meas $2_$exp-ave.fif --fwd $2_$exp-ave-7-$m-fwd.fif --overwrite >>& $log
      if ($m == 'eeg')
          mne_do_forward_solution --bem $2-5120-5120-5120-bem.fif --eegonly --meas $2_$exp-ave.fif --fwd $2_$exp-ave-7-$m-fwd.fif --overwrite >>& $log
      endif
   end
end
