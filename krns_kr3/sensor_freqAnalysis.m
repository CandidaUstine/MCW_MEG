function sensor_freqAnalysis(subjID, tag, sessID, pow_type, freq, rank)

%% Wrapper Script to run sensor level freq analysis.
% Can computer induced or evoked power - specified by the tag power type -
% 'induced' vs 'evoked' vs 'fft' and for a specified frequency - alpha, beta, gamma,
% theta
%%
%Author: Candida Jane Maria Ustine, custine@mcw.edu
%for krns_krs study 12/29/2014
%Usage: sensor_freqAnalysis('9567', 'Word', 'all', 'fft', 'alpha', '')
%%%for rank use '' or 'first'

%% Initialise Fieldtrip Defaults
ft_defaults
if strcmp(sessID, 'all')
    sessList = {'s5', 's6', 's7', 's8'}
else
    sessList = {sessID}
end

if strcmp(freq, 'alpha')
    foi = 8:1:14
elseif strcmp(freq, 'beta')
    foi = 14:1:25
elseif strcmp(freq, 'gamma')
    foi = 25:1:40
elseif strcmp(freq, 'theta')
    foi = 4:1:8
elseif strcmp(freq, 'allFreq')
    foi = 4:2:40
else
    foi = 14:1:25 %choose beta as default
end

runList = { 'run1', 'run2', 'run3', 'run4', 'run5', 'run6','run7', 'run8', 'run9', 'run10', 'run11', 'run12'} %
for sessID= sessList
    
    compAll_file = strcat('/home/custine/MEG/data/krns_kr3/', subjID, '/', sessID, '/coh/', subjID,'_',sessID,'_',rank, tag, '_', freq,'_', pow_type, '_sensor_freqAnalysis.mat')
    compAll_file{1}
    save(compAll_file{1}, 'sessID')
    for run=runList
        
        %% Initialise Subject Specific Defaults
        inpath = ['/home/custine/MEG/data/krns_kr3/', subjID, '/', sessID, '/'];
        
        fiff = strcat('/home/custine/MEG/data/krns_kr3/', subjID, '/', sessID, '/', subjID,'_',sessID,'_',run,'_raw.fif')
        hdr = ft_read_header(fiff{1});
        comp_file = strcat('/home/custine/MEG/data/krns_kr3/', subjID, '/', sessID, '/coh/', subjID,'_',sessID,'_', run,'_',rank, tag,'_', freq,'_', pow_type, '_sensor_freqAnalysis.mat')
        modeve_file = strcat('/home/custine/MEG/data/krns_kr3/', subjID, '/', sessID, '/eve/triggers/', subjID,'_',sessID,'_', run,'_', tag, '-TriggersMod.eve')
        eve_file = strcat('/home/custine/MEG/data/krns_kr3/', subjID, '/', sessID, '/eve/triggers/', subjID,'_',sessID,'_', run,'_', tag, '-Triggers.eve')
        
        comp_file
        hdr = ft_read_header(fiff{1});
        %Fevents = ft_read_event(modeve_file{1}, 'header', hdr); Use this if reading eve.fif file 
        M = dlmread(eve_file{1})
        Fevents = M(:,3);
        Fsamp = M(:,1);
        [len, ~] = size(Fevents);
        F = [];
        FT = [];
        eventID = [];
