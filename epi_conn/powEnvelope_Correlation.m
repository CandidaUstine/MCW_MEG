% freq = 'beta'
% subj = 'EP6'
% P = dlmread(strcat('/home/custine/MEG/data/epi_conn/', subj, '/coh/', subj, '_', freq, '_CRM-noise_powEnv_LabelsMatrix.txt'));
% R = corrcoef(P'); 
% dlmwrite(strcat('/home/custine/MEG/data/epi_conn/', subj, '/coh/', subj, '_',freq, '_CRM-noise_powEnv-Corr_LabelsMatrix.txt'), R, 'delimiter', ' ')


freq = 'beta'
EP1 = dlmread(strcat('/home/custine/MEG/data/epi_conn/EP1/coh/EP1_', freq, '_powEnv-Corr_LabelsMatrix.txt'));
EP3 = dlmread(strcat('/home/custine/MEG/data/epi_conn/EP3/coh/EP3_', freq, '_powEnv-Corr_LabelsMatrix.txt'));
EP5 = dlmread(strcat('/home/custine/MEG/data/epi_conn/EP5/coh/EP5_', freq, '_powEnv-Corr_LabelsMatrix.txt'));
EP7 = dlmread(strcat('/home/custine/MEG/data/epi_conn/EP7/coh/EP7_', freq, '_powEnv-Corr_LabelsMatrix.txt'));

EP4 = dlmread(strcat('/home/custine/MEG/data/epi_conn/EP4/coh/EP4_', freq, '_powEnv-Corr_LabelsMatrix.txt'));
EP6 = dlmread(strcat('/home/custine/MEG/data/epi_conn/EP6/coh/EP6_', freq, '_powEnv-Corr_LabelsMatrix.txt'));
EP8 = dlmread(strcat('/home/custine/MEG/data/epi_conn/EP8/coh/EP8_', freq, '_powEnv-Corr_LabelsMatrix.txt'));
EP10 = dlmread(strcat('/home/custine/MEG/data/epi_conn/EP10/coh/EP10_', freq, '_powEnv-Corr_LabelsMatrix.txt'));

fid = fopen('/home/custine/MEG/results/source_level/ConnectivityPlots/label_names.txt','r')
labels = {};while (1);sss = fgetl(fid);if ~ischar(sss);break;end;labels{end+1} = sss;end
fclose(fid)

EP5c = dlmread(strcat('/home/custine/MEG/data/epi_conn/EP5/coh/EP5_', freq, '_CRM_powEnv-Corr_LabelsMatrix.txt'));
EP6c = dlmread(strcat('/home/custine/MEG/data/epi_conn/EP6/coh/EP6_', freq, '_CRM_powEnv-Corr_LabelsMatrix.txt'));
EP5d = dlmread(strcat('/home/custine/MEG/data/epi_conn/EP5/coh/EP5_', freq, '_DFNAM_powEnv-Corr_LabelsMatrix.txt'));
EP6d = dlmread(strcat('/home/custine/MEG/data/epi_conn/EP6/coh/EP6_', freq, '_DFNAM_powEnv-Corr_LabelsMatrix.txt'));

EP5cn = dlmread(strcat('/home/custine/MEG/data/epi_conn/EP5/coh/EP5_', freq, '_CRM-noise_powEnv-Corr_LabelsMatrix.txt'));
EP6cn = dlmread(strcat('/home/custine/MEG/data/epi_conn/EP6/coh/EP6_', freq, '_CRM-noise_powEnv-Corr_LabelsMatrix.txt'));
EP5dn = dlmread(strcat('/home/custine/MEG/data/epi_conn/EP5/coh/EP5_', freq, '_DFNAM-noise_powEnv-Corr_LabelsMatrix.txt'));
EP6dn = dlmread(strcat('/home/custine/MEG/data/epi_conn/EP6/coh/EP6_', freq, '_DFNAM-noise_powEnv-Corr_LabelsMatrix.txt'));

labels

%% Differences 
% Noise - Resting 
EP5cNdiffR = EP5cn - EP5 
EP5dNdiffR = EP5dn - EP5 
EP6cNdiffR = EP6cn - EP6 
EP6dNdiffR = EP6dn - EP6 

% CRM or DFNAM stimuli - Resting 

EP5cSdiffR = EP5c - EP5 
EP5dSdiffR = EP5d - EP5 
EP6cSdiffR = EP6c - EP6 
EP6dSdiffR = EP6d - EP6 



%%
EL = cat(3, EP1, EP3, EP5, EP7);
ER = cat(3, EP4, EP6, EP8, EP10);

EL = squeeze(mean(EL, 3));
ER = squeeze(mean(ER, 3));
% imagesc(EL)
% caxiscenter
%  set(gca,'xtick',[],'ytick',[])
% for ii=1:68;text(ii,0,labels{ii},'rotation',90);text(0,ii,labels{ii},'horizontalalignment','right');end
% 
% figure
% %% LTE
% imagesc(EL([1:2:68 2:2:68],[1:2:68 2:2:68]))
% caxiscenter
% % title('LTE Mean')
% TitleH = title('LTE MEAN');
% set(TitleH, 'Position', [34 73], ...
%   'VerticalAlignment', 'bottom')
% set(gca,'xtick',[],'ytick',[])
% pos = 0
% for ii=0:2:68;
%     ij = ii+1 
%     pos = pos + 1
%     text(pos,0,labels{ij},'rotation',90); 
%     text(0,pos,labels{ij},'horizontalalignment','right');    
% end
% pos = 34
% for ii=1:2:68;
%     ij = ii+1 
%     pos = pos +1
%     text(pos,0,labels{ij},'rotation',90); 
%     text(0,pos,labels{ij},'horizontalalignment','right');    
% end
% 
% figure
% %% RTE 
% imagesc(ER([1:2:68 2:2:68],[1:2:68 2:2:68]))
% caxiscenter
% set(gca,'xtick',[],'ytick',[])
% TitleH = title('RTE MEAN');
% set(TitleH, 'Position', [34 73], ...
%   'VerticalAlignment', 'bottom')
% 
% pos = 0
% for ii=0:2:68;
%     ij = ii+1 
%     pos = pos + 1
%     text(pos,0,labels{ij},'rotation',90); 
%     text(0,pos,labels{ij},'horizontalalignment','right');    
% end
% pos = 34
% for ii=1:2:68;
%     ij = ii+1 
%     pos = pos +1
%     text(pos,0,labels{ij},'rotation',90); 
%     text(0,pos,labels{ij},'horizontalalignment','right');    
% end
% %% Individual subjects 
% figure
% subplot(2,2,1)
% imagesc(EP1([1:2:68 2:2:68],[1:2:68 2:2:68]))
% caxiscenter
% title('EP1')
% 
% 
% subplot(2,2,2)
% imagesc(EP3([1:2:68 2:2:68],[1:2:68 2:2:68]))
% caxiscenter
% title('EP3')
% 
% subplot(2,2,3) 
% imagesc(EP5([1:2:68 2:2:68],[1:2:68 2:2:68]))
% caxiscenter
% title('EP5')
% 
% subplot(2,2,4) 
% imagesc(EP7([1:2:68 2:2:68],[1:2:68 2:2:68]))
% caxiscenter
% title('EP7')
% 
% figure
% subplot(2,2,1) 
% imagesc(EP4([1:2:68 2:2:68],[1:2:68 2:2:68]))
% caxiscenter
% title('EP4')
% 
% subplot(2,2,2) 
% imagesc(EP6([1:2:68 2:2:68],[1:2:68 2:2:68]))
% caxiscenter
% title('EP6')
% 
% subplot(2,2,3) 
% imagesc(EP8([1:2:68 2:2:68],[1:2:68 2:2:68]))
% caxiscenter
% title('EP8')
% 
% subplot(2,2,4) 
% imagesc(EP10([1:2:68 2:2:68],[1:2:68 2:2:68]))
% caxiscenter
% title('EP10')
% 
 %% Within Subjects - Temporal Regions alone 

%    for j = [8, 9, 16, 17, 30,31, 34, 35, 60, 61, 64, 65, 66, 67
%  [9, 10, 17, 18, 31,32, 35, 36, 61, 62, 65, 66, 67, 68]
EP1_t = []
EP3_t = []
EP5_t = []
EP7_t = []
EP4_t = []
EP6_t = []
EP8_t = []
EP10_t = []

EP1_all = []
EP3_all = []
EP4_all = []
EP7_all = []
EP5_all = []
EP6_all = []
EP8_all = []
EP10_all = []

labels_t = []

for i = [9, 17, 31, 35, 61, 65, 67, 10 18,32, 36, 62, 66, 68]
    %labels_t = [labels_t, labels{i}
    for j = [9, 17, 31, 35, 61, 65, 67, 10 18,32, 36, 62, 66, 68]
%         EP1_t = [EP1_t, EP5cSdiffR(i,j)];
%         EP3_t = [EP3_t, EP5dSdiffR(i,j)];
%         EP5_t = [EP5_t, EP6cSdiffR(i,j)];
%         EP7_t = [EP7_t, EP6dSdiffR(i,j)];

        EP4_t = [EP4_t, EP5(i,j)];
        EP6_t = [EP6_t, EP6(i,j)];
        EP8_t = [EP8_t, EP5c(i,j)];
        EP10_t = [EP10_t, EP6c(i,j)];  
        EP5_t = [EP5_t, EP5d(i,j)];
        EP7_t = [EP7_t, EP6d(i,j)]; 
    end
    EP1_all = cat(1, EP1_all, EP1_t);
    EP1_t = [];
    EP3_all = cat(1, EP3_all, EP3_t);
    EP3_t = []; 
    EP5_all = cat(1, EP5_all, EP5_t);
    EP5_t = [];
    EP7_all = cat(1, EP7_all, EP7_t);
    EP7_t = [];

    EP4_all = cat(1, EP4_all, EP4_t);
    EP4_t = []; 
    EP6_all = cat(1, EP6_all, EP6_t);
    EP6_t = [];
    EP8_all = cat(1, EP8_all, EP8_t);
    EP8_t = [];
    EP10_all = cat(1, EP10_all, EP10_t);
    EP10_t = [];    
    
end


%% Individual subjects 
figure
subplot(2,2,1)
imagesc(EP1_all)
caxiscenter
TitleH = title('EP5 (CRM - Resting)');
set(TitleH, 'Position', [7 18], ...
  'VerticalAlignment', 'bottom')
pos = 0;for ii=[9, 17, 31, 35, 61, 65, 67, 10 18,32, 36, 62, 66, 68];pos = pos+1;text(pos,0,labels{ii},'rotation',90);text(0,pos,labels{ii},'horizontalalignment','right');end

subplot(2,2,2)
imagesc(EP3_all)
caxiscenter
TitleH = title('EP5 (DFNAM - Resting)');
set(TitleH, 'Position', [7 18], ...
  'VerticalAlignment', 'bottom')

subplot(2,2,3) 
imagesc(EP5_all)
caxiscenter
TitleH = title('EP6 (CRM - Resting)')
set(TitleH, 'Position', [7 18], ...
  'VerticalAlignment', 'bottom')

subplot(2,2,4) 
imagesc(EP7_all)
caxiscenter
TitleH = title('EP6 (DFNAM - Resting)')
set(TitleH, 'Position', [7 18], ...
  'VerticalAlignment', 'bottom')

figure
subplot(3,2,1) 
imagesc(EP4_all)
caxiscenter
TitleH = title('EP5 Rest')
set(TitleH, 'Position', [7 18], ...
  'VerticalAlignment', 'bottom')
pos = 0;for ii=[9, 17, 31, 35, 61, 65, 67, 10 18,32, 36, 62, 66, 68];pos = pos+1;text(pos,0,labels{ii},'rotation',90);text(0,pos,labels{ii},'horizontalalignment','right');end

subplot(3,2,2) 
imagesc(EP6_all)
caxiscenter
TitleH = title('EP6 Rest')
set(TitleH, 'Position', [7 18], ...
  'VerticalAlignment', 'bottom')

subplot(3,2,3) 
imagesc(EP8_all)
caxiscenter
TitleH = title('EP5 CRM')
set(TitleH, 'Position', [7 18], ...
  'VerticalAlignment', 'bottom')

subplot(3,2,4) 
imagesc(EP10_all)
caxiscenter
TitleH = title('EP6 CRM')
set(TitleH, 'Position', [7 18], ...
  'VerticalAlignment', 'bottom')

subplot(3,2,5) 
imagesc(EP5_all)
caxiscenter
TitleH = title('EP5 DFNAM')
set(TitleH, 'Position', [7 18], ...
  'VerticalAlignment', 'bottom')

subplot(3,2,6) 
imagesc(EP7_all)
caxiscenter
TitleH = title('EP6 DFNAM')
set(TitleH, 'Position', [7 18], ...
  'VerticalAlignment', 'bottom')



% 
% % % 
% % % % EP1_t = cat(1, EP1(8,:), EP1(9,:), EP1(16,:), EP1(17,:), EP1(30,:), EP1(31, :), EP1(34,:), EP1(35, :), EP1(60, :), EP1(61, :), EP1(64, :), EP1(65, :), EP1(66, :), EP1(67,:));
% % % % EP3_t = cat(1, EP3(8,:), EP3(9,:), EP3(16,:), EP3(17,:), EP3(30,:), EP3(31, :), EP3(34,:), EP3(35, :), EP3(60, :), EP3(61, :), EP3(64, :), EP3(65, :), EP3(66, :), EP3(67,:));
% % % % EP5_t = cat(1, EP5(8,:), EP5(9,:), EP5(16,:), EP5(17,:), EP5(30,:), EP5(31, :), EP5(34,:), EP5(35, :), EP5(60, :), EP5(61, :), EP5(64, :), EP5(65, :), EP5(66, :), EP5(67,:));
% % % % EP7_t = cat(1, EP7(8,:), EP7(9,:), EP7(16,:), EP7(17,:), EP7(30,:), EP7(31, :), EP7(34,:), EP7(35, :), EP7(60, :), EP7(61, :), EP7(64, :), EP7(65, :), EP7(66, :), EP7(67,:));
% % % % 
% % % % EP4_t = cat(1, EP4(8,:), EP4(9,:), EP4(16,:), EP4(17,:), EP4(30,:), EP4(31, :), EP4(34,:), EP4(35, :), EP4(60, :), EP4(61, :), EP4(64, :), EP4(65, :), EP4(66, :), EP4(67,:));
% % % % EP6_t = cat(1, EP6(8,:), EP6(9,:), EP6(16,:), EP6(17,:), EP6(30,:), EP6(31, :), EP6(34,:), EP6(35, :), EP6(60, :), EP6(61, :), EP6(64, :), EP6(65, :), EP6(66, :), EP6(67,:));
% % % % EP8_t = cat(1, EP8(8,:), EP8(9,:), EP8(16,:), EP8(17,:), EP8(30,:), EP8(31, :), EP8(34,:), EP8(35, :), EP8(60, :), EP8(61, :), EP8(64, :), EP8(65, :), EP8(66, :), EP8(67,:));
% % % % EP10_t = cat(1, EP10(8,:), EP10(9,:), EP10(16,:), EP10(17,:), EP10(30,:), EP10(31, :), EP10(34,:), EP10(35, :), EP10(60, :), EP10(61, :), EP10(64, :), EP10(65, :), EP10(66, :), EP10(67,:));
% % % % 
% % % 

















