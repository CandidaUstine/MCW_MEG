#!/bin/csh -f

#usage: preProc_avg subjID

if ( $#argv == 0 ) then 
    echo "Hey dummy! Enter a subject! :)"
    exit 1
endif

if ( $#argv == 1 ) then
    set log='./preProc_avg.log'
    echo "Logging to default log..." >>& $log
endif

if ( $#argv == 2) then
    set log=$2
endif

# if log exists, delete
if ( -e $log ) then
    rm $log
endif

foreach proj ('projon') ##Enter projoff here if needed! :) 
        echo "Making Average Parameter files -.ave" >>& $log 
        python /home/custine/MEG/scripts/makeAveFiles.py $1 $proj >>& $log 
  
        echo "Making average fif files..." >>& $log 
        cd /home/custine/MEG/data/msabri/$1/ave_$proj

        ##Left average 
        mne_process_raw \
        --raw ../$1_Left_raw.fif \
        --ave ../ave/$1_Left.ave \
        --$proj --lowpass 20 --highpass 0.5 --filtersize 8192>>& $log

        ##Right average 
        mne_process_raw \
        --raw ../$1_Right_raw.fif \
        --ave ../ave/$1_Right.ave \
        --$proj --lowpass 20 --highpass 0.5 --filtersize 8192>>& $log

        ##LeftDual average 
        mne_process_raw \
        --raw ../$1_LeftDual_raw.fif \
        --ave ../ave/$1_LeftDual.ave \
        --$proj --lowpass 20 --highpass 0.5 --filtersize 8192>>& $log

        ##RightDual average 
        mne_process_raw \
        --raw ../$1_RightDual_raw.fif \
        --ave ../ave/$1_RightDual.ave \
        --$proj --lowpass 20 --highpass 0.5 --filtersize 8192>>& $log

end




