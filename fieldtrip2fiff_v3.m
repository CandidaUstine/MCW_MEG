function fieldtrip2fiff_v3(filename, data) 

% this ensures that the path is correct and that the ft_defaults global variable is available
ft_defaults

% ensure that the filename has the correct extension
[pathstr, name, ext] = fileparts(filename);
if ~strcmp(ext, '.fif')
  error('if the filename is specified with extension, this should read .fif');
end
fifffile = [pathstr filesep name '.fif'];
eventfile = [pathstr filesep name '-eve.fif'];

% ensure the mne-toolbox to be on the path
ft_hastoolbox('mne', 1);

% check the input data
data   = ft_checkdata(data, 'datatype', {'raw', 'timelock'}, 'feedback', 'yes');
israw = ft_datatype(data, 'raw');
if israw
    disp('You fieldtrip data is ready to be converted to fiff... Wait... ')
end

% Create a fiff-header, or take it from the original header if possible
if ft_senstype(data, 'neuromag') && isfield(data, 'hdr')
  fprintf('Using the original FIFF header, but channel locations are read \nfrom .grad and .elec in the data, if they exist\n')
  info = data.hdr.orig;
end
% info.sfreq = data.fsample;
% info.ch_names = data.label(:)';
% info.chs      = sens2fiff(data);
% info.nchan    = numel(data.label);

[outfid, cals] = fiff_start_writing_raw(fifffile, info);
fiff_write_raw_buffer(outfid, data.trial, cals);
fiff_finish_writing_raw(outfid);

end

