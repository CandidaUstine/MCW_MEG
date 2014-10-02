
function freqAnalysis(subjID, run)

inpath = ['/home/custine/MEG/data/epi_conn/', subjID, '/'];
fiff = strcat(inpath,'run1_raw.fif')
ssp_file = strcat(inpath, 'ssp/fieldtrip/', run, '_2secSamples_comp.mat')
source_file = strcat(inpath, 'sources.mat')
anatomical_file = strcat(inpath, 'anatomicals.mat')
fig_name = strcat(inpath, subjID, '_dics_fq_f10.fig')
%src = strcat('source_dics_', subjID)

load(ssp_file, 'TFRmtmfft_fourier_data')
load(anatomical_file)

hdr = ft_read_header(fiff);
[meg] = ft_channelselection('MEG', hdr.label)

cfg = []
cfg.grad = TFRmtmfft_fourier_data.grad
cfg.vol = vol_T1
cfg.channel = meg
cfg.grid.pos = bnd.pnt
cfg.grid.unit = 'cm'
cfg.normalize = 'yes'
leadfield_fq = ft_prepare_leadfield(cfg)

cfg = []
cfg.method = 'dics'
cfg.grid = leadfield_fq
cfg.vol = vol_T1
cfg.dics.lambda = 0
cfg.dics.projectnoise = 'yes'
cfg.frequency = 10
source_dics_EP1 = ft_sourceanalysis(cfg, TFRmtmfft_fourier_data)

m = source_dics_EP1.avg.pow(:,1);

figure; ft_plot_mesh(bnd, 'vertexcolor', m)
save(source_file, 'leadfield_fq','source_dics_EP1', '-append')

savefig(fig_name)
end
