import os
from os.path import join as pj
import sys
from glob import glob


def ssp_event_creator(subjID, event):

 fiffs = []
 in_path = pj('/home/custine/MEG/data/msabri/', subjID)  ### TO CHANGE HERE
 fiffs = glob(pj('*_raw.fif'))
 fiffs[:] = filter(lambda x: 'EmptyRoom' not in x and 'Spont' not in x, fiffs) ### TO Change here 
 fiffs.sort()
 cmd = ['warning off all']
 line = "addpath('/home/custine/MEG/scripts/');"
 cmd.append(line)
 if event == 'ecg': 
   mlab = "ssp_find_ecg_event( '%s','%s');"
 elif event == 'eog':
   mlab = "ssp_find_eog_event('%s', '%s');"

 for fif in fiffs:
     cmd.append(mlab % (subjID, fif))
 cmd.append('exit;')
 ssp_dir = pj('/home/custine/MEG/data/msabri/', subjID, 'ssp')
 print ssp_dir
 write_file_with_list(pj(ssp_dir, 'ssp_event_creator.m'), cmd)


def write_file_with_list(path,lines):
    """
    Any file writing should go through here.
    """
    try:
        with open(path,'w') as f:
            text = '\n'.join(lines)
            f.write(text + '\n')
            print("Hi! Wrote %s (%d)" % (os.sep.join(path.split(os.sep)[5:]),len(lines)))
    except IOError:
        raise


if __name__ == '__main__':
    subjID = sys.argv[1]
    event = sys.argv[2]
    ssp_event_creator(subjID, event)
