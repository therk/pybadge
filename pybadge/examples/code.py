'''
circuitpython-badge/minimal_examples/timers.py
This is an example that demonstrates how you can move towards more complex programs with
multiple things happening at once (in truth the microcontroller can only do one thing at a
time and we are still working with a procedural program). The example takes time stamps so we
can test if x amount of time has passed, and if so then make something happen!
Aidan T 2018
'''

import badge
import time

badge.init()

p = badge.Pix() # initialise the led matrix

t1 = time.time() # sample the current time since you powered on in seconds
t2 = time.time() # another time sample!

interval1 = 1 # to test for a 1 second interval
interval2 = 3 # to test for a 3 second interval

# let's make some matrix functions to play with

l = 0
r = 0

def flashleftbar():
    global l

    l = not l

    for y in range(11):
        p.pixel(3, y, l)

    #badge.show(p)

def flashrightbar():
    global r

    r = not r

    for y in range(11):
        p.pixel(10, y, r)

    #badge.show(p)

while True:
    if (time.time() - t1) >= interval1:
        t1 = time.time() # update time sample 1
        flashleftbar()

    if (time.time() - t2) >= interval2:
        t2 = time.time() # update time sample 2
        flashrightbar()

    badge.show(p)
