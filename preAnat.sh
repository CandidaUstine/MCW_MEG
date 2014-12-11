#!/bin/csh -f 

#Created on Thu Feb 27 15:51:25 2014
#@author: custine
#Usage: ./preAnat.sh exp subjID

date 

echo $2
date

setenv SUBJECT $2
set BEM_METHOD = WATER 
set surf_dir = /home/custine/MRI/structurals/subjects
set subj_dir = /home/custine/MEG/data/$1/$2/

if ($1 == 'krns_kr3') then 
    echo "Study Name: " 
    echo $1 
    set surf_dir = /mnt/file1/binder/KRNS/anatomies/surfaces
    set subj_dir = /home/custine/MEG/data/krns_kr3/$1/$2/
    setenv SUBJECTS_DIR $surf_dir
endif
set log = /home/custine/MEG/data/$1/$2/logs/$2_preAnat.log
setenv SUBJECTS_DIR $surf_dir

##remove the existing log file
if ( -e $log ) then
    rm $log
endif

echo "Jane here"
date >>& $log

echo $surf_dir 
echo $subj_dir
echo $log

if ( $#argv == 3 ) then
    touch $log
    echo "Logging to default log..." >>& $log
endif

echo "Hello! Make sure the Cortical surface reconstructions have been created for your subject before you run this step..." 
echo "Hello! Make sure the Cortical surface reconstructions have been created for your subject before you run this step..." >>& $log

#Setting up the anatomical MR images for MRILab 
echo "Setting up the anatomical MR images for MRILab..." 
mne_setup_mri >>& $log 

#Setting up the Source Space(creating a decimated dipole grid on the wm surface - default 7mm grid spacing)
echo "Setting up the Source Space..."
mne_setup_source_space >>& $log 
mne_setup_source_space --ico 4 >>& $log 

#Creating the BEM Model meshes 
echo "Creating the BEM meshes..."
echo "Using the Watershed method to create the surfaces"
mne_watershed_bem >>& $log
cd $surf_dir/$2/bem

ls
rm *.surf
ln -s ./watershed/$2_outer_skin_surface outer_skin.surf
ln -s ./watershed/$2_outer_skull_surface outer_skull.surf
ln -s ./watershed/$2_inner_skull_surface inner_skull.surf
mv $SUBJECTS_DIR/$2/bem/$2-bem.fif $SUBJECTS_DIR/$2/bem/$2-orig-bem.fif

#Setting up the BEM surfaces for viewing 
mne_setup_forward_model --surf --ico 4 >>& $log ##IF surfaces are not contained within each other in the proper manner then use the --innershift and --outershift tags in order to modify the surfaces while creating the forward model. 

mne_make_scalp_surfaces >>& $log
mv $surf_dir/$2/bem/$2-head.fif $surf_dir/$2/bem/$2-head-old.fif >>& $log

ln $surf_dir/$2/bem/$2-head-medium.fif $surf_dir/$2/bem/$2-head.fif >>& $log




