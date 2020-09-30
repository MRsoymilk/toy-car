import configparser
from gpiozero import Servo

from GetChar import GetChar


config = configparser.ConfigParser()
config.read('./config.ini')

# init camera
servo_camera_v = Servo(config.getint('Pin', 'CameraV'))
servo_camera_h = Servo(config.getint('Pin', 'CameraH'))

# get input
getchar = GetChar()

value_servo_camera_v = 0.0
value_servo_camera_h = 0.0

def init():

    global keep_going
    global value_servo_camera_h
    global value_servo_camera_v

    servo_camera_v.value, value_servo_camera_v = 0.0, 0.0
    servo_camera_h.value, value_servo_camera_h = 0.0, 0.0

def valueChange(value, step, border):
    if abs(value + step) > abs(border):
        value = border
    else:
        value += step
    return value

def handleEvent():
    cmd = getchar() 

    global keep_going
    global value_servo_camera_h
    global value_servo_camera_v

    if cmd == 'q' or cmd == 'Q':
        print("exit ...")
        keep_going = False
        init()
    elif cmd == 'k' or cmd == 'K':
        print("up camera")
        value_servo_camera_v = valueChange(value_servo_camera_v, -0.1, -1)
    elif cmd == 'j' or cmd == 'J':
        print("down camera")
        value_servo_camera_v = valueChange(value_servo_camera_v, 0.1, 1)
    elif cmd == 'h' or cmd == 'H':
        print("left camera")
        value_servo_camera_h = valueChange(value_servo_camera_h, 0.1, 1)
    elif cmd == 'l' or cmd == 'L':
        print("right camera")
        value_servo_camera_h = valueChange(value_servo_camera_h, -0.1, -1)
    else:
        print("reset")
        init()

keep_going = True
while keep_going:
    handleEvent()
    
    servo_camera_h.value = value_servo_camera_h
    servo_camera_v.value = value_servo_camera_v
