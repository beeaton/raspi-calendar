#!/usr/bin/python

import time
import os
import RPi.GPIO as GPIO #read the GPIO pins
import uinput
import logging
from logging.config import fileConfig

fileConfig('logging.ini')
logger = logging.getLogger()

MonitorOn = False

#testin git push - Making sure it works

#initialize GPIO buttons
ledPrevPin = 4
buttonPrevPin = 17

ledNextPin = 27
buttonNextPin = 22

ledMultiPin = 18
buttonMultiPin = 23

pir_pin = 25

GPIO.setmode(GPIO.BCM)

GPIO.setup(buttonPrevPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)    #Previous button switch
GPIO.setup(ledPrevPin, GPIO.OUT)                                #Previous LED Pin
 
GPIO.setup(buttonNextPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)    #Next button switch
GPIO.setup(ledNextPin, GPIO.OUT)                                #Next LED Pin

GPIO.setup(buttonMultiPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)   #Multi-button switch 
GPIO.setup(ledMultiPin, GPIO.OUT)                               #Multi-button LED Pin

GPIO.setup(pir_pin, GPIO.IN)                                    #Enable PIR to sense montion

device = uinput.Device([
    uinput.KEY_P,
    uinput.KEY_N,
    uinput.KEY_M,
    uinput.KEY_A,
    uinput.KEY_W
	])

#start google calendar with week view
view = 'w'
device.emit_click(uinput.KEY_W)

LEDStartTime = time.time()
MonitorStartTime = time.time()

#Timeout settings for monitor and LED buttons
LEDTimeout = 10
MonitorTimeout = 30

def turnOnLEDButtons():
    logging.debug("   Turning on LED lights on buttons")
    GPIO.output(ledPrevPin, GPIO.HIGH)
    GPIO.output(ledNextPin, GPIO.HIGH)
    GPIO.output(ledMultiPin, GPIO.HIGH)

def turnOffLEDButtons():
    logging.debug("   Turning off LED lights on buttons")
    GPIO.output(ledPrevPin, GPIO.LOW)
    GPIO.output(ledNextPin, GPIO.LOW)
    GPIO.output(ledMultiPin, GPIO.LOW)
    
def turnOffMonitor():
   if MonitorOn:
       logger.info("   Montion not detected and turning off monitor")
       os.system("xscreensaver-command -activate")
    
def turnOnMonitor():
   if MonitorOn == False:
    logger.info("   Montion detected and turning on monitor")
    os.system("xscreensaver-command -deactivate")

#Start Main program
try:
    logger.info("   Starting calendar app")
    turnOnLEDButtons()
    turnOnMonitor()

    while True:
       input_state_back = GPIO.input(buttonPrevPin)
       input_state_forward = GPIO.input(buttonNextPin)
       input_state_multi = GPIO.input(buttonMultiPin)
       input_motion_detected = GPIO.input(pir_pin)
       
       if input_motion_detected:
           MontionDetected = True
           LEDStartTime = time.time()
           MonitorStartTime = time.time()
           turnOnLEDButtons()
           turnOnMonitor()
           MonitorOn = True
       else:
           MontionDetected = False
       
       if time.time()-LEDStartTime < LEDTimeout: #LED will be on for 10 seconds after montion is detected
           logging.debug("   LED is still on "+str(time.time()-LEDStartTime))
       else:
           turnOffLEDButtons()
           logging.debug("   LED is now off")
        
       if time.time()-MonitorStartTime < MonitorTimeout: #Monitor screensaver will stay off for 30 seconds while montion is detected
           logging.debug("   Monitor is still on")
       else:
           logging.debug("   Turning off monitor")
           turnOffMonitor()
           MonitorOn = False
       
       if input_state_back == False:
           logging.info("   Button P Pressed")
           LEDStartTime = time.time()
           device.emit_click(uinput.KEY_P)
           turnOnLEDButtons()
           time.sleep(0.5)
       
       if input_state_forward == False:
           logging.info("   Button N Pressed.")
           LEDStartTime = time.time()
           device.emit_click(uinput.KEY_N)
           time.sleep(0.5)
       
       if input_state_multi == False and input_state_back == False and input_state_forward == False:
           logging.info("   All buttons pressed.  Rebooting System")
           LEDStartTime = time.time()
           GPIO.cleanup()
           os.system("sudo reboot")
           
       if input_state_multi == False:
           if view == 'm':
               device.emit_click(uinput.KEY_W)
               view = 'w'
               logging.debug("   Keypress W")
               time.sleep(0.5)
           if view == 'w':  
               device.emit_click(uinput.KEY_A)
               view = 'a'
               logging.debug("   Keypress A")
               time.sleep(0.5)
           if view == 'a':
               device.emit_click(uinput.KEY_M)
               view = 'm'
               logging.debug("   Keypress M")
               time.sleep(0.5)
except KeyboardInterrupt:  
    logger.info("   Keyboard interrrupted code")
    
finally:
    logger.info("   Cleaning up GPIO ports")
    GPIO.cleanup()
