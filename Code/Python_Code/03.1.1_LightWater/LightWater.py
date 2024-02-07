#!/usr/bin/env python3
########################################################################
# Filename    : LightWater.py
# Description : Use LEDBar Graph(10 LED) 
# auther      : www.freenove.com
# modification: 2019/12/28
########################################################################
import RPi.GPIO as GPIO
import time
from enum import Enum
import random

ledPins = [11, 12, 13, 15, 16, 18, 22, 3, 5, 24]

class LightStyle(Enum):
    FLOW_AND_HOVER = "FLOW_AND_HOVER"
    FLOW = "FLOW"
    RANDOM_SINGLE = "RANDOM_SINGLE"
    SAMPLE = "SAMPLE"
    FLASH_ALL = "FLASH_ALL"
    LOADING = "LOADING"
    GAIN = "GAIN"
    FOXTROT = "FOXTROT"
    CROSS_HATCH = "CROSS_HATCH"
    STACK_UP = "STACK_UP"
    PEW_PEW = "PEW_PEW"
    RANDOM_THIRDS = "RANDOM_THIRDS"
    SAMPLE_THIRDS = "SAMPLE_THIRDS"
    SAMPLE_TWO_CHOICES = "SAMPLE_TWO_CHOICES"
    RANDOM_CHORDS = "RANDOM_CHORDS"
    CONVERGE = "CONVERGE"
    CONVERGE_FILL = "CONVERGE_FILL"
    DIVERGE = "DIVERGE"
    DIVERGE_FILL = "DIVERGE_FILL"

STEP = 0.1
DOUBLE_STEP = STEP * 2
STYLE = LightStyle.DIVERGE_FILL
RANDOMISE_STYLES = True

def setup():    
    GPIO.setmode(GPIO.BOARD)        # use PHYSICAL GPIO Numbering
    GPIO.setup(ledPins, GPIO.OUT)   # set all ledPins to OUTPUT mode
    GPIO.output(ledPins, GPIO.HIGH) # make all ledPins output HIGH level, turn off all led

def loop(style, randomise = False):
    while True:
        if randomise:
            style = get_random_style()
            print(f'style => {style}')
        if style == LightStyle.FLOW_AND_HOVER:
            flow_and_hover()
        elif style == LightStyle.FLOW:
            flow()
        elif style == LightStyle.RANDOM_SINGLE:
            random_single()
        elif style == LightStyle.SAMPLE:
            sample()
        elif style == LightStyle.FLASH_ALL:
            flash_all()
        elif style == LightStyle.LOADING:
            loading()
        elif style == LightStyle.GAIN:
            gain_imitation()
        elif style == LightStyle.FOXTROT:
            foxtrot()
        elif style == LightStyle.CROSS_HATCH:
            cross_hatch()
        elif style == LightStyle.STACK_UP:
            stack_up()
        elif style == LightStyle.PEW_PEW:
            pew_pew()
        elif style == LightStyle.RANDOM_THIRDS:
            random_thirds()
        elif style == LightStyle.SAMPLE_THIRDS:
            sample_thirds()
        elif style == LightStyle.SAMPLE_TWO_CHOICES:
            sample_two_choices()
        elif style == LightStyle.RANDOM_CHORDS:
            random_chords()
        elif style == LightStyle.CONVERGE:
            converge()
        elif style == LightStyle.CONVERGE_FILL:
            converge_fill()
        elif style == LightStyle.DIVERGE:
            diverge()
        elif style == LightStyle.DIVERGE_FILL:
            diverge_fill()

        clear()


def destroy():
    GPIO.cleanup()                     # Release all GPIO


def get_random_style():
    return random.choice(list(LightStyle))

def flow_and_hover():
    """
    The OG - lights LEDs individually in one then the other direction.
    Hits on the ends twice, hence looking like it hovers
    """
    for pin in ledPins:     # make led(on) move from left to right
        GPIO.output(pin, GPIO.LOW)
        time.sleep(STEP)
        GPIO.output(pin, GPIO.HIGH)
    for pin in ledPins[::-1]:       # make led(on) move from right to left
        GPIO.output(pin, GPIO.LOW)
        time.sleep(STEP)
        GPIO.output(pin, GPIO.HIGH)

def flow():
    """
    A twist on The OG - lights LEDs individually in one then the other direction.
    Only flashes the end once, so it looks like it "bounces" off the ends
    """
    END = -1
    for pin in ledPins[:END]:     # make led(on) move from left to right
        GPIO.output(pin, GPIO.LOW)
        time.sleep(STEP)
        GPIO.output(pin, GPIO.HIGH)
    for pin in ledPins[::-1][:END]:       # make led(on) move from right to left
        GPIO.output(pin, GPIO.LOW)
        time.sleep(STEP)
        GPIO.output(pin, GPIO.HIGH)