%         size(Fevents)
        for i = 1:len
            if strcmp(rank, 'first')
                x = num2str(Fevents(i));
                x =  x(1:1); 
                if strcmp(pow_type, 'fft')
                    if strcmp(x, '1')
                %hdr.orig.raw.first_samp
                %F = [F, Fevents(i).sample];
                        disp 'here'
                        new = Fsamp(i) - hdr.orig.raw.first_samp;
                        new;
                        F = [F, new];
                        eventID = [eventID, Fevents(i)];
                    end
                end
            else
                Fevents(i);
                new = Fsamp(i) - hdr.orig.raw.first_samp;
                new;
                F = [F, new];
                eventID = [eventID, Fevents(i)];
            end
        end
        size(eventID)
        %% Define Trial samples
        F = F';
        size(F)
        [len, ~] = size(F);
        begS = F(:,1);
        
        begS = begS(1:len);
        endS = [];
        for i = 1:size(begS);
            endS(i) = (begS(i)+ 1200); %%1118 samples
        end
        offset = zeros(1,len);
        size(begS)
        size(offset)
        size(endS)
        samples = horzcat(begS, endS', offset');
        
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
        data = ft_preprocessing(cfg); 

        cfg.layout    = 'neuromag306mag.lay';
        cfg.method = 'trial';
        cfg.trials = 'all';
        
        % Power Calculations INDUCED(RAW DATA) VS EVOKED(TL AVG)
        if strcmp(pow_type, 'fft')
