#!/usr/bin/env python
# -*- coding: utf-8 -*-


from omxplayer.player import OMXPlayer
from pathlib import Path
from time import sleep
from datetime import datetime


# https://python-omxplayer-wrapper.readthedocs.io/en/latest/omxplayer/#module-omxplayer.player
class VideoPlayer():

    def __init__(self, videoPath,  useVideoAudio):

        self.audio = useVideoAudio
        self.videoPath = videoPath
        """
        -o              audio output
        --no-osd        do not show status info on screen
        --aspect-mode   aspect of the video on screen
        --loop          continuously play the video
        """

        self.player = OMXPlayer(self.videoPath, args="-o alsa:hw:1,0 --no-osd --aspect-mode fill --loop")

        if not self.audio:
            self.player.mute()


    def is_playing(self):
        return self.player.is_playing()


    def stop_video(self):
        self.player.stop()