def random_single():
    """
    Go random a bunch of times
    """
    choices = random.choices(ledPins, k=len(ledPins))
    print(f'choices => {list(map(lookup_index, choices))}')
    for pin in choices:
        GPIO.output(pin, GPIO.LOW)
        time.sleep(STEP)
        GPIO.output(pin, GPIO.HIGH)

def sample():
    """
    Pick each pin once, in a random sampling
    """
    seq = random.sample(ledPins, k=len(ledPins))
    print(f'indices of seq => {list(map(lookup_index, seq))}')
    for pin in seq:
        GPIO.output(pin, GPIO.LOW)  
        time.sleep(STEP)
        GPIO.output(pin, GPIO.HIGH)

def loading():
    """
    Looks like a side scrolling "loading" animation
    """
    for pin in ledPins:
        GPIO.output(pin, GPIO.LOW)  
        time.sleep(STEP)
    for pin in ledPins:
        GPIO.output(pin, GPIO.HIGH)
        time.sleep(STEP)

def flash_all():
    for _ in range(len(ledPins) // 2):
        for pin in ledPins:
            GPIO.output(pin, GPIO.LOW)  
        time.sleep(DOUBLE_STEP)
        for pin in ledPins:
            GPIO.output(pin, GPIO.HIGH)
        time.sleep(DOUBLE_STEP)

def gain_imitation():
    """
    Act like the input/gain symbol on a sound desk
    """
    for pin in ledPins:
        GPIO.output(pin, GPIO.LOW)  
        time.sleep(STEP)
    for pin in ledPins[::-1]:
        GPIO.output(pin, GPIO.HIGH)
        time.sleep(STEP)

def foxtrot():
    """
    Two steps forward, one back, til full
    0 1 0 - 1 2 1 - 2 3 2 - ... - 7 8 7 - 8 9
    """
    FORWARD = 2
    BACK = 1
    for i in range(len(ledPins) - 1):
        for j in range(i, i + FORWARD + BACK):
            index = j
            if j == i + FORWARD:
                index = j - BACK
                pin = ledPins[index]
                GPIO.output(pin, GPIO.HIGH)
            else:
                pin = ledPins[index]
                GPIO.output(pin, GPIO.LOW)
            time.sleep(STEP)
            
            # If we hit the end, don't go back
            if index == len(ledPins) - 1:
                return

def cross_hatch():
    """
    Alternate indices
    """
    for _ in range(len(ledPins) // 2):
        for i in range(len(ledPins)):
            pin = ledPins[i]
            if i % 2 == 0:
                GPIO.output(pin, GPIO.LOW)
            else:
                GPIO.output(pin, GPIO.HIGH)
        time.sleep(DOUBLE_STEP)
        for i in range(len(ledPins)):
            pin = ledPins[i]
            if i % 2 == 1:
                GPIO.output(pin, GPIO.LOW)
            else:
                GPIO.output(pin, GPIO.HIGH)
        time.sleep(DOUBLE_STEP)

def random_thirds():
    """
    Randomise thirds (skip one)
    Should be within valid range of upper and lower bounds
    """
    choices = random.choices(range(len(ledPins) - 2), k=len(ledPins))
    print(f'choices => {list( choices)}')
    for index in choices:
        one = ledPins[index]
        two = ledPins[index + 2]
        GPIO.output(one, GPIO.LOW)  
        GPIO.output(two, GPIO.LOW)  
        time.sleep(STEP)
        GPIO.output(one, GPIO.HIGH)
        GPIO.output(two, GPIO.HIGH)

def sample_thirds():
    """
    Random sampling of thirds (skip one)
    Pick each third only once
    Should be within valid range of upper and lower bounds
    """
    seq = random.sample(range(len(ledPins) - 2), k=len(ledPins) - 2)
    print(f'seq => {list(map(lambda i: f"{i}:{i+2}", seq))}')
    for index in seq:
        one = ledPins[index]
        two = ledPins[index + 2]
        GPIO.output(one, GPIO.LOW)  
        GPIO.output(two, GPIO.LOW)  
        time.sleep(STEP)
        GPIO.output(one, GPIO.HIGH)
        GPIO.output(two, GPIO.HIGH)


def sample_two_choices():
    """
    Randomly pick two a bunch of times
    """
    samples = []
    for _ in range(len(ledPins)):
        samples.append(random.sample(ledPins, k=2))

    print(f'samples => {list(map(lambda pair: list(map(lookup_index, pair)), samples))}')
    
    for pair in samples:
        for pin in pair:
            GPIO.output(pin, GPIO.LOW)

        time.sleep(STEP)

        for pin in pair:
            GPIO.output(pin, GPIO.HIGH)


def stack_up():
    """
    looks like falling from top and stacking up
    """
    for i in range(len(ledPins)):
        for j in range(len(ledPins) - i):
            index = j
            pin = ledPins[index]
            GPIO.output(pin, GPIO.LOW)
            time.sleep(STEP)
            if index != len(ledPins) - i - 1:
                GPIO.output(pin, GPIO.HIGH)

def pew_pew():
    """
    Two quick iterations, then a pause.
    Like a couple of laser bursts.
    Gap is the num of pins between shots.
    """
    GAP = 3
    for _ in range(2):
        for _ in range(2):
            for i in range(len(ledPins) + GAP):
                pin1 = None
                pin2 = None
                if i < len(ledPins):
                    pin1 = ledPins[i]
                    GPIO.output(pin1, GPIO.LOW)
                if i >= GAP:
                    pin2 = ledPins[i - GAP]
                    GPIO.output(pin2, GPIO.LOW)
                time.sleep(STEP / 4)
                if pin1:
                    GPIO.output(pin1, GPIO.HIGH)
                if pin2:
                    GPIO.output(pin2, GPIO.HIGH)
        time.sleep(DOUBLE_STEP * 2)

def random_chords():
    """
    Randomly sample a random k amount (2, 4) a bunch of times
    """
    samples = []
    for _ in range(len(ledPins)):
        k = random.randint(2, 4)
        samples.append(random.sample(ledPins, k=k))

    print(f'samples => {list(map(lambda sampling: len(sampling), samples))}')
    
    for sampling in samples:
        for pin in sampling:
            GPIO.output(pin, GPIO.LOW)

        time.sleep(STEP)

        for pin in sampling:
            GPIO.output(pin, GPIO.HIGH)

def converge_fill():
    """
    out to in and stay on
    """
    for _ in range(2):
        time.sleep(STEP)
        for i in range(len(ledPins) // 2):
            left = ledPins[i]
            right = ledPins[-i - 1]
            GPIO.output(left, GPIO.LOW)
            GPIO.output(right, GPIO.LOW)
            time.sleep(STEP)

        for pin in ledPins:
            GPIO.output(pin, GPIO.HIGH)

def diverge_fill():
    """
    in to out and stay on
    """
    for _ in range(2):
        half = (len(ledPins) // 2) - 1
        time.sleep(STEP)
        for i in range(len(ledPins) // 2):
            left = ledPins[half - i]
            right = ledPins[half + i + 1]
            GPIO.output(left, GPIO.LOW)
            GPIO.output(right, GPIO.LOW)
            time.sleep(STEP)
        
        for pin in ledPins:
            GPIO.output(pin, GPIO.HIGH)

def converge():
    """
    out to in
    """
    for _ in range(2):
        time.sleep(STEP)
        for i in range(len(ledPins) // 2):
            left = ledPins[i]
            right = ledPins[-i - 1]
            GPIO.output(left, GPIO.LOW)
            GPIO.output(right, GPIO.LOW)
            time.sleep(STEP)
            GPIO.output(left, GPIO.HIGH)
            GPIO.output(right, GPIO.HIGH)

def diverge():
    """
    in to out
    """
    for _ in range(2):
        half = (len(ledPins) // 2) - 1
        time.sleep(STEP)
        for i in range(len(ledPins) // 2):
            left = ledPins[half - i]
            right = ledPins[half + i + 1]
            GPIO.output(left, GPIO.LOW)
            GPIO.output(right, GPIO.LOW)
            time.sleep(STEP)
            GPIO.output(left, GPIO.HIGH)
            GPIO.output(right, GPIO.HIGH)

# UTIL
def lookup_index(pin):
    return ledPins.index(pin)

def clear():
    for pin in ledPins:
        GPIO.output(pin, GPIO.HIGH)

if __name__ == '__main__':     # Program entrance
    print ('Program is starting...')
    setup()
    try:
        loop(STYLE, RANDOMISE_STYLES)
        destroy()
    except KeyboardInterrupt:  # Press ctrl-c to end the program.
        pass
    finally:
        destroy()
