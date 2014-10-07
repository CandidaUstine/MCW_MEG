#!/bin/csh -f

##Created on Fri Oct  3 13:12:35 2014
##author: custine
##For epi_conn study 

##Usage: ./makeSTC.sh subjID t1 t2 
##Ex: ./makeSTC.sh EP1 300 500
## OR  ./makeSTC.sh EP1    ->(Will consider the entire time window) 

echo "Subject ID: " 
echo $1 
set subj_dir = /home/custine/MEG/data/epi_conn/$1/
set surf_dir = /home/custine/MRI/structurals/subjects/
setenv SUBJECTS_DIR $surf_dir
setenv SUBJECT $1
set log = /home/custine/MEG/data/epi_conn/$1/logs/$1_makeSTC.log

set subjID = $1
set tmin = $2
set tmax = $3
set runList = (run1) 

##Remove the existing log file
if ( -e $log ) then
    rm $log
endif

if ( $#argv == 3 ) then
    touch $log
    echo "Using default time window..." >>& $log
    set t = 'full'
else 
    set t = 'time'
endif

cd $subj_dir/ave_projon/
date >>&$log 


  # if ($t == 'full') then
        #echo "Making mne maps... " >>& $log
	#mne_make_movie --inv $1_$2_$3_All-ave-7-meg-inv.fif --meas $1_$2_$3_All-ave.fif --set $c --bmin -100 --bmax -0.01 --stc stc/$1_$2_$3_All_c{$c}M-mne.stc --smooth 5 --morph fsaverage --subject $1 >>& $log  
 
 #       echo "Making dSPM maps... " >>& $log
#	mne_make_movie --inv $1_run1-ave-7-meg-inv.fif --meas $1_run1-ave.fif --set $c --bmin -100 --bmax -0.01 --stc stc/$1_$2_$3_All_c{$c}M-spm.stc --smooth 5 --morph fsaverage --spm --subject $1 >>& $log  

        #echo "Making sLORETA maps... " >>& $log
	#mne_make_movie --inv $1_$2_$3_All-ave-7-meg-inv.fif --meas $1_$2_$3_All-ave.fif --set $c --bmin -100 --bmax -0.01 --stc stc/$1_$2_$3_All_c{$c}M-sLORETA.stc --smooth 5 --morph fsaverage --sLORETA --subject $1 >>& $log 


  # else
        #echo "Making mne maps... " >>& $log
	#mne_make_movie --inv $1_$2_$3_All-ave-7-meg-inv.fif --meas $1_$2_$3_All-ave.fif --set $c --tmin $tmin --tmax $tmax --bmin -100 --bmax -0.01 --stc stc/$1_$2_$3_All_c{$c}M_{$tmin}-{$tmax}-mne.stc --smooth 5 --morph fsaverage --subject $1 >>& $log  
 
        #echo "Making dSPM maps... " >>& $log
	#mne_make_movie --inv $1_$2_$3_All-ave-7-meg-inv.fif --meas $1_$2_$3_All-ave.fif --set $c --tmin $4 --tmax $5 --bmin -100 --bmax -0.01 --stc stc/$1_$2_$3_All_c{$c}M_{$tmin}-{$tmax}-spm.stc --smooth 5 --morph fsaverage --spm --subject $1 >>& $log  

        #echo "Making sLORETA maps... " >>& $log
	#mne_make_movie --inv $1_$2_$3_All-ave-7-meg-inv.fif --meas $1_$2_$3_All-ave.fif --set $c --tmin $4 --tmax $5 --bmin -100 --bmax -0.01 --stc stc/$1_$2_$3_All_c{$c}M_{$tmin}-{$tmax}-sLORETA.stc --smooth 5 --morph fsaverage --sLORETA --subject $1 >>& $log     
   #endif 

   foreach run ($runList)
        echo "Making dSPM maps for individual runs... " >>& $log
        echo $run 
	mne_make_movie --inv $1_{$run}-ave-7-meg-inv.fif --meas {$run}-ave.fif --bmin -100 --bmax -0.01 --stc stc/$1_{$run}-spm.stc --smooth 5 --morph fsaverage --spm --subject $1 >>& $log 
   end





