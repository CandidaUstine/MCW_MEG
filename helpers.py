import os
from os.path import join as pj
import sys
from glob import glob


def ssp_event_creator(exp, subjID, event):

 fiffs = []
 in_path = '/home/custine/MEG/data/'+exp+'/'+ subjID  ### TO CHANGE HERE
 fiffs = glob(pj(in_path,'*_raw.fif'))
 #print fiffs
 fiffs[:] = filter(lambda x: 'EmptyRoom' not in x and 'VisualRun2' not in x and 'Spont' not in x, fiffs) ### TO Change here 
 fiffs.sort()
 cmd = ['warning off all']
 line = "addpath('/home/custine/MEG/scripts/');"
 cmd.append(line)
 if event == 'ecg': 
   mlab = "ssp_find_ecg_event('%s', '%s', '%s');"
 elif event == 'eog':
   mlab = "ssp_find_eog_event('%s', '%s', '%s');"

 for fif in fiffs:
     cmd.append(mlab % (exp, subjID, fif))
 cmd.append('exit;')
 ssp_dir = '/home/custine/MEG/data/'+exp+'/'+ subjID+'/ssp/'
 print ssp_dir
 write_file_with_list(pj(ssp_dir, 'ssp_event_creator.m'), cmd)
 #sys.exit(cmd)


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
    exp = sys.argv[1]
    subjID = sys.argv[2]
    event = sys.argv[3]
    ssp_event_creator(exp, subjID, event)
