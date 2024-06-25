import socket
import pickle
import struct
class sg90:
    def __init__(self,server_ip):
        self.port = None
        self.hz = None
        self.start_duty_cycle = None
        self.change_duty_cycle = None
        self.run = "start"
        self.server_ip = server_ip

    def set_run(self, str_run):
        self.run = str_run

    def get_run(self):
        return self.run

    def get_start(self):
        return self.start_duty_cycle

    def get_change(self):
        return self.change_duty_cycle

    def set_serip(self, server_ip):
        self.server_ip = server_ip

    def set_port_hz(self, port, hz):
        self.port = port
        self.hz = hz

    def get_port_hz(self):
        return self.port, self.hz

    def start(self, duty_cycle):
        self.start_duty_cycle = duty_cycle
        self.run = "start"
        client_socket = socket.socket()
        client_socket.connect(self.server_ip)
        len_self = len(pickle.dumps(self))
        len_self = struct.pack('i', len_self)
        client_socket.send(len_self)
        client_socket.send(pickle.dumps(self))
        client_socket.close()

    def ChangeDutyCycle(self, duty_cycle):
        self.change_duty_cycle = duty_cycle
        self.run = "change"
        client_socket = socket.socket()
        client_socket.connect(self.server_ip)
        len_self = len(pickle.dumps(self))
        len_self = struct.pack('i', len_self)
        client_socket.send(len_self)
        client_socket.send(pickle.dumps(self))
        client_socket.close()

    def ChangeFrequency(self, fre):
        self.hz = fre

    def printself(self):
        print(f"hz:{self.hz}")
        print(f"port:{self.port}")
        print(f"duty_cycle:{self.duty_cycle}")
        print(f"server_ip:{self.server_ip}")






