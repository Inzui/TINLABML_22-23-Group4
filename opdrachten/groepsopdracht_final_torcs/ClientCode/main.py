from Services.torcsClient import TorcsClient
import os
import pandas as pd
import numpy as np

def main():
    client = TorcsClient()
    client.run()

if __name__ == '__main__':
    main()