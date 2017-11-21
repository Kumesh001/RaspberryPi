import time
import RPi.GPIO as GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(17,GPIO.OUT)
GPIO.setup(2,GPIO.OUT)

GPIO.output(17,False)

while True:
    print("On")
    GPIO.output(17,True)
    GPIO.output(2,GPIO.HIGH)
    time.sleep(5)
    print("Off")
    GPIO.output(17,False)
    GPIO.output(2,GPIO.LOW)
    time.sleep(5)
    
GPIO.cleanup()