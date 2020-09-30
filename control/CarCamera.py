import configparser
import io
import threading
import time
from gpiozero import Servo
from picamera import PiCamera
from PIL import Image


class CarCamera:
    thread = None
    frame = None
    last_access = 0
    Size = None
    camera = PiCamera()
    camera.resolution = (320, 320)
    lock = threading.Lock()

    def __init__(self):
        print("read camera config start")
        config = configparser.ConfigParser()
        config.read('./config.ini')
        global Size
        Size = config.getint('Camera', 'Size')
        print("read camera config end")

    def initialize(self):
        if CarCamera.thread is None:
            CarCamera.thread = threading.Thread(target=self._thread)
            CarCamera.thread.start()

            while self.frame is None:
                time.sleep(0)

    @classmethod
    def _thread(cls):
        with CarCamera.camera as camera:
            global Size
            print("camera warm up")
            camera.start_preview()
            time.sleep(1)

            stream = io.BytesIO()

            for foo in camera.capture_continuous(stream, 'jpeg', use_video_port=True):
                stream.seek(0)
                cls.frame = stream.read()
                
                stream.seek(0)
                stream.truncate()
                if time.time() - cls.last_access > 10:
                    break
        cls.thread = None


    def get_frame(self):
        CarCamera.last_access = time.time()
        self.initialize()
        return self.frame

    def capture(self, name):
        CarCamera.lock.acquire()
        CarCamera.camera.capture(name)
        CarCamera.lock.release()
    
