#!/usr/bin/python

import time
import RPi.GPIO as GPIO #read the GPIO pins

ledPrevPin = 18

GPIO.setmode(GPIO.BCM)

GPIO.setup(ledPrevPin, GPIO.OUT)                                #Previous LED Pin

GPIO.output(ledPrevPin, GPIO.HIGH)

try:
    while True:
        i = 1
        
except KeyboardInterrupt:  
    GPIO.cleanup()
    
finally:
    GPIO.cleanup()