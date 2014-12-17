%%stats in Matlab 
%function stats(freq)
%% Hotelling T statistic 
%  http://en.wikipedia.org/wiki/Hotelling's_T-squared_distribution#Hotelling.27s_two-sample_T-squared_statistic
% Left vs Right each with 68 regions, 4 subject groups in each grup.
freq = 'theta'
L1 = dlmread(strcat('/home/custine/MEG/data/epi_conn/EP1/coh/EP1_', freq, '_subj_connectivityMatrix.txt'));
L2 = dlmread(strcat('/home/custine/MEG/data/epi_conn/EP3/coh/EP3_', freq, '_subj_connectivityMatrix.txt'));
L3 = dlmread(strcat('/home/custine/MEG/data/epi_conn/EP5/coh/EP5_', freq, '_subj_connectivityMatrix.txt'));
L4 = dlmread(strcat('/home/custine/MEG/data/epi_conn/EP7/coh/EP7_', freq, '_subj_connectivityMatrix.txt'));
L1 = L1+L1';
L2 = L2+L2';
L3 = L3+L3';
L4 = L4+L4';
L = cat(3, L1, L2, L3, L4);
R1 = dlmread(strcat('/home/custine/MEG/data/epi_conn/EP4/coh/EP4_', freq, '_subj_connectivityMatrix.txt'));
R2 = dlmread(strcat('/home/custine/MEG/data/epi_conn/EP6/coh/EP6_', freq, '_subj_connectivityMatrix.txt'));
R3 = dlmread(strcat('/home/custine/MEG/data/epi_conn/EP8/coh/EP8_', freq, '_subj_connectivityMatrix.txt'));
R4 = dlmread(strcat('/home/custine/MEG/data/epi_conn/EP10/coh/EP10_', freq, '_subj_connectivityMatrix.txt'));
R1 = R1+R1';
R2 = R2+R2';
R3 = R3+R3';
R4 = R4+R4';
R = cat(3, R1, R2, R3, R4);

% whos

% fid = fopen('/home/custine/MEG/results/source_level/ConnectivityPlots/label_names.txt')
% input = textscan(fid, '%s', 'delimiter', '\n')
% jane = input{1,1}
% for i = 1:68 
%     label_names(i) = jane(i,1)
% 
% end
fid = fopen('/home/custine/MEG/results/source_level/ConnectivityPlots/lh_labels.txt')
input = textscan(fid, '%s', 'delimiter', '\n')
jane = input{1,1}
for i = 1:34 
    lh_labels(i) = jane(i,1)

end
fid = fopen('/home/custine/MEG/results/source_level/ConnectivityPlots/rh_labels.txt')
input = textscan(fid, '%s', 'delimiter', '\n')
jane = input{1,1}
for i = 1:34 
    rh_labels(i) = jane(i,1)

end

