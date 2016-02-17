#!/usr/bin/python

import time
import os
import RPi.GPIO as GPIO #read the GPIO pins

GPIO.setmode(GPIO.BCM)

pir_pin = 25
ledPrevPin = 18
buttonPrevPin = 17

GPIO.setup(pir_pin, GPIO.IN)                                    #Enable PIR to sense montion

GPIO.setup(ledPrevPin, GPIO.OUT)                                #Previous LED Pin
GPIO.output(ledPrevPin, GPIO.HIGH)

GPIO.setup(buttonPrevPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)    #Previous button switch

LEDStartTime = time.time()
MonitorStartTime = time.time()


#Timeout settings for monitor and LED buttons
LEDTimeout = 10
MonitorTimeout = 30

#Start Main program
try:
   while True:
       input_motion_detected = GPIO.input(pir_pin)
       input_state_back = GPIO.input(buttonPrevPin)
       
       if input_motion_detected:
           MontionDetected = True
           LEDStartTime = time.time()
           MonitorStartTime = time.time()
       else:
           MontionDetected = False
           
       if time.time()-LEDStartTime < LEDTimeout: #LED will be on for 10 seconds after montion is detected
            print "LED is on "+str(time.time()-LEDStartTime) 
            GPIO.output(ledPrevPin, GPIO.HIGH)
       else:
            GPIO.output(ledPrevPin, GPIO.LOW)
            
       if time.time()-MonitorStartTime < MonitorTimeout: #Monitor screensaver will stay off for 30 seconds while montion is detected
           print "Monitor is still on " +str(time.time()-MonitorStartTime) 
       else:
           print "Turning off monitor"
       
       if input_state_back == False:
           print("   Button P Pressed")
           LEDStartTime = time.time()
           time.sleep(0.5)
           
       time.sleep(1)

except KeyboardInterrupt:  
    print "Keyboard interrrupted code"

finally:
    print "Cleaning up GPIO ports"
    GPIO.cleanup()
    