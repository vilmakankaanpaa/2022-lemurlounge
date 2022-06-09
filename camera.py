# -*- coding: utf-8 -*-
#!/usr/bin/env python3

# Following instructions here
# https://projects.raspberrypi.org/en/projects/getting-started-with-picamera/4
from picamera import PiCamera
from time import sleep

class Camera():

    def __init__(self):

        self.camera = PiCamera()
        self.is_recording = False


    def start_recording(self, videoName, directory):
        if not self.is_recording:
            self.camera.start_recording(directory + videoName + '.h264')
            self.is_recording = True


    def stop_recording(self):
        if self.is_recording:
            self.camera.stop_recording()
            self.is_recording = False


    def start_preview(self):
        # views preview of camera on the attached screen
        self.camera.start_preview()


    def stop_preview(self):
        self.camera.stop_preview()


    def capture_image(self, imageName):
        self.camera.start_preview()
        # Note: it’s important to sleep for at least two seconds
        # before capturing an image, because this gives the camera’s
        # sensor time to sense the light levels.
        path = '/home/pi/sakis-tunnel-2021/'
        sleep(5)
        self.camera.capture(path + imageName + '.jpg')
        self.camera.stop_preview()

    def close(self):
        self.camera.close()