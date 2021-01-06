import cv2
import configparser
import time
import threading
from gpiozero import Servo, Motor

config = configparser.ConfigParser()
config.read('./config.ini')

# init camera
servo_camera_v = Servo(config.getint('Pin', 'CameraV'))
servo_camera_h = Servo(config.getint('Pin', 'CameraH'))
value_camera_v = servo_camera_v.value
value_camera_h = servo_camera_h.value
servo_camera_v.detach()
servo_camera_h.detach()

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

capture = cv2.VideoCapture(0)

while True:
    _, frame = capture.read()
    flag = cv2.waitKey(1)
    # quit
    if flag == ord('q') or flag == ord('Q'):
        break
    # adjust camera
    elif flag == ord('h') or flag == ord('H'):
        if value_camera_h + 0.1 <= 1:
            value_camera_h += 0.1
            servo_camera_h.value = value_camera_h
            time.sleep(0.1)
            servo_camera_h.detach()
        print("left camera, value {:.2f}".format(value_camera_h))
    elif flag == ord('j') or flag == ord('J'):
        if value_camera_v + 0.1 <= 1:
            value_camera_v += 0.1
            servo_camera_v.value = value_camera_v
            time.sleep(0.1)
            servo_camera_v.detach()
        print("down camera, value {:.2f}".format(value_camera_v))
    elif flag == ord('k') or flag == ord('K'):
        if value_camera_v - 0.1 >= -1:
            value_camera_v -= 0.1
            servo_camera_v.value = value_camera_v
            time.sleep(0.1)
            servo_camera_v.detach()
        print("up camera, value {:.2f}".format(value_camera_v))
    elif flag == ord('l') or flag == ord('L'):
        if value_camera_h - 0.1 > -1:
            value_camera_h -= 0.1
            servo_camera_h.value = value_camera_h
            time.sleep(0.1)
            servo_camera_h.detach()
        print("right camera, value {:.2f}".format(value_camera_h))
    # car motion
    elif flag == ord('w') or flag == ord('W'):
        direction.value = 0
        time.sleep(0.2)
        direction.detach()
        threading.Thread(target=cv2.imwrite, args=(
            File + '/w/' + str(time.time()) + '.png', frame,)).start()
        print("car forward")
    elif flag == ord('a') or flag == ord('A'):
        direction.value = Left
        time.sleep(0.2)
        direction.detach()
        threading.Thread(target=cv2.imwrite, args=(
            File + '/a/' + str(time.time()) + '.png', frame,)).start()
        print("car left")
    elif flag == ord('d') or flag == ord('D'):
        direction.value = Right
        time.sleep(0.2)
        direction.detach()
        threading.Thread(target=cv2.imwrite, args=(
            File + '/d/' + str(time.time()) + '.png', frame,)).start()
        print("car right")
    elif flag == ord(' '):
        if motor.value == 0:
            motor.forward(Speed)
            print("... motion ...")
        else:
            motor.value = 0
            print("... pause ...")
    elif flag == ord('p') or flag == ord('P'):
        motor.value = 0
        print("... pause ...")

    cv2.imshow('toy-car', frame)

capture.release()
cv2.destroyAllWindows()