%% Hotelling T squared stats 
% for i = 1:68
%     x = squeeze(L(i,:,:));
%     MX = mean(x,2);
%     y = squeeze(R(i,:,:));
%     MY = mean(y,2);
%     
%     Wx = (x(:,1)-MX)'*(x(:,1)-MX) + (x(:,2)-MX)'*(x(:,2)-MX) + (x(:,3)-MX)'*(x(:,3)-MX) + (x(:,4)-MX)'*(x(:,4)-MX);
%     Wy = (y(:,1)-MY)'*(y(:,1)-MY) + (y(:,2)-MY)'*(y(:,2)-MY) + (y(:,3)-MY)'*(y(:,3)-MY) + (y(:,4)-MY)'*(y(:,4)-MY);
%     
%     W = (Wx + Wy) * ((4 * 4) / (4 + 4));
%     tsq = ((4*4)/(4+4))*(MX-MY)'*inv(W)*(MX-MY)
%     
%     tsq_temp(i) = tsq;
% end
% for i = 1:68 
%     for j = 1:68 
%         if j==1 
%             tsq_mat(i,j) = tsq_temp(i);
%         else
%             tsq_mat(i,j) = double(0.0);
%         end
%     end
% endylim([0 0.5])
% 
% 
% dlmwrite(strcat('/home/custine/MEG/results/source_level/ConnectivityPlots/Hotel-Tsq_PLV_GrandAvgConnectivityMatrix_', freq , '_Left-Right.txt'), tsq_temp', 'delimiter', ' ')
%%

% %% Equilidean distance 
% 
% for i = 1:68
%     x = squeeze(L(i,:,:));
%     y = squeeze(R(i,:,:));
%     
%     d =  sqrt((mean(x(:,1)) - mean(y(:,1)))*(mean(x(:,1)) - mean(y(:,1))) + (mean(x(:,2)) - mean(y(:,2)))*(mean(x(:,2)) - mean(y(:,2))) + (mean(x(:,3)) - mean(y(:,3)))*(mean(x(:,3)) - mean(y(:,3))) + (mean(x(:,4)) - mean(y(:,4)))*(mean(x(:,4)) - mean(y(:,4))));
%     d_temp(i) = d;
% end
% 
% dlmwrite(strcat('/home/custine/MEG/results/source_level/ConnectivityPlots/textfiles/EqDist_GrandAvgConnectivityMatrix_', freq , '_Left-Right.txt'), d_temp', 'delimiter', ' ')
% plot(d_temp)
% %set(gca,'XTickLabel' label_names)
% 
% figure
% D = d_temp;
% ylim([0 0.5])
% DL = []
% DR = []
% for i = 1:68
%     %L(i)
%     if mod(i,2) == 1
%         DL = [DL, D(i)];
%     else 
%         DR = [DR, D(i)];
%     end
% end
% 
% %plotting
% figure
% subplot(3,1,1)
% ylim([0 0.5])
% plot(D)
% title(strcat(freq, ' - Euclidean Distance LTE vs RTE'))
% subplot(3,1,2)
% plot(DL)
% title('Euclidean Distance LTE vs RTE - Left Hemisphere')
% subplot(3,1,3)
% plot(DR)
% title('Euclidean Distance LTE vs RTE - Right Hemisphere')
% 
% for i = 1:68
%     x = squeeze(L(i,:,:));
%     y = squeeze(R(i,:,:));
%     for j= 1:1000
%         rp = randperm(8);
%         all = cat(2,x,y);
%         subj1 = mean(all(:,rp(1)));
%         subj2 = mean(all(:,rp(2)));
%         subj3 = mean(all(:,rp(3)));
%         subj4 = mean(all(:,rp(4)));
%         subj5 = mean(all(:,rp(5)));
%         subj6 = mean(all(:,rp(6)));
%         subj7 = mean(all(:,rp(7)));
%         subj8 = mean(all(:,rp(8)));
%         dn(i,j) = sqrt(((subj1-subj5)*(subj1-subj5)) + ((subj2-subj6)*(subj2-subj6)) + ((subj3-subj7)*(subj3-subj7)) + ((subj4-subj8)*(subj4-subj8)));
% 
%     end
% end
% dn
% dnsort = sort(dn,2)
% 
% upperdn = dnsort(:,951:1000)

%%
% %% Difference between Hemispheres 
% 
% Li = mean(mean(L,3),2)
% Ri = mean(mean(R,3),2)
% 
% x = 1:68
% % plot(x, Li, x, Ri)
% % title ('LTE vs RTE - all regions')
%  
% 
% Li_LH = []
% Ri_LH = []
% Li_RH = []
% Ri_RH = []
% 
% for i = 1:68
%     %L(i)
%     if mod(i,2) == 1
% %         L(i)
%         Li_LH = [Li_LH, Li(i)]
%         Ri_LH = [Ri_LH, Ri(i)];
%     else 
%         Li_RH = [Li_RH, Li(i)];
%         Ri_RH = [Ri_RH, Ri(i)];
%     end
% end
% 
% 
% Li_LH;
% Ri_LH;
% x = 1:34; 
% LTE_diff = minus(Li_LH, Li_RH); %difference between left and right hemisphere in LTE patients 
% RTE_diff = minus(Ri_LH, Ri_RH);

%% %Plotting
% figure
% subplot(3,1,1)
% ylim([0 0.5])
% plot(x, Li_LH, x, Ri_LH)
% legend('y = LTE LH', 'y = RTE LH', 'location', 'northwest')
% set(gca,'XTick',[1:34]);
% title (strcat(freq, ' - Left Hemiphere Connectivity in LTE and RTE')); 
% hold on
% subplot(3,1,2)
% ylim([0 0.5])
% plot(x, Li_RH, x, Ri_RH)
% set(gca,'XTick',[1:34])
% legend('y = LTE RH', 'y = RTE RH', 'location', 'northwest')
% title (strcat(freq, ' - Right Hemiphere Connectivity in LTE and RTE')) 
% hold on
% subplot(3,1,3)
% ylim([-0.1 0.1])
% plot(x,LTE_diff, x, RTE_diff)
% set(gca,'XTick',[1:34])
% legend('y = LTE Diff', 'y = RTE Diff', 'location', 'northwest')
% title(strcat(freq, ' - Difference (LH-RH) in LTE and RTE pateints')) 
% % % 
% % % 
% % % % %end
% % % 
%% Within Subject Differences 

L1_LH = []
L2_LH = []
L3_LH = []
L4_LH = []

R1_LH = []
R2_LH = []
R3_LH = []
R4_LH = []

L1_RH = []
L2_RH = []
L3_RH = []
L4_RH = []

R1_RH = []
R2_RH = []
R3_RH = []
R4_RH = []


for i = 1:68
    %L(i)
    if mod(i,2) == 1
        L1_LH = [L1_LH, L1(i)]
        L2_LH = [L2_LH, L2(i)]
        L3_LH = [L3_LH, L3(i)]
        L4_LH = [L4_LH, L4(i)] 
        R1_LH = [R1_LH, R1(i)]
        R2_LH = [R2_LH, R2(i)]
        R3_LH = [R3_LH, R3(i)]
        R4_LH = [R4_LH, R4(i)]         
    else
        L1_RH = [L1_RH, L1(i)]
        L2_RH = [L2_RH, L2(i)]
        L3_RH = [L3_RH, L3(i)]
        L4_RH = [L4_RH, L4(i)] 
        R1_RH = [R1_RH, R1(i)]
        R2_RH = [R2_RH, R2(i)]
        R3_RH = [R3_RH, R3(i)]
        R4_RH = [R4_RH, R4(i)]         
    end
end

L1_diff = L1_LH - L1_RH
L2_diff = L2_LH - L2_RH
L3_diff = L3_LH - L3_RH
L4_diff = L4_LH - L4_RH

R1_diff = R1_LH - R1_RH
R2_diff = R2_LH - R2_RH
R3_diff = R3_LH - R3_RH
R4_diff = R4_LH - R4_RH
x = 1:34; 
figure

subplot(4,1,1)
 
ylim([-0.5 0.5])
plot(x, L1_diff)
title(strcat(freq, ' - Within Subject Difference (LH-RH) in LTE patients'))
subplot(4,1,2)
ylim([-0.5 0.5])
plot(x,L2_diff)
subplot(4,1,3)
ylim([-0.5 0.5])
plot(x, L3_diff) 
subplot(4,1,4)
ylim([-0.5 0.5])
plot(x, L4_diff) 

%right Te
figure 
subplot(4,1,1)

ylim([-0.5 0.5])
plot(x, R1_diff)
title(strcat(freq, ' - Within Subject Difference (LH-RH) in RTE patients')) 
subplot(4,1,2)
ylim([-0.5 0.5])
plot(x,R2_diff)
subplot(4,1,3)
ylim([-0.5 0.5])
plot(x, R3_diff) 
subplot(4,1,4)
ylim([-0.5 0.5])
plot(x, R4_diff) 



