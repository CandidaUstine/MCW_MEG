% %% Trial One 
% %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% 
% subjID = '9367'
% sessID = {'s5', 's6'}
% word = textread('/home/custine/MEG/scripts/krns_kr3/word.txt', '%s')
% wordID = textread('/home/custine/MEG/scripts/krns_kr3/wordID.txt', '%d') 
% 
% 
% for sess = sessID
%     sess
% end
% 
% for w = word(1:2)
%     for id = wordID(1:2)
%         w
%         id = num2str(id,'%03d')
% 
%         sess = 's5'
%         inpath = ['/home/custine/MEG/data/krns_kr3/', subjID, '/', sess, '/epochs/'];
%         run1 = strcat(inpath, '/run1/', subjID,'_',sess, '_run1_',id,w,'-epochs.mat')
%         run2 = strcat(inpath, '/run2/',subjID,'_',sess, '_run2_',id,w,'-epochs.mat')
%         run3 = strcat(inpath, '/run3/',subjID,'_',sess, '_run3_',id,w,'-epochs.mat')
%         run4 = strcat(inpath, '/run4/',subjID,'_',sess, '_run4_',id,w,'-epochs.mat')
%         run5 = strcat(inpath, '/run5/',subjID,'_',sess, '_run5_',id,w,'-epochs.mat')
%         run6 = strcat(inpath, '/run6/',subjID,'_',sess, '_run6_',id,w,'-epochs.mat')
%         run7 = strcat(inpath, '/run7/',subjID,'_',sess, '_run7_',id,w,'-epochs.mat')
%         run8 = strcat(inpath, '/run8/',subjID,'_',sess, '_run8_',id,w,'-epochs.mat')
%         run9 = strcat(inpath, '/run9/',subjID,'_',sess, '_run9_',id,w,'-epochs.mat')
%         run10 = strcat(inpath, '/run10/',subjID,'_',sess, '_run10_',id,w,'-epochs.mat')
%         run11 = strcat(inpath, '/run11/',subjID,'_',sess, '_run11_',id,w,'-epochs.mat')
%         run12 = strcat(inpath, '/run12/',subjID,'_',sess, '_run12_',id,w,'-epochs.mat')
% 
% 
%         epochs1 = load(run1{1});
%         epochs2 = load(run2{1});
%         epochs3 = load(run3{1});
%         epochs4 = load(run4{1});
%         epochs5 = load(run5{1});
%         epochs6 = load(run6{1});
%         epochs7 = load(run7{1});
%         epochs8 = load(run8{1});
%         epochs9 = load(run9{1});
%         epochs10 = load(run10{1});
%         epochs11 = load(run11{1});
%         epochs12 = load(run12{1});
% 
%         % 
% 
%         
%         epochsR1 = epochs1.epochs_data;
%         
%         if isempty(epochs2)
%             epochsR2 = struct('epochs_data', {0,0,0})
%         else
%             epochsR2 = epochs2.epochs_data;
%         end
%         epochsR2 = epochs2.epochs_data;
%         epochsR3 = epochs3.epochs_data;
%         epochsR4 = epochs4.epochs_data;
%         epochsR5 = epochs5.epochs_data;
%         epochsR6 = epochs6.epochs_data;
%         epochsR7 = epochs7.epochs_data;
%         epochsR8 = epochs8.epochs_data;
%         epochsR9 = epochs9.epochs_data;
%         epochsR10 = epochs10.epochs_data;
%         epochsR11 = epochs11.epochs_data;
%         epochsR12 = epochs12.epochs_data;
%         
% 
% 
%         epochs = cat(1, epochsR1, epochsR2, epochsR3, epochsR4, epochsR5, epochsR6, epochsR7, epochsR8, epochsR9, epochsR10, epochsR11, epochsR12);
% 
%         newavg = squeeze(mean(epochs,1));
% 
%         evokednew = fiff_read_evoked_all('/home/custine/MEG/data/krns_kr3/9367/s5/ave_projon/9367_s5_AllItems_All-ave.fif')
%         evokednew.info
%         info = evokednew.info; 
%         ev_all = []
%         ev_all.evoked.aspect_kind = 100;
%         ev_all.evoked.is_smsh = 0; 
%         ev_all.evoked.nave = size(epochs,1);
%         ev_all.evoked.first = -200;
%         ev_all.evoked.last = 1200;
%         ev_all.evoked.comment = w;
%         ev_all.evoked.times = linspace(-0.1, 0.6, 1401);
%         ev_all.evoked.epochs = newavg;
%         ev_all.info = info;
% 
%         g_ave_file = strcat(inpath, '/epochs/', subjID,'_',sess, '_',id,w,'-ave.fif')
% 
%         fiff_write_evoked(g_ave_file{1}, ev_all)
%     end
% end
% %% Trial Two 
% %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% word = textread('/home/custine/MEG/scripts/krns_kr3/word.txt', '%s');
% wordID = textread('/home/custine/MEG/scripts/krns_kr3/wordID.txt', '%d')
% subjID = '9511'
% 
% % epochs = ['/home/custine/MEG/data/krns_kr3/9367/9367_sum-epochs.mat']
% % epochs = load(epochs);
% % epochsR = epochs.sumArr; 
% 
% epochsMean = ['/home/custine/MEG/data/krns_kr3/9511/9511_mean-epochs.mat']
% epochsMean = load(epochsMean);
% epochsR = epochsMean.meanArr; 
% 
% epochsLen = ['/home/custine/MEG/data/krns_kr3/9511/9511_20150525_filtered_len-epochs.mat']
% epochsLen = load(epochsLen);
% 
% 
% evokednew = fiff_read_evoked_all('/home/custine/MEG/data/krns_kr3/9511/s5/ave_projon/9511_s5_AllItems_All-ave.fif')
% evokednew.info
% info = evokednew.info; 
% 
% len = (epochsLen.lenArr)'
% 
% for i = 2:258
%     id = i -1
%     w = word(id)
%     ep_len = len(i) 
%     item = double(epochsR(i,:, :));
%     mean = squeeze(item/ep_len);
%     
%     meanArr(id,:,:) = mean;
%     
%     ev_all = []
%     ev_all.evoked.aspect_kind = 100;
%     ev_all.evoked.is_smsh = 0; 
%     ev_all.evoked.nave = ep_len;
%     ev_all.evoked.first = -200;
%     ev_all.evoked.last = 1200;
%     ev_all.evoked.comment = char(w); %'single word';
%     ev_all.evoked.times = linspace(-0.1, 0.6, 1401);
%     ev_all.evoked.epochs = mean;
%     ev_all.info = info;
%     id = num2str(id,'%03d')
%     
%     g_ave_file = strcat('/home/custine/MEG/data/krns_kr3/9511/epochs/', subjID, '_',id,'_', w,'-ave.fif')
%     fiff_write_evoked(g_ave_file{1}, ev_all)
% %     item(1,1,1)
% end

