#!/usr/bin/env python3

# setup

import time
import RPi.GPIO as g

#g.cleanup()
#g.setwarnings(False)
#g.setmode(g.BOARD)

#pin_1 = 37
#pin_2 = 35
#pin_3 = 33
#pin_4 = 31

pin_1 = 26
pin_2 = 19
pin_3 = 13
pin_4 = 6

# lib

from RpiMotorLib import RpiMotorLib as l

pins = [pin_1, pin_2, pin_3, pin_4]

m = l.BYJMotor("name", "28BYJ")
time.sleep(1)

m.motor_run(pins,verbose=1, steps = 156)

