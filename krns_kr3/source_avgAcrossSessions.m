function source_avgAcrossSessions(subjID, exp,condNum,norm,type,numSamples)

%%type is spm or mne
%%norm is 0 or 1
%%if you pick mne and norm=1, you should end up with something basically identical to
%%spm
%%numSamples: 1400 (-100 to 599.5sec and 2000Hz sampling rate) 
%%Ex: source_avgAcrossSessions('9367', 'Noun_Place_All', 1, 1, 'spm', 1400) 

dataPath = ['/home/custine/MEG/data/krns_kr3/', subjID, '/'];
sessList = {'s5', 's6', 's7', 's8'} 
norm = 1
n = 4 
%%for each subject, get the stc data out
for hemI = 1:2
    allSubjData = zeros(20484,numSamples,n);

    if hemI == 1
        hem = 'lh';
    elseif hemI == 2
        hem = 'rh';
    end
    
    count = 0;
    for sess=sessList
        count=count+1;
        sess 
        subjID
        sessDataPath = strcat(sess, '/ave_projon/stc/');
        %Read in stc file for subject

        filename = strcat(dataPath,sessDataPath,subjID,'_',sess,'_',exp,'_c',int2str(condNum),'M-',type,'-',hem,'.stc')
        filename
        sessSTC = mne_read_stc_file(filename{1});
        sessData = sessSTC.data;
        
        if norm == 1
            sessBaseline = mean(sessSTC.data(:,1:200),2); %200 because -100 tp 599.5 baseline is 100 ms before 0, and 2000Hz sampling rate 
            sessBaseline = repmat(sessBaseline,1,numSamples);
            sessSD = std(sessSTC.data(:,1:200),0,2);
            sessSD = repmat(sessSD,1,numSamples);
            sessSTC.data = (sessSTC.data-sessBaseline)./(sessSD);
        end
       
        allSessData(:,:,count) = sessData;

    end
    size(allSubjData)
    gaSessData = mean(allSessData,3); %%

    newSTC = sessSTC;  %%just use the last subject's STC to get the structure of the file
    newSTC.data = gaSessData;
   % outFile = strcat(dataPath,'results/source_space/ga_stc/single_condition/ga_',listPrefix, '_',exp,'_c',int2str(condNum),'M-',type,'-',hem,'.stc');
    if norm==1
        outFile = strcat('/home/custine/MEG/results/source_level/ga_stc/krns_kr3/gaSess_',subjID,'_',exp,'_c',int2str(condNum),'M-',type,'-',hem,'.stc')  
    end
    mne_write_stc_file(outFile,newSTC);
    
end
