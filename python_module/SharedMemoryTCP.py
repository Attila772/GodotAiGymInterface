import json
from multiprocessing.sharedctypes import Value
from sqlite3 import connect
import threading
import ctypes
import socket


kernel32 = ctypes.windll.kernel32
kernel32.SetThreadPriority(kernel32.GetCurrentThread(), 31)
timer = kernel32.CreateWaitableTimerA(ctypes.c_void_p(), True, ctypes.c_void_p())
delay = ctypes.c_longlong(1000000)
kernel32.SetWaitableTimer(timer, ctypes.byref(delay), 0, ctypes.c_void_p(), ctypes.c_void_p(), False)

class SharedMemoryTCP():
    def __init__(self,data = {}):
        self.data = data
        self.serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.serversocket.bind(("127.0.0.1", 8000))
        print(socket.gethostname(),"8000")
        self.connection = None
        self.clientaddress = None
        self.onAfterRecieve = lambda x: None
        
    def start(self):
        print("waiting for client")
        self.serversocket.listen(5)
        (clientsocket, address) = self.serversocket.accept()
        print("client connected")
        self.connection = clientsocket
        self.clientaddress = address
        t1 = threading.Thread(target = self.connection_handler)
        t1.start()
        
        
    def connection_handler(self):
        while True:
            data = self.connection.recv(1024)
            if not data:
                continue      
            received = received.decode("utf-8")
            data = json.load(received)
            match data["cmd"]:
                case "get":
                    json_data = json.dumps(self.data)
                    self.connection.send(json_data.encode())
                case "set":  
                    self.data[data["name"]] = data["value"]
                    pass
                    
            
    def set_var(self,name,value):
        kernel32.WaitForSingleObject(timer, 0xffffffff)
        self.data[name] = value
        jsontosend = self.data
        jsontosend["cmd"] = "set"
        self.connection.send(json.dumps(self.data).encode())
        
    def set_var_locally(self,name,value):
        self.data[name] = value