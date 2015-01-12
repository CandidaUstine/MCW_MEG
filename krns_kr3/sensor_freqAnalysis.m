function sensor_freqAnalysis(subjID, tag, sessID)

%Wrapper Script to run sensor level freq analysis.

%Author: Candida Jane Maria Ustine, custine@mcw.edu
%for krns_krs study 12/29/2014
%Usage: sensor_freqAnalysis('9567', 'Noun_Place', 'all')

%% Initialise Fieldtrip Defaults
ft_defaults
if strcmp(sessID, 'all')
    sessList = {'s5', 's6', 's7', 's8'}
else 
    sessList = {sessID}
end
runList = {'run1', 'run2', 'run3', 'run4', 'run5', 'run6','run7', 'run8', 'run9', 'run10', 'run11', 'run12'}
for sessID= sessList

    compAll_file = strcat('/home/custine/MEG/data/krns_kr3/', subjID, '/', sessID, '/coh/', subjID,'_',sessID,'_sensor_freqAnalysis.mat')
    save(compAll_file{1}, 'sessID')
    for run=runList 
        
        %% Initialise Subject Specific Defaults
        inpath = ['/home/custine/MEG/data/krns_kr3/', subjID, '/', sessID, '/'];
        
        fiff = strcat('/home/custine/MEG/data/krns_kr3/', subjID, '/', sessID, '/', subjID,'_',sessID,'_',run,'_raw.fif')
        comp_file = strcat('/home/custine/MEG/data/krns_kr3/', subjID, '/', sessID, '/coh/', subjID,'_',sessID,'_', run,'_sensor_freqAnalysis.mat')
        
        eve_file = strcat('/home/custine/MEG/data/krns_kr3/', subjID, '/', sessID, '/eve/triggers/', subjID,'_',sessID,'_', run,'_', tag, '-TriggersMod-eve.fif')
        hdr = ft_read_header(fiff{1});
        Fevents = ft_read_event(eve_file{1}, 'header', hdr);
        [len, ~] = size(Fevents);
        F = [];
        endS = []
        begS = []
        for i = 1:len
            F = [F, Fevents(i).sample];
        end
        
        %% Define Trial samples
        F = F';
        [len, ~] = size(F);
        begS = F(:,1);
        begS = begS(1:len-1);
        endS = F(:,1);
        endS = endS(2:len);
        offset = zeros(1, len-1)';
        samples = horzcat(begS, endS, offset)
        
        %% Define Trials
        dat = ft_read_data(fiff{1});
        hdr = ft_read_header(fiff{1});
        cfg = [];
        cfg.trl = samples;
        % cfg.trialdef.prestim = -0.1
        % cfg.trialdef.poststim = 3
        % cfg.trialdef.eventvalue = 1 % Standard trigger value
        cfg.headerfile = fiff{1};
        cfg.inputfile = fiff{1};
        cfg.trl.dataset = fiff{1};
        cfg.dataset = fiff{1};
        cfg = ft_definetrial(cfg);
        cfg.trl = samples;
        
        %% Preprocess the data:
        data = ft_preprocessing(cfg);
        
        %%
        [meg] = ft_channelselection('MEG', hdr.label); %% NOTE: MUST BE ALL CHANNELS FOR THE FT_PREPROCESSING STEP AND THEN WHEN YOU ARE DOING THE ICA YOU CAN JUST COMPUTE ON THE MAGNETOMETERS OR ALL MEG CHANNELS… :) IMPORTANT!!!
        %cfg.channel = {'all', '-refchan'};
        cfg.channel = meg;
        cfg.layout    = 'neuromag306mag.lay';
        cfg.method = 'trial';
        cfg.trials = 'all';
        
        %% Frequency Analysis
        cfg = []
        cfg.output = 'fourier';
        cfg.method = 'mtmfft';
        cfg.foilim = [1 40];
        %cfg.foi = 18
        cfg.keeptrials = 'yes';
        cfg.taper = 'hanning';
        cfg.toi = 0:0.05:2.0; %the times on which the analysis windows should be centered (in seconds)
        cfg.channel = meg
        TFRmtmfft_fourier_data = ft_freqanalysis(cfg, data);
        
        cfg = [];
        cfg.output = 'pow';
        cfg.method = 'mtmconvol';
        cfg.foi = 2:2:40;
        cfg.keeptrials = 'yes';
        cfg.taper = 'hanning';
        cfg.toi = 0:0.05:0.6; %the times on which the analysis windows should be centered (in seconds)
        cfg.channel = meg;
        cfg.t_ftimwin    = ones(length(cfg.foi),1).*0.5; %length of sliding time window = 0.5 sec
        TFRconvol_pow_data = ft_freqanalysis(cfg, data)
        
        save(comp_file{1},'cfg', 'data', 'TFRmtmfft_pow_data', 'TFRmtmfft_fourier_data');

    end
    %% Sensor level average across runs ina  session. 
    disp 'Jane Here' 
    run1 = strcat('/home/custine/MEG/data/krns_kr3/', subjID, '/', sessID, '/coh/', subjID,'_',sessID,'_run1_sensor_freqAnalysis.mat');
    run2 = strcat('/home/custine/MEG/data/krns_kr3/', subjID, '/', sessID, '/coh/', subjID,'_',sessID,'_run2_sensor_freqAnalysis.mat');
    run3 = strcat('/home/custine/MEG/data/krns_kr3/', subjID, '/', sessID, '/coh/', subjID,'_',sessID,'_run3_sensor_freqAnalysis.mat');
    run4 = strcat('/home/custine/MEG/data/krns_kr3/', subjID, '/', sessID, '/coh/', subjID,'_',sessID,'_run4_sensor_freqAnalysis.mat');
    run5 = strcat('/home/custine/MEG/data/krns_kr3/', subjID, '/', sessID, '/coh/', subjID,'_',sessID,'_run5_sensor_freqAnalysis.mat');
    run6 = strcat('/home/custine/MEG/data/krns_kr3/', subjID, '/', sessID, '/coh/', subjID,'_',sessID,'_run6_sensor_freqAnalysis.mat');
    run7 = strcat('/home/custine/MEG/data/krns_kr3/', subjID, '/', sessID, '/coh/', subjID,'_',sessID,'_run7_sensor_freqAnalysis.mat');
    run8 = strcat('/home/custine/MEG/data/krns_kr3/', subjID, '/', sessID, '/coh/', subjID,'_',sessID,'_run8_sensor_freqAnalysis.mat');
    run9 = strcat('/home/custine/MEG/data/krns_kr3/', subjID, '/', sessID, '/coh/', subjID,'_',sessID,'_run9_sensor_freqAnalysis.mat');
    run10 = strcat('/home/custine/MEG/data/krns_kr3/', subjID, '/', sessID, '/coh/', subjID,'_',sessID,'_run10_sensor_freqAnalysis.mat');
    run11 = strcat('/home/custine/MEG/data/krns_kr3/', subjID, '/', sessID, '/coh/', subjID,'_',sessID,'_run11_sensor_freqAnalysis.mat');
    run12 = strcat('/home/custine/MEG/data/krns_kr3/', subjID, '/', sessID, '/coh/', subjID,'_',sessID,'_run12_sensor_freqAnalysis.mat');
    
    [meg] = ft_channelselection('MEG', hdr.label);
    %%Load individual Freq structures 
    run1 = load(run1{1}, 'TFRmtmfft_pow_data'); 
    run2 = load(run2{1}, 'TFRmtmfft_pow_data'); 
    run3 = load(run3{1}, 'TFRmtmfft_pow_data'); 
    run4 = load(run4{1}, 'TFRmtmfft_pow_data'); 
    run5 = load(run5{1}, 'TFRmtmfft_pow_data'); 
    run6 = load(run6{1}, 'TFRmtmfft_pow_data'); 
    run7 = load(run7{1}, 'TFRmtmfft_pow_data'); 
    run8 = load(run8{1}, 'TFRmtmfft_pow_data');
    run9 = load(run9{1}, 'TFRmtmfft_pow_data'); 
    run10 = load(run10{1}, 'TFRmtmfft_pow_data');
    run11 = load(run11{1}, 'TFRmtmfft_pow_data'); 
    run12 = load(run12{1}, 'TFRmtmfft_pow_data');
    
    cfg = [];
    cfg.keepindividual = 'no';
    cfg.parameter = 'powspctrm';
    cfg.channel = meg;
    cfg.foilim = 'all'
    [grandavg] = ft_freqgrandaverage(cfg, run1.TFRmtmfft_pow_data, run2.TFRmtmfft_pow_data, run3.TFRmtmfft_pow_data, run4.TFRmtmfft_pow_data, run5.TFRmtmfft_pow_data, run6.TFRmtmfft_pow_data, run7.TFRmtmfft_pow_data, run8.TFRmtmfft_pow_data, run9.TFRmtmfft_pow_data, run10.TFRmtmfft_pow_data, run11.TFRmtmfft_pow_data, run12.TFRmtmfft_pow_data)
    save(compAll_file{1}, 'grandavg')
end


end
