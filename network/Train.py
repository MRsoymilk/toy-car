import Net
import configparser
import numpy as np
import torch
import torch.optim as optim
import torch.nn as nn
import os
from torch.utils.data import random_split
from torchvision.datasets import ImageFolder

print("init")
config = configparser.ConfigParser()
config.read('./config.ini')

BATCH_SIZE = config.getint('Network', 'BatchSize')
EPOCH = config.getint('Network', 'Epoch')
LEARN_RATE = config.getfloat('Network', 'LearnRate')
DATA_DIR = config.get('Network', 'Data')
MODEL = config.get('Network', 'Model')

classes = os.listdir(DATA_DIR)
print("classes: ", classes)

transformations = Net.transformations

print("load data")
dataset = ImageFolder(DATA_DIR, transform=transformations)

len_data = len(dataset)
len_train = int(len_data * 0.8)
len_valid = int(len_data * 0.1)
len_test = len_data - len_train - len_valid

train_data, valid_data, test_data = random_split(dataset, [len_train, len_valid, len_test])

train_loader = torch.utils.data.DataLoader(train_data, shuffle=True, batch_size=BATCH_SIZE)
valid_loader = torch.utils.data.DataLoader(valid_data, shuffle=True, batch_size=BATCH_SIZE)
test_loader = torch.utils.data.DataLoader(test_data, shuffle=True, batch_size=BATCH_SIZE)

net = Net.Net()

criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(net.parameters(), lr=LEARN_RATE)

print("train network")
valid_loss_min = np.Inf
for epoch in range(1, EPOCH + 1):
    train_loss = 0.0
    valid_loss = 0.0
    # train
    for data, target in train_loader:
        optimizer.zero_grad()
        output = net(data)
        loss = criterion(output, target)
        loss.backward()
        optimizer.step()
        train_loss += loss.item() * data.size(0)
    
    # valid test
    net.eval()
    for data, target in valid_loader:
        output = net(data)
        loss = criterion(output, target)
        valid_loss += loss.item() * data.size(0)


    if valid_loss <= valid_loss_min:
        print("\nValidataion loss decreased ({:.6f} ---> {:.6f}). Saving model.".format(
            valid_loss_min, valid_loss
        ))
        torch.save(net.state_dict(), MODEL)
        valid_loss_min = valid_loss

    train_loss = train_loss / len(train_loader.sampler)
    valid_loss = valid_loss / len(valid_loader.sampler)
    print("Epoch: {}\tTraining Loss: {:.6f}\tValidation Loss: {:.6f}".format(epoch, train_loss, valid_loss))

    # Accuracy
    net.load_state_dict(torch.load(MODEL))
    class_correct = list(0. for i in range(len(classes)))
    class_total = list(0. for i in range(len(classes)))

    net.eval()
    for data, target in test_loader:
        output = net(data)
        _, pred = torch.max(output, 1)
        correct_tensor = pred.eq(target.data.view_as(pred))
        correct = np.squeeze(correct_tensor.numpy())

        for i in range(len(correct)):
            label = target.data[i]
            class_correct[label] += correct[i].item()
            class_total[label] += 1

    print('\n')
    for i in range(len(classes)):
        if class_total[i] > 0:
            print("Test Accuracy of {}: {} % ({} / {})".format(
                classes[i], 100 * class_correct[i] / class_total[i], np.sum(class_correct[i]),
                np.sum(class_total[i])))
        else:
            print("Test Accuracy of {}: N/A (no training examples)".format(classes[i]))

    print("\nTest Accuracy (Overall): {}% --- {}/{}".format(
        100. * np.sum(class_correct) / np.sum(class_total), np.sum(class_correct), np.sum(class_total)))
