#!/bin/csh -f
#usage: ./ssp_wrapper.sh subjID sessID type
#eg: ./ssp_wrapper.sh 9579 s5 ecgeog/ecg/eog



if ( $#argv == 0 ) then 
    echo "NO ARGUMENT SPECIFIED: Format - subjID tag paradigm"
    exit 1
endif

echo "Subject ID: " 
echo $1 

set subj_dir = /home/custine/MEG/data/krns_kr3/$1/$2/


echo 'Computing the Projections for the subject'
cd $subj_dir
mkdir ssp/mne/eve -m g+rws
mkdir ssp/mne/proj -m g+rws
pwd
echo $3

# set ngrad = 1
# set nmag = 1
# set neeg = 1 
##Using new set of projectors for ECG(1mag, 1grad, 0eeg-specified in ssp_clean_ecgeogProj.py script) and EOG(1mag 1grad 1eeg).

##Default Parameters
set magrej = 4000
set gradrej = 3000
set eegrej = 500
if $3 == 'ecg' then 
    set lfreq = 40
    set hfreq = .7
    set projtmin = -0.08
    set projtmax = 0.08
    set ngrad = 1
    set nmag = 1
    set neeg = 0
    set e_tmin = -0.2
    set e_tmax = 0.2
    set h_tmin = -0.08
    set h_tmax = 0.08
else if $3 == 'eog' then
    set lfreq = 40
    set hfreq = 0.7 
    set projtmin = -0.2
    set projtmax = 0.2
    set ngrad = 2 
    set nmag = 2
    set neeg = 2 ##2nd ssp vector had no/negative effect so changed back to 1 ##changed back to 3 after modifying HPF 
    set e_tmin = -0.2
    set e_tmax = 0.2
    set h_tmin = -0.08
    set h_tmax = 0.08
else if $3 == 'ecgeog' then
    set lfreq = 40
    set hfreq = 0.7 
    set e_tmin = -0.2
    set e_tmax = 0.2
    set h_tmin = -0.08
    set h_tmax = 0.08
endif 

set runList = (run1 run2 run3 run4 run5 run6 run7 run8 run9 run10 run11 run12) 

foreach run ($runList)
			
	set run = $1_$2_{$run}_raw.fif	
	echo $run
	python  /home/custine/MEG/scripts/krns_kr3/ssp_ecgeogProj.py --in_path $subj_dir -i $run -c "ECG 064" --e_tmin $e_tmin --e_tmax $e_tmax --h_tmin $h_tmin --h_tmax $h_tmax --l-freq $lfreq --h-freq $hfreq --rej-grad $gradrej --rej-mag $magrej --rej-eeg $eegrej --tag $3 -g 1 -m 1 -e 0							   
end

