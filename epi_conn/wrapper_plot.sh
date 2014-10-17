#!/bin/csh -f 
 
##Wrapper for mne_plot_inverse_coherence_epochs.py script 

#./wrapper_plot.sh subjID 
 



foreach m ('alpha' 'beta' 'gamma' 'theta')

	python plot_mne_inverse_coherence_epochs.py $1 $m 
end


