from Services.torcsClient import TorcsClient
import os
import pandas as pd
import numpy as np
from sklearn import linear_model
from sklearn.neural_network import MLPRegressor

def train():
    #Load the csv 
    data = pd.read_csv('/vagrant/torcs-ai_client_examples/scr-client-cpp/data/forza_2023-05-19.csv', 
                    sep=';', index_col=False, header=0,
                    usecols=["s_speed_x", "s_speed_y", "s_speed_z", "s_angle", "s_z", "s_track_position", "a_accelation", "a_steer", "s_distance_from_start"])

    print(data.head())


    X = data[["s_speed_x", "s_speed_y", "s_speed_z", "s_angle", "s_z", "s_track_position", "s_distance_from_start"]]
    Y = data[["a_accelation", "a_steer"]]
    print(X.head())
    print(Y.head())

    # Create linear regression object
    regr = linear_model.LinearRegression()
    # Train the model using the training sets
    regr.fit(X, Y)

    return regr
def main():
    regr = train()
    client = TorcsClient(regr)
    client.run()

if __name__ == '__main__':
    main()