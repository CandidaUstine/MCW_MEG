function sensor_phaseAnalysis(subjID, tag, sessID)

%% Wrapper Script to run sensor level Phase analysis.
%
%%
%Author: Candida Jane Maria Ustine, custine@mcw.edu
%for krns_krs study 2/20/2015
%Usage: sensor_phaseAnalysis('9567', 'Sentence', 's5')

%% Initialise Fieldtrip Defaults
ft_defaults
if strcmp(sessID, 'all')
    sessList = {'s5', 's6', 's7', 's8'}
else
    sessList = {sessID}
end

runList = { 'run1'} %, 'run2', 'run3', 'run4', 'run5', 'run6','run7', 'run8', 'run9', 'run10', 'run11', 'run12'} %
for sessID= sessList
    
    compAll_file = strcat('/home/custine/MEG/data/krns_kr3/', subjID, '/', sessID, '/coh/', subjID,'_',sessID,'_', tag,  '_sensor_phaseAnalysis.mat')
    compAll_file{1}
    save(compAll_file{1}, 'sessID')
    for run=runList
        
        %% Initialise Subject Specific Defaults
        inpath = ['/home/custine/MEG/data/krns_kr3/', subjID, '/', sessID, '/'];
        
        fiff = strcat('/home/custine/MEG/data/krns_kr3/', subjID, '/', sessID, '/ssp/mne/', subjID,'_',sessID,'_',run,'_clean_ecg_raw.fif')
        hdr = ft_read_header(fiff{1});
        comp_file = strcat('/home/custine/MEG/data/krns_kr3/', subjID, '/', sessID, '/coh/', subjID,'_',sessID,'_', run,'_', tag, '_sensor_phaseAnalysis_with_ecg_ssp.mat')
        modeve_file = strcat('/home/custine/MEG/data/krns_kr3/', subjID, '/', sessID, '/eve/triggers/', subjID,'_',sessID,'_', run,'_', tag, '-TriggersMod.eve')
        eve_file = strcat('/home/custine/MEG/data/krns_kr3/', subjID, '/', sessID, '/eve/triggers/', subjID,'_',sessID,'_', run,'_', tag, '-Triggers.eve')
        
        eve_file{1}
        hdr = ft_read_header(fiff{1});
        %Fevents = ft_read_event(modeve_file{1}, 'header', hdr); Use this if reading eve.fif file 
        M = dlmread(eve_file{1})
        Fevents = M(:,3)
        Fsamp = M(:,1)
        endS = M(:,13); %end of sentence (samples ) got from modified (2/23/15) getTriggers.py script sentence script. column 13 is the end of the sentence. 
        sentLen = M(:,14);
        [len, ~] = size(Fevents);
        Fbeg = [];
        Fend = [];
        eventID = [];
        size(Fevents)
        for i = 1:len
            Fevents(i);
            newFsamp = Fsamp(i) - hdr.orig.raw.first_samp;
            newFend = endS(i) - hdr.orig.raw.first_samp;
            Fbeg = [Fbeg, newFsamp];
            Fend = [Fend, newFend];
            eventID = [eventID, Fevents(i)];
         end
%         end
        size(eventID);
        %% Define Trial samples
        Fbeg = Fbeg';
        size(Fbeg)
        [len, ~] = size(Fbeg);

        offset = zeros(1,len);
        size(Fbeg)
        size(offset)
        size(Fend)
        samples = horzcat(Fbeg, Fend', offset')
        
        %% Define Trials
        dat = ft_read_data(fiff{1});
        hdr = ft_read_header(fiff{1});
        cfg = [];
        [meg] = ft_channelselection('MEG', hdr.label);
        [mag] = ft_channelselection('MEGMAG', hdr.label);
        cfg.channel = meg;       
        cfg.trl = samples;
        cfg.headerfile = fiff{1};
        cfg.inputfile = fiff{1};
        cfg.trl.dataset = fiff{1};
        cfg.dataset = fiff{1};
        cfg = ft_definetrial(cfg);
        cfg.trl = samples;
        
        %% Preprocess the data:
        data = ft_preprocessing(cfg)
        data.hdr.orig.projs(1).active = 1
        data.hdr.orig.projs(2).active = 1
         
        %FFT of the Signal 
        [~, len] = size(data.trial); 
        len;
        for i = 1:len 
            new = fft(data.trial{i}', 16384);
            size(new(1:500,:));
            FT(:,:,i) = new(1:500,:);
        end
        FT;
        
        save(comp_file{1}, 'cfg', 'eventID', 'FT', 'sentLen', 'data')
  end
end
end










