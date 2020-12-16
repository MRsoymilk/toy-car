import Net
import configparser
import torch
from PIL import Image

config = configparser.ConfigParser()
config.read('./config.ini')
MODEL = config.get("Network", "Model")

transformations = Net.transformations
net = Net.Net()

net.eval()
net.load_state_dict(torch.load(MODEL))

image = Image.open("./html/rwby.jpg")
image = transformations(image).float()
image = torch.autograd.Variable(image[None, ...])

torch.onnx.export(
    net,
    image,
    MODEL.split('pth')[0] + 'onnx',
    export_params=True,
    output_names=['toy-car']
)

print("finish")
