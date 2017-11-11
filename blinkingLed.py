import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

TRIG=15
ECHO=14

print("Distance measured In Process")

GPIO.setwarnings(False)
GPIO.setup(18,GPIO.OUT)
GPIO.setup(TRIG,GPIO.OUT)
GPIO.setup(ECHO,GPIO.IN)


GPIO.output(TRIG,False)
print("Waiting for the sensor to sense the data")

while True:
    GPIO.output(TRIG,True)
    time.sleep(0.0001)
    GPIO.output(TRIG,False)
    while GPIO.input(ECHO)==0:
        pulse_start=time.time()
    while GPIO.input(ECHO)==1:
         pulse_end=time.time()
    pulse_duration=pulse_end-pulse_start
    distance=pulse_duration*17150
    distance=round(distance,2)
    print("Distance is:",distance,"cm")

    if distance > 15:
        print("Turn the led on")
        GPIO.output(18,GPIO.HIGH)
        time.sleep(2)
    else:
        print("Turn the led Off")
        GPIO.output(18,GPIO.LOW)
        time.sleep(2)
    
    if distance > 150:
        print("Reach out of bound")
        break;

GPIO.cleanup()