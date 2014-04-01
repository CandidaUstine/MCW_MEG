function preProc_avg_FT(exp, subjID, paradigmName, condNum, condName)

%FieldTrip Script to create the MEG/EEG average within a subject and to compute the
%average of all runs within a subject for a given condition.
%Candida Ustine, custine@mcw.edu 
%March 25th, 2014 
%Usage: preProc_avg_FT('custine', 'cu1', 'Audio', 1, 'STD') 


%% Initialise Fieldtrip Defaults 
ft_defaults

%% Initialise Subject Specific Defaults  
inpath = ['/home/custine/MEG/data/',exp,'/', subjID];
fiff = strcat(inpath,'/ssp/fieldtrip/', subjID,'_',paradigmName,'Run1_clean_comp_raw.fif') %Uses the first run of the experiment to collect header information. 
run1 = strcat(inpath,'/ssp/fieldtrip/', subjID,'_Run1_', int2str(condNum), '_comp.mat')
run2 = strcat(inpath,'/ssp/fieldtrip/', subjID,'_Run2_', int2str(condNum), '_comp.mat')
topoplot_fig = strcat(inpath, '/ave_projon/plots/fieldtrip/Topoplot_Event-', condName,'_Grandavg')
multiplot_fig = strcat(inpath, '/ave_projon/plots/fieldtrip/Multiplot_Event-', condName,'_Grandavg')
avg_file =  strcat(inpath, '/ave_projon/', subjID, '_', condName,'_ft_avg.mat')

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
cfg.vartrllength = 1 % Accept variable length trials
tl_run1 = ft_timelockanalysis(cfg, run1.data_clean)
tl_run2 = ft_timelockanalysis(cfg, run2.data_clean)

%% Compute Within Subject Average across runs 
cfg = []
cfg.keepindividual = 'no'
cfg.channel = meg
cfg.method = 'within'
cfg.parameter = 'avg'
[tl_all] = ft_timelockgrandaverage(cfg, tl_run1, tl_run2)

%% Plot the averages 
cfg = []
cfg.showoutline = 'yes'
cfg.layout = 'neuromag306mag.lay'
cfg.xlim = [0.0 0.5]
cfg.parameter = 'avg'
ft_multiplotER(cfg, tl_all)
%set(gcf, 'Position',[0 0 560 420])
print('-dpdf', multiplot_fig)
figure
ft_topoplotER(cfg, tl_all); colorbar;
print('-dpng', topoplot_fig)

%Plot the runs 
figure;
ft_multiplotER(cfg, tl_run1)

figure;
ft_multiplotER(cfg, tl_run2)
save(avg_file, 'tl_all', 'tl_run1', 'tl_run2', 'cfg', 'meg', 'hdr')
end
