#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pygame import mixer
from time import sleep

class AudioPlayer:

    mixer.init()

    def load_audio(self, audioFile):
      mixer.music.load(audioFile)
      mixer.music.set_volume(1.0)
      mixer.music.play(loops=-1)
      mixer.music.pause()

    def play_audio(self):
      mixer.music.unpause()

    def stop_audio(self):
      mixer.music.pause()

    def is_playing(self):

      if mixer.music.get_busy() == 0:
        return False
      
      return True

    def has_quit(self):
      
      if mixer.get_init() == None:
        return True
      
      return False
