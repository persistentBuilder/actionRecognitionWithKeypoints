from __future__ import print_function, division
import torch
import numpy as np
import argparse
import torch.nn as nn
import torch.nn.functional as F

class largeNet(nn.Module):
    def __init__(self):
        super(largeNet, self).__init__()
        #conv layers
        self.conv1 = nn.Conv2d(1, 50, kernel_size=3)
        self.conv1_bn = nn.BatchNorm2d(50)
        self.conv1_drop = nn.Dropout2d(p=0.1)

        self.conv2 = nn.Conv2d(50, 100, kernel_size=3)
        self.conv2_bn = nn.BatchNorm2d(100)
        self.conv2_drop = nn.Dropout2d(p=0.1)

        self.conv3 = nn.Conv2d(100, 150, kernel_size=3)
        self.conv3_bn = nn.BatchNorm2d(150)
        self.conv3_drop = nn.Dropout2d(p=0.2)
        
        #fully connected layers
        self.fc1 = nn.Linear(151200, 300)
        self.fc1_bn = nn.BatchNorm1d(300)
        self.fc1_drop = nn.Dropout(p=0.3)

        self.fc2 = nn.Linear(300, 300)
        self.fc2_bn = nn.BatchNorm1d(300)
        self.fc2_drop = nn.Dropout(p=0.4)

        self.fc3 = nn.Linear(300, 101)
        self.fc3_drop = nn.Dropout(p=0.5)

    def forward(self, x):
        x = F.relu((self.conv1_drop((self.conv1(x)))))
        x = F.relu((self.conv2_drop((self.conv2(x)))))
        x = F.relu((self.conv3_drop((self.conv3(x)))))
        x = x.view(x.size()[0], -1)
        x = F.relu(self.fc1_drop((self.fc1(x))))
        #x = F.relu(self.fc1_drop(self.fc1_bn(self.fc1(x))))
        x = F.relu(self.fc2_drop((self.fc2(x))))
        #x = F.relu(self.fc2_drop(self.fc2_bn(self.fc2(x))))
        x = (self.fc3_drop(self.fc3(x)))
        return F.log_softmax(x, dim=1)

