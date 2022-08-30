from atexit import register
import json
from flask import Flask,jsonify,session
import threading
from flask_classful import FlaskView,route
import logging


class Data:
    data = {}

    def setData(self,data):
        self.data = data
        return data
    
    def getData(self):
        return self.data
    
    def setValue(self,key,value):
        self.data[key] = value
        return self.data[key]
    
    def getValue(self,key):
        return self.data[key]
    
    def deleteData(self,key):
        del self.data[key]
        return self.data
    
    def renameRecord(self,oldName,newName):
        self.data[newName] = self.data[oldName]
        del self.data[oldName]
        return self.data
    

class SharedMemoryHTTP():
    app = Flask(__name__)
    onDataRecieved = lambda x: None
    onDataSendt = lambda x: None
    DataCollection = None
    
    
    def __init__(self):
        data = Data()
        data.setValue("tensor",[0.0,0.0,0.0])
        log = logging.getLogger('werkzeug')
        log.setLevel(logging.ERROR)
        self._startSharedMem()
        
      

    def _startSharedMem(self):
        t1 = threading.Thread(target=self.app.run)
        t1.start()

    def _start(self):
       self.app.run(debug=True, threaded=True)
       
    @app.route("/")
    def index():
        _data = Data()
        return jsonify(_data.getData())
       
    
    @app.route('/set/<key>/<value>')
    def setValue(self,key,value):
        _data = Data()
        new_val = self.stringToFloatArr(value)
       # _data.setValue(key,value)
        return jsonify(_data.getData())
    
    
    def setVariable(self,key,value):
        _data = Data()
        _data.setValue(key,value)
        

    def getVariable(self,key):
        _data = Data()
        _data.getValue(key)
      
    
    
    def stringToFloatArr(self,data):
        data = data.replace("[","")
        data = data.replace("]","")
        new_data = data.split(",")
        print(new_data)
        


   


    