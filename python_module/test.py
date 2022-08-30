from SharedMemoryTCP import SharedMemoryTCP
import time
import ctypes

import random





SharedMem = SharedMemoryTCP()
SharedMem.start()
while True:
    #random float
    rand_float = random.uniform(0.0,1.0)
    SharedMem.set_var("tensor",[1.0,rand_float,3.0])
    
    
   
    