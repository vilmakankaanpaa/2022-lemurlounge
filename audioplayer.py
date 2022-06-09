#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from mpyg321.mpyg321 import MPyg321Player, PlayerStatus
from time import sleep

import configs

class AudioPlayer(MPyg321Player):

    # Player status values:
    # 0 - ready
    # 1 - playing
    # 2 - paused
    # 3 - stopped
    # 4 - has quit

    # use self.stop(), self.pause()

    def is_playing(self):

        if self.status == 1: # playing
            return True
        else:
            return False


    def has_quit(self):

        if self.status == 4: # has quit
            return True
        else:
            return False


    def play_audio(self, file):

        # TODO: cannot be paused with this system
        #if self.status == 2: # paused
        #    self.resume()
        #elif self.status != 1: # ready (0) or stopped (3)
            # currently not paused and not playing -> start
        self.play_song(file, loop=True)
        #else:
        #    pass

    #def pause(self):
    #    self.pause()

    #def stop(self):
    #    self.stop()
