import serial
import time

ser = serial.Serial('/dev/ttyACM0',9600)
ser.flushInput()
while True:
    print("Hello")
    ser.write('O')
    time.sleep(2)
    print("Bye")
    ser.write('F')
    time.sleep(3)
    
print("End")