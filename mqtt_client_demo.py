import paho.mqtt.client as mqtt

import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(18,GPIO.OUT)


def on_connect(client,userdata,flags,rc):
    print("Connected with result code"+str(rc))
    
    client.subscribe("CoreElectronics/test")
    client.subscribe("CoreElectronics/topic")



def on_message(client,userdata,msg):
    print(msg.topic+" "+str(msg.payload))
    
    if msg.payload == "On":
        print("turn the led on")
        GPIO.output(18,GPIO.HIGH)
        time.sleep(1)
        
    if msg.payload == "Off":
        print("Turning the led off")
        GPIO.output(18,GPIO.LOW)
        time.sleep(1)
    
    
client=mqtt.Client()
client.on_connect=on_connect
client.on_message=on_message

client.connect('test.mosquitto.org',1883,60)

client.loop_forever()
