'''import os
import sys
import AWSIoTPythonSDK
sys.path.insert(0,os.path.dirname(AWSIoTPythonSDK.__file__))
'''
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import RPi.GPIO as GPIO
import time
import logging
import argparse
import json
import serial
import requests

ser= serial.Serial('/dev/ttyACM0',9600)
ser.flushInput()
ser.write('F')
'''
GPIO.setmode(GPIO.BCM)

Relay1=17
led=2

state=0
GPIO.setwarnings(False)
GPIO.setup(Relay1,GPIO.OUT)
GPIO.setup(led,GPIO.OUT)
GPIO.output(led,GPIO.LOW)
    
GPIO.output(Relay1,GPIO.LOW)'''

# Custom MQTT message callback
def customCallback(client, userdata, message):
    print("Received a new message: ")
    print(message.payload)
    print("from topic: ")
    print(message.topic)
    print("--------------\n\n")

print("I m here")
# Read in command-line parameters
parser = argparse.ArgumentParser()
parser.add_argument("-e", "--endpoint", action="store", required=True, dest="host", help="Your AWS IoT custom endpoint")
parser.add_argument("-r", "--rootCA", action="store", required=True, dest="rootCAPath", help="Root CA file path")
parser.add_argument("-c", "--cert", action="store", dest="certificatePath", help="Certificate file path")
parser.add_argument("-k", "--key", action="store", dest="privateKeyPath", help="Private key file path")
parser.add_argument("-w", "--websocket", action="store_true", dest="useWebsocket", default=False,
                    help="Use MQTT over WebSocket")
parser.add_argument("-id", "--clientId", action="store", dest="clientId", default="basicPubSub",
                    help="Targeted client id")
parser.add_argument("-t", "--topic", action="store", dest="topic", default="sdk/test/Python", help="Targeted topic")

print("Now parsing the argument")

args = parser.parse_args()
host = args.host
rootCAPath = args.rootCAPath
certificatePath = args.certificatePath
privateKeyPath = args.privateKeyPath
useWebsocket = args.useWebsocket
clientId = args.clientId
topic = args.topic

if args.useWebsocket and args.certificatePath and args.privateKeyPath:
    parser.error("X.509 cert authentication and WebSocket are mutual exclusive. Please pick one.")
    exit(2)

if not args.useWebsocket and (not args.certificatePath or not args.privateKeyPath):
    parser.error("Missing credentials for authentication.")
    exit(2)

# Configure logging
logger = logging.getLogger("AWSIoTPythonSDK.core")
logger.setLevel(logging.DEBUG)
streamHandler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
streamHandler.setFormatter(formatter)
logger.addHandler(streamHandler)

# Init AWSIoTMQTTClient
print("Now Initialsing the Mqtt client")

myAWSIoTMQTTClient = None
if useWebsocket:
    myAWSIoTMQTTClient = AWSIoTMQTTClient(clientId, useWebsocket=True)
    myAWSIoTMQTTClient.configureEndpoint(host, 443)
    myAWSIoTMQTTClient.configureCredentials(rootCAPath)
else:
    myAWSIoTMQTTClient = AWSIoTMQTTClient(clientId)
    myAWSIoTMQTTClient.configureEndpoint(host, 8883)
    myAWSIoTMQTTClient.configureCredentials(rootCAPath, privateKeyPath, certificatePath)

# AWSIoTMQTTClient connection configuration
myAWSIoTMQTTClient.configureAutoReconnectBackoffTime(1, 32, 20)
myAWSIoTMQTTClient.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
myAWSIoTMQTTClient.configureDrainingFrequency(2)  # Draining: 2 Hz
myAWSIoTMQTTClient.configureConnectDisconnectTimeout(10)  # 10 sec
myAWSIoTMQTTClient.configureMQTTOperationTimeout(5)  # 5 sec

# Connect and subscribe to AWS IoT
print("Connecting the deivce now")

myAWSIoTMQTTClient.connect()
myAWSIoTMQTTClient.subscribe(topic, 1, customCallback)
time.sleep(2)

# Publish to the same topic in a loop forever
print("Welcome to the while loop")

def bubbleSort(alist):
    for passnum in range(len(alist)-1,0,-1):
        for i in range(passnum):
            if alist[i]>alist[i+1]:
                temp=alist[i]
                alist[i]=alist[i+1]
                alist[i+1]=temp
timer=0
loopCount = 0
previousState=0
countState=0
currentState=""
while True:
    state=requests.get('https://ub4qge1nh1.execute-api.us-west-2.amazonaws.com/prod/TriggerFunction')
    response=json.loads(state.content)
    count=response['Count']
    
    if countState!=count:
        dates=[]
        countState=count
        for line in response['Items']:
            dates.append(line['Date'])
            
        bubbleSort(dates)
        
        for line in response['Items']:
            if line['Date']==dates[-1]:
                currentState=line['Result']
    print("currentState is")
    print(currentState)
    
    if currentState=="ON":
        print("Socket is ON")
        ser.write('O')
        time.sleep(0.0002)
        read_serial=ser.readline()
        dataArray=read_serial.split(',')
        print(dataArray)
        
        current = dataArray[0]
        voltage  =dataArray[1]
        power   = dataArray[2]
        energy  = dataArray[3]
        timeValue    = dataArray[4]
   
        message={
            "Current":current,
            "Power":power,
            "Energy":energy,
            "Voltage":voltage,
            "Time":timeValue
        }
        print("Publishing the message")
        myAWSIoTMQTTClient.publish(topic,json.dumps(message),1)
    else:
        ser.write('F')
        time.sleep(0.0002)
        timeValue2    = dataArray[4]

        message={
            "Current":0,
            "Power":0,
            "Energy":0,
            "Voltage":230,
            "Time":timeValue2
        }
        print("Publishing the message")
        myAWSIoTMQTTClient.publish(topic,json.dumps(message),1)
        print("Socket is switched off")
    
    loopCount += 1
    print("Now going to sleep")
    time.sleep(0.003)
    timer +=3
GPIO.cleanup()