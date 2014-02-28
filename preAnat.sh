#!/bin/csh -f 

#Created on Thu Feb 27 15:51:25 2014
#@author: custine
#Usage: ./preAnat.sh exp subjID


setenv SUBJECT $2
set BEM_METHOD = WATER 

remove teh existing log file
if ( -e /home/custine/MEG/data/{$1}/{$2}/logs/preAnat.log ) then
    rm /home/custine/MEG/data/{$1}/{$2}/logs/preAnat.log
endif

if ( $#argv == 3 ) then
    #set log = '/home/custine/MEG/data/{$1}/{$2}/ave_projon/logs/preProc_avg.log'
    touch /home/custine/MEG/data/{$1}/{$2}/logs/preAnat.log
    echo "Logging to default log..." >>& /home/custine/MEG/data/{$1}/{$2}/logs/preAnat.log
endif

echo "Hello! Make sure the Cortical surface reconstructions have been created for your subject before you run this step..." 

#Setting up the anatomical MR images for MRILab 
echo "Setting up the anatomical MR images for MRILab..."
mne_setup_mri --overwrite >>& /home/custine/MEG/data/{$1}/{$2}/logs/preAnat.log 

#Setting up the Source Space(creating a decimated dipole grid on the wm surface - default 7mm grid spacing)
echo "Setting up the Source Space..."
mne_setup_source_space >>& /home/custine/MEG/data/{$1}/{$2}/logs/preAnat.log 

#Creating the BEM Model meshes 
echo "Creating the BEM meshes..."
echo "Using the Watershed method to create the surfaces"
mne_watershed_bem --overwrite >>& /home/custine/MEG/data/{$1}/{$2}/logs/preAnat.log
cd /home/custine/MRI/structurals/subjects/$2/bem
rm *.surf
ln -s ./watershed/$2_outer_skin_surface outer_skin.surf
ln -s ./watershed/$2_outer_skull_surface outer_skull.surf
ln -s ./watershed/$2_inner_skull_surface inner_skull.surf
#mv $SUBJECTS_DIR/$1/bem/$1-bem.fif $SUBJECTS_DIR/$1/bem/$1-orig-bem.fif

#Setting up the BEM 
mne_setup_forward_model --surf --ico 4  >>& /home/custine/MEG/data/{$1}/{$2}/logs/preAnat.log
 
