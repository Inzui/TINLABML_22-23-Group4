from Services.torcsClient import TorcsClient
from Drivers.driverRegression import DriverRegression
from Drivers.driverPid import DriverPid

def main():
    # client = TorcsClient(DriverPid(maxGear = 4, maxCornerSpeed = 50, brakingDistance = 90, finishAccelerationTime = 3), training = False, speedUp = False)
    client = TorcsClient(DriverRegression(), training = False, hostname = "192.168.56.20")
    client.run()

if __name__ == '__main__':
    main()