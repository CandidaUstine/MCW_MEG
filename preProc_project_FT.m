function preProc_project_FT(exp, subjID, paradigmName, run, triggerNum)

%Wrapper Script to run the ICA analysis on the Neuromag Raw.fif input file.
%Computes the first 20 ICA componenets of teh specified input and plots the
%components as a time series. After running this script, check the
%Component topoplot figue and identify the artifacts you would like to
%reject. See the fieldtrip website for information on how to identify your
%artifacts. 

%Author: Candida Jane Maria Ustine, custine@mcw.edu
%Created on 03/24/2014 
%Usage: preProc_project_FT('custine', 'cu1', 'Audio', 'Run1')

%% Initialise Fieldtrip Defaults 
ft_defaults

%% Initialise Subject Specific Defaults  
inpath = ['/home/custine/MEG/data/',exp,'/', subjID, '/'];
fiff = strcat(inpath, subjID,'_',paradigmName,run, '_raw.fif')

%% Detect ECG Artifacts 
Fevents = ft_read_event(fiff);
[len, ~] = size(Fevents);
F = [];
endS = []
for i = 1:len
    if Fevents(i).value == triggerNum %%(1 for Standard tone event code value, 2 for DEVIANT tone event code  value)  %enter trigger number/value of the interested event
       F = [F, Fevents(i).sample];
    end
end
disp(F);
F = F';
[len, ~] = size(F);
begS = F(:,1);
begS = begS(1:len-1);
for i = 1:size(begS);
    endS(i) = (begS(i)+ 1000);
end
offset = zeros(1,len-1);
samples = horzcat(begS, endS', offset')

dat = ft_read_data(fiff);
hdr = ft_read_header(fiff);
cfg = []
cfg.artfctdef.ecg.channel = 'ECG'
cfg.artfctdef.ecg.pretim = 0.05
cfg.artfctdef.ecg.psttim = 0.1
cfg.artfctdef.ecg.method = 'zvalue'
cfg.artfctdef.ecg.cutfof = 3
cfg.artfctdef.ecg.inspect = 'E0G062'
cfg.artfctdef.ecg.channel = 'EOG062'
cfg.trl = samples
cfg.trialdef.prestim = -0.1
cfg.trialdef.poststim = 3
cfg.trialdef.eventvalue = 1 % Standard trigger value
cfg.headerfile = fiff
cfg.inputfile = fiff
cfg.trl.dataset = fiff
cfg.dataset = fiff
% cfg.trialdef.poststim = 0.2
cfg = ft_definetrial(cfg)
%samples = samples(1:5, 1:3)
cfg.trl = samples
%[cfg, artifact] = ft_artifact_ecg(cfg)

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%% Reject Artifacts
%cfg = ft_rejectartifact(cfg)

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%% ICA To Remove ECG Artifacts
cfg.trialdef.eventtype = 'deviant'

%remove all jump and muscle artifacts before running your ICA
cfg = ft_artifact_jump(cfg)
[meg] = ft_channelselection('MEGMAG', hdr.label)
cfg.channel = meg
cfg.layout    = 'neuromag306mag.lay'

%You can now preprocess the data:
data = ft_preprocessing(cfg)

% %Reject Visual Trials and see the epoched response: (Optional) 
% data_clean   = ft_rejectvisual(cfg, data);

%you should downsample your data before continuing, otherwise ICA decomposition will take too long
% data_orig = data
% cfg = []
% cfg.resamplefs = 300
% cfg.detrend = 'no'
% data = ft_resampledata(cfg, data)

%% Set the ICA method 
cfg            = [];
cfg.method = 'runica';
%cfg.channel = {'all', '-refchan'};
[meg] = ft_channelselection('MEGMAG', hdr.label)
%[meg] = ft_channelselection('MEGGRAD', hdr.label)
cfg.channel = [meg]
cfg.runica.pca = 101 % number of magnetometers -1
comp           = ft_componentanalysis(cfg, data);

%% Plot the ICA Components 
%Look at the topography of the components. http://fieldtrip.fcdonders.nl/template/layout
cfg = [];
cfg.component = [1:20];       % specify the component(s) that should be plotted
cfg.layout    = 'neuromag306mag.lay'; % specify the layout file that should be used for plotting: mag/planar/all
cfg.comment   = 'no';
[cfg] = ft_topoplotIC(cfg, comp)

%Look at their time courses
cfg = []
cfg.channel = [1:20]
cfg.viewmode = 'component'
cfg.layout = 'neuromag306mag.lay'
ft_databrowser(cfg, comp)

%%decompose the original data as it was prior to downsampling to 150Hz
cfg = [];
cfg.unmixing  = comp.unmixing;
cfg.topolabel = comp.topolabel;
comp_orig     = ft_componentanalysis(cfg, data); %using the sampled data :) 

% the original data can now be reconstructed, excluding those components
cfg = [];
cfg.component = [1 2 3];
data_clean = ft_rejectcomponent(cfg, comp_orig,data); %using the sampled data :) 

%% Sensor Level analysis 
cfg = []
cfg.channel = meg
cfg.vartrllength = 1
tl = ft_timelockanalysis(cfg, data_clean)
cfg = []
cfg.showlabels = 'yes'
cfg.showoutline = 'yes'
cfg.layout = 'neuromag306mag.lay'
cfg.xlim = [0 0.5]
figure
ft_multiplotER(cfg, tl)
% % ft_topoplotER(cfg, tl)
 

%% Rough column 
% cfg = []
% cfg.headerfile = 'cu1_AudioRun1_raw.fif'
% cfg.inputfile = 'cu1_AudioRun1_raw.fif'
% cfg.datafile = 'cu1_AudioRun1_raw.fif'
% cfg.headerformat = 'neuromag_fif'
% cfg.dataformat = 'neuromag_fif'
% [cfg, artifact] = ft_artifact_zvalue(cfg)




end
