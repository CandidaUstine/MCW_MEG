import os
from os.path import join as pj
from glob import glob 

def ssp_event_creator(exp, subjID, event):

    fiffs = []
    in_path = '/home/custine/MEG/data/'+ exp+'/'+subjID+'/'  ### TO CHANGE HERE
    fiffs = glob(pj(in_path,'*_raw.fif'))
    fiffs[:] = filter(lambda x: 'EmptyRoom' not in x and 'Spont' not in x, fiffs) ### TO Change here 
    fiffs.sort()
    if event == 'ecg': 
      mlab = "ssp_find_ecg_event( '%s','%s');"
    elif event == 'eog':
      mlab = "ssp_find_eog_event('%s');"
    
    cmd = ['warning off all']
    for fif in fiffs:
         cmd.append(mlab %subjID %fif)
    cmd.append('exit;')
    ssp_dir = pj(in_path, '/', subjID, '/ssp/')
    if not os.path.isdir(ssp_dir):
         os.mkdir(ssp_dir)
    write_file_with_list(pj(ssp_dir, 'reject.m'), cmd)


def write_file_with_list(path,lines,quiet=False):
    """
    Any file writing should go through here.
    """
    try:
        with open(path,'w') as f:
            text = '\n'.join(lines)
            f.write(text + '\n')
        if not quiet:
            print("Hi! Wrote %s (%d)" % (os.sep.join(path.split(os.sep)[5:]),len(lines)))
    except IOError:
        raise
