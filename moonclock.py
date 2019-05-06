#!/usr/bin/python

from Adafruit_MotorHAT import Adafruit_MotorHAT, Adafruit_StepperMotor
import atexit
from datetime import *
import math
import time

ROTATION_CONSTANT = 3.0 + 1.0/3.0

# rotate the motor by a certain number of steps
def move_the_motor(steps):
    moon_stepper.step(int(steps * ROTATION_CONSTANT + 0.5), Adafruit_MotorHAT.FORWARD, Adafruit_MotorHAT.SINGLE)

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

# clean up function for safe termination
def turnOffMotors():
    mh.getMotor(1).run(Adafruit_MotorHAT.RELEASE)
    mh.getMotor(2).run(Adafruit_MotorHAT.RELEASE)
    mh.getMotor(3).run(Adafruit_MotorHAT.RELEASE)
    mh.getMotor(4).run(Adafruit_MotorHAT.RELEASE)

# register clean up function
atexit.register(turnOffMotors)


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

def test_phase(i):
    date = datetime.now();
    day = i
    month = date.month
    year = date.year
    return moon_phase(day, month, year)

while True:
#for i in range(27):
#    new_phase = test_phase(i + 4)
    mh = Adafruit_MotorHAT()
    # gain control of stepper and set its speed
    moon_stepper = mh.getStepper(200,1)
    moon_stepper.setSpeed(3)
    new_phase = get_new_phase()
    update_phase(current_phase, new_phase)
    print("loop!")
    current_phase = new_phase
    time.sleep(3)
    turnOffMotors()
    time.sleep(900) #wait 15 minutes for next update
