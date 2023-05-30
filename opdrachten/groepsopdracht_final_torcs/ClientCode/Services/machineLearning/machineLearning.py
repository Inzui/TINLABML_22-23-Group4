import numpy as np
import pandas as pd
import pickle
from scipy import stats
from sklearn import linear_model
from sklearn.neural_network import MLPRegressor

trainingSetPath = "/vagrant/torcs-ai_client_examples/scr-client-cpp/data/forza_2023-05-19.csv"
modelPath = "/vagrant/ClientCode/Services/machineLearning/model.sav"

class MachineLearning:
    def __init__(self):
        try:
            self.regressor = self.load()
            print('model loaded')
        except FileNotFoundError:
            self.regressor = self.train()
            self.save()
            print('model trained and saved')

    def train(self):
        #Load the csv 
        data = pd.read_csv(trainingSetPath, 
                        sep=';', index_col=False, header=0,
                        usecols=["s_speed_x", "s_speed_y", "s_speed_z", "s_angle", "s_z", "s_track_position", "a_accelation", "a_steer", "s_distance_from_start"])
        
        #remove outliers
        data = self._removeOutliers(data)

        #Split the data into variables and results
        X = data[["s_speed_x", "s_speed_y", "s_speed_z", "s_angle", "s_z", "s_track_position", "s_distance_from_start"]]
        Y = data[["a_accelation", "a_steer"]]

        # Create linear regression object
        regr = linear_model.LinearRegression()

        # Train the model using the training set
        regr.fit(X, Y)
        return regr

    def predict(self, df):
        pass

    def save(self):
        pickle.dump(self.regressor, open(modelPath, 'wb'))

    def load(self):
        loadedModel = pickle.load(open(modelPath, 'rb'))
        return loadedModel

    def _removeOutliers(self, df):
        df = df[(np.abs(stats.zscore(df, axis=0))<4).all(axis=1)]
        df.reset_index(inplace=True)
        return df