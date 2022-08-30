from iSharedMemory import SharedMemory as SM
import time
import random

data = {
 "tensor": [0.0,0.0,0.0],
 "tensor2": [0.0,0.0,2.0]   
}

def onAfterRecieve(data):
    pass


SharedMem = SM(data=data)
SharedMem.start()
if SharedMem.connection != None:
    SharedMem.share_mem("tensor",[1.0,2.0,3.0])

SharedMem.onAfterRecieve = onAfterRecieve
while True:
    #random float
    rand_float = random.uniform(0.0,1.0)
    SharedMem.share_mem("tensor",[1.0,rand_float,3.0])
   
   
    
    