from SharedMemoryTCP import SharedMemoryTCP
import time


import random



def example():
    pass



SharedMem = SharedMemoryTCP()
SharedMem.onAfterRecieve = example
SharedMem.start()

while True:
    #random float
    rand_float = random.uniform(0.0,1.0)
    SharedMem.set_var("tensor",[1.0,rand_float,3.0])
    
    
   
    