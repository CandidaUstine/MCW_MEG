function sensor_plot_freqAnalysis(subjID, tag, sessID, pow_type, freq, rank)


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

for sessID= sessList

    sessData = strcat('/home/custine/MEG/data/krns_kr3/', subjID, '/', sessID, '/coh/', subjID,'_',sessID,'_' ,rank,tag, '_', freq,'_', pow_type, '_sensor_freqAnalysis.mat');
    sessData = load(sessData{1})
    sessData
    plot_file = strcat('/home/custine/MEG/data/krns_kr3/', subjID, '/', sessID, '/fig/', subjID,'_',sessID,'_', rank,tag, '_', freq, '_grandavg_', pow_type, '_sensor_freqAnalysis.png')
    grandavg_FT = sessData.grandavg_FT;
    grandavg_FT = grandavg_FT';
    size(grandavg_FT)
    megcolorplot(grandavg_FT);
    print(1, plot_file{1}, '-dpng')   
    clf(1)
end



end