%% Stats with Words (Beta coef and t stats) all 5 ratings together 
epochsMean = ['/home/custine/MEG/data/krns_kr3/9511/9511_20150525_filtered_mean-epochs.mat'] %%Last row is empty for the ones created on Memorial day. so 258=[]
epochsMean = load(epochsMean);
epochsR = epochsMean.meanArr;
epochsR(258,:,:) = []; 

rows2remove = [7 34 39 45 81 85 92 93 97 125 137 153 164 167 210 230 250]
epochsR(rows2remove,:,:) = [];
epochsRsel = epochsR;
save('/home/custine/MEG/data/krns_kr3/9511/9511_20150525_filtered_meanSel-epochs.mat', 'epochsRsel')


mean = load('/home/custine/MEG/data/krns_kr3/9511/9511_20150525_filtered_meanSel-epochs.mat')
designmat = load('/home/custine/MEG/data/krns_kr3/9367/5attributeRatings.mat')
dm = designmat.rat;
% % ratingF = ['/home/custine/MEG/scripts/krns_kr3/Info/ratingsMATRIX_Motion.txt']
% % designmat = textread(ratingF);
% % dm = designmat;
[x, y, z] = pca(dm); %%Creating the regressions analysis using the PCA components. 
dm = y;

epochsRsel = mean.epochsRsel;
% [B, E, df] = fmrianalysis_regression(epochsRsel,dm);
[B, E, df] = fmrianalysis_regression(epochsRsel,[dm ones(240,1)],[eye(5) zeros(5,1)]);

A = reshape(B, 5, 325, 1401);

A1 = squeeze(A(1, :, :));
A2 = squeeze(A(2, :, :));
A3 = squeeze(A(3, :, :));
A4 = squeeze(A(4, :, :));
A5 = squeeze(A(5, :, :));

