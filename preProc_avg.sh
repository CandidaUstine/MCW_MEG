#!/bin/csh -f

#usage: preProc_avg exp subjID par log-optional

if ( $#argv == 0 ) then 
    echo "Hey dummy! Enter a subject! :)"
    exit 1
endif

#if log exists, delete
if ( -e /home/custine/MEG/data/{$1}/{$2}/ave_projon/logs/preProc_avg.log ) then
    rm /home/custine/MEG/data/{$1}/{$2}/ave_projon/logs/preProc_avg.log
endif

if ( $#argv == 3 ) then
    #set log = '/home/custine/MEG/data/{$1}/{$2}/ave_projon/logs/preProc_avg.log'
    touch /home/custine/MEG/data/{$1}/{$2}/ave_projon/logs/preProc_avg.log
    echo "Logging to default log..." >>& /home/custine/MEG/data/{$1}/{$2}/ave_projon/logs/preProc_avg.log
endif

if ( $#argv == 4) then
    set log=$4
endif

echo $3
foreach proj ('projon') ##Enter projoff here if needed! :) 
        echo $3

        echo "Making Average Parameter files -.ave" >>& /home/custine/MEG/data/{$1}/{$2}/ave_projon/logs/preProc_avg.log
        python /home/custine/MEG/scripts/makeAveFiles.py $2 $proj >>& /home/custine/MEG/data/{$1}/{$2}/ave_projon/logs/preProc_avg.log 
  
        echo "Making average fif files..." >>& /home/custine/MEG/data/{$1}/{$2}/ave_projon/logs/preProc_avg.log 
        cd /home/custine/MEG/data/$1/$2/ave_$proj

        ##compute mne average 
        mne_process_raw \
        --raw ../$2_$3_raw.fif \
        --ave ../ave/$2_$3.ave \
        --$proj --lowpass 20 --highpass 0.7 --filtersize 8192 >>& /home/custine/MEG/data/{$1}/{$2}/ave_projon/logs/preProc_avg.log
end




