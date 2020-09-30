import cv2
import threading
import time
import configparser
from gpiozero import Servo, DistanceSensor, Motor
from picamera import PiCamera


print("read config")
config = configparser.ConfigParser()
config.read('./config.ini')

print("init")
carCamera = PiCamera()

motor = Motor(config.getint('Pin', 'MotorA'), config.getint('Pin', 'MotorB'))
Speed = config.getfloat('Car', 'Speed')
direction = Servo(config.getint('Pin', 'Direction'))
Left = config.getfloat('Car', 'Left')
Right = config.getfloat('Car', 'Right')

sensor_distance = DistanceSensor(echo=config.getint('Pin', 'SensorEcho'), trigger=config.getint('Pin', 'SensorTrig'))

print("load network")

import torch
import torch.nn as nn
import torch.nn.functional as F
import torchvision
import torchvision.transforms as transforms

import Net

loader = transforms.Compose([transforms.ToTensor(),
        transforms.Normalize([0.5], [0.5])])

net = Net.Net()
net.eval()
net.load_state_dict(torch.load(config.get('Network', 'Model')))

classes = Net.classes

KEEP_GOING = True
CAR_CONTROL = True

def judge():
    tick = time.time()
    global carCamera
    global KEEP_GOING
    KEEP_GOING = False
    carCamera.capture('/tmp/check.png') 
    image = cv2.imread('/tmp/check.png', cv2.IMREAD_GRAYSCALE)

    image = image[0:160, 0:320]
    image = cv2.GaussianBlur(image, (5, 5), 0)
    clahe = cv2.createCLAHE(3, (3, 3))
    image = clahe.apply(image)
    _, image = cv2.threshold(image, 80, 255, cv2.THRESH_BINARY_INV)
    image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
    image = cv2.resize(image, (32, 32))
    print('\r', "image predict", end='', flush=True)
    image = loader(image).float() 
    image = torch.autograd.Variable(image[None, ...])
    outputs = net(image) 
    predict = outputs.max(1, keepdim=True)[1]
    print('\r\n', "predict: ", classes[predict])
    KEEP_GOING = True
    tock = time.time()
    print('\r\n judge time: ', tock - tick)
    return classes[predict]


def car_control():
    global KEEP_GOING
    global CAR_CONTROL

    while KEEP_GOING:
        if CAR_CONTROL:
            print("start predict")
            _predict = judge()
            if _predict == 'w':
                motor.forward(Speed)
                direction.value = 0
            elif _predict == 'a':
                motor.forward(Speed)
                direction.value = Left
            elif _predict == 'd':
                motor.forward(Speed)
                direction.value = Right
            # motor run 0.5s
            time.sleep(0.5)
            motor.stop()
            print("end predict")

    print("car control exit...")

def main():
    car_control()

if __name__ == '__main__':
    main()

