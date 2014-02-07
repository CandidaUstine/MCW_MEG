#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This experiment was created using PsychoPy2 Experiment Builder (v1.77.01), Tue 21 Jan 2014 10:52:46 AM CST
If you publish work using this script please cite the relevant PsychoPy publications
  Peirce, JW (2007) PsychoPy - Psychophysics software in Python. Journal of Neuroscience Methods, 162(1-2), 8-13.
  Peirce, JW (2009) Generating stimuli for neuroscience using PsychoPy. Frontiers in Neuroinformatics, 2:10. doi: 10.3389/neuro.11.010.2008
"""

import time 
import sys 
from psychopy import visual, event, core 

win = visual.Window([800,800], color="black", units='pix')
squareL = visual.PatchStim(win, tex="none", mask = "none", color="blue", size  =[200, 200], pos=[-200,0])
squareR = visual.PatchStim(win, tex= "none", mask="none", color=  "red", size=[200, 200], pos=[200,0]) 
while True:    
    squareL.draw()
    win.flip()
    core.wait(1)
    squareR.draw()
    win.flip()
    core.wait(1)
    if event.getKeys('p'):
        event.waitKeys('r')
    elif event.getKeys('q') or event.getKeys('s'):
            break
            
#numStims = 16
#spacing = 30
#locations=[]p
#while True:
#    for curStim in range(numStims):
#        pass
#    if event.getKeys('space'):
#        break
#    win.flip() 

##square.setOri(45)
##square.setColor('red')
##square.draw()
##win.flip()
##core.wait(1)

##secs=1/90.0
##degs=360/90.0
##while True:
##    square.setOri(degs, '+')
##    square.draw()
##    win.flip()
##    core.wait(secs)
##    if event.getKeys('s'):
##        event.waitKeys('r')
sys.exit()

