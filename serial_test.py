import serial
import matplotlib.pyplot as plt

ser = serial.Serial('/dev/ttyACM0',9600)
power_axis=[]
current_axis=[]
time_axis=[]

while True:
    read_serial=ser.readline()
    dataArray=read_serial.split(',')
    current_axis.append(dataArray[0])
    power_axis.append(dataArray[1])
    time_axis.append(dataArray[2])
    
    '''for eachLine in dataArray:
        if len(dataArray)>=1:
            x,y,time=eachLine.split(',')
            
    
    print(power_axis)
    print(current_axis)
    print(time_axis)'''
    print(power_axis)
    print(current_axis)
    print(time_axis)