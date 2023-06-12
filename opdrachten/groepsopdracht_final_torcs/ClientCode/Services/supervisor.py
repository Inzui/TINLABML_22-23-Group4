from Dto.commandDto import CommandDto
from Drivers.driverInterface import DriverInterface
from Services.memoryService import MemoryService
from datetime import timedelta

import os, shutil
import pandas as pd
import numpy as np

class Supervisor():
    def __init__(self, driver: DriverInterface, training = False):
        self.training = training
        self.driver = driver
        self.driver.start()

        self.trainingSetDir = os.path.abspath(os.path.join(__file__, "..", "..", "Models"))
        self.bestTrainingSetPath = os.path.join(self.trainingSetDir, "BestTrainingSet.csv")
        self.driver.trainingSetPath = os.path.join(self.trainingSetDir, "TrainingSet.csv")
        self.lapTimePath = os.path.join(self.trainingSetDir, "FastestLap.txt")

        self.bestLapTime = MemoryService.loadFastestLapTime(self.lapTimePath)
        self.lastLapTime = 0
        self.improvementsCount = 0

        if (os.path.exists(self.bestTrainingSetPath)):
            shutil.copy(self.bestTrainingSetPath, self.driver.trainingSetPath)
        self.df = pd.read_csv(self.driver.trainingSetPath)
        self.timeOfTrack = 0

    def run(self, carState: dict, command: CommandDto):
        if (self.training):
            command.meta = float(self.edgeDetected(carState["track"], carState["curLapTime"]))
            if (command.meta == 1.0):
                self.amountOfTrack = 0
                self.lastLapTime = 10000
            elif (carState["lastLapTime"] > 0):                 # If the car has finished the lap, restart the simulation.
                command.meta = 1
                self.lastLapTime = carState["lastLapTime"]
            
    def retrain(self):
        print(f"Lap finished: Best lap time: '{str(timedelta(seconds = self.bestLapTime))}', Current lap time: '{str(timedelta(seconds = self.lastLapTime))}'.")

        if (self.lastLapTime < self.bestLapTime):               # If the last lap time is better, keep the new training set.
            self.improvementsCount += 1
            self.bestLapTime = self.lastLapTime
            print(f"New best lap time (Improvement #{self.improvementsCount}): '{str(timedelta(seconds = self.bestLapTime))}'.")

            MemoryService.writeFastestlapTime(self.lapTimePath, self.bestLapTime)
            shutil.copy(self.driver.trainingSetPath, self.bestTrainingSetPath)

        shutil.copy(self.bestTrainingSetPath, self.driver.trainingSetPath)

        print("Training driver...")

        if(not self.lastLapTime == 0):
            self._genNewTrainingSet()
        
        self.driver.train()
    
    def edgeDetected(self, trackData: list, time: float) -> bool:
        timeElapsed = 0
        if (max(trackData) == -1.0): 
            if(self.timeOfTrack == 0):
                self.timeOfTrack = time
            timeElapsed = time - self.timeOfTrack
        else:
            self.timeOfTrack = 0
        print(timeElapsed)

        return timeElapsed > 2

    def _genNewTrainingSet(self):                                                
        print("Generating new training set...")
        self.df = pd.read_csv(self.driver.trainingSetPath, sep=',')
        self._augmentData()
        self.df.to_csv(self.driver.trainingSetPath, sep=',', index=False) 
        
    def _augmentData(self):
        columns = ["ACCELERATION", "BRAKE", "STEERING"]

        tempDf = self.df[columns]
        self.df = self.df.drop(columns, axis = 1)

        self.df = self.df.applymap(self._add_noise)

        for column in columns:
            self.df[column] = tempDf[column].values

    def _add_noise(self, data, noise_scale=0.01):
        noise = np.random.normal(0, noise_scale)
        return data + noise