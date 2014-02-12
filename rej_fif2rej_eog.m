function rej_fif2rej_eog(expt,subjID,paradigmName, do_plot)
%------------------------
%
% Writes out rejection files, each with two columns.
% First column is time point (in samples) and next is
% channel on which that time point should be rejected
%
% Inputs
%   fiff - fif file path
%   (optional) do_plot - 1 if you'd like to visualize rejections, 0 if not
%------------------------


% add 'eeg' or 'mag' or 'grad' if you want to make rej files based on these channels
%chan_c = {'veog', 'heog' };
chan_c = {'veog'};

%%%%%%%%%
% find the appropriate rej_thr.txt file
fiff = strcat('/home/custine/MEG/data/',expt,'/',subjID,'/',subjID,'_',paradigmName,'_raw.fif')

[~, n, ~] = fileparts(fiff);
ind = find(n == '_', 1, 'first');
sub_thr = ['/home/custine/MEG/data' expt '/' subjID '/rej/rej_thr.txt']; 
if exist(sub_thr, 'file')
    disp('Using subject specific thresholds...')
    rej_path = sub_thr;
else
    disp('Using default thresholds...')
    rej_path = '/home/custine/MEG/scripts/function_inputs/rej_thr.txt';
end
S = importdata(rej_path);

% find each rej thr
[~, i] = ismember(S.textdata, 'veog');
veog_rej = S.data(i == 1)

veog_chan = 307;
%heog_chan = 3xx %%Must Update this when info is available! 

for chan = chan_c
    chan_str = chan{1};
        switch chan_str
            case 'veog'
                chans = veog_chan;
                meth = 'win';
                thr = veog_rej;
                f = @window;
            case 'heog'
                chans = heog_chan;
                meth = 'win';
                thr = heog_rej;
                f = @window;
            otherwise
                error('Bad chan_str specifier')
        end

    %build new filename
    [p, n, ~] = fileparts(fiff);
    new_fn = [n '_' chan_str '.txt'];
    tmp = fullfile(p, 'rej');
    if exist(tmp, 'dir') ~= 8
        [status, ~, ~] = mkdir(tmp);
        if status ~= 1
            error(['Cannot make ' tmp]);
        end
    end
    new_path = fullfile(tmp, new_fn);

    % some output
    fprintf('fiff: %s\ndata: %s\nmethod: %s\nrejection file: %s\n', fiff, chan_str, meth, new_path);

    % load data
    ds = fiff_setup_read_raw(fiff);
    
    
    % don't load bad chan
    [~, ia, ~] = intersect(ds.info.ch_names, ds.info.bads);
    [~, ib, ~] = intersect(chans, ia);
    chans(ib) = [];
    
    X = fiff_read_raw_segment(ds,ds.first_samp,ds.last_samp,chans);
    %X = fiff_read_raw_segment(ds,1,120000,chans);
    
    Xm = detrend(X', 'constant')';
    
    Xrms = sqrt(mean(Xm.^2,1));
    %figure;plot(Xrms(:,1:40000));
    
    %chans = 3;
    % compute bad sample points
    bad_mat = f(Xrms, thr, ds, chans, do_plot);


    % write out bad samples
    fprintf('Writing results to %s\n', new_path);
    dlmwrite(new_path, bad_mat, 'delimiter', '\t', 'precision', '%d');

    clear X Xm bad_mat new_path new_fn tmp
end

end

function bad_mat = window(X, thr, ds,chans, p)
    fprintf('Running window rejection method...\n')
    %thr = 2e-13
    srate = ds.info.sfreq;
    N = length(X);
    %w = 100*(srate/1000) %each window is 100ms on either side of the current timepoint
    w = 60
    mat_ind = 1;
    bad_mat = zeros(N,2);
    first = double(ds.first_samp);
    n = 2:N-1;
    tic
    for ii = n
        pre_ind = ii-1:-1:ii-w;
        pre_m = mean(X(pre_ind(pre_ind > 0)));
        post_ind = ii+1:ii+w;
        post_m = mean(X(post_ind(post_ind <= N)));
        d = post_m - pre_m;
        if d > thr || d < -thr
            tp = first + ii;
            bad_mat(mat_ind,:) = [tp chans];
            mat_ind = mat_ind + 1;
        end
    end
    bad_mat = bad_mat(1:mat_ind-1,:);
    fprintf('Finished window rejection method in %3.3f s\n', toc)
    if p
    %     t = double(ds.first_samp):double(ds.last_samp);
        [n, x] = hist(bad_mat(:,1), length(X));
        n(1,2) = 0;
        size(n)
        %figure;bar(x,n)
        plotter(chans, ds, X, n, x, first, thr)
    end
end



function plotter(c_num, ds, dat, n, x, first, thr)
figure(c_num);close(c_num);figure(c_num)
set(c_num, 'Position', [2100 600 560 420] );
%t = double(ds.first_samp):double(ds.last_samp);
t=double(1:50000);
hold on;
axis([first first+length(t) 0 2])
plot(t, dat(1:50000)*1e12, 'b');title('RMS frontal channels in picoTesla, 50000 samples')
%bar(x, n/(1/thr),'EdgeColor', [1 0 0]);
bar(x,n*3,'EdgeColor', [1 0 0])
%axis([first first+length(dat) 0 3e-12])
hold off;
end


