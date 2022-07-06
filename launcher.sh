#!/bin/sh

### BEGIN INIT INFO
# Provides:          noip
# Required-Start:    $remote_fs $syslog
# Required-Stop:     $remote_fs $syslog
# Default-Start:     2 3 4 5
# Default-Stop:      0 1 6
# Short-Description: Simple script to start a program at boot
### END INIT INFO

# move the mouse to different location, because at the start it would be on
# the left corner and would trigger the task bar and leave it there
xdotool mousemove 100 100

# start the monkeytunnel program
cd /home/pi/lemur-audio-player
/usr/bin/python3 monkeytunnel.py
cd /
