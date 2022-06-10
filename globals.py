# -*- coding: utf-8 -*-
#!/usr/bin/env python3

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

    global mediaorder
    mediaorder = [None, None, None]

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
    mediaDelay = 3
