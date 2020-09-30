import torch
import torch.optim as optim
import torch.nn as nn
import torch.nn.functional as F
import torchvision
import torchvision.transforms as transforms
import configparser

import Net

print("init")
config = configparser.ConfigParser()
config.read('./config.ini')

classes = Net.classes

EPOCH = config.getint('Network', 'Epoch')
LEARN_RATE = config.getfloat('Network', 'LearnRate')

TRAIN = config.get('Network', 'Train')
TEST = config.get('Network', 'Test')
PATH = config.get('Network', 'Model')


transform = transforms.Compose([
    transforms.ToTensor(),
     transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))])

print("load data")
trainset = torchvision.datasets.ImageFolder(TRAIN, transform=transform)
trainloader = torch.utils.data.DataLoader(trainset, batch_size=4,
                                          shuffle=True, num_workers=2)
testset = torchvision.datasets.ImageFolder(TEST, transform=transform)
testloader = torch.utils.data.DataLoader(testset, batch_size=4,
                                         shuffle=False, num_workers=2)
net = Net.Net()


criterion = nn.CrossEntropyLoss()
optimizer = optim.SGD(net.parameters(), lr=LEARN_RATE, momentum=0.9)


print("train network")
for epoch in range(EPOCH):  # loop over the dataset multiple times
    print("epoch: ", epoch)
    running_loss = 0.0
    for i, data in enumerate(trainloader, 0):
        # get the inputs; data is a list of [inputs, labels]
        inputs, labels = data

        # zero the parameter gradients
        optimizer.zero_grad()

        # forward + backward + optimize
        outputs = net(inputs)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()

        # print statistics
        running_loss += loss.item()
        if i % 100 == 99:
            print('[%d, %5d] loss: %.3f' % (epoch + 1, i + 1, running_loss / 100))
            running_loss = 0.0

print("finish training")

print("save model")
torch.save(net.state_dict(), PATH)

print("prepare test data")
dataiter = iter(testloader)
images, labels = dataiter.next()

net = Net.Net()
net.load_state_dict(torch.load(PATH))

print("calculate accurate")
correct = 0
total = 0
with torch.no_grad():
    for data in testloader:
        images, labels = data
        outputs = net(images)
        _, predicted = torch.max(outputs.data, 1)
        total += labels.size(0)
        correct += (predicted == labels).sum().item()

print('Accuracy of the network on the test images: %d %%' % (100 * correct / total))

