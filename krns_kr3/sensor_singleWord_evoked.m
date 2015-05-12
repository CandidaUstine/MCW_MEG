%% Trial One 
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

subjID = '9367'
sessID = {'s5', 's6'}
word = textread('/home/custine/MEG/scripts/krns_kr3/word.txt', '%s')
wordID = textread('/home/custine/MEG/scripts/krns_kr3/wordID.txt', '%d') 


for sess = sessID
    sess
end

for w = word(1:2)
    for id = wordID(1:2)
        w
        id = num2str(id,'%03d')

        sess = 's5'
        inpath = ['/home/custine/MEG/data/krns_kr3/', subjID, '/', sess, '/epochs/'];
        run1 = strcat(inpath, '/run1/', subjID,'_',sess, '_run1_',id,w,'-epochs.mat')
        run2 = strcat(inpath, '/run2/',subjID,'_',sess, '_run2_',id,w,'-epochs.mat')
        run3 = strcat(inpath, '/run3/',subjID,'_',sess, '_run3_',id,w,'-epochs.mat')
        run4 = strcat(inpath, '/run4/',subjID,'_',sess, '_run4_',id,w,'-epochs.mat')
        run5 = strcat(inpath, '/run5/',subjID,'_',sess, '_run5_',id,w,'-epochs.mat')
        run6 = strcat(inpath, '/run6/',subjID,'_',sess, '_run6_',id,w,'-epochs.mat')
        run7 = strcat(inpath, '/run7/',subjID,'_',sess, '_run7_',id,w,'-epochs.mat')
        run8 = strcat(inpath, '/run8/',subjID,'_',sess, '_run8_',id,w,'-epochs.mat')
        run9 = strcat(inpath, '/run9/',subjID,'_',sess, '_run9_',id,w,'-epochs.mat')
        run10 = strcat(inpath, '/run10/',subjID,'_',sess, '_run10_',id,w,'-epochs.mat')
        run11 = strcat(inpath, '/run11/',subjID,'_',sess, '_run11_',id,w,'-epochs.mat')
        run12 = strcat(inpath, '/run12/',subjID,'_',sess, '_run12_',id,w,'-epochs.mat')


        epochs1 = load(run1{1});
        epochs2 = load(run2{1});
        epochs3 = load(run3{1});
        epochs4 = load(run4{1});
        epochs5 = load(run5{1});
        epochs6 = load(run6{1});
        epochs7 = load(run7{1});
        epochs8 = load(run8{1});
        epochs9 = load(run9{1});
        epochs10 = load(run10{1});
        epochs11 = load(run11{1});
        epochs12 = load(run12{1});

        % 

        
        epochsR1 = epochs1.epochs_data;
        
        if isempty(epochs2)
            epochsR2 = struct('epochs_data', {0,0,0})
        else
            epochsR2 = epochs2.epochs_data;
        end
        epochsR2 = epochs2.epochs_data;
        epochsR3 = epochs3.epochs_data;
        epochsR4 = epochs4.epochs_data;
        epochsR5 = epochs5.epochs_data;
        epochsR6 = epochs6.epochs_data;
        epochsR7 = epochs7.epochs_data;
        epochsR8 = epochs8.epochs_data;
        epochsR9 = epochs9.epochs_data;
        epochsR10 = epochs10.epochs_data;
        epochsR11 = epochs11.epochs_data;
        epochsR12 = epochs12.epochs_data;
        


        epochs = cat(1, epochsR1, epochsR2, epochsR3, epochsR4, epochsR5, epochsR6, epochsR7, epochsR8, epochsR9, epochsR10, epochsR11, epochsR12);

        newavg = squeeze(mean(epochs,1));

        evokednew = fiff_read_evoked_all('/home/custine/MEG/data/krns_kr3/9367/s5/ave_projon/9367_s5_AllItems_All-ave.fif')
        evokednew.info
        info = evokednew.info; 
        ev_all = []
        ev_all.evoked.aspect_kind = 100;
        ev_all.evoked.is_smsh = 0; 
        ev_all.evoked.nave = size(epochs,1);
        ev_all.evoked.first = -200;
        ev_all.evoked.last = 1200;
        ev_all.evoked.comment = w;
        ev_all.evoked.times = linspace(-0.1, 0.6, 1401);
        ev_all.evoked.epochs = newavg;
        ev_all.info = info;

        g_ave_file = strcat(inpath, '/epochs/', subjID,'_',sess, '_',id,w,'-ave.fif')

        fiff_write_evoked(g_ave_file{1}, ev_all)
    end
end
%% Trial Two 
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
word = textread('/home/custine/MEG/scripts/krns_kr3/word.txt', '%s');
wordID = textread('/home/custine/MEG/scripts/krns_kr3/wordID.txt', '%d')
subjID = '9367'

epochs = ['/home/custine/MEG/data/krns_kr3/9367/9367_sum-epochs.mat']
epochs = load(epochs);

epochsLen = ['/home/custine/MEG/data/krns_kr3/9367/9367_len-epochs.mat']
epochsLen = load(epochsLen);

epochsR = epochs.meanArr; 
evokednew = fiff_read_evoked_all('/home/custine/MEG/data/krns_kr3/9367/s5/ave_projon/9367_s5_AllItems_All-ave.fif')
evokednew.info
info = evokednew.info; 


for id = 4:4
    id
    w = word(id)
    item = double(epochsR(id,:, :));
    
    
    ev_all = []
    ev_all.evoked.aspect_kind = 100;
    ev_all.evoked.is_smsh = 0; 
    ev_all.evoked.nave = 1;
    ev_all.evoked.first = -200;
    ev_all.evoked.last = 1200;
    ev_all.evoked.comment = char(w); %'single word';
    ev_all.evoked.times = linspace(-0.1, 0.6, 1401);
    ev_all.evoked.epochs = squeeze((item));
    ev_all.info = info;
    id = num2str(id,'%03d')
    
    g_ave_file = strcat('/home/custine/MEG/data/krns_kr3/9367/epochs/', subjID, '_',id,'_', w,'-ave.fif')
    fiff_write_evoked(g_ave_file{1}, ev_all)
%     item(1,1,1)
end


