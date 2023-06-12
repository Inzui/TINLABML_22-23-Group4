import pandas as pd

import torch
import torch.nn as nn

import numpy

df = pd.read_csv('./../../../Logs/train_data/aalborg.csv')

target = ['ACCELERATION', 'BRAKE', 'STEERING']

x = df.drop(target, axis=1)
y = df[target]

n_input, n_hidden, n_out, batch_size, learning_rate = len(x.columns), 100, len(y.columns), len(x), 0.01

data_x = torch.tensor(x.values)
data_x = data_x.to(torch.float32)
data_y = torch.tensor(y.values)
data_y = data_y.to(torch.float32)

model = nn.Sequential(nn.Linear(n_input, n_hidden),
                      nn.ReLU(),
                      nn.Linear(n_hidden, n_out),
                      nn.Sigmoid())
print(model)

loss_function = nn.MSELoss()
optimizer = torch.optim.SGD(model.parameters(), lr=learning_rate)

losses = []
for epoch in range(5000):
    pred_y = model(data_x)
    loss = loss_function(pred_y, data_y)
    losses.append(loss.item())

    model.zero_grad()
    loss.backward()

    optimizer.step()

correct = 0
wrong = 0

for i in range(0, len(y), 50):

    test_x = torch.tensor(x.loc[i].values)
    test_x = test_x.to(torch.float32)

    predict = model(test_x).detach().numpy()
    
    print(predict)
    print(y.loc[i].values)
    print()