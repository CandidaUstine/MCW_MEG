# -*- coding: utf-8 -*-
"""
Clean a raw file from EOG and ECG artifacts with PCA (ie SSP)
@author: custine
INSTRUCTIONS
This is the python script for creating and applying the SSP ecg and eog projectors using mne-py on the raw data. 
Use this script with discretion. You can edit the number of Grad and Mag projectors you want to create for each event(ECG or EOG)  depending on the effect of the artifact. This script is usually run using a  wrapper script: preProc_project.sh.  
Syntax: ./preProc_project.sh subjID tag nmag ngrad neeg
Author: Candida Jane Maria Ustine, M.Eng. 
"""


import os
import sys
sys.path.insert(0,'/home/custine/MEG/scripts/mne-python/')
import mne
from mne import fiff

########################################################################################################
########### MAKING ECG PROJECTOR ##########
def compute_proj_ecg(in_path, in_fif_fname, h_tmin, h_tmax, n_grad, n_mag, n_eeg, l_freq, h_freq, filter_length, n_jobs, reject, avg_ref):

## Reading input fif File
    raw_in = fiff.Raw(in_fif_fname)
    prefix = in_fif_fname[:-8]
    in_fif_fname = in_path + in_fif_fname
    print in_fif_fname
    out_path = os.path.join(in_path + 'ssp/')

    out_fif_fname = in_path + 'ssp/' + prefix + '_clean_ecg_raw.fif'
    ecg_proj_fname = in_path  + prefix + '_ecg_proj.fif'
    ecg_event_fname = in_path + 'ssp/' + prefix + '_ecg-eve.fif'        
    
#    print 'Implementing ECG artifact rejection on data'
#    ecg_events, _, _ = mne.artifacts.find_ecg_events(raw_in)
#    if not len(ecg_events) < 30:
#           # print ecg_event_fname
#           print "Writing ECG events in %s" % ecg_event_fname
#           mne.write_events(ecg_event_fname, ecg_events)
        
## Making ECG projector
    print 'Computing ECG projector'
    print out_path
    #os.getcwd()
    command = ('mne_process_raw --cd %s --raw %s --events %s --digtrig STI101 --makeproj '
                       '--projtmin -0.1 --projtmax 0.1 --saveprojtag _ecg_proj '
                       '--projnmag 1 --projngrad 1 --projevent 402 --highpass 5 '
                       '--lowpass 35 --projmagrej 5000 --projgradrej 4000'
                       % (in_path, in_fif_fname, ecg_event_fname))
    print command
    st = os.system(command)
    if st != 0:
            print "Error while running : %s" % command
                   
    return in_fif_fname, ecg_proj_fname, len(ecg_event_fname), out_fif_fname

########################################################################################################
########### MAKING EOG PROJECTOR ########## 
                             
def compute_proj_eog(in_path, in_fif_fname, e_tmin, e_tmax, n_grad, n_mag, n_eeg, l_freq, h_freq, filter_length, n_jobs, reject, avg_ref):


    prefix = in_fif_fname[:-8]
    print prefix
    in_fif_fname = in_path + in_fif_fname
    print in_fif_fname

    out_fif_fname = in_path + 'ssp/' + prefix + '_clean_eog_raw.fif'
    eog_proj_fname = in_path + prefix + '_eog_proj.fif' 
    eog_event_fname = in_path + 'ssp/' + prefix + '_eog-eve.fif'
    
    print "Computing the EOG projector"
    command = ('mne_process_raw --cd %s --raw %s --events %s --digtrig STI101 --makeproj '
                               '--projtmin %s --projtmax %s --saveprojtag _eog_proj '
                               '--projnmag %s --projngrad %s --projevent 202 --highpass 0.3 '
                               '--lowpass 35 --filtersize 8192 --projmagrej 5000 --projgradrej 4000'  ###projeegrej 500 by default
                               % (in_path, in_fif_fname, eog_event_fname, e_tmin, e_tmax, n_mag, n_grad))
    st = os.system(command)
    if st != 0:
            print "Error while running : %s" % command
                    
    return in_fif_fname, eog_proj_fname, len(eog_event_fname), out_fif_fname

