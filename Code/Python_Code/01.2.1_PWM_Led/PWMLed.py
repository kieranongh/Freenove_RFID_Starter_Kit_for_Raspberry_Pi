# Source: https://sourceforge.net/p/raspberry-gpio-python/wiki/PWM/

import time
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BOARD)
GPIO.setup(12, GPIO.OUT)

p = GPIO.PWM(12, 50)  # channel=12 frequency=50Hz
p.start(0)

STEP = 0.05
try:
    while True:
        for dc in range(0, 101, 1):
            p.ChangeDutyCycle(dc)
            time.sleep(STEP)
        for dc in range(100, -1, -1):
            p.ChangeDutyCycle(dc)
            time.sleep(STEP)
except KeyboardInterrupt:
    pass
p.stop()
GPIO.cleanup()