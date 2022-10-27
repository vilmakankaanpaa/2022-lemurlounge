import subprocess
import configs

class Microphone():

    def __init__(self):
        self.recorder = None
        self.is_recording = False

    def record(self, filename):

        if not self.is_recording:
            filepath = configs.MIC_RECORDINGS + filename + '.wav'
            self.recorder = subprocess.Popen(args=["arecord","-D","plughw:1,0","-f","dat",filepath], stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True)
            self.is_recording = True

    def stop(self):
        if self.is_recording:
            self.recorder.terminate()
            self.is_recording = False
