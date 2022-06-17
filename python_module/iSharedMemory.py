

from posixpath import split
import socket
from threading import Thread


class SharedMemory():
    
    def __init__(self,data) -> None:
        self.data = data
        self.serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.serversocket.bind((socket.gethostname(), 80))
        self.connection = None
        self.clientaddress = None
        
        
    def start(self):
            self.serversocket.listen(5)
            (clientsocket, address) = self.serversocket.accept()
            self.connection = clientsocket
            self.clientaddress = address
            t1 = Thread(target = self.connection_handler)
            t1.start()
            
    def connection_handler(self):
        while True:
            data = self.connection.recv(1024)
            if not data:
                continue
            print(data.decode())
            split = data.decode().split(",")
            
            match split[0]:
                case ["cmd"]:
                    pass
                case ["set"]:
                    try:
                        type_of = type(self.data[split[1]])
                        self.data[split[1]]= type_of(split[2])
                    except(TypeError,ValueError) as e:
                        pass
                case ["get"]:
                    self.send_data()
            
            
    def set_data(self,key,value):
        self.data[key] = value
    
    def get_data(self,key):
        return self.data[key]
        
    def initialize(self):
        msg = "initialize" +","+ str(self.data)
        self.connection.send(msg.encode())
        
    def share_value(self,key):
        msg = "set" + "," + key + "," + str(self.data[key])
        self.connection.send(msg.encode())
    
    def send_command(self,command):
        self.connection.send(str(command).encode())