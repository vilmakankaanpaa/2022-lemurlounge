# -*- coding: utf-8 -*-
#!/usr/bin/env python3

import sys
import os
import csv
import shutil
from datetime import datetime

# Local source
import configs

sys.excepthook = sys.__excepthook__

def printlog(srcfile, msg):

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    data = [[timestamp, srcfile, msg]]

    # print to a file
    #log_local(data=data, sheet=configs.local_printlog)

    # print to terminal
    print(timestamp,msg)


def log_local(data, sheet):

    with open(sheet, 'a', newline='') as logfile:
        logwriter = csv.writer(logfile, delimiter=',')
        for row in data:
            logwriter.writerow(row)


def delete_local_file(path):

    if os.path.exists(path):
        os.remove(path)
    else:
        printlog('Filemanager','Could not delete local file at {}, it does not exist'.format(path))


def list_recordings():
    videos = []
    dir = None

    dir = get_directory_for_recordings()
    dirContent = os.listdir(dir)
    printlog('Filemanager','Size of dir: {}'.format(len(dirContent)))
    for filename in dirContent:
        if filename.endswith('.h264'):
            videos.append(filename)

    return videos, dir


def nof_recordings():

    if check_usb_disk_access():
        dirContent = os.listdir(configs.RECORDINGS_PATH)
        # there is one file for testing in the folder: test.txt, hence -1
        return len(dirContent)-1
    else:
        dirContent = os.listdir(configs.RECORDINGS_PATH_backup)
        return len(dirContent)


def check_usb_disk_access():
    # can e.g. check whether usb is connected via if you can access the test.txt init
    path = configs.RECORDINGS_PATH + 'test.txt'
    print(path)
    exists = os.path.exists(path)
    print(exists)
    return exists


def get_directory_for_recordings():
    usb = check_usb_disk_access()
    if usb:
        return configs.RECORDINGS_PATH
    else:
        printlog('Filemanager','ERROR: Could not access USB drive!')
        return configs.RECORDINGS_PATH_backup


def check_disk_space(disk):
    total, used, free = shutil.disk_usage(disk)

    #print("Total: %d GiB" % (total // (2**30)))
    #print("Used: %d GiB" % (used // (2**30)))
    #print("Free: %d GiB" % (free // (2**30)))

    relative = free/total

    return round(relative, 2)
