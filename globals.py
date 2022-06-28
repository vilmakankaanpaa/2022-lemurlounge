# -*- coding: utf-8 -*-
#!/usr/bin/env python3

from datetime import datetime
import configs

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

    # Conditions: 4 audio conditions (white noise included)
    global mediafile
    today = datetime.now().minute #datetime.now().date()

    # Dates are start date of the condition
    # for testing use minutes:
    period1 = 1 # datetime.date.fromisoformat(configs.period1Date) where e.g. congis.period1Date = '2022-06-31'
    period2 = 3
    period3 = 5
    period4 = 7

    global periodDates 
    # periodDates = [
    #   datetime.date.fromisoformat(configs.period1Date),
    #   datetime.date.fromisoformat(configs.period2Date),
    #   datetime.date.fromisoformat(configs.period3Date),
    #   datetime.date.fromisoformat(configs.period4Date)
    # ]
    periodDates = [
      period1,period2,period3,period4
    ]
    
    if today >= period4:
      mediafile = configs.audio4
    elif today >= period3:
      mediafile = configs.audio3
    elif today >= period2:
      mediafile = configs.audio2
    elif today >= period1:
      mediafile = configs.audio1
    else:
      mediafile = None

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
