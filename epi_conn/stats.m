%%stats in Matlab 
function stats(freq)
%% Hotelling T statistic 
%  http://en.wikipedia.org/wiki/Hotelling's_T-squared_distribution#Hotelling.27s_two-sample_T-squared_statistic
% Left vs Right each with 68 regions, 4 subject groups in each grup.

L1 = dlmread(strcat('/home/custine/MEG/data/epi_conn/EP1/coh/EP1_', freq, '_subj_plv_ConnectivityMatrix.txt'));
L2 = dlmread(strcat('/home/custine/MEG/data/epi_conn/EP3/coh/EP3_', freq, '_subj_plv_ConnectivityMatrix.txt'));
L3 = dlmread(strcat('/home/custine/MEG/data/epi_conn/EP5/coh/EP5_', freq, '_subj_plv_ConnectivityMatrix.txt'));
L4 = dlmread(strcat('/home/custine/MEG/data/epi_conn/EP7/coh/EP7_', freq, '_subj_plv_ConnectivityMatrix.txt'));
L = cat(3, L1, L2, L3, L4);


R1 = dlmread(strcat('/home/custine/MEG/data/epi_conn/EP4/coh/EP4_', freq, '_subj_plv_ConnectivityMatrix.txt'));
R2 = dlmread(strcat('/home/custine/MEG/data/epi_conn/EP6/coh/EP6_', freq, '_subj_plv_ConnectivityMatrix.txt'));
R3 = dlmread(strcat('/home/custine/MEG/data/epi_conn/EP8/coh/EP8_', freq, '_subj_plv_ConnectivityMatrix.txt'));
R4 = dlmread(strcat('/home/custine/MEG/data/epi_conn/EP10/coh/EP10_', freq, '_subj_plv_ConnectivityMatrix.txt'));
R = cat(3, R1, R2, R3, R4); 
% whos
%label_names = csvread(strcat('/home/custine/MEG/results/source_level/ConnectivityPlots/label_names.csv'))

for i = 1:68
    x = squeeze(L(i,:,:));
    MX = mean(x,2);
    y = squeeze(R(i,:,:));
    MY = mean(y,2);
    
    Wx = (x(:,1)-MX)'*(x(:,1)-MX) + (x(:,2)-MX)'*(x(:,2)-MX) + (x(:,3)-MX)'*(x(:,3)-MX) + (x(:,4)-MX)'*(x(:,4)-MX);
    Wy = (y(:,1)-MY)'*(y(:,1)-MY) + (y(:,2)-MY)'*(y(:,2)-MY) + (y(:,3)-MY)'*(y(:,3)-MY) + (y(:,4)-MY)'*(y(:,4)-MY);
    
    W = (Wx + Wy) * ((4 * 4) / (4 + 4));
    tsq = ((4*4)/(4+4))*(MX-MY)'*inv(W)*(MX-MY)
    
    tsq_temp(i) = tsq;
end
for i = 1:68 
    for j = 1:68 
        if j==1 
            tsq_mat(i,j) = tsq_temp(i);
        else
            tsq_mat(i,j) = double(0.0);
        end
    end
end


dlmwrite(strcat('/home/custine/MEG/results/source_level/ConnectivityPlots/Hotel-Tsq_PLV_GrandAvgConnectivityMatrix_', freq , '_Left-Right.txt'), tsq_temp', 'delimiter', ' ')

end