########################################################################################################                             
                              
if __name__ == '__main__':
    from optparse import OptionParser

    parser = OptionParser()
    parser.add_option("-i", "--in", dest="raw_in",
                    help="Input raw FIF file", metavar="FILE")
    parser.add_option("-o", "--out", dest="raw_out",
                    help="Input raw FIF file", metavar="FILE",
                    default=None)
    parser.add_option("--in_path", dest="in_path",
                    help="Raw file path name",
                    default=None)
    parser.add_option("--h_tmin", dest="h_tmin", type="float",
                    help="time before event in seconds",
                    default=-0.08)
    parser.add_option("--h_tmax", dest="h_tmax", type="float",
                    help="time after event in seconds",
                    default=0.08)
    parser.add_option("--e_tmin", dest="e_tmin", type="float",
                    help="time before event in seconds",
                    default=-0.2)
    parser.add_option("--e_tmax", dest="e_tmax", type="float",
                    help="time after event in seconds",
                    default=0.2)
    parser.add_option("-g", "--n-grad", dest="n_grad", type="int",
                    help="Number of SSP vectors for gradiometers",
                    default=1)
    parser.add_option("-m", "--n-mag", dest="n_mag", type="int",
                    help="Number of SSP vectors for magnetometers",
                    default=1)
    parser.add_option("-e", "--n-eeg", dest="n_eeg", type="int",
                    help="Number of SSP vectors for EEG",
                    default=1) 
    parser.add_option("--l-freq", dest="l_freq",
                    help="Filter low cut-off frequency in Hz",
                    default=None)  # XXX
    parser.add_option("--h-freq", dest="h_freq",
                    help="Filter high cut-off frequency in Hz",
                    default=None)  # XXX
    parser.add_option("-p", "--preload", dest="preload",
                    help="Temporary file used during computaion",
                    default='tmp.mmap')
    parser.add_option("-a", "--average", dest="average", action="store_true",
                    help="Compute SSP after averaging",
                    default=False)
    parser.add_option("--filtersize", dest="filter_length",
                    help="Number of SSP vectors for EEG",
                    default=2048)
    parser.add_option("-j", "--n-jobs", dest="n_jobs",
                    help="Number of jobs to run in parallel",
                    default=1)
    parser.add_option("-c", "--channel", dest="ch_name",
                    help="Channel to use for ECG detection (Required if no ECG found)",
                    default=None)
    parser.add_option("--rej-grad", dest="rej_grad",
                    help="Gradiometers rejection parameter in fT/cm (peak to peak amplitude)",
                    default=3000)
    parser.add_option("--rej-mag", dest="rej_mag",
                    help="Magnetometers rejection parameter in fT (peak to peak amplitude)",
                    default=4000)
    parser.add_option("--rej-eeg", dest="rej_eeg",
                    help="EEG rejection parameter in uV (peak to peak amplitude)",
                    default=250)
    parser.add_option("--rej-eog", dest="rej_eog",
                    help="EOG rejection parameter in uV (peak to peak amplitude)",
                    default=250)
    parser.add_option("--avg-ref", dest="avg_ref", action="store_true",
                    help="Add EEG average reference proj",
                    default=False)
    parser.add_option("--bad", dest="bad_fname",
                    help="Text file containing bad channels list (one per line)",
                    default=None)
    parser.add_option("--tag", dest="tag",
                    help="Tag that defines whether to run ecg or eog projection. Can take ecg or eog or ecgeog",
                    default=None)

    options, args = parser.parse_args()
    raw_in = options.raw_in
    raw_out = options.raw_out
    if raw_in is None:
        parser.print_help()
        sys.exit(-1)
   
    in_path = options.in_path
    out_path = in_path + 'ssp/'
    e_tmin = options.e_tmin
    e_tmax = options.e_tmax
    h_tmin = options.h_tmin
    h_tmax = options.h_tmax
    n_grad = options.n_grad
    n_mag = options.n_mag
    n_eeg = options.n_eeg
    l_freq = options.l_freq
    h_freq = options.h_freq
    preload = options.preload
    filter_length = options.filter_length
    n_jobs = options.n_jobs
    tag = options.tag
    reject = dict(grad=1e-13 * float(options.rej_grad),
                  mag=1e-15 * float(options.rej_mag),
                  eeg=1e-6 * float(options.rej_eeg))
                  ##eog=1e-6 * float(options.rej_eog))
    avg_ref = options.avg_ref
    bad_fname = options.bad_fname
 