evokednew = fiff_read_evoked_all('/home/custine/MEG/data/krns_kr3/9511/s5/ave_projon/9511_s5_Verb_All-ave.fif')
evokednew.info;
info = evokednew.info; 
%Colour
ev_all = []
ev_all.evoked.aspect_kind = 100;
ev_all.evoked.is_smsh = 0; 
ev_all.evoked.nave = 1;
ev_all.evoked.first = -200;
ev_all.evoked.last = 1200;
ev_all.evoked.comment = 'Beta coef'; %'single word';
ev_all.evoked.times = linspace(-0.1, 0.6, 1401);
ev_all.evoked.epochs = A1; %%Do for A2, A3, A4 A5 etc... 
ev_all.info = info;
g_ave_file = strcat('/home/custine/MEG/data/krns_kr3/9511/BetaRegression/beta_regression_1Colour_20150525-ave.fif')
fiff_write_evoked(g_ave_file, ev_all)

%Motion 
ev_all = []
ev_all.evoked.aspect_kind = 100;
ev_all.evoked.is_smsh = 0; 
ev_all.evoked.nave = 1;
ev_all.evoked.first = -200;
ev_all.evoked.last = 1200;
ev_all.evoked.comment = 'Beta coef'; %'single word';
ev_all.evoked.times = linspace(-0.1, 0.6, 1401);
ev_all.evoked.epochs = A2; %%Do for A2, A3, A4 A5 etc... 
ev_all.info = info;
g_ave_file = strcat('/home/custine/MEG/data/krns_kr3/9511/BetaRegression/beta_regression_2Motion_20150525-ave.fif')
fiff_write_evoked(g_ave_file, ev_all)

%Shape 
ev_all = []
ev_all.evoked.aspect_kind = 100;
ev_all.evoked.is_smsh = 0; 
ev_all.evoked.nave = 1;
ev_all.evoked.first = -200;
ev_all.evoked.last = 1200;
ev_all.evoked.comment = 'Beta coef'; %'single word';
ev_all.evoked.times = linspace(-0.1, 0.6, 1401);
ev_all.evoked.epochs = A3; %%Do for A2, A3, A4 A5 etc... 
ev_all.info = info;
g_ave_file = strcat('/home/custine/MEG/data/krns_kr3/9511/BetaRegression/beta_regression_3Shape_20150525-ave.fif')
fiff_write_evoked(g_ave_file, ev_all)

%Sound 
ev_all = []
ev_all.evoked.aspect_kind = 100;
ev_all.evoked.is_smsh = 0; 
ev_all.evoked.nave = 1;
ev_all.evoked.first = -200;
ev_all.evoked.last = 1200;
ev_all.evoked.comment = 'Beta coef'; %'single word';
ev_all.evoked.times = linspace(-0.1, 0.6, 1401);
ev_all.evoked.epochs = A4; %%Do for A2, A3, A4 A5 etc... 
ev_all.info = info;
g_ave_file = strcat('/home/custine/MEG/data/krns_kr3/9511/BetaRegression/beta_regression_4Sound_20150525-ave.fif')
fiff_write_evoked(g_ave_file, ev_all)

%Upper Limb 
ev_all = []
ev_all.evoked.aspect_kind = 100;
ev_all.evoked.is_smsh = 0; 
ev_all.evoked.nave = 1;
ev_all.evoked.first = -200;
ev_all.evoked.last = 1200;
ev_all.evoked.comment = 'Beta coef'; %'single word';
ev_all.evoked.times = linspace(-0.1, 0.6, 1401);
ev_all.evoked.epochs = A5; %%Do for A2, A3, A4 A5 etc... 
ev_all.info = info;
g_ave_file = strcat('/home/custine/MEG/data/krns_kr3/9511/BetaRegression/beta_regression_5UpperLimb_20150525-ave.fif')
fiff_write_evoked(g_ave_file, ev_all)

%%
t = B./sqrt(E);
t(find(isnan(t))) = zeros;
t(find(isinf(t))) = zeros;
A = reshape(t, 5, 325, 1401);
A1 = squeeze(A(1, :, :));
A2 = squeeze(A(2, :, :));
A3 = squeeze(A(3, :, :));
A4 = squeeze(A(4, :, :));
A5 = squeeze(A(5, :, :));
for ii=1:5;subplot(2,3,ii);imagesc(-100:2:600,1:3:306,squeeze(A(ii,1:3:306,:)));caxis([-3 3]);end


evokednew = fiff_read_evoked_all('/home/custine/MEG/data/krns_kr3/9511/s5/ave_projon/9511_s5_Verb_All-ave.fif')
evokednew.info;
info = evokednew.info; 
%Colour
ev_all = []
ev_all.evoked.aspect_kind = 100;
ev_all.evoked.is_smsh = 0; 
ev_all.evoked.nave = 1;
ev_all.evoked.first = -200;
ev_all.evoked.last = 1200;
ev_all.evoked.comment = 't'; %'single word';
ev_all.evoked.times = linspace(-0.1, 0.6, 1401);
ev_all.evoked.epochs = A1; %%Do for A2, A3, A4 A5 etc... 
ev_all.info = info;
g_ave_file = strcat('/home/custine/MEG/data/krns_kr3/9511/BetaRegression/t_1Colour_20150525-ave.fif')
fiff_write_evoked(g_ave_file, ev_all)

