#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from time import sleep
from datetime import datetime
from filemanager import printlog, get_directory_for_recordings
from ir_sensors import Sensors
from audioplayer import AudioPlayer
from videoplayer import VideoPlayer
import globals
import configs


class Switches():

    def __init__(self, logger, camera, mic):

        self.monkeyInside = False
        self.switchesOpen = [False, False, False]
        self.switchPlaying = None
        self.queue = None # Use the queue to store the switch number?
        #self.second_queue = None # for rare cases of X is changed to Y but X is still kept open: when Y closes, X should be put back
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

      self.audioFilePath = configs.audiopath + globals.mediafile + '.mp3'
      globals.audioPlayer.load_audio(self.audioFilePath)

    def turnOn(self):
    # Turn media on

        if self.logger.ix_period == None:
            # First interaction of the new interactive period
            self.logger.start_ixPeriod()

        self.starttime = datetime.now()
        self.endtime = None

        if self.queue != None:
            self.switchPlaying = self.queue
            self.queue = None
        # elif self.second_queue != None:
        #     self.switchPlaying = self.second_queue
        #     self.second_queue = None
        else:
            # Media switching too fast and the system variables are maybe not up to date
            return

        # New interaction starts whenever new media turns on
        self.logger.log_interaction_start(self.switchPlaying, self.switchesOpen, self.sensorVolts)
        printlog('Switches','Interaction started,')

        # Start recording
        if globals.recordingOn and not self.camera.is_recording:
            try:
                file = self.logger.new_recording_name()
                directory = get_directory_for_recordings()
                self.camera.start_recording(file, directory)
                self.mic.record(file)
                printlog('Switches','Starting to record.')

            except Exception as e:
                printlog('Switches','ERROR: Could not start recording cam. {}'.format(type(e).__name__, e))
                self.logger.log_system_status('Switches','ERROR: Could not start recording. {}'.format(type(e).__name__, e))

        sleep(0.2)

        #filename = globals.mediaorder[self.switchPlaying]
        # Just using one audio file at any one time

        if globals.usingAudio:
            printlog('Switches','Playing audio {}.'.format(globals.mediafile))
            try:
                if globals.audioPlayer.has_quit():
                    globals.audioPlayer = AudioPlayer()
                    globals.audioPlayer.load_audio(self.audioFilePath)
                globals.audioPlayer.play_audio()

            except Exception as e:
                printlog('Switches','ERROR: Could not start audio. {}'.format(type(e).__name__, e))
                self.logger.log_system_status('Switches','ERROR: Could not start audio. {}'.format(type(e).__name__, e))

        elif globals.usingVideo:
            printlog('Switches','Playing video {}.'.format(filename))
            filepath = configs.videopath + filename + '.mp4'

            try:
                globals.videoPlayer = VideoPlayer(filepath, globals.videoAudio)

            except Exception as e:
                printlog('Switches','ERROR: Could not start video. {}'.format(type(e).__name__, e))
                self.logger.log_system_status('Switches','ERROR: Could not start video. {}'.format(type(e).__name__, e))

        else:
            # no stimulus
            return

        sleep(0.1)


    def turnOff(self):
    # Turn media off

        if globals.audioPlayer.is_playing():
            printlog('Switches','Turning audio off.'.format(self.switchPlaying))
            globals.audioPlayer.stop_audio()

        if globals.videoPlayer != None:
            printlog('Switches','Turning video off.'.format(self.switchPlaying))
            if globals.videoPlayer.is_playing():
                globals.videoPlayer.stop_video()
                globals.videoPlayer = None

        self.endtime = datetime.now()
        self.logger.log_interaction_end(self.endtime)
        printlog('Switches','Interaction ended.')

        self.starttime = None
        self.switchPlaying = None

        sleep(0.2)


    # def changeSwitch(self):
    # # For cases when switch X is palying but the switch Y will be turned on.
    #     changedSwitch = self.switchPlaying
    #
    #     self.turnOff()
    #     self.turnOn()
    #
    #     if self.switchesOpen[changedSwitch]:
    #         # switch that was turned off is still open
    #         self.second_queue = changedSwitch


    def update(self):

        # Update the status of the sensor readings by checking them all.
        self.switchesOpen, mostRecentOpen, anyChanged, self.sensorVolts = self.sensors.update()

        if not self.monkeyInside and any(self.switchesOpen):
            printlog('Main','Monkey came in!')
            self.monkeyInside = True

        elif self.monkeyInside and not any(self.switchesOpen):
            printlog('Main','All monkeys left. :(')
            self.monkeyInside = False

        if mostRecentOpen != None:
            self.queue = mostRecentOpen

        # if self.queue != None:
        #     if self.switchesOpen[self.queue] != True:
        #         # Switch set in queue earlier is no longer open
        #         self.queue = None
        #
        # if mostRecentOpen != None:
        #     if mostRecentOpen != self.switchPlaying:
        #         # Set switch that was opened to the queue
        #         self.queue = mostRecentOpen


    def manageMedia(self):

        # 1. Sensors fired but stimuli not playing --> Start
        # 2. Stimuli playing but sensors not fired
            # 2.1. Delay has not passed --> keep playing
            # 2.2. Delay passed --> stop playing

        try:

            if self.switchPlaying == None:
                # media is not currently playing
                if self.queue != None:
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
            printlog('Switches','ERROR with updating media: {}'.format(type(e).__name__, e))
            self.logger.log_system_status('Switches','ERROR with updating media: {}'.format(type(e).__name__, e))


    # 1. Switch on queue but no switches playing media
    #       -> Turn on
    # 2. Switch on queue but it's already playing
    #       -> Do nothing / don't even add on the queue
    # 3. Switch on queue but another switch playing
    #       -> Wait until delay passed -> leave to queue or start playing
    # 4. No queue, delay passed, switch still open -> keep playing
    # 5. No queue (new switches), delay passed, switch closed; But a switch that was changed from previously is still open in second_queue. -> switch back to this switch.
    # 6. All switches closed but one is playing
    #       -> Check if delay has passed -> continue or stop playing
        # try:
        #
        #     if self.switchPlaying == None:
        #         # media is not currently playing
        #         if self.queue != None:
        #             # Turn new switch on
        #             self.turnOn()
        #     else:
        #         # media is currently playing
        #         if self.queue != None:
        #             if self.delayPassed():
        #                 self.changeSwitch()
        #         else:
        #             # queue is empty
        #             if not any(self.switchesOpen):
        #                 # all switches closed too
        #                 if self.delayPassed():
        #                     self.turnOff()
        #             else:
        #                 # either the switch currently playing is open or another one
        #                     # must be in second_queue
        #                 if not self.switchesOpen[self.switchPlaying]:
        #                     # the switch playing is not open anymore, but another switch is
        #                     if self.second_queue != None:
        #                         if self.delayPassed():
        #                             self.changeSwitch()
        #                     else:
        #                         # Weird case: no queue but something else than the current one playing is open.
        #                         # Just change to play the switch that is detected open.
        #                         printlog('Switches','Weird case: no queue but something else than the current one playing is open')
        #                         for i in range(0,len(self.switchesOpen)):
        #                             if self.switchPlaying == i:
        #                                 continue
        #                             if self.switchesOpen[i]:
        #                                 if self.delayPassed():
        #                                     self.second_queue = i
        #                                     self.changeSwitch()
        #                 else:
        #                     # the switch playing is still open, don't turn off
        #                     pass
        #
        # except Exception as e:
        #     printlog('Switches','ERROR with updating media: {}'.format(type(e).__name__, e))
        #     self.logger.log_system_status('Switches','ERROR with updating media: {}'.format(type(e).__name__, e))
