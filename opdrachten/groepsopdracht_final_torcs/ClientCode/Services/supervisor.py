from Dto.commandDto import CommandDto
from Drivers.driverInterface import DriverInterface
import os, shutil, logging, time
import pandas as pd
import numpy as np

class Supervisor():
    def __init__(self, driver: DriverInterface, training = False):
        self.training = training
        self.driver = driver
        self.driver.start()

        self.bestLapTime = 1000000
        self.lastLapTime = 0

        self.trainingSetDir = os.path.join(os.getcwd(), "Models")
        self.bestTrainingSetPath = os.path.join(self.trainingSetDir, "BestTrainingSet.csv")
        self.driver.trainingSetPath = os.path.join(self.trainingSetDir, "TrainingSet.csv")
        self.df = pd.read_csv(self.driver.trainingSetPath)

    def run(self, carState: dict, command: CommandDto):
        if (self.training and carState["lastLapTime"] > 0):     # If the car has finished the lap, restart the simulation.
            command.meta = 1
            self.lastLapTime = carState["lastLapTime"]
            
    def retrain(self):
        print(f"Lap finished: Best lap time: '{self.bestLapTime}', Current lap time: '{self.lastLapTime}'.")

        if (self.lastLapTime < self.bestLapTime):               # If the last lap time is better, keep the new training set.
            print(f"New best lap time: '{self.lastLapTime}'.")
            self.bestLapTime = self.lastLapTime
            shutil.copy(self.driver.trainingSetPath, self.bestTrainingSetPath)

        shutil.copy(self.bestTrainingSetPath, self.driver.trainingSetPath)

        self._genNewTrainingSet()
        self.driver.train()

    def _genNewTrainingSet(self):                                                
        print("Generating new training set...")
        self.df = pd.read_csv(self.driver.trainingSetPath, sep=';')
        self._augmentData()
        self.df.to_csv(self.driver.trainingSetPath, sep=';', index=False) 
        
    def _augmentData(self):
        self.df = self.df.applymap(self._add_noise)

    def _add_noise(self, data, noise_scale=0.1):
        noise = np.random.normal(0, noise_scale)
        return data + noise