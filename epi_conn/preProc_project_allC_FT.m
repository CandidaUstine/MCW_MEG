function preProc_project_allC_FT(subjID, run)

%Wrapper Script to run the ICA analysis on the Neuromag Raw.fif input file.
%Computes the first 20 ICA componenets of the specified input and plots the
%components as a time series. After running this script, check the
%Component topoplot figue and identify the artifacts you would like to
%reject. See the fieldtrip website for information on how to identify your
%artifacts. 

%Author: Candida Jane Maria Ustine, custine@mcw.edu
%Modified for epi_conn on 09/19/2014 
%Usage: preProc_project_allC_FT('EP1')

%% Initialise Fieldtrip Defaults 
ft_defaults

%% Initialise Subject Specific Defaults  
inpath = ['/home/custine/MEG/data/epi_conn/', subjID, '/'];
fiff = strcat(inpath,'run1_raw.fif')% % % % %For the whole time window of the raw file (same as Option 2 below) 
% % % F = F'
% % % [len, ~] = size(F);
% % % begS = F(1,1)
% % % endS = F(len,1)
% % % samples = horzcat(begS, endS, 0)
% % % samples = [1 490000 0]

eve_file = strcat(inpath, 'eve/', run, '.eve')
comp_file = strcat(inpath,'ssp/fieldtrip/', run,'_2secSamples_comp.mat')


Fevents = load(eve_file)
% disp(Fevents)
%Fevents = ft_read_event(fiff)
[len, ~] = size(Fevents);
F = [];
endS = []
% OPTION 1: Keep this (and comment out OPTION 2) IF you are proceeding with Averaging after ICA analysis. 
for i = 1:len-1
       F = [F, Fevents(i,1,1)];
end

% % % % %For the whole time window of the raw file (same as Option 2 below) 
% % % F = F'
% % % [len, ~] = size(F);
% % % begS = F(1,1)
% % % endS = F(len,1)
% % % samples = horzcat(begS, endS, 0)
% % % samples = [1 490000 0]

% new 2 second samples - HCP 
begS = []
temp = 1
begS(1) = 1;
endS(1) = 4001
for i = 2: 59; %%x = number you get when you diving total samples(620999-130500) by 4000 - so for EP1 490000/4000 = 122 , EP3 (617999-75000)/4000 = 135 so 134, EP4 (1066499 - 109500)/4000 = 238 so 237, EP5 227, EP6: 135 so 134, EP7: 138 so 137, EP8: 93 so 92; EP9: 181 so 180; EP10: 137 so 136; EP2: 60 so 59
    begS(i) = (begS(i-1) + 4000 +1);
end
for i = 2:58; %x-1
    endS(i) = begS(i+1)-1;
end
endS(59) = endS(58) + 4000;
offset = zeros(1,59);
size(offset)
samples = horzcat(begS', endS', offset')

%% Define Trials 

dat = ft_read_data(fiff);
hdr = ft_read_header(fiff);
cfg = []
cfg.trl = samples
cfg.headerfile = fiff
cfg.inputfile = fiff
cfg.trl.dataset = fiff
cfg.dataset = fiff
cfg = ft_definetrial(cfg)
cfg.trl = samples

[meg] = ft_channelselection('MEG', hdr.label) %% NOTE: MUST BE ALL CHANNELS FOR THE FT_PREPROCESSING STEP AND THEN WHEN YOU ARE DOING THE ICA YOU CAN JUST COMPUTE ON THE MAGNETOMETERS OR ALL MEG CHANNELS… :) IMPORTANT!!! 
%cfg.channel = {'all', '-refchan'};
cfg.channel = meg
cfg.layout    = 'neuromag306mag.lay'
cfg.method = 'trial'
cfg.trials = 'all'

% %%Filtering Band PAss filter [1.3 to 150 Hz) and Band stop filter(Notch filter) to filter the 60hz out and the low freq artifact at 7Hz
cfg.bpfilter = 'yes'
cfg.bsfilter = 'yes'
cfg.bpfreq = [1.3 100]
cfg.bsfreq = [59 61] %%cfg.bsfreq = [6 9; 59 61]

%% Data Processing 
% You can now preprocess the data:
data = ft_preprocessing(cfg)

% %you should downsample your data before continuing, otherwise ICA decomposition will take too long
data_orig = data
cfg = []
cfg.resamplefs = 600
cfg.detrend = 'no'
data = ft_resampledata(cfg, data)

