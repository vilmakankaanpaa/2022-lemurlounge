# -*- coding: utf-8 -*-
#!/usr/bin/env python3

import configs
import os
import permutations

def init():

    global usingUSB
    usingUSB = True

    global usingAudio
    usingAudio = True

    global mediafile
    mediafile = 'whitenoise'

    if not os.path.exists('/home/pi/lemur-audio-player/contentorder.txt'):
      audios = [
        configs.audio1,
        configs.audio2,
        configs.audio3,
        configs.audio4,
        configs.audio5,
        configs.audio6
        ]
      permutations.newOrder(
        content=audios,
        startDate='2022-10-29', # YYYY-MM-DD
        occurrences=10,
        cycle=1
        )

    # Dictionary for the dates when the media file is switched and the new value
    global datesForMediaChange
    datesForMediaChange = permutations.getDictionary()

    # use camera to record interactions
    global recordingOn
    recordingOn = True

    global pid
    global modeSince

    global audioPlayer
    audioPlayer = None

    # in practice, delays are about 1 second longer because of sleep times during code
    global periodDelay
    periodDelay = 3 # seconds, delay to stop interactive period and recording after interactions
    global mediaDelay
    mediaDelay = 1
