import RPi.GPIO as GPIO 
from time import sleep, time

GPIO.setmode(GPIO.BCM)  

#Set up GPIO pins
GPIO.setup(21, GPIO.OUT)
GPIO.setup(20, GPIO.OUT)
GPIO.setup(16, GPIO.OUT)

try: 
    #trying to send 00 to Arduino
    GPIO.output(20, 0)
    GPIO.output(21, 0)

except KeyboardInterrupt:
    GPIO.cleanup()

def cleaning_done():
    while(True):
         if (GPIO.Input(20) == GPIO.HIGH):
             
             #Function to call inspection
             

             pass

def start_cleaning():
    while(True):
        GPIO.output(21, 1)
        if (GPIO.Input(20) == GPIO.HIGH):

            #Probably call LCD to change status
            pass
        
#RPI to send Arduino 

def stop_cleaning():
    GPIO.output(16, 1)
    time.sleep(1)

    #Reset GUI to first screen
    

