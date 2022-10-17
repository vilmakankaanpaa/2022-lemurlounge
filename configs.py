# -*- coding: utf-8 -*-
#!/usr/bin/env python3

# Configurations for paths and URLs

# roots
root = '/home/pi/lemur-audio-player/'
external_disk = '/media/pi/8F57-C519/'

# paths to use
RECORDINGS_PATH = external_disk + 'camera-records/'
RECORDINGS_PATH_backup = root + 'camera-records/'
MIC_RECORDINGS = external_disk + 'mic-records/'
MIC_RECORDINGS_backup = root + 'mic-records/'

# file names
audiopath = root + 'audio/'
# use 'configs.audiopath' + audioX + '.mp3'
audio1 = 'rain'
audio2 = 'traffic'
audio3 = 'music'
audio4 = 'zen'
audio5 = 'whitenoise'

# local logfiles
local_ix_log = 'logs/ix_logs.csv'
local_program_log = 'logs/progrun_logs.csv'
local_system_log = 'logs/system_logs.csv'
local_printlog = 'logs/printlog.txt'
local_output = 'logs/output.txt'
