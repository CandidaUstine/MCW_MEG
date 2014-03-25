function preProc_avg_FT(exp, subjID, paradigmName, condNum)

%FieldTrip Script to create the MEG/EEG average within a subject and to compute the
%average of all runs within a subject.
%Candida Ustine, custine@mcw.edu 
%March 25th, 2014 


%% Initialise Fieldtrip Defaults 
ft_defaults

%% Initialise Subject Specific Defaults  
inpath = ['/home/custine/MEG/data/',exp,'/', subjID, '/'];
fiff = strcat(inpath, subjID,'_',paradigmName,'Run1_raw.fif') %Uses the first run of the experiment to collect header information. 
run1 = strcat(inpath, subjID,'_Run1_comp.mat')
run2 = strcat(inpath, subjID,'_Run2_comp.mat')

%% Compute Individual Run averages 

%Get Header Label Info 
cfg = []
hdr = ft_read_header(fiff);
hdr = ft_read_header(fiff);
[meg] = ft_channelselection('MEGMAG', hdr.label)

%Load the Individual Runs mat files 
run1 = load(run1)
run2 = load(run2)

%compute the averages 
cfg = []
cfg.channel = meg
cfg.vartrllength = 1
tl_run1 = ft_timelockanalysis(cfg, run1.data)
tl_run2 = ft_timelockanalysis(cfg, run2.data)

%% Compute Within Subject Average across runs 
cfg = []
cfg.keepindividual = 'yes'
cfg.channel = meg
cfg.method = 'within'
cfg.parameter = 'avg'
[tl_all] = ft_timelockgrandaverage(cfg, tl_run1, tl_run2)

%% Plot the averages 
cfg = []
cfg.showoutline = 'yes'
cfg.layout = 'neuromag306mag.lay'
cfg.xlim = [0.0 0.5]
ft_multiplotER(cfg, tl_all)
figure
ft_topoplotER(cfg, tl)

%Plot the runs 
figure;
ft_multiplotER(cfg, tl_run1)
figure;
ft_multiplotER(cfg, tl_run2)


end
