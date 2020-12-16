import Net
import configparser
import torch
import os
import sys
from PIL import Image

config = configparser.ConfigParser()
config.read('./config.ini')
MODEL = config.get("Network", "Model")

DATA_DIR = config.get('Network', 'Data')
classes = os.listdir(DATA_DIR)

transformations = Net.transformations
net = Net.Net()
net.eval()
net.load_state_dict(torch.load(MODEL))

image = Image.open(sys.argv[1])
image = transformations(image).float()
image = torch.autograd.Variable(image[None, ...])

outputs = net(image)
predict = outputs.max(1, keepdim=True)[1]
print("predict: ", classes[predict])