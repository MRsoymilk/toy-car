import configparser
import time
import threading
from gpiozero import Servo, Motor
from picamera import PiCamera
from GetChar import GetChar

config = configparser.ConfigParser()
config.read('./config.ini')

# init camera
servo_camera_v = Servo(config.getint('Pin', 'CameraV'))
servo_camera_h = Servo(config.getint('Pin', 'CameraH'))
value_camera_v = servo_camera_v.value
value_camera_h = servo_camera_h.value
servo_camera_v.detach()
servo_camera_h.detach()


class CarCamera:
    def __init__(self):
        self.camera = PiCamera()
        self.camera.resolution = (200, 200)
        self.lock = threading.Lock()

    def capture(self, name):
        self.lock.acquire()
        self.camera.capture(name)
        self.lock.release()


# init power motor
motor = Motor(config.getint('Pin', 'MotorA'), config.getint('Pin', 'MotorB'))
Speed = config.getfloat('Car', 'Speed')

# init direction servo
direction = Servo(config.getint('Pin', 'Direction'))
direction.detach()
Left = config.getfloat('Car', 'Left')
Right = config.getfloat('Car', 'Right')

# init others
File = config.get('Network', 'Data')

getchar = GetChar()
capture = CarCamera()

print("... start ...")
while True:
    flag = getchar()
    # quit
    if flag == 'q' or flag == 'Q':
        break
    # car motion
    elif flag == 'w' or flag == 'W':
        threading.Thread(target=capture.capture, args=(
            File + '/w/' + str(time.time()) + '.png',)).start()
        direction.value = 0
        time.sleep(0.2)
        direction.detach()
        print("car forward")
    elif flag == 'a' or flag == 'A':
        threading.Thread(target=capture.capture, args=(
            File + '/a/' + str(time.time()) + '.png',)).start()
        direction.value = Left
        time.sleep(0.2)
        direction.detach()
        print("car left")
    elif flag == 'd' or flag == 'D':
        threading.Thread(target=capture.capture, args=(
            File + '/d/' + str(time.time()) + '.png',)).start()
        direction.value = Right
        time.sleep(0.2)
        direction.detach()
        print("car right")
    elif flag == ' ':
        if motor.value == 0:
            motor.forward(Speed)
            print("... motion ...")
        else:
            motor.value = 0
            print("... pause ...")
    elif flag == 'p' or flag == 'P':
        motor.value = 0
        print("... pause ...")

