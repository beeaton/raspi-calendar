#!/usr/bin/python

#First version of the program as a test
#Really cool

import time
import os
import RPi.GPIO as GPIO #read the GPIO pins
import uinput

#initialize GPIO buttons
buttonPrevPin = 17
ledPrevPin = 18
buttonNextPin = 21
ledNextPin = 23
buttonMultiPin = 22
ledMultiPin = 24
pir_pin = 25

GPIO.setmode(GPIO.BCM)

GPIO.setup(buttonPrevPin, GPIO.IN, pull_up_down=GPIO.PUD_UP) 	#Previous button switch
GPIO.setup(ledPrevPin, GPIO.OUT)								#Previous LED Pin
 
GPIO.setup(buttonNextPin, GPIO.IN, pull_up_down=GPIO.PUD_UP) 	#Next button switch
GPIO.setup(ledNextPin, GPIO.OUT)								#Next LED Pin

GPIO.setup(buttonMultiPin, GPIO.IN, pull_up_down=GPIO.PUD_UP) 	#Multi-button switch 
GPIO.setup(ledMultiPin, GPIO.OUT)								#Multi-button LED Pin

GPIO.setup(pir_pin, GPIO.IN)                                    #Enable PIR to sense montion

device = uinput.Device([
    uinput.KEY_P,
    uinput.KEY_N,
	uinput.KEY_F5,
	uinput.KEY_M,
	uinput.KEY_A
	uinput.KEY_W
	])

view = 'm'


LEDButtonOn=True
MontionDetected = True
LEDStartTime = time.time()
MonitorStartTime = time.time()

#Timeout settings for monitor and LED buttons
LEDTimeout = 10
MonitorTimeout = 30


print "Starting calendar app" + " " +time.strftime("%I:%M:%S")
print "Turning on LED buttons and leaving on for " + str(LEDTimeout) +" seconds" + " " + time.strftime("%I:%M:%S")
turnOnLEDButtons()
turnOnMonitor()


def turnOnLEDButtons():
    print "Turning on LED lights on buttons"
    GPIO.output(ledPrevPin, GPIO.HIGH)
    GPIO.output(ledNextPin, GPIO.HIGH)
    GPIO.output(ledMultiPin, GPIO.HIGH)

def turnOffLEDButtons():
    print "Turning off LED lights on buttons"
    GPIO.output(ledPrevPin, GPIO.LOW)
    GPIO.output(ledNextPin, GPIO.LOW)
    GPIO.output(ledMultiPin, GPIO.LOW)
    
def turnOffMonitor():
    print "Montion detected and turning on monitor"
    os.system("xscreensaver-command -activate")

def turnOnMonitor():
    print "Montion not detected and turning off monitor"
    os.system("xscreensaver-command -deactivate")


#Start Main program
try:
   while True:
       input_state_back = GPIO.input(buttonPrevPin)
       input_state_forward = GPIO.input(buttonNextPin)
       input_state_multi = GPIO.input(buttonMultiPin)
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
        
       if time.time()-MonitorStartTime < MonitorTimeout: #Monitor screensaver will stay off for 30 seconds while montion is detected
           print "Monitor is still on"
       else:
           print "Turning off monitor"
           turnOffMonitor()
       
       if input_state_back == False:
           print("Button P Pressed")
           device.emit_click(uinput.KEY_P)
           time.sleep(0.5)
       
       if input_state_forward == False:
           print("Button N Pressed.")
           device.emit_click(uinput.KEY_N)
           time.sleep(0.5)
       
       if input_state_multi == False and input_state_back == False and input_state_forward == False:
           print("All buttons pressed.  Rebooting System"
           os.system("sudo reboot")
           
       if input_state_multi == False:
           if view == 'm':
               device.emit_click(uinput.KEY_W)
               view = 'w'
               print("Keypress W")
               time.sleep(0.5)
           if view == 'w':
               device.emit_click(uinput.KEY_A)
               view = 'a'
               print("Keypress A")
               time.sleep(0.5)
           if view == 'a':
               device.emit_click(uinput.KEY_M)
               view = 'm'
               print("Keypress M")
               time.sleep(0.5)
except KeyboardInterrupt:  
    print "Keyboard interrrupted code"
    
#except Exception, e:
#    print "Other exception"
    
finally:
    print "Cleaning up GPIO ports"
    GPIO.cleanup()
    