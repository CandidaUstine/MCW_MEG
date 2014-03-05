function ssp_find_eog_event(exp,subjID, infif)

%%input file
%in_fif_File = infif;
%%EOG Event file
inpath = ['/home/custine/MEG/data/',exp,'/', subjID, '/'];
[~, name, ~] = fileparts(infif);
[name1, remain]= strtok(name, '_');
[name2, ~]=strtok(remain, '_');
eog_eventFileName = [inpath, 'ssp/' name1,'_', name2, '_eog-eve.fif'];
in_fif_File = infif;

%reading eog channels from data files
[fiffsetup] = fiff_setup_read_raw(in_fif_File);
channelNames = fiffsetup.info.ch_names;
ch_EOG = strmatch('EOG',channelNames);
sampRate = fiffsetup.info.sfreq;
start_samp = fiffsetup.first_samp;
end_samp = fiffsetup.last_samp;
[eog] = fiff_read_raw_segment(fiffsetup, start_samp ,end_samp, ch_EOG(1));

% Detecting Blinks
filteog = eegfilt(eog, sampRate,0,10);
EOG_type = 202;
firstSamp = fiffsetup.first_samp;
temp = filteog-mean(filteog);
 
eog_std_dev_value=1; %Change according to the subject(Default 1) (Higher number- detect only distict narrow peaks) 

if sum(temp>(mean(temp)+1*std(temp))) > sum(temp<(mean(temp)+1*std(temp)))   
    eog_events = peakfinder((filteog),eog_std_dev_value*std(filteog),-1);
else
    eog_events = peakfinder((filteog),eog_std_dev_value*std(filteog),1);
end

writeEventFile(eog_eventFileName, firstSamp, eog_events, EOG_type);
disp('EOG event file saved as ')
disp(eog_eventFileName)
end
