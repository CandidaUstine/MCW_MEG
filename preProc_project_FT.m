function preProc_project_FT(exp, subjID, paradigmName, run, condNum)

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
comp_file = strcat(inpath, subjID,'_',run, '_comp.mat')

%r = genvarname(run) 

% Detect ECG Artifacts 
Fevents = ft_read_event(fiff);
[len, ~] = size(Fevents);
F = [];
endS = []
for i = 1:len
    if Fevents(i).value == condNum %%(1 for Standard tone event code value, 2 for DEVIANT tone event code  value)  %enter trigger number/value of the interested event
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
cfg.trl = samples
cfg.trialdef.prestim = -0.1
cfg.trialdef.poststim = 3
cfg.trialdef.eventvalue = 1 % Standard trigger value
cfg.headerfile = fiff
cfg.inputfile = fiff
cfg.trl.dataset = fiff
cfg.dataset = fiff
cfg = ft_definetrial(cfg)
cfg.trl = samples

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% % % Reject Artifacts
% % cfg = ft_rejectartifact(cfg)

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% ICA To Remove ECG Artifacts
cfg.trialdef.eventtype = 'deviant'

%remove all jump and muscle artifacts before running your ICA
cfg = ft_artifact_jump(cfg)
[meg] = ft_channelselection('all', hdr.label) %% NOTE: MUST BE ALL CHANNELS FOR THE FT_PREPROCESSING STEP AND THEN WHEN YOU ARE DOING THE ICA YOU CAN JUST COMPUTE ON THE MAGNETOMETERS OR ALL MEG CHANNELS… :) IMPORTANT!!! 
cfg.channel = {'all', '-refchan'};
cfg.channel = meg
cfg.layout    = 'neuromag306mag.lay'

%You can now preprocess the data:
data = ft_preprocessing(cfg)

% %Reject Visual Trials and see the epoched response: (Optional) 
% data_clean   = ft_rejectvisual(cfg, data);

%you should downsample your data before continuing, otherwise ICA decomposition will take too long
data_orig = data
cfg = []
cfg.resamplefs = 300
cfg.detrend = 'no'
data = ft_resampledata(cfg, data)

%% Set the ICA method 
cfg            = [];% the original data can now be reconstructed, excluding those components
cfg.method = 'fastica';
%cfg.channel = {'all', '-refchan'};
[meg] = ft_channelselection('MEG', hdr.label)
%[meg] = ft_channelselection('MEGGRAD', hdr.label)
cfg.channel = [meg]
%cfg.runica.pca = 101 % number of magnetometers -1
comp = ft_componentanalysis(cfg, data);

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
figure
ft_databrowser(cfg, comp)
 
save(comp_file, 'cfg', 'data', 'comp')

% % the original data can now be reconstructed, excluding those components
% cfg = [];
% cfg.component = [1 2 3];
% data_clean = ft_rejectcomponent(cfg, comp_orig,data); %using the sampled data :) 

end
