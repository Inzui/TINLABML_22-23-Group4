import enum, socket
import logging
import os
import time
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

    def __init__(self, hostname="localhost", port=3001):
        self.hostaddr = (hostname, port)
        self.serializer = Serializer()
        self.state = State.STOPPED
        self.socket = None

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

        angles = -90, -75, -60, -45, -30, -20, -15, -10, -5, 0, 5, 10, 15, 20, 30, 45, 60, 75, 90
        assert len(angles) == 19, f"Inconsistent length {len(angles)} of range of finder iterable."

        data = {"init": angles}
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

                logger.info(carState.getJSON())

                command = CommandDto()
                command.gear = 1
                command.accelerator = 1
                command.steering = -1

                buffer = self.serializer.encode(command.actuator_dict)
                self.socket.sendto(buffer, self.hostaddr)

        except socket.error as ex:
            print(f"Communication with server failed: {ex}.")

        except KeyboardInterrupt:
            print("User requested shutdown.")
            self.stop()

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