from Drivers.driverInterface import *
from Dto.commandDto import CommandDto

import numpy as np
import pandas as pd
import pickle
from scipy import stats
from sklearn import linear_model
from sklearn.neural_network import MLPRegressor

class DriverRegression(DriverInterface):
    def __init__(self):
        self.trainingSetPath = "/vagrant/torcs-ai_client_examples/scr-client-cpp/data/forza_2023-05-19.csv"
        self.modelPath = "/vagrant/ClientCode/Models/model.sav"
    
    def start(self):
        try:
            self.regressor = self._load()
            print('model loaded')
        except FileNotFoundError:
            self.regressor = self.train()
            print('model trained and saved')
    
    def drive(self, carState: dict) -> CommandDto:
        command = CommandDto()
        arr = np.array([carState['speed'][0], carState['speed'][1], carState["speed"][2], carState["angle"], carState["location"][2],
                                 carState["trackPos"], carState["distFromStart"]]).astype(float)
        action = self.predict([arr])
        # print(action)

        #implemented automatic gear, from 50 it shifts up every 30 km/h faster, 
        #when using it right now, the car starts to wobble and crashes.
        #command.gear = self.getGear(data['speed'][0])
        command.gear = 1
        command.accelerator = action[0][0]
        command.steering = action[0][1]
        command.brake = action[0][2]

        return command

    def normalEquation(self, X, Y):
        beta = np.dot(np.dot(np.linalg.inv(np.dot(np.transpose(X), X)), np.transpose(X)), Y)
        return beta
    
    def scikitLearn(self, X, Y):
        reg = linear_model.LinearRegression()
        reg.fit(X, Y)
        beta = reg.coef_.reshape(-1,1)
        return beta
    
    def scikitMLP(self, X, Y):
        reg = MLPRegressor(hidden_layer_sizes=(50, 50, 50 ), max_iter=500, activation='logistic', solver='adam', random_state=1)
        reg.fit(X.values, Y.values)
        return reg

    def train(self):
        #Load the csv 
        data = pd.read_csv(self.trainingSetPath, 
                        sep=';', index_col=False, header=0,
                        usecols=["s_speed_x", "s_speed_y", "s_speed_z", "s_angle", "s_z", "s_track_position", 
                                 "a_accelation", "a_steer", "s_distance_from_start", "a_brake"])
        
        #clean data
        data = self._cleanData(data)
        data = self._removeOutliers(data)

        #Split the data into variables and results
        X = data[["s_speed_x", "s_speed_y", "s_speed_z", "s_angle", "s_z", "s_track_position", "s_distance_from_start"]]
        Y = data[["a_accelation", "a_steer", "a_brake"]]

        # # Create linear regression object
        # regr = linear_model.LinearRegression()

        # # Train the model using the training set
        # regr.fit(X, Y)

        beta = self.normalEquation(X, Y)
        
        # regr = self.scikitMLP(X, Y)
        self._save()
        return beta

    def predict(self, df):
        # return self.regressor.predict(df)
        return np.dot(df, self.regressor)
        # return self.regressor.predict(df)

    def _save(self):
        pickle.dump(self.regressor, open(self.modelPath, 'wb'))

    def _load(self):
        loadedModel = pickle.load(open(self.modelPath, 'rb'))
        return loadedModel

    def _removeOutliers(self, df):
        df = df[(np.abs(stats.zscore(df, axis=0))<4).all(axis=1)]
        df.reset_index(inplace=True)
        return df
    
    def _cleanData(self, df):
        #remove entries where distance raced is 0
        df = df[df["s_speed_x"] >= 0]
        df.reset_index(inplace=True)
        return df