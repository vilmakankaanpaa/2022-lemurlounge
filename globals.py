# -*- coding: utf-8 -*-
#!/usr/bin/env python3

from datetime import date
import configs
import os
import permutations

# Global variables
def init():

    # Manually changing the mode:
    # 1. Change testMode
    # 2. Change the mediaorder set in monkeytunnel.py

    # 0 = no-stimulus, 1 = audio, 2 = video, 3 = no stimulus but play black video
    global testMode
    testMode = 1

    global ordername
    ordername = 'None'

    # global mediaorder
    # mediaorder = [None, None, None]

    global usingAudio
    usingAudio = False
    global usingVideo
    usingVideo = False

    if testMode == 1:
        usingAudio = True
    elif testMode == 2:
        usingVideo = True
    elif testMode == 3: # No stimulus, but with black video
        usingVideo = True

    # Media changing daily
    global mediafile 
    mediafile = configs.audio4 # white noise as default

    if not os.path.exists('contentOrder.txt'):
      audios = [
        configs.audio1,
        configs.audio2,
        configs.audio3,
        configs.audio4,
        configs.audio5
        ]
      permutations.createNewOrder(
        content=audios, 
        startDate=date.today().isoformat(), 
        contentDays=7
        )
    
    # Dictionary for the dates when the media file is switched and the new value
    global datesForMediaChange
    datesForMediaChange = permutations.getDictionary()        

    # use camera to record interactions
    global recordingOn
    recordingOn = True

    # use the audio of the video files
    global videoAudio
    videoAudio = False

    global pid
    global modeSince

    global audioPlayer
    audioPlayer = None
    global videoPlayer
    videoPlayer = None

    # in practice, delays are about 1 second longer because of sleep times during code
    global periodDelay
    periodDelay = 3 # seconds, delay to stop interactive period and recording after interactions
    global mediaDelay
    mediaDelay = 1
