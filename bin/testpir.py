#!/usr/bin/python

import time
import os
import RPi.GPIO as GPIO #read the GPIO pins


pir_pin = 25

GPIO.setup(pir_pin, GPIO.IN)                                    #Enable PIR to sense montion

LEDStartTime = time.time()
MonitorStartTime = time.time()


#Timeout settings for monitor and LED buttons
LEDTimeout = 10
MonitorTimeout = 30

#Start Main program
try:
   while True:
       input_motion_detected = GPIO.input(pir_pin)
       
       if input_motion_detected:
           MontionDetected = True
           LEDStartTime = time.time()
           MonitorStartTime = time.time()
       else:
           MontionDetected = False
           
       if time.time()-LEDStartTime < LEDTimeout: #LED will be on for 10 seconds after montion is detected
            print "LED is still on "+str(time.time()-LEDStartTime) 
       else:
            print "LED is now off"

except KeyboardInterrupt:  
    print "Keyboard interrrupted code"

finally:
    print "Cleaning up GPIO ports"
    GPIO.cleanup()
    