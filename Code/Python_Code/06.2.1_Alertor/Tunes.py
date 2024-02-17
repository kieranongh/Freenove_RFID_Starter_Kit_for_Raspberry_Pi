#!/usr/bin/env python3
########################################################################
# Filename    : Alertor.py
# Description : Make Alertor with buzzer and button
# Author      : www.freenove.com
# modification: 2019/12/27
########################################################################
import RPi.GPIO as GPIO
import time

buzzerPin = 11    # define the buzzerPin
buttonPin = 12    # define the buttonPin


class Note:
    pitch: str
    length: float

    def __init__(self, pitch: str, length: float):
        self.pitch = pitch
        self.length = length

    def __str__(self):
        return f"{self.pitch} - {self.length}"


def setup():
    global p    
    GPIO.setmode(GPIO.BOARD)         # Use PHYSICAL GPIO Numbering
    GPIO.setup(buzzerPin, GPIO.OUT)   # set RGBLED pins to OUTPUT mode
    GPIO.setup(buttonPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)    # Set buttonPin to INPUT mode, and pull up to HIGH level, 3.3V
    p = GPIO.PWM(buzzerPin, 1) 
    p.start(0);

frere_jacque = [Note("C4", 1), Note("D4", 1), Note("E4", 1), Note("C4", 1),
             Note("C4", 1), Note("D4", 1), Note("E4", 1), Note("C4", 1),
             Note("E4", 1), Note("F4", 1), Note("G4", 2),
             Note("E4", 1), Note("F4", 1), Note("G4", 2),
             Note("G4", 0.5), Note("A4", 0.5), Note("G4", 0.5), Note("F4", 0.5), Note("E4", 1), Note("C4", 1),
             Note("G4", 0.5), Note("A4", 0.5), Note("G4", 0.5), Note("F4", 0.5), Note("E4", 1), Note("C4", 1),
             Note("C4", 1), Note("G3", 1), Note("C4", 2),
             Note("C4", 1), Note("G3", 1), Note("C4", 2),]
    
def loop():
    siren_value = True
    currently_pressed = False
    while True:
        if not currently_pressed and GPIO.input(buttonPin) == GPIO.LOW: # button is pressed
            siren_value = not siren_value
            print(f'siren turned {siren_value}')
            currently_pressed = True

        if GPIO.input(buttonPin) == GPIO.HIGH:
            # print(f'buttonPin high => {GPIO.input(buttonPin)}')
            currently_pressed = False
        
        if siren_value:
            run_tune(frere_jacque)
        else:
            silent()

def arpeggio():
    """
    Simple arpeggios on octaves of A
    """
    p.start(95)
    for x in range(1,5):
        toneVal = 110 * x
        p.ChangeFrequency(toneVal)
        time.sleep(0.5)


def run_tune(notes: list[Note]):
    BASE_TIME = 0.5
    NOTE_DIFF = 0.001

    p.start(95)
    
    for note in notes:
        print(f'note => {note}')
        pitch = getFrequency(note.pitch)

        p.ChangeFrequency(pitch)
        length = (BASE_TIME * note.length) - NOTE_DIFF
        time.sleep(length)
        p.stop()
        time.sleep(NOTE_DIFF)
        p.start(95)

def silent():
    p.stop()
            
def destroy():
    GPIO.output(buzzerPin, GPIO.LOW)     # Turn off buzzer
    p.stop()  # stop PWM
    GPIO.cleanup()                       # Release GPIO resource
  
def getFrequency(note, A4=440):
    notes = ['A', 'A#', 'B', 'C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#']

    octave = int(note[2]) if len(note) == 3 else int(note[1])
        
    keyNumber = notes.index(note[0:-1])
    
    if (keyNumber < 3) :
        keyNumber = keyNumber + 12 + ((octave - 1) * 12) + 1
    else:
        keyNumber = keyNumber + ((octave - 1) * 12) + 1

    return A4 * 2** ((keyNumber- 49) / 12)

if __name__ == '__main__':     # Program entrance
    print ('Program is starting...')
    setup()
    try:
        loop()
    except KeyboardInterrupt:  # Press ctrl-c to end the program.
        pass
    finally:
        destroy()

