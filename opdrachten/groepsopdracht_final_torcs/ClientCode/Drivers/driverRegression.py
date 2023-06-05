from Drivers.driverInterface import *
from Dto.commandDto import CommandDto

import numpy as np
import pandas as pd
import pickle, os
from scipy import stats
from sklearn import linear_model
from sklearn.neural_network import MLPRegressor

class DriverRegression(DriverInterface):
    def __init__(self):
        self.regressor = None
        self.trainingSetPath = os.path.join(os.getcwd(), "Models", "BestTrainingSet.csv")
        self.modelPath = "/vagrant/ClientCode/Models/modelNewData.sav"
        self.train()
        # try:
        #     self._load()
        #     print('model loaded')
        # except FileNotFoundError:
        #     self.train()
        #     print('model trained and saved')
    
    def drive(self, carState: dict) -> CommandDto:
        command = CommandDto()
        currentState = np.array([carState["speed"][0], carState["trackPos"], carState["angle"], 
                                    carState["track"][0], carState["track"][1], carState["track"][2], carState["track"][3],
                                    carState["track"][4], carState["track"][5], carState["track"][6], carState["track"][7],
                                    carState["track"][8], carState["track"][9], carState["track"][10], carState["track"][11],
                                    carState["track"][12], carState["track"][13], carState["track"][14], carState["track"][15],
                                    carState["track"][16], carState["track"][17], carState["track"][18]])
        
        action = self._predict([currentState])

        #implemented automatic gear, from 50 it shifts up every 30 km/h faster, 
        #when using it right now, the car starts to wobble and crashes.
        command.gear = self.getGear(carState['speed'][0])
        command.accelerator = action[0][0]
        command.brake = action[0][1]
        command.steering = action[0][2]

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
        reg = MLPRegressor(hidden_layer_sizes=(100,100,100), max_iter=5000, activation='logistic', solver='adam', random_state=1)
        reg.fit(X.values, Y.values)
        return reg

    def train(self):
        #Load the csv 
        trainingsSet = pd.read_csv(self.trainingSetPath, 
                        sep=',', index_col=False, header=0)

        #clean data
        trainingsSet = self._cleanData(trainingsSet)
        trainingsSet = self._removeOutliers(trainingsSet)

        #Split the data into variables and results
        X = trainingsSet[["SPEED", "TRACK_POSITION", "ANGLE_TO_TRACK_AXIS",
                                 "TRACK_EDGE_0", "TRACK_EDGE_1", "TRACK_EDGE_2", "TRACK_EDGE_3", "TRACK_EDGE_4", "TRACK_EDGE_5",
                                  "TRACK_EDGE_6", "TRACK_EDGE_7", "TRACK_EDGE_8", "TRACK_EDGE_9", "TRACK_EDGE_10", "TRACK_EDGE_11",
                                   "TRACK_EDGE_12", "TRACK_EDGE_13", "TRACK_EDGE_14", "TRACK_EDGE_15", "TRACK_EDGE_16", "TRACK_EDGE_17",
                                     "TRACK_EDGE_18"]]
        Y = trainingsSet[["ACCELERATION", "BRAKE", "STEERING"]]

        # # Create linear regression object
        # regr = linear_model.LinearRegression()

        # # Train the model using the training set
        # regr.fit(X, Y)

        # regr = self.normalEquation(X, Y)
        
        self.regressor = self.scikitMLP(X, Y)
        self._save()

    def _predict(self, df):
        return self.regressor.predict(df)
        # return np.dot(df, self.regressor)

    def _save(self):
        pickle.dump(self.regressor, open(self.modelPath, 'wb'))

    def _load(self):
        loadedModel = pickle.load(open(self.modelPath, 'rb'))
        self.regressor = loadedModel

    def _removeOutliers(self, df):
        df = df[(np.abs(stats.zscore(df, axis=0))<4).all(axis=1)]
        df.reset_index(inplace=True)
        return df
    
    def _cleanData(self, df):
        #remove entries where distance raced is 0
        df = df[df["SPEED"] >= 0]
        df.reset_index(inplace=True)
        return df
    
    def getGear(self, speed):
        gear = 1
        if speed > 50:
            gear = (speed + 10) // 30
        return gear