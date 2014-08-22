function preProc_avg_FT(subjID, sessID, runNum)

%FieldTrip Script to create the MEG/EEG average within a subject and to compute the
%average of all runs within a subject for a given condition.
%Candida Ustine, custine@mcw.edu 
%March 25th, 2014 
%Modified for krns_kr3 study on 08/14/2014 
%Usage: preProc_avg_FT('9444', 's1', 'run1')


%% Initialise Fieldtrip Defaults 
ft_defaults

%% Initialise Subject Specific Defaults  
inpath = ['/home/custine/MEG/data/krns_kr3/', subjID, '/', sessID];
fiff = strcat(inpath, '/', subjID,'_',sessID, '_', runNum, '_raw.fif') %Uses the first run of the experiment to collect header information. 
run1 = strcat(inpath,'/ssp/fieldtrip/',  subjID,'_',sessID, '_', runNum, '_allC_comp.mat')
%run2 = strcat(inpath,'/ssp/fieldtrip/', subjID,'_Run2_', int2str(condNum), '_comp.mat')
topoplot_fig = strcat(inpath, '/ave_projon/plots/fieldtrip/Topoplot_', subjID, '_',sessID, '_', runNum, '_clean-ave')
multiplot_fig = strcat(inpath, '/ave_projon/plots/fieldtrip/Multiplot_', subjID, '_',sessID, '_', runNum, '_clean-ave')
avg_file =  strcat(inpath, '/ave_projon/', subjID,'_',sessID, '_', runNum, '_clean_ft_avg.mat')

%% Compute Individual Run averages 

%Get Header Label Info 
cfg = []
hdr = ft_read_header(fiff);
hdr = ft_read_header(fiff);
[meg] = ft_channelselection('MEGMAG', hdr.label)

%Load the Individual Runs mat files 
run1 = load(run1)
%run2 = load(run2)

%compute the averages 
cfg = [] 
cfg.channel = meg
cfg.vartrllength = 1 % Accept variable length trials
tl_run1 = ft_timelockanalysis(cfg, run1.data_clean)
%tl_run2 = ft_timelockanalysis(cfg, run2.data_clean)

% %% Compute Within Subject Average across runs 
% cfg = []
% cfg.keepindividual = 'no'
% cfg.channel = meg
% cfg.method = 'within'
% cfg.parameter = 'avg'
% [tl_all] = ft_timelockgrandaverage(cfg, tl_run1, tl_run2)

%% Plot the averages 
cfg = []
cfg.showoutline = 'yes'
cfg.layout = 'neuromag306mag.lay'
cfg.xlim = [0.0 1]
cfg.parameter = 'avg'
ft_multiplotER(cfg, tl_run1) %%modify to be tl_run1 or tl_all
%set(gcf, 'Position',[0 0 560 420])
print('-dpng', multiplot_fig)
figure
ft_topoplotER(cfg, tl_run1); colorbar; %%modify to be tl_run1 or tl_all
print('-dpng', topoplot_fig)

% % %Plot the runs 
% % figure;
% % ft_multiplotER(cfg, tl_run1)
% % 
% % figure;
% % ft_multiplotER(cfg, tl_run2)
% % save(avg_file, 'tl_all', 'tl_run1', 'tl_run2', 'cfg', 'meg', 'hdr')
save(avg_file, 'tl_run1','cfg', 'meg', 'hdr')
end
