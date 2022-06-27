# -*- coding: utf-8 -*-
#!/usr/bin/env python3

import os
import sys
#import RPi.GPIO as GPIO
from time import sleep
from datetime import datetime #, date, time
#import random

# Local sources
from filemanager import check_disk_space, printlog, get_directory_for_recordings, log_local
from logger import Logger
from camera import Camera
from microphone import Microphone
from switches import Switches
import configs
import globals
#from ir_sensors import Sensors

sys.excepthook = sys.__excepthook__


# def ensure_disk_space(logger):

#     directory = get_directory_for_recordings()
#     # TODO: don't depend on the given directory
#     if directory == configs.RECORDINGS_PATH:
#         # Path is to the USB

#         freeSpace = check_disk_space(configs.external_disk)
#         logger.log_system_status('Main','Directory {}, free: {}'.format(directory, freeSpace))

#         if freeSpace < 0.04: # this is ca. 1.1/28.0 GB of the USB stick left
#             # if space is scarce, we need to upload some files ASAP
#             logger.log_system_status('Main','Disk space on USB getting small! Uploading files already.')
#             # But let's not upload all in order not to disturb
#             # the functioning of the tunnel for too long..
#             logger.upload_recordings(max_nof_uploads=5)

#     elif directory == configs.RECORDINGS_PATH_backup:
#         # PATH to local directory

#         logger.log_system_status('Main','Issue: Camera is recording to local folder.')
#         freeSpace = check_disk_space(configs.root)
#         printlog('Main','Directory {}, free: {}'.format(directory, freeSpace))
#         if freeSpace < 0.10: # 10% of the ca. 17 GB of free space on Pi
#             logger.log_system_status('Main','Disk space on Pi getting small! Uploading files already.')
#             # Pi is so small that we just need them all out.
#             logger.upload_recordings()
#     else:
#         pass


if __name__ == "__main__":

    globals.init()

    printlog('Main',datetime.isoformat(datetime.now()))
    globals.pid = os.getpid()

    printlog('Main','Starting up monkeytunnel..')

    if globals.testMode == 1:
        globals.mediafile = configs.audio1
    else:
        globals.mediafile = None

    # if globals.testMode == 1:
    #     globals.mediaorder = [configs.audio1,configs.audio2,configs.audio3]
    #
    # elif globals.testMode == 2:
    #     globals.mediaorder = [configs.video2,configs.video3,configs.video1]
    #
    # elif globals.testMode == 3:
    #     globals.mediaorder = [configs.video5,configs.video5,configs.video5]
    # else:
    #     globals.mediaorder = [None, None, None]

    # printlog('Main','Mediaorder: {}.'.format(globals.mediaorder))

    logger = Logger()
    camera = Camera()
    mic = Microphone()

    # Timer for when files (recordings, logfiles) should be uploaded
    #uploadFiles_timer = datetime.now()
    # Timer for when data should be uploaded (interactions & sensors readings)
    #uploadData_timer = datetime.now()
    # Timer for when disk space should be checked
    #checkSpace_timer = datetime.now()
    pingTimer = datetime.now()
    # Timer to avoid uploading data during and right after interactions
    #ix_timer = datetime.now()

    lastActivity = datetime.now()
    activated = False

    #logfilesUploadedToday = False

    try:
        switches = Switches(logger, camera, mic)

        logger.log_program_run_info()
        logger.log_system_status('Main','Tunnel started.')

        #logger.upload_recordings(5)
        #logger.upload_mic_recordings(5)

        printlog('Main','Ready for use!')

        while True:

            if (datetime.now() - pingTimer).total_seconds() / 60 > 10:
                #ping every 10 minutes
                logger.log_system_status('Main','Time when last activity ended: {}.'.format(lastActivity))
                printlog('Main','Still alive!')
                pingTimer = datetime.now()

            # Checking if should update the request quota for Google Sheets
            # It is 100 requests per 100 seconds (e.g. logging of 100 rows)
            #logger.gservice.check_quota_timer()

            # Checks the state of switches and handles what to do with media: should it start or stop or content switched.
            # Also logs when interaction starts and ends.
            switches.update()
            switches.manageMedia()

            if logger.ix_id == None:
                activated = False
            else:
                activated = True

            if switches.endtime != None:
                lastActivity = switches.endtime

            # Stop interactive period and recording after certain time since last interaction
            if not activated:

                timeSinceActivity = round((datetime.now() - lastActivity).total_seconds(),2)

                if timeSinceActivity > globals.periodDelay:
                    # delay has passed

                    #logger.end_ixPeriod()

                    if globals.recordingOn and camera.is_recording:
                        try:
                            camera.stop_recording()
                            mic.stop()
                            sleep(0.2)
                            printlog('Main','Stopping to record, time since last interaction end: {}.'.format(timeSinceActivity))
                        except Exception as e:
                            logger.log_system_status('Main','Error when trying to stop camera or mic from recording: {}'.format(type(e).__name__, e))



            timeSinceIx = (datetime.now() - lastActivity).total_seconds() / 60
            # # Upload log data to Sheets every 6 minutes.
            # if (datetime.now() - uploadData_timer).total_seconds() / 60 > 6:
            #     if not activated and timeSinceIx > 1:
            #         # Upload data logs after some time passed since activity
            #         printlog('Main','Uploading data from ix logs..')
            #         logger.upload_ix_logs()
            #         uploadData_timer = datetime.now()

            # Check disk space every 20 minutes
            # if (datetime.now() - checkSpace_timer).total_seconds() / 60 > 20:
            #     try:
            #         ensure_disk_space(logger)
            #         checkSpace_timer = datetime.now()
            #     except Exception as e:
            #         printlog('Main','Error in reading / logging disk space: {}'.format(type(e).__name__, e))


            # Upload recordings and log files in the evening
            # hourNow = datetime.now().hour
            # if not activated and timeSinceIx > 1:
            #     if (hourNow == 22 or hourNow == 23):
            #         if (datetime.now()-uploadFiles_timer).total_seconds() / 60 > 25:
            #             # During these hours, only check about 4 times if there are any
            #             # videos / logfiles to upload
            #             printlog('Main','Starting to upload files from today.')
            #             logger.upload_recordings(5)
            #             logger.upload_mic_recordings(5)

            #             if not logfilesUploadedToday:
            #                 # do this only once a day
            #                 logger.upload_logfiles()
            #                 logfilesUploadedToday = True

            #             uploadFiles_timer = datetime.now()

            #     elif hourNow == 0:
            #         logfilesUploadedToday = False

            sleep(0.2)


    except KeyboardInterrupt:
        printlog('Main','Exiting, KeyboardInterrupt')

    finally:

        try:
            logger.log_system_status('Exit','Exiting program.')
            #logger.upload_ix_logs()
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
            globals.audioPlayer.stop()

        ix_data = logger.ix_tempdata
        if len(ix_data) != 0:
            printlog('Exit','Logging ix data to csv.')
            # timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            # file = timestamp + '_ix_backup.csv'
            # TODO: double check this works if exits in middle of interaction
            for row in ix_data:
              log_local(row, sheet=configs.local_ix_log)