%             %Event IDs
%             E = dlmread(eve_file{1});
%             eventID = E(:,3);
            %Frequency Analysis - Matlab 
            [~, len] = size(data.trial);     
            for i = 1:len 
                new = fft(data.trial{i}', 2048);
                FT(:,:,i) = new;
            end
            FT = FT(1:308, :, :);
% %           %Frequency Analysis - Fieldtrip 
%             cfg = []
%             cfg.output = 'fourier';
%             cfg.method = 'mtmfft';
%             %cfg.foilim = [1 40];
%              cfg.foi = foi
% %             cfg.keeptrials = 'yes';
%             cfg.taper = 'hanning';
%             cfg.toi = 0:0.05:.6; %the times on which the analysis windows should be centered (in seconds)
%             cfg.channel = meg
%             TFRmtmfft_fourier_data = ft_freqanalysis(cfg, data);
            save(comp_file{1},'cfg', 'eventID', 'FT' ) %''TFRmtmfft_fourier_data');
            
        elseif strcmp(pow_type, 'induced')
            cfg = [];
            cfg.output = 'pow';
            cfg.method = 'mtmconvol';
            cfg.foi = foi;
            cfg.keeptrials = 'yes';
            cfg.taper = 'hanning';
            cfg.toi = -0.1:0.05:0.6; %the times on which the analysis windows should be centered (in seconds)
            cfg.channel = meg;
            cfg.t_ftimwin    = 4./cfg.foi %length of sliding time window
            TFRconvol_pow_induced = ft_freqanalysis(cfg, data)
            save(comp_file{1},'cfg', 'data', 'TFRconvol_pow_induced')
            
        elseif strcmp(pow_type,'evoked')
            %%Time Lock analysis - compute the averages
            cfg = []
            cfg.channel = meg
            cfg.vartrllength = 1
            tl = ft_timelockanalysis(cfg, data)
            cfg = []
            cfg.baseline = [-0.1 -0.005]
            tl = ft_timelockbaseline(cfg, tl)
            %%Frequency Analysis
            cfg = []
            cfg.output = 'pow'
            cfg.channel = meg
            cfg.method = 'mtmconvol'
            cfg.taper = 'hanning';
            cfg.foi = foi; %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
            cfg.t_ftimwin = 4./cfg.foi;
            cfg.toi = -0.1:0.05:0.6;
            TFRconvol_pow_evoked = ft_freqanalysis(cfg, tl)
            
            save(comp_file{1},'cfg', 'data', 'TFRconvol_pow_evoked')
        end
        
     end
    %% Sensor level average across runs ina  session. - GRAND AVERAGE - POWER SPECTRUM 
    
    disp 'Jane Here'
    plot_file = strcat('/home/custine/MEG/data/krns_kr3/', subjID, '/', sessID, '/fig/', subjID,'_',sessID,'_',rank, tag, '_', freq, '_grandavg_', pow_type, '_sensor_freqAnalysis.png')
    run1 = strcat('/home/custine/MEG/data/krns_kr3/', subjID, '/', sessID, '/coh/', subjID,'_',sessID,'_run1_' ,rank,tag, '_', freq,'_', pow_type, '_sensor_freqAnalysis.mat');
    run2 = strcat('/home/custine/MEG/data/krns_kr3/', subjID, '/', sessID, '/coh/', subjID,'_',sessID,'_run2_',rank,tag, '_', freq,'_', pow_type, '_sensor_freqAnalysis.mat');
    run3 = strcat('/home/custine/MEG/data/krns_kr3/', subjID, '/', sessID, '/coh/', subjID,'_',sessID,'_run3_',rank,tag, '_', freq,'_', pow_type,'_sensor_freqAnalysis.mat');
    run4 = strcat('/home/custine/MEG/data/krns_kr3/', subjID, '/', sessID, '/coh/', subjID,'_',sessID,'_run4_', rank,tag, '_',freq,'_', pow_type,'_sensor_freqAnalysis.mat');
    run5 = strcat('/home/custine/MEG/data/krns_kr3/', subjID, '/', sessID, '/coh/', subjID,'_',sessID,'_run5_', rank,tag, '_',freq,'_', pow_type,'_sensor_freqAnalysis.mat');
    run6 = strcat('/home/custine/MEG/data/krns_kr3/', subjID, '/', sessID, '/coh/', subjID,'_',sessID,'_run6_', rank,tag, '_',freq,'_', pow_type,'_sensor_freqAnalysis.mat');
    run7 = strcat('/home/custine/MEG/data/krns_kr3/', subjID, '/', sessID, '/coh/', subjID,'_',sessID,'_run7_', rank,tag, '_',freq,'_', pow_type,'_sensor_freqAnalysis.mat');
    run8 = strcat('/home/custine/MEG/data/krns_kr3/', subjID, '/', sessID, '/coh/', subjID,'_',sessID,'_run8_',rank,tag, '_', freq,'_', pow_type,'_sensor_freqAnalysis.mat');
    run9 = strcat('/home/custine/MEG/data/krns_kr3/', subjID, '/', sessID, '/coh/', subjID,'_',sessID,'_run9_', rank,tag, '_',freq,'_', pow_type,'_sensor_freqAnalysis.mat');
    run10 = strcat('/home/custine/MEG/data/krns_kr3/', subjID, '/', sessID, '/coh/', subjID,'_',sessID,'_run10_',rank,tag, '_', freq,'_', pow_type,'_sensor_freqAnalysis.mat');
    run11 = strcat('/home/custine/MEG/data/krns_kr3/', subjID, '/', sessID, '/coh/', subjID,'_',sessID,'_run11_',rank, tag, '_',freq,'_', pow_type,'_sensor_freqAnalysis.mat');
    run12 = strcat('/home/custine/MEG/data/krns_kr3/', subjID, '/', sessID, '/coh/', subjID,'_',sessID,'_run12_',rank,tag, '_', freq,'_', pow_type,'_sensor_freqAnalysis.mat');
    
%     [meg] = ft_channelselection('MEG', hdr.label);
    
    if strcmp(pow_type, 'fft') 
        %figure
        run1 = load(run1{1}, 'FT');
        run2 = load(run2{1}, 'FT');
        run3 = load(run3{1}, 'FT');
        run4 = load(run4{1}, 'FT');
        run5 = load(run5{1}, 'FT');
        run6 = load(run6{1}, 'FT');
        run7 = load(run7{1}, 'FT');
        run8 = load(run8{1}, 'FT');
        run9 = load(run9{1}, 'FT');
        run10 = load(run10{1}, 'FT');
        run11 = load(run11{1}, 'FT');
        run12 = load(run12{1}, 'FT');
        meanrun1= mean(run1.FT,3);
        meanrun2= mean(run2.FT,3);
        meanrun3= mean(run3.FT,3);
        meanrun4= mean(run4.FT,3);
        meanrun5= mean(run5.FT,3);
        meanrun6= mean(run6.FT,3);
        meanrun7= mean(run7.FT,3);
        meanrun8= mean(run8.FT,3); 
        meanrun9= mean(run9.FT,3);     
        meanrun10= mean(run10.FT,3);
        meanrun11= mean(run11.FT,3);
        meanrun12= mean(run12.FT,3);  
        meanruns = cat(3, meanrun1, meanrun2, meanrun3, meanrun4, meanrun5, meanrun6, meanrun7, meanrun8, meanrun9, meanrun10, meanrun11, meanrun12);
        grandavg_FT = mean(meanruns,3);  
        reorder = megcolorplot(grandavg_FT');
        %grandavgFT = grandavgFT(1:308,:)
        size(reorder)
        save(compAll_file{1}, 'grandavg_FT', 'meanruns', 'reorder')
        disp 'Results saved in'
        compAll_file{1}       
        
    %%INDUCED POWER
    elseif strcmp(pow_type, 'induced')
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
        [grandavg_induced] = ft_freqgrandaverage(cfg, run1.TFRmtmfft_pow_data, run2.TFRmtmfft_pow_data, run3.TFRmtmfft_pow_data, run4.TFRmtmfft_pow_data, run5.TFRmtmfft_pow_data, run6.TFRmtmfft_pow_data, run7.TFRmtmfft_pow_data, run8.TFRmtmfft_pow_data, run9.TFRmtmfft_pow_data, run10.TFRmtmfft_pow_data, run11.TFRmtmfft_pow_data, run12.TFRmtmfft_pow_data)
        save(compAll_file{1}, 'grandavg_induced')
        
    
    %%EVOKED POWER    
    elseif strcmp(pow_type, 'evoked')
        %%Load individual Freq evoked structures
        run1 = load(run1{1}, 'TFRconvol_pow_evoked');
        run2 = load(run2{1}, 'TFRconvol_pow_evoked');
        run3 = load(run3{1}, 'TFRconvol_pow_evoked');
        run4 = load(run4{1}, 'TFRconvol_pow_evoked');
        run5 = load(run5{1}, 'TFRconvol_pow_evoked');
        run6 = load(run6{1}, 'TFRconvol_pow_evoked');
        run7 = load(run7{1}, 'TFRconvol_pow_evoked');
        run8 = load(run8{1}, 'TFRconvol_pow_evoked');
        run9 = load(run9{1}, 'TFRconvol_pow_evoked');
        run10 = load(run10{1}, 'TFRconvol_pow_evoked');
        run11 = load(run11{1}, 'TFRconvol_pow_evoked');
        run12 = load(run12{1}, 'TFRconvol_pow_evoked');
        
        cfg = [];
        cfg.parameter = 'powspctrm';
        cfg.channel = meg;
        cfg.foilim = 'all'
        [grandavg_evoked] = ft_freqgrandaverage(cfg, run1.TFRconvol_pow_evoked, run2.TFRconvol_pow_evoked, run3.TFRconvol_pow_evoked, run4.TFRconvol_pow_evoked, run5.TFRconvol_pow_evoked, run6.TFRconvol_pow_evoked, run7.TFRconvol_pow_evoked, run8.TFRconvol_pow_evoked, run9.TFRconvol_pow_evoked, run10.TFRconvol_pow_evoked, run11.TFRconvol_pow_evoked, run12.TFRconvol_pow_evoked)
        save(compAll_file{1}, 'grandavg_evoked')
        
        
        cfg = [];
        cfg.parameter = 'powspctrm';
        cfg.layout = 'neuromag306mag.lay';
        cfg.showlabels = 'no';
        cfg.colorbar = 'yes';
        cfg.xlim = [0 0.6]
        %figure
        ft_multiplotTFR(cfg, grandavg_evoked)
        
        orient('portrait')
        print(1, plot_file{1}, '-dpng')       
    end
    clf(1)
 end

end
    