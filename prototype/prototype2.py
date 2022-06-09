# Code for testing the final functional prototype

import RPi.GPIO as GPIO
from time import sleep
import sys
import os
from datetime import datetime
import csv

boottime = datetime.now()

def log(row):

    file = open('prototype.csv', 'a', newline='')
    writer = csv.writer(file, delimiter=',')
    writer.writerow(row)

    file.close()

def react(channel):

    global count
    global latestchange

    since_boot = round((datetime.now() - boottime).total_seconds(),4)

    if GPIO.input(channel) == GPIO.HIGH:
        count += 1
        latestchange = True

        print('\n▲ Flip open, interaction: ', count, '(', round(since_boot,1), 's)')
        log([datetime.now(),'flip','Flip open {}'.format(count), since_boot])

    else:
        latestchange = False

        print('\n▼ Flip closed, interaction: ', count, '(', round(since_boot,1), 's)')
        log([datetime.now(),'flip','Flip closed {}'.format(count), since_boot])


if __name__ == "__main__":

    try:
        # Use Brodadcom (the GPIO numbering)
        GPIO.setmode(GPIO.BCM)
        # Set to use the GPIO pin no. 17.
        # Use Pull Up resistance for the reed sensor wiring.
        GPIO.setup(17,GPIO.IN, pull_up_down=GPIO.PUD_UP)
        # not using bouncetime because we need to make sure to record all
        # the openings. We'll control the quick changes in other ways.
        GPIO.add_event_detect(17, GPIO.BOTH, callback=react)

        # Count of interactions
        global count
        count = 0

        # Determines when media should be playing
        #global mediastatus
        mediastatus = False

        # Store the latest change of status
        global latestchange
        latestchange = False

        starttime = None
        delay = 4

        while True:
            # Run the other parts of program here.
            sleep(0.1)

            if mediastatus and not latestchange: # playing but flip is closed
                playtime = round((datetime.now() - starttime).total_seconds(),4)

                if playtime > delay: # delay has passed
                    mediastatus = False
                    print(playtime, 'Turning media off.')
                    log([datetime.now(),'media','Turning media off.', playtime])

            elif not mediastatus and latestchange:
                mediastatus = True
                starttime = datetime.now()
                print ('Turning media on.')
                log([datetime.now(),'media','Turning media on.', 0])



    except KeyboardInterrupt:
        print('exiting')

    finally:
        GPIO.cleanup()
