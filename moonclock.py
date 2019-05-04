#!/usr/bin/python

from Adafruit_MotorHAT import Adafruit_MotorHAT, Adafruit_StepperMotor
import atexit
from datetime import *
import math
import time

# rotate the motor by a certain number of steps
def move_the_motor(steps):
    moon_stepper.step(int(steps * 6.66 + 0.5), Adafruit_MotorHAT.FORWARD, Adafruit_MotorHAT.SINGLE)

current_phase = 0

def moon_phase(mDay, mMonth, mYear):
    r = mYear % 100
    r %= 19
    if r > 9:
        r -= 19
    r = ((r * 11) % 30) + mMonth + mDay
    if mMonth < 3:
        r += 2
    s = 4 if mYear < 2000 else 8.3
    r -= s
    r = (math.floor(r + 0.5) % 30)
    return r + 30 if r < 0 else r

output_list = []

mh = Adafruit_MotorHAT()

# clean up function for safe termination
def turnOffMotors():
    mh.getMotor(1).run(Adafruit_MotorHAT.RELEASE)
    mh.getMotor(2).run(Adafruit_MotorHAT.RELEASE)
    mh.getMotor(3).run(Adafruit_MotorHAT.RELEASE)
    mh.getMotor(4).run(Adafruit_MotorHAT.RELEASE)

# register clean up function
atexit.register(turnOffMotors)

# gain control of stepper and set its speed
moon_stepper = mh.getStepper(200,1)
moon_stepper.setSpeed(3)

# determine how many steps to move and move motor
def update_phase(current_phase, new_phase):
    if new_phase == current_phase:
        return
    steps = new_phase - current_phase
    steps = steps + 30 if steps < 0 else steps
    move_the_motor(steps)

# get the phase of the current day
def get_new_phase():
    date = datetime.now()
    day = date.day
    month = date.month
    year = date.year
    return moon_phase(day, month, year)
    
while True:
    new_phase = get_new_phase()
    update_phase(current_phase, new_phase)
    print("loop!")
    current_phase = new_phase
    time.sleep(60)

#wait 15 minutes for next update
