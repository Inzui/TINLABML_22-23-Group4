import argparse
from Services.torcsClient import TorcsClient
from Drivers.driverRegression import DriverRegression
from Drivers.driverPid import DriverPid

def main(ipaddress: str, port: int):
    if (ipaddress == None):
        ipaddress = "localhost"
    if (port == None):
        port = 3001

    # client = TorcsClient(DriverPid(maxGear = 4, maxCornerSpeed = 50, brakingDistance = 90, finishAccelerationTime = 3), training = False, speedUp = False)
    client = TorcsClient(DriverRegression(), training = False, hostname = ipaddress, port = port)
    client.run()

if __name__ == '__main__':
    argParser = argparse.ArgumentParser()
    argParser.add_argument("-i", "--ipaddress", type = str, help = "Torcs Server IP-Address")
    argParser.add_argument("-p", "--port", type = int, help = "Torcs Server Port")
    args = argParser.parse_args()

    main(args.ipaddress, args.port)