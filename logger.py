#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import uuid
from datetime import datetime, date

import configs
import globals
import filemanager
from filemanager import printlog

sys.excepthook = sys.__excepthook__

class Logger:

    def __init__(self):

        # program run id to match data from same run easily
        self.pid = str(globals.pid) + str(uuid.uuid4())[0:4]

        self.ix_tempdata = []

        # Info on ongoing interaction with the tunnel
        self.ix_period = None
        self.ix_id = None
        self.ix_date = None
        self.ix_start = None
        self.ix_switchesOpen = [False, False, False]
        self.ix_voltReadings = [0, 0, 0]
        self.ix_content = None
        self.ix_recording = None

    def log_system_status(self, src, msg):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        data = [timestamp, src, msg]
        filemanager.log_local([data], configs.local_system_log)


    def log_program_run_info(self):

        # Logged only once in the start of monkeytunnel.py

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        data = [
            self.pid,
            timestamp,
            globals.usingAudio,
            globals.recordingOn]

        data = [data]

        # Log locally, for offline use only
        filemanager.log_local(data, configs.local_program_log)


    def start_ixPeriod(self):
        self.ix_period = str(uuid.uuid4())[0:7]

    def end_ixPeriod(self):
        self.ix_period = None


    def log_interaction_start(self, switchesOpen, volts):

        self.ix_id = str(uuid.uuid4())[0:6]
        self.ix_date = date.isoformat(date.today())
        self.ix_start = datetime.now()
        self.ix_switchesOpen = '{}, {}, {}'.format(switchesOpen[0],switchesOpen[1],switchesOpen[2])
        self.ix_voltReadings = '{}, {}, {}'.format(round(volts[0],2), round(volts[1],2), round(volts[2],2))
        self.ix_content = globals.mediafile


    def log_interaction_end(self, endtime):

        pid = self.pid
        period = self.ix_period
        ID = self.ix_id
        date = self.ix_date
        startime = self.ix_start
        duration = round((endtime - self.ix_start).total_seconds(),2)

        stimulus = 'no-stimulus'
        if globals.testMode == 1:
            stimulus = 'audio'
        elif globals.testMode == 2:
            stimulus = 'visual'

        switchesOpen = self.ix_switchesOpen
        volts = self.ix_voltReadings
        content = self.ix_content
        video = self.ix_recording + '.h264'

        data = [pid, period, ID, date, stimulus,
        content, switchesOpen, volts, startime.strftime("%Y-%m-%d %H:%M:%S"),
        endtime.strftime("%Y-%m-%d %H:%M:%S"), duration, video]

        self.ix_tempdata.append(data)

        # reset
        self.ix_id = None
        self.ix_date = None
        self.ix_start = None
        self.ix_content = None

        # log this data to logal csv file (for full offline use only)
        # when online, data is later logged from tempdata triggered from 
        # monkeytunnel
        try:
          filemanager.log_local(self.ix_tempdata, configs.local_ix_log)
          self.ix_tempdata = []
        except Exception as e:
          printlog('Logger','ERROR: Could not log ix data: {}, {}'.format(type(e).__name__, e))


    def new_recording_name(self):

        self.ix_recording = (self.ix_start).strftime("%Y-%m-%d_%H-%M") + '_' + self.ix_period
        return self.ix_recording
