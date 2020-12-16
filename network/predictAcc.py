import Net
import configparser
import torch
import os
import sys
import time
from PIL import Image
from openvino.inference_engine import IECore

config = configparser.ConfigParser()
config.read('./config.ini')
MODEL = config.get("Network", "Model")

DATA_DIR = config.get('Network', 'Data')
classes = os.listdir(DATA_DIR)

transformations = Net.transformations
net = Net.Net()
net.eval()
net.load_state_dict(torch.load(MODEL))

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
image = Image.open(sys.argv[1])
image = transformations(image).float()
image = torch.autograd.Variable(image[None, ...])
res = exec_net.infer(inputs={input_blob: image})
res = res[output_blob]
predict = classes[res.argmax()]
print("predict: ", predict)