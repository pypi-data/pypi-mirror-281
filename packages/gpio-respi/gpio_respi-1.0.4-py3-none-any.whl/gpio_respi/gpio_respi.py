import socket
import pickle
import struct
import sg90
import time
class gpio_respi:
    # client_socket = socket.socket()
    server_ip = ("127.0.0.1", 6686)
    BCM = "bcm"
    OUT = "out"
    IN = "in"
    HIGH = "high"
    LOW = "low"

    def __init__(self):
        self.mode = None
        self.port = {}
        self.power = None
        self.now_port = None
        self.run_type = None

    def connect_server(self):
        pass

    def setmode(self, bcm):
        self.mode = gpio_respi.BCM

    def getmode(self):
        return self.mode

    def setup(self, port, type1):
        self.port[port] = type1

    def getport(self):
        return self.port

    def output(self, port, type2):
        client_socket = socket.socket()
        client_socket.connect(gpio_respi.server_ip)
        self.now_port = port
        self.power = type2
        self.run_type = "output"
        len_self = len(pickle.dumps(self))
        len_self = struct.pack('i', len_self)
        client_socket.send(len_self)
        client_socket.send(pickle.dumps(self))
        client_socket.close()

    def input(self, port):
        client_socket = socket.socket()
        client_socket.connect(gpio_respi.server_ip)
        self.now_port = port
        self.run_type = "input"
        len_self = len(pickle.dumps(self))
        len_self = struct.pack('i', len_self)
        client_socket.send(len_self)
        client_socket.send(pickle.dumps(self))

        recv_len = struct.unpack('i', client_socket.recv(4))[0]
        recv_data = client_socket.recv(recv_len).decode('utf-8')
        print(recv_data)
        client_socket.close()
        return 0

    def printself(self):
        print(f"mode:{self.mode}")
        print(f"port:{self.port}")
        print(f"power:{self.power}")
        print(f"now_port:{self.now_port}")

    def PWM(self, port, hz):
        _sg90 = sg90(gpio_respi.server_ip)
        _sg90.set_port_hz(port, hz)
        return _sg90

GPIO = gpio_respi()
