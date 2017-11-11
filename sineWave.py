import math
import time

numCycle=5
pi=math.pi

def sin(x):
    return math.sin(x)

x=0

while x < (numCycle*2*pi):
      bar=int(20*sin(x))
      x+=0.3
      print((21+bar)*'=')
      time.sleep(0.03)
