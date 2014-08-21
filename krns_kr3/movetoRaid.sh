#!/bin/csh -f

##Created on Wed Aug 13 11:22:39 2014
##@author: custine
#usage: ./movetoRaid.sh subjID sessID num


echo  $1 $2 $3
#cd /home/custine/MEG/data/krns_kr3/
#if ( ! -d $1  ) then 
#	mkdir $1
#endif


cd /mnt/yak/binder_data/krns/kr3/$1/$3/*/sss/

ls

pwd


cd $1_$2_run1
pwd
rsync -a *_sss.fif /home/custine/MEG/data/krns_kr3/$1/$2/
cd ..

cd $1_$2_run2
pwd
rsync -a *_sss.fif /home/custine/MEG/data/krns_kr3/$1/$2/
cd ..

cd $1_$2_run3
pwd
rsync -a *_sss.fif /home/custine/MEG/data/krns_kr3/$1/$2/
cd ..

cd $1_$2_run4
pwd
rsync -a *_sss.fif /home/custine/MEG/data/krns_kr3/$1/$2/
cd ..

cd $1_$2_run5
pwd
rsync -a *_sss.fif /home/custine/MEG/data/krns_kr3/$1/$2/
cd ..


cd $1_$2_run6
pwd
rsync -a *_sss.fif /home/custine/MEG/data/krns_kr3/$1/$2/
cd ..

cd $1_$2_run7
pwd
rsync -a *_sss.fif /home/custine/MEG/data/krns_kr3/$1/$2/
cd ..

cd $1_$2_run8
pwd
rsync -a *_sss.fif /home/custine/MEG/data/krns_kr3/$1/$2/
cd ..

cd $1_$2_run9
pwd
rsync -a *_sss.fif /home/custine/MEG/data/krns_kr3/$1/$2/
cd ..

cd $1_$2_run10
pwd
rsync -a *_sss.fif /home/custine/MEG/data/krns_kr3/$1/$2/
cd ..

cd $1_$2_run11
pwd
rsync -a *_sss.fif /home/custine/MEG/data/krns_kr3/$1/$2/
cd ..

cd $1_$2_run12
pwd
rsync -a *_sss.fif /home/custine/MEG/data/krns_kr3/$1/$2/
cd ..

cd $1_$2_emptyroom
pwd
rsync -a *_sss.fif /home/custine/MEG/data/krns_kr3/$1/$2/
cd ..

#cd /home/custine/MEG/data/krns_kr3/$1/$2
