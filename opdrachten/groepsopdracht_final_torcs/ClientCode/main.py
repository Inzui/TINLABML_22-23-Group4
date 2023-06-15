import argparse
from Services.torcsClient import TorcsClient
from Drivers.driverRegression import DriverRegression
from Drivers.driverPid import DriverPid

def main(ipaddress: str, port: int, training: bool):
    if (ipaddress == None):
        ipaddress = "192.168.56.20"
    if (port == None):
        port = 3001
    if (training == None):
        training = False

    # client = TorcsClient(DriverPid(maxGear = 4, maxCornerSpeed = 50, brakingDistance = 90, finishAccelerationTime = 3), training = False, speedUp = False)
    client = TorcsClient(DriverRegression(), training = training, hostname = ipaddress, port = port)
    client.run()

if __name__ == '__main__':
    argParser = argparse.ArgumentParser()
    argParser.add_argument("-i", "--ipaddress", type = str, help = "Torcs Server IP-Address")
    argParser.add_argument("-p", "--port", type = int, help = "Torcs Server Port")
    argParser.add_argument("-t", "--training", type = bool, help = "Go into training mode (unavailable when using Docker)")
    args = argParser.parse_args()

    main(args.ipaddress, args.port, args.training)