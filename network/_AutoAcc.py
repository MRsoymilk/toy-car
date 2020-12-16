import cv2
import time
import configparser
import torch
import torchvision.transforms as transforms
import time
from PIL import Image
from gpiozero import Servo, Motor
from openvino.inference_engine import IECore

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
transformations = transforms.Compose([
    transforms.Resize((32, 32)),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
])

classes = ['a', 'd', 'w']

# openvino setting start =========
ie = IECore()
print("read network")
tick = time.time()
net = ie.read_network('./network/model/model.xml', './network/model/model.bin')
input_blob = next(iter(net.input_info))
output_blob = next(iter(net.outputs))
net.batch_size = 1
print("load network")
exec_net = ie.load_network(network=net, device_name='MYRIAD')
print("time: ", time.time() - tick)
# openvino setting end =========


def judge(frame):
    tick = time.time()
    img = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
    img = img.convert('RGB')
    img = transformations(img).float()
    img = torch.autograd.Variable(img[None, ...])
    res = exec_net.infer(inputs={input_blob: img})
    res = res[output_blob]
    predict = classes[res.argmax()]
    tock = time.time()
    print("predict: {} --> time: {}".format(predict, tock - tick))
    return predict


def car_control():
    capture = cv2.VideoCapture(0)
    while True:
        _, frame = capture.read()
        predict = judge(frame)
        motor.forward(Speed)
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


    capture.release()
    cv2.destroyAllWindows()


def main():
    car_control()


if __name__ == '__main__':
    main()
