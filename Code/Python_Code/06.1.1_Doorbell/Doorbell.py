#!/usr/bin/env python3
########################################################################
# Filename    : Doorbell.py
# Description : Make doorbell with buzzer and button
# auther      : www.freenove.com
# modification: 2019/12/28
########################################################################
import RPi.GPIO as GPIO

buzzerPin = 11    # define buzzerPin
buttonPin = 12    # define buttonPin

def setup():
    GPIO.setmode(GPIO.BOARD)        # use PHYSICAL GPIO Numbering
    GPIO.setup(buzzerPin, GPIO.OUT)   # set buzzerPin to OUTPUT mode
    GPIO.setup(buttonPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)    # set buttonPin to PULL UP INPUT mode

def loop():
    buzz_value = GPIO.LOW
    already_switched = False

    while True:
        if not already_switched and GPIO.input(buttonPin) == GPIO.LOW: # if button is pressed
            if buzz_value == GPIO.HIGH:
                buzz_value = GPIO.LOW
            else:
                buzz_value = GPIO.HIGH
            print(f'buzzer turned {buzz_value}')
            GPIO.output(buzzerPin, buzz_value) # set buzzer value
            already_switched = True
        if GPIO.input(buttonPin) == GPIO.HIGH:
            already_switched = False


def destroy():
    GPIO.output(buzzerPin, GPIO.LOW) # set buzzer value
    GPIO.cleanup()                     # Release all GPIO

if __name__ == '__main__':     # Program entrance
    print ('Program is starting...')
    setup()
    try:
        loop()
    except KeyboardInterrupt:  # Press ctrl-c to end the program.
        destroy()

