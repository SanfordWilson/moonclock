from datetime import *
import math

def move_the_motor(steps):
    return 1*steps

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

while True:

    cur_date = datetime.now()
    day = cur_date.day
    month = cur_date.month
    year = cur_date.year
    phase = moon_phase(day, month, year)
    print("The current date is %s-%s" % (month, day))

    if phase > current_phase:
        move_the_motor(phase - current_phase)
    elif phase < current_phase:
        move_the_motor(phase+30 - current_phase

    current_phase = phase
    
    time.sleep(900) #wait 15 minutes for next update
