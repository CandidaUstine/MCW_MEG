#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This experiment was created using PsychoPy2 Experiment Builder (v1.77.01), Tue 21 Jan 2014 02:45:01 PM CST
If you publish work using this script please cite the relevant PsychoPy publications
  Peirce, JW (2007) PsychoPy - Psychophysics software in Python. Journal of Neuroscience Methods, 162(1-2), 8-13.
  Peirce, JW (2009) Generating stimuli for neuroscience using PsychoPy. Frontiers in Neuroinformatics, 2:10. doi: 10.3389/neuro.11.010.2008

Experiment coded by Candida Jane Maria Ustine - custine@mcw.edu
Created on January 23rd, 2014
Updates: 

"""

from __future__ import division  # so that 1/3=0.333 instead of 1/3=0
from psychopy import visual, core, data, event, logging, sound, gui
from psychopy.constants import *  # things like STARTED, FINISHED
import numpy as np  # whole numpy lib is available, prepend 'np.'
from numpy import sin, cos, tan, log, log10, pi, average, sqrt, std, deg2rad, rad2deg, linspace, asarray
from numpy.random import random, randint, normal, shuffle
import os  # handy system and path functions
import csv

#for parallel port control and function for sending triggers for EEG
try:
    import ctypes
    from ctypes import windll
    p=windll.inpout64
    timer=core.Clock()
    def sendEEGTrig(trigger):
        trigger=ctypes.c_long(trigger)
        p.Out32(0x2040,trigger)
        t0=timer.getTime()
        while timer.getTime()<t0+0.005: pass   #wait until 5ms has passed to set all pins to low
        p.Out32(0x2040,0) #set trigger back to 0 again
except:
    def sendEEGTrig(trigger):
        print trigger
    pass

# Store info about the experiment session
expName= 'AudioStim'
expInfo = {'participant':'', 'session':'001','ScreenHz':'60',}
dlg = gui.DlgFromDict(dictionary=expInfo, title=expName)
if dlg.OK == False: core.quit()  # user pressed cancel
expInfo['date'] = data.getDateStr()  # add a simple timestamp
expInfo['expName'] = expName


# Setup files for saving
if not os.path.isdir('data'):
    os.makedirs('data')  # if this fails (e.g. permissions) we will get error
filename = 'data' + os.path.sep + '%s_%s_%s' %(expName, expInfo['participant'], expInfo['date'])
logFile = logging.LogFile(filename+'.log', level=logging.EXP)
logging.console.setLevel(logging.WARNING)  # this outputs to the screen, not a file

# An ExperimentHandler isn't essential but helps with data saving
thisExp = data.ExperimentHandler(name=expName, version='',
    extraInfo=expInfo, runtimeInfo=None,
    originPath=None,
    savePickle=True, saveWideText=True,
    dataFileName=filename)

# Setup the Window
win = visual.Window(size=(1920, 1080), fullscr=True, screen=0, allowGUI=False, allowStencil=False,
    monitor='testMonitor', color=[0,0,0], colorSpace='rgb')

win.setMouseVisible(False)

ScreenHz =np.int(expInfo['ScreenHz'])

datFile=open('/home/custine/Desktop/Experiments/Scripts/data'+os.path.sep+'%s_%s_dat_%s.txt'%(expInfo['expName'],expInfo['participant'],expInfo['date']),'w')
datFile.write('Subject\tTrial\tStim\tecode\tisi\tstimDur\ttiming\tjoyRT\tScreenHz\n')

## Joystick button for recording button press
##joyButtonNum=2   # so number 3 on the gamepad

# store frame rate of monitor if we can measure it successfully
expInfo['frameRate']=win._getActualFrameRate()
if expInfo['frameRate']!=None:
    frameDur = 1.0/round(expInfo['frameRate'])
else:
    frameDur = 1.0/60.0 # couldn't get a reliable measure so guess
    
# ######### EEG Event Codes
startCode=254         #DO NOT CHANGE THIS
pauseCode=255       #DO NOT CHANGE THIS
boundaryCode=252
##joystickPressed=251

# #Event codes defined in input file
# #Standard Tone = 200
# #Defiant Tone = 300 
# # Fixation To be defined 

# ############INITIALISE EXPERIMENT COMPONENTS###############

#Sound files path 
soundPath = "/home/custine/Desktop/Experiments/tones" #Do not include '/' in the end

# Initialize components for instructions and end of experiment
pressScr = visual.TextStim(win=win, ori=0, name='pressScr',
    text='PRESS ANY BUTTON TO BEGIN.',    font='Arial',
    pos=[0, 0], height=0.1, wrapWidth=None,
    color='yellow', opacity=1,
    depth=0.0,antialias=False)
endtxt = visual.TextStim(win=win, ori=0, name='endtxt',
    text='END OF EXPERIMENT\n\nThanks for participating!', font='Arial',
    pos=[0, 0], height=0.1, wrapWidth=None,
    color='white', colorSpace='rgb', opacity=1,
    depth=0.0)

# Initialize components for Routine "trial"
trialClock = core.Clock()
##sound_a = sound.Sound(u'440', secs=3.0)
##sound_a.setVolume(1)
##image = visual.ImageStim(win=win, name='image',
##    image=u'/home/custine/Desktop/Experiments/data/red.jpeg', mask=None,
##    ori=0, pos=[0, 0], size=[0.5, 0.5],
##    color=[1,1,1], colorSpace=u'rgb', opacity=1,
##    texRes=128, interpolate=True, depth=-1.0)
isiScr = visual.TextStim(win=win, ori=0, name='isiScr',
    text=None,    font=u'Arial',
    pos=[0, 0], height=0.1, wrapWidth=None,
    color=u'white', colorSpace=u'rgb', opacity=1,
    depth=-1.0)
textScr = visual.TextStim(win=win, ori=0, name='text',
    text=None,    font=u'Arial',
    pos=[0, 0], height=0.1, wrapWidth=None,
    color=1.0, colorSpace=u'rgb', opacity=1,
    depth=0.0)
breakScr = visual.TextStim(win=win, ori=0, name='text',
    text='TAKE A BREAK.\n\npress any key to continue',    font=u'Arial',
    pos=[0, 0], height=0.1, wrapWidth=None,
    color=1.0, colorSpace=u'rgb', opacity=1,
    depth=0.0)
pauseScr=visual.TextStim(win=win, ori=0, name='pauseScr',
        text=u'PAUSED',
        font=u'Arial',
        pos=[0, 0], height=0.1,wrapWidth=None,
        color=u'red', colorSpace=u'rgb', opacity=1,
        depth=0.0)

# ############ EXPERIMENT TIMING in frames
# all ISIs 400 ms
# all tones 300ms

# Create some handy timers
globalClock = core.Clock()  # to track the time since experiment started
routineTimer = core.CountdownTimer()  # to track time remaining of each (non-slip) routine 

# #### EEG/MEG Trigger 
sendEEGTrig(startCode)
core.wait(0.005)
sendEEGTrig(boundaryCode)

# set up handler to look after randomisation of conditions etc
trials = data.TrialHandler(nReps=1, method=u'sequential',
    extraInfo=expInfo, originPath=None,
    trialList=data.importConditions('psychopytest.csv'),
    seed=None, name='trials')
thisExp.addLoop(trials)  # add the loop to the experiment
thisTrial = trials.trialList[0]  # so we can initialise stimuli with some values

# abbreviate parameter names if possible (e.g. rgb=thisTrial.rgb)
if thisTrial != None:
    for paramName in thisTrial.keys():
        exec(paramName + '= thisTrial.' + paramName)

#update component parameters for each repeat
event.clearEvents()
##joyRT=[]
itemTime = 0.0
##TEst
sound_1 = sound.Sound(u'/home/custine/Desktop/Experiments/tones/tone_400Hz.wav')
##sound_1.play()

for thisTrial in trials:
    currentLoop = trials
    if thisTrial != None:
        for paramName in thisTrial.keys():
            exec(paramName + '= thisTrial.' + paramName)

#    if trials.thisTrialN==0: takerest=trials.trialList[0]
#    else: takerest=trials.trialList[trials.thisTrialN-1]

#    if trials.thisTrialN!=0 and thisTrial.block!=takerest['block']:          #display break for each block
#        breakScr.draw()
#        sendEEGTrig(boundaryCode)
#        core.wait(0.005)
#        sendEEGTrig(pauseCode)
#        win.flip()
#        if 'escape' in event.getKeys():
#            core.quit()
#        while sum(joy.getAllButtons())==0: # wait until a button is pressed on the gamepad to continue
#           breakScr.draw()
#           if 'escape' in event.getKeys():
#                core.quit()
#           event.clearEvents()#do this each frame to avoid getting clogged with mouse events
#           win.flip()#redraw the buffer
#
#        sendEEGTrig(startCode)
#        core.wait(0.005)
#        sendEEGTrig(boundaryCode)

    event.clearEvents()
##    joyRT=[]

    print thisTrial.stim
    soundfile_path = '%s'%(soundPath)+os.path.sep+'%s'%(thisTrial.stim)
    soundfile_path = os.path.join(soundPath, thisTrial.stim)
    soundfile_path_str= str(soundfile_path)
    #soundfile_path = os.path.join("/home/custine/Desktop/Experiments/tones/", thisTrial.stim)
    print soundfile_path
#    
# ###### #####STANDARD TONE STIM  #########################################################################3
    if thisTrial.stimDur==-1: 
        ##imageScr.setImage('%s'%(imagePath)+os.path.sep+'%s'%(thisTrial.stim)) ################################
        sound_1 = sound.SoundPygame(value = u'/home/custine/Desktop/Experiments/tones/tone_400Hz.wav') # so that sound_1 takes new values each trial
        #sound_1 = sound.Sound(soundfile_path)
        sound_1.setVolume(.5)
        #sound_1.play()
        isiStart = 0
        isiEnd = int(np.round((thisTrial.isiDur/1000)*ScreenHz))
        stimStart=isiEnd
        stimEnd = stimStart+ int(np.round((thisTrial.stimDur/1000)*ScreenHz))
        
        #------Prepare to start Routine "trial"-------
        t = 0
        trialClock.reset()  # clock 
        frameN = -1
        routineTimer.add(1.000000)
        # update component parameters for each repeat
        # keep track of which components have finished
        trialComponents = []
        trialComponents.append(sound_1)
        trialComponents.append(isiScr)
        pausePress=[]
        resumePress=[]
        trialComponents.append(pauseScr)
        pauseKey = event.BuilderKeyResponse() #create an object of type KeyResponse
        pauseKey.status=NOT_STARTED
        resumeKey = event.BuilderKeyResponse() #create an object of type KeyResponse
        resumeKey.status=NOT_STARTED
        for thisComponent in trialComponents:
            if hasattr(thisComponent, 'status'):
                thisComponent.status = NOT_STARTED

        #-------Start Routine "trial"-------
        continueRoutine = True
        while continueRoutine and routineTimer.getTime() > 0:
            # get current time
            t = trialClock.getTime()
            frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
            
            # update/draw components on each frame
            event.clearEvents(eventType='mouse')
            
            # check for quit (the [Esc] key)
            if event.getKeys(["escape"]):
                sendEEGTrig(boundaryCode)
                core.wait(0.005)
                sendEEGTrig(pauseCode)
                core.quit()

#            #*pauseKey* updates
#            if frameN>=0 and pauseKey.status==NOT_STARTED:
#                #keep track of start time/frame for later
#                pauseKey.tStart=t#underestimates by a little under one frame
#                pauseKey.frameNStart=frameN#exact frame index
#                pauseKey.status=STARTED
#                #keyboard checking is just starting
#                event.clearEvents()
#            elif pauseKey.status==STARTED and joy.getButton(joyButtonNum):
#                pauseKey.status=FINISHED
#            if pauseKey.status==STARTED:#only update if being drawn
#                pausePress = event.getKeys(keyList=['p'])
#                if len(pausePress)>0:
#                    sendEEGTrig(boundaryCode)
#                    core.wait(0.005)
#                    sendEEGTrig(pauseCode)
#                    pauseKey.status=FINISHED
                    
#            # *isiScr* updates
#            if frameN >= isiStart and isiScr.status == NOT_STARTED:
#                # keep track of start time/frame for later
#                isiScr.tStart = t  # underestimates by a little under one frame
#                isiScr.frameNStart = frameN  # exact frame index
#                isiScr.setAutoDraw(True)
#            elif isiScr.status==NOT_STARTED and len(pausePress)>0:
#                isiScr.setAutoDraw(False)
#                isiScr.status=FINISHED
#            elif isiScr.status == STARTED and frameN >= isiEnd:
#                isiScr.setAutoDraw(False)
#                isiScr.status=FINISHED
#            elif isiScr.status == STARTED and len(pausePress)>0:
#                isiScr.setAutoDraw(False)
#                isiScr.status=FINISHED
                
            # *stim* updates
            if frameN==stimStart and sound_1.status == NOT_STARTED:
                # keep track of start time/frame for later
                sound_1.tStart = t  # underestimates by a little under one frame
                sound_1.frameNStart = frameN  # exact frame index
                sound_1.play()  # start the sound (it finishes automatically)
            elif sound_1.status == STARTED and t >= (2):
                sound_1.stop()  # stop the sound (if longer than duration
                sound_1.status=FINISHED
                continueRoutine=False
#            elif sound_1.status==NOT_STARTED and len(pausePress)>0:
#               sound_1.status=FINISHED
#            elif sound_1.status==STARTED and len(pausePress)>0:
#                sound_1.stop()
#                sound_1.status=FINISHED
#                elif imageScr.status == STARTED and len(pausePress)==0 and joy.getButton(joyButtonNum):
#                    imageScr.setAutoDraw(False)
#                    imageScr.status=FINISHED
#                    continueRoutine=False

#            #*resumeKey* updates
#            if resumeKey.status==NOT_STARTED and len(pausePress)>0:
#                #keep track of start time/frame for later
#                resumeKey.tStart=t#underestimates by a little under one frame
#                resumeKey.frameNStart=frameN#exact frame index
#                resumeKey.status=STARTED
#                #keyboard checking is just starting
#                event.clearEvents()
#            if resumeKey.status==NOT_STARTED and joy.getButton(joyButtonNum):
#                resumeKey.status=FINISHED
#            if resumeKey.status==STARTED:#only update if being drawn
#                resumePress = event.getKeys(keyList=['r'])
#                if len(resumePress)>0:#at least one key was pressed
#                    sendEEGTrig(startCode) #start recording EEG again and mark boundary
#                    core.wait(0.05)
#                    sendEEGTrig(boundaryCode)
#                    resumeKey.status=FINISHED
#                    continueRoutine=False
            
            # check if all components have finished
            if not continueRoutine:  # a component has requested a forced-end of Routine
                routineTimer.reset()  # if we abort early the non-slip timer needs reset
                break
            continueRoutine = False  # will revert to True if at least one component still running
            for thisComponent in trialComponents:
                if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                    continueRoutine = True
                    break  # at least one component has not yet finished
            
            # check for quit (the [Esc] key)
            if event.getKeys(["escape"]):
                core.quit()
            
            # refresh the screen
            if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                win.flip()
                #send EEG trigger codes when appropriate
                if hasattr(textScr, 'frameNStart') and frameN==textScr.frameNStart and frameN>=isiEnd and pauseScr.status==NOT_STARTED:
                    sendEEGTrig(thisTrial.ecode)
                    itemTime=globalClock.getTime()

# ###### #####DEFIANT TONE STIM  ##########################################################################
    elif thisTrial.stimDur == -2: 
       ##imageScr.setImage('%s'%(imagePath)+os.path.sep+'%s'%(thisTrial.stim)) ################################
        sound_1 = sound.SoundPygame(value = u'/home/custine/Desktop/Experiments/tones/tone_250Hz.wav') # so that sound_1 takes new values each trial
        #sound_1 = sound.Sound(u'/home/custine/Desktop/Experiments/tones/tone_400Hz.wav')
        sound_1.setVolume(.5)
        #sound_1.play()
        isiStart = 0
        isiEnd = int(np.round((thisTrial.isiDur/1000)*ScreenHz))
        stimStart=isiEnd
        stimEnd = stimStart+ int(np.round((thisTrial.stimDur/1000)*ScreenHz))
        
        #------Prepare to start Routine "trial"-------
        t = 0
        trialClock.reset()  # clock 
        frameN = -1
        routineTimer.add(1.000000)
        # update component parameters for each repeat
        # keep track of which components have finished
        trialComponents = []
        trialComponents.append(sound_1)
        trialComponents.append(isiScr)
        pausePress=[]
        resumePress=[]
        trialComponents.append(pauseScr)
        pauseKey = event.BuilderKeyResponse() #create an object of type KeyResponse
        pauseKey.status=NOT_STARTED
        resumeKey = event.BuilderKeyResponse() #create an object of type KeyResponse
        resumeKey.status=NOT_STARTED
        for thisComponent in trialComponents:
            if hasattr(thisComponent, 'status'):
                thisComponent.status = NOT_STARTED

        #-------Start Routine "trial"-------
        continueRoutine = True
        while continueRoutine and routineTimer.getTime() > 0:
            # get current time
            t = trialClock.getTime()
            frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
            
            # update/draw components on each frame
            event.clearEvents(eventType='mouse')
            
            # check for quit (the [Esc] key)
            if event.getKeys(["escape"]):
                sendEEGTrig(boundaryCode)
                core.wait(0.005)
                sendEEGTrig(pauseCode)
                core.quit()

#            #*pauseKey* updates
#            if frameN>=0 and pauseKey.status==NOT_STARTED:
#                #keep track of start time/frame for later
#                pauseKey.tStart=t#underestimates by a little under one frame
#                pauseKey.frameNStart=frameN#exact frame index
#                pauseKey.status=STARTED
#                #keyboard checking is just starting
#                event.clearEvents()
#            elif pauseKey.status==STARTED and joy.getButton(joyButtonNum):
#                pauseKey.status=FINISHED
#            if pauseKey.status==STARTED:#only update if being drawn
#                pausePress = event.getKeys(keyList=['p'])
#                if len(pausePress)>0:
#                    sendEEGTrig(boundaryCode)
#                    core.wait(0.005)
#                    sendEEGTrig(pauseCode)
#                    pauseKey.status=FINISHED
                    
#            # *isiScr* updates
#            if frameN >= isiStart and isiScr.status == NOT_STARTED:
#                # keep track of start time/frame for later
#                isiScr.tStart = t  # underestimates by a little under one frame
#                isiScr.frameNStart = frameN  # exact frame index
#                isiScr.setAutoDraw(True)
#            elif isiScr.status==NOT_STARTED and len(pausePress)>0:
#                isiScr.setAutoDraw(False)
#                isiScr.status=FINISHED
#            elif isiScr.status == STARTED and frameN >= isiEnd:
#                isiScr.setAutoDraw(False)
#                isiScr.status=FINISHED
#            elif isiScr.status == STARTED and len(pausePress)>0:
#                isiScr.setAutoDraw(False)
#                isiScr.status=FINISHED
                
            # *stim* updates
            if frameN==stimStart and sound_1.status == NOT_STARTED:
                # keep track of start time/frame for later
                sound_1.tStart = t  # underestimates by a little under one frame
                sound_1.frameNStart = frameN  # exact frame index
                sound_1.play()  # start the sound (it finishes automatically)
            elif sound_1.status == STARTED and t >= (2):
                sound_1.stop()  # stop the sound (if longer than duration
                sound_1.status=FINISHED
                continueRoutine=False
#            elif sound_1.status==NOT_STARTED and len(pausePress)>0:
#               sound_1.status=FINISHED
#            elif sound_1.status==STARTED and len(pausePress)>0:
#                sound_1.stop()
#                sound_1.status=FINISHED
#                elif imageScr.status == STARTED and len(pausePress)==0 and joy.getButton(joyButtonNum):
#                    imageScr.setAutoDraw(False)
#                    imageScr.status=FINISHED
#                    continueRoutine=False

#            #*resumeKey* updates
#            if resumeKey.status==NOT_STARTED and len(pausePress)>0:
#                #keep track of start time/frame for later
#                resumeKey.tStart=t#underestimates by a little under one frame
#                resumeKey.frameNStart=frameN#exact frame index
#                resumeKey.status=STARTED
#                #keyboard checking is just starting
#                event.clearEvents()
#            if resumeKey.status==NOT_STARTED and joy.getButton(joyButtonNum):
#                resumeKey.status=FINISHED
#            if resumeKey.status==STARTED:#only update if being drawn
#                resumePress = event.getKeys(keyList=['r'])
#                if len(resumePress)>0:#at least one key was pressed
#                    sendEEGTrig(startCode) #start recording EEG again and mark boundary
#                    core.wait(0.05)
#                    sendEEGTrig(boundaryCode)
#                    resumeKey.status=FINISHED
#                    continueRoutine=False
            
            # check if all components have finished
            if not continueRoutine:  # a component has requested a forced-end of Routine
                routineTimer.reset()  # if we abort early the non-slip timer needs reset
                break
            continueRoutine = False  # will revert to True if at least one component still running
            for thisComponent in trialComponents:
                if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                    continueRoutine = True
                    break  # at least one component has not yet finished
            
            # check for quit (the [Esc] key)
            if event.getKeys(["escape"]):
                core.quit()
            
            # refresh the screen
            if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                win.flip()
                #send EEG trigger codes when appropriate
                if hasattr(textScr, 'frameNStart') and frameN==textScr.frameNStart and frameN>=isiEnd and pauseScr.status==NOT_STARTED:
                    sendEEGTrig(thisTrial.ecode)
                    itemTime=globalClock.getTime()
        
 # ################################################################################################
    trials.addData('timing',itemTime)

    #-------Ending Routine "trial"-------
    for thisComponent in trialComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
                
    #push to dat File
    datFile.write('%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n'%(expInfo['participant'],trials.thisTrialN+1,thisTrial.stim,thisTrial.ecode,thisTrial.isiDur,thisTrial.stimDur,itemTime,expInfo['ScreenHz']))
    #completed 1 repeats of 'trials' loop
    
datFile.close()

#get names of stimulus parameters
if trials.trialList in ([], [None], None):  params=[]
else:  params = trials.trialList[0].keys()
#save data for this loop
trials.saveAsPickle(filename+'trials')
trials.saveAsExcel(filename+'.xlsx', sheetName='trials',
    stimOut=params,
    dataOut=['n','all_mean','all_std', 'all_raw'])
    

# EXPERIMENT END SCREEN
endtxt.draw()
win.flip()
core.wait(3)

#Shutting down:
win.close()
core.quit()