%Motion 
ev_all = []
ev_all.evoked.aspect_kind = 100;
ev_all.evoked.is_smsh = 0; 
ev_all.evoked.nave = 1;
ev_all.evoked.first = -200;
ev_all.evoked.last = 1200;
ev_all.evoked.comment = 't'; %'single word';
ev_all.evoked.times = linspace(-0.1, 0.6, 1401);
ev_all.evoked.epochs = A2; %%Do for A2, A3, A4 A5 etc... 
ev_all.info = info;
g_ave_file = strcat('/home/custine/MEG/data/krns_kr3/9511/BetaRegression/t_2Motion_20150525-ave.fif')
fiff_write_evoked(g_ave_file, ev_all)

%Shape 
ev_all = []
ev_all.evoked.aspect_kind = 100;
ev_all.evoked.is_smsh = 0; 
ev_all.evoked.nave = 1;
ev_all.evoked.first = -200;
ev_all.evoked.last = 1200;
ev_all.evoked.comment = 't'; %'single word';
ev_all.evoked.times = linspace(-0.1, 0.6, 1401);
ev_all.evoked.epochs = A3; %%Do for A2, A3, A4 A5 etc... 
ev_all.info = info;
g_ave_file = strcat('/home/custine/MEG/data/krns_kr3/9511/BetaRegression/t_3Shape_20150525-ave.fif')
fiff_write_evoked(g_ave_file, ev_all)

%Sound 
ev_all = []
ev_all.evoked.aspect_kind = 100;
ev_all.evoked.is_smsh = 0; 
ev_all.evoked.nave = 1;
ev_all.evoked.first = -200;
ev_all.evoked.last = 1200;
ev_all.evoked.comment = 't'; %'single word';
ev_all.evoked.times = linspace(-0.1, 0.6, 1401);
ev_all.evoked.epochs = A4; %%Do for A2, A3, A4 A5 etc... 
ev_all.info = info;
g_ave_file = strcat('/home/custine/MEG/data/krns_kr3/9511/BetaRegression/t_4Sound_20150525-ave.fif')
fiff_write_evoked(g_ave_file, ev_all)

%Upper Limb 
ev_all = []
ev_all.evoked.aspect_kind = 100;
ev_all.evoked.is_smsh = 0; 
ev_all.evoked.nave = 1;
ev_all.evoked.first = -200;
ev_all.evoked.last = 1200;
ev_all.evoked.comment = 't'; %'single word';
ev_all.evoked.times = linspace(-0.1, 0.6, 1401);
ev_all.evoked.epochs = A5; %%Do for A2, A3, A4 A5 etc... 
ev_all.info = info;
g_ave_file = strcat('/home/custine/MEG/data/krns_kr3/9511/BetaRegression/t_5UpperLimb_20150525-ave.fif')
fiff_write_evoked(g_ave_file, ev_all)

%%
%%
%% Stats with Words (Beta coef and t stats) Independent ratings  
epochsMean = ['/home/custine/MEG/data/krns_kr3/9511/9511_20150525_filtered_mean-epochs.mat'] %%Last row is empty for the ones created on Memorial day. so 258=[]
epochsMean = load(epochsMean);
epochsR = epochsMean.meanArr;
epochsR(258,:,:) = []; 

rows2remove = [7 34 39 45 81 85 92 93 97 125 137 153 164 167 210 230 250]
epochsR(rows2remove,:,:) = [];
epochsRsel = epochsR;
save('/home/custine/MEG/data/krns_kr3/9511/9511_20150525_filtered_meanSel-epochs.mat', 'epochsRsel')

%Colour
mean = load('/home/custine/MEG/data/krns_kr3/9511/9511_20150525_filtered_meanSel-epochs.mat')
% ratingF = ['/home/custine/MEG/scripts/krns_kr3/Info/ratingsMATRIX_Colour.txt']
% designmat = textread(ratingF);
% dm = designmat;

%WordLength
wordlen = ['/home/custine/MEG/scripts/krns_kr3/Info/WordLength_ExclPreposition&2Used.txt']
wordlen = textread(wordlen);
dm = wordlen

