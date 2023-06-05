from Services.torcsClient import TorcsClient
from Drivers.driverRegression import DriverRegression

def main():
    client = TorcsClient(DriverRegression(), training = True)
    client.run()

if __name__ == '__main__':
    main()