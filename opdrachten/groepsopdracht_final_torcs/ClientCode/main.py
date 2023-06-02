from Services.torcsClient import TorcsClient
from Drivers.driverRegression import DriverRegression

def main():
    client = TorcsClient(DriverRegression())
    client.run()

if __name__ == '__main__':
    main()