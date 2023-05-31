import enum, socket
import logging
import os
import time
import json
import pandas as pd
import numpy as np
from Dto.carStateDto import CarStateDto
from Dto.commandDto import CommandDto


#logging parameters
LOG_PATH = "../../home/vagrant/Documents/Logs"
if (not os.path.exists(LOG_PATH)):
    os.mkdir(LOG_PATH)
logging.basicConfig(filename=os.path.join(LOG_PATH, f"Race Log - {time.ctime(time.time())}.log"), 
                    level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', 
                    datefmt='%Y-%m-%d %H:%M:%S')
logger = logging.getLogger(__name__)

# special messages from server:
MSG_IDENTIFIED = b"***identified***"
MSG_SHUTDOWN = b"***shutdown***"
MSG_RESTART = b"***restart***"

# timeout for socket connection in seconds and msec:
TO_SOCKET_SEC = 1
TO_SOCKET_MSEC = TO_SOCKET_SEC * 1000

class TorcsClient:
    """Client for TORCS racing car simulation with SCRC network server.

    Attributes:
        hostaddr (tuple): Tuple of hostname and port.
        port (int): Port number to connect, from 3001 to 3010 for ten clients.
        driver (Driver): Driving logic implementation.
        serializer (Serializer): Implementation of network data encoding.
        state (State): Runtime state of the client.
        socket (socket): UDP socket to server.
    """

    def __init__(self, regr, hostname="localhost", port=3001):
        self.hostaddr = (hostname, port)
        self.serializer = Serializer()
        self.state = State.STOPPED
        self.socket = None
        self.regr = regr
        self.dataFrame = pd.DataFrame()

    def run(self):
        """Enters cyclic execution of the client network interface."""

        if self.state is State.STOPPED:
            print("Starting cyclic execution.")

            self.state = State.STARTING

            try:
                print(f"Registering driver client with server {self.hostaddr}.")
                self._configure_udp_socket()
                self._register_driver()
                self.state = State.RUNNING
                print("Connection successful.")

            except socket.error as ex:
                print(f"Cannot connect to server: {ex}")
                self.state = State.STOPPED

        while self.state is State.RUNNING:
            self._process_server_msg()

        print("Client stopped.")
        self.state = State.STOPPED

    def stop(self):
        """Exits cyclic client execution (asynchronously)."""
        if self.state is State.RUNNING:
            print("Disconnecting from racing server.")
            self.state = State.STOPPING

    def _configure_udp_socket(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.settimeout(TO_SOCKET_SEC)

    def _register_driver(self):
        """
        Sends driver"s initialization data to server and waits for acceptance
        response.
        """

        self.angles = -90, -75, -60, -45, -30, -20, -15, -10, -5, 0, 5, 10, 15, 20, 30, 45, 60, 75, 90
        assert len(self.angles) == 19, f"Inconsistent length {len(self.angles)} of range of finder iterable."

        data = {"init": self.angles}
        buffer = self.serializer.encode(
            data,
            prefix = f"SCR-{self.hostaddr[1]}"
        )

        print("Registering client.")

        connected = False
        while not connected and self.state is not State.STOPPING:
            try:
                print(f"Sending init buffer {buffer}.")
                self.socket.sendto(buffer, self.hostaddr)

                buffer, _ = self.socket.recvfrom(TO_SOCKET_MSEC)
                print(f"Received buffer {buffer}.")
                if MSG_IDENTIFIED in buffer:
                    print("Server accepted connection.")
                    connected = True

            except socket.error as ex:
                print(f"No connection to server yet ({ex}).")

    def _process_server_msg(self):
        try:
            buffer, _ = self.socket.recvfrom(TO_SOCKET_MSEC)
            if not buffer:
                return
            elif MSG_SHUTDOWN in buffer:
                print("Server requested shutdown.")
                self.stop()
            elif MSG_RESTART in buffer:
                print("Server requested restart of driver.")
            else:
                sensor_dict = self.serializer.decode(buffer)
                carState = CarStateDto(sensor_dict)
                print(carState)

                data = carState.getDict()
                self._preprocessing(data)
    	        
                self.printAllData(data)
                self._updateDataFrame(data)

                arr = np.array([data['speed'][0], data['speed'][1], data["speed"][2], data["angle"], data["location"][2], data["trackPos"], data["distFromStart"]]).astype(float)
                print (arr)
                logger.info(json.dumps(data))
                
                action = self.regr.predict([arr])
                print(action)
                command = CommandDto()

                #implemented automatic gear, from 50 it shifts up every 30 km/h faster, 
                #when using it right now, the car starts to wobble and crashes.
                #command.gear = self.getGear(data['speed'][0])
                command.gear = 1
                command.accelerator = action[0][0] if float(data["distFromStart"]) < 3200 else 1
                command.steering = action[0][1]

                buffer = self.serializer.encode(command.actuator_dict)
                self.socket.sendto(buffer, self.hostaddr)

        except socket.error as ex:
            print(f"Communication with server failed: {ex}.")

        except KeyboardInterrupt:
            print("User requested shutdown.")
            self.stop()

    def getGear(self, speed):
        gear = 1
        if speed > 50:
            gear = (speed + 10) // 30
        return gear

    def printAllData(self, data):
        [print(key, "->", data[key]) for key in data]

    def _updateDataFrame(self, data):
        #If the dataframe hasn't been initialised before, we 
        #do it here with the column names
        if self.dataFrame.empty:
            self.dataFrame = pd.DataFrame(columns=list(data.keys()))
        
        index = len(self.dataFrame)

        #We have to add each value individualy using 'at', 
        #because otherwise panda's won't allow the use of a list
        #as a single cell value
        for key in data:
            self.dataFrame.at[index, key] = data[key]
        #print(self.dataFrame)

    def _preprocessing(self, data):
        #Cleaning
        #Possibly other things: angle
        uselessData = ["damage", "fuel", "focus", "roll", "pitch", "yaw", "speedGlobalX", "speedGlobalY", "gear", "rpm", "wheelSpinVel"]
        for dataKey in uselessData:
            data.pop(dataKey)

        #Normalization
        #Speed to one vector
        speedX = data.pop("speedX")
        speedY = data.pop("speedY")
        speedZ = data.pop("speedZ")
        speed = {"speed" : (float(speedX), float(speedY), float(speedZ))}
        data.update(speed)

        #Location to one vector
        x = data.pop("x")
        y = data.pop("y")
        z = data.pop("z")
        location = {"location" : (float(x), float(y), float(z))}
        data.update(location)

        #Remove unnecassary opponent info
        opponents = data.pop("opponents")
        opponentsDict = {}
        for i in range(len(opponents)):
            if(opponents[i] != "200"):
                #Add dict, where {key = angle : value = distance} (0 degrees is the rear of the car)
                opponentsDict.update({i*10 : float(opponents[i])})
        data.update({"opponents": opponentsDict})

        for key in data:
            if(isinstance(data[key], str)):
                data.update({key: float(data[key])})
            elif(isinstance(data[key], list)):
                floatList = [float(x) for x in data[key]]
                data.update({key: tuple(floatList)})





class State(enum.Enum):
    STOPPED = 1,
    STARTING = 2,
    RUNNING = 3,
    STOPPING = 4,

class Serializer:
    @staticmethod
    def encode(data, *, prefix=None):
        """Encodes data in given dictionary.

        Args:
            data (dict): Dictionary of payload to encode. Values are arrays of
                numbers.
            prefix (str|None): Optional prefix string.

        Returns:
            Bytes to be sent over the wire.
        """
        elements = []

        if prefix:
            elements.append(prefix)

        for k, v in data.items():
            if v and v[0] is not None:
                # string version of number array:
                vstr = map(lambda i: str(i), v)

                elements.append("({} {})".format(k, " ".join(vstr)))

        return "".join(elements).encode()

    @staticmethod
    def decode(buff):
        """
        Decodes network representation of sensor data received from racing
        server.
        """
        d = {}
        s = buff.decode()

        pos = 0
        while len(s) > pos:
            start = s.find("(", pos)
            if start < 0:
                # end of list:
                break

            end = s.find(")", start + 1)
            if end < 0:
                print(f"Opening brace at position {start} not matched in buffer {buff}.")
                break

            items = s[start + 1:end].split(" ")
            if len(items) < 2:
                print(f"Buffer {buff} not holding proper key value pair.")
            else:
                key = items[0]
                if len(items) == 2:
                    value = items[1]
                else:
                    value = items[1:]
                d[key] = value

            pos = end + 1

        return d