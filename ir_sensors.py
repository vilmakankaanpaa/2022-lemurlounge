import spidev

from filemanager import printlog
from datetime import datetime

# Spidev used to connect to and read the sensors
spi = spidev.SpiDev()
spi.open(0,0)
spi.max_speed_hz=1000000

class Sensors():

    def __init__(self):

        # Channels and thresholds. 0-3 from right to left when facing screen.
        # Might depend on location so good to test every time the device moves.
        self.voltThresholds = {0:0.55, 1:0.55, 2:0.40}

        self.sensorReadings = [[False,0],[False,0],[False,0]]

        # After how many checks the value is changed and "determined".
        self.checkThreshold = 1
        # Determined state of sensors
        self.activatedSensors = [False, False, False]

        self.timer = datetime.now()
        self.counter = 0


    def read_channel(self, channel=0):

        val = spi.xfer2([1,(8+channel)<<4,0])
        data = ((val[1]&3) << 8) + val[2]
        volts = (data/1023.0)*3.3
        return volts


    def single_sensor(self, sensorNo):

        # Read the sensor values
        volts = self.read_channel(sensorNo)
        # Based on threshold, set True or False.
        inRange = volts > self.voltThresholds.get(sensorNo)

        # Did the value change?
        changed = False
        if self.sensorReadings[sensorNo][0] != inRange:
            changed = True

        self.sensorReadings[sensorNo][0] = inRange

        # Count and mark the times the value has not changed since the last
        # check. This is counter towards the threshold to decide if the
        # readings are correct and should be 'determined' values.
        counter = 0
        current = self.sensorReadings[sensorNo][1]
        if not changed and current <= self.checkThreshold:
            # Allow the checks counter go one above threshold.
            counter += 1
        elif not changed and current > self.checkThreshold:
            counter = current
        # elif changed, keep at 0

        self.sensorReadings[sensorNo][1] = counter

        return volts


    def check_sensors(self):

        voltsList = [] # the closer, the larger volts

        for i in range(3):
            volts = self.single_sensor(i)
            voltsList.append(round(volts,3))

        if (datetime.now()-self.timer).total_seconds()/60 > 10:
            if self.counter < 10:
                printlog('Sensors: ',voltsList)
                self.counter += 1
            else:
                self.timer = datetime.now()
                self.counter = 0

        return voltsList


    def check_changed(self):

        # Every time the value has been confirmed enough times (it is same as the set threshold), the value of it will be updated to activated.

        mostRecentOpen = None
        changed = False

        for i in [0,2,1]: # check the sensors in this order

            inRange = self.sensorReadings[i][0]
            nofChecks = self.sensorReadings[i][1]

            if nofChecks == self.checkThreshold and inRange != self.activatedSensors[i]:
                changed = True
                # set the new status of the sensor ('determined' now)
                self.activatedSensors[i] = inRange
                if inRange == True:
                    mostRecentOpen = i
                    printlog('Switches','Switch {} open.'.format(i))
                else:
                    printlog('Switches','Switch {} closed.'.format(i))

        return mostRecentOpen, changed


    def update(self):

        # Read the sensor values now
        volts = self.check_sensors()
        # After checking with threshold, which are activated?
        mostRecentOpen, someChanged = self.check_changed()

        return self.activatedSensors, mostRecentOpen, someChanged, volts
