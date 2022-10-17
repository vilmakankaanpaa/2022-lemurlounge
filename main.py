# -*- coding: utf-8 -*-
#!/usr/bin/env python3

import os
import sys
from time import sleep
from datetime import datetime, date

# Local sources
from filemanager import printlog, log_local
from logger import Logger
from camera import Camera
from microphone import Microphone
from controller import Controller
import configs
import globals

sys.excepthook = sys.__excepthook__


def update_mediafile(controller, logger):

  printlog('Main','Checking date for switching media')
  
  today = date.today().isoformat()
  datesDict = globals.datesForMediaChange
  
  media = globals.mediafile
  if today in datesDict:
    media = datesDict[today]

  if globals.mediafile != media:
    logger.log_system_status('Main', 'Media change: from {} to {}.'.format(globals.mediafile, media))
    printlog('Main','Media change: from {} to {}.'.format(globals.mediafile, media))
    globals.mediafile = media

    if media == None:
        globals.usingAudio = False
    elif media != None:
        globals.usingAudio = True

    controller.triggerAudioChange()


if __name__ == "__main__":

    globals.init()

    printlog('Main',datetime.isoformat(datetime.now()))
    globals.pid = os.getpid()

    start = datetime.now()
    while not os.path.isdir(configs.external_disk):
      printlog('Main','Usb not found yet, sleeping')
      sleep(10)
      if (datetime.now()-start).total_seconds() > 180:
        printlog('Main','USB still not found after 3 minutes, exiting')
        exit(0)

    printlog('Main','Starting up monkeytunnel..')


    logger = Logger()
    camera = Camera()
    mic = Microphone()

    mediaUpdateTimer = datetime.now()

    lastActivity = datetime.now()
    activated = False

    try:
        controller = Controller(logger, camera, mic)
        update_mediafile(controller, logger) # pick the correct media to use

        logger.log_program_run_info()
        logger.log_system_status('Main','Tunnel started.')

        printlog('Main','Ready for use!')

        while True:

            if (datetime.now() - mediaUpdateTimer).total_seconds() / 60 > 20: 
              # check every 20 minutes
              update_mediafile(controller, logger)
              mediaUpdateTimer = datetime.now()

              while(datetime.now().hour >= 18 or datetime.now().hour < 6):
                printlog('Main','Time is {}, going to sleep for an hour.'.format(datetime.now().hour))
                logger.log_system_status('Main','Time is {}, going to sleep for an hour.'.format(datetime.now().hour))
                sleep(60*60) # sleep for an hour at a time

            controller.update() # Checks if lemur is inside.
            controller.manageMedia() # Start/stop audio. Log the interaction details.

            if logger.ix_id == None:
                activated = False
            else:
                activated = True

            if controller.endtime != None:
                lastActivity = controller.endtime

            # Stop interactive period and recording after certain time since last interaction
            if not activated:

                timeSinceActivity = round((datetime.now() - lastActivity).total_seconds(),2)

                if timeSinceActivity > globals.periodDelay:
                    # delay has passed

                    logger.end_ixPeriod()

                    if globals.recordingOn and camera.is_recording:
                        try:
                            camera.stop_recording()
                            mic.stop()
                            sleep(0.2)
                            printlog('Main','Stopping to record, time since last interaction end: {}.'.format(timeSinceActivity))
                        except Exception as e:
                            logger.log_system_status('Main','Error when trying to stop camera or mic from recording: {}'.format(type(e).__name__, e))


            timeSinceIx = (datetime.now() - lastActivity).total_seconds() / 60

            sleep(0.2)


    except KeyboardInterrupt:
        printlog('Main','Exiting, KeyboardInterrupt')

    finally:

        try:
            logger.log_system_status('Exit','Exiting program.')
        except:
            pass

        if camera.is_recording:
            printlog('Exit','Stopping camera recording.')
            camera.stop_recording()
        
        camera.close()
        
        if mic.is_recording:
            printlog('Exit','Stopping mic recording.')
            mic.stop()

        if globals.videoPlayer != None:
            printlog('Exit','Stopping video.')
            globals.videoPlayer.stop_video()

        if globals.audioPlayer.is_playing():
            printlog('Exit','Stopping audio.')
            globals.audioPlayer.stop_audio()

        ix_data = logger.ix_tempdata
        if len(ix_data) != 0:
            printlog('Exit','Logging ix data to csv.')
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            file = timestamp + '_ix_backup.csv'
            for row in ix_data:
              log_local(ix_data, sheet=file)
