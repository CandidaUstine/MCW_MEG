function preProc_setup_FT(exp, subjID) %, paradigmName, run, condNum)

% 

%Author: Candida Jane Maria Ustine, custine@mcw.edu
%Modified for krns study 
%Usage: preProc_setup_FT('custine', 'cu1')

%% Initialise Fieldtrip Defaults 
ft_defaults

%% Initialise Subject Specific Defaults  
inpath = ['/home/custine/MEG/data/',exp,'/', subjID, '/']
%disp(inpath)
cd(inpath)

mkdir('eve')
mkdir('ave')
mkdir('ave')
mkdir('ave_projon')
mkdir('ave_projon', 'logs')
mkdir('ave_projon', 'plots')
mkdir('ave_projoff')
mkdir('ave_projoff', 'logs')
mkdir('ave_projoff', 'plots')
mkdir('ica')
mkdir('rej')
mkdir('logs')
mkdir('raw_backup')

%% Backup Raw files 
movefile('*.fif', 'raw_backup')
copyfile('raw_backup/*.fif')

% files = dir('raw_backup/*.fif');
% for file = files'
% [pathstr,name,ext] = fileparts(file.name);
% %disp(name(1:end-4))
% newname = strcat(name(1:end-4), '.fif')
% %movefile('cu1_AudioRun1_raw.fif', '/home/custine/MEG/data/custine/cu2/')
% end



end