%% ICA 
% %%%%%%% Set the ICA method 
% cfg            = []; % the original data can now be reconstructed, excluding those components
% cfg.method = 'fastica';
% %cfg.channel = {'all', '-refchan'};
% [meg] = ft_channelselection('MEG', hdr.label)
% %[meg] = ft_channelselection('MEGGRAD', hdr.label)
% cfg.channel = [meg]
% cfg.fastica.maxNumIterations = 20
% %cfg.runica.pca = 101 % number of magnetometers -1
% comp = ft_componentanalysis(cfg, data);

% %%%%%%Plot the ICA Components 
%Look at the topography of the components. http://fieldtrip.fcdonders.nl/template/layout
% cfg = [];
% cfg.component = [1:20];       % specify the component(s) that should be plotted
% cfg.layout    = 'neuromag306all.lay'; % specify the layout file that should be used for plotting: mag/planar/all
% cfg.comment   = 'no';
% [cfg] = ft_topoplotIC(cfg, comp)

% %%%%%%%Look at their time courses
% cfg = []
% cfg.channel = [1:20]
% cfg.viewmode = 'component'
% cfg.layout = 'neuromag306all.lay'
% ft_databrowser(cfg, comp)
% save(comp_file, 'cfg', 'data', 'comp','comp_file')

% %%%%%%Reject the bad componenets 
% % % % the original data can now be reconstructed, excluding those components
% % % load(comp_file)
% cfg = [];
% cfg.component = [5];
% data_clean = ft_rejectcomponent(cfg, comp, data); %using the sampled data :) 
% save(comp_file, 'data_clean', 'comp', 'data')


%% Frequency Analysis 
cfg = []
cfg.output = 'fourier' 
cfg.method = 'mtmfft'
cfg.foilim = [1 40]
cfg.keeptrials = 'yes'
cfg.taper = 'hanning'
cfg.toi = 0:0.05:2.0 %the times on which the analysis windows should be centered (in seconds)
cfg.channel = meg
TFRmtmfft_fourier_data = ft_freqanalysis(cfg, data)

cfg = []
cfg.output = 'pow' 
cfg.method = 'mtmfft'
cfg.foilim = [1 40]
cfg.keeptrials = 'yes'
cfg.taper = 'hanning'
cfg.toi = 0:0.05:2.0 %the times on which the analysis windows should be centered (in seconds)
cfg.channel = meg
TFRmtmfft_pow_data = ft_freqanalysis(cfg, data)

save(comp_file, 'cfg', 'data', 'TFRmtmfft_pow_data', 'TFRmtmfft_fourier_data')

%end


%%

%% Continuous Data - Resting State :) discovered on 9/30/2014 
% http://fieldtrip.fcdonders.nl/faq/how_can_i_do_time-frequency_analysis_on_continuous_data
% 
dat = ft_read_data(fiff);
hdr = ft_read_header(fiff);
cfg = []
cfg.dataset = fiff
cfg.bpfilter = 'yes'
cfg.bsfilter = 'yes'
cfg.bpfreq = [1.3 100]
cfg.bsfreq = [59 61]

data_continuous = ft_preprocessing(cfg)
cfg = []
cfg.length = 2
cfg.overlap = 0
data_segmented = ft_redefinetrial(cfg, data_continuous)

cfg = []
cfg.resamplefs = 600
cfg.detrend = 'no'
data_segmented = ft_resampledata(cfg, data_segmented)

%% TimeLock Analysis 
hdr = ft_read_header(fiff);
[meg] = ft_channelselection('MEG', hdr.label);
cfg = []
cfg.inputfile = 'emptyroom_raw.fif'
cfg.headerfile = 'emptyroom_raw.fif'
cfg.channel = 'MEG'
data_empty = ft_preprocessing(cfg)
cfg = []
cfg.vartrllength = 0
cfg.covariance = 'yes'
cfg.covariancewindow = 'all'
cfg.channel = 'MEG'
tlcov = ft_timelockanalysis(cfg, data_empty)

noise_cov = tlcov.cov;
cfg = []
cfg.vartrllength = 0
cfg.channel = 'MEG'
cfg.keeptrials = 'no'
tl_run1 = ft_timelockanalysis(cfg, data_segmented)
tl_run1.cov = noise_cov

%% Freuency Analysis 
cfg = []
cfg.method = 'mtmfft'
cfg.taper = 'hanning'
cfg.output = 'powandcsd'
cfg.foilim = [1 30]
cfg.keeptrials = 'no'
cfg.channelcmb = {'MEGMAG', 'MEGMAG'}
freq_segmented = ft_freqanalysis(cfg, data_segmented)

