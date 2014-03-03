#!/bin/csh -f 

##Created on Mon Mar  3 09:47:21 2014
##@author: custine
##./makeFwd.sh exp subjID

setenv SUBJECT $2
set subj_dir = /home/custine/MRI/structurals/subjects/$2/

##remove the existing log file
if ( -e /home/custine/MEG/data/{$1}/{$2}/logs/makeFwd.log ) then
    rm /home/custine/MEG/data/{$1}/{$2}/logs/makeFwd.log
endif

if ( $#argv == 3 ) then
    touch /home/custine/MEG/data/{$1}/{$2}/logs/makeFwd.log
    echo "Logging to default log..." >>& /home/custine/MEG/data/{$1}/{$2}/logs/makeFwd.log
endif

cd /home/custine/MEG/data/$1/$2/ave_projon/

foreach m ('meg') ## 'eeg')
   foreach exp ('Left' 'Right' 'LeftDual' 'SponEyeOpen')
      echo $exp
      mne_do_forward_solution --bem $2-5120-5120-5120-bem.fif --megonly --meas $2_$exp-ave.fif --fwd $2_$exp-ave-7-$m-fwd.fif --overwrite >>& /home/custine/MEG/data/{$1}/{$2}/logs/makeFwd.log
     # if ($m == 'eeg')
     #     mne_do_forward_solution --bem $2-5120-5120-5120-bem.fif --eegonly --meas $2_$exp-ave.fif --fwd $2_$exp-ave-7-$m-fwd.fif --overwrite >>& /home/custine/MEG/data/{$1}/{$2}/logs/makeFwd.log
     # endif
   end
end
