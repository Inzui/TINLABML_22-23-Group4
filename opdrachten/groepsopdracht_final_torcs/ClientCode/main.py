from Services.torcsClient import TorcsClient
from Services.machineLearning.machineLearning import MachineLearning
import os
import pandas as pd
import numpy as np

def main():
    machineLearning = MachineLearning()
    machineLearning.train()
    
    client = TorcsClient()
    client.run()

if __name__ == '__main__':
    main()