########################################################################################################
############### APPLYING THE ECG AND EOG PROJECTORS ####################   
    if (tag == "ecg"):
            in_fif_fname, ecg_proj_fname, ecg_events, out_fif_fname = compute_proj_ecg(in_path, raw_in, h_tmin, h_tmax, n_grad, n_mag, n_eeg, l_freq, h_freq, filter_length, n_jobs, reject, avg_ref)
            print 'Applying ECG projector'
            command = ('mne_process_raw --cd %s --raw %s --proj %s --projoff --save %s --filteroff'
                       % (out_path, in_fif_fname, ecg_proj_fname, out_fif_fname))
            print 'Command executed: %s' % command
            st = os.system(command)
            if st != 0:
                    raise ValueError('Pb while running : %s' % command)
            print ('Done removing ECG artifacts. '
                   'IMPORTANT : Please eye-ball the data !!')


    elif (tag == "eog"):
            in_fif_fname, eog_proj_fname, eog_events, out_fif_fname = compute_proj_eog(in_path, raw_in, e_tmin, e_tmax, n_grad, n_mag, n_eeg, l_freq, h_freq, filter_length, n_jobs, reject, avg_ref)
            print eog_proj_fname
            print 'Applying EOG projector'
            command = ('mne_process_raw --cd %s --raw %s --proj %s --projoff --save %s --digtrig STI101 --filteroff'
                       % (in_path, in_fif_fname, eog_proj_fname, out_fif_fname))
            print 'Command executed: %s' % command
            st = os.system(command)
            if st != 0:
                    raise ValueError('Pb while running : %s' % command)
            print ('Done removing EOG artifacts.'
                   'IMPORTANT : Please eye-ball the data !!')

    elif (tag == "ecgeog"):
            in_fif_fname, ecg_proj_fname, ecg_events, out_fif_fname = compute_proj_ecg(in_path, raw_in, h_tmin, h_tmax, n_grad, n_mag, n_eeg, l_freq, h_freq, filter_length, n_jobs, reject, avg_ref)
            in_fif_fname, eog_proj_fname, eog_events, out_fif_fname = compute_proj_eog(in_path, raw_in, e_tmin, e_tmax, n_grad, n_mag, n_eeg, l_freq, h_freq, filter_length, n_jobs, reject, avg_ref)
            
            prefix = raw_in[:-8]
            print prefix
            out_fname = in_path + 'ssp/' + prefix + '_clean_ecgeog_raw.fif' 

            print 'Applying ECG and EOG projector'
            command = ('mne_process_raw --cd %s --raw %s --proj %s --proj %s --projoff --save %s --filteroff'
                       % (in_path, in_fif_fname, ecg_proj_fname, eog_proj_fname,
                       out_fname))
            print 'Command executed: %s' % command
            st = os.system(command)
            if st != 0:
                raise ValueError('Pb while running : %s' % command)
            print ('Done removing ECG and EOG artifacts. '
                   'IMPORTANT : Please eye-ball the data !!')

