#!/bin/csh -f

##Created on Wed Apr  2 14:45:27 2014
##author: custine
##For Krns_kr3 study 

##Usage: ./makeSTC.sh subjID sessID par t1 t2 
##Ex: ./makeSTC.sh 9367 s5 Word 300 500
## OR  ./makeSTC.sh 9367 s5 Word    ->(Will consider the entire time window) 


echo "Subject ID: " 
echo $1 
echo "Session ID: " 
echo $2
set subj_dir = /home/custine/MEG/data/krns_kr3/$1/$2
set surf_dir = /mnt/file1/binder/KRNS/anatomies/surfaces
setenv SUBJECTS_DIR $surf_dir
setenv SUBJECT $1
set log = /home/custine/MEG/data/krns_kr3/$1/$2/logs/$1_$2_$3_makeSTC.log

set subjID = $1
set sessID = $2
set par = $3
set tmin = $4
set tmax = $5  

if ($par == 'AllItems') then 
   set condList = ( 1 )
else if ($par == 'Word') then
   set condList = (1) 
else if ($par == 'Noun') then
   set condList = (1) 
else 
   set condList = (1)
endif 

set runList = (run1 run2 run3 run4 run5 run6 run7 run8 run9 run10 run11 run12) 

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
mkdir stc 

foreach c ($condList)
	echo "Preparing the Space time estimates(stc files) for the condition $c" >>& $log

   if ($t == 'full') then
        echo "Making mne maps... " >>& $log
	mne_make_movie --inv $1_$2_$3_All-ave-7-meg-inv.fif --meas $1_$2_$3_run_All-ave.fif --set $c --bmin -500 --bmax -0.01 --stc stc/$1_$2_$3_All_c{$c}M-mne.stc --smooth 5 --subject $1 >>& $log #--morph fsaverage
 
        echo "Making dSPM maps... " >>& $log
	mne_make_movie --inv $1_$2_$3_All-ave-7-meg-inv.fif --meas $1_$2_$3_run_All-ave.fif --set $c --bmin -500 --bmax -0.01 --stc stc/$1_$2_$3_All_c{$c}M-spm.stc --smooth 5 --spm --subject $1 >>& $log  

        echo "Making sLORETA maps... " >>& $log
	mne_make_movie --inv $1_$2_$3_All-ave-7-meg-inv.fif --meas $1_$2_$3_run_All-ave.fif --set $c --bmin -500 --bmax -0.01 --stc stc/$1_$2_$3_All_c{$c}M-sLORETA.stc --smooth 5 --sLORETA --subject $1 >>& $log #--morph fsaverage


   else
        #echo "Making mne maps... " >>& $log
	#mne_make_movie --inv $1_$2_$3_All-ave-7-meg-inv.fif --meas $1_$2_$3_All-ave.fif --set $c --tmin $tmin --tmax $tmax --bmin -100 --bmax -0.01 --stc stc/$1_$2_$3_All_c{$c}M_{$tmin}-{$tmax}-mne.stc --smooth 5 --morph fsaverage --subject $1 >>& $log  
 
        echo "Making dSPM maps... " >>& $log
	mne_make_movie --inv $1_$2_$3_All-ave-7-meg-inv.fif --meas $1_$2_$3_run_All-ave.fif --set $c --tmin $4 --tmax $5 --bmin -500 --bmax -0.01 --stc stc/$1_$2_$3_All_c{$c}M_{$tmin}-{$tmax}-spm.stc --smooth 5 --spm --subject $1 >>& $log  #--morph fsaverage 

        #echo "Making sLORETA maps... " >>& $log
	#mne_make_movie --inv $1_$2_$3_All-ave-7-meg-inv.fif --meas $1_$2_$3_All-ave.fif --set $c --tmin $4 --tmax $5 --bmin -100 --bmax -0.01 --stc stc/$1_$2_$3_All_c{$c}M_{$tmin}-{$tmax}-sLORETA.stc --smooth 5 --morph fsaverage --sLORETA --subject $1 >>& $log     
   endif 

   foreach run ($runList)
        echo "Making dSPM maps for individual runs... " >>& $log
        echo $run 
	mne_make_movie --inv $1_$2_{$run}_$3-ave-7-meg-inv.fif --meas $1_$2_{$run}_$3_run-ave.fif --set $c --bmin -100 --bmax -0.01 --stc stc/$1_$2_{$run}_$3_c{$c}M-spm.stc --smooth 5 --spm --subject $1 >>& $log  #--morph fsaverage
   end

end 