epochsRsel = mean.epochsRsel;
% [B, E, df] = fmrianalysis_regression(epochsRsel,dm);
[B, E, df] = fmrianalysis_regression(epochsRsel,[dm ones(240,1)],[eye(1) zeros(1,1)]);
t = B./sqrt(E);
t(find(isinf(t))) = zeros;
t(find(isnan(t))) = zeros;
A = reshape(t, 1, 325, 1401);
imagesc(-100:2:600, 1:3:306, squeeze(A(1,1:3:306,:)));caxis([-3 3]);
print('/home/custine/MEG/data/krns_kr3/9511/BetaRegression/9511_t_1Colour.png', '-dpng')

%Motion
mean = load('/home/custine/MEG/data/krns_kr3/9511/9511_20150525_filtered_meanSel-epochs.mat')
ratingF = ['/home/custine/MEG/scripts/krns_kr3/Info/ratingsMATRIX_Motion.txt']
designmat = textread(ratingF);
dm = designmat;
epochsRsel = mean.epochsRsel;
% [B, E, df] = fmrianalysis_regression(epochsRsel,dm);
[B, E, df] = fmrianalysis_regression(epochsRsel,[dm ones(240,1)],[eye(1) zeros(1,1)]);
t = B./sqrt(E);
t(find(isinf(t))) = zeros;
t(find(isnan(t))) = zeros;
A = reshape(t, 1, 325, 1401);
imagesc(-100:2:600, 1:3:306, squeeze(A(1,1:3:306,:)));caxis([-3 3]);
print('/home/custine/MEG/data/krns_kr3/9511/BetaRegression/9511_t_2Motion.png', '-dpng')

%Shape
mean = load('/home/custine/MEG/data/krns_kr3/9511/9511_20150525_filtered_meanSel-epochs.mat')
ratingF = ['/home/custine/MEG/scripts/krns_kr3/Info/ratingsMATRIX_Shape.txt']
designmat = textread(ratingF);
dm = designmat;
epochsRsel = mean.epochsRsel;
% [B, E, df] = fmrianalysis_regression(epochsRsel,dm);
[B, E, df] = fmrianalysis_regression(epochsRsel,[dm ones(240,1)],[eye(1) zeros(1,1)]);
t = B./sqrt(E);
t(find(isinf(t))) = zeros;
t(find(isnan(t))) = zeros;
A = reshape(t, 1, 325, 1401);
imagesc(-100:2:600, 1:3:306, squeeze(A(1,1:3:306,:)));caxis([-3 3]);
print('/home/custine/MEG/data/krns_kr3/9511/BetaRegression/9511_t_3Shape.png', '-dpng')

%Sound
mean = load('/home/custine/MEG/data/krns_kr3/9511/9511_20150525_filtered_meanSel-epochs.mat')
ratingF = ['/home/custine/MEG/scripts/krns_kr3/Info/ratingsMATRIX_Sound.txt']
designmat = textread(ratingF);
dm = designmat;
epochsRsel = mean.epochsRsel;
% [B, E, df] = fmrianalysis_regression(epochsRsel,dm);
[B, E, df] = fmrianalysis_regression(epochsRsel,[dm ones(240,1)],[eye(1) zeros(1,1)]);
t = B./sqrt(E);
t(find(isinf(t))) = zeros;
t(find(isnan(t))) = zeros;
A = reshape(t, 1, 325, 1401);
imagesc(-100:2:600, 1:3:306, squeeze(A(1,1:3:306,:)));caxis([-3 3]);
print('/home/custine/MEG/data/krns_kr3/9511/BetaRegression/9511_t_4Sound.png', '-dpng')

%UpperLimb
mean = load('/home/custine/MEG/data/krns_kr3/9511/9511_20150525_filtered_meanSel-epochs.mat')
ratingF = ['/home/custine/MEG/scripts/krns_kr3/Info/ratingsMATRIX_UpperLimb.txt']
designmat = textread(ratingF);
dm = designmat;
epochsRsel = mean.epochsRsel;
% [B, E, df] = fmrianalysis_regression(epochsRsel,dm);
[B, E, df] = fmrianalysis_regression(epochsRsel,[dm ones(240,1)],[eye(1) zeros(1,1)]);
t = B./sqrt(E);
t(find(isinf(t))) = zeros;
t(find(isnan(t))) = zeros;
A = reshape(t, 1, 325, 1401);
imagesc(-100:2:600, 1:3:306, squeeze(A(1,1:3:306,:)));caxis([-3 3]);
print('/home/custine/MEG/data/krns_kr3/9511/BetaRegression/9511_t_5UpperLimb.png', '-dpng')



