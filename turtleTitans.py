# Turtle Titans
# Thomas Bailey


import cmath
import math
import random
import queue
import turtle
from threaded_turtle import ThreadSerializer, TurtleThread

# ===========
# DEFINITIONS
# ===========

# turtles
scale = 10
start_speed = 10
start_size = 10

# ===========
# CLASSES
# ===========

class titan(turtle.Turtle):
    scale = 10
    start_speed = 10
    start_size = 10
    
    turtle.titans = []
    """ A version of turtle I will use for combat and stuff so it can move """
    def __init__(self, name, x, y, heading, size, sight_range, *args, **kwargs):
        # x, y, heading(angle), size(int), sight_range(int)
        super(titan, self).__init__(*args, **kwargs)

        # position / graphics
        self.pu() # pen up
        self.setposition(x, y) # placement

        # math
        self.radians()

        # attributes
        self.name = name
        self.sight_range = sight_range
        
        #  size
        self.size = size
        self.shapesize(1 + (size/4), 1 + (size/4), 1) # size length, size width, outline size
        
        # AI flags
        self.hunting = False
        self.fleeing = False
    
        turtle.titans.append(self)

    def __repr__(self):
        return self.name
    
    def think(self):
        # Forget about last cycle

        # Who is close to me? (Primary)
        self.titan_dist = sorted(turtle.titans, key=lambda titan: self.distance(titan.xcor(), titan.ycor()), reverse = False)
        
        #self.primary = min(turtle.titans, key = lambda titan: self.distance(titan.pos())) 
            
        # Anyone in range who's bigger than me?
        for titan in self.titan_dist:
            if self.distance(titan) > self.sight_range:
                self.fleeing = False
                break # Nope
            if titan.size > self.size:
                self.primary = titan
                self.fleeing = True
                return # Yep, forget about hunting
        
        # No? Anyone in range I 'm bigger than?
        for titan in self.titan_dist:
            if self.distance(titan) > self.sight_range:
                self.hunting = False
                break # Nope
            if titan.size < self.size:
                self.primary = titan
                self.hunting = True
                return # It's killing time!

    def step(self, commander):
        # Angle
        if self.hunting:
            self.direction = self.towards(self.primary.pos())
        elif self.fleeing:
            self.direction = self.towards(self.primary.pos()) - cmath.pi
        else:
            self.direction = random_angle()
            
        commander.seth(self.direction)
        commander.forward(scale+self.size)
            
    def start(self, commander):
        while True:
            self.think()
            self.step(commander)
            
# ===========
# FUNCTIONS
# ===========

# random

def random_angle():
    """ Returns random radian angle in range (-π, π) """
    return (random.random() * cmath.pi) * random.choice([1, -1])
    
# math

boomer = titan("boomer", 10, 10, random_angle(), 5, 200)
killer = titan("killer", -10, -10, random_angle(), 1, 200)
bomber = titan("bomber", -20, 20, random_angle(), 5, 200)
stabber = titan("stabber", 0, 50, random_angle(), 1, 200)

# GAME LOOP
turn = 0
ctrl = ThreadSerializer()
threads = []
for titan in turtle.titans:
    tt = TurtleThread(ctrl, titan, target = titan.start)
    tt.daemon = True
    tt.start()
for tt in threads:
    tt.start()
try:
    ctrl.run_forever(1)
except queue.Empty:
    print('Done')
