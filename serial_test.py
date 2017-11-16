import serial
import matplotlib.pyplot as plt

ser = serial.Serial('/dev/ttyACM0',9600)
power1=[]
current1=[]
power2=[]
current2=[]

while True:
    read_serial=ser.readline()
    
    dataArray=read_serial.split(',')
    
    current1.append(float(dataArray[0]))
    power1.append(float(dataArray[1]))
    current2.append(float(dataArray[2]))
    power2.append(float(dataArray[3]))
    
    '''for eachLine in dataArray:
        if len(dataArray)>=1:
            x,y,time=eachLine.split(',')
            
    
    print(power_axis)
    print(current_axis)
    print(time_axis)'''
    print(current1)
    print(power1)
    print(current2)
    print(power2)