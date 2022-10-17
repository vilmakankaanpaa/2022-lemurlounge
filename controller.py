#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from time import sleep
from datetime import datetime
from filemanager import printlog, get_directory_for_recordings
from sensors import Sensors
from audioplayer import AudioPlayer
import globals
import configs


class Controller():

    def __init__(self, logger, camera, mic):

        self.monkeyInside = False
        self.switchesOpen = [False, False, False]
        self.audioPlaying = False
        self.starttime = None
        self.endtime = None
        self.delay = globals.mediaDelay # seconds

        self.sensors = Sensors()
        self.sensorVolts = [0,0,0]

        self.logger = logger
        self.camera = camera
        self.mic = mic

        self.audioFilePath = configs.audiopath + globals.mediafile + '.mp3'
        globals.audioPlayer = AudioPlayer()
        globals.audioPlayer.load_audio(self.audioFilePath)

        globals.videoPlayer = None


    def delayPassed(self):
    # Check if delay for starting/stopping/changing media has passed

        playtime = round((datetime.now() - self.starttime).total_seconds(),2)
        if playtime > self.delay:
            return True
        else:
            return False


    def triggerAudioChange(self):

        if globals.usingAudio:
            self.audioFilePath = configs.audiopath + globals.mediafile + '.mp3'
            globals.audioPlayer.load_audio(self.audioFilePath)

    def turnOn(self):
    # Turn media on

        if self.logger.ix_period == None:
            # First interaction of the new interactive period
            self.logger.start_ixPeriod()

        self.starttime = datetime.now()
        self.endtime = None

        self.audioPlaying = True

        # New interaction starts whenever new media turns on
        self.logger.log_interaction_start(self.switchesOpen, self.sensorVolts)

        # Start recording
        if globals.recordingOn and not self.camera.is_recording:
            try:
                file = self.logger.new_recording_name()
                directory = get_directory_for_recordings()
                self.camera.start_recording(file, directory)
                self.mic.record(file)
                printlog('Controller','Starting to record.')

            except Exception as e:
                printlog('Controller','ERROR: Could not start recording cam. {}'.format(type(e).__name__, e))
                self.logger.log_system_status('Controller','ERROR: Could not start recording. {}'.format(type(e).__name__, e))

        sleep(0.2)

        if globals.usingAudio:
            printlog('Controller','Playing audio {}.'.format(globals.mediafile))
            try:
                if globals.audioPlayer.has_quit():
                    globals.audioPlayer = AudioPlayer()
                    globals.audioPlayer.load_audio(self.audioFilePath)
                globals.audioPlayer.play_audio()

            except Exception as e:
                printlog('Controller','ERROR: Could not start audio. {}'.format(type(e).__name__, e))
                self.logger.log_system_status('Controller','ERROR: Could not start audio. {}'.format(type(e).__name__, e))

        else:
            # no stimulus
            return

        sleep(0.1)


    def turnOff(self):
    # Turn media off

        if globals.audioPlayer.is_playing():
            printlog('Controller','Turning audio off.')
            globals.audioPlayer.pause_audio()

        self.endtime = datetime.now()
        self.logger.log_interaction_end(self.endtime)
        printlog('Controller','Interaction ended.')

        self.starttime = None
        self.audioPlaying = False

        sleep(0.2)


    def update(self):
    # Update the status of the sensor readings by checking them all.

        self.switchesOpen, mostRecentOpen, anyChanged, self.sensorVolts = self.sensors.update()

        if not self.monkeyInside and any(self.switchesOpen):
            printlog('Main','Monkey came in!')
            self.monkeyInside = True

        elif self.monkeyInside and not any(self.switchesOpen):
            printlog('Main','All monkeys left. :(')
            self.monkeyInside = False


    def manageMedia(self):

        # 1. Sensors fired but stimuli not playing --> Start
        # 2. Stimuli playing but sensors not fired
            # 2.1. Delay has not passed --> keep playing
            # 2.2. Delay passed --> stop playing

        try:

            if not self.audioPlaying:
                # media is not currently playing but switches are open
                 if any(self.switchesOpen):
                    # Turn media on
                    self.turnOn()
            else:
                # media is currently playing
                if not any(self.switchesOpen):
                    if self.delayPassed():
                        self.turnOff()
                else:
                    # the media is playing and switches are open, don't turn off
                    pass

        except Exception as e:
            printlog('Controller','ERROR with updating media: {}'.format(type(e).__name__, e))
            self.logger.log_system_status('Controller','ERROR with updating media: {}'.format(type(e).__name__, e))
