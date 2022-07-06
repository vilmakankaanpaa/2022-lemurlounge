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

# video files
videopath = root + 'video/'
# use 'configs.videopath' + audioX + '.mp4'
#video1 = 'forest'
video1 = 'underwater'
video2 = 'worms'
video3 = 'abstract'
video5 = 'black'

# dates for switching media
period1Date = '2022-07-1'
period2Date = '2022-07-5'
period3Date = '2022-07-9'
period4Date = '2022-08-13'
# ....

# local logfile names
# local_ix_log = 'ix_backup.csv'
# local_program_log = 'progrun_backup.csv'
local_ix_log = external_disk + 'logs/ix_logs.csv'
local_program_log = external_disk + 'logs/progrun_logs.csv'
local_system_log = external_disk + 'logs/system_logs.csv'
local_printlog = 'printlog.txt'
local_output = 'output.txt'
# To store file names not being able to upload
# local_uploadlog = "uploadlog.txt"
# local_mic_uploadlog = "mic_uploadlog.txt"

# Google sheets API parameters for logging data
SPREADSHEET_ID = '1qh6czdoIkbHTeeRIu6tQZmIGVsXYSKScXbcqotv6nMU'
#SPREADSHEET_ID = '1-sFTPHnKqSMEMJ6mKf0D3lMXn77QECNJbL_vR-Prskg'
IX_SHEET = 'interactions'
STARTS_SHEET = 'system-starts'
PING_SHEET = 'ping-alive'
SYSTEM_SHEET = 'system-status'

# Google Drive API parameters for uploading listDriveFiles
#GDRIVE_FOLDER_ID = '1F-kDuVRUCY_HZTpls-HjgoMZfQsHHsFy'  #recordings
#GDRIVE_FOLDER_ID_LOGS = '1ZhqiXGb0yIBRg-h_UlASro2tIVav0YmO'  #system logs
GDRIVE_FOLDER_ID = '1atA3l6nSu8SaRNU_Bo2t5R-FIM73YmC5'  #recordings
GDRIVE_FOLDER_ID_LOGS = '1AS0sOxC3veNfWZnxMqnZ8jPKdcK3_BxI'  #system logs

service_account_file = '/home/pi/lemur-audio-player/service_account.json'