cfg = []
cfg.method = 'coh'
cfg.channel = 'MEGMAG'
coh = ft_connectivityanalysis(cfg, freq_segmented)
cfg = []
cfg.parameter = 'cohspctrm'
figure
ft_connectivityplot(cfg, coh)

% % %% What works!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
% % % do the vol_shape part.... in filedtrp 
% % cfg = []
% % cfg.method = 'dics'
% % cfg.frequency    = 18;
% % cfg.vol = vol_al_shape
% % source = ft_sourceanalysis(cfg, TFRmtmfft_fourier_data)
% % source.avg
% % %has only pow. 

%% 
%%% :) sort of... 
%vol_T1 done form the fieldtrip volumerealign part with R a s and then
%marking fiducials... NOTE: DO REALIGNMENT TWICE.... :) TO GET THE 180
%SHIFT.... 

cfg = []
cfg.method = 'interactive'
mri = ft_volumerealign(cfg, mri)
cfg = []
cfg.coordsys = 'neuromag'
mri = ft_determine_coordsys(mri)
y
r
a
s
i
mri = ft_volumerealign(cfg, mri)
cfg = []
cfg.output = {'brain', 'tpm', 'skull', 'scalp'}
seg_T1 = ft_volumesegment(cfg, mri)
cfg = []
cfg.method = 'singleshell'
vol_T1 = ft_prepare_headmodel(cfg, seg_T1)
vol_T1 = ft_convert_units(vol_T1, 'cm')
figure
ft_plot_vol(vol_T1, 'facecolor', 'red'); alpha 0.5
ft_plot_mesh(shape, 'edgecolor', 'none'); camlight
%% REDUCE THE NUMBER OF VERTICES ###### 
cfg=[];cfg.numvertices=1500;
cfg.method = 'singleshell'

%% Then doing the well you know... source analysis 
%%with time lock data
cfg = []
cfg.grid.inside = 1:size(vol_T1.bnd.pnt, 1) % all source points are inside of the brain
cfg.grad = tl_run1.grad  % sensor positions
cfg.channel = meg;  % the used channels
cfg.vol = vol_T1 % volume conduction model
cfg.grid.pos = vol_T1.bnd.pnt % source points
cfg.normalize = 'yes'
%cfg.reducerank = 2
leadfield_tl = ft_prepare_leadfield(cfg)
load('sources.mat', 'tl_run1')
cfg = []
cfg.grid = leadfield_tl
cfg.vol = vol_T1
cfg.keepfilter = 'yes'
cfg.method = 'lcmv'
cfg.lcmv.fixedori = 'yes'
source = ft_sourceanalysis(cfg, tl_run1)
source.avg %HAS AVG POW POS MOM AND ALL THOSE THINGS.... 
% %SEE BELOW:source = 
% 
%        time: [1x1601 double]
%         pos: [3000x3 double]
%      inside: [3000x1 double]
%     outside: [1x0 double]
%      method: 'average'
%         avg: [1x1 struct]
%         cfg: [1x1 struct]
% 
% source.avg
% 
% ans = 
% 
%        ori: {3000x1 cell}
%        pow: [3000x1 double]
%        mom: {3000x1 cell}
%     filter: {3000x1 cell}
%% with freq data
cfg = []
cfg.grid.inside = 1:size(vol_T1.bnd.pnt, 1)
cfg.grad = freq_segmented.grad  % sensor positions
cfg.channel = meg;  % the used channels
cfg.vol = vol_T1
cfg.grid.pos = vol_T1.bnd.pnt % source points
cfg.normalize = 'yes'
leadfield_fq = ft_prepare_leadfield(cfg)
cfg = []
cfg.grid = leadfield_fq
cfg.vol = vol_T1
cfg.keepfilter = 'yes'
cfg.keeptrials = 'no'
cfg.method = 'dics'
cfg.frequency    = 18;
cfg.channel = mag;
cfg.supchan = grad;
source_fq = ft_sourceanalysis(cfg, freq_segmented)
source_fq.avg
%% NETWORK ANALYSIS:
cfg = []
cfg.method = 'betweenness' % see http://fieldtrip.fcdonders.nl/reference/ft_networkanalysis for more methods.... 
cfg.parameter = 'cohspctrm'
stat = ft_networkanalysis(cfg, coh)

end













