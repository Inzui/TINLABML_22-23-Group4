from Drivers.driverInterface import *
from Dto.commandDto import CommandDto

import numpy as np
import pandas as pd
import pickle, os

class DriverRegression(DriverInterface):
    def __init__(self):
        self.regressor = None
        self.modelDir = os.path.abspath(os.path.join(__file__, "..", "..", "Models"))
        # self.trainingSetPath = os.path.join(self.modelDir, "BestTrainingSet.csv")
        self.trainingSetPath = "/vagrant/Logs/train_data/manual_combined.csv"
        self.modelPath = os.path.join(self.modelDir, "modelNewData.sav")
        # self.train()
        try:
            self._load()
            print('model loaded')
        except FileNotFoundError:
            print('no model found')
        self.lastgear = 1
    
    def drive(self, carState: dict) -> CommandDto:
        command = CommandDto()
        currentState = np.array([carState["speed"][0], carState["trackPos"], carState["angle"], 
                                    carState["track"][0], carState["track"][1], carState["track"][2], carState["track"][3], carState["track"][4],
                                    carState["track"][5], 
                                    carState["track"][9], 
                                    carState["track"][13], carState["track"][14], carState["track"][15], carState["track"][16], carState["track"][17], carState["track"][18],
                                    np.mean([carState["track"][6], carState["track"][7], carState["track"][8]]),
                                    np.mean([carState["track"][10], carState["track"][11], carState["track"][12]])])
        
        
        action = self._predict([currentState])

        command.gear = self.getGear(carState['speed'][0],action[0][0])
        command.accelerator = action[0][0]
        command.brake = action[0][1]
        command.steering = action[0][2]

        return command

    def _predict(self, df):
        return self.regressor.predict(df)
        # return np.dot(df, self.regressor)

    def _load(self):
        loadedModel = pickle.load(open(self.modelPath, 'rb'))
        self.regressor = loadedModel
    
    def getGear(self, speed, accel):
        gear = 1
        if speed > 50:
            gear = (speed + 10) // 30
            if self.lastgear > gear and accel >0.5:
                gear = self.lastgear
        self.lastgear = gear
        return gear