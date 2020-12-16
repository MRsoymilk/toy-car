import Net
import cv2
import time
import configparser
import torch
from gpiozero import Servo, DistanceSensor, Motor
from PIL import Image

print("read config")
config = configparser.ConfigParser()
config.read('./config.ini')

print("init")
motor = Motor(config.getint('Pin', 'MotorA'), config.getint('Pin', 'MotorB'))
Speed = config.getfloat('Car', 'Speed')
direction = Servo(config.getint('Pin', 'Direction'))
Left = config.getfloat('Car', 'Left')
Right = config.getfloat('Car', 'Right')

print("load network")
transformations = Net.transformations
net = Net.Net()
net.eval()
net.load_state_dict(torch.load(config.get('Network', 'Model')))
classes = Net.classes


def judge(image):
    tick = time.time()
    print("\rimage predict", end='', flush=True)
    image = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    image = transformations(image).float()
    image = torch.autograd.Variable(image[None, ...])
    outputs = net(image)
    predict = outputs.max(1, keepdim=True)[1]
    print("\rpredict: {} ---> time: {:.2f}".format(
        classes[predict], time.time() - tick))
    return classes[predict]


def car_control():
    capture = cv2.VideoCapture(0)
    motor.forward(Speed)
    while True:
        _, frame = capture.read()
        predict = judge(frame)
        if predict == 'w':
            direction.value = 0
            time.sleep(0.2)
            direction.detach()
        elif predict == 'a':
            direction.value = Left
            time.sleep(0.2)
            direction.detach()
        elif predict == 'd':
            direction.value = Right
            time.sleep(0.2)
            direction.detach()


def main():
    car_control()


if __name__ == '__main__':
    main()
