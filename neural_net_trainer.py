# -*- coding: utf-8 -*-
"""
Created on Sat Apr  2 22:55:17 2022

@author: tbere
"""
import pickle
import torch
from torch import nn
import torch.nn.functional as F
import os
    
class ConvNet(nn.Module):
    def __init__(self):
        super(ConvNet,self).__init__()
        self.conv1 = nn.Conv2d(1, 28, 3)
        self.conv2 = nn.Conv2d(28, 16, 3)
        self.fc = nn.Linear(in_features=16*2*3,out_features=7) #took awhile to figure out
        
    def forward(self,x):
        """
        Feed-forward method of CNN.
        Parameters
        ----------
        x : int
            Connect 4 grid as training data.

        Returns
        -------
        output : TYPE
            DESCRIPTION.

        """
        output = F.leaky_relu(self.conv1(x))
        output = F.leaky_relu(self.conv2(output))
        output = output.view(output.size(0),-1)
        output = self.fc(output) 
        return output 

def train_and_test():
    """
    Function used to train and test a CNN using the ConvNet model.
    Returns
    -------
    None.

    """
    device = 'cpu'
    num_epochs  = 2 #Number of times to train - does not affect accuracy
    learning_rate = 0.01 #Massively affects performance 
    
    cnn = ConvNet().to(device)
    
    #loss/optimiser
    criterion = nn.CrossEntropyLoss()
    optimiser = torch.optim.SGD(cnn.parameters(),lr = learning_rate)
    
    train_dir = os.listdir('./train')
    for n in range(1,len(train_dir)):
        images = [] #board input
        labels = []
        file_extension = './train/Game'+str(n)+"_Depth_6.pkl"
        with open(file_extension,'rb') as f:
            while True:
                try:
                    training_data=pickle.load(f)
                    images.append(torch.tensor(training_data[0]).float().flatten())
                    labels.append(torch.tensor(training_data[1]).float())
                except EOFError:
                    break
        f.close()
        
        # train loop
        for epoch in range(num_epochs):
            for i in range(len(images)):
                images[i] = images[i].view((1,1,6,7))
                image =  images[i].to(device)
                label = labels[i].to(device)
                
                #forward
                outputs = cnn(image)
                label = label.view(-1,label.size(0))
                loss = criterion(outputs,label)
                
                #backward
                optimiser.zero_grad()   
                loss.backward()
                optimiser.step()
    torch.save(cnn.state_dict(),'cnnmodel_demo.pt')
    
    test_dir = os.listdir('./test')
    correct = 0
    number_of_samples = 0
    for n in range(len(train_dir)+1,len(train_dir)+len(test_dir)):
        images = [] #board input
        labels = []
        with torch.no_grad():
            file_extension = './test/Game'+str(n)+"_Depth_6.pkl"
            with open(file_extension,'rb') as f:
                while True:
                    try:
                        training_data=pickle.load(f)
                        images.append(torch.tensor(training_data[0]).float().flatten())
                        labels.append(training_data[1])
                    except EOFError:
                        break
            f.close()
            for i in range(len(images)):
                images[i] = images[i].view((1,1,6,7))
                image = images[i].to(device)
                label = labels[i]
                
                outputs = cnn(image)
                #value, index
                _,column = torch.max(outputs,1) 
    
                label_index = label.index(1)
                correct += (column.item() == label_index)
                number_of_samples += 1
    
    acc = 100 * (correct / number_of_samples)
    print(str(acc)+"%")

#train_and_test()