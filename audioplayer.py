#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#from mpyg321.mpyg321 import MPyg321Player, PlayerStatusx
from pygame import mixer
from time import sleep

#class AudioPlayer(MPyg321Player):
class AudioPlayer:

    # Player status values:
    # 0 - ready
    # 1 - playing
    # 2 - paused
    # 3 - stopped
    # 4 - has quit

    # use self.stop(), self.pause()

    mixer.init()

    def load_audio(self, audioFile):
      mixer.music.load(audioFile)
      mixer.music.set_volume(0.7)
      mixer.music.play(loops=-1)
      mixer.music.pause()

    def change_audio(self, audioFile):
      mixer.music.unload()
      self.load_audio(audioFile)

    def play_audio(self):
      mixer.music.unpause()

    def stop_audio(self):
      mixer.music.pause()

    def is_playing(self):

      if mixer.music.get_busy() == 0:
        return False
      
      return True

    #     if self.status == 1: # playing
    #         return True
    #     else:
    #         return False


    def has_quit(self):
      
      if mixer.get_init() == None:
        return True
      
      return False

    #     if self.status == 4: # has quit
    #         return True
    #     else:
    #         return False


    #def play_audio(self, file):

    #     # TODO: cannot be paused with this system
    #     #if self.status == 2: # paused
    #     #    self.resume()
    #     #elif self.status != 1: # ready (0) or stopped (3)
    #         # currently not paused and not playing -> start
    #     self.play_song(file, loop=True)
    #     #else:
    #     #    pass

    # #def pause(self):
    # #    self.pause()

    # #def stop(self):
    # #    self.stop()
