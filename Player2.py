import random
from time import sleep
class player:
    def __init__(self):
        pass

    def move(self,B,N,cur_x,cur_y):
        if random.randint(0,2)==0:
            return (0,random.choice([-1,1]))
        else:
            return (random.choice([-1,1]),0)